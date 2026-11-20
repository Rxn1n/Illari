#!/usr/bin/env python3
"""Consulta reproducible de OPERA DSWx-S1 (CMR y GIBS) cerca de dos fechas NISAR.
No confundir RGB cartográfico con las clases raster WTR del producto original.
"""
from collections import Counter
from datetime import date, timedelta
import io
import json
import pathlib
import time
import urllib.parse
import urllib.request
from PIL import Image

CMR="https://cmr.earthdata.nasa.gov/search/granules.json"
WMS="https://gibs.earthdata.nasa.gov/wms/epsg3857/best/wms.cgi"
BB=(-79.96004,-2.23006,-79.83991,-2.10992)  # W,S,E,N, correspondencia GeoTIFF local
XY=(-8901111,-248311,-8887739,-234930) # EPSG 3857
ROOT=pathlib.Path("reports/opera_probe")
ROOT.mkdir(parents=True,exist_ok=True)
DATES=("2026-10-07","2026-10-19")
LAYER="OPERA_L3_Dynamic_Surface_Water_Extent-Sentinel-1"

def fetch(url, n=3):
    for k in range(n):
        try:
            r=urllib.request.Request(url,headers={"User-Agent":"ILLARI-SpaceApps/1.0","Accept":"*/*"})
            with urllib.request.urlopen(r,timeout=45) as f: return f.read(), f.headers.get("Content-Type",""),f.geturl()
        except Exception:
            if k+1==n: raise
            time.sleep(2**k)

def cmr_search():
    qs=urllib.parse.urlencode({
        "short_name":"OPERA_L3_DSWX-S1_V1",
        "bounding_box":",".join(map(str,BB)),
        "temporal":"2026-09-28T00:00:00Z,2026-10-27T23:59:59Z",
        "page_size":1000})
    raw,typ,_=fetch(CMR+"?"+qs)
    feed=json.loads(raw).get("feed",{})
    items=[]
    for e in feed.get("entry",[]):
        links=e.get("links",[])
        wtr=[x["href"] for x in links if "WTR" in x.get("href","").upper()
             and x.get("href","").lower().endswith((".tif",".tiff"))]
        items.append({"id":e.get("id"),"title":e.get("title"),"date":(e.get("time_start") or "")[:10],
                      "wtr_links":wtr[:2],"browse_links":[x.get("href") for x in links if "image" in x.get("type","")][:1]})
    return items

def url_for(day,width=64):
    height=round(width*(XY[3]-XY[1])/(XY[2]-XY[0]))
    args={"SERVICE":"WMS","REQUEST":"GetMap","VERSION":"1.3.0","LAYERS":LAYER,
          "STYLES":"","FORMAT":"image/png","TRANSPARENT":"TRUE","CRS":"EPSG:3857",
          "BBOX":",".join(map(str,XY)),"WIDTH":width,"HEIGHT":height,"TIME":day}
    return WMS+"?"+urllib.parse.urlencode(args)

def wms_probe(day,width=64):
    raw,typ,final=fetch(url_for(day,width))
    if "image/" not in typ: raise RuntimeError(f"not an image: {typ}, {raw[:200]!r}")
    im=Image.open(io.BytesIO(raw)).convert("RGBA")
    c=Counter(im.getdata())
    opaque=sum(n for (r,g,b,a),n in c.items() if a>0)
    colors=[{"rgba":list(col),"n":n} for col,n in c.most_common(10)]
    return im,{"date":day,"image_size":list(im.size),"opaque_fraction":round(opaque/(im.width*im.height),4),
               "top10_colors":colors,"url":url_for(day,width)}

def main():
    report={"bbox_wsen":BB,"EPSG":3857,"layer":LAYER,"nir_dates":DATES,
            "catalog_records":[],"wms_probe":[],"errors":[]}
    try:report["catalog_records"]=cmr_search()
    except Exception as exc:report["errors"].append("CMR: "+repr(exc))
    start=date(2026,10,1);stop=date(2026,10,25)
    for i in range((stop-start).days+1):
        day=(start+timedelta(days=i)).isoformat()
        try:
            im,v=wms_probe(day,64)
            report["wms_probe"].append(v)
        except Exception as exc:report["wms_probe"].append({"date":day,"error":repr(exc)})
    good=[r for r in report["wms_probe"] if r.get("opaque_fraction",0)>0.08]
    for target in DATES:
        options=sorted(good,key=lambda x:abs((date.fromisoformat(x["date"])-date.fromisoformat(target)).days))
        if options:
            chosen=options[0]["date"]
            try:
                im,v=wms_probe(chosen,640)
                p=ROOT/f"OPERA_DSWxS1_GIBS_{chosen}.png"
                im.save(p)
                v["filename"]=p.name
                report.setdefault("chosen",[]).append({"target":target,**v})
            except Exception as exc:
                report["errors"].append(f"hires {chosen}: "+repr(exc))
    report["catalog_total"]=len(report["catalog_records"])
    report["wms_days_with_opaque"]=len(good)
    (ROOT/"sondeo.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({"catalog_total":report["catalog_total"],"sample_catalog":report["catalog_records"][:3],
                      "wms_days_with_opaque":len(good),"date_probes":report["wms_probe"][:5],
                      "chosen":[{k:z[k] for k in ("target","date","opaque_fraction","filename")} for z in report.get("chosen",[])],
                      "errors":report["errors"]},ensure_ascii=False,indent=2))

if __name__=="__main__":main()
