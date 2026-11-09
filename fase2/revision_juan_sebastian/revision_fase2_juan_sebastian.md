---
title: "Revisión y firma de la Fase 2 · Proyecto 05"
---

**Para:** Juan Sebastián Calixto (verifica la Fase 2) · **De:** Luis Felipe Ramírez · **Fecha:** 9 de noviembre de 2026

Presentación de las Fases 2 y 3: **miércoles 11-11, 15 minutos, hablamos los dos.**

## Qué tienes que hacer (unos 40 minutos)

1. Lee las 10 decisiones de abajo y marca Sí o No en cada una. Al lado de cada una va **la respuesta que recomendamos**, ya ajustada con lo que encontró la auditoría con Gemini.
2. Revisa la corrección del conteo de la tabla de controles (sección B) y firma la tabla.
3. Di si aprobamos aplicar las correcciones de texto de la auditoría (sección C).
4. Firma al final.

Todo el material está en la carpeta del proyecto:

| Qué | Archivo |
|---|---|
| Hoja original de decisiones | `fase2/decisiones_fase2.md` |
| Tabla de controles (la que se firma) | `fase2/secciones/15_tabla_controles.md` |
| Bitácora de la Fase 2 | `fase2/bitacora_fase2.md` (y `bitacora_fase2.pdf`) |
| Informe de la auditoría con Gemini | `fase2/auditoria_gemini/informe_auditoria.md` |
| Auditoría con Gemini 3.1 Pro (app) | PC de Lucho: `InvTeorica\auditoria_gemini_pro\resumen_pro.md` |

**Regla de roles (9.12, aprobada el 21-10-2026):** en la Fase 2 verifica Juan Sebastián, que no implementó. Las decisiones 1 a 7 son de verificación y te tocan a ti; las 8 a 10, a los dos. En la Fase 3 los roles se invierten.

**Lo más importante de la auditoría:** Gemini no encontró ningún error de física ni de signo que cambie un resultado. Sí encontró errores de documento: el más importante es que la tabla de controles cuenta 6 filas dos veces.

## A. Las 10 decisiones

### 1. Control de tabulación: redefinirlo

- **Qué se decide:** el control "tabulación estable a 10⁻⁶ entre las mallas 0.02 y 0.04" falla en 4 de 9 casos. La causa está medida: error del trapecio en la cúspide de Coulomb, de orden h⁴/ε (orden 4.00, confirmado por el recálculo independiente V1).
- **Respuesta recomendada: Sí.** Redefinirlo como Richardson en h con exponente 4 y estabilidad < 10⁻⁶ del valor extrapolado. Cerca del umbral, donde el orden no es 4, se usan h = 0.02 y 0.01 con el orden medido. Gemini confirmó el orden h⁴ con código propio.
- Evidencia: sección 11.4; tabla 15, filas A13 y A14.

**Respuesta de Juan Sebastián:** ☐ Sí  ☐ No  Comentario: ______________________________

### 2. Anomalía de τ = 5 en el PIGS

- **Qué se decide:** la producción da E(τ = 5) a −3.19σ de la transferencia. Las dos réplicas dan +0.03σ y +0.99σ, y las 40 cadenas juntas, −0.83σ. Pero las tres corridas no concuerdan bien entre sí (χ² = 11.13 con 3 g.l., p = 0.011).
- **Respuesta recomendada: Sí, con la redacción cambiada.** La opción original decía "no hay sesgo del muestreador"; las dos auditorías de Gemini señalan que eso es más fuerte de lo que permite p = 0.011. La redacción nueva queda así: *"la dispersión entre corridas indica heterogeneidad estadística; la causa (fluctuación poco probable o error subestimado) no se puede determinar con los datos actuales y queda abierta para la Fase 3"*. Las tres corridas se muestran en la presentación. Descartar la corrida original queda rechazado, porque sesgaría el resultado.
- Evidencia: secciones 12.4 y 12.V3; tabla 15, filas A16 a A19.

**Respuesta de Juan Sebastián:** ☐ Sí  ☐ No  Comentario: ______________________________

### 3. Umbral 0.1 de la ley de caja para declarar "no ligado"

- **Qué se decide:** el 0.1 de desviación relativa frente a π²/[2(R − a_s)²] lo fijó la IA, porque el plan 9.6 no daba un número. La terna intermedia de δ = 1.20 queda fuera por 0.001 (0.101), y el veredicto sale de la terna 200/400/800 (0.021).
- **Respuesta recomendada: Sí, declarando cómo se fijó.** Dejar escrito que el 0.1 se fijó conociendo ya los datos de la Fase 2. El efecto fue conservador, pero es un vicio de procedimiento. El 0.1 queda **fijado desde hoy para la Fase 3, antes de ver sus datos**. El "R ≥ 5|a_s|" que propuso Gemini se rechaza como criterio, porque lo eligió conociendo a_s.
- Evidencia: sección 14.5; tabla 15, fila C8.

**Respuesta de Juan Sebastián:** ☐ Sí  ☐ No  Comentario: ______________________________

### 4. Pozo cuadrado: ley ε^(3/2) y extrapolación en h de orden ~1

- **Qué se decide:** el pozo no sigue la ley ε² (con el salto sale ε^(3/2), medido pero no demostrado y sin fuente), y su malla es de orden ~1. B3 pasa, y el ajuste a cinco puntos (B3b) falla en V0 = 1.3 (+2.2×10⁻⁵).
- **Respuesta recomendada: Sí.** El pozo queda como control **cualitativo** y Hulthén como control **cuantitativo**; el 3/2 no se presenta como resultado demostrado. Las referencias que Gemini dio para el 3/2 eran de memoria y no se verificaron, así que no se citan.
- Evidencia: sección 13.3; tabla 15, filas B21 a B28.

**Respuesta de Juan Sebastián:** ☐ Sí  ☐ No  Comentario: ______________________________

### 5. Pared en R sin imagen

- **Qué se decide:** el núcleo solo tiene imagen en r = 0, así que la pared en R se corre hacia afuera unos 0.5826√ε. Hoy el código estima ese sesgo y lo incluye en el error de las cajas.
- **Respuesta recomendada: "Sí, solo término en el error" para la Fase 3.** Poner la imagen en R cambia el método aprobado y exige una validación nueva que no cabe antes del miércoles. Gemini comprobó que los veredictos de las cajas no dependen de esta corrección. La imagen en R queda como mejora opcional de la Fase 4.
- Evidencia: sección 14.4; tabla 15, fila C3.

**Respuesta de Juan Sebastián:** ☐ Sí (imagen en R)  ☐ Sí (solo término en el error)  ☐ No  Comentario: ______________

### 6. Corrección de Wigner-Kirkwood de U_C fuera de r = 10

- **Qué se decide:** la aproximación para r > 10 tenía un error ε²V''/12 (1.7×10⁻⁶ en r = 10). Se añadió el término de Wigner-Kirkwood y el error bajó a 8×10⁻⁹.
- **Respuesta recomendada: Sí.** No cambia el núcleo exacto dentro de r ≤ 10, y Gemini 3.1 Pro confirmó el coeficiente /12. El residuo de 8×10⁻⁹ se explica con el término de orden ε³, pero esos coeficientes son de memoria de Gemini y no entran a la bitácora sin una fuente o una deducción propia.
- Evidencia: secciones 11.1 y 11.9.

**Respuesta de Juan Sebastián:** ☐ Sí  ☐ No  Comentario: ______________________________

### 7. Tabla de controles de la Fase 2 (firma de verificación)

- **Qué se decide:** si firmas `secciones/15_tabla_controles.md`.
- **Respuesta recomendada: Sí, con el conteo corregido (ver sección B).** Son 82 controles distintos (64 pasan, 9 no pasan, 9 medidos), no 88/70/9/9. Ninguna tolerancia se cambió después de ver un resultado para que pasara, salvo las dos declaradas (⟨r²⟩ de Hulthén en 10.3 y la potencia del histograma en V3).

**Respuesta de Juan Sebastián:** ☐ Sí  ☐ No  Comentario: ______________________________

### 8. Figuras congeladas y primer gráfico

- **Qué se decide:** si se congelan las figuras de `fase2/figuras/` con sus huellas sha256, y cuál de las dos versiones del primer gráfico se usa: la 16 (cuatro paneles) o la 18 (hecha para las diapositivas).
- **Respuesta recomendada: Sí; usar la figura 18 en las diapositivas** y añadir en el pie que los puntos del PIGS y de las réplicas están desplazados en x para que se vean (lo pidió la auditoría). Las huellas se recalculan para que no dependan de qué otras figuras hay en la carpeta.

**Respuesta de Juan Sebastián:** ☐ Sí, figura elegida: ______  ☐ No  Comentario: ______________________________

### 9. Bitácora y registro de IA de la Fase 2

- **Qué se decide:** si se aprueban `bitacora_fase2.md` (y su PDF) y el registro de IA como registro de la Fase 2.
- **Respuesta recomendada: Sí, después de aplicar las correcciones de la sección C** y de añadir al registro las fichas de las dos auditorías con Gemini: `gemini-3.6-flash` y `gemini-3-flash-preview` por API (5-11), y "3.1 Pro" en la app (5 y 9-11). Con eso ya se cumple el requisito de una auditoría hecha por otro modelo que no es Claude.

**Respuesta de Juan Sebastián:** ☐ Sí  ☐ No  Comentario: ______________________________

### 10. Presentación y fuentes de control

- **Qué se decide:** (a) el material de la presentación; (b) la tabla de fuentes `fuentes_control/fuentes_control.md`.
- **Respuesta recomendada: Sí.** (a) La presentación del miércoles es de 15 minutos sobre las Fases 2 y 3, la damos los dos y se aprueba después de un ensayo cronometrado. (b) La tabla de fuentes se acepta con dos notas: en H9, Roy cita δc = 1.19061227 ± 4×10⁻⁸ y el nuestro es 1.1906124211 (unas 4σ de diferencia; el nuestro se recalculó dos veces con código aparte); en H8, el año no cuadra (arXiv de 2001, revista de 2000) y hay que verificarlo. Las referencias de pago (empezando por Cai, Cai e Inomata, Phys. Rev. A 34, 4621) se buscan en la biblioteca.

**Respuesta de Juan Sebastián:** ☐ Sí  ☐ No  Comentario: ______________________________

## B. Corrección del conteo de la tabla de controles

Hay seis controles que aparecen dos veces, con el mismo valor, en los bloques A y D. Los seis pasan:

| Bloque A | Bloque D | Control |
|---|---|---|
| A22 | D3 | Hellmann-Feynman, δ = 0.2 |
| A23 | D4 | Hellmann-Feynman, δ = 0.5 |
| A24 | D5 | Hellmann-Feynman, δ = 1.0 |
| A25 | D6 | Virial |
| A26 | D2 | Cotas |
| A27 | D21 | Sin ligado en δ ≥ 2 (L19) |

| | Filas | Pasan | No pasan | Medidos |
|---|---|---|---|---|
| Lo que dice hoy el resumen | 88 | 70 | 9 | 9 |
| **Controles distintos (corregido)** | **82** | **64** | **9** | **9** |

**Propuesta:** dejar las filas y añadir al resumen "88 filas = 82 controles distintos; A22–A27 repiten D2–D6 y D21". Así no cambian los identificadores que cita la bitácora.

☐ De acuerdo  ☐ Prefiero quitar los duplicados  Comentario: ______________________________

## C. Correcciones de texto que salieron de la auditoría

Ninguna cambia un resultado. Hoy no hay nada aplicado; se aplican solo si las apruebas.

| # | Corrección | Dónde |
|---|---|---|
| 1 | El resumen dice "21 pasan, 0 fallan"; debe decir 22 pasan, 1 no pasa (B3b) y 5 medidos | sección 13 |
| 2 | Tiempos del texto que no coinciden con la salida: 27 → 23.7 s (11); 161 → 135.8 s (12b); 110 → 132.5 s (13); 95 → 101 s (14) | secciones 11 a 14 |
| 3 | "9 pruebas" debe decir 14; "10/11 criterios" no coincide con la tabla de 13 filas; imprimir en el script el ⟨r²⟩ con Richardson | sección 12 y script 12 |
| 4 | L02, L15 y L18 no salen de `15_limites.py` sino de `11_transferencia_controles.py`: citar el script correcto | bitácora, Parte VI |
| 5 | L05: reportar el valor con Richardson en Δδ (la diferencia baja de 5.6×10⁻⁶ a menos de 10⁻⁹) | Parte VI |
| 6 | Errata −3.08×10⁻⁵ → −3.07×10⁻⁵ (δ = 1.18, R = 400), también en la tabla de fuentes | `fuentes_control.md` |
| 7 | Llamar "referencia V1" (no "exacto") al −0.3268085113692 de δ = 0.2 | sección 10 |
| 8 | Añadir que la sección 10 remite a `fuentes_control.md` y a la Fase 1 | sección 10 |
| 9 | Código: `todos()` debe dar error si no encuentra criterios; B3b debe ir en `CRIT_DECL`; las huellas sha256 no deben depender de qué hay en la carpeta | scripts 16 y 13 |
| 10 | Notas en las fuentes: constantes en el origen δ/2 (Hulthén) y δ (Yukawa); la fórmula del 2s solo vale para δ < 0.5 | `fuentes_control.md` |

**Advertencia para el registro de IA:** en la app, Gemini 3.1 Pro no ejecuta código (lo admitió). Varias referencias que dio eran de memoria o falsas, por ejemplo "J. Math. Phys." para Cai, Cai e Inomata. Ninguna cita de Gemini entra a la bitácora sin verificarla en la fuente.

☐ Apruebo aplicar las 10  ☐ Apruebo con cambios: ______________________________

## Firmas

Luis Felipe Ramírez: ______________________   Fecha: ____________

Juan Sebastián Calixto (verificación): ______________________   Fecha: ____________
