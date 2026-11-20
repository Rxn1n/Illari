#!/usr/bin/env python3
"""ILLARI: visualize public NASA GIBS NISAR false-color images for a CMR-verified pair.

A GIBS daily image is a *mosaic*, not necessarily a single CMR GCOV granule.
This produces an RGB change visualization, NOT calibrated SAR, flood extent or fire proof.
"""
import datetime as dt
import io
import json
import math
import pathlib
import urllib.parse
import urllib.request
from PIL import Image, ImageChops, ImageDraw, ImageFont

INPUT = pathlib.Path("reports/nisar_guayaquil_cmr.json")
OUT = pathlib.Path("reports/nisar_gibs_preview")
LAYER = "NISAR_L2_Geocoded_Polarimetric_Covariance"
WMS = "https://gibs.earthdata.nasa.gov/wms/epsg3857/best/wms.cgi"
BBOX = (-80.05, -2.33, -79.75, -1.95)  # west, south, east, north
WIDTH = 480

def merc(lat, lon):
    a=6378137.0
    return (a*math.radians(lon), a*math.log(math.tan(math.pi/4+math.radians(lat)/2)))

def map_url(date, width=WIDTH):
    west,south,east,north=BBOX
    x0,y0=merc(south,west); x1,y1=merc(north,east)
    height=round(width*(y1-y0)/(x1-x0))
    params={"SERVICE":"WMS","REQUEST":"GetMap","VERSION":"1.3.0",
        "LAYERS":LAYER,"STYLES":"","FORMAT":"image/png","TRANSPARENT":"TRUE",
        "CRS":"EPSG:3857","BBOX":",".join(f"{x:.1f}" for x in (x0,y0,x1,y1)),
        "WIDTH":width,"HEIGHT":height,"TIME":date}
    return WMS+"?"+urllib.parse.urlencode(params),height

def fetch(date):
    url,_=map_url(date)
    req=urllib.request.Request(url,headers={"User-Agent":"ILLARI case study (NASA data attribution)","Accept":"image/png"})
    with urllib.request.urlopen(req,timeout=50) as r:
        data=r.read()
        typ=r.headers.get("Content-Type","")
    if not typ.startswith("image/"):
        raise RuntimeError("NASA GIBS returned "+typ+": "+data[:350].decode("utf-8","replace"))
    image=Image.open(io.BytesIO(data)).convert("RGBA")
    alpha=image.getchannel("A")
    valid=sum(v>0 for v in alpha.getdata())
    if valid < image.width*image.height*0.12:
        raise RuntimeError(f"Very low GIBS coverage on {date}: {valid} pixels")
    return image,url,valid/(image.width*image.height)

def summarize_before_after(before,after):
    p=list(before.getdata());q=list(after.getdata());valid=0;change=0
    diff=Image.new("RGBA",before.size,(0,0,0,0))
    dpx=[]
    for a,b in zip(p,q):
        if a[3]==0 or b[3]==0:
            dpx.append((0,0,0,0));continue
        if sum(a[:3])==0 or sum(b[:3])==0:
            dpx.append((0,0,0,0));continue
        valid+=1
        delta=sum(abs(a[i]-b[i]) for i in range(3))/3
        if delta>=35:change+=1
        v=int(min(255,delta*2))
        dpx.append((v,int(v*.4),0,225))
    diff.putdata(dpx)
    return diff,valid,change

def main():
    info=json.loads(INPUT.read_text(encoding="utf-8"))
    pair=info.get("par")
    OUT.mkdir(parents=True,exist_ok=True)
    report={"source":"NASA GIBS daily RGB mosaic, confirmed by CMR granule dates only",
        "status":"NO_DATA","note":"False-color 8-bit imagery; no calibrated SAR values, no flood extent.",
        "granule_ids":[p["id"] for p in pair] if pair else [],
        "event_2026_10_26_covered_by_pair":bool(pair and pair[0]["date"]<"2026-10-26"<=pair[1]["date"]),
        "images_processed":False,"flood_area_km2":None}
    if pair:
        a,b=pair
        try:
            x,u,ca=fetch(a["date"]);y,v,cb=fetch(b["date"])
            if x.size!=y.size:raise RuntimeError("Image dimensions differ.")
            x.save(OUT/"nisar_antes.png");y.save(OUT/"nisar_despues.png")
            d,valid,changed=summarize_before_after(x,y)
            d.save(OUT/"diferencia_visual_rgb.png")
            margin=55
            combined=Image.new("RGB",(x.width*3,x.height+margin),(14,21,27))
            draw=ImageDraw.Draw(combined)
            for i,(img,label) in enumerate([(x,"ANTES "+a["date"]),(y,"DESPUES "+b["date"]),(d,"DIFERENCIA RGB (NO CALIBRADA)")]):
                combined.paste(img.convert("RGB"),(i*x.width,margin))
                draw.text((i*x.width+9,15),label,fill="white")
            combined.save(OUT/"comparacion_nisar_gibs.png")
            report.update({"status":"VISTA_RGB_GIBS_GENERADA","images_processed":True,
                "source_urls":[u,v],"coverage_before":ca,"coverage_after":cb,
                "valid_shared_rgb_pixels":valid,"changed_rgb_pixels_threshold35":changed,
                "relative_rgb_change_percent":round(100*changed/valid,2) if valid else None,
                "note":"GIBS WMS daily mosaic may combine granules; differences of RGB display values, not radar backscatter in dB. Results are NOT measured flooded area. Both dates precede Oct 26 event."})
        except Exception as exc:
            report["error"]=str(exc)
    (OUT/"resultado.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:report.get(k) for k in ("status","granule_ids","error","coverage_before","coverage_after","relative_rgb_change_percent","event_2026_10_26_covered_by_pair")},ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
