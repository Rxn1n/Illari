# Registro de cambios de ILLARI

**Créditos vigentes:** Darío Proaño — **ideador y director del proyecto**; Anthony Cisneros (rxn1n) — **diseño y código**; María Teresa Loor, Manuela Palacios, Mateo Caicedo y Ana Belén Manzano — **coautores**.

*Las menciones de autoría de versiones anteriores se conservan como registro histórico; los créditos vigentes se detallan en `AUTHORS.md`.*

Fechas en hora de Ecuador. Todo el código se generó con asistencia de IA (ver `USO_DE_IA.md`).

## 1.5.2 · 16 nov 2026 · autoría y reintentos ante cortes de NASA GIBS

- **Autoría igual a la del repositorio de Darío Proaño** (`Dariuxcks/Illari`): **ideador y director del proyecto: Darío Proaño** · **diseño y código: Anthony Cisneros a.k.a rxn1n** · coautores: María Teresa Loor, Manuela Palacios, Mateo Caicedo, Ana Belén Manzano. Actualizado en la app, metadatos, exportaciones, `AUTHORS.md`, `README.md`, `LICENSE` y `USO_DE_IA.md`.
- **Reintentos cuando NASA GIBS corta la conexión.** El 16 nov 2026, GIBS dejaba sin respuesta cerca de la mitad de las peticiones WMS (el navegador las ve como «Failed to fetch»). ILLARI solo reintentaba cuando NASA respondía con un error; ahora también reintenta esos cortes (hasta 3 intentos), salvo sin internet.

## Nota técnica · 15 nov 2026 · compatibilidad SAR CMR/GIBS

- Se exige compatibilidad de track, dirección, frame, composición de polarizaciones y madurez del producto antes de comparar mosaicos NISAR.
- Las fechas detectadas solo por exploración de GIBS no aportan geometría suficiente: se informa «Comparación SAR no disponible» y no se calculan áreas de cambio.
- Si no existe pareja válida para un evento, no se elige arbitrariamente el par de fechas contiguas. Se puede probar un par anterior únicamente si también es compatible.
- Un error de NASA CMR/GIBS ya no provoca automáticamente una escena SAR simulada; la simulación se selecciona de forma explícita. Las ecuaciones de Guayaquil y Quito siguen intactas.
- Se corrige la descripción de madurez NISAR conforme a ASF: BETA sin calibración completa, PROVISIONAL calibrado/parcialmente validado y VALIDATED calibrado/validado.

## Nota documental · 15 nov 2026 · modelos predictivos (sin cambios en ecuaciones)

- Se documenta que los pesos de Guayaquil (50 % lluvia, 30 % caudal, 20 % marea) son **consideraciones exploratorias del equipo**, adoptadas por tiempo limitado del hackathon; no hubo calibración estadística de los pesos ni entrenamiento con eventos históricos.
- Se deja expresamente pendiente calibrar y validar esos parámetros con datos históricos, o emplear otro modelo predictivo adecuado. No se altera ninguna ecuación ni su valor.
- Se añade `MODELOS_PREDICTIVOS.md`, con fórmulas y separación entre las fuentes que alimentan pronósticos y las observaciones NISAR/OPERA/VIIRS/IMERG.

## 1.5.1 · 15 nov 2026 · satélites VIIRS elegidos automáticamente

- **Los focos de calor VIIRS ya no dependen de un satélite fijo.** Para cada fecha, ILLARI pregunta a NASA GIBS qué plataformas tienen datos publicados (prioridad Suomi NPP → NOAA-20 → NOAA-21) y usa las dos primeras que respondan.
  - Suomi NPP dejó de publicarse en GIBS a inicios de noviembre de 2026. Desde entonces entran NOAA-20 y NOAA-21 (mismo sensor VIIRS) sin cambios manuales; si Suomi NPP vuelve, se usa otra vez.
  - Las fechas anteriores siguen usando Suomi NPP + NOAA-20: las cifras de eventos pasados (Casitagua, inundaciones de octubre) no cambian.
  - La consulta se repite en cada sincronización (30 min).
- El fondo «color real» elige igual el satélite VIIRS que tenga imagen para esa fecha.
- La capa «Focos VIIRS» del mapa se pide por WMS (NASA no la ofrece como teselas raster) y por fin se dibuja; la leyenda dice qué satélites tienen datos ese día.
- Un archivo que NASA no publicó para una fecha se trata como «sin datos ese día», no como error.
- Autoría y dirección: **ideador y director del proyecto: Darío Proaño** · **diseño y código: Anthony Cisneros a.k.a rxn1n** · coautores: María Teresa Loor, Manuela Palacios, Mateo Caicedo, Ana Belén Manzano. Actualizado en la app, metadatos, exportaciones, `AUTHORS.md`, `README.md`, `LICENSE` y `USO_DE_IA.md`.

## 1.5.0 · 13 nov 2026 · sincronizado al momento

- **Situación actual** como vista inicial en Guayaquil y Quito:
  - toma el par NISAR comparable más reciente;
  - muestra la serie de agua de Sentinel-1 (OPERA) de los últimos 30 días, los focos VIIRS de los últimos 7 días y el último mapa DIST.
- **Lluvia medida por satélite con NASA GPM IMERG**, vía GIBS y sin clave:
  - últimas 3 h, últimas 24 h (barras cada 30 min) y últimos 7 días;
  - comparación día por día con la lluvia que reconstruye el modelo.
  - Se decodifica con la paleta oficial de GIBS (220 clases, copiada con verificación SHA-256). La capa diaria ×24 coincide con la suma de sus medias horas (21,0 frente a 20,1 mm el 4 nov).
- **Actualización automática** cada 30 minutos y al volver a la pestaña, más el botón «Actualizar». La hora de la última sincronización está siempre visible.
- **Titular confirmado:** el indicador principal del Observado es lo que NISAR detecta y otro satélite de NASA confirma; lo que ve solo el radar se muestra aparte.
- **Normalización radiométrica local (~7 km):** descuenta cambios de brillo que no son agua ni fuego (calibración PROVISIONAL frente a VALIDATED, humedad). En Quito, el par 19 → 31 oct bajó de 553 km² de «posible quemado» a 51 km², y el titular confirmado da 0 ha. Se prefieren pares de la misma versión del producto.
- **Corrección:** los focos VIIRS ya no borran píxeles quemados antes de contar la vegetación (Casitagua: 401 ha en vegetación natural).
- **Robustez ante fallas pasajeras de NASA GIBS:**
  - reintentos con espera y una imagen más chica si la grande falla;
  - si una fecha no responde, se usa otra fecha válida;
  - nunca se pasa a la escena simulada mientras el catálogo de NASA responda;
  - si una actualización falla, se conserva la última lectura buena.

## 1.4.1 · 13 nov 2026

- Autoría: **BY Anthony Cisneros a.k.a rxn1n** (autor y creador) en la cabecera de la app, en el pie del panel, en los metadatos (`<meta name="author">`) y en las exportaciones CSV/JSON.
- Nuevo `AUTHORS.md` con autor y coautores; `LICENSE` y `README.md` actualizados.
- Publicación en GitHub Pages (`rxn1n.github.io/Illari`) y Vercel.
- **Relieve más confiable:** ahora se lee de **NASA SRTM** en teselas Terrarium de AWS Open Data (sin clave ni límite de consultas). Antes, la primera visita pedía unos 8.600 puntos de elevación a Open-Meteo y podía chocar con su límite (HTTP 429), lo que dejaba el Estimado en simulación. Open-Meteo (Copernicus DEM) queda como respaldo, en serie y con reintentos. Diferencia mediana entre ambos DEM en la malla: 3 m en Guayaquil y 10 m en Quito.

## 1.4.0 · 13 nov 2026

Reducción medible de las limitaciones restantes, con datos reales:

- **Consenso de 8 modelos de lluvia** (ECMWF, GFS, ICON, GEM, JMA, Météo-France, UKMO y CMA) con dos niveles:
  - **AVISO**, cuando el percentil 75 llega a 30 mm o más;
  - **ALERTA**, cuando el promedio llega a 30 mm o más.
- **Validación del consenso** con pronósticos emitidos un día antes, 1 ago–11 nov 2026, en el Centro de Guayaquil:

  | Pronóstico | Aguaceros fuertes avisados | Falsas alarmas |
  |---|---|---|
  | Un modelo | 5 de 7 | 5 |
  | ALERTA (promedio) | 5 de 7 | 3 |
  | AVISO (percentil 75) | 7 de 7 | 14 |

  El 26 oct el AVISO pronosticaba 54 mm y cayeron 58.
- **Área quemada solo en vegetación natural** (MODIS): en el Casitagua bajó de 476 a 402 ha, frente a unas 300 ha reportadas.

## 1.3.0 · 13 nov 2026

Alineado con la página oficial del desafío (objetivos y recursos) y con la Guía de usuario de datos NISAR de ASF.

- **Archivo SAR de la ciudad**, desde la API pública de ASF, la misma de Vertex y sin cuenta:
  - NISAR, Sentinel-1, ALOS PALSAR, UAVSAR y RADARSAT-1, con línea de tiempo 2006–2026, enlaces a Vertex y Earthdata Search, y vistas HH y HV de la última pasada NISAR.
  - Hallazgo: NASA voló el radar UAVSAR sobre Guayaquil en 2013–2015.
- **Agencias socias del desafío** (CONAE SAOCOM; CSA RCM y RADARSAT-1): condiciones de acceso y enlaces.
- **¿Por qué se ve así?:** física del radar (HH, HV, doble rebote, dispersión de volumen) y factores humanos.
  - La cobertura del suelo de MODIS IGBP 2024 muestra dónde cayó el cambio.
  - La población GPW 2020 da el número mínimo de personas en zonas con agua nueva.
- **Serie temporal NISAR** de una misma órbita, con animación ▶ de todas sus pasadas.
- Las fechas BETA (sin calibrar) no se comparan con PROVISIONAL o VALIDATED, como advierte ASF.
- **Recursos oficiales del desafío** enlazados en el método.
- Resultado real: tras la tormenta del 26 oct hubo 36,9 km² de agua abierta nueva (Sentinel-1):
  - 37 % cultivos, 28 % humedales, 3 % zona urbana;
  - al menos 15 800 personas en esas zonas.

## 1.2.0 · 12 nov 2026, noche

Objetivo: resolver técnicamente las limitaciones de la ficha técnica, no solo describirlas. Todo se verificó contra los servidores reales de NASA y Open-Meteo.

- **Confirmación multisensor** con productos clasificados y validados de NASA, sin clave (GIBS):
  - **OPERA DSWx-S1 (agua, radar Sentinel-1):** cada 2–6 días; serie de agua abierta y agua nueva por sector.
  - **OPERA DSWx-HLS (agua, óptico):** cuando no hay nubes.
  - **OPERA DIST-ALERT (pérdida de vegetación, 30 m)** y **focos VIIRS** para Quito.
  - Las clases se leen con la paleta oficial, sin interpretar tonos. Nueva capa «Confirmación OPERA».
- **Validación retrospectiva de los índices:** pronósticos emitidos en el pasado (Open-Meteo Previous Runs e Historical Forecast) frente a lo ocurrido.
  - Guayaquil: aciertos y falsas alarmas de lluvia fuerte.
  - Quito: FWI en días con y sin focos VIIRS, y umbral local calibrado.
- Resultado real, 12 nov: la tormenta del 26 oct aumentó el agua abierta de Guayaquil de 212 a 232 km² (Sentinel-1, 24 → 28 oct). En Quito, el FWI mediano fue 3,7 en días con fuego frente a 0,2 sin fuego.

## 1.1.0 · 12 nov 2026 (antes del inicio del hackathon)

Verificado contra los servidores reales de NASA desde un navegador:
- CMR y GIBS responden con CORS, también desde origen `null` (abrir el archivo con doble clic).
- GIBS publica el mosaico diario `NISAR_L2_Geocoded_Polarimetric_Covariance` desde el 29 oct 2025. **No** publica la capa de 12 días por WMS, así que se eliminó.

Cambios:
- **Comparador válido:** solo se comparan pares con el mismo track, la misma dirección y el mismo modo de polarización. Si no, la comparación se bloquea y se explica el motivo. La huella de cada pasada en CMR excluye órbitas que cubren menos de media ciudad.
- **Ficha del par:** muestra fecha y hora UTC, track, dirección, frame, polarización, colección y cobertura de las dos fechas.
- **Estado de las fuentes:** cada consulta externa queda registrada con su resultado, código HTTP y hora. El registro se exporta en la escena `.json`.
- **Simulación siempre identificada:** banner, sello del mapa, marca de agua "SIMULACIÓN" (también en el PNG exportado), CSV, JSON y aviso con botón para reconectar.
- **Agua recalibrada** con la paleta real de NASA: el agua tranquila se ve oscura y azulada, no azul brillante.
- **Áreas comunicadas como aproximaciones (≈):** se indica que no están calibradas y que falta validación independiente. Los índices del modo Estimado se presentan como exploratorios, no como probabilidades.
- Avisos cuando la pasada posterior llega varios días después del evento o cuando las fechas están muy separadas.

## 1.0.0 · 12 nov 2026

- Unión de GroundWatch NISAR y Vigía Ecuador: Observado (radar NISAR) y Estimado (pronóstico), para Guayaquil y Quito.
