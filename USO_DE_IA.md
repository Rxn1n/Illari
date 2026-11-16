# Uso de inteligencia artificial en ILLARI

Las reglas de NASA Space Apps permiten usar IA, pero piden indicar con claridad dónde y cómo se usó.
El código y los datos generados con IA deben reconocerlo en su texto descriptivo y en sus metadatos.

| Parte del proyecto | ¿Se usó IA? | Cómo |
|---|---|---|
| `index.html` (interfaz, mapa, detección de cambios, índices, exportación) | Sí | Generado con Claude (Anthropic) a partir de la propuesta de Darío Proaño (ideador y director del proyecto) y de las indicaciones de Anthony Cisneros (rxn1n), diseño y código, y de los coautores. Revisado y probado con pruebas automáticas. El reconocimiento está en el comentario inicial del archivo y en la etiqueta `<meta name="ai-generated">`. |
| Calibración del agua en el modo en vivo | Sí, con verificación | La regla (píxel oscuro y azulado) se midió el 12 nov 2026 sobre la imagen NISAR real de Guayaquil servida por NASA GIBS. |
| README, guía, resumen técnico y ficha técnica | Sí | Redactados con Claude; aprobados por el autor. |
| Datos satelitales y de pronóstico | No | Se leen en vivo de NASA (CMR, GIBS) y Open-Meteo, sin modificación por IA. |
| Imágenes y video del pitch | A definir | Si se usa IA para imágenes o video, deben llevar una marca de agua visible que diga que son generados por IA. |

**Responsabilidad.** El equipo verifica cada resultado antes de presentarlo. Ninguna cifra de la escena simulada debe presentarse como medición.

**Para el formulario de envío.** En la pregunta "Did you utilize any Artificial Intelligence tools?" respondan **Sí**.
Describan: "Code, documentation and calibration support generated with Claude (Anthropic); all satellite data come unmodified from NASA CMR/GIBS and Open-Meteo; outputs verified by the team."
