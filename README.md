# ILLARI

**Ideador y director del proyecto:** Darío Proaño · **Diseño y código:** Anthony Cisneros a.k.a [rxn1n](https://github.com/Rxn1n)

**Coautores · equipo ILLARI:** María Teresa Loor, Manuela Palacios, Mateo Caicedo, Ana Belén Manzano

> **Pruébalo en línea (sin instalar nada):** https://rxn1n.github.io/Illari/ · espejo en Vercel: https://illari-three.vercel.app/

Plataforma web **de código abierto (MIT)** que convierte datos de observación terrestre en información
útil para la gestión de riesgos en Ecuador. Es el proyecto para el reto *Dancing with the SARs*
(NASA Space Apps Challenge 2026).

| Módulo | Observado (radar NISAR) | Estimado (pronóstico) |
|---|---|---|
| **Guayaquil · inundaciones** (principal) | Agua nueva y agua bajo edificios o vegetación entre dos fechas, en km² por sector | Índice 0–100 a 16 días: lluvia, caudal de ríos y marea |
| **Quito · incendios** (secundario) | Áreas quemadas (caída de retrodispersión HV), en hectáreas por sector | Susceptibilidad FWI con pendiente a 16 días |

ILLARI **separa siempre la evidencia satelital de las estimaciones**: el modo Observado tiene borde sólido verde,
y el modo Estimado borde punteado ámbar. Cada vista lleva su sello y cada resultado su procedencia.

## Sincronizado al momento (1.5.0)

Al abrir, ILLARI muestra la **Situación actual** y se actualiza sola cada 30 minutos (también con el botón **Actualizar**). Arriba del panel indica la hora de la última sincronización.

| Dato en vivo | Fuente | Frecuencia / demora típica |
|---|---|---|
| Radar NISAR: el par comparable más reciente | NASA CMR + GIBS | cada 12 días; NASA publica días después |
| Agua abierta (Sentinel-1), 30 últimos días | NASA OPERA DSWx | cada 2–6 días; ~1 día de demora |
| **Lluvia medida por satélite**: últimas 3 h, 24 h y 7 días, cada 30 min | **NASA GPM IMERG** (Early y diaria, vía GIBS) | cada 30 min; ~6 h de demora |
| Focos de calor y pérdida de vegetación | NASA VIIRS + OPERA DIST | diaria |
| Lluvia, caudal de ríos y marea: últimos 30 días + 16 días de pronóstico | Open-Meteo, GloFAS | horaria |

- El **titular** del modo Observado es lo que el radar NISAR detecta **y otro satélite de NASA confirma** (Sentinel-1 para agua; VIIRS + DIST para fuego). Lo que ve solo el radar aparece aparte, marcado «solo radar».
- **Lluvia medida frente a modelada:** la tarjeta IMERG pone lado a lado la lluvia observada por satélite y la que reconstruye el modelo que alimenta el pronóstico.
- **Robustez:** si NASA GIBS falla de forma pasajera, ILLARI reintenta, usa otra fecha válida y lo explica, sin pasar a la escena simulada. Las diferencias de calibración entre fechas (p. ej. PROVISIONAL frente a VALIDATED) se descuentan con una normalización local de ~7 km.

## Uso

- **Sin instalación:** abre `index.html` con doble clic en Chrome o Edge. No hay servidor, cuentas ni claves.
- **Conexión directa a datos reales:** al abrirse, ILLARI consulta en vivo:
  - las pasadas del radar NISAR sobre la ciudad (catálogo público NASA CMR);
  - las imágenes NISAR de NASA GIBS, que compara antes y después de un evento;
  - la lluvia medida por satélite (NASA GPM IMERG), los mapas de agua de Sentinel-1 (OPERA), los focos VIIRS y el pronóstico de Open-Meteo.
- **Sin descargas:** no hay que descargar nada. Si no hay internet, muestra una escena simulada marcada como tal.
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

**Observado en vivo (NASA GIBS).** Primero se verifica que las dos fechas sean comparables: mismo track, misma dirección y mismo modo de polarización. Si no lo son, la comparación se bloquea.
En la visualización de NASA (co-polar HH en rojo y azul, cruzada HV en verde), medida sobre Guayaquil, el agua tranquila se ve **oscura y azulada**, la vegetación verde intensa y la ciudad amarilla.
Tras suavizar los canales (5×5), ILLARI marca:
- *posible agua nueva*: píxeles que pasan a oscuros y azulados (R+G+B < 200 y B/(R+G+B) > 0,24) y pierden brillo;
- *posible agua bajo edificios*: zonas donde el canal rojo sube con fuerza;
- *posible área quemada*: zonas verdes cuyo canal verde cae con fuerza.

Son imágenes de 8 bits: las áreas son **aproximaciones** sin validación independiente, y así se indica en la interfaz, la procedencia y las exportaciones.

**Observado, inundación con archivos (avanzado).**
1. Cada imagen GCOV se re-muestrea a una malla común (promedio por bloques), se filtra el moteado (3×3) y se pasa a dB.
2. Se marca *agua nueva* donde la imagen posterior está bajo el umbral de agua (Otsu automático, o manual)
   y al menos 3 dB más oscura que la anterior.
3. Se marca *posible inundación bajo vegetación o edificios* donde la HH sube 3 dB o más (doble rebote).
4. Se descartan las cotas sobre 25 m y los píxeles aislados.

**Observado, incendio.** Se marca *posible área quemada* donde la HV cae 2,5 dB o más sobre vegetación previa.
Con productos GUNW se usa en cambio la pérdida de coherencia.

**Estimado.** Usa el índice FWI canadiense (validado con el caso de prueba oficial) y un índice compuesto de
inundación. Están documentados en la sección "Método, fuentes y limitaciones" de la app.

## Confirmación y validación (1.2.0)

- **Confirmación multisensor (Observado):** el agua nueva del radar se contrasta con OPERA DSWx-S1 (Sentinel-1, cada 2–6 días) y DSWx-HLS (óptico). Las áreas quemadas se contrastan con OPERA DIST-ALERT (30 m) y con focos VIIRS. Las clases se leen con la paleta oficial de cada producto.
- **¿El pronóstico habría avisado? (Estimado):** se comparan pronósticos emitidos en el pasado con lo ocurrido.
  - Guayaquil: aciertos y falsas alarmas de lluvia fuerte.
  - Quito: FWI en días con y sin fuego, y umbral local.
- **Resultados reales del 12 nov:**
  - Sentinel-1 mostró que el agua abierta de Guayaquil pasó de 212 a 232 km² tras la tormenta del 26 oct.
  - VIIRS confirmó 4 días de fuego en el Casitagua (17–20 sep).
  - El pronóstico avisó 5 de 7 aguaceros fuertes, pero subestimó el del 26 oct (17 mm frente a 58).

## Cumplimiento del desafío «Dancing with the SARs» (1.3.0)

- **Aplicación interactiva con datos NISAR para seguir cambios en la superficie:** inundaciones en Guayaquil e incendios en Quito, con mapa de cambios, comparador ⇆, serie temporal animada y tablero por sector.
- **Datos de los recursos oficiales:**
  - NASA Earthdata (catálogo CMR y GIBS) y ASF (API de Vertex), en vivo y sin cuenta;
  - archivos NISAR originales como opción avanzada;
  - otras frecuencias: Sentinel-1 (banda C, vía OPERA), ALOS PALSAR y UAVSAR (banda L);
  - contexto: población GPW y cobertura MODIS.
- **Hipótesis físicas:** la tarjeta «¿Por qué se ve así?» explica las polarizaciones y los factores naturales y humanos.
- **Usuarios:** código abierto (MIT), sin instalación, en español, con niveles de confianza explícitos.

## Autoría

- **Ideador y director del proyecto:** Darío Proaño, responsable de la concepción original y la dirección general del proyecto.
- **Diseño y código:** Anthony Cisneros a.k.a rxn1n ([github.com/Rxn1n](https://github.com/Rxn1n)).
- **Coautores (equipo ILLARI):** María Teresa Loor, Manuela Palacios, Mateo Caicedo, Ana Belén Manzano ([`AUTHORS.md`](AUTHORS.md)).

## Uso de IA

El código y la documentación se generaron con asistencia de Claude (Anthropic). Los detalles están en `USO_DE_IA.md` y los cambios en `CHANGELOG.md`.
Se preparó antes del 14 nov 2026: confirmen con su Local Lead si se permite presentarlo como base y declárenlo en el envío.

## Limitaciones

- Con el moteado del radar, el viento sobre el agua, la sombra en laderas y la revisita de 12 días, una inundación de horas puede no verse.
- Los umbrales son una primera calibración; validar con los reportes de Segura EP, Bomberos Quito y la SNGR.
- Los productos NISAR PROVISIONAL y BETA están calibrados pero aún en validación.

En una emergencia, llama al **ECU 911**. ILLARI no reemplaza las alertas oficiales.
