# ILLARI · Guayaquil through radar

How did the radar return over Guayaquil, Ecuador, change in twelve days? Compare calibrated NASA–ISRO NISAR observations from **7 and 19 October 2026** in an interactive viewer. This case study addresses *Dancing with the SARs* at NASA Space Apps 2026.

| Edition | Read the six-slide presentation | Explore the observations | Read the method and results |
|---|---|---|---|
| **English** | [PDF](https://rxn1n.github.io/Illari/docs/demostracion/ILLARI_Guayaquil_English.pdf) · [PowerPoint](docs/demostracion/ILLARI_Guayaquil_English.pptx) | [Open the viewer](https://rxn1n.github.io/Illari/docs/demostracion/visor-en.html) | [English guide](docs/demostracion/guide-en.md) |
| **Spanish** | [PDF](https://rxn1n.github.io/Illari/docs/demostracion/ILLARI_guia_demostracion.pdf) · [PowerPoint](docs/demostracion/ILLARI_guia_demostracion.pptx) | [Abrir el visor](https://rxn1n.github.io/Illari/docs/demostracion/visor.html) | [Guía en español](docs/demostracion/README.md) |

### What to look for / Qué observar

**English.** Choose HH or HV and move the before/after slider. Within the outlined 500 × 500 m window **A**, median backscatter increased by **0.67 dB in HH** and **0.64 dB in HV**. The medians across the entire urban crop were **+0.23 dB** and **+0.13 dB**, respectively. Both acquisitions predate the storm of 26 October. The maps quantify radar change; its environmental cause remains open.

**Spanish.** Elige HH o HV y mueve el divisor entre fechas. En la **ventana A** de 500 × 500 m, la mediana del cambio fue **+0,67 dB en HH** y **+0,64 dB en HV**. Para el recorte urbano completo fue **+0,23 dB** y **+0,13 dB**, respectivamente. Las dos pasadas preceden a la tormenta del 26 de octubre. Para atribuir una causa al cambio hacen falta observaciones adicionales.

[Reproduce the measurements / Reproducir las mediciones](docs/demostracion/reproduce.md) · [Acquisition identifiers](CASO_NISAR_GUAYAQUIL.md) · [Exploratory OPERA comparison](CASO_NISAR_OPERA_GUAYAQUIL.md) · [Challenge brief](https://edeon.sonoma.edu/nasaspaceapps-26/index.html)

### Live dashboard / Tablero en vivo

The [Spanish dashboard](https://rxn1n.github.io/Illari/) also offers daily NASA GIBS imagery, an option to open GCOV/GUNW files, and experimental flood and fire indicators for Guayaquil and Quito. Its forecast models use separate weather, river and terrain inputs. To use the October case offline, download either standalone viewer from [the case folder](docs/demostracion) and open the HTML file.

El tablero en vivo explora indicios de cambio y permite consultar pronósticos. El visor del caso contiene mediciones GCOV ya procesadas y se puede abrir sin conexión una vez descargado. [Guía técnica del tablero](GUIA_TECNICA.md) · [Modelos predictivos y sus límites](MODELOS_PREDICTIVOS.md)

### Credits and development history / Autoría y cronología

Project concept and direction: Darío Proaño. Design and code: Anthony Cisneros ([rxn1n](https://github.com/Rxn1n)). Coauthors: María Teresa Loor, Manuela Palacios, Mateo Caicedo and Ana Belén Manzano. [Authors](AUTHORS.md) · [MIT licence](LICENSE).

The project history records work on the dashboard and calibration on 12 November, before the 14–15 November hackathon. The repository also documents the later NISAR case analysis, viewer and subsequent revisions. The initial build used Claude (Anthropic); analysis, debugging, tests and case materials also used ChatGPT (OpenAI). [Development history](CHANGELOG.md) · [AI disclosure](USO_DE_IA.md) · Original project sites: [GitHub Pages](https://rxn1n.github.io/Illari/) and [Vercel](https://illari-three.vercel.app/).
