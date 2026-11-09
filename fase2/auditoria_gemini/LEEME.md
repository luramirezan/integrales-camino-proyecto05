# Auditoría externa de la Fase 2 con Gemini (por puntos)

Pedido del profesor: que otra IA (no Claude) audite la Fase 2. En vez de darle toda la bitácora de una vez, `auditar.py` la recorre en 10 puntos (P10–P16, tabla de controles PT, decisiones PD y fuentes PF). Cada punto es una **conversación nueva** con Gemini que solo ve el material de ese punto, con la plantilla de `../fuentes_control/auditor_otra_ia.md` y ejecución de Python activada para que recalcule con código propio.

Flujo por punto: `abrir` (Gemini entrega hallazgos) → Claude verifica cada hallazgo calculando y escribe una respuesta → `responder` (1 a 3 rondas) → `cerrar` (tabla final con estado de cada hallazgo). El informe con hallazgos, respuestas y verificaciones es `informe_auditoria.md`; `informe` genera `anexo_tablas_finales_gemini.md` con la última respuesta literal de cada punto.

- Transcripciones literales (prompt, respuestas, código que ejecutó Gemini): `conversaciones/<punto>.md`.
- Respuestas de los autores enviadas en cada ronda: `respuestas/<punto>_rN.md`.
- La API key se pasa por la variable de entorno `GEMINI_API_KEY`; no se guarda en ningún archivo.
- Un desacuerdo se resuelve calculando, no votando. Las decisiones finales son del equipo.
