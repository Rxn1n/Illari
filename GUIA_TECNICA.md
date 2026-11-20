# ILLARI · Guía técnica (Spanish)

[English case guide](docs/demostracion/guide-en.md) · [Caso de Guayaquil](docs/demostracion/README.md)

## Sincronizado al momento (1.5.0)

Al abrir, ILLARI muestra la **Situación actual** y se actualiza sola cada 30 minutos (también con el botón **Actualizar**). Arriba del panel indica la hora de la última sincronización.

| Dato en vivo | Fuente | Frecuencia / demora típica |
|---|---|---|
| Radar NISAR: el par comparable más reciente | NASA CMR + GIBS | cada 12 días; NASA publica días después |
| Agua abierta (Sentinel-1), 30 últimos días | NASA OPERA DSWx | cada 2–6 días; ~1 día de demora |
| **Lluvia medida por satélite**: últimas 3 h, 24 h y 7 días, cada 30 min | **NASA GPM IMERG** (Early y diaria, vía GIBS) | cada 30 min; ~6 h de demora |
| Focos de calor y pérdida de vegetación | NASA VIIRS + OPERA DIST | diaria |
| Lluvia, caudal de ríos y marea: últimos 30 días + 16 días de pronóstico | Open-Meteo, GloFAS | horaria |

- El panel de contraste muestra las fechas y los desfases entre NISAR y OPERA. Una coincidencia espacial en periodos diferentes se identifica como exploratoria.
- **Lluvia medida frente a modelada:** la tarjeta IMERG pone lado a lado la lluvia observada por satélite y la que reconstruye el modelo que alimenta el pronóstico.
- **Robustez:** si NASA GIBS falla de forma pasajera, ILLARI reintenta, usa otra fecha válida y lo explica, sin pasar a la escena simulada. El modo Observado exige que los dos mosaicos tengan la misma madurez documentada.

## Uso

- **Sin instalación:** abre `index.html` con doble clic en Chrome o Edge. No hay servidor, cuentas ni claves.
- **Conexión directa a datos reales:** al abrirse, ILLARI consulta en vivo:
  - las pasadas del radar NISAR sobre la ciudad (catálogo público NASA CMR);
  - las imágenes NISAR de NASA GIBS, que compara antes y después de un evento;
  - la lluvia medida por satélite (NASA GPM IMERG), los mapas de agua de Sentinel-1 (OPERA), los focos VIIRS y el pronóstico de Open-Meteo.
- **Sin descargas:** no hay que descargar nada. El radar en vivo necesita conexión. La simulación de Observado solo se activa si se elige expresamente. El HTML descargado del visor del caso contiene las observaciones de octubre y funciona sin conexión.
- **Opción avanzada:** el botón **Catálogo NASA** permite además abrir archivos GCOV/GUNW originales para trabajar con valores calibrados.

## Fuentes

| Fuente | Uso | Clave |
|---|---|---|
| **NISAR GCOV en NASA GIBS** (capa diaria `NISAR_L2_Geocoded_Polarimetric_Covariance`, desde el 29 oct 2025, falso color HH/HV, 15,6 m; fechas, órbita y polarización de cada pasada desde NASA CMR) | Imágenes de radar en vivo y detección de cambios | **No** |
| NISAR L2 **GCOV** y **GUNW** originales (ASF DAAC) | Opción avanzada con valores calibrados | Earthdata Login gratuito |
| NASA Earthdata **CMR** | Búsqueda en vivo de productos sobre cada ciudad | No |
| **NASA GPM IMERG** (GIBS: `IMERG_Precipitation_Rate_30min` y diaria; paleta oficial `GPM_Precipitation_Rate`) | Lluvia observada: 3 h, 24 h, 7 y 30 días | No |
| NASA **GIBS** (VIIRS) y **FIRMS** | Imagen del día, focos de calor | FIRMS opcional |
| **Open-Meteo**: pronóstico, GloFAS, mareas (respaldo de relieve: Copernicus DEM) | Pronóstico | No |
| **NASA SRTM** vía AWS Terrain Tiles (Open Data) | Relieve y pendiente | No |
| Esri World Imagery y World Street Map | Mapa base | No |

## Método (resumen)

**Observado en vivo (NASA GIBS).** Antes de calcular cambios se exige una pareja de adquisiciones con metadatos CMR compatibles: **mismo track, dirección, frame, composición de polarizaciones y nivel de madurez**. Se rechazan mosaicos diarios ambiguos o con múltiples geometrías. El sondeo directo a GIBS puede encontrar fechas publicadas, pero **no permite determinar su geometría por sí solo**: si falta CMR, ILLARI indica *Comparación SAR no disponible* y no calcula superficies. No se activa automáticamente una escena simulada; la demostración queda como elección explícita. Cuando un par compatible falla temporalmente en GIBS, se intenta un par anterior igualmente compatible.
En la visualización de NASA (co-polar HH en rojo y azul, cruzada HV en verde), medida sobre Guayaquil, el agua tranquila se ve **oscura y azulada**, la vegetación verde intensa y la ciudad amarilla.
Tras suavizar los canales (5×5), ILLARI aplica estas reglas exploratorias:
- *posible agua nueva*: píxeles que pasan a oscuros y azulados (R+G+B < 200 y B/(R+G+B) > 0,24) y pierden brillo;
- *posible agua bajo edificios*: zonas donde el canal rojo sube con fuerza;
- *posible área quemada*: zonas verdes cuyo canal verde cae con fuerza.

Son imágenes de 8 bits: las áreas son **aproximaciones** sin validación independiente, y así se indica en la interfaz, la procedencia y las exportaciones.

**Observado, inundación con archivos (avanzado).**
1. Cada imagen GCOV se re-muestrea a una malla común (promedio por bloques), se filtra el moteado (3×3) y se pasa a dB.
2. Se marca *agua nueva* donde la imagen posterior está bajo el umbral de agua (Otsu automático, o manual)
   y al menos 3 dB más oscura que la anterior.
3. Se marca *posible inundación bajo vegetación o edificios* donde la HH sube 3 dB o más (doble rebote).
4. Con relieve de procedencia identificada se descartan candidatos sobre 25 m. Si falta, se omite el filtro de altitud y se indica en el resultado. También se descartan píxeles aislados.

**Observado, incendio.** Se marca *posible área quemada* donde la HV cae 2,5 dB o más sobre vegetación previa.
Con productos GUNW se usa en cambio la pérdida de coherencia.

**Estimado.** Usa el índice FWI canadiense (validado con el caso de prueba oficial) y un índice compuesto de
inundación. Están documentados en la sección "Método, fuentes y limitaciones" de la app.

## Ecuaciones de los modelos predictivos: alcance y justificación

**Guayaquil:** el índice exploratorio de peligro de inundación aplica
`I = 100 × (0,50 × R + 0,30 × Q + 0,20 × M)`,
donde `R` representa lluvia normalizada (24/72 h), `Q` caudal fluvial normalizado y `M` nivel del mar normalizado. Después se aplica una susceptibilidad por elevación en el mapa.

**Los porcentajes 50 % / 30 % / 20 % son consideraciones iniciales del equipo ILLARI.**
Fueron seleccionados como hipótesis operativa por el **tiempo limitado del hackathon**;
**NO** proceden de una estimación de coeficientes con regresión o datos históricos de inundaciones.
La calibración y validación estadística de estos pesos, o la formulación de **otra ecuación predictiva**
entrenada y evaluada con eventos reales, es una tarea pendiente que no se completó por falta de tiempo.
Por tanto, el índice **no es una probabilidad validada** ni un pronóstico certificado de inundación.
Los umbrales de normalización también deben someterse a evaluación local.

**Quito:** emplea el sistema canadiense Fire Weather Index (FWI), calculado con temperatura,
humedad relativa, viento y precipitación; ILLARI adapta el índice de propagación ISI a la
pendiente del terreno mediante `min(4, exp(0,0693 × pendiente_en_grados))`.
Esta adaptación y sus umbrales locales requieren comprobación independiente.

**Relación entre fuentes:** las predicciones proceden de Open-Meteo (meteorología),
GloFAS (caudales modelados), Open-Meteo Marine (nivel del mar modelado) y NASA SRTM
(relieve; respaldo Copernicus DEM). Por separado, NISAR/OPERA/VIIRS observan cambios;
GPM IMERG estima precipitación observada por satélite para contraste. **Las detecciones
satelitales no son entradas directas de las ecuaciones predictivas actuales, y los
coeficientes no se entrenaron con esos satélites.**

**Documento técnico bilingüe:** [Ecuaciones y relación entre observación y predicción](MODELOS_PREDICTIVOS.md)
(español e inglés, con fórmulas y referencias al código).

## Contraste multisensor y evaluación retrospectiva

- **Corroboración multisensor (Observado):** el posible cambio hídrico de NISAR se contrasta con dos fechas de OPERA DSWx-S1. El tablero busca hasta seis días a cada lado de cada adquisición NISAR, elige dos mapas en orden cronológico, muestra los dos desfases y rotula como exploratorio todo cruce con fechas distintas. DSWx-HLS (óptico) permite observar presencia de agua, pero no demuestra por sí solo que sea nueva. Las posibles señales compatibles con áreas quemadas se contrastan con OPERA DIST-ALERT (30 m) y focos térmicos VIIRS; sin una imagen DIST anterior comparable no se clasifican alteraciones como «nuevas». Las clases se leen mediante las paletas de los productos y la coincidencia no equivale a validación en terreno.
- **¿El pronóstico habría avisado? (Estimado):** se comparan pronósticos emitidos en el pasado con lo ocurrido.
  - Guayaquil: aciertos y falsas alarmas de lluvia fuerte.
  - Quito: FWI en días con y sin fuego, y umbral ajustado al periodo analizado.

## Caso real NISAR reproducible (7–19 oct 2026)

**[Caso NISAR Guayaquil: adquisiciones oficiales, imágenes y límites de la demostración](CASO_NISAR_GUAYAQUIL.md)**.

Se verificaron en NASA CMR **dos escenas GCOV PROVISIONAL reales** del track 112, descendente, frame 090, polarización DHDH, adquiridas el **7 y 19 de octubre de 2026**. GitHub Actions descargó las visualizaciones en falso color NASA GIBS de ambas fechas y generó una comparación RGB preliminar. El [visor del caso](https://rxn1n.github.io/Illari/docs/demostracion/visor.html) muestra por separado el análisis de los recortes GCOV calibrados. El 7,95 % reportado corresponde a píxeles que superaron un umbral arbitrario de diferencia RGB y **no representa superficie inundada**.

En el inventario de junio a noviembre no se encontró un par compatible que abarque el evento **26 oct 2026** y cubra el centro urbano: el caso 7–19 de octubre **no demuestra esa inundación**. Informes y PNG reproducibles: [ejecución GitHub Actions](https://github.com/Rxn1n/Illari/actions/runs/43781984829).

## Contraste inicial GCOV–OPERA (6–19 oct 2026)

**[Informe de cruce NISAR GCOV con OPERA DSWx-S1](CASO_NISAR_OPERA_GUAYAQUIL.md).** Se compararon bandas científicas NISAR HH/HV de **7 y 19 oct** con mosaicos cartográficos OPERA de **6 y 18 oct**. El cruce de umbrales exploratorios identifica solo **7 celdas nominales de 10 m** en común entre agua abierta aparente nueva según OPERA y caída conjunta HH/HV según NISAR. El resultado evidencia una **corroboración muy limitada** y **no es una superficie inundada validada**; la cartografía OPERA procede de PNG GIBS remuestreados, no de sus GeoTIFF WTR originales. Las cuatro fechas preceden al evento del 26 oct y no prueban esa inundación.

## Cumplimiento del desafío «Dancing with the SARs» (1.3.0)

- **Aplicación interactiva con datos NISAR para seguir cambios en la superficie:** caso calibrado de cambio de señal en Guayaquil y exploración de indicios de inundación e incendio, con mapa de cambios, comparador ⇆, serie temporal animada y tablero por sector.
- **Datos de los recursos oficiales:**
  - NASA Earthdata (catálogo CMR y GIBS) y ASF (API de Vertex), en vivo y sin cuenta;
  - archivos NISAR originales como opción avanzada;
  - contraste con Sentinel-1 (banda C, vía OPERA); ALOS PALSAR y UAVSAR (banda L) como referencias en el archivo SAR;
  - contexto: población GPW y cobertura MODIS.
- **Hipótesis físicas:** la tarjeta «¿Por qué se ve así?» explica las polarizaciones y los factores naturales y humanos.
- **Usuarios:** código abierto (MIT), sin instalación, en español, con niveles de confianza explícitos.


## Limitaciones

- Con el moteado del radar, el viento sobre el agua, la sombra en laderas y la revisita de 12 días, una inundación de horas puede no verse.
- Los umbrales son una primera calibración; validar con los reportes de Segura EP, Bomberos Quito y la SNGR.
- **Madurez NISAR (ASF):** BETA **no está completamente calibrado**, PROVISIONAL está calibrado y parcialmente validado, y VALIDATED está calibrado y validado. ILLARI no mezcla estos niveles al comparar mosaicos GIBS. Véase [ASF — disponibilidad y madurez de datos NISAR](https://nisar-docs.asf.alaska.edu/availability-overview/).

En una emergencia, llama al **ECU 911**. ILLARI no reemplaza las alertas oficiales.
