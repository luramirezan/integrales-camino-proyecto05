# Qué sigue: Fase 2 del proyecto 05 (umbral de enlace en el potencial de Yukawa)

Juan Sebastián Calixto y Luis Felipe Ramírez · 19 de octubre de 2026 · Lo que estaba marcado como propuesta (método, punto δ = 0.2, calendario, roles, Hulthén) lo aprobó Lucho el 21-10-2026 (decisiones 4 a 6 de `decisiones_pendientes.md`); solo queda pendiente la decisión 7, sobre el material de presentación de la Fase 1.

## Lo que pide el profesor (`enunciado/guia_texto.txt`)

- **Tarea del proyecto 05 en la Fase 2:** "construir un solucionador radial y una formulación de tiempo imaginario que trate correctamente la singularidad; la primera exposición compara ambos en un punto fuertemente ligado".
- **Evidencia común de la Fase 2:** código ejecutable, primer gráfico, bitácora de IA y primera presentación escalonada. En esta fase se congelan las figuras de la primera ronda y se comprueba que el resultado mínimo ya tiene un caso de control.
- **Primera presentación:** cohorte B, **semana 7**. Muestra la pregunta, la acción, el caso de referencia, un cálculo preliminar y el riesgo principal. En el formato de la guía son 9 min de exposición y 5 de discusión, y hablan todos los integrantes.
- **Ojo:** la presentación de 15 minutos de la Fase 1 es más larga que los 9 min de la guía; la de la semana 7 debe ajustarse a 9 + 5.
- **Roles:** formulación física, implementación y verificación rotan al comienzo de las Fases 2 y 3. Para problemas con singularidades hay que declarar si el peso muestreado es real, positivo y normalizable.

## El plan ya escrito (sección 9 de la bitácora)

- **Método elegido (aprobado el 21-10-2026, 9.3):** acción de pares en el sector radial ℓ = 0: núcleo exacto de Coulomb tabulado (U_C, con h_tab = 0.01 y 0.005 y Richardson) más el resto acotado W = (1 − e^(−δr))/r ∈ [0, δ] en factorización simétrica. El peso es real, positivo y normalizable. Se evalúa de dos maneras: autovalor de la matriz de transferencia en banda (sin muestreo) y PIGS desde u_T = r e^(−r). La referencia independiente es el solucionador radial de la sección 5. Queda prohibida la acción primitiva con 1/r desnudo; el suavizado solo sirve como control, con a declarado y extrapolado.
- **Punto fuertemente ligado (aprobado el 21-10-2026, 9.4):** δ = 0.2 (E0 = −0.32680851, ⟨r⟩ = 1.5497, brecha al 2s 0.3147), con control en Coulomb δ = 0. Parámetros: R = 40; ε = 0.1 (y 0.2 y 0.05); τ = 10 (δ = 0) y 20 (δ = 0.2); malla h = 0.02 con control en 0.04; 8 cadenas de 5×10⁴ barridos; semillas 20261012 a 20261020.
- **Controles y criterios de aceptación (9.7):** Coulomb con la transferencia: |E + 0.5| < 10⁻⁶ y ⟨r⟩ = 1.5 a 10⁻⁴. Coulomb con PIGS: E_L ≡ −0.5, y ⟨r⟩ y ⟨r²⟩ a menos de 2σ. δ = 0.2 con la transferencia: |E − E_rad| < 10⁻⁶ y |⟨r⟩ − ⟨r⟩_rad| < 10⁻³. δ = 0.2 con PIGS: E, ⟨r⟩ y ⟨r²⟩ a menos de 2σ, tomando σ como el mayor entre bloques y semillas. Ley ε² con orden aparente en [1.8, 2.2]. Proyección: cambio < 10⁻⁶ de τ a 1.5τ. Tabulación estable a 10⁻⁶ entre las mallas 0.02 y 0.04. **Añadido (aprobado el 21-10-2026):** Hulthén como control exacto en al menos dos δ (sección 0.6.1).
- **Lo que ya funciona (9.5):** en δ = 0.2 la transferencia queda a 1.5×10⁻⁸ del radial y PIGS a −0.3σ; Coulomb a 1.1×10⁻⁷.
- **Calendario (aprobado el 21-10-2026, 9.11):** la Fase 2 va hasta la semana 7; la Fase 3, de la 8 a la 11; la Fase 4, de la 12 a la 16, con la segunda presentación en la semana 14.
- **Roles en la Fase 2 (aprobados el 21-10-2026, 9.12):** formulación física y verificación, Juan Sebastián Calixto; implementación, Luis Felipe Ramírez. En la Fase 3 se invierten. Quien implementa no verifica en la misma fase.

## Lista de tareas, en orden

| # | Tarea | Responsable propuesto | Entregable |
|---|---|---|---|
| 0 | Firmar `decisiones_pendientes.md` y decidir la 7 tras un ensayo cronometrado (decisiones 1 a 6 aprobadas el 21-10-2026; con la 7 se cierra la Fase 1) | los dos | hoja firmada; entrada en el registro de IA |
| 1 | Pasar el solucionador radial de la sección 5 a un módulo con prueba propia (Coulomb y tabla 5.1) | Juan Sebastián | módulo y prueba que pasa |
| 2 | Módulo de la tabla U_C (dos h_tab, Richardson) con la prueba de Coulomb | Luis Felipe | módulo; prueba \|E + 0.5\| < 10⁻⁶ |
| 3 | Módulo de la transferencia en banda (Nyström, h = 0.02 y 0.04) | Luis Felipe | E0(ε) y ⟨r⟩ en δ = 0 y 0.2 |
| 4 | Módulo PIGS (puentes, extremos, escala; 8 cadenas; semillas fijas) | Luis Felipe | E, ⟨r⟩, ⟨r²⟩ con el error mayor entre bloques y semillas |
| 5 | Control exacto de Hulthén en dos δ (aprobado el 21-10-2026) | Juan Sebastián | tabla de controles |
| 6 | Verificar la tabla 9.7 completa para la Fase 2 (L01 a L09 de la sección 7 incluidos) y declarar el peso | Juan Sebastián | tabla de controles firmada |
| 7 | Barrido ε ∈ {0.2, 0.1, 0.05} en δ = 0.2 y comprobación de la ley ε² (prueba de L18) | Luis Felipe (ejecuta) y Juan Sebastián (verifica) | orden aparente y valor extrapolado |
| 8 | Primer gráfico: δ = 0.2 radial frente a transferencia y PIGS con barras de error, más E_mixto(τ); congelar figuras | los dos | figura congelada con su script |
| 9 | Bitácora de IA de la Fase 2 (fecha, consulta, respuesta, decisión humana, comprobación, corrección) | quien haga cada consulta; Juan Sebastián la consolida | registro actualizado |
| 10 | Primera presentación (semana 7): pregunta, acción, caso de referencia, cálculo preliminar, riesgo de la caja | los dos; reparto por **propuesta** | diapositivas y guion |

**Abierto, sin bloquear la Fase 2:** cotejar con los PDF las ecuaciones de Kleinert (2.376) y Saporiti (24); verificar en la fuente primaria el δc de Gebremedhin y Weatherford y la cifra de Rogers et al.; actualizar el `print` de τ = 5/|E0| del script 08; planear para la Fase 3 la auditoría de autovalores cercanos a cero con otro modelo (supuesto S1).
