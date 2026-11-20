# ILLARI — Ecuaciones de los modelos predictivos / Predictive model equations

**Proyecto / Project:** ILLARI — NASA Space Apps Challenge 2026, *Dancing with the SARs*  
**Ideador y director del proyecto / Project originator and director:** Darío Proaño  
**Diseño y código / Design and code:** Anthony Cisneros (rxn1n)  
**Versión analizada / Version reviewed:** 1.5.1 · 15 noviembre / November 2026  
**Naturaleza / Scope:** documentación metodológica de las ecuaciones **ya implementadas**; no propone cambios en cálculos ni resultados / documentation of **existing** equations; no changes to code or output.

---

# Español

## 1. Qué predice ILLARI y qué observa

ILLARI tiene dos procesos **independientes en el código**. **Estimado** calcula índices de condiciones favorables a inundaciones en Guayaquil y propagación del fuego en Quito mediante meteorología y modelos hidrológicos. **Observado** compara adquisiciones radar **NISAR** anteriores y posteriores para identificar cambios posibles de agua o vegetación y los contrasta con otros productos. El radar NISAR **no alimenta directamente** los índices predictivos actuales; tampoco se han estimado sus coeficientes con observaciones satelitales. No son probabilidades calibradas de ocurrencia.

- **Pronósticos y relieve:** Open-Meteo (lluvia, temperatura, humedad, viento), Open-Meteo Flood / **GloFAS** (caudal fluvial modelado), Open-Meteo Marine (altura del nivel del mar modelada) y **NASA SRTM** (elevación y pendiente, con respaldo Copernicus DEM).
- **Observaciones y contraste:** **NISAR** (cambios en retrodispersión o coherencia), **OPERA DSWx-S1 / DSWx-HLS** (mapas de agua de Sentinel-1 e imágenes ópticas), **OPERA DIST-ALERT** (alteración de vegetación), **VIIRS** (focos térmicos) y **NASA GPM IMERG** (precipitación estimada por satélites). Son evidencias complementarias, no variables directas del índice compuesto ni del FWI.
- **Contexto:** MODIS IGBP (cobertura terrestre) y GPW (población estimada) permiten interpretar la exposición, pero tampoco modifican las ecuaciones meteorológicas.

## 2. Guayaquil: índice exploratorio de peligro de inundación

### 2.1. Índice compuesto actualmente implementado

```text
I(t,x) = 100 × [ 0,50 R(t,x) + 0,30 Q(t) + 0,20 M(t) ]
```

Las tres entradas se expresan en una escala adimensional entre 0 y 1: **R** = precipitación, **Q** = anomalía relativa de caudales Daule/Babahoyo y **M** = nivel del mar o marea del Golfo de Guayaquil. **I** se interpreta como un índice 0–100 de peligro relativo, **no como porcentaje de probabilidad**.

**Justificación de los pesos:** 50 % (lluvia), 30 % (caudal) y 20 % (marea) son **consideraciones iniciales del equipo ILLARI**, elegidas como hipótesis física y operacional por el **tiempo limitado de desarrollo del hackathon**. **No se calcularon por regresión, ajuste multivariable, optimización ni validación contra un inventario histórico de inundaciones**. La etapa de estimar estadísticamente esos pesos, evaluar sus umbrales y su incertidumbre, **o utilizar otra ecuación predictiva ajustada a datos históricos**, no se realizó debido al tiempo disponible. Por tanto **no deben interpretarse como coeficientes calibrados ni como probabilidades de inundación**. **Las ecuaciones se conservan sin cambios.**

### 2.2. Precipitación acumulada

```text
P24(t) = precipitación total del día t en mm
P72(t) = P24(t) + P24(t−1) + P24(t−2)
R(t)   = max{ clamp(P24(t)/80), clamp(P72(t)/150) }
clamp(z) = min(1, max(0,z))
```

Los divisores **80 mm/24 h** y **150 mm/72 h** son umbrales operativos del programa que requieren justificación local. La ponderación 50 % se aplica a **R**, no a los milímetros sin normalizar. Los datos de 24 h provienen del pronóstico diario de Open-Meteo. En cada posición y día el código calcula el acumulado y luego el máximo de las dos razones.

### 2.3. Componente fluvial

```text
Qj(t) = clamp[ ( qj(t) − qj,50 ) / ( qj,99 − qj,50 ) ]
Q(t)  = max{ QDaule(t), QBabahoyo(t) }
```

**qj(t)**: caudal modelado del río j (m³/s); **qj,50** y **qj,99**: percentiles históricos 50 y 99 obtenidos mediante GloFAS/Open-Meteo para la serie solicitada de 1984 a julio de 2022. El programa usa el mayor de los dos valores normalizados. Si el historial o el servicio fluvial falta, el código actual puede reemplazar su componente por **0**; esto es una **limitación de disponibilidad**, no evidencia de caudal normal.

### 2.4. Componente marino

```text
hmax(t) = máximo diario de las alturas horarias del nivel del mar modelado
M(t)    = clamp[ ( hmax(t) − h50 ) / ( h99 − h50 ) ]
```

**h50** y **h99** se calculan con las alturas máximas diarias disponibles en la ventana consultada (~30 días pasados y 16 futuros), **no con una climatología mareográfica extensa**. El uso del máximo diario simplifica la coincidencia horaria entre marea y lluvia. Este componente tampoco demuestra por sí mismo una inundación.

### 2.5. Relieve, interpolación espacial y mapa

```text
S(h) = clamp[ (12 − h)/9 ]
wij  = dij^(−2) / Σk dik^(−2)        (interpolación IDW, con distancia regularizada)
Imapa(t,x) = S[h(x)] × Σj wij(x) Ij(t)
```

El mapa interpola el índice compuesto de estaciones/puntos de malla próximos y lo multiplica por la **susceptibilidad por elevación**, calculada con NASA SRTM y respaldo Copernicus DEM. **h** se expresa en metros. Los umbrales 12 m y 9 m reflejan una hipótesis simplificadora: no representan un modelo hidráulico de drenaje urbano ni incluyen diques o alcantarillado. Las cifras del mapa pueden ser inferiores a **I** por la corrección de terreno. El código utiliza una regularización de distancia mínima para evitar divisiones por cero.

### 2.6. Consenso meteorológico adicional (no reemplaza el índice)

El módulo de consenso utiliza hasta ocho modelos meteorológicos disponibles (ECMWF, GFS, ICON, GEM, JMA, Météo-France, UKMO y CMA):

```text
μP(t)   = (1/n) × Σm Pm(t)
P75(t)  = percentil 75 de {Pm(t)}
AVISO   = P75(t) ≥ 30 mm/día
ALERTA  = μP(t)  ≥ 30 mm/día
```

Este consenso **se presenta como una señal adicional de lluvia intensa**. No sustituye los pesos 50/30/20 del índice de inundación ni constituye una calibración de inundaciones. El respaldo retrospectivo del programa contrasta pronóstico de lluvia contra un análisis de lluvia del mismo ecosistema Open-Meteo, no contra una base externa de inundaciones reales.

## 3. Quito: Canadian Fire Weather Index (FWI) y pendiente

### 3.1. Entradas y memoria de humedad

Se incorporan **T** (temperatura al mediodía, °C), **H** (humedad relativa, %), **W** (viento, km/h) y **r** (lluvia acumulada en las 24 h usadas por el algoritmo, mm), procedentes de Open-Meteo. El sistema FWI es **recursivo**: los índices de humedad del combustible de un día condicionan los del siguiente:

```text
(FFMCt, DMCt, DCt) = f(FFMCt−1, DMCt−1, DCt−1, Tt, Ht, Wt, rt)
ISI(t) = g(FFMCt, Wt)
BUI(t) = h(DMCt, DCt)
FWI(t) = k(ISI(t), BUI(t))
```

- **FFMC:** Fine Fuel Moisture Code (humedad de combustibles finos).
- **DMC:** Duff Moisture Code (sequedad de materia orgánica superficial).
- **DC:** Drought Code (sequedad profunda).
- **ISI:** Initial Spread Index (propagación inicial asociada a combustible fino y viento).
- **BUI:** Buildup Index (combustible disponible).
- **FWI:** índice de intensidad potencial de incendio basado en ISI y BUI.

La implementación comienza cada serie con **FFMC = 85, DMC = 6, DC = 15**. Emplea los factores **le = 9, lf = 1,39**. Esas condiciones iniciales y factores son supuestos computacionales y requieren evaluar la sensibilidad local.

### 3.2. Ecuaciones explícitas de ISI, BUI y FWI implementadas

```text
m  = 147,2 × (101 − FFMC)/(59,5 + FFMC)
sf = 19,115 × exp(−0,1386m) × [1 + m^5,31/(4,93×10^7)]
ISI = sf × exp(0,05039W)

Si DMC ≤ 0,4DC:
   BUI = 0,8DC·DMC/(DMC + 0,4DC)
Si DMC > 0,4DC:
   BUI = DMC − [1 − 0,8DC/(DMC + 0,4DC)] × [0,92 + (0,0114DMC)^1,7]
BUI = max(0, BUI)

Si BUI ≤ 80:
   b = 0,1ISI × (0,626BUI^0,809 + 2)
Si BUI > 80:
   b = 0,1ISI × [1000/(25 + 108,64exp(−0,023BUI))]
Si b ≤ 1: FWI = b
Si b > 1: FWI = exp{2,72 × [0,434 ln(b)]^0,647}
```

El resto de las ecuaciones del sistema canadiense actualizan diariamente FFMC, DMC y DC por temperatura, humedad, precipitación y viento; se implementan en `fwiStep()` (líneas ~720–740 de `index.html`). El FWI **no es una probabilidad porcentual de ignición**.

### 3.3. Adaptación topográfica de ILLARI

La elevación SRTM permite estimar la pendiente local **θ** en grados, mediante diferencias centrales de alturas vecinas:

```text
θ = (180/π) × atan{ sqrt[(∂z/∂x)^2 + (∂z/∂y)^2] }
Fpend(θ) = min{4, exp(0,0693θ)}
ISIaj = ISIinterp × Fpend(θ)
FWIaj = FWI( ISIaj, BUIinterp )
```

La corrección por pendiente, incluido el **límite 4**, es una **adaptación del equipo**: no es parte de la fórmula canadiense estándar y no constituye un ajuste local validado. El valor de **FWIaj** expresa peligro meteorológico-topográfico relativo, no predice con certeza dónde comenzará un incendio.

### 3.4. Interpolación y sectores

El programa calcula series FWI de puntos meteorológicos, interpola ISI y BUI sobre una cuadrícula mediante **IDW de exponente 2**, y aplica el factor local de pendiente **antes de recalcular FWI**. Para sectores concretos se usa su serie meteorológica local y la pendiente de la celda más cercana. Por eso el FWI mostrado en el mapa y el de cada sector no tienen por qué coincidir exactamente.

## 4. ¿Cómo se relacionan satélites y ecuaciones?

| Instrumento/producto | Variable o resultado | Papel en ILLARI |
|---|---|---|
| NISAR (SAR banda L, GCOV/GUNW) | Retrodispersión HH/HV o coherencia, antes/después | **Observación**, posible agua nueva o pérdida de vegetación; no entrada directa del pronóstico |
| OPERA DSWx-S1 / DSWx-HLS | Clasificación de agua a distintas fechas | **Corroboración** temporal/espacial de agua |
| OPERA DIST-ALERT | Alteración/pérdida de vegetación | Contexto de cambio; no confirma por sí solo causa incendiaria |
| VIIRS | Anomalías térmicas | Corroboración de presencia de fuego próxima en tiempo y espacio |
| GPM IMERG | Lluvia estimada a partir de satélites | Comparación de lluvia observada con la modelada; **no sustituye** P24 del pronóstico |
| SRTM (NASA) | Elevación / pendiente | **Entrada directa**: multiplicador por cota en Guayaquil y pendiente en Quito |
| MODIS IGBP / GPW | Cobertura de suelo y población estimada | Contexto de exposición, sin entrenar ecuaciones |
| Open-Meteo meteorología | Precipitación, T, H, viento | **Entradas directas** a R y FWI |
| GloFAS/Open-Meteo Flood | Caudales modelados | **Entrada directa** a Q |
| Open-Meteo Marine | Altura del nivel del mar modelada | **Entrada directa** a M |

**Secuencia real:** pronóstico meteorológico e hidrológico + relieve → índice de peligro estimado; en paralelo, observación satelital antes/después → inferencias de cambios → contraste con otros satélites. La coincidencia entre mapas no prueba causalidad ni calibra los modelos.

## 5. Limitaciones y trabajo no realizado por tiempo

1. **Guayaquil:** los pesos 0,50 / 0,30 / 0,20 y umbrales no se calibraron con inundaciones históricas; tampoco se entrenó un modelo alternativo. Esta fue una **decisión explícita del equipo por las restricciones temporales del hackathon**.
2. **Quito:** el FWI estándar tiene fundamento publicado, pero su ajuste topográfico y calibración local para ecosistemas ecuatorianos requieren evaluación.
3. **Predicción ≠ observación:** no atribuir al radar NISAR la predicción meteorológica. El SAR ayuda a observar cambios en fechas disponibles, no anticipa por sí mismo eventos futuros.
4. **Calidad de evidencia:** mosaicos NISAR en falso color de 8 bits y mapas OPERA no reemplazan automáticamente mediciones de campo; el respaldo retrospectivo de lluvia no valida ocurrencia de inundación.
5. **Ausencia de datos:** el código actual puede asignar valor cero a factores fluvial/marino no disponibles, reduciendo el índice sin demostrar condiciones seguras.
6. **Validación futura:** obtener registros de inundación/incendio por fecha y sector; separar periodos de entrenamiento/validación/prueba; estimar sensibilidad, especificidad, precisión, Brier y calibración; documentar incertidumbre y posibles modelos de comparación.

**Código fuente principal:** [index.html](index.html) · `rainScore`, `elevSusc`, `buildFlood`, `fwiStep`, `fwiFromIB`, `buildFire`, `loadMulti`, `loadBack`.

---

# English

## 1. Forecasting versus Earth observation

ILLARI deliberately separates two pipelines. **Estimated** calculates exploratory environmental hazard indices using meteorological and hydrological models. **Observed** detects potential changes in NISAR acquisitions and seeks corroboration from other Earth-observation products. **NISAR is not a direct input to the existing forecast equations**, and the coefficients were not trained on satellite-derived event labels.

**Direct model inputs:** Open-Meteo weather forecasts (rain, temperature, relative humidity, wind), Open-Meteo Flood/GloFAS modelled river discharge, Open-Meteo Marine modelled sea level, and NASA SRTM topography (Copernicus DEM fallback). **Observational checks:** NISAR SAR, OPERA DSWx-S1/HLS water maps, OPERA DIST vegetation disturbance, VIIRS thermal hotspots and GPM IMERG satellite-derived rainfall. MODIS land cover and GPW population provide exposure context.

## 2. Guayaquil: exploratory flood hazard index

```text
I(t,x) = 100 × [ 0.50 R(t,x) + 0.30 Q(t) + 0.20 M(t) ]
R(t) = max{ clamp(P24(t)/80), clamp(P72(t)/150) }
P72(t) = P24(t) + P24(t−1) + P24(t−2)
Qj(t) = clamp[(qj(t) − qj,50)/(qj,99 − qj,50)]
Q(t) = max{QDaule(t), QBabahoyo(t)}
M(t) = clamp[(hmax(t) − h50)/(h99 − h50)]
clamp(z) = min(1,max(0,z))
```

`P24` and `P72` are forecast accumulated rainfall (mm); river flow `qj` (m³/s) is compared with historical GloFAS percentiles **50 and 99**; the daily maximum modelled sea-level height `hmax` is normalized with percentiles **50 and 99** from the available short window of sea-level forecasts/analyses. The ratios are bounded to 0–1.

**Why these weights?** The **50% rainfall, 30% river flow and 20% tide weights are exploratory assumptions adopted by the ILLARI team because of the limited hackathon development time.** They are **not statistically estimated, fitted by regression or independently validated against a historical flood-event dataset**. Estimating weights and assessing uncertainty against independent records, **or selecting and validating an alternative forecasting equation**, were not completed due to time constraints. The implemented equations and numerical weights remain unchanged. **The 0–100 index is not a calibrated flood probability.**

**Terrain and spatial interpolation:**

```text
S(h) = clamp[(12−h)/9]
wij = dij^(−2) / Σk dik^(−2)    [IDW, regularized short distance]
Imap(t,x) = S[h(x)] × Σj wij(x) Ij(t)
```

Elevation `h` comes primarily from NASA SRTM (Copernicus DEM fallback). These thresholds are simplified susceptibility assumptions, not urban drainage hydraulics.

**Additional eight-model rainfall consensus (separate from flood index):**

```text
meanP(t) = (1/n) × Σm Pm(t)
P75(t)  = 75th percentile of daily precipitation forecast models
WATCH   = P75(t) ≥ 30 mm/day
ALERT   = meanP(t) ≥ 30 mm/day
```

This is a rainfall warning heuristic, **not a fitted flood prediction model**. The existing weather hindcast compares historical forecasts with analysis from the Open-Meteo model ecosystem, rather than independently observed flood occurrence.

## 3. Quito: Canadian Fire Weather Index and slope correction

The Fire Weather Index (FWI) system takes daily noon **temperature T (°C), relative humidity H (%), wind W (km/h)** and accumulated **precipitation r (mm)**, and maintains recursive moisture state variables:

```text
(FFMCt, DMCt, DCt) = f(previous states, Tt, Ht, Wt, rt)
ISI = g(FFMC, W)
BUI = h(DMC, DC)
FWI = k(ISI, BUI)
```

FFMC = Fine Fuel Moisture Code; DMC = Duff Moisture Code; DC = Drought Code; ISI = Initial Spread Index; BUI = Buildup Index. ILLARI initializes **FFMC=85, DMC=6, DC=15**, with implementation factors **le=9, lf=1.39**.

**Implemented final formulae:**

```text
m = 147.2 × (101−FFMC)/(59.5+FFMC)
sf = 19.115 × exp(−0.1386m) × [1+m^5.31/(4.93×10^7)]
ISI = sf × exp(0.05039W)

If DMC ≤ 0.4DC:
  BUI = 0.8DC·DMC/(DMC+0.4DC)
Else:
  BUI = DMC − [1−0.8DC/(DMC+0.4DC)]×[0.92+(0.0114DMC)^1.7]
BUI = max(0,BUI)

If BUI ≤ 80: b = 0.1ISI × (0.626BUI^0.809+2)
Else:        b = 0.1ISI × [1000/(25+108.64exp(−0.023BUI))]
If b ≤ 1: FWI = b
Else:      FWI = exp{2.72 × [0.434ln(b)]^0.647}
```

The full daily FFMC, DMC and DC recursion is implemented in `fwiStep()` in `index.html`.

**ILLARI-specific topographic adjustment:**

```text
θ = (180/π) × atan{ sqrt[(∂z/∂x)^2 + (∂z/∂y)^2] }
Fslope(θ) = min{4, exp(0.0693θ)}
ISIadjusted = ISIinterpolated × Fslope(θ)
FWIadjusted = FWI(ISIadjusted, BUIinterpolated)
```

NASA SRTM supplies elevations to calculate terrain slopes. The capped exponential factor is **a project adaptation, not the standard Canadian FWI formula**, and its local performance is not independently calibrated. Spatial weights use inverse-distance weighting with power **2**. This outputs a **relative potential fire-weather hazard**, not a statistical probability that a wildfire will ignite.

## 4. Relationship among satellite products and forecasts

| Source | Role in existing ILLARI |
|---|---|
| NISAR GCOV/GUNW | SAR backscatter/coherence change detection: **observation**, not a direct forecast input |
| OPERA DSWx-S1/HLS | Water classifications and time-separated corroboration |
| OPERA DIST | Vegetation disturbance mapping; not proof of fire cause on its own |
| VIIRS | Thermal hotspots as supporting evidence of fire |
| GPM IMERG | Satellite-estimated rainfall for observational comparison, **not the rainfall fed to the current index** |
| NASA SRTM | **Direct terrain input:** flood elevation susceptibility and fire slope |
| MODIS IGBP / GPW | Land cover and population/exposure context |
| Open-Meteo weather | **Direct forecast input** to rainfall score and Canadian FWI |
| Open-Meteo Flood / GloFAS | **Direct forecast input** to river score |
| Open-Meteo Marine | **Direct forecast input** to sea-level score |

**Key limitation:** Satellite-observed change, physical corroboration, forecast hazard and independently validated event prediction are **four different claims**. They should not be conflated.

## 5. Work deferred because of time constraints

The team did not have enough hackathon time to calibrate the flood weights or develop an alternative statistically trained flood predictor. Future work should collect georeferenced, dated disaster records, calibrate against independent observations, evaluate held-out periods and compare interpretable baselines with more advanced models. Model uncertainties, missing data and product acquisition timing must be documented.

**Code reference:** [index.html](index.html), functions `rainScore`, `elevSusc`, `buildFlood`, `fwiStep`, `fwiFromIB`, `buildFire`, `loadMulti`, `loadBack`.

---

## Fuentes técnicas / Technical sources

- [Código de ILLARI / ILLARI source](https://github.com/Rxn1n/Illari/blob/main/index.html) — implementación exacta / exact implementation.
- [Natural Resources Canada — Canadian Forest Fire Weather Index (FWI) System](https://cwfis.cfs.nrcan.gc.ca/background/summary/fwi).
- Van Wagner, C. E. (1987). *Development and Structure of the Canadian Forest Fire Weather Index System*. Canadian Forestry Service.
- [NASA / ASF — NISAR data documentation](https://nisar-docs.asf.alaska.edu/).
- [NASA OPERA](https://www.jpl.nasa.gov/go/opera/).
- [NASA GPM IMERG](https://gpm.nasa.gov/data/imerg).
- [Open-Meteo — Weather Forecast API](https://open-meteo.com/en/docs); [Flood API](https://open-meteo.com/en/docs/flood-api); [Marine API](https://open-meteo.com/en/docs/marine-weather-api).

*Documento descriptivo de un prototipo exploratorio. No reemplaza los sistemas oficiales de gestión de riesgos / Exploratory prototype documentation; not an official hazard warning service.*
