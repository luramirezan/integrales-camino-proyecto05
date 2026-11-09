# Guion de la Fase 2: primera presentación (semana 7)

**Proyecto 05 · Umbral de ligadura del 1s en V(r) = −g e^(−μr)/r** · Presentan: Juan Sebastián Calixto (JS) y Luis Felipe Ramírez (LF) · 27-10-2026 · 9 min de exposición + 5 min de discusión.

Diapositivas: `diapositivas_fase2.pptx` (y `diapositivas_fase2.pdf`), generadas por `generar_diapositivas_fase2.py`, que lee todas las cifras de `fase2/resultados/*.json` y de `secciones/15_tabla_controles.md`. El primer gráfico es `figuras/16_primer_grafico.png` (`codigo/16_primer_grafico.py`); `codigo/18_figura_presentacion.py` hizo una versión de respaldo. Las notas del orador de cada lámina son el mismo texto de este guion. Tiempos calculados a 150 palabras por minuto a partir del número de palabras de cada bloque.

## Reparto

| # | Lámina | Quién | Palabras | Tiempo |
|---|---|---|---|---|
| 1 | Portada | Juan Sebastián | 55 | 22 s |
| 2 | La pregunta y lo que pide la Fase 2 | Juan Sebastián | 91 | 36 s |
| 3 | La acción de pares y el peso declarado | Juan Sebastián | 135 | 54 s |
| 4 | Una acción, dos evaluaciones y una referencia | Juan Sebastián | 100 | 40 s |
| 5 | Caso de referencia: Coulomb (δ = 0) | Juan Sebastián | 113 | 45 s |
| 6 | Controles exactos: Hulthén y pozo cuadrado | Juan Sebastián | 126 | 50 s |
| 7 | Cálculo preliminar en δ = 0.2: radial frente a tiempo imaginario | Luis Felipe | 106 | 42 s |
| 8 | Proyección desde una función de prueba no exacta | Luis Felipe | 127 | 51 s |
| 9 | Errores sistemáticos: Trotter y malla | Luis Felipe | 97 | 39 s |
| 10 | Riesgo principal: la caja cerca del umbral | Luis Felipe | 148 | 59 s |
| 11 | Balance de la Fase 2 y qué sigue | Luis Felipe | 82 | 33 s |
| 12 | Respaldo 1: los controles que no pasan | (no se expone) | 0 | 0 s |
| 13 | Respaldo 2: límites físicos con la integral de camino | (no se expone) | 0 | 0 s |
| 14 | Respaldo 3: la pared en R sin imagen | (no se expone) | 0 | 0 s |
| 15 | Respaldo 4: decisiones pendientes de firma | (no se expone) | 0 | 0 s |
| 16 | Respaldo 5: registro de la IA en la Fase 2 | (no se expone) | 0 | 0 s |

**Total expuesto:** 1180 palabras, unos 7 min 52 s (máximo 9 min; queda margen para cambiar de lámina y señalar figuras). Juan Sebastián: 620 palabras (4 min 08 s), láminas 1 a 6 (pregunta, acción y peso, métodos, Coulomb, Hulthén y pozo: formulación y verificación). Luis Felipe: 560 palabras (3 min 44 s), láminas 7 a 11 (cálculo en δ = 0.2, proyección, errores, caja y balance: implementación). Las láminas 12 a 16 son de respaldo y no se exponen. El reparto es una propuesta y lo confirma el equipo.

## Texto de cada lámina

### 1. Portada (Juan Sebastián, 22 s)

**En la lámina:**

- Umbral de ligadura en el potencial de Yukawa
- Fase 2: acción de pares, controles exactos y primer cálculo con la integral de camino
- Juan Sebastián Calixto (formulación y verificación) · Luis Felipe Ramírez (implementación) / Investigación Teórica · Proyecto 05 · primera presentación, semana 7 · 27 de octubre de 2026
- [imagen: ecuación V(r), δ, δc]

**Se dice:**

> Buenos días. Somos Juan Sebastián Calixto y Luis Felipe Ramírez, y presentamos la Fase 2 del proyecto 5: el umbral de ligadura del estado 1s en el potencial de Yukawa. Yo presento la pregunta, la acción y los controles; Luis Felipe, el cálculo en delta igual a 0.2 y el riesgo de la caja.

### 2. La pregunta y lo que pide la Fase 2 (Juan Sebastián, 36 s)

**En la lámina:**

- La pregunta y lo que pide la Fase 2
- Unidades ħ = m = g = 1: longitudes en a = ħ²/(mg), energías en mg²/ħ². δc de la Fase 1 (energía cero, R = 200 a 800).
- ¿Para qué apantallamiento μ (a g, m y ħ fijos) deja de existir el estado ligado 1s de V(r) = −g e−μr/r, y cómo se comportan E₀ y ⟨r⟩ al acercarse a ese valor?
- 1. Solucionador radial / • Diferencias finitas + Richardson / • Referencia independiente / • Módulo radial.py
- 2. Tiempo imaginario / • Acción que trate bien −1/r / • Transferencia (sin muestreo) / • PIGS (Monte Carlo)
- 3. Comparar en δ = 0.2 / • Punto fuertemente ligado / • Control: Coulomb, δ = 0 / • Controles exactos: Hulthén y pozo
- [imagen: ecuación V(r), δ, δc]

**Se dice:**

> La pregunta sigue igual: ¿para qué apantallamiento mu deja de existir el estado ligado 1s, y cómo se comportan la energía y el radio medio al acercarnos? En unidades reducidas todo depende de delta, y la referencia de la Fase 1 es delta c igual a 1.1906124211. Para esta fase la guía pide dos herramientas: un solucionador radial y una formulación de tiempo imaginario que trate bien la singularidad uno sobre r, y compararlas en un punto fuertemente ligado. Elegimos delta igual a 0.2, con el hidrógeno como control.

### 3. La acción de pares y el peso declarado (Juan Sebastián, 54 s)

**En la lámina:**

- La acción de pares y el peso declarado
- pares.py (tabla U_C, h_tab = 0.01 y 0.005 con Richardson), transferencia.py; cifras de 11_transferencia.json (peso). Prohibida la primitiva con 1/r desnudo.
- • ρC: núcleo exacto de Coulomb; toda la singularidad −1/r va dentro de UC / • K_D con imagen en r = 0: impone u(0) = 0 (sector ℓ = 0) / • W acotado y suave: sesgo de la factorización O(ε²) / • δ = 0: el método es exacto para todo ε
- Veredicto sobre el peso
| Propiedad | Valor |
| Real | sí: sin fases |
| Positivo | sí: 0 elementos negativos |
| Finito | sí: 0 elementos no finitos |
| U_C(0.01, 0.01), ε = 0.1 | −0.788 |
| Primitiva en r = 0.01: ε/r | 10  (factor e^10) |
- Normalizable: U_C es finita en el origen, así que la integral sobre un eslabón converge (con la primitiva diverge: Fase 1, sección 8).
- [imagen: ecuaciones T, K_D, U_C, W]

**Se dice:**

> La acción es la de pares que aprobamos en la Fase 1. Separamos el potencial en Coulomb más un resto W. Cada eslabón es el núcleo libre con imagen, que impone u de cero igual a cero, por la acción exacta de Coulomb, U C, y por el resto W repartido entre los dos extremos. U C la tabulamos con dos mallas y Richardson. Toda la singularidad queda dentro del núcleo exacto, y W está acotado entre cero y delta. El peso es real, positivo y normalizable: en la matriz hay cero elementos negativos y cero no finitos. En r igual a 0.01, con epsilon 0.1, la acción exacta vale menos 0.79; la primitiva daría e a la 10. Y en delta igual a cero el método es exacto para cualquier epsilon.

### 4. Una acción, dos evaluaciones y una referencia (Juan Sebastián, 40 s)

**En la lámina:**

- Una acción, dos evaluaciones y una referencia
- Módulos en fase2/codigo/: radial.py, pares.py, transferencia.py, pigs.py. Semillas de producción 20262000 + k.
- Transferencia en banda / • Nyström: h = 0.02 (control 0.04) / • Autovalor mayor λ₀ (eigsh) / • Sin ruido estadístico / • Llega hasta R = 800
- PIGS / • Caminos desde u_T = r e^(−r) / • u_T no exacta para δ > 0 / • 8 cadenas por punto / • Error: el mayor entre bloques y cadenas
- Radial (referencia) / • Diferencias finitas / • h = 1/40 y 1/80 (o 1/80 y 1/160) / • Richardson en h / • Independiente de la acción
- Extrapolaciones / ε = 0.2, 0.1, 0.05 → ε → 0 (ley ε²) / h = 0.02, 0.04 → h → 0 (Richardson)
- [imagen: ecuaciones E0(ε) y peso P[r0..rM]]

**Se dice:**

> Con esa misma acción hacemos dos evaluaciones. La matriz de transferencia: discretizamos r con paso 0.02, control 0.04, y sacamos el autovalor mayor, sin muestreo. Y PIGS: muestreamos caminos que salen de una función de prueba, r por e a la menos r, que no es exacta para delta mayor que cero. Usamos ocho cadenas por punto y reportamos el mayor entre el error por bloques y el error entre cadenas. La referencia independiente es el solucionador radial, con diferencias finitas y Richardson. El sesgo de Trotter se extrapola con epsilon 0.2, 0.1 y 0.05.

### 5. Caso de referencia: Coulomb (δ = 0) (Juan Sebastián, 45 s)

**En la lámina:**

- Caso de referencia: Coulomb (δ = 0)
- 11_transferencia.json (resultados 0.0, h = 0.02, R = 40); 12c_pigs_coulomb_tau5.json (A_coulomb, 8 cadenas, τ = 10). Exactos: E = −1/2, ⟨r⟩ = 3/2, ⟨r²⟩ = 3.
- Transferencia (h = 0.02, ε = 0.2 / 0.1 / 0.05)
- 2.2×10⁻⁷
- máx |E + 1/2|
- 6.6×10⁻⁷
- máx |⟨r⟩ − 3/2|
- El sesgo de Trotter es nulo en δ = 0: lo que queda es error de malla y de tabla.
- PIGS (8 cadenas, τ = 10)
| Observable | PIGS | Exacto | Desvío |
| ⟨r⟩ | 1.49027 ± 0.00720 | 1.5 | −1.35σ |
| ⟨r²⟩ | 2.9679 ± 0.0343 | 3 | −0.94σ |
| Histograma de r | p = 0.004 | p > 0.001 | pasa justo |
- Ojo: E_L ≡ −1/2 en todo camino es tautológico (W = 0). El control real es la distribución de r.
- • La tabla de U_C con Richardson es clave: sin ella el error en E sería 2.6×10⁻⁵ (ε = 0.2)

**Se dice:**

> Primer control: Coulomb, delta igual a cero. La transferencia da menos un medio a menos de 2.2 por diez a la menos siete, y el radio medio a 6.6 por diez a la menos siete de tres medios. En PIGS, la energía local vale menos un medio en todo camino, pero eso es tautológico: con W igual a cero no prueba nada. El control real es la distribución. Con ocho cadenas, el radio medio queda a menos 1.35 sigmas de tres medios y el de r cuadrado a menos 0.94 sigmas. El histograma pasa con p igual a 0.004, por encima del umbral de una milésima, pero justo.

### 6. Controles exactos: Hulthén y pozo cuadrado (Juan Sebastián, 50 s)

**En la lámina:**

- Controles exactos: Hulthén y pozo cuadrado
- 13_controles.json vía tabla 15 (filas B8 a B27). Hulthén: E = −(1/2)(1 − δ/2)², ⟨r⟩ = (12 − δ²)/(2(4 − δ²)). Pozo: transferencia sin U_C, salto en un nodo con borde medio.
| Control | Resultado |
| Hulthén δ = 0.2, 1.0, 1.5 | E_ext − E_exacta: 5.1×10⁻⁹, 2.5×10⁻⁹, −1.8×10⁻⁹ |
| Hulthén, orden de Trotter | 1.990 y 1.991 (δ = 1.0, 1.5) |
| Pozo V₀ = 2, orden medido | 1.497, 1.499, 1.502 |
| Pozo V₀ = 2, E_ext − E_exacta | 3.5×10⁻⁶ (ley ε²: −1.2×10⁻⁴) |
| Pozo V₀ = 1.3, E_ext − E_exacta | −4.2×10⁻⁷ |
| Pozo V₀ = 1.3, ajuste ε^1.5 a 5 puntos | 2.2×10⁻⁵ > 10⁻⁵: no pasa |
- • Hulthén: misma singularidad −1/r, mismo método sin cambios; sesgo ε², extrapolado a ≤ 5×10⁻⁹ / • Pozo: un salto en V cambia la ley a ε^(3/2); con la ley ε² del plan el error sería 30 veces mayor
- [imagen: figuras/13_controles.png]

**Se dice:**

> Tras la Fase 1, el profesor pidió controles exactos. Hulthén tiene la misma singularidad y solución exacta, así que entra en el mismo método sin cambios: con delta 0.2, 1 y 1.5, la transferencia extrapolada queda a menos de 5.1 por diez a la menos nueve del exacto, y el sesgo baja como epsilon cuadrado, con orden 1.99. El pozo cuadrado enseña otra cosa: con un salto en el potencial, el sesgo no va como epsilon cuadrado sino como epsilon a la tres medios. Extrapolando con el orden medido queda a 3.5 por diez a la menos seis; con la ley epsilon cuadrado el error sería de 1.2 por diez a la menos cuatro. Luis Felipe sigue con los resultados.

### 7. Cálculo preliminar en δ = 0.2: radial frente a tiempo imaginario (Luis Felipe, 42 s)

**En la lámina:**

- Cálculo preliminar en δ = 0.2: radial frente a tiempo imaginario
- 16_primer_grafico.png; cifras de 11_transferencia.json y 12_pigs.json. Radial: R = 40, h = 1/80 y 1/160. PIGS: semillas 20262000–07.
| δ = 0.2 | E₀ | ⟨r⟩ |
| Radial | −0.3268085110 | 1.54972 |
| Transf. ε → 0 | −0.3268085066 | — |
| Transf. ε = 0.1 | −0.3268085215 | 1.54974 |
| PIGS τ = 20 | −0.326725 ± 0.000068 | 1.5537 ± 0.0071 |
- Diferencias con el radial / • Transferencia ε = 0.1: −1.0×10⁻⁸ / • Transferencia ε → 0: 4.4×10⁻⁹ / • PIGS: E a +1.22σ, ⟨r⟩ a +0.56σ, ⟨r²⟩ = 3.243 ± 0.039
- [imagen: figuras/16_primer_grafico.png]

**Se dice:**

> Gracias. Este es el primer gráfico: radial frente a tiempo imaginario en delta 0.2. En el panel a, la transferencia con epsilon 0.1 queda a uno por diez a la menos ocho del radial, y extrapolada a epsilon cero, a 4.4 por diez a la menos nueve. PIGS, con tau igual a 20 y ocho cadenas, da menos 0.326725 más o menos 0.000068: está a 1.22 sigmas. En el panel b, el radio medio de PIGS es 1.554 más o menos 0.007, a 0.56 sigmas del radial, 1.5497. Los tres métodos coinciden dentro de sus errores.

### 8. Proyección desde una función de prueba no exacta (Luis Felipe, 51 s)

**En la lámina:**

- Proyección desde una función de prueba no exacta
- 12_pigs.json (tau_scan, proyeccion_informativo), 11_transferencia.json (proyeccion), 12c_pigs_coulomb_tau5.json (C_tau5_combinado). ε = 0.1, u_T = r e^(−r).
- u_T = r e−r no es exacta para δ > 0
| τ = 5 | E_mixto | Desvío |
| Producción (8) | −0.326955 | −3.19σ |
| Réplica 1 (16) | −0.326761 | +0.03σ |
| Réplica 2 (16) | −0.326718 | +0.99σ |
| Las 40 cadenas | −0.326785 | −0.83σ |
- Transferencia en τ = 5: −0.326763 / χ² de las 3 corridas: p = 0.011 / Decisión pendiente de firma
- • Mixto (transferencia): sobra 2.3×10⁻⁴ en τ = 1 y 2.6×10⁻⁷ en τ = 20 / • Puro ⟨r⟩ en PIGS, τ = 2 → 20: −0.033 (−3.6σ); transferencia −0.031
- [imagen: figuras/12_pigs_tau.png y ecuación de E_mixto]

**Se dice:**

> La proyección parte de una función de prueba que no es exacta. La energía mixta baja de forma monótona hacia E cero: sobra 2.3 por diez a la menos cuatro en tau igual a 1 y solo 2.6 por diez a la menos siete en tau igual a 20. El estimador puro del radio sí muestra la proyección en PIGS, a la derecha. Un punto no pasa: en tau igual a 5 la producción queda a menos 3.19 sigmas. Repetimos con 32 cadenas nuevas: las réplicas dan más 0.03 y más 0.99 sigmas, y las 40 cadenas juntas, menos 0.83. Pero las tres corridas no concuerdan del todo, con p igual a 0.011, así que no lo damos por cerrado.

### 9. Errores sistemáticos: Trotter y malla (Luis Felipe, 39 s)

**En la lámina:**

- Errores sistemáticos: Trotter y malla
- 11_transferencia.json (trotter, estabilidad_nystrom, orden_nystrom); tabla 15, filas A7 a A14. R = 40 (δ = 0.2) y R = 174 (δ = 1.0).
- Trotter (ley ε²) / • Orden 1.958 (δ = 0.2) y 1.983 (δ = 1.0) / • Extrapolado ε → 0 en δ = 0.2: 4.4×10⁻⁹ del radial
- Malla de Nyström: no pasa / • |E(0.04) − E(0.02)| hasta 3.2×10⁻⁶ > 10⁻⁶ / • Error de extremo en la cúspide: ∝ h⁴/ε (orden 4.00) / • Remedio: Richardson en h (exponente 4); pendiente de firma
- [imagen: figuras/11_trotter.png]

**Se dice:**

> Dos errores sistemáticos de la transferencia. El de Trotter baja como epsilon cuadrado: orden 1.96 en delta 0.2 y 1.98 en delta 1, siempre que antes quitemos el error de malla. Ese error de malla nace en la cúspide del origen, va como h a la cuarta sobre epsilon, y hace fallar nuestro control de estabilidad: 3.2 por diez a la menos seis entre h 0.02 y 0.04, frente a una tolerancia de diez a la menos seis. Con Richardson en h desaparece; esa redefinición del control está pendiente de firma.

### 10. Riesgo principal: la caja cerca del umbral (Luis Felipe, 59 s)

**En la lámina:**

- Riesgo principal: la caja cerca del umbral
- 14_cajas.json (celdas, veredictos, pared). Transferencia extrapolada en h y ε; radial con h = 1/40 y 1/80 y Richardson. Criterio 9.6 de la Fase 1.
| R | δ = 1.18: E₀ (transf.) | ⟨r⟩/R | δ = 1.20: E₀ (transf.) | ⟨r⟩/R |
| 50 | 3.36×10⁻⁴ | 0.293 | 6.41×10⁻⁴ | 0.324 |
| 100 | 3.19×10⁻⁵ | 0.268 | 1.87×10⁻⁴ | 0.332 |
| 200 | −2.41×10⁻⁵ | 0.225 | 5.79×10⁻⁵ | 0.352 |
| 400 | −3.08×10⁻⁵ | 0.153 | 1.84×10⁻⁵ | 0.386 |
| 800 | −3.10×10⁻⁵ | 0.080 | 5.67×10⁻⁶ | 0.426 |
- Condición (c): 9/9 ternas / mismo signo, misma tendencia y E₀ compatibles entre transferencia y radial / • 1.15: ligado (50/100/200) / • 1.18: ligado (200/400/800) / • 1.20: no ligado (a_s = −142.9)
- Cuidados / • Sin extrapolar en ε: sesgo hasta 5 % (ε = 0.1) y 20 % (ε = 0.2) de |E₀| / • Pared en R sin imagen: caja efectiva R + 0.5826√ε
- Avance: δc ∈ [1.18, 1.20] por los dos métodos; el intervalo final es de la Fase 4
- [imagen: figuras/14_cajas.png]

**Se dice:**

> El riesgo principal es la caja cerca del umbral. Allí el estado es un halo y una sola caja engaña: en delta 1.18, que está ligado, las cajas de 50 y 100 dan energía positiva. Por eso usamos el criterio de varias cajas, y la condición c exige que la transferencia y el radial den el mismo signo, la misma tendencia y energías compatibles. Se cumple en las nueve ternas. El veredicto: 1.15 ligado, 1.18 ligado con cajas de 200 a 800, y 1.20 no ligado, con el radio relativo subiendo a 0.43. Así delta c queda entre 1.18 y 1.20 por los dos métodos. Dos cuidados: sin extrapolar en epsilon, la transferencia exagera la ligadura hasta un 20 por ciento de la energía; y la pared en R no tiene imagen, lo que corre la caja un poco hacia afuera.

### 11. Balance de la Fase 2 y qué sigue (Luis Felipe, 33 s)

**En la lámina:**

- Balance de la Fase 2 y qué sigue
- secciones/15_tabla_controles.md (generada por 16_tabla_controles.py desde los JSON). Estado: SIN FIRMAR.
- filas en la tabla de controles
- pasan
- no pasan (causa medida)
- medidas o informativas
- Lo que ya tenemos / • Acción de pares con peso real, positivo y normalizable / • Radial, transferencia y PIGS de acuerdo en δ = 0.2 / • Hulthén exacto a 10⁻⁹; pozo: ley ε^(3/2) / • Criterio de cajas con la condición (c): δc ∈ [1.18, 1.20]
- Pendiente / • Firma de la tabla (Juan Sebastián) y 6 decisiones / • Imagen en R o caja efectiva; τ = 5 / • Fase 3: ⟨r⟩ cerca del umbral (transferencia) / • Fase 4: intervalo final de δc

**Se dice:**

> En resumen: la tabla de controles tiene 88 filas; 70 pasan, 9 no pasan y 9 son medidas. Los que no pasan tienen causa medida y los mostramos tal cual. La tabla aún no está firmada: faltan seis decisiones del equipo, entre ellas la imagen en R y el caso tau igual a 5. Lo que sigue es la Fase 3, el radio cerca del umbral, y la Fase 4, el intervalo final de delta c. Gracias; quedamos atentos a sus preguntas.

### 12. Respaldo 1: los controles que no pasan (respaldo, no se expone)

**En la lámina:**

- Respaldo 1: los controles que no pasan
- secciones/15_tabla_controles.md, sección «Lo que no pasa y por qué».
| Fila | Control | Valor | Causa medida |
| A5 | δ = 0.2, transferencia con h = 0.04 | 1.51×10⁻⁶ y 3.22×10⁻⁶ > 10⁻⁶ (ε = 0.1, 0.05) | error de malla h⁴/ε en la cúspide |
| A7 | Ley ε² en δ = 0.2 sin Richardson en h | orden 1.046 | Trotter del tamaño del error de malla |
| A13 | Estabilidad Nyström 0.02 → 0.04 | hasta 3.20×10⁻⁶ > 10⁻⁶ | error de extremo del trapecio, h⁴/ε |
| A16 | PIGS frente a transferencia, τ = 2, 5, 10, 20 | τ = 5: −3.2σ en E | réplicas +0.03σ y +0.99σ; p = 0.011 |
| B27 | Pozo V₀ = 1.3, ajuste ε^1.5 a 5 puntos | +2.16×10⁻⁵ > 10⁻⁵ | orden aún preasintótico (1.67 → 1.52) |
| C4 | Orden de Trotter en las cajas | 12/15; 1.65, 1.49, 1.79 | pared en R sin imagen (R = 50, 100) |
| C5 | Orden de la malla cerca del umbral | 1.361 (R = 50); 2.287 (R = 100) | no es 4: usar h = 0.02 y 0.01 |
| D19 | L16 propagador libre (suma) | 8.1×10⁻⁵ a 3.2×10⁻⁴ frente a 10⁻¹⁰ | criterio mal fijado: error O(h²) |
| E1 | Radial δ = 0.2 (h = 1/40, 1/80) | +6.23×10⁻⁹ > 5×10⁻⁹ | con h = 1/80, 1/160: +4.0×10⁻¹⁰ |

*Se muestra si preguntan por los fallos.*

### 13. Respaldo 2: límites físicos con la integral de camino (respaldo, no se expone)

**En la lámina:**

- Respaldo 2: límites físicos con la integral de camino
- 15_limites.py → 15_limites.json; tabla 15, parte D.
| Límite (δ = 0.2 salvo L19) | Valor (tabla 15, parte D) |
| L05 Hellmann-Feynman | 0.74485846 frente a 0.74485290 (+5.6×10⁻⁶) |
| L06 virial | −1.33×10⁻⁴ (h = 0.02) → extrapolado −5.91×10⁻⁷ |
| L07 cúspide | a₂/a₁ = −0.99937 |
| L14 estado 2s | E₁ = −0.012107865 (dif. con radial 2.1×10⁻¹⁰) |
| L19 δ = 2 sin ligado | E(200) = +1.219×10⁻⁴; ley de caja a −1.0×10⁻³ |
- [imagen: figuras/15_limites.png]

*Se muestra si preguntan por la lista de límites de la IA (L01 a L19).*

### 14. Respaldo 3: la pared en R sin imagen (respaldo, no se expone)

**En la lámina:**

- Respaldo 3: la pared en R sin imagen
- 14_cajas.json (pared, V3_criterio_estricto).
| Celda | Orden sin corregir | Con R + β√ε: orden | Residuo extrapolado |
| 1.15, R50 | 1.84 | 1.985 | 7.5×10⁻⁸ |
| 1.18, R50 | 1.65 | 1.984 | 1.5×10⁻⁷ |
| 1.2, R50 | 1.49 | 1.984 | 2.1×10⁻⁷ |
| 1.2, R100 | 1.79 | 1.991 | 2.7×10⁻⁸ |
- • K_D solo tiene imagen en r = 0: la pared en R se vigila solo en los nodos de tiempo, y la caja efectiva es R + β√ε, β = 0.5826 / • Criterio estricto |dif| ≤ err_tr: 15/15 con el término de pared y 6/15 sin él / • No cambia ningún signo ni tendencia; poner imagen en R lo decide el equipo (decisión 5)

*Se muestra si preguntan por la caja efectiva.*

### 15. Respaldo 4: decisiones pendientes de firma (respaldo, no se expone)

**En la lámina:**

- Respaldo 4: decisiones pendientes de firma
- secciones/15_tabla_controles.md, «Decisiones pendientes de firma (Juan Sebastián)».
- 1. Redefinir el control de tabulación de 9.7 como Richardson en h con exponente 4 y estabilidad del valor extrapolado (sección 11.4). / 2. Si la anomalía de τ=5 queda cerrada con las réplicas y la combinación (parte A; sección 12). / 3. El umbral 0.1 de la desviación de la ley de caja para "no ligado" (sección 14.5). / 4. El tratamiento del pozo con orden ε^(3/2) y extrapolación en h de orden ~1 (sección 13). / 5. Si se corrige la pared en R (imagen en R o R_ef) en las Fases 3 y 4, o se mantiene el término de pared en el error (sección 14.4). / 6. Si se acepta la corrección de Wigner-Kirkwood de U_C fuera de r=10 como parte del método (sección 11.9).

*Se muestra si preguntan qué falta para cerrar la fase.*

### 16. Respaldo 5: registro de la IA en la Fase 2 (respaldo, no se expone)

**En la lámina:**

- Respaldo 5: registro de la IA en la Fase 2
- verificacion/V1_recalculo_independiente.md, V2_auditoria_adversarial.md, V3_respuesta_hallazgos.md.
- Cómo trabajamos / • Claude escribió los módulos y scripts; cada cifra sale de un script ejecutado / • V1: recálculo independiente con código propio (disparo, FEDVR) / • V2: auditoría adversarial que buscó fallos a propósito / • V3: respuesta a cada hallazgo, con copia previa de todo
- Errores de la IA que se corrigieron / • Signo cambiado en el desplazamiento espectral de U_C (detectado frente a la Fase 1) / • El código afirmaba un error de extremos menor que el real fuera de r = 10: se añadió Wigner-Kirkwood / • Un criterio inventado sin aprobar («proyección visible»): se pasó a informativo / • La pared sin imagen no estaba declarada: ahora el código avisa y estima el sesgo

*Se muestra si preguntan cómo se usó la IA y qué se corrigió.*

## Preguntas probables del profesor y respuestas

Responde por defecto quien expuso el tema, pero los dos deben poder contestar cualquiera.

**P: ¿Por qué no usan la acción primitiva, o un potencial suavizado, si es más sencillo?**  
R: Con la primitiva el peso no es normalizable: e^(ε/r) explota en el origen (en r = 0.01 con ε = 0.1 el exponente ya vale 10). El suavizado introduce un parámetro que mueve el umbral y habría que extrapolarlo. Con la acción de pares la singularidad va dentro del núcleo exacto: U_C(0.01, 0.01) = −0.788 es finita y el resto W está acotado en [0, δ]. (JS)

**P: ¿Cómo saben que el peso es normalizable y positivo, y no solo lo suponen?**  
R: Lo comprueba el código en cada tabla: 0 elementos negativos y 0 no finitos en la matriz, y U_C acotada en el origen. Además, en δ = 0 el método reproduce E = −1/2 para todo ε, que no pasaría si el peso estuviera mal normalizado. (JS)

**P: Si PIGS es la integral de camino, ¿para qué la transferencia?**  
R: Usan la misma acción. La transferencia no tiene ruido, llega a cajas de R = 800 y separa los errores sistemáticos (Trotter, malla, proyección) del ruido estadístico. PIGS es el Monte Carlo que pide la guía; cerca del umbral su tiempo de proyección crece como 1/|E0| y no es viable (Fase 1), así que lo usamos hasta δ ≈ 1. (LF)

**P: El punto τ = 5 está a −3.19σ. ¿No es un sesgo del PIGS?**  
R: Lo reportamos tal cual. Dos réplicas con semillas nuevas dan +0.03σ y +0.99σ, y las 40 cadenas juntas −0.83σ. Pero las tres corridas no concuerdan del todo (p = 0.011), así que no lo damos por cerrado: es la decisión 2 pendiente de firma. En τ = 2, 10 y 20 el acuerdo es menor que 2σ. (LF)

**P: ¿Por qué el pozo cuadrado da ε^(3/2) y no ε²?**  
R: Lo medimos: órdenes 1.497, 1.499, 1.502 en V0 = 2. La ley ε² supone un potencial suave; con un salto, la factorización falla en una capa de anchura ~√ε alrededor del salto (explicación plausible, no demostrada). Si se extrapolara con ε² el error sería −1.2×10⁻⁴; con el orden medido queda en 3.5×10⁻⁶. Por eso el Yukawa, que es suave salvo en el origen (y esa parte la absorbe U_C), sí sigue ε². (JS)

**P: Si en δ = 1.18 una caja da E > 0, ¿cómo deciden que está ligado?**  
R: Con el criterio de varias cajas de la Fase 1 (9.6): al menos tres cajas en razón 2, malla convergida, y las tendencias de E0, ⟨r⟩/R y F1/2. En 1.18, ⟨r⟩/R baja de 0.225 a 0.080 entre R = 200 y 800 (estado localizado); en 1.20 sube hasta 0.426 (estado de caja, con la ley de dispersión de a_s). La condición (c) exige que transferencia y radial coincidan en signo y tendencia: se cumple en 9/9 ternas. (LF)

**P: Un control de la malla de Nyström no pasa. ¿Por qué siguen adelante?**  
R: Porque la causa está medida: es error de extremo del trapecio en la cúspide del origen, va como h⁴/ε (orden 4.00) y vale hasta 3.2×10⁻⁶. Con Richardson en h desaparece y el extrapolado queda a 4.4×10⁻⁹ del radial. La redefinición del control está pendiente de firma. Cerca del umbral el orden no es 4, así que en la Fase 4 usaremos h = 0.02 y 0.01. (LF)

**P: ¿Qué hizo la IA y qué verificaron ustedes?**  
R: Claude escribió los módulos y scripts. Hubo dos verificaciones: un recálculo independiente con código propio (V1) y una auditoría adversarial (V2); cada hallazgo se respondió en V3 recalculando. Ejemplos de errores corregidos: un signo en la tabla U_C, una afirmación falsa sobre el error fuera de r = 10 y la pared en R sin imagen, que no estaba declarada. Ninguna cifra de la presentación está escrita a mano. (JS)

