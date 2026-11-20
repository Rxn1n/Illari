# Spanish · Guayaquil vista por radar

[English](guide-en.md) · **Spanish**

[Explorar el caso de Guayaquil](https://rxn1n.github.io/Illari/docs/demostracion/visor.html) · [Leer la presentación en PDF](ILLARI_guia_demostracion.pdf) · [Descargar PowerPoint](ILLARI_guia_demostracion.pptx) · [Mapa comparativo](mapa.png) · [Visor para uso sin conexión](visor.html)

**Resultado de la evaluación.** ILLARI demuestra que una persona puede usar observaciones NISAR reales para localizar y cuantificar cambios de la señal radar en la superficie de Guayaquil. El caso compara el mismo recorte urbano los días **7 y 19 de octubre de 2026**. El reto pide una aplicación interactiva para seguir y visualizar cambios en la superficie terrestre mediante NISAR. Este caso aporta evidencia de esa capacidad en una ciudad y un intervalo concreto. La identificación de la causa física de los cambios, incluida una posible inundación, requiere validación adicional. [Enunciado publicado por la sede de Sonoma](https://edeon.sonoma.edu/nasaspaceapps-26/index.html)

## Qué objetivos pueden comprobarse

| Objetivo | Evidencia disponible | Alcance |
|---|---|---|
| Utilizar radar NISAR real | Dos productos GCOV PROVISIONAL comparten track 112 descendente, frame 090, modo 4005 y polarización DHDH. Sus identificadores y horas de adquisición constan en la ficha del par. [Procedencia](../../CASO_NISAR_GUAYAQUIL.md) | El tablero en vivo presenta mosaicos diarios GIBS en falso color. El visor de este caso emplea valores calibrados extraídos de los GCOV. |
| Permitir una comparación interactiva | El divisor permite examinar el mismo lugar en las dos fechas. Los controles HH y HV cambian la polarización de las dos imágenes y del mapa de diferencias. [Visor del caso](https://rxn1n.github.io/Illari/docs/demostracion/visor.html) | Los cuatro recortes comparten una malla de 1335 × 1327 píxeles de 10 m en UTM 17S. Las vistas se redujeron para la pantalla después del cálculo. |
| Localizar y cuantificar el cambio | Para cada píxel se restó la señal del día 7 a la del día 19, expresada en decibelios. Las medianas de esas diferencias son **+0,23 dB en HH** y **+0,13 dB en HV**. [Mapa de ambas polarizaciones](mapa.png) | Los valores describen el retorno del radar en el recorte analizado. La humedad, la vegetación y la estructura de la superficie pueden influir en ese retorno. |

## Cómo leer el visor

El panel **Antes y después** abre con la polarización **HH**, en la que el radar emite y recibe la señal en horizontal. Al mover **Posición del divisor** sobre la ribera, se alternan las adquisiciones del 7 y del 19 con el encuadre y la escala de grises fijos. La barra de 2 km proporciona una referencia espacial. Al elegir **HV**, se observa el componente recibido en vertical tras una emisión horizontal.

El panel **Cambio de señal** muestra simultáneamente la diferencia para la polarización elegida. El **azul** indica que el 19 llegó menos señal al radar, el **naranja** que llegó más y los tonos próximos al blanco indican diferencias cercanas a cero. Los extremos de la escala corresponden a cambios de −6 dB o inferiores y de +6 dB o superiores. La cifra bajo el mapa resume todo el recorte. Una mediana cercana a cero puede coexistir con áreas locales de aumento y disminución.

Las adquisiciones también se pueden localizar en **Guayaquil → Observado** del tablero principal. Las filas del 7 y 19 de octubre con **T112 D · F090 · DHDH · PROVISIONAL** corresponden al par documentado. El visor del caso conserva ese intervalo para consultas posteriores. [Tablero público](https://rxn1n.github.io/Illari/)

### Localizar la ventana A

El recuadro A marca una zona de 500 × 500 m centrada en 2,14843° S, 79,91730° O. Al alternar HH y HV, el contorno conserva su posición. En sus 2.500 píxeles, la mediana del cambio fue +0,67 dB en HH y +0,64 dB en HV. Se eligió para ilustrar un aumento local. Puede ocultarse con «Mostrar el recuadro A». [Reproducir estos valores](reproduce.md)

## Interpretación ambiental

El contraste exploratorio con OPERA DSWx-S1 utilizó mapas de agua de los días **6 y 18 de octubre**, cada uno un día anterior a la observación NISAR correspondiente. En el área común, la regla de disminución simultánea en HH y HV identificó **5265 celdas**. OPERA marcó **1413 celdas equivalentes** como agua abierta nueva aparente. Ambas reglas coincidieron en **7 celdas**, aproximadamente el **0,50 %** de las señaladas por OPERA. La comparación usó mosaicos de visualización OPERA remuestreados a la malla NISAR. Esa coincidencia limitada deja abierta la interpretación hidrológica. Además, la tormenta del 26 de octubre sucedió después de las cuatro observaciones. [Método, umbrales y resultados](../../CASO_NISAR_OPERA_GUAYAQUIL.md)

## Validación y reproducibilidad

| Tema | Estado o siguiente paso | Qué permite comprobar |
|---|---|---|
| Científica | Estudiar un episodio documentado con observaciones compatibles anteriores y posteriores, usar bandas de agua WTR originales de OPERA y contrastarlas con una referencia independiente sobre el terreno. | Cuántas zonas inundadas se identifican correctamente y dónde aparecen omisiones o falsas alarmas. |
| Reproducibilidad | El código público regenera los dos mapas de diferencia NISAR y sus medianas a partir de los GCOV originales o de los cuatro GeoTIFF. | Un tercero puede comprobar las cifras del recorte y la ventana A. [Datos y comandos](reproduce.md) |

Datos de NASA–ISRO NISAR distribuidos por ASF DAAC. Ideación y dirección del proyecto, Darío Proaño. Diseño y código de ILLARI, Anthony Cisneros (rxn1n). Esta evaluación se preparó con asistencia de ChatGPT.
