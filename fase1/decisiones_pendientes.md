# Decisiones pendientes del equipo (Fase 1, proyecto 05)

**Al confirmar esta hoja se cierra el criterio C9 (bitácora de IA con decisión humana) y con él la Fase 1:** las condiciones C1 a C8 ya están cumplidas (bitácora, X.1).

Para Luis Felipe Ramírez (Lucho) y Juan Sebastián Calixto · 19 de octubre de 2026. Hoy la bitácora dice "pendiente de confirmar por el equipo" en unas 50 líneas (secciones 00 a 10 y `correcciones_ronda2.md`). Aquí quedan agrupadas en siete decisiones. Marquen Sí o No en cada una; si es No, escriban qué cambia. Con la hoja firmada, la IA pasa las respuestas a la columna "Decisión humana" de la tabla 10.2 y a los registros de cada sección.

### 1. Aprobar los resultados de los bloques 1 a 6

- **Qué se decide:** si el equipo da por buenos la adimensionalización, el límite de Coulomb, la cota variacional, las cotas superiores, la referencia numérica y las fuentes, con sus revisiones adversariales (fichas R1-01 a R1-07).
- **Opción propuesta:** aprobar. El intervalo es 1.19055 ≤ δc ≤ 1.24305 y la referencia, 1.1906124211. El valor de Gebremedhin y Weatherford queda como "tomado de una cita secundaria".
- **Evidencia:** `secciones/01` a `06`, scripts `01` a `06` (re-ejecutados en X.4) y bitácora, partes V y VII.
- [x] Sí, verificación hecha el 21-10-2026  [ ] No  Comentario: Lucho aprueba el 21-10-2026 con la condición de verificar una vez más. La verificación independiente y el cotejo de fuentes se hicieron ese mismo día: todo coincidió salvo los umbrales de una sola caja de 6.2(c), que tenían un error de malla y se corrigieron (1.177013 a 1.188924; R2-13 y `secciones/correcciones_ronda2.md`, "Verificación del 21-10-2026").

### 2. Aprobar las correcciones de la segunda ronda y el marco

- **Qué se decide:** si se aceptan las correcciones K1 a K19 de la auditoría (entre ellas: quitar el "enunciado" con 1/δ, la curva de Calogero, la fila de δ = 1, la atribución a Rogers, la tabla de cajas con Richardson) y el marco de la sección 0: la pregunta (0.1), el régimen (0.2), el criterio de cierre (0.3) y la notación a_sc para la longitud de dispersión (0.5).
- **Opción propuesta:** aprobar todo.
- **Evidencia:** `secciones/correcciones_ronda2.md`, tabla 10.3, sección 0, fichas R2-01, R2-02, R2-06, R2-08 y R2-09.
- [x] Sí  [ ] No  Comentario: Lucho, 21-10-2026: "aprueba todo".

### 3. Adoptar la lista de límites L01 a L19 como batería de pruebas

- **Qué se decide:** si la lista que propuso la IA, con las correcciones de 7.4 (L13 corregido; L10, L11 y L17 precisados), es la batería de pruebas de las Fases 2 a 4, con los usos de la tabla 7.5.
- **Opción propuesta:** adoptarla. L18 (orden de Trotter) se prueba en la Fase 2.
- **Evidencia:** sección 7, `07_limites_fisicos.py` y ficha R2-03.
- [x] Sí  [ ] No  Comentario: Lucho, 21-10-2026: aprueba la opción propuesta.

### 4. Adoptar la acción de pares como método de la Fase 2

- **Qué se decide:** la formulación de tiempo imaginario que pide la guía: núcleo exacto de Coulomb más el resto W (R1, en el marco radial R5), evaluada con la matriz de transferencia en banda y con PIGS. La acción primitiva con 1/r desnudo queda prohibida y el suavizado solo sirve de control, extrapolado.
- **Opción propuesta:** adoptarla. Alternativa descartada por ahora: Duru-Kleinert (solo bibliográfica).
- **Evidencia:** secciones 8.4, 8.5 y 8.7 (pendiente del sesgo 1.99), sección 9.3 y fichas R2-04 y R2-05.
- [x] Sí  [ ] No  Comentario: Lucho, 21-10-2026: aprueba la opción propuesta.

### 5. Aprobar el plan de cómputo

- **Qué se decide:** δ = 0.2 como punto fuertemente ligado de la primera exposición, con control en δ = 0 (9.4); la rejilla de cajas R ∈ {50, 100, 200, 400, 800} y el criterio de enlace de tres cajas con ⟨r⟩/R y F½ (9.6); los controles y criterios de aceptación (9.7), añadiendo Hulthén como control exacto (0.6.1); y el calendario por semanas (9.11: Fase 2 hasta la semana 7; Fase 3, semanas 8 a 11; Fase 4, semanas 12 a 16).
- **Opción propuesta:** aprobar todo. La extensión de la Fase 4 (E1 u E2 de la sección 0.9) se decide más adelante.
- **Evidencia:** sección 9 y `09_prueba_costos.py` (transferencia a 1.5×10⁻⁸ del radial y PIGS a −0.3σ en δ = 0.2), y `que_sigue_fase2.md`.
- [x] Sí  [ ] No  Comentario: Lucho, 21-10-2026: aprueba la opción propuesta.

### 6. Roles y reparto de la exposición

- **Qué se decide:** (a) los roles que tuvo cada uno en la Fase 1 (hoy "pendiente" en 0.0 y 10.1); (b) la rotación de 9.12: en la Fase 2, formulación y verificación para Juan Sebastián e implementación para Luis Felipe; en la Fase 3 se invierte; (c) el reparto del guion de 15 minutos: Juan Sebastián, láminas 1 a 9 (7 min 35 s); Luis Felipe, 10 a 17 (7 min 20 s).
- **Opción propuesta:** (a) escribir aquí los roles reales de la Fase 1: ________________; (b) y (c), como están.
- **Evidencia:** sección 9.12, `guion_fase1.md` (tabla de reparto) y ficha R2-11.
- [x] Sí  [ ] No  Comentario: Lucho, 21-10-2026: la rotación de la Fase 2 y el reparto de la presentación quedan así. (a) Roles de la Fase 1 (Lucho, 21-10-2026): Juan Sebastián Calixto, formulación física; Luis Felipe Ramírez, implementación y verificación.

### 7. Aprobar el material de presentación de la Fase 1

- **Qué se decide:** si se aprueban `diapositivas_fase1.pptx` (18 láminas, 17 expuestas, unos 14 min 55 s) y `guion_fase1.md` con sus preguntas y respuestas. Es lo que falta de la condición C10. Ojo: la guía da 9 min de exposición por equipo en las rondas de presentaciones, así que conviene confirmar con el profesor que esta sesión admite 15 min.
- **Opción propuesta:** aprobar, después de un ensayo cronometrado de los dos.
- **Evidencia:** `diapositivas_fase1.pptx`, `guion_fase1.md` y `.pdf`, y ficha R2-12.
- [ ] Sí  [ ] No  Comentario: Lucho, 21-10-2026: aún pendiente.

Firmas y fecha: Luis Felipe Ramírez ____________ · Juan Sebastián Calixto ____________ · Fecha: ____________
