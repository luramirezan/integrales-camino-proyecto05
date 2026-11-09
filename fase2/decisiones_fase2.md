# Decisiones pendientes del equipo (Fase 2, proyecto 05)

Para Luis Felipe Ramírez (Lucho) y Juan Sebastián Calixto · 27 de octubre de 2026.

**Por qué existe esta hoja.** Toda la Fase 2 la ejecutó la IA (Claude) en un flujo de agentes que pidió Lucho el 27-10-2026. En la bitácora (`bitacora_fase2.md`) y en las secciones 10 a 15 cada "decisión humana" dice "pendiente de confirmar por el equipo". Aquí quedan agrupadas en diez decisiones. Marquen Sí o No en cada una; si es No, escriban qué cambia. Con la hoja firmada, la IA pasa las respuestas a la columna "Decisión humana" del registro de IA (`secciones/17_registro_ia.md`) y a la tabla de controles (`secciones/15_tabla_controles.md`).

**Al firmarla se cierran los criterios K4 (decisión humana en la bitácora de IA) y K6 (tabla de controles firmada) del cierre de la Fase 2** (bitácora, Parte X). La decisión 10 (presentación) cierra K5.

Regla de la Fase 2 (9.12 de la Fase 1, aprobada el 21-10-2026): verifica Juan Sebastián, que no implementó. Las decisiones 1 a 7 son de verificación y le tocan a él; las 8 a 10, a los dos.

### 1. Control de tabulación de 9.7: redefinirlo

- **Qué se decide:** el control "tabulación estable a 10⁻⁶ entre las mallas Nyström 0.02 y 0.04" falla en 4 de 9 casos (1.5×10⁻⁶ a 3.2×10⁻⁶ con ε ≤ 0.1 en δ = 0 y 0.2). La causa está medida y la confirmó el recálculo independiente V1: error de extremo del trapecio en la cúspide de Coulomb, de orden h⁴/ε (orden aparente 4.00).
- **Opción propuesta:** redefinirlo como "Richardson en h con exponente 4 entre 0.02 y 0.04 (o 0.01 y 0.02) y estabilidad < 10⁻⁶ del valor extrapolado". Cerca del umbral el orden de la malla no es 4 (1.36 y 2.29 en δ = 1.18): allí usar h = 0.02 y 0.01 y el orden medido.
- **Evidencia:** sección 11.4; tabla 15, filas A13 y A14; V1 (comprobado con núcleo exacto propio).
- [ ] Sí  [ ] No  Comentario: ____________________

### 2. Anomalía de τ = 5 en el PIGS

- **Qué se decide:** la producción da E(τ = 5) a −3.19σ de la transferencia. Réplica 1 (16 cadenas): +0.03σ. Réplica 2 (16 cadenas): +0.99σ. Las 40 cadenas juntas: −0.83σ. Pero las tres corridas no concuerdan del todo entre sí (χ² = 11.13 con 3 g.l., p = 0.011).
- **Opción propuesta:** aceptar que no hay sesgo del muestreador (la combinación y la prueba de histograma no lo muestran), mostrar las tres corridas en la presentación y dejar la anomalía como "abierta, p ≈ 1 %" en la Fase 3, donde se estudia la autocorrelación.
- **Evidencia:** sección 12.4 y 12.V3; tabla 15, filas A16 a A19.
- [ ] Sí  [ ] No  Comentario: ____________________

### 3. Umbral 0.1 de la ley de caja para declarar "no ligado"

- **Qué se decide:** el 0.1 de desviación relativa frente a π²/[2(R − a_s)²] lo fijó la IA (9.6 no daba número). La terna intermedia de δ = 1.20 queda fuera por 0.001 (0.101); el veredicto sale de la terna 200/400/800 (0.021).
- **Opción propuesta:** aprobar 0.1 para la Fase 3 y decidirlo antes de ver los datos de la Fase 3.
- **Evidencia:** sección 14.5; tabla 15, fila C8.
- [ ] Sí  [ ] No  Comentario: ____________________

### 4. Pozo cuadrado: ley ε^{3/2} medida y extrapolación en h de orden ~1

- **Qué se decide:** el pozo no cumple la ley ε² del plan (con el salto sale ε^{3/2}, medido, no demostrado y sin fuente) y su malla Nyström es de orden ~1. Con el orden medido B3 pasa (+3.6×10⁻⁶ y −4.2×10⁻⁷ < 10⁻⁵), pero el ajuste a cinco puntos (B3b) falla en V0 = 1.3 (+2.2×10⁻⁵).
- **Opción propuesta:** usar el pozo como control **cualitativo** (separa "singularidad" de "caja/umbral") y Hulthén como control **cuantitativo**; no presentar el 3/2 como resultado demostrado.
- **Evidencia:** sección 13.3; tabla 15, filas B21 a B28; V1 (H2).
- [ ] Sí  [ ] No  Comentario: ____________________

### 5. Pared en R sin imagen

- **Qué se decide:** K_D solo tiene imagen en r = 0; la pared en R se corre hacia afuera unos 0.5826√ε (medido). Hoy el código estima el sesgo y avisa, y el error de las cajas lo incluye. Cambiar el núcleo (imagen también en R, o usar R_ef = R − 0.5826√ε) modifica el método aprobado.
- **Opción propuesta:** para las Fases 3 y 4, poner la imagen en R (o R_ef) y comprobarlo contra el radial en R = 50 y 100; mientras tanto, mantener el término de pared en el error.
- **Evidencia:** sección 14.4; V1 (H1), V2 (H3); tabla 15, fila C3.
- [ ] Sí (imagen en R)  [ ] Sí (solo término en el error)  [ ] No  Comentario: ____________________

### 6. Corrección de Wigner-Kirkwood de U_C fuera de r = 10

- **Qué se decide:** la aproximación de extremos para r > 10 tenía un error ε²V''/12 (1.7×10⁻⁶ en r = 10, no "< 10⁻⁷" como decía el código). Se añadió el término de Wigner-Kirkwood; el error baja a 8×10⁻⁹.
- **Opción propuesta:** aceptarla como parte del método (no cambia el núcleo exacto dentro de r ≤ 10).
- **Evidencia:** sección 11.1 y 11.9; V2 (H2), V1 (H3).
- [ ] Sí  [ ] No  Comentario: ____________________

### 7. Tabla de controles de la Fase 2 (firma de verificación)

- **Qué se decide:** si Juan Sebastián firma `secciones/15_tabla_controles.md`: 88 filas, 70 pasan, 9 no pasan (todas con causa medida y declarada), 9 medidas. Ninguna tolerancia se cambió después de ver el resultado para que pase, salvo las dos que se declaran (Hulthén ⟨r²⟩ en la sección 10.3 y la prueba de potencia del histograma en V3).
- **Opción propuesta:** firmar, con las decisiones 1 a 6.
- **Evidencia:** sección 15; V1, V2 y V3.
- [ ] Sí  [ ] No  Comentario: ____________________

### 8. Figuras congeladas y primer gráfico

- **Qué se decide:** si se congelan las figuras de `fase2/figuras/` con sus huellas sha256 (bitácora, apartado X.3), y si la figura de la primera exposición es `16_primer_grafico.png` (cuatro paneles: E, ⟨r⟩, ⟨r²⟩ y E_mixto(τ) en δ = 0.2). Nota: otro agente del mismo flujo dejó `18_primer_grafico.png` (script `18_figura_presentacion.py`) para las diapositivas; el equipo debe elegir una sola.
- **Opción propuesta:** congelar todas; usar una de las dos en la presentación y anotar cuál.
- [ ] Sí, figura elegida: ________  [ ] No  Comentario: ____________________

### 9. Bitácora y registro de IA de la Fase 2

- **Qué se decide:** si se aprueban `bitacora_fase2.md` (y su PDF) y `secciones/17_registro_ia.md` como registro de la Fase 2, con la advertencia de que el auditor fue otra instancia de Claude (supuesto S1).
- **Opción propuesta:** aprobar, y hacer en la Fase 3 la auditoría con otro modelo (`fuentes_control/auditor_otra_ia.md`), que además pide la guía para la Fase 3 ("auditoría adversarial de autovalores cercanos a cero").
- [ ] Sí  [ ] No  Comentario: ____________________

### 10. Primera presentación (semana 7, 9 + 5 min) y fuentes de control

- **Qué se decide:** (a) aprobar el material de la primera presentación de `fase2/presentacion/` (otro agente del mismo flujo dejó a las 03:16 UTC un borrador (`diapositivas_fase2.pptx` y `.pdf`, `guion_fase2.md`); este registro no lo revisó y el equipo no lo ha aprobado), tras un ensayo cronometrado de 9 min; (b) revisar `fuentes_control/fuentes_control.md` (su registro de IA dice "pendiente de revisión por el equipo"); (c) queda pendiente aún la decisión 7 de la Fase 1 (material de presentación de la Fase 1).
- **Opción propuesta:** (a) aprobar tras el ensayo; (b) aceptar la tabla de fuentes con sus estados tal como están y bajar con la biblioteca los PDF de pago, empezando por H1 (Cai, Cai e Inomata 1986).
- [ ] Sí  [ ] No  Comentario: ____________________

Firmas y fecha: Luis Felipe Ramírez ____________ · Juan Sebastián Calixto ____________ · Fecha: ____________
