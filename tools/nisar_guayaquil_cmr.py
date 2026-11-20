#!/usr/bin/env python3
"""ILLARI: inventario reproducible de dos adquisiciones NISAR GCOV reales sobre Guayaquil.
Consulta los metadatos NASA CMR. NO descarga píxeles HDF5 ni calcula inundaciones.
"""
import collections
import datetime as dt
import json
import pathlib
import time
import urllib.parse
import urllib.request

CMR = "https://cmr.earthdata.nasa.gov/search/granules.json"
BBOX = "-80.05,-2.33,-79.75,-1.95"  # west,south,east,north
EVENT = "2026-10-26"
CENTER = (-2.17, -79.90)
COLLECTIONS = {
    "NISAR_L2_GCOV_V1": "VALIDATED",
    "NISAR_L2_GCOV_PROVISIONAL_V1": "PROVISIONAL",
    "NISAR_L2_GCOV_BETA_V1": "BETA",
}

def get_json(url):
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={
                "Accept": "application/json",
                "User-Agent": "ILLARI-NISAR-case-study/1.0 public research"})
            with urllib.request.urlopen(req, timeout=45) as result:
                return json.load(result)
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)

def query(collection):
    entries = []
    for page in range(1, 16):
        qs = urllib.parse.urlencode({
            "short_name": collection, "bounding_box": BBOX,
            "temporal": "2026-06-17T00:00:00Z,2026-11-15T23:59:59Z",
            "page_size": "2000", "page_num": str(page)})
        batch = get_json(CMR + "?" + qs).get("feed", {}).get("entry", [])
        entries.extend(batch)
        if len(batch) < 2000:
            return entries
    raise RuntimeError("CMR: límite de paginación alcanzado; no afirmar cobertura completa.")

def contains_center(entry):
    lat, lon = CENTER
    for b in entry.get("boxes", []):
        s, w, n, e = map(float, b.split())
        if s <= lat <= n and w <= lon <= e:
            return True
    for poly in entry.get("polygons", []):
        if not poly:
            continue
        raw = list(map(float, poly[0].split()))
        pts = list(zip(raw[::2], raw[1::2]))
        inside = False
        for i in range(len(pts)):
            a, b = pts[i-1], pts[i]
            if (a[0] > lat) != (b[0] > lat):
                x = (b[1]-a[1])*(lat-a[0])/(b[0]-a[0]) + a[1]
                if lon < x:
                    inside = not inside
        if inside:
            return True
    return False

def parse_scene(entry, maturity):
    name = entry.get("title", "")
    p = name.replace(".h5", "").split("_")
    if len(p) < 14 or p[0] != "NISAR" or p[1] != "L2" or p[2] not in ("PR", "UR") or p[3] != "GCOV":
        return None
    if not p[5].isdigit() or p[6] not in ("A", "D") or not p[7].isdigit():
        return None
    timestamp = entry.get("time_start") or p[11]
    date = timestamp[:10] if "-" in timestamp else timestamp[:4] + "-" + timestamp[4:6] + "-" + timestamp[6:8]
    links = entry.get("links") or []
    data = next((l.get("href") for l in links if ".h5" in l.get("href","") and l.get("href","").startswith("https://")), None)
    preview = next((l.get("href") for l in links if l.get("type","").startswith("image/") and l.get("href","").startswith("https://")), None)
    return {
        "id":name, "date":date, "track":p[5], "direction":p[6],
        "frame":p[7], "mode":p[8], "polarization":p[9],
        "source_mode":p[10], "maturity":maturity,
        "center_covered":contains_center(entry), "has_footprint":bool(entry.get("boxes") or entry.get("polygons")),
        "hdf5":data, "browse":preview
    }

def pairs_from(scenes):
    groups = collections.defaultdict(list)
    for s in scenes:
        key = (s["track"],s["direction"],s["frame"],s["mode"],
               s["polarization"],s["source_mode"],s["maturity"])
        groups[key].append(s)
    output = []
    for values in groups.values():
        by_date = {s["date"]:s for s in sorted(values,key=lambda v:v["id"])}
        dates = sorted(by_date)
        for i,bdate in enumerate(dates):
            for adate in dates[max(0,i-6):i]:
                gap = (dt.date.fromisoformat(bdate)-dt.date.fromisoformat(adate)).days
                if 0 < gap <= 60:
                    output.append((by_date[adate],by_date[bdate]))
    def score(p):
        a,b=p
        crosses = a["date"] < EVENT <= b["date"]
        center = a["center_covered"] and b["center_covered"]
        m = {"VALIDATED":3,"PROVISIONAL":2,"BETA":1}[a["maturity"]]
        lag = abs((dt.date.fromisoformat(b["date"])-dt.date.fromisoformat(EVENT)).days)
        gap = (dt.date.fromisoformat(b["date"]) - dt.date.fromisoformat(a["date"])).days
        return (int(crosses),int(center),m,-lag,-gap)
    return sorted(output,key=score,reverse=True)

def main():
    all_scenes, errors, counts = [], [], {}
    for collection,maturity in COLLECTIONS.items():
        try:
            data=query(collection)
            counts[collection]=len(data)
            all_scenes.extend(filter(None,(parse_scene(e,maturity) for e in data)))
        except Exception as e:
            counts[collection]=None
            errors.append(collection+": "+type(e).__name__+": "+str(e))
    candidates=pairs_from(all_scenes)
    selected=list(candidates[0]) if candidates else None
    event_pairs = [p for p in candidates if p[0]["date"] < EVENT <= p[1]["date"] and
                   p[0]["center_covered"] and p[1]["center_covered"]]
    status=("PAR_ANTES_DESPUES_EVENTO" if selected and event_pairs else
            "PAR_SOLO_CONTEXTO_PREVIO_O_POSTERIOR" if selected else
            "CMR_INACCESIBLE" if errors and not all_scenes else "SIN_PAR_COMPATIBLE")
    result={"status":status,"actualizado_utc":dt.datetime.now(dt.timezone.utc).isoformat(),
      "zona":BBOX,"evento":EVENT,"consultas":counts,"escenas":len(all_scenes),
      "pares_compatibles":len(candidates),"pares_que_cruzan_evento":len(event_pairs),
      "par":selected,"candidatos_principales":[list(p) for p in candidates[:12]],"errores":errors,
      "pixels_GCOV_analizados":False,"superficie_inundada_km2":None}
    folder=pathlib.Path("reports")
    folder.mkdir(exist_ok=True)
    (folder/"nisar_guayaquil_cmr.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    lines=["# Caso NISAR Guayaquil — inventario reproducible", "",
      "Evento de contexto: inundaciones reportadas el 26 de octubre de 2026.",
      "Fuente de metadatos: NASA CMR / ASF; bbox: "+BBOX+".", "",
      "**Resultado de catálogo:** "+status+".",
      "Escenas candidatas: "+str(len(all_scenes))+"; pares comparables: "+str(len(candidates))+".",
      "Pares que cruzan el 26 de octubre y abarcan el centro urbano: "+str(len(event_pairs))+".",
      "ADVERTENCIA: si ese número es cero, NO existe evidencia SAR antes/después del evento en este inventario.", "",
      "**Alcance:** solamente metadatos de adquisiciones; no se han descargado imágenes GCOV ni medido áreas inundadas.", ""]
    if selected:
        a,b=selected
        lines += ["## Par encontrado","",
          "| Campo | Antes | Después |","|---|---|---|",
          "| Fecha | "+a["date"]+" | "+b["date"]+" |",
          "| Identificador NASA | "+a["id"]+" | "+b["id"]+" |",
          "| Track / dirección / frame | "+a["track"]+"/"+a["direction"]+"/"+a["frame"]+" | "+b["track"]+"/"+b["direction"]+"/"+b["frame"]+" |",
          "| Polarización / modo | "+a["polarization"]+"/"+a["mode"]+" | "+b["polarization"]+"/"+b["mode"]+" |",
          "| Madurez | "+a["maturity"]+" | "+b["maturity"]+" |",
          "| Huella incluye centro | "+str(a["center_covered"])+" | "+str(b["center_covered"])+" |",""]
        if a["date"] < EVENT <= b["date"]:
            lines.append("Las fechas rodean el evento; esto NO demuestra que el agua persistiera hasta la adquisición posterior.")
        else:
            lines.append("Las fechas NO rodean el evento: este par permite estudiar cambios generales, NO atribuirlos a la inundación.")
        for title,x in (("Antes",a),("Después",b)):
            if x["hdf5"]: lines.append("- GCOV "+title+": "+x["hdf5"])
            if x["browse"]:lines.append("- Vista previa "+title+": "+x["browse"])
    else:
        lines.append("No hay evidencia suficiente para elegir dos adquisiciones. No inventar fechas ni resultados.")
    if candidates:
        lines+=["","## Otros pares comparables del catálogo (metadatos; no imágenes)", "",
            "| Antes | Después | Track | Frame | Madurez | Centro | Cruza evento |",
            "|---|---|---|---|---|---|---|"]
        for a,b in candidates[:12]:
            lines.append("| "+a["date"]+" | "+b["date"]+" | "+a["track"]+" | "+a["frame"]+
                         " | "+a["maturity"]+" | "+str(a["center_covered"] and b["center_covered"])+
                         " | "+str(a["date"] < EVENT <= b["date"])+" |")
    if errors:
        lines+=["","## Errores de consulta"]+["- "+e for e in errors]
    lines += ["","## Próximo paso necesario","",
      "Descargar los archivos HDF5 GCOV de ambas fechas (puede requerir Earthdata Login),",
      "verificar cobertura espacial y geometría, comparar HHHH/HVHV en gamma-0 sobre la",
      "misma región y evaluar los resultados con OPERA y evidencia de terreno.","",
      "Fuentes: https://nisar-docs.asf.alaska.edu/gcov/ ; https://nisar-docs.asf.alaska.edu/availability-overview/",""]
    (folder/"nisar_guayaquil_cmr.md").write_text("\n".join(lines),encoding="utf-8")
    print(json.dumps({"status":status,"scenes":len(all_scenes),"pairs":len(candidates),
                      "cross_event_pairs":len(event_pairs),
                      "chosen":[a["id"] for a in selected] if selected else None,
                      "errors":errors},ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
