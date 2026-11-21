# Material para auditoría (parte 2 de 3)

Responde solo "Recibido".

## controles.md

# Tabla de controles de E5 (generada por `codigo/07_controles.py` desde los JSON)

Los criterios se fijaron antes de correr los Monte Carlo (`criterios_previos.md`; las filas C8b, C16 y C9b y la restricción x ≥ x_min de C10 están en su adenda, escrita después de una prueba preliminar y antes de las corridas finales).

Resumen: 43 filas; 34 pasan, 4 no pasan (con su causa medida), 1 no aplicable, 4 informativas.

| # | control | criterio fijado antes | valor | ¿pasa? | script |
|---|---|---|---|---|---|
| C1 | a(δ): disparo frente a fase variable (7 δ) | dif. rel. < 1e-8 | máx 1.7e-11 | sí | 01 |
| C2 | a(1.20) frente a −142.9 de la Fase 3 | |Δa| < 0.05 | -142.9349 (|Δa| = 0.035) | sí | 01 |
| C3 | Perfil φ(r): disparo frente a Nyström | máx |Δφ| < 1e-5 (r ≤ 8) | δ=1.2: 2.2e-04; δ=1.3: 2.1e-05; δ=1.5: 3.7e-06; δ=2: 3.1e-06; δ=2.5: 1.3e-06; δ=3: 8.1e-08; δ=4: 2.0e-07 | **no pasa** | 01 |
| C4 | Identidad a = −(2/δ²) E_Γ[φ] | dif. rel. < 1e-8 | máx 4.7e-12 | sí | 01 |
| C5 | Mezcla de exponenciales frente a Ciesielski–Taylor (k = 1..5) | err. rel. < 1e-6 | máx 9.9e-12 | sí | 01 |
| C6 | δ/p_1 = δ_c(1s), δ/p_2 = δ_c(2s) | err. rel. < 1e-7 | 1.190612421060 (-1.3e-13); 0.3102092827 (-5.6e-08) | sí | 01 |
| C7 | MC libre δ = 3, 4: a extrapolado (η⁴) y φ(r) en 7 radios | |MC − EDO| < 3σ | a: -0.70σ, -0.12σ; φ(r): máx |dev| 1.37σ | sí | 02 |
| C8 | Orden del sesgo con el trapecio | entre 1.5 y 2.5 | media infinita para todo η (Prop. 3); a = -2.4e+145 (η = 0.8) | no aplicable | 02 |
| C8b | Orden del sesgo con el esquema de puente (δ = 2.5, 3, 4) | entre 3 y 5 (fijado tras prueba preliminar) | 3.25, 4.58, 3.35, 3.97, 3.49, 3.40 | sí | 02 |
| C9 | θ̂ = δ κ̂ (cola de X, 1 % superior) frente a δ/δ_c | |θ̂ − δ/δ_c| < 3σ_θ | κ̂ = 0.84160 ± 0.00266 frente a 1/δ_c = 0.83990 (+0.64σ, igual para todos los δ) | sí | 03 |
| C9b | θ̂ con partida fija r₀ = 1, δ = 1.5 (independiente) | |θ̂ − δ/δ_c| < 3σ | 1.2557 ± 0.0089 frente a 1.2599 (-0.47σ) | sí | 03 |
| C10 | Ley de X frente a la mezcla (KS, x ≥ x_min) | √N·D < 1.63 | √N·D = 1.11 (x_min = 0.0211) | sí | 03 |
| C11 (δ=1.5) | Pendiente log-log de la varianza muestral | ±0.15 de 2/θ − 1 | +0.784 frente a +0.587 | **no pasa** | 03 |
| C11 (δ=2) | Pendiente log-log de la varianza muestral | ±0.15 de 2/θ − 1 | +0.343 frente a +0.191 | **no pasa** | 03 |
| C11 (δ=3) | Pendiente log-log de la varianza muestral | |pendiente| < 0.1 | +0.081 | sí | 03 |
| C11 (δ=4) | Pendiente log-log de la varianza muestral | |pendiente| < 0.1 | +0.031 | sí | 03 |
| C12 | MI con supersolución: pesos ≤ 1 | máx(peso) ≤ 1 | 1.000000 | sí | 04, 05 |
| C13 (δ=3) | a_MI (η = 0.1) frente a la EDO | |Δ| < 3σ (σ = estadística + sesgo medido) | -0.34283 frente a -0.34324: +2.38σ (extrapolado p = 3.20: +3.85σ; p = 2: +1.39σ) | sí | 04 |
| C13 (δ=1.5) | a_MI (η = 0.1) frente a la EDO | |Δ| < 3σ (σ = estadística + sesgo medido) | -3.65861 frente a -3.66823: +2.10σ (extrapolado p = 3.20: +2.38σ; p = 2: +1.32σ) | sí | 04 |
| C13 (δ=1.3) | a_MI (η = 0.1) frente a la EDO | |Δ| < 3σ (σ = estadística + sesgo medido) | -11.54919 frente a -11.57992: +1.38σ (extrapolado p = 3.20: +1.30σ; p = 2: +0.81σ) | sí | 04 |
| C13 (δ=1.25) | a_MI (η = 0.1) frente a la EDO | |Δ| < 3σ (σ = estadística + sesgo medido) | -21.94346 frente a -21.94869: +0.09σ (extrapolado p = 3.20: -0.03σ; p = 2: -0.19σ) | sí | 04 |
| C13 (δ=1.2) | a_MI (η = 0.1) frente a la EDO | |Δ| < 3σ (σ = estadística + sesgo medido) | -142.24039 frente a -142.93487: +0.72σ (extrapolado p = 3.20: +0.71σ; p = 2: +0.66σ) | sí | 04 |
| C13 (δ=1.2, inf.) | a_MI (η = 0.2) cerca del umbral | informativo (σ = estadística + sesgo de 04) | -142.66 ± 0.96 frente a -142.93 (+0.29σ) | medido | 05 |
| C13 (δ=1.195, inf.) | a_MI (η = 0.2) cerca del umbral | informativo (σ = estadística + sesgo de 04) | -306.03 ± 2.39 frente a -306.71 (+0.28σ) | medido | 05 |
| C13 (δ=1.192, inf.) | a_MI (η = 0.2) cerca del umbral | informativo (σ = estadística + sesgo de 04) | -975.24 ± 9.44 frente a -971.54 (-0.39σ) | medido | 05 |
| C13 (δ=1.1907, inf.) | a_MI (η = 0.2) cerca del umbral | informativo (σ = estadística + sesgo de 04) | -15889.76 ± 421.82 frente a -15404.50 (-1.15σ) | medido | 05 |
| C14 (δ=3) | Varianza relativa medida frente a la cota | medida ≤ cota + 3σ | 0.0263 ≤ 0.0988 | sí | 04 |
| C15 (δ=3) | Varianza muestral estable con n (MI) | |pendiente| < 0.1 | -0.002 (η = 0.1) | sí | 04 |
| C14 (δ=2) | Varianza relativa medida frente a la cota | medida ≤ cota + 3σ | 0.0701 ≤ 0.1919 | sí | 04 |
| C15 (δ=2) | Varianza muestral estable con n (MI) | |pendiente| < 0.1 | -0.010 (η = 0.1) | sí | 04 |
| C14 (δ=1.5) | Varianza relativa medida frente a la cota | medida ≤ cota + 3σ | 0.1509 ≤ 0.3333 | sí | 04 |
| C15 (δ=1.5) | Varianza muestral estable con n (MI) | |pendiente| < 0.1 | -0.006 (η = 0.1) | sí | 04 |
| C14 (δ=1.3) | Varianza relativa medida frente a la cota | medida ≤ cota + 3σ | 0.2283 ≤ 0.4540 | sí | 04 |
| C15 (δ=1.3) | Varianza muestral estable con n (MI) | |pendiente| < 0.1 | +0.013 (η = 0.1) | sí | 04 |
| C14 (δ=1.25) | Varianza relativa medida frente a la cota | medida ≤ cota + 3σ | 0.2552 ≤ 0.4964 | sí | 04 |
| C15 (δ=1.25) | Varianza muestral estable con n (MI) | |pendiente| < 0.1 | +0.004 (η = 0.1) | sí | 04 |
| C14 (δ=1.2) | Varianza relativa medida frente a la cota | medida ≤ cota + 3σ | 0.2959 ≤ 0.5461 | sí | 04 |
| C15 (δ=1.2) | Varianza muestral estable con n (MI) | |pendiente| < 0.1 | +0.031 (η = 0.2) | sí | 04 |
| C16 (η=0.8) | E[δΛ] = 1 (esquema de puente) | |E − 1| < 3σ | 0.98861 ± 0.00030 (-38.59σ) | **no pasa** | 02 |
| C16 (η=0.4) | E[δΛ] = 1 (esquema de puente) | |E − 1| < 3σ | 1.00032 ± 0.00035 (+0.89σ) | sí | 02 |
| C16 (η=0.2) | E[δΛ] = 1 (esquema de puente) | |E − 1| < 3σ | 0.99952 ± 0.00036 (-1.32σ) | sí | 02 |
| C16 (η=0.1) | E[δΛ] = 1 (esquema de puente) | |E − 1| < 3σ | 1.00026 ± 0.00066 (+0.39σ) | sí | 02 |
| C16 (03) | E[δΛ] = 1 en la muestra de 03 | |E − 1| < 3σ | 1.00004 ± 0.00036 | sí | 03 |

## Notas

- **C3.** no pasa en δ = 1.2, 1.3. Causa: el núcleo 1/max(r, r') tiene un quiebre en r' = r y los puntos de la rejilla del MC no son nodos de Nyström; el error absoluto escala con φ (≈ 250 en δ = 1.2). El error relativo en δ = 1.2 es 1.0e-06 con 600 paneles y baja a 1.4e-07 con 1200 (08_verificacion); a coincide a 4.2e-11. Es un error del método de control, no del disparo.
- **C8.** El criterio presuponía un estimador con media finita; el trapecio no lo es (adenda 1 de criterios_previos.md).
- **C9.** Los 7 δ comparten la muestra (covarianza de escala); no son 7 controles independientes.
- **C10.** Una sola muestra universal vale para δ = 3 y 4 (y para todos los δ).
- **C11 (δ=1.5).** Causa medida: el estadístico es preasintótico y muy ruidoso. Con muestras de la ley exacta del mismo tamaño da +0.616 ± 0.086 (10 muestras); el MC queda a z = +1.97.
- **C11 (δ=2).** Causa medida: el estadístico es preasintótico y muy ruidoso. Con muestras de la ley exacta del mismo tamaño da +0.262 ± 0.039 (10 muestras); el MC queda a z = +2.06.
- **C13 (δ=3).** La extrapolación con el orden de la regla de 04 (p = 3.20, promedio de pares preasintóticos) queda a 3.85σ; con p = 2 (orden de Euler; par más fino observado 1.93) queda a +1.39σ. La revisión a p = 2 se hizo después de ver los datos (04b).
- **C15 (δ=1.2).** Con η = 0.1 solo hay N = 7007 caminos (menos de 10 bloques de 2000); se usa la corrida con η = 0.2.
- **C16 (η=0.8).** Causa: con η = 0.8 los pasos son tan largos que la cuadratura de 3 nodos en el tiempo del puente no basta (la media del puente sí es exacta). Con η ≤ 0.4 pasa.


## verificacion.md

# Verificación de E5: comprobaciones independientes y relectura del código

Todas las cifras salen de `resultados/*.json` (entre paréntesis, el archivo).

## 1. Segundos métodos y casos exactos

| Qué se comprueba | Cómo | Resultado |
|---|---|---|
| a(δ) | Tres métodos independientes: disparo lineal DOP853 (M1), fase variable de Calogero (Riccati, M2), Nyström de la ecuación integral (M3), más `comun3.long_dispersion` de la Fase 3 | M2 y M3 coinciden con M1 a ≤ 1.7e-11 relativo en los 7 δ; a(1.20) = −142.9349, frente a −142.9 de la Fase 3 (01) |
| Perfil φ(r) | Disparo frente a Nyström | Diferencia relativa 1.0e-6 en δ = 1.2 con 600 paneles, 1.4e-7 con 1200 (08): el control C3 no pasa en δ = 1.2 y 1.3 por el método de control, que converge al refinar |
| Ley de Λ | Caso exacto de Ciesielski–Taylor (pozo cuadrado, φ(0) = 1/cos√(2p)), derivado aquí | p_k y w_k (k = 1…5) con error ≤ 9.9e-12 (01) |
| Polos | δ/p_1 y δ/p_2 frente a δ_c(1s) y δ_c(2s) | 1.190612421060 y 0.3102092827 en los 7 δ (01) |
| Identidad del estimador | a = −(2/δ²) E_Γ[φ] por Gauss–Laguerre | ≤ 4.7e-12 (01) |
| Pendiente c = −d(1/a)/dδ en δ_c | Diferencias finitas de la EDO | 0.7413, igual a la pendiente 0.741 de κ de la Fase 3 (01): 1/a es analítica a través del umbral |
| E[Λ] exacto | S(r) en forma cerrada (G_0 q); E_Γ[δΛ] = 1 | MC con η ≤ 0.4: compatible (02, 03); partida r_0 = 1 en δ = 2: 0.43211 ± 0.00053 frente a 0.43233 (08) |
| E[W²] (δ = 4) | Gauge de 2q por EDO | MC 2.2053 ± 0.0058 frente a 2.2069 (08); varianza relativa 0.2054 frente a 0.2071 |
| Covarianza de escala | Misma semilla, δ = 1 y 2.7 | δΛ idénticos hasta 5.6e-15 (08) |
| Pesos del MI ≤ φ_T(r_0) | Partida fija r_0 = 0.5, δ = 1.5, η = 0.1 | máx Y = 6.668289 ≤ φ_T = 6.693432; varianza relativa 0.0234 ≤ cota 0.1927; media 5.60619 ± 0.00271 frente a 5.61188 (08) |
| θ independiente de la partida | Partida fija r_0 = 1 en δ = 1.5 | θ = 1.2557 ± 0.0089 frente a 1.2599 (03) |
| C11 a tamaño finito | El mismo estadístico sobre 10 muestras de la ley exacta | δ = 1.5: +0.616 ± 0.086 (MC +0.784, z = +1.97); δ = 2: +0.262 ± 0.039 (MC +0.343, z = +2.06) (03). El MC es compatible con la ley exacta a ~2σ; lo que falla es la comparación con la pendiente asintótica |

## 2. Lo que encontramos al revisar (y cambió el trabajo)

1. **El trapecio da media infinita.** El primer simulador usaba dt[q(r) + q(r')]/2. En δ = 3 dio a ≈ −10^{239}. La
   causa (Proposición 3 de `teoria.md`) es que el extremo r' cae cerca del origen con densidad ∼ r'² y e^{C/r'} no es
   integrable. Se cambió a la media exacta sobre el puente browniano (forma cerrada del Yukawa promediado sobre una
   gaussiana), que además da un estimador dominado por el exacto (Jensen condicional). La forma cerrada se comprobó
   contra cuadratura numérica en una prueba de desarrollo (no guardada en JSON): diferencia ≤ 1e-14 en seis puntos,
   salvo 1e-7 en R/σ = 7e-4 con el primer umbral del límite R → 0; desde entonces ese límite se usa solo si R/σ < 1e-5.
2. **Euler 3D en la difusión guiada.** Con el Euler de la deriva ∇ ln φ_T en 3D, las dos derivas grandes (+1/r de
   Bessel-3 y ≈ −1/r de la guía) se discretizan por separado. Se pasó a un paso híbrido (imagen radial 1D con la deriva
   total pequeña para r ≥ 1/δ_T).
3. **Orden de la extrapolación del MI.** La regla de 04 promedió órdenes preasintóticos (p = 3.20); el extrapolado de
   δ = 3 quedó a +3.85σ. El par más fino (η = 0.1/0.05) da 1.93 y el error de Euler es O(η²); con p = 2 (`04b`) los
   seis extrapolados quedan entre −0.19σ y +1.78σ. Esta revisión se hizo después de ver los datos; la tabla de
   controles evalúa C13 con la regla original (σ = estadística + sesgo medido) y pasa en los cinco δ.
4. **Guías que no son supersoluciones amplifican el sesgo.** Con δ_T = 1.8 > δ = 1.5, el sesgo de a con η = 0.2 es
   +3.9 %, y el exponente de la cola sale 2.30 ± 0.07 frente a 2.47 predicho; con η = 0.1 baja a +0.70 % y θ = 2.43 ± 0.08
   (08). Con la supersolución el sesgo de η = 0.2 es ≈ 0.5 %. Lo atribuimos a que los pesos > 1 hacen la media sensible
   a la cercanía de la criticidad efectiva del esquema discreto.
5. **Marca de camino truncado.** El núcleo guiado marcaba los caminos truncados con L = −1, que es un valor legítimo
   cuando E_L < 0 (guías con δ_T > δ). Se cambió a NaN. No afecta a 04 (allí E_L ≥ 0 y no hubo truncados).
6. **C15 en δ = 1.2 con η = 0.1:** N = 7007 no alcanza para 10 bloques de 2000; se usa la corrida con η = 0.2.

## 3. Relectura del código (17-11-2026)

Se releyó `fk_comun.py` y los scripts 01 a 08 línea por línea. Puntos comprobados:

- Frobenius: u = r − p r² + … para q ∼ 1/r; con r_0 = 1e-10 el error es despreciable también para el pozo cuadrado y
  para q_eff con coeficiente distinto en 1/r.
- `Guia`: b = (u/r)'/(u/r) = u'/u − 1/r y b1 = u'/u; en r = 0 se copia el valor del segundo nodo (la cancelación en
  r = 1e-9 da ruido). Fuera de R_in se usa la forma analítica 1 + A/r; el índice de la tabla nunca pasa de n_tab porque
  r ≤ R_in siempre (los caminos que salen se reinyectan exactamente en R_in o terminan).
- Cierre: probabilidad de volver R_in/r (libre) y (R_in + A)/(r + A) (guiado, función armónica de la transformada h).
- E_L = e^{−δ_T r}(1 − e^{−(δ−δ_T) r})/r con `expm1`: estable en r → 0 (límite δ − δ_T) y válida para δ_T > δ.
- Semillas: todas fijas y distintas por corrida (tabla en los JSON); el piloto que fija N en 04 y 05 también es
  determinista.
- Unidades: dt = η²r² con η adimensional; R_in = 36/δ (q(R_in) < 1e-16/R_in).

## 4. Cifras citadas en LEEME.md y seccion_articulo.md

Se comprobaron una por una contra los JSON después de la última corrida (17-11-2026). Las de la tabla de controles las
escribe `07_controles.py` directamente.


## fuentes.md

# Fuentes de E5 y su estado de verificación (17-11-2026)

Marcas: **[V]** verificada en la página del editor, DOI o índice (Numdam, AMS, Springer, RePEc); **[V-arXiv]** solo en
arXiv; **[no verificada]** no se abrió hoy. Para cada una se dice qué se comprobó y qué no. Todas las consultas se
hicieron con WebSearch/WebFetch el 17-11-2026. Los PDF de la AMS (ams.org) y de archive.numdam.org no se pudieron
descargar desde este entorno (el proxy los rechazó), salvo el de Numdam del artículo de Chung, que sí se leyó.

| # | Referencia | Marca | Qué se comprobó | Qué NO se comprobó |
|---|---|---|---|---|
| 1 | K. L. Chung, "The gauge and conditional gauge theorem", *Séminaire de probabilités* XIX (1985), 496–503, Springer LNM; MR 889497; numdam.org/item/SPS_1985__19__496_0 | [V] | Datos en Numdam; texto leído (OCR): D de medida finita, sin regularidad de ∂D, q acotada; "si u ≢ ∞ en D, u es acotada"; extensión de Zhao a q ∈ K_d en dominios acotados (d ≥ 3) | El símbolo "m(D) < ∞" está ilegible en el OCR; se reconstruyó del contexto |
| 2 | K. L. Chung y Z. Zhao, *From Brownian Motion to Schrödinger's Equation*, Grundlehren der math. Wiss. 312, Springer (1995), DOI 10.1007/978-3-642-57856-4 | [V] | Título, autores, serie y volumen, año, ISBN y DOI en la página de Springer | El contenido (no se pudo abrir el índice ni los capítulos) |
| 3 | M. Cranston, reseña del libro anterior, *Bull. AMS* 39 (1), 109–111 (2002), DOI 10.1090/S0273-0979-01-00925-9 | [V] | Volumen y páginas; el enunciado del teorema de la gauge como "acotada en D o idénticamente infinita", q en la clase de Kato, g(x) = E_x[exp ∫_0^τ V(B_s) ds] | La reseña no aclara si D es acotado ni trata ℝ^d |
| 4 | Z. Zhao, "Subcriticality and gaugeability of the Schrödinger operator", *Trans. AMS* 334, 75–96 (1992), DOI 10.1090/S0002-9947-1992-1068934-5 | [V] | Datos y resumen en la página de la AMS: −Δ/2 + V en ℝ^d, d ≥ 3, V ∈ K_d con condición de Kato en el infinito; teorema de equivalencia entre subcriticidad, positividad fuerte y gaugeabilidad | El enunciado completo (el PDF no se pudo descargar). Por eso el Teorema 1 de `teoria.md` se demuestra sin usarlo |
| 5 | Z. Zhao, "Subcriticality, positivity, and gaugeability of the Schrödinger operator", *Bull. AMS* 23, 513–517 (1990), DOI 10.1090/S0273-0979-1990-15965-8 | [V] | Título, volumen, páginas y DOI | Autor y contenido (la página no los muestra; el autor se infiere del título y de 4) |
| 6 | Z.-Q. Chen, "Gaugeability and conditional gaugeability", *Trans. AMS* 354 (11), 4639–4679 (2002) | [V] | Resumen en la AMS: para procesos de Borel transitorios con dual fuerte, gaugeabilidad, gaugeabilidad condicional y subcriticidad son equivalentes. Las páginas salen de la bibliografía de L. Li (arXiv:1603.07038) | El enunciado completo |
| 7 | P. J. Fitzsimmons y J. Pitman, "Kac's moment formula and the Feynman–Kac formula for additive functionals of a Markov process", *Stoch. Proc. Appl.* 79 (1), 117–134 (1999) | [V] | Revista, volumen y páginas en RePEc (econpapers/ideas); el informe técnico de Berkeley (n.º 427) da la fórmula P_μ(A_v^n) = n! μ G_v^n 1 con G_v = G M_v | — |
| 8 | M. Kac y J. M. Luttinger, "Scattering length and capacity", *Ann. Inst. Fourier* 25 (3-4), 317–321 (1975), DOI 10.5802/aif.586 | [V] | Datos y resumen en la página del editor y en EuDML: expresión de la longitud de dispersión como integral de Wiener y relación con la capacidad electrostática | La fórmula y las hipótesis sobre V (el PDF no se pudo descargar). No se cita su fórmula |
| 9 | P. He, "A formula on scattering length of dual Markov processes", *Proc. AMS* 139 (5), 1871–1877 (2011), DOI 10.1090/S0002-9939-2010-10618-4 | [V] | Datos y resumen: extiende la fórmula de Kac (probada por Takeda en el caso simétrico) a procesos con dualidad débil | El signo de V no figura en el resumen; las referencias que cita (Takeda, "positive smooth measures"; Taylor, "positive potentials") indican potenciales positivos |
| 10 | Z. Ciesielski y S. J. Taylor, "First passage times and sojourn times for Brownian motion in space and the exact Hausdorff measure of the sample path", *Trans. AMS* 103 (3) (1962), DOI 10.1090/S0002-9947-1962-0143257-8 | [V] | Título, autores, volumen, año y DOI | Páginas y contenido. La fórmula E_0[e^{pT}] = 1/cos√(2p) que usamos como caso exacto la derivamos nosotros (`teoria.md`, sección 5) |
| 11 | J. P. Edwards, U. Gerber, C. Schubert, M. A. Trejo, T. Tsiftsi y A. Weber, "Applications of the worldline Monte Carlo formalism in quantum mechanics", arXiv:1903.00536 | [V-arXiv] | Texto leído en arXiv (ar5iv y PDF): Yukawa con μ = 0 a 0.5 (m = α = 1), definición literal de "undersampling", ventana t ∈ [7, 15], suavizado por integrales de línea, cita μ_c ≈ 1.19 αm sin calcularlo | La revista (el texto no da referencia de publicación) |
| 12 | Fases 1–3 del grupo: `fase3/LEEME.md` (a_s(1.20) = −142.9, κ ≈ 0.741(δ_c − δ), δ_c = 1.1906124210606), `fase3/codigo/comun3.py` (long_dispersion), `fase2/codigo/pigs.py` | [V] (propias) | Valores y código leídos e importados sin modificar | — |
| 13 | Principio de Birman–Schwinger; desigualdad de Hardy–Littlewood–Sobolev (condición de Rollnik del Yukawa); teorema de Jentzsch | [no verificada] | Se usan como resultados estándar de libro; en `teoria.md` la identificación de 1/κ_1 se comprueba directamente (ψ = G_0 q^{1/2} e) y numéricamente (C6) | No se abrió ninguna fuente hoy |
| 14 | L. Li, "Criticality and subcriticality of generalized Schrödinger forms with non-local perturbations", arXiv:1603.07038 | [V-arXiv] | Solo como fuente secundaria de la referencia de Chen 2002 y de la frase "gaugeability has a very close connection with the subcriticality" | — |

**Lo que no encontramos:** ningún trabajo que use la gauge de Feynman–Kac de un potencial **atractivo** cerca de su
umbral como método numérico para la longitud de dispersión, ni que discuta la varianza infinita del estimador o la ley
de mezcla de exponenciales con tasas δ/δ_c(ns). Es una búsqueda limitada (unas 20 consultas), no una prueba de que no
exista.


## codigo/fk_comun.py

```python
"""fk_comun.py -- Proyecto 05, Fase 4, extension E5: utilidades comunes (EDO y Monte Carlo de caminos brownianos).

Unidades hbar = m = g = 1, generador (1/2) Laplaciano, V(r) = -e^{-delta r}/r. Escribimos q = -V = e^{-delta r}/r >= 0.

Representacion de Feynman-Kac a energia cero (delta > delta_c):
    phi(x) = E_x[ exp( int_0^inf q(B_t) dt ) ],   -1/2 Lap phi + V phi = 0,   phi(r) -> 1 - a/r,
    a = 2 int_0^inf r^2 V(r) phi(r) dr  (a < 0 sin ligado; convencion del grupo: a > 0 con ligado).
En radial: u = r phi, u'' = 2 V u = -2 q u, u(0) = 0. La solucion regular u~ (u~'(0) = 1) vale alpha (r - a) lejos,
y phi(r) = u~(r) / (alpha r).

Contenido
  * EDO: solucion regular u~ con DOP853 (metodo M1), fase variable de Calogero a'(r) = 2 V (r - a)^2 (metodo M2),
    ecuacion integral phi = 1 + G0 q phi resuelta por Nystrom (metodo M3, solo para el perfil).
  * Ley exacta de Lambda = int_0^inf q(B_t) dt: E_x[e^{p Lambda}] = phi_p(x) (solucion de energia cero de p q).
    Sus polos son p_k = 1/kappa_k (Birman-Schwinger), aqui p_k = delta / delta_c(k s). La ley de Lambda es la mezcla
    P(Lambda > lam) = sum_k w_k e^{-p_k lam},  w_k(r) = -u~_{p_k}(r) / (r alpha'(p_k) p_k).
  * Monte Carlo (nucleos compilados con numba, un camino tras otro, semilla fija): proceso radial de Bessel-3 con
    transicion EXACTA (norma de un gaussiano 3D) y paso adaptativo dt = eta^2 r^2. La integral de q en cada paso es la
    media EXACTA de int q sobre el puente browniano 3D entre los extremos (Yukawa promediado sobre la gaussiana del
    puente, cuadratura de 3 nodos en el tiempo). El trapecio simple NO sirve (media infinita, ver simular_libre).
    Cierre exacto fuera de R_in (si r > R_in, el camino vuelve a la esfera R_in con probabilidad R_in/r, y si vuelve se
    reinicia exactamente en R_in; si no, termina).
  * Muestreo por importancia (transformada h de Doob con phi_T): deriva grad ln phi_T (Euler en 3D), peso
    exp(-int E_L), E_L = (H phi_T)/phi_T. Con phi_T la solucion de energia cero de delta_T < delta, E_L = q_T - q >= 0.
    Cierre exacto: phi_T = 1 + A/r fuera de R_in, probabilidad de volver (R_in + A)/(r + A).
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

DELTA_C = 1.1906124210606       # 1s, referencia del proyecto (Fase 3)
DELTA_C2 = 0.31020928           # 2s, prototipos/umbrales_energia_cero.py (propuesta, seccion 3); se recalcula en 01


def q_yuk(r, d):
    return np.exp(-d * r) / r


# ----------------------------------------------------------------------------------------------- EDO, metodo M1
def regular(qfun, p=1.0, Rf=None, r_eval=None, rtol=1e-12, atol=1e-30, con_derivada_p=False, r0=1e-10, cortes=None):
    """Solucion regular de u'' = -2 p q(r) u, u(0) = 0, u'(0) = 1 (Frobenius: q ~ 1/r => u = r - p r^2).
    Devuelve dict con u, up en r_eval y en Rf; si con_derivada_p, tambien v = du/dp y v'."""
    if con_derivada_p:
        def f(r, s):
            qq = qfun(r)
            return [s[1], -2 * p * qq * s[0], s[3], -2 * qq * s[0] - 2 * p * qq * s[2]]
        y0 = [r0 - p * r0 ** 2, 1 - 2 * p * r0, -r0 ** 2, -2 * r0]
    else:
        def f(r, s):
            return [s[1], -2 * p * qfun(r) * s[0]]
        y0 = [r0 - p * r0 ** 2, 1 - 2 * p * r0]
    # integracion por tramos (cortes = discontinuidades de q, p. ej. el pozo cuadrado del control de Ciesielski-Taylor)
    bordes = [r0] + [c for c in (cortes or []) if r0 < c < Rf] + [Rf]
    sols = []
    for i in range(len(bordes) - 1):
        sol = solve_ivp(f, [bordes[i], bordes[i + 1]], y0, method="DOP853", rtol=rtol, atol=atol,
                        dense_output=r_eval is not None)
        sols.append(sol)
        y0 = sol.y[:, -1]
    out = dict(uR=sol.y[0, -1], upR=sol.y[1, -1], Rf=Rf)
    if con_derivada_p:
        out.update(vR=sol.y[2, -1], vpR=sol.y[3, -1])
    if r_eval is not None:
        re_ = np.asarray(r_eval, float)
        k = np.clip(np.searchsorted(bordes, re_, side="right") - 1, 0, len(sols) - 1)
        Y = np.empty((len(y0), re_.size))
        for i, s_ in enumerate(sols):
            m = k == i
            if m.any():
                Y[:, m] = s_.sol(re_[m])
        out.update(u=Y[0], up=Y[1])
        if con_derivada_p:
            out.update(v=Y[2], vp=Y[3])
    return out


def a_disparo(d, Rf=None):
    """Longitud de dispersion por disparo lineal (M1). Rf con delta Rf = 60 (q(Rf) ~ 1e-28)."""
    Rf = Rf if Rf is not None else 60.0 / d
    s = regular(lambda r: q_yuk(r, d), Rf=Rf)
    return float(Rf - s["uR"] / s["upR"])


def a_fase_variable(d, Rf=None):
    """M2: fase variable a energia cero (Calogero): da/dr = 2 V(r) (r - a)^2, a(0) = 0. Independiente de M1."""
    Rf = Rf if Rf is not None else 60.0 / d
    f = lambda r, a: [-2.0 * q_yuk(r, d) * (r - a[0]) ** 2]
    s = solve_ivp(f, [1e-12, Rf], [0.0], method="DOP853", rtol=1e-13, atol=1e-14)
    return float(s.y[0, -1])


def phi_edo(d, r, Rf=None):
    """Perfil phi(r) = u~(r)/(alpha r) (M1) normalizado a 1 en el infinito."""
    Rf = Rf if Rf is not None else 60.0 / d
    r = np.atleast_1d(np.asarray(r, float))
    s = regular(lambda x: q_yuk(x, d), Rf=Rf, r_eval=np.maximum(r, 1e-9))
    alpha = s["upR"]
    return s["u"] / (alpha * np.maximum(r, 1e-9)), alpha


def phi_nystrom(d, r_eval, n_pan=600, n_gl=8, Rf=None):
    """M3: phi(r) = 1 + int_0^inf 2 r'^2 q(r') phi(r') / max(r, r') dr' (Green radial de -1/2 Lap), Nystrom con
    Gauss-Legendre compuesto en x = sqrt(r') (concentra nodos cerca del origen). Devuelve phi(r_eval) y a."""
    Rf = Rf if Rf is not None else 60.0 / d
    xg, wg = np.polynomial.legendre.leggauss(n_gl)
    edges = np.linspace(0, np.sqrt(Rf), n_pan + 1)
    X = ((edges[:-1, None] + edges[1:, None]) / 2 + (edges[1:, None] - edges[:-1, None]) / 2 * xg).ravel()
    WX = (np.broadcast_to((edges[1:, None] - edges[:-1, None]) / 2 * wg, (n_pan, n_gl))).ravel()
    R = X ** 2
    W = WX * 2 * X                          # dr = 2 x dx
    g = 2 * R ** 2 * q_yuk(R, d) * W        # 2 r'^2 q(r') dr'
    K = g[None, :] / np.maximum(R[:, None], R[None, :])
    # Sustraccion de la singularidad (el nucleo tiene un quiebre en r' = r): phi(r') = phi(r) + [phi(r') - phi(r)],
    # con S(r) = int_0^inf 2 r'^2 q(r') / max(r, r') dr' en forma cerrada.
    S = lambda x: 2 * (1 - np.exp(-d * x) * (1 + d * x)) / (d * d * x) + 2 * np.exp(-d * x) / d
    M = -K.copy()
    M[np.diag_indices_from(M)] += 1 - S(R) + K.sum(1)
    phi_n = np.linalg.solve(M, np.ones(len(R)))
    r_eval = np.atleast_1d(np.asarray(r_eval, float))
    Ke = g[None, :] / np.maximum(r_eval[:, None], R[None, :])
    # phi en r_eval por la propia ecuacion (r_eval no es nodo; error ~1e-7 por el quiebre)
    phi_r = 1 + (Ke * phi_n[None, :]).sum(1)
    a = -float((g * phi_n).sum())
    return phi_r, a


# ------------------------------------------------------------------------------------- ley exacta de Lambda
def alpha_de_p(qfun, p, Rf, cortes=None):
    return regular(qfun, p=p, Rf=Rf, cortes=cortes)["upR"]


def polos(qfun, Rf, p_max, n_scan=400, cortes=None):
    """Ceros p_k de alpha(p) en (0, p_max): polos de E[e^{p Lambda}]. Barrido y brentq."""
    ps = np.linspace(1e-3, p_max, n_scan)
    al = np.array([alpha_de_p(qfun, p, Rf, cortes) for p in ps])
    raices = []
    for i in range(n_scan - 1):
        if np.sign(al[i]) != np.sign(al[i + 1]):
            raices.append(brentq(lambda p: alpha_de_p(qfun, p, Rf, cortes), ps[i], ps[i + 1], xtol=1e-14, rtol=1e-15))
    return raices


def pesos_mezcla(qfun, Rf, pk, r_eval, cortes=None):
    """w_k(r) = -u~_{p_k}(r) / (r alpha'(p_k) p_k) en los puntos r_eval (r_eval > 0)."""
    r_eval = np.atleast_1d(np.asarray(r_eval, float))
    s = regular(qfun, p=pk, Rf=Rf, r_eval=r_eval, con_derivada_p=True, cortes=cortes)
    dalpha = s["vpR"]
    return -s["u"] / (r_eval * dalpha * pk), float(s["upR"]), float(dalpha)


# ------------------------------------------------------------- Yukawa promediado sobre una gaussiana 3D
from scipy.special import erfc as _erfc, erfcx as _erfcx


def q_gauss(R, sig, d):
    """E[ e^{-d|X|}/|X| ] con X ~ N(m, sig^2 I_3), R = |m|. Forma cerrada (convolucion del Yukawa con la gaussiana):
    f = [e^{d^2 s^2/2 - d R} erfc((d s^2 - R)/(s sqrt2)) - e^{d^2 s^2/2 + d R} erfc((d s^2 + R)/(s sqrt2))] / (2R),
    escrita con erfcx para que no haya desbordes. Para R/s < 1e-5 se usa el valor en R = 0. Acotada por sqrt(2/pi)/s."""
    R = np.asarray(R, float)
    sig = np.asarray(sig, float) * np.ones_like(R)
    A = (d * sig ** 2 - R) / (sig * np.sqrt(2.0))
    B = (d * sig ** 2 + R) / (sig * np.sqrt(2.0))
    g = np.exp(-R ** 2 / (2 * sig ** 2))
    T1 = np.where(A <= 0, np.exp(np.minimum(d * d * sig ** 2 / 2 - d * R, 700)) * _erfc(np.minimum(A, 0)),
                  g * _erfcx(np.maximum(A, 0)))
    T2 = g * _erfcx(B)
    Rs = np.maximum(R, 1e-300)
    f = (T1 - T2) / (2 * Rs)
    f0 = np.sqrt(2 / np.pi) / sig * (1 - d * sig * np.sqrt(np.pi / 2) * _erfcx(d * sig / np.sqrt(2)))
    return np.where(R < 1e-5 * sig, f0, f)



# ------------------------------------------------------------------------------------- Monte Carlo (numba)
import math
from numba import njit

_GLT = np.array([(1 - math.sqrt(0.6)) / 2, 0.5, (1 + math.sqrt(0.6)) / 2])   # Gauss-Legendre de 3 nodos en (0, 1)
_GLW = np.array([5 / 18, 8 / 18, 5 / 18])
_SQ2 = math.sqrt(2.0)


@njit(cache=True)
def _q_gauss1(R, sig, d):
    """E[e^{-d|X|}/|X|], X ~ N(m, sig^2 I_3), R = |m| (forma cerrada; ver q_gauss)."""
    if R < 1e-5 * sig:
        x = d * sig / _SQ2
        return math.sqrt(2 / math.pi) / sig * (1 - d * sig * math.sqrt(math.pi / 2) * math.exp(x * x) * math.erfc(x))
    e = d * d * sig * sig / 2
    if R > 8.0 * sig:
        # lejos de la singularidad el Yukawa es autofuncion del laplaciano (Lap q = d^2 q): la media gaussiana es
        # exactamente q(R) e^{d^2 sig^2/2} salvo erfc(R/(sig sqrt2) - ...) < 1e-14 (mismo valor que la forma cerrada)
        return math.exp(e - d * R) / R
    A = (d * sig * sig - R) / (sig * _SQ2)
    B = (d * sig * sig + R) / (sig * _SQ2)
    T1 = math.exp(e - d * R) * math.erfc(A)
    T2 = math.exp(e + d * R) * math.erfc(B)
    return (T1 - T2) / (2 * R)


@njit(cache=True)
def _int_puente(r, z1, rho2, dt, d):
    sdt = math.sqrt(dt)
    tot = 0.0
    for j in range(3):
        t = _GLT[j]
        m = math.sqrt((r + t * sdt * z1) ** 2 + t * t * dt * rho2)
        tot += _GLW[j] * _q_gauss1(m, math.sqrt(t * (1 - t) * dt), d)
    return tot * dt


def integral_puente(r, z1, rho2, dt, d):
    """Version vectorizada (para pruebas) de la media de int q sobre el puente browniano."""
    sdt = np.sqrt(dt)
    tot = 0.0
    for t, w in zip(_GLT, _GLW):
        m = np.sqrt((r + t * sdt * z1) ** 2 + (t * t) * dt * rho2)
        tot = tot + w * q_gauss(m, np.sqrt(t * (1 - t) * dt), d)
    return tot * dt


@njit(cache=True)
def _kernel_libre(r0, d, eta, R_in, seed, metodo, max_pasos):
    np.random.seed(seed)
    N = r0.size
    Lam = np.empty(N)
    pasos = np.empty(N, dtype=np.int64)
    for i in range(N):
        r = r0[i]
        L = 0.0
        n = 0
        while True:
            dt = (eta * r) ** 2
            sdt = math.sqrt(dt)
            z = np.random.standard_normal()
            chi2 = -2.0 * math.log(1.0 - np.random.random())     # z2^2 + z3^2 (chi^2 con 2 grados)
            rn = math.sqrt((r + sdt * z) ** 2 + dt * chi2)
            if metodo == 0:
                L += _int_puente(r, z, chi2, dt, d)
            else:
                L += 0.5 * (math.exp(-d * r) / r + math.exp(-d * rn) / rn) * dt
            n += 1
            if rn > R_in:
                if np.random.random() < R_in / rn:
                    rn = R_in
                else:
                    break
            r = rn
            if n >= max_pasos:
                L = -1.0      # marca de camino truncado
                break
        Lam[i] = L
        pasos[i] = n
    return Lam, pasos


def simular_libre(r0, d, eta, R_in, seed, metodo="puente", max_pasos=200_000_000, devolver_pasos=False):
    """Lambda = int_0^inf q(B_t) dt para caminos que parten de los radios r0. Bessel-3 exacto con dt = eta^2 r^2.
      metodo = "puente":   media EXACTA de int q sobre el puente browniano entre los extremos;
      metodo = "trapecio": dt (q(r) + q(r'))/2. NO SIRVE: q(r') dt ~ eta^2 r^2 / r' y r' puede caer muy cerca del
                           origen; como la densidad de r' cerca de 0 va como r'^2, E[exp(c/r')] = infinito y la media
                           del estimador discretizado es infinita para todo eta > 0 (se documenta en 03).
    Cierre: si r > R_in, vuelve a R_in con probabilidad R_in/r (exacto para BM 3D) o termina."""
    L, p = _kernel_libre(np.ascontiguousarray(r0, dtype=np.float64), float(d), float(eta), float(R_in), int(seed),
                         0 if metodo == "puente" else 1, int(max_pasos))
    if (L < 0).any():
        raise RuntimeError(f"{int((L < 0).sum())} caminos truncados")
    return (L, p) if devolver_pasos else L


# ------------------------------------------------------------------------- muestreo por importancia (MI)
class Guia:
    """phi_T = solucion de energia cero normalizada del Yukawa con delta_T (delta_c < delta_T), tabulada en [0, R_in] en
    una rejilla uniforme (h = R_in/n_tab); fuera, phi_T = 1 + A/r con A = -a_T. Deriva b(r) = phi_T'/phi_T; energia
    local E_L = (H phi_T)/phi_T = q_T - q >= 0 para el Yukawa objetivo con delta > delta_T."""

    def __init__(self, d, dT, R_in, n_tab=400000):
        self.d, self.dT, self.R_in = d, dT, R_in
        Rf = max(60.0 / dT, R_in)
        self.h = R_in / n_tab
        self.rt = np.linspace(0, R_in, n_tab + 1)
        s = regular(lambda x: q_yuk(x, dT), Rf=Rf, r_eval=np.maximum(self.rt, 1e-9))
        alpha = s["upR"]
        self.aT = float(Rf - s["uR"] / s["upR"])
        self.A = -self.aT
        rr = np.maximum(self.rt, 1e-9)
        self.phiT_tab = s["u"] / (alpha * rr)
        self.b_tab = s["up"] / s["u"] - 1.0 / rr      # (u/r)'/(u/r)
        self.b_tab[0] = self.b_tab[1]                 # limite r -> 0 (cancelacion numerica en 1e-9)
        self.b1_tab = s["up"] / s["u"]                # u_T'/u_T: deriva del proceso RADIAL guiado (1/r + b)
        self.b1_tab[0] = self.b1_tab[1]
        self.rc = 1.0 / dT                            # cambio de imagen: 3D para r < rc, radial 1D para r >= rc
        self.alpha = alpha

    def phiT(self, r):
        r = np.asarray(r, float)
        return np.where(r <= self.R_in, np.interp(r, self.rt, self.phiT_tab), 1 + self.A / np.maximum(r, 1e-300))


@njit(cache=True)
def _EL(r, d, dT):
    if r < 1e-12:
        return d - dT
    return math.exp(-dT * r) * (-math.expm1(-(d - dT) * r)) / r


@njit(cache=True)
def _kernel_guiado(r0, d, dT, R_in, A, h, btab, b1tab, rc, eta, seed, max_pasos):
    """Paso hibrido. Para r < rc (cerca del origen): imagen 3D, la parte de Bessel-3 es exacta (norma del gaussiano 3D)
    y la deriva acotada grad ln phi_T va por Euler. Para r >= rc: imagen radial 1D, Euler con la deriva total
    u_T'/u_T = 1/r + phi_T'/phi_T, que es pequena (~ 1/(r + A)) donde las dos derivas grandes (+1/r de Bessel y
    ~ -1/r de la guia) se cancelan; asi el error de Euler no se aplica a cada una por separado."""
    np.random.seed(seed)
    N = r0.size
    Lout = np.empty(N)
    pasos = np.empty(N, dtype=np.int64)
    nt = btab.size - 1
    for i in range(N):
        r = r0[i]
        L = 0.0
        n = 0
        er = _EL(r, d, dT)
        while True:
            dt = (eta * r) ** 2
            sdt = math.sqrt(dt)
            x = r / h
            k = int(x)
            z = np.random.standard_normal()
            if r < rc:
                f = x - k
                b = btab[k] * (1 - f) + btab[k + 1] * f
                chi2 = -2.0 * math.log(1.0 - np.random.random())
                rn = math.sqrt((r + b * dt + sdt * z) ** 2 + dt * chi2)
            else:
                if k >= nt:
                    b1 = 1.0 / (r + A)
                else:
                    f = x - k
                    b1 = b1tab[k] * (1 - f) + b1tab[k + 1] * f
                rn = r + b1 * dt + sdt * z
                if rn < 0.0:
                    rn = -rn
            en = _EL(rn, d, dT)
            L += 0.5 * (er + en) * dt        # E_L acotada (<= delta - delta_T): el trapecio no tiene problema aqui
            n += 1
            if rn > R_in:
                if np.random.random() < (R_in + A) / (rn + A):
                    rn = R_in
                    en = _EL(rn, d, dT)
                else:
                    break
            r = rn
            er = en
            if n >= max_pasos:
                L = np.nan     # marca de camino truncado (L puede ser negativo si E_L < 0)
                break
        Lout[i] = L
        pasos[i] = n
    return Lout, pasos


def simular_guiado(r0, guia, eta, seed, max_pasos=2_000_000_000, devolver_pasos=False):
    """Difusion guiada a energia cero: dX = grad ln phi_T dt + dB (paso hibrido, ver _kernel_guiado), dt = eta^2 r^2,
    log-peso -int E_L (trapecio). Devuelve Lg = int E_L dt (>= 0); el estimador es phi_T(r0) exp(-Lg) <= phi_T(r0)."""
    L, p = _kernel_guiado(np.ascontiguousarray(r0, dtype=np.float64), float(guia.d), float(guia.dT), float(guia.R_in),
                          float(guia.A), float(guia.h), guia.b_tab, guia.b1_tab, float(guia.rc), float(eta), int(seed),
                          int(max_pasos))
    if np.isnan(L).any():
        raise RuntimeError(f"{int(np.isnan(L).sum())} caminos guiados truncados")
    return (L, p) if devolver_pasos else L


def dT_para_razon(d, razon=1.25):
    """delta_T con a_T = razon * a (regla fijada antes: 1/a_T = 0.8/a)."""
    a = a_disparo(d)
    return brentq(lambda x: a_disparo(x) - razon * a, DELTA_C + 1e-7, d - 1e-9, xtol=1e-13)

```
