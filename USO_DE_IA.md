# Uso de inteligencia artificial en ILLARI

**Ideador y director del proyecto:** Darío Proaño. **Diseño y código:** Anthony Cisneros (rxn1n).

Las reglas de NASA Space Apps permiten usar IA, pero piden indicar con claridad dónde y cómo se usó.
El código y los datos generados con IA deben reconocerlo en su texto descriptivo y en sus metadatos.

| Parte del proyecto | ¿Se usó IA? | Cómo |
|---|---|---|
| `index.html` (interfaz, mapa, detección de cambios, índices, exportación) | Sí | Generado con Claude (Anthropic) a partir de la propuesta de Darío Proaño (ideador y director del proyecto) y de las indicaciones de Anthony Cisneros (rxn1n), diseño y código, y de los coautores. Revisado y probado con pruebas automáticas. El reconocimiento está en el comentario inicial del archivo y en la etiqueta `<meta name="ai-generated">`. |
| Calibración del agua en el modo en vivo | Sí, con verificación | La regla (píxel oscuro y azulado) se midió el 12 nov 2026 sobre la imagen NISAR real de Guayaquil servida por NASA GIBS. |
| README, guía, resumen técnico y ficha técnica | Sí | Redactados con Claude; aprobados por la dirección del proyecto. |
| Revisión del selector NISAR y caso de demostración de Guayaquil | Sí | ChatGPT (OpenAI) asistió en la corrección y las pruebas del selector CMR/GIBS y en la preparación del visor, el mapa, la guía y la presentación. El visor y el mapa representan mediciones de los recortes GCOV entregados por el equipo. |
| Datos satelitales y de pronóstico | No | Se leen en vivo de NASA (CMR, GIBS) y Open-Meteo, sin modificación por IA. |
| Material de evaluación English / Spanish | Sí | ChatGPT asistió en la redacción, traducción y construcción de las presentaciones y visores. Los mapas reproducen mediciones de radar del equipo. El recuadro A identifica un subconjunto de su malla. |

**Responsabilidad.** El equipo verifica cada resultado antes de presentarlo. Ninguna cifra de la escena simulada debe presentarse como medición.

**Para el formulario de envío.** En la pregunta "Did you utilize any Artificial Intelligence tools?" respondan **Sí**.
Describan: "The team used Claude (Anthropic) for the initial code and documentation and ChatGPT (OpenAI) for debugging, testing, and demonstration materials. The Guayaquil case uses measurements derived from NASA–ISRO NISAR GCOV products."
