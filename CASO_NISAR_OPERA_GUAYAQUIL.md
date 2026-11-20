# ILLARI — Contraste exploratorio NISAR GCOV / NASA OPERA DSWx-S1

**Dirección e ideación:** Darío Proaño. **Diseño y código del proyecto:** Anthony Cisneros (rxn1n).  
**Zona:** centro de Guayaquil (recorte original aprox. oeste −79.96, sur −2.23, este −79.84, norte −2.11).  
**Estado:** contraste espacial y temporal exploratorio realizado con datos reales, **NO validación independiente de inundación**.

## 1. Fuentes y fechas

| Sistema | Antes | Después | Propiedad |
|---|---|---|---|
| **NISAR GCOV PROVISIONAL (NASA/ISRO)** | 7 oct 2026, 23:39 UTC | 19 oct 2026, 23:39 UTC | Retrodispersión calibrada HH/HV; track 112, descendente, frame 090 |
| **OPERA DSWx-S1 (NASA, Sentinel-1)** | 6 oct 2026 | 18 oct 2026 | Clasificación cartográfica de agua, consultada mediante NASA GIBS |

NISAR: GeoTIFF recortados y proporcionados por el equipo, con matriz común **1335 × 1327 píxeles, 10 m, EPSG:32717**, 1 771 545 píxeles válidos por banda y fecha.  
OPERA: en el catálogo oficial NASA CMR se encontraron **21 productos** en la caja y el intervalo examinados. El servicio NASA GIBS expuso imágenes clasificadas de **6 y 18 oct**; ambos días están **un día antes** de los GCOV NISAR correspondientes.

**Precaución de productos:** los mapas OPERA usados en el cruce son **visualizaciones PNG de NASA GIBS**, no los raster WTR originales de 30 m. Se solicitaron en **640 × 640 píxeles** (aprox. 20,9 m/píxel proyectado), se decodificaron **solo colores exactos** de la leyenda y se remuestrearon por vecino más cercano sobre el grid NISAR de 10 m. El remuestreo no aumenta la resolución real de OPERA y puede introducir discrepancias espaciales en bordes. **Las áreas que siguen son equivalentes nominales de píxeles de la malla remuestreada, no delimitaciones de precisión hidrológica**.

## 2. Método reproducible

**Señal NISAR:** para cada polarización, se calculó `ΔdB = dB(19 oct) − dB(7 oct)`. Se aplicó filtro de **mediana espacial 3×3 sobre la matriz de diferencias** y se marcó una *disminución simultánea* donde `ΔHH ≤ −3 dB` **y** `ΔHV ≤ −2,5 dB`. Los umbrales son **heurísticos** y la disminución conjunta NO es por sí misma una prueba física suficiente de inundación.

**Señal OPERA:** agua abierta nueva aparente donde las dos fechas tienen clases interpretables (0–3), la del **18 oct = clase 1 (agua abierta)** y la del **6 oct = clase 0 o 2** (no clase 1 ni clase 3). Esta regla descarta nuevos píxeles no clasificables. Es una **comparación de clases de mosaico**, no etiqueta de terreno validada.

**Corroboración:** intersección geométrica de los dos criterios anteriores dentro del área común, conservando registro del desfase de **un día** entre satélites. Los mapas no deben atribuirse al episodio de inundación del **26 oct**, posterior a las cuatro adquisiciones empleadas.

## 3. Resultados medidos

| Categoría exploratoria | Píxeles equivalentes de 10 m | Área equivalente km² |
|---|---:|---:|
| Área de comparación con clases OPERA válidas | 1 769 004 | 176,9004 |
| OPERA: agua abierta nueva aparente | 1 413 | 0,1413 |
| OPERA: agua abierta persistente | 291 277 | 29,1277 |
| NISAR: caída HH y HV simultánea | 5 265 | 0,5265 |
| **Intersección caída HH/HV + agua nueva OPERA** | **7** | **0,0007** |

- La intersección es **7/1 413 ≈ 0,50 %** de la zona que OPERA clasifica como agua nueva aparente, y aproximadamente **7/5 265 ≈ 0,13 %** del conjunto con disminución conjunta HH/HV.
- Esto indica **concordancia espacial extremadamente limitada entre ambas reglas**, dadas estas fechas, umbrales y representaciones. NO demuestra que no hubo inundación ni que uno de los sensores «falle».
- Los cambios de retrodispersión pueden responder a humedad, vegetación, geometría de observación, agua, diferencias de procesamiento y otros factores. La proximidad de las fechas, la calidad de la georreferenciación y las máscaras de incertidumbre condicionan el contraste.
- Se debe priorizar descargar las bandas **WTR GeoTIFF originales de OPERA**, inspeccionar las clases y fechas efectivas por tesela, corregir potenciales desplazamientos y considerar criterios por tipo de cobertura (incluidos incrementos HH por doble rebote en áreas urbanas).

## 4. Comprobación y material reproducible

- [Sondeo oficial OPERA: código fuente](tools/sondear_opera_dswx.py).
- [Consulta NISAR GCOV en CMR](tools/nisar_guayaquil_cmr.py).
- [Ejecución GitHub Actions con datos OPERA y sus PNG](https://github.com/Rxn1n/Illari/actions/runs/43790524771).
- [Mediciones GCOV y procedimiento reproducible](docs/demostracion/reproduce.md). Se pueden regenerar los dos rásteres de diferencias y las medianas del caso NISAR. El cruce OPERA de esta tabla está documentado como análisis exploratorio histórico; las máscaras de ese cruce no forman parte del paquete público.

**Conclusión limitada:** se demostró la capacidad de efectuar una comparación pixel a pixel entre datos GCOV NISAR calibrados y cartografía OPERA DSWx-S1 próxima en el tiempo. Las **7 celdas coincidentes no constituyen una estimación validada de inundación**. Es necesario trabajar con WTR originales y contrastar contra referencia externa antes de usar la clasificación operativamente.
