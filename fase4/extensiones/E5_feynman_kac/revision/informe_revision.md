# Revisión adversarial independiente de E5 (17-11-2026)

*Revisor: Claude (IA), agente R5, distinto del agente que escribió E5. Todo el código de esta carpeta (`r1` a `r5`) está
escrito desde cero y no importa `fk_comun.py`. Las cifras salen de `r*_*.json` y `r*_salida.txt`. Un proceso, ningún
run por encima de 6 minutos.*

## Veredicto

La matemática central es correcta. El Teorema 1 (E[W^p] < ∞ si y solo si p < δ/δ_c, igualdad incluida), la Proposición 3
(trapecio con media infinita), la forma cerrada de la media gaussiana del Yukawa, la dominación por Jensen del esquema de
puente, la Proposición 4 (pesos en (0, 1] y varianza relativa ≤ φ_T/φ − 1), la ley de mezcla (con el paso abierto que el
propio texto declara) y el umbral 4/e del ansatz resisten la revisión. Los números se reproducen con métodos distintos.
Encontré un hueco técnico menor en la prueba (x = 0), dos afirmaciones que el texto daba como más firmes de lo que
estaban (orden η⁴ del sesgo, ventaja de costo frente a PIGS), un resultado omitido en `verificacion.md` y criterios
algo laxos. No hay errores graves. Las correcciones se hicieron en el texto de E5; las copias previas están en
`revision/*_antes_revision.md`.

## Tabla de hallazgos

| ID | Gravedad | Descripción | Evidencia | Corrección |
|---|---|---|---|---|
| R5-01 | Menor (hueco de prueba) | En la prueba del Teorema 1, g_x = q^{1/2}G_0(x, ·) no está en L² para x = 0: ‖g_0‖² = π^{−1}∫e^{−δr}/r dr = ∞. El teorema se enuncia para todo x ∈ ℝ³. | Cálculo directo | Nota en `teoria.md` §3: para n ≥ 2 se usa h_0 = K g_0 = q^{1/2}(G_0 q G_0(0, ·)) ∈ L² (crece como log(1/\|y\|)). El resultado no cambia. |
| R5-02 | Informativo (confirmado) | La causa atribuida a C16 (η = 0.8): la cuadratura de 3 nodos en el tiempo del puente. | Simulador propio (r3): η = 0.8 con 3 nodos da E[δΛ] = 0.98939 ± 0.00094 (−11.4σ); con 12 nodos, 0.99978 ± 0.00094 (−0.23σ). Con η = 0.4 da igual con 3 y con 12 nodos (+0.66σ y +0.65σ). | Ninguna: la causa es correcta. |
| R5-03 | Moderada (sobreafirmación) | "Sesgo de orden η⁴" se presentaba como medido. (a) El par 0.8/0.4 de 02 está contaminado por el error de cuadratura de R5-02. (b) Los órdenes 0.4/0.2 (4.58, 3.97, 3.40) tienen incertidumbre de ±2.4, ±1.4 y ±1.1, porque el sesgo en η = 0.2 es 0.6σ, 1.0σ y 1.3σ. (c) Los tres δ comparten una muestra. C8b "pasa" con valores casi sin información. | Propagación de errores sobre `02_validacion_mc.json`. Con 12 nodos (r4, N = 10⁶) el orden 0.8/0.4 sin cuadratura es 3.38 ± 0.30 (δ = 3) y 3.60 ± 0.41 (δ = 4). Extrapolar 02 con p = 2 da −2.9σ, −2.9σ y −2.1σ de la EDO: los datos sí excluyen p = 2. | `teoria.md` §6.3, `seccion_articulo.md` y `LEEME.md` ahora dicen "argumento heurístico; los datos excluyen el orden 2 y no fijan el 4". C8b no se reevalúa, porque el criterio se fijó antes. |
| R5-04 | Moderada (argumento) | Comparación de costo: "1/(δ − δ_c) frente a (δ_c − δ)^{−2} de PIGS o de la transferencia". El tiempo físico de la difusión guiada hasta r ∼ A crece como A² ∝ (δ − δ_c)^{−2}, la misma escala que τ ∝ 1/\|E_0\|. La ganancia a ∝ A pasos viene del paso adaptativo dt = η²r², no de trabajar a energía cero. Además la transferencia de la Fase 3 no proyecta con τ: diagonaliza, y su costo crece con la caja R ∼ 1/κ. | Estimación de Green 1D: pasos ≈ ∫ 2(A − r)/(η²r²) dr ∝ A/η², tiempo ≈ A². La medida (pendiente 0.982) confirma pasos ∝ \|a_T\|. | Texto corregido en `teoria.md` §7, `seccion_articulo.md` (se quitó "análogo exacto" y "con la ventaja de") y `LEEME.md` §8. |
| R5-05 | Menor | δ = 1.1907: a = −15889.8 ± 349.8 (estadística) frente a −15404.49. Eso es −1.39σ estadístico y −1.15σ con σ = estadística + sesgo (72.0, sumado linealmente). Si el sesgo de η = 0.2 (+0.47 %, que acerca a a cero) se resta con su signo, queda −1.59σ. Es compatible, pero "−1.15σ" es la versión más favorable. | Cálculo sobre `05_cerca_umbral.json`. Numerov propio: a(1.1907) = −15404.49 (r1). | Se informa aquí. No cambia la conclusión (el MI funciona al 2.3 %). |
| R5-06 | Moderada (omisión) | `verificacion.md` §2.4 citaba la guía subsolución δ_T = 1.8 con η = 0.2 (+3.9 %) y η = 0.1 (+0.70 %), pero omitía η = 0.05: +1.32 % (2.4σ), θ = 2.28 ± 0.11. La secuencia no converge de forma monótona. Con θ ≈ 2.3–2.5 el cuarto momento es infinito y el error estándar no es fiable. La explicación ("criticidad efectiva del esquema discreto") no está medida. | `08_verificacion_salida.txt` (f) | Se añadió el valor de η = 0.05 y la advertencia en `verificacion.md`. |
| R5-07 | Menor (criterio laxo, declarado) | C13 usa σ = estadística + \|sesgo estimado\| sin restar el sesgo, lo que infla σ. Con la regla de 04, el extrapolado de δ = 3 queda a +3.85σ y C13 "pasa" igual. Los extrapolados con p = 2 (04b) quedan en 5 de 6 casos del mismo lado (+1.39, +1.78, +1.32, +0.81, −0.19, +0.66σ), lo que sugiere un sesgo residual de la extrapolación del orden de 10⁻³ relativo. | `04b_extrapolacion_salida.txt` | La revisión a p = 2 está declarada como posterior a ver los datos y es razonable (Euler débil O(dt), par más fino 1.93). Se deja constancia aquí; no se cambian los criterios. |
| R5-08 | Menor (coherencia) | C3: el criterio previo dice "r ≤ 10" y la tabla dice "r ≤ 8". La rejilla llega a 8, así que no hay efecto. La causa del fallo (criterio absoluto con φ ≈ 250 en δ = 1.2) es correcta: el error relativo es 1.0e-6 y baja con los paneles. | `01`, `08` (a) | Ninguna, salvo esta nota. |
| R5-09 | Informativo | C11: la causa (estadístico preasintótico y ruidoso) está medida con muestras de la ley exacta, pero el MC queda en z ≈ +2 en los cinco δ (1.97, 2.06, 2.12, 2.20, 1.83). Las cinco cifras no son independientes (una sola muestra universal), así que equivalen a una fluctuación de 2σ y no a cinco. | `03_colas_salida.txt` (6) | Ninguna. |
| R5-10 | Menor (sobreafirmación) | Proposición 4: "acotada uniformemente cuando δ → δ_c⁺" es un límite argumentado, no demostrado. | Los valores se estabilizan en 0.546, 0.552, 0.555, 0.556 | Se añadió el argumento (φ ≈ \|a\|χ, φ_T ≈ 1.25\|a\|χ) y se pasó a la lista de "argumento" de §10. |
| R5-11 | Informativo | El ansatz en δ = 1.3, c = 1.25 da α = −1.8e-3 sin nodos hasta Rf = 46: es un caso límite. | r5: con Rf = 2000 aparece el nodo (α = −1.7705e-3 estable). c = 2 sigue con varianza finita. | Ninguna: la clasificación de E5 es correcta. |
| R5-12 | Informativo | El estimador de colisiones de la serie de Neumann (sin caminos, r2) está acotado por 1/(1 − 2/δ) para δ > 2. Ese otro estimador "libre" tiene varianza finita en 2 < δ ≤ 2δ_c, donde W no la tiene. El Teorema 1 habla del peso W de caminos, y así se enuncia, pero "el MC libre no sirve" vale para el estimador de caminos. | r2 | Sugerencia para el artículo, no aplicada. |
| R5-13 | Menor (fuentes) | Las páginas de Ciesielski–Taylor (434–450) estaban "no verificadas". El DOI de Chen 2002 faltaba. Birman–Schwinger, HLS y Jentzsch estaban como [no verificada]. | Página de la AMS; portal de BIT; arXiv:1111.6788; arXiv:1508.02041; EuDML | `fuentes.md` filas 6, 10 y 13a–c; páginas en `teoria.md` y `seccion_articulo.md`. |

## Lo verificado de forma independiente

**Matemática (teoria.md), paso a paso.**
- **Fórmula de Kac.** Comprobada en el informe técnico de Berkeley n.º 427 de Fitzsimmons y Pitman: E_μ[A_v^n] = n!(G M_v)^n 1, con v ≥ 0 y T un tiempo de muerte markoviano. Con T = ∞ se usa G_0(x, y) = 1/(2π\|x − y\|), el Green de ½Δ en ℝ³ (correcto: es el doble del de Δ).
- **Rollnik.** La norma de Hilbert–Schmidt es ∬ qq/(4π²\|x − y\|²). HLS con n = 3, λ = 2 y p = r = 3/2 cumple 1/p + 1/r + λ/n = 2, y q ∈ L^{3/2} porque ∫ r^{−3/2} r² dr converge en 0.
- **Jentzsch.** El núcleo q^{1/2}G_0q^{1/2} es estrictamente positivo y K es compacto y positivo, así que κ_1 es simple y e_1 > 0.
- **Cotas.** La cota inferior vale por Cauchy–Schwarz en el complemento de e_1. Los términos cumplen ≥ (c_1/κ_1)(pκ_1)^n(1 + o(1)), así que la serie diverge si pκ_1 ≥ 1: **la igualdad está bien incluida**.
- **Identificación 1/κ_1 = p_1.** e_1 es radial (κ_1 es simple y K conmuta con las rotaciones). Entonces ψ = G_0q^{1/2}e_1 > 0 da una solución radial con α(1/κ_1) = 0, así que 1/κ_1 ≥ p_1. Al revés, la solución en p_1 da un autovalor 1/p_1 ≤ κ_1. Por tanto 1/κ_1 = p_1.
- **Escala.** Con r = s/p se obtiene −½Δ_r − p e^{−δr}/r = p²[−½Δ_s − e^{−(δ/p)s}/s]: multiplicar V por p equivale a cambiar δ por δ/p. Coincide con δ = μħ²/(mg), porque pV equivale a g' = pg y δ' = δ/p.
- **Proposición 3 (trapecio).** Es cierta para todo η > 0. dt se fija con el punto de partida, la densidad de r' cerca de 0 es ∼ r'², el factor e^{dt·q(r')/2} ≥ e^{C/r'} y ∫r'²e^{C/r'} dr' = ∞. Lo comprobé en el código: el trapecio usa dt = (ηr)² del punto inicial.
- **Media sobre el puente.** La cantidad exacta es E[∫_0^{dt} q(X_s) ds \| x, y] = dt∫_0^1 E[q(N(x + t(y − x), t(1 − t)dt·I))] dt. Rederivé la forma cerrada completando cuadrados: coincide. El sesgo es exactamente E[W_disc(∏e^{g_k} − 1)], con g_k la brecha de Jensen por paso, y la estimación heurística da O(η⁴) (ver R5-03).
- **E[δΛ] = 1 con partida Γ.** Lo rehice a mano: E_Γ[Φ] = 1/(2δ) y G_0q = 2Φ.
- **Proposición 4.** E[Y²] ≤ φ_T E[Y]. Para la partida Γ, E[Y²] ≤ E_Γ[φ_Tφ]. Es correcta.
- **Cambio de medida.** M_t = φ_T(B_t)e^{∫q_T} es una martingala local positiva con E[M_∞] = φ_T(x) = M_0 (Teorema 1 con δ_T > δ_c), así que es uniformemente integrable y (2) vale. Las fórmulas E^T[Y^p] = φ_T^{p−1}E[e^{∫((1−p)q_T + pq)}] y E_L = q_T − q también son correctas.
- **Ansatz y cierre.** E_L del ansatz y el umbral 4/e: correctos (también con b > 2/δ, cuando el mínimo está en r = 0). La cúspide b² + Ab = A es correcta. El cierre guiado (R_in + A)/(r + A) es la función armónica correcta de la transformada h.
- **Código del MI.** La deriva es b = (u/r)'/(u/r) en 3D y u'/u en radial, que es correcto. El peso es exp(−∫(q_T − q)) con el signo correcto. _EL coincide con (e^{−δ_T r} − e^{−δr})/r.

**Recálculo independiente.**

| Cantidad | E5 | Revisión (método propio) | Diferencia |
|---|---|---|---|
| a(1.2) | −142.9348653 | −142.9348642 (Numerov + Richardson h⁴, r1) | 7.7e-9 relativo |
| a(1.5), a(2), a(3), a(4) | −3.66823368, −1.10345919, −0.34324097, −0.16901737 | −3.66823369, −1.10345918, −0.34324097, −0.16901737 | ≤ 4e-9 |
| a(1.195), a(1.192), a(1.1907) | −306.7134, −971.5385, −15404.50 | −306.7143, −971.5389, −15404.49 | ≤ 3e-6 |
| δ_c (cero de α) | 1.1906124210606 | 1.190612420990 | 6e-11 |
| w̄_1 | 0.80317 | 0.80317 | — |
| a(3), MC | −0.343302 ± 0.000086 (puente, extrapolado) | −0.343180 ± 0.000039 (colisiones, sin discretización, r2) | +1.56σ frente a la EDO |
| a(4), MC | −0.169020 ± 0.000023 | −0.169041 ± 0.000013 | −1.85σ frente a la EDO |
| a(2.5), MC | — | −0.559966 ± 0.000081 | +0.52σ |
| φ(r), δ = 2.5, 3 y 4 (12 puntos) | δ = 3 y 4: todos ≤ 1.37σ | todos ≤ 1.68σ (r2) | — |
| θ(δ = 2) | 1.6832 ± 0.0053 | Hill, 1 % superior: 1.6910 ± 0.0138 (r3, N = 1.5e6, η = 0.25, semilla propia) | pred. 1.6798: +0.81σ |
| θ(δ = 3) | 2.5248 ± 0.0080 | Hill: 2.5304 ± 0.0207 | pred. 2.5197: +0.52σ |
| δ_c desde la cola | 1.18821 ± 0.00376 | 1/0.84160 = 1.18821 y 0.00266/0.84160² = 0.00376 (aritmética comprobada). Hill propio: 1.1827 ± 0.0097 (δ = 2) y 1.1856 ± 0.0097 (δ = 3) | compatibles |

Sobre el sesgo de la MLE de la cola: con u = 5.227, la fracción del segundo polo por encima del umbral es
w̄_2e^{−u/δ_c(2s)}/(w̄_1e^{−u/δ_c}) ≈ 6e-7, despreciable. La sensibilidad al umbral (0.838 a 0.842) cabe en 1σ.

**Muestreo por importancia, δ = 1.1907.** Ver R5-05: −1.39σ estadístico, −1.15σ con el sesgo sumado y −1.59σ con el
sesgo restado con su signo. Con N = 621 y la varianza relativa acotada (0.30), el error estándar es fiable.

**Controles.** C3, C11 y C16 no pasan por las causas que E5 dice; C16 lo confirmé con 12 nodos (R5-02). La extrapolación
con p = 2 está declarada como posterior a ver los datos y es razonable (R5-07). Los criterios laxos son C8b (R5-03) y la
σ lineal de C13 (R5-07).

**Fuentes** (WebSearch/WebFetch, 17-11-2026).
- **Zhao 1992:** AMS, *Trans. AMS* 334, 75–96. El resumen dice lo atribuido.
- **Chen 2002:** *Trans. AMS* 354 (11), 4639–4679, DOI 10.1090/S0002-9947-02-03059-3. El resumen dice "gaugeability, conditional gaugeability and subcriticality are equivalent" para procesos transitorios con dual fuerte, como se atribuye.
- **Fitzsimmons–Pitman:** RePEc, SPA 79 (1), 117–134, 1999, y el informe de Berkeley n.º 427 con la fórmula y v ≥ 0.
- **Ciesielski–Taylor:** AMS, 103, 434–450 (1962). El texto no se abrió. La fórmula 1/cos√(2p) es correcta por la equivalencia clásica con el tiempo de salida de (−1, 1) en 1D, E e^{−λτ} = 1/cosh√(2λ).
- **Birman–Schwinger:** solo fuente secundaria (Gridnev, arXiv:1111.6788, §4, con cita a Klaus–Simon).
- **HLS:** Ngô–Nguyen, arXiv:1508.02041.
- **Jentzsch:** datos en EuDML (*J. reine angew. Math.* 141, 235–244, 1912); el texto no se abrió.

## Archivos de la revisión
- `r1_numerov.py/.json`: a(δ), δ_c y w̄_1 por Numerov.
- `r2_colisiones.py/.json`: MC sin caminos (serie de Neumann).
- `r3_caminos.py`, `r3_caminos_lib.py`, `r3_caminos.json`, `r3_salida.txt`: simulador propio, C16 y Hill.
- `r4_orden_sesgo.py/.json`, `r4_salida.txt`: orden del sesgo con 12 nodos.
- `r5_ansatz.py/.json`: sensibilidad del ansatz a Rf.
- `*_antes_revision.md`: copias de los textos antes de las correcciones.
