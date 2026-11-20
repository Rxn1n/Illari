# ILLARI — Caso reproducible NISAR Guayaquil (7 y 19 de octubre de 2026)

> **Seguimiento del caso.** Esta ficha documenta la primera etapa de catálogo y visualización RGB. El análisis posterior de los recortes GCOV calibrados se puede explorar en el [visor HH/HV](https://rxn1n.github.io/Illari/docs/demostracion/visor.html). La [guía de demostración](docs/demostracion/README.md) explica la diferencia entre los dos productos y el alcance del contraste con OPERA.

**Ideador y director:** Darío Proaño · **Diseño y código:** Anthony Cisneros (rxn1n)  
**Estado:** inventario **real de CMR comprobado** + visualización **real de NASA GIBS**; aún **sin validación de cambios en valores GCOV calibrados ni superficie inundada**.  
**Fecha de ejecución:** 15 de noviembre de 2026 (hora Ecuador; UTC 16 de noviembre).

## Resumen de la evidencia obtenida

La consulta automática de NASA CMR en un servidor GitHub Actions encontró **42 registros GCOV** sobre la caja de Guayaquil, de los cuales **38 PROVISIONAL y 4 VALIDATED**; encontró **102 combinaciones de pares compatibles por metadatos** (no 102 eventos). Se identificó un par del **7 y 19 de octubre de 2026**, separado por 12 días, en el **track 112, descendente, frame 090, modo 4005, polarización DHDH y madurez PROVISIONAL**. Ambas huellas CMR contienen el punto de referencia del centro de Guayaquil.

**Limitación del evento:** el catálogo no proporcionó ningún par compatible que cruce el **26 de octubre de 2026** y cubra el centro urbano, dentro del periodo consultado. Por tanto **esta comparación NO puede demostrar ni estimar la inundación del 26 de octubre**.

## Adquisiciones verificadas

| Campo | Antes | Después |
|---|---|---|
| Fecha UTC | 2026-10-07 | 2026-10-19 |
| Hora UTC inicial | 23:39:44 | 23:39:44 |
| Track / dirección / frame | 112 / D / 090 | 112 / D / 090 |
| Ciclo | 032 | 033 |
| Modo / polarización / fuente | 4005 / DHDH / A | 4005 / DHDH / A |
| Colección | NISAR_L2_GCOV_PROVISIONAL_V1 | NISAR_L2_GCOV_PROVISIONAL_V1 |
| Archivo oficial | `NISAR_L2_PR_GCOV_032_112_D_090_4005_DHDH_A_20261007T233944_20261007T234018_P05023_N_F_J_001` | `NISAR_L2_PR_GCOV_033_112_D_090_4005_DHDH_A_20261019T233944_20261019T234018_P05023_N_F_J_001` |

Los enlaces a los archivos HDF5 originales están en el informe CMR generado por GitHub Actions (la descarga puede requerir Earthdata Login).

## Primera demostración visual real

Se consultó la capa de **NASA GIBS** `NISAR_L2_Geocoded_Polarimetric_Covariance` con `TIME=2026-10-07` y `TIME=2026-10-19`, utilizando la misma caja geográfica y geometría WMS EPSG:3857. La respuesta fue **imagen de radar en falso color (8 bits)** en ambos casos.

- Dimensiones de ambas imágenes: **480 × 608 píxeles**.
- Cobertura visible de ambas imágenes: **100 % según alfa de imagen**. Esto no prueba cobertura uniforme de un único granule.
- Píxeles con comparación RGB válida en ambas fechas: **291 840**.
- Píxeles cuya media de diferencias absolutas en los canales R/G/B fue al menos 35 niveles (escala 0–255): **23 197** (**7,95 %**).

**Interpretación correcta:** 7,95 % significa solamente la **proporción de píxeles de visualización cuya diferencia RGB supera el umbral exploratorio elegido**, no la proporción de territorio afectado, ni porcentaje de inundación, ni probabilidad, ni medición calibrada de retrodispersión. La diferencia puede deberse a cambios estacionales, humedad, características del mosaico o procesamiento de las imágenes.

**Precaución decisiva:** GIBS ofrece un **mosaico diario**, mientras que los identificadores GCOV son escenas individuales del catálogo CMR. Confirmar que existen escenas con esas fechas y metadatos **no demuestra por sí solo que cada píxel del mosaico provenga de esos granules**. La comparación HDF5 GCOV es el paso necesario para establecer correspondencia inequívoca y calcular cambios científicos calibrados.

## Cómo reproducir

1. Abrir el [script del catálogo CMR](tools/nisar_guayaquil_cmr.py) y el [script de imágenes GIBS](tools/nisar_guayaquil_gibs.py).
2. Ejecutar `python tools/nisar_guayaquil_cmr.py`.
3. Instalar Pillow: `python -m pip install pillow`.
4. Ejecutar `python tools/nisar_guayaquil_gibs.py`.
5. Revisar `reports/nisar_guayaquil_cmr.json`, `reports/nisar_guayaquil_cmr.md` y los PNG de `reports/nisar_gibs_preview/`.

Todo esto ya se ejecutó correctamente desde GitHub Actions: **[ejecución con archivos descargables](https://github.com/Rxn1n/Illari/actions/runs/43781984829)**. Los productos generados están en el artefacto `reporte-nisar-guayaquil-cmr` de esa ejecución. La documentación y los scripts quedan en el repositorio; los datos del reporte pertenecen al artefacto de la ejecución.

## Próximo paso científico indispensable

Procesar las dos adquisiciones originales GCOV en formato HDF5, tomando el mismo recorte espacial y la misma polarización, comprobando el producto disponible (p. ej. HHHH/HVHV) y unidades de retrodispersión. Luego comparar valores **calibrados**, estimar incertidumbre y contrastar los cambios con OPERA y, cuando sea posible, evidencia de campo. **No atribuir la comparación octubre 7 → 19 a la inundación de octubre 26**.

## Fuentes

- [NASA CMR](https://cmr.earthdata.nasa.gov/search/granules.json)
- [NASA ASF — GCOV](https://nisar-docs.asf.alaska.edu/gcov/)
- [NASA ASF — Convenciones de nombres](https://nisar-docs.asf.alaska.edu/naming-conventions/)
- [NASA GIBS](https://gibs.earthdata.nasa.gov/)
