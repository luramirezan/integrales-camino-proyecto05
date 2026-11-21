# Material para auditoría (parte 1 de 3)

Responde solo "Recibido" hasta la parte 3, que trae el encargo.

## Contexto

Proyecto de física teórica (curso universitario de integrales de camino). Potencial de Yukawa V(r) = −e^{−δr}/r en unidades ħ = m = g = 1, δ = μħ²/(mg); el estado 1s deja de existir en δ_c = 1.1906124210606.

## seccion_articulo.md

# Un criterio de umbral sin caja: caminos brownianos a energía cero

## Motivación

Los métodos de las Fases 2 y 3 (radial, transferencia y PIGS) proyectan el fundamental con e^{−τH} dentro de una caja.
Cerca del umbral ambos recursos se disparan: el estado ocupa R ∼ 1/κ y el tiempo de proyección necesario crece como
1/|E_0| ∝ (δ_c − δ)^{−2}; en δ = 1.19, |E_0| ≈ 10⁻⁷. Los Monte Carlo de línea de mundo del Yukawa [Edwards et al.,
arXiv:1903.00536] sufren además el "undersampling": los lazos crecen como √t y dejan de muestrear el potencial. Aquí
proponemos trabajar **a energía cero y del lado no ligado**, donde la representación de Feynman–Kac no necesita ni caja
ni tiempo de proyección, y estudiamos qué tan bien funciona.

## Método

Con ħ = m = g = 1, generador ½Δ y q = −V = e^{−δr}/r, para δ > δ_c la solución de −½Δφ + Vφ = 0 con φ → 1 es

  φ(x) = E_x[W],  W = exp(∫_0^∞ q(B_t) dt),  φ(r) = 1 − a/r fuera del potencial,

con a < 0 sin ligado (convención del grupo). Como a = 2∫ r²Vφ dr y r²V = −r e^{−δr}, la longitud de dispersión es una
media de pesos: **a = −(2/δ²) E[W]** si el camino parte de r_0 ∼ Γ(2, 1/δ). El movimiento browniano en ℝ³ es
transitorio: el camino se va al infinito y el cálculo termina solo. Para no simular la cola del camino usamos un cierre
exacto: fuera de R_in = 36/δ el potencial es < 10⁻¹⁶, y un camino que sale vuelve a la esfera R_in con probabilidad R_in/r
(si vuelve, se reinicia allí; si no, termina).

**Discretización.** El paso es dt = η²r² y la transición del radio es exacta (norma de un gaussiano 3D). La integral de q
en cada paso **no** puede hacerse con el trapecio: el extremo del paso cae cerca del origen con densidad ∼ r'², el factor
e^{η²r²/2r'} no es integrable y la media del estimador discretizado es infinita para todo η (en la práctica obtuvimos
a(3) ≈ −2.4×10^{145}). Usamos en su lugar la media exacta de ∫q sobre el puente browniano 3D entre los extremos, que
tiene forma cerrada para el Yukawa. Por la desigualdad de Jensen condicional, el estimador resultante está dominado por el
exacto en todos sus momentos; su sesgo es negativo y de orden η⁴ (órdenes medidos entre 3.25 y 4.58).

## Resultado 1: la varianza es infinita en δ_c < δ ≤ 2δ_c

Por la fórmula de momentos de Kac [Fitzsimmons y Pitman 1999], E[Λ^n] = n!((G_0q)^n 1)(x). Escribiendo la serie con el
operador compacto y positivo K = q^{1/2}G_0q^{1/2}, cuyo mayor autovalor es κ_1 = δ_c/δ (principio de Birman–Schwinger,
comprobado directamente), se obtiene:

> **E[W^p] es finito si y solo si p < δ/δ_c.** En particular la media existe para todo δ > δ_c, pero la **varianza es
> infinita para δ_c < δ ≤ 2δ_c ≈ 2.381**, igualdad incluida.

La prueba completa está en `teoria.md`. Es un caso particular, con prueba elemental, de la equivalencia entre
gaugeabilidad y subcriticalidad de Zhao [Trans. AMS 334 (1992)], de quien solo verificamos el resumen.

Hay más: la ley de Λ es una mezcla de exponenciales con tasas p_k = δ/δ_c(ks), las constantes críticas de **todos** los
estados s (1s, 2s, 3s, …). Por eso la cola del peso es una ley de potencias casi pura, P(W > w) ≈ w̄_1 w^{−θ} con
**θ = δ/δ_c** y corrección w^{−2.84θ}. El mismo código reproduce el caso exacto del tiempo de estancia en una bola
(φ(0) = 1/cos√(2p), al estilo de Ciesielski y Taylor) con error 10⁻¹¹.

**Comprobación numérica.** Con una muestra de 10⁷ caminos (η = 0.2), la tasa de la cola de X = δΛ es
κ̂ = 0.84160 ± 0.00266 frente a 1/δ_c = 0.83990; es decir, la cola del Monte Carlo da δ_c = 1.18821 ± 0.00376. Como la
ley de X no depende de δ (covarianza de escala), θ̂ = δκ̂: 1.2624 ± 0.0040 en δ = 1.5 frente a 1.2599, y 1.6832 ± 0.0053
en δ = 2 frente a 1.6798 (figuras e5_03 y e5_04). La ley completa pasa Kolmogorov–Smirnov (√N·D = 1.11). La
consecuencia práctica se ve en la figura e5_05: en δ = 1.5 un solo camino multiplica la media acumulada por 3.7 cerca de
n = 10⁶, y la varianza muestral crece sin parar. Cerca del umbral (δ = 1.2, θ = 1.008) el error de la media bajaría como
n^{−0.008}: el Monte Carlo libre no sirve, aunque la media exista.

Donde la varianza es finita el método funciona: en δ = 3 y 4, extrapolando en η, a = −0.343302 ± 0.000086 y
−0.169020 ± 0.000023 frente a −0.343241 y −0.169017 de la EDO (figuras e5_01 y e5_02).

## Resultado 2: el remedio, una difusión guiada a energía cero

Con una función de prueba φ_T > 0, φ_T → 1, la transformada h de Doob da

  φ(x) = φ_T(x) E^T_x[exp(−∫_0^∞ E_L(X_t) dt)],  dX = ∇ln φ_T dt + dB,  E_L = Hφ_T/φ_T.

Si φ_T es **supersolución** (E_L ≥ 0), el peso está en (0, 1] y la varianza relativa queda acotada por φ_T/φ − 1. Como
guía usamos la solución de energía cero de un Yukawa ligeramente más atractivo, δ_c < δ_T < δ (regla fijada antes:
a_T = 1.25a), para el que E_L = q_T − q ≥ 0. Resultados (figuras e5_02 y e5_06):

| δ | a (EDO) | a (importancia) | varianza relativa (cota) |
|---|---|---|---|
| 1.5 | −3.6682 | −3.6629 ± 0.0041 (η → 0) | 0.151 (0.333) |
| 1.3 | −11.580 | −11.560 ± 0.025 (η → 0) | 0.228 (0.454) |
| 1.2 | −142.93 | −142.1 ± 1.2 (η → 0) | 0.296 (0.546) |
| 1.195 | −306.71 | −306.0 ± 2.4 (η = 0.2, con sesgo) | 0.296 (0.551) |
| 1.192 | −971.5 | −975 ± 9 (η = 0.2, con sesgo) | 0.293 (0.555) |
| 1.1907 | −15404.5 | −15890 ± 420 (η = 0.2, con sesgo) | 0.301 (0.556) |

La varianza relativa no crece al acercarse al umbral. Lo que crece es el costo: la guía hace que el camino se comporte
como un browniano 1D hasta r ∼ |a_T|, y el número de pasos por camino crece como |a_T|^{0.98}, es decir como
1/(δ − δ_c). Es el análogo exacto, a energía cero, del tiempo de proyección de PIGS; con la ventaja de que crece como
(δ − δ_c)^{−1} en lugar de (δ_c − δ)^{−2}. Para δ = 1.1907 (a ≈ −1.5×10⁴), 621 caminos de 2.2×10⁶ pasos dan a con 2.3 %
de error en 100 s.

Una guía que **no** es supersolución (δ_T > δ, pesos > 1) solo da varianza finita si −½Δ − (2q_δ − q_{δT}) es subcrítico
(mapa de la figura e5_07). En δ = 1.5, δ_T = 3 cae fuera de esa región: el exponente de la cola del peso es 1.37
(predicho 1.47) y un solo peso de 3×10⁵ desvía a en 27 %. El ansatz sencillo 1 + A/(r + b) solo puede ser supersolución si
δ ≥ 4/e ≈ 1.47, y con la cúspide de Kato da varianza infinita en δ = 1.3 salvo que A ≥ 2|a|.

## Discusión

1. El método responde la pregunta de la guía por otro camino: "¿hay ligado?" equivale a "¿es finita la gauge?", y la
   cercanía al umbral se lee en |a| ∝ 1/(δ − δ_c) sin caja. La pendiente de 1/a en δ_c, 0.7413, es la misma que la de κ
   en el lado ligado (Fase 3: 0.741): 1/a pasa de forma analítica por el umbral.
2. Sobre el peso que pide la guía: en todas las variantes es real y positivo. El del Monte Carlo libre tiene media finita
   pero **varianza no normalizable** en δ_c < δ ≤ 2δ_c; el del trapecio ni siquiera tiene media finita; el de la
   difusión guiada con supersolución está acotado.
3. Limitaciones: la ley de mezcla usa una convergencia (Σ|w_k| < ∞) que no demostramos; la difusión guiada usa Euler
   (sesgo ≈ 0.5 % con η = 0.2, que se extrapola o se suma al error); el criterio general para guías con E_L de signo
   variable se apoya en Zhao 1992, del que leímos solo el resumen.

## Referencias

- P. J. Fitzsimmons y J. Pitman, *Stoch. Proc. Appl.* 79, 117–134 (1999). [V]
- K. L. Chung, *Séminaire de probabilités* XIX, 496–503 (1985). [V]
- K. L. Chung y Z. Zhao, *From Brownian Motion to Schrödinger's Equation*, Grundlehren 312, Springer (1995),
  DOI 10.1007/978-3-642-57856-4 [V]; reseña de M. Cranston, *Bull. AMS* 39, 109–111 (2002). [V]
- Z. Zhao, *Trans. AMS* 334, 75–96 (1992) [V, resumen]; Z.-Q. Chen, *Trans. AMS* 354, 4639–4679 (2002). [V, resumen]
- M. Kac y J. M. Luttinger, *Ann. Inst. Fourier* 25 (3-4), 317–321 (1975) [V]; P. He, *Proc. AMS* 139, 1871–1877
  (2011). [V]
- Z. Ciesielski y S. J. Taylor, *Trans. AMS* 103 (1962), DOI 10.1090/S0002-9947-1962-0143257-8. [V, sin páginas]
- J. P. Edwards, U. Gerber, C. Schubert, M. A. Trejo, T. Tsiftsi y A. Weber, arXiv:1903.00536. [V-arXiv]


## teoria.md

# Teoría de la extensión E5: gauge de Feynman–Kac, longitud de dispersión y colas del peso

*Proyecto 05 · Fase 4, extensión E5 · 17-11-2026 · redactado por Claude (IA). Las cifras salen de
`resultados/01_referencia_edo.json` (EDO y ley exacta), `02_validacion_mc.json`, `03_colas.json` y
`04_importancia.json`.*

En este documento se separa con cuidado lo que está **demostrado** (con la prueba o con una fuente verificada), lo que está
**derivado aquí con un paso no demostrado** (se dice cuál) y lo que es **conjetura o argumento físico**. Las fuentes
llevan la marca de `fuentes.md`.

## 1. Marco y convenciones

Unidades ħ = m = g = 1. El generador del movimiento browniano B_t en ℝ³ es ½Δ. El potencial es
V(r) = −e^{−δr}/r y escribimos q = −V = e^{−δr}/r ≥ 0. Definimos el funcional y el peso

  Λ = ∫_0^∞ q(B_t) dt,  W = e^{Λ} ≥ 1,  φ(x) = E_x[W].

En radial, con u = rφ, la ecuación de energía cero −½Δφ + Vφ = 0 es u'' = −2qu, u(0) = 0. Si ũ es la solución regular
(ũ'(0) = 1), lejos del potencial ũ = α(r − a), y la solución normalizada a 1 en el infinito es φ(r) = ũ(r)/(αr), con
φ(r) = 1 − a/r fuera del potencial. Integrando r·u'' entre 0 e ∞ se obtiene a = 2∫_0^∞ r² V φ dr. La convención del
grupo es a > 0 con ligado; sin ligado, a < 0 y φ > 1. Referencia de la Fase 3: δ_c = 1.1906124210606.

Un cambio de escala que se usa en todo el trabajo: el operador −½Δ − p e^{−δr}/r, con la dilatación r → r/p, es
unitariamente equivalente a p²[−½Δ − e^{−(δ/p) r}/r]. Por eso **multiplicar el potencial por p equivale a cambiar δ por
δ/p**. El potencial pV tiene un estado de energía cero (el primer ligado s aparece) cuando δ/p = δ_c, es decir en
p_1 = δ/δ_c.

## 2. Lo que dice la literatura (verificado) y lo que no

- **Teorema de la gauge (dominio acotado).** Chung (*Sém. Probab.* XIX, 1985, 496–503) [V]: para un dominio D de medida
  finita, sin hipótesis sobre ∂D, y q acotada, la gauge u(x) = E_x[exp ∫_0^{τ_D} q(B_s) ds] es o bien idénticamente
  infinita en D o bien acotada en D. El artículo atribuye a Zhao la extensión a q en la clase de Kato K_d para dominios
  acotados (leímos el PDF de Numdam por OCR; el símbolo "m(D) < ∞" está ilegible y lo reconstruimos del contexto). La
  reseña de Cranston (*Bull. AMS* 39, 109–111, 2002) [V] repite la dicotomía "acotada o idénticamente infinita" con q
  en la clase de Kato. El libro de Chung y Zhao (Grundlehren 312, Springer 1995) [V, solo datos del editor] es la
  referencia completa; no pudimos abrir su texto.
- **La gauge en ℝ^d, d ≥ 3 (dominio no acotado).** Z. Zhao, *Trans. AMS* 334, 75–96 (1992) [V, resumen]: para
  −½Δ + V en ℝ^d, d ≥ 3, con V en K_d y una condición de Kato en el infinito, demuestra la equivalencia entre
  subcriticidad, positividad fuerte y gaugeabilidad. Z.-Q. Chen, *Trans. AMS* 354, 4639–4679 (2002) [V, resumen]
  generaliza a procesos de Borel transitorios: gaugeabilidad, gaugeabilidad condicional y subcriticidad son
  equivalentes. **No pudimos leer los enunciados completos** (el PDF de la AMS no se pudo descargar desde este entorno);
  por eso la parte esencial de nuestro resultado (sección 3) se demuestra **sin** usarlos.
- **Fórmula de momentos de Kac.** Fitzsimmons y Pitman, *Stoch. Proc. Appl.* 79, 117–134 (1999) [V: RePEc y el informe
  técnico de Berkeley]: para v ≥ 0 y un tiempo de muerte markoviano T, E_μ[A_v^n] = n! μ(G M_v)^n 1, con G el operador de
  Green del proceso muerto y M_v la multiplicación por v.
- **Longitud de dispersión como integral de Wiener.** Kac y Luttinger, *Ann. Inst. Fourier* 25 (3-4), 317–321 (1975)
  [V, datos y resumen]; P. He, *Proc. AMS* 139, 1871–1877 (2011) [V, datos y resumen]. El resumen de He dice que extiende
  la fórmula de Kac a procesos con dualidad débil; las referencias que cita (Takeda, "positive smooth measures"; Taylor,
  "positive potentials") indican que toda esta línea trata potenciales **positivos (repulsivos)**. No leímos el texto de
  Kac–Luttinger, así que no citamos su fórmula; nuestra a = −(2/δ²) E_Γ[φ] es una identidad elemental (sección 4), no
  la de ellos.
- **Tiempo de estancia en una bola.** Ciesielski y Taylor, *Trans. AMS* 103 (3) (1962), DOI 10.1090/S0002-9947-1962-0143257-8 [V, título, volumen y DOI; páginas no verificadas]. No pudimos abrir
  el texto; la fórmula E_0[e^{pT}] = 1/cos√(2p) para el tiempo total T en la bola unidad de ℝ³ la **derivamos** aquí
  (sección 5) y la usamos como caso exacto.

**Resumen:** no encontramos la gauge usada para un potencial **atractivo** cerca de su umbral, ni la discusión de la
varianza del estimador. Todo lo que sigue sobre eso es nuestro.

## 3. Resultado principal (demostrado): momentos del peso y ventana de varianza infinita

**Teorema 1.** Sea δ > δ_c, x ∈ ℝ³ y p > 0. Entonces E_x[W^p] = E_x[e^{pΛ}] < ∞ si y solo si p < δ/δ_c. En ese caso
E_x[e^{pΛ}] = φ_p(x), la solución de energía cero de pV normalizada a 1 en el infinito. En particular:

- la media E_x[W] = φ(x) es finita para todo δ > δ_c (porque δ/δ_c > 1);
- la **varianza es infinita si y solo si δ_c < δ ≤ 2δ_c ≈ 2.381**, **incluido el caso de igualdad** δ = 2δ_c;
- en general, el momento de orden p es finito si y solo si δ/p > δ_c.

**Prueba.** Sea G_0 el operador de Green de −½Δ en ℝ³, con núcleo G_0(x, y) = 1/(2π|x − y|) (el movimiento browniano en
ℝ³ es transitorio y no hace falta matarlo). Por la fórmula de Kac [Fitzsimmons y Pitman 1999], con T = ∞,
E_x[Λ^n] = n! ((G_0 q)^n 1)(x). Como todos los términos son ≥ 0, por Tonelli

  E_x[e^{pΛ}] = 1 + Σ_{n≥1} p^n ((G_0 q)^n 1)(x).  (1)

Sea K = q^{1/2} G_0 q^{1/2} en L²(ℝ³). Su norma de Hilbert–Schmidt es ∫∫ q(x)q(y)/(4π²|x − y|²) dx dy, finita para el
Yukawa (q ∈ L^{3/2} ∩ L¹ y la desigualdad de Hardy–Littlewood–Sobolev; es la condición de Rollnik). Entonces K es
compacto, autoadjunto y positivo, con autovalores κ_1 ≥ κ_2 ≥ … > 0. Su núcleo es estrictamente positivo (q > 0 en todo
punto y G_0 > 0), así que por el teorema de Jentzsch (Perron–Frobenius para operadores integrales) κ_1 es simple y su
autofunción e_1 es > 0 en casi todo punto. Con f = q^{1/2} ∈ L² (∫q dx = 4π/δ²) y g_x = q^{1/2} G_0(x, ·) ∈ L²,

  ((G_0 q)^n 1)(x) = ⟨g_x, K^{n−1} f⟩ = Σ_k c_k(x) κ_k^{n−1},  c_k(x) = ⟨g_x, e_k⟩⟨e_k, f⟩.

Cota superior: |⟨g_x, K^{n−1} f⟩| ≤ ‖g_x‖ ‖f‖ κ_1^{n−1}, así que (1) converge si p κ_1 < 1. Cota inferior: c_1(x) > 0
(porque g_x, f ≥ 0 no nulas y e_1 > 0) y κ_k ≤ κ_2 < κ_1 para k ≥ 2, así que ⟨g_x, K^{n−1}f⟩ = c_1 κ_1^{n−1}(1 + o(1)).
Si p κ_1 ≥ 1 los términos de (1) no tienden a 0 y la serie diverge. Por tanto E_x[e^{pΛ}] < ∞ si y solo si p < 1/κ_1.

Falta identificar 1/κ_1. Si K e = κ e, la función ψ = G_0 q^{1/2} e cumple q^{1/2}ψ = κe y ψ = κ^{−1} G_0 q ψ, es decir,
−½Δψ − κ^{−1} q ψ = 0, y ψ = O(1/|x|) en el infinito: es una solución de energía cero acotada (ligado o resonancia) de
−½Δ − κ^{−1} q. Al revés, una solución así da un autovector de K. Es el principio de Birman–Schwinger, y aquí lo hemos
comprobado directamente. El menor acoplamiento p con solución de energía cero acotada es aquel en que aparece el primer
estado ligado s, p_1 = δ/δ_c (sección 1), así que 1/κ_1 = δ/δ_c. Para p < p_1, la serie (1) es la serie de Neumann
de φ_p = 1 + G_0(p q) φ_p, que es la ecuación integral de la solución de energía cero normalizada. ∎

Comprobación numérica (control C6): el primer cero de la pendiente α(p) de la solución regular de u'' = −2pqu da
δ/p_1 = 1.190612421060 en los siete δ, igual que δ_c (diferencia relativa < 1e-12). El segundo cero da
δ/p_2 = 0.3102092827, el umbral del estado 2s. En δ = 2δ_c la función φ_2 no existe (α(2) = 0), y por convergencia
monótona E[W²] = lím_{p→2⁻} φ_p(x) = ∞.

**Comentario sobre el teorema de la gauge.** El Teorema 1 es un caso particular, con prueba elemental, de la equivalencia
"gaugeable si y solo si subcrítico" de Zhao (1992) para q ≥ 0. El teorema general hace falta solo para potenciales con
signo (sección 7, guías que no son supersoluciones).

## 4. Identidad del estimador de a

Como r² V(r) = −r e^{−δr} y ∫_0^∞ r e^{−δr} dr = 1/δ², a = 2∫ r² V φ dr se escribe

  a = −(2/δ²) E_{r_0 ∼ Γ(2, 1/δ)}[φ(r_0)] = −(2/δ²) E[W],  con r_0 sorteado con densidad δ² r e^{−δr}.

Así a es la media de un solo peso por camino, con partida aleatoria. La identidad se comprobó por cuadratura de
Gauss–Laguerre (control C4: diferencia relativa ≤ 4.7e-12). La varianza de este estimador es infinita en la misma
ventana del Teorema 1.

**Covarianza de escala.** Si r_0 ∼ Γ(2, 1/δ), la ley de X = δΛ no depende de δ. Prueba: con B_t = B̃_{δ²t}/δ (escala
browniana) y partida B̃_0 = δ r_0 ∼ Γ(2, 1), Λ = ∫ δ e^{−|B̃_{δ²t}|}/|B̃_{δ²t}| dt = δ^{−1} ∫ e^{−|B̃_s|}/|B̃_s| ds. ∎
El esquema numérico (paso dt = η² r², R_in = 36/δ) respeta esta escala camino a camino, así que **una sola muestra de
X da W = e^{X/δ} para todos los δ**.

## 5. Ley exacta de Λ: mezcla de exponenciales con tasas δ/δ_c(ns)

**Proposición 2 (derivada aquí; un paso sin demostrar).** Si Σ_k |c_k(x)|/κ_k < ∞, entonces

  P_x(Λ > λ) = Σ_k w_k(x) e^{−p_k λ},  p_k = δ/δ_c(ks),  w_k(x) = c_k(x)/κ_k,  Σ_k w_k = 1.

Equivalentemente, en radial, w_k(r) = −ũ_{p_k}(r)/(r α'(p_k) p_k), que es menos el residuo de φ_p(r) en p = p_k
dividido por p_k. Solo cuentan los estados s porque la partida y q son radiales.

*Derivación.* Por la sección 3, E_x[Λ^n]/n! = Σ_k c_k κ_k^{n−1} = Σ_k (c_k/κ_k) κ_k^n para n ≥ 1. La mezcla con signo
ν = Σ_k w_k Exp(p_k) tiene momentos n! Σ_k w_k p_k^{−n}, iguales. Las medidas λ dP_Λ y λ dν tienen todos los momentos
iguales y función generatriz analítica cerca de 0, así que coinciden; como P(Λ = 0) = 0 (q > 0), también las masas
totales, Σ_k w_k = 1. El paso sin demostrar es la convergencia absoluta Σ|w_k| < ∞. Numéricamente, para la partida
Γ(2, 1/δ) los pesos son todos positivos y bajan como k^{−3} aproximadamente (w̄_1 = 0.80317, w̄_2 = 0.11778,
w̄_3 = 0.03691, …; los 14 primeros suman 0.99742). Para una partida fija cerca del origen los w_k alternan de signo y
bajan despacio (en r = 0.05: 1.841, −1.327, 0.608, …), como en el caso exacto de Ciesielski–Taylor en el centro de la
bola, donde la serie converge solo condicionalmente.

**Caso exacto (control C5).** Para q = 1_{r<1} (Λ = tiempo total en la bola unidad), la solución de energía cero da
φ_p(0) = 1/cos√(2p): dentro u = C sin(kr), k = √(2p); fuera φ = 1 − a/r; la continuidad de φ y φ' en r = 1 da
C cos k = 1. Polos p_k = (k − ½)²π²/2 y desarrollo en fracciones simples de 1/cos z: w_k = (−1)^{k+1} 4/((2k − 1)π),
con Σ w_k = 1 (serie de Leibniz). El mismo código que usamos para el Yukawa reproduce p_k y w_k (k = 1…5) con error
relativo ≤ 1e-11.

**Corolario (cola del peso).** Con θ = p_1 = δ/δ_c,

  P(W > w) = w_1 w^{−θ} [1 + O(w^{−(p_2 − p_1)})],  p_2/p_1 = δ_c/δ_c(2s) = 3.838.

La cola es una ley de potencias casi pura: la corrección baja como w^{−2.84θ}. Para la partida Γ, w̄_1 = 0.80317 es
universal (no depende de δ). Si solo se usa el Teorema 1 (sin la Proposición 2), lo demostrado es que el índice de la
cola, en el sentido de los momentos, es exactamente θ = δ/δ_c.

**Consecuencias para el Monte Carlo (argumento estándar de leyes estables, no demostrado aquí para W).** Para
1 < θ < 2, la media muestral converge, pero con error de orden n^{1/θ − 1} y fluctuaciones de ley estable de índice θ;
la varianza muestral crece como n^{2/θ − 1}. En δ = 1.5 (θ = 1.260) el error baja como n^{−0.21}; en δ = 1.2
(θ = 1.008), como n^{−0.008}: **el Monte Carlo libre no sirve cerca del umbral, aunque la media sea finita.**

## 6. Discretización: por qué el trapecio no sirve y qué esquema sí

**Proposición 3 (demostrada).** Con dt = η² r² y el trapecio ∫q dt ≈ dt[q(r) + q(r')]/2, la media del estimador
discretizado es infinita para todo η > 0. *Prueba:* en un paso desde r, r' = |x + √dt Z| tiene densidad ∼ c r'² cerca
de 0, y el peso contiene el factor exp(η² r² e^{−δr'}/(2r')) ≥ exp(C/r'); ∫_0 r'² e^{C/r'} dr' = ∞, y los demás
factores son ≥ 1. ∎ En las pruebas, a(δ = 3) dio −2.4e145 (η = 0.8) y −4.6e84 (η = 0.4) con 1e6 caminos; con η = 0.2 el
evento raro no salió en esa muestra, pero la media sigue siendo infinita.

**Esquema de puente (el que usamos).** Cada paso usa la transición exacta del proceso de Bessel-3 (norma de un gaussiano
3D) y, en lugar del trapecio, la media **exacta** de ∫q sobre el puente browniano 3D entre los extremos. En el tiempo
s = t·dt, la posición del puente es gaussiana de media x + t(y − x) y varianza t(1 − t)dt por componente, y para el
Yukawa la media gaussiana tiene forma cerrada:

  E[e^{−δ|X|}/|X|] = [e^{δ²σ²/2 − δR} erfc((δσ² − R)/(σ√2)) − e^{δ²σ²/2 + δR} erfc((δσ² + R)/(σ√2))]/(2R),

con R = |media| (lejos de la singularidad se reduce a q(R) e^{δ²σ²/2}, porque Δq = δ²q fuera del origen). La integral
en t se hace con Gauss–Legendre de 3 nodos interiores (σ > 0, sin singularidad). Propiedades:

1. **Dominación.** Condicionado a los puntos de la malla (los tiempos son predecibles: dt_k depende solo de la posición
   en t_k), los tramos son puentes independientes. Por Jensen condicional, exp(Σ I_k) ≤ E[e^{∫q} | malla]; por tanto
   E[W_disc^p] ≤ E[W^p] para todo p ≥ 1 (salvo la cuadratura en t). El esquema no puede crear colas que no existan y su
   sesgo en φ es negativo.
2. **E[Λ] insesgado.** Por la propiedad de la torre, E[Λ_disc] = E[Λ] salvo la cuadratura en t. Con la partida Γ,
   E[δΛ] = 1 exactamente (C16). Medido: 0.98861 ± 0.00030 con η = 0.8 (la cuadratura de 3 nodos falla con pasos tan
   grandes), y 1.00032 ± 0.00035, 0.99952 ± 0.00036, 1.00026 ± 0.00066 con η = 0.4, 0.2, 0.1.
3. **Orden del sesgo.** El único sesgo es la brecha de Jensen paso a paso, ½ Σ_k Var(∫_k q | extremos). Con
   dt = η²r², la varianza de un tramo es del orden de η² (q dt)²; sumada sobre los ∼ 1/η² pasos por escala da un sesgo
   relativo O(η⁴). Medido (02): orden 3.25 a 3.49 entre η = 0.8 y 0.4, y 3.40 a 4.58 entre 0.4 y 0.2.
4. **Cierre exacto en R_in.** Fuera de R_in = 36/δ, q < e^{−36}/R_in; si el paso sale de R_in, el camino vuelve a la
   esfera R_in con probabilidad R_in/r (función armónica 1/r) y se reinicia allí exactamente (propiedad de Markov fuerte),
   o escapa para siempre. No hay tiempo de proyección ni caja.

## 7. Muestreo por importancia: transformada h de Doob a energía cero

Sea φ_T > 0 con φ_T → 1 en el infinito y E_L = (Hφ_T)/φ_T, H = −½Δ + V. La difusión guiada
dX = ∇ ln φ_T(X) dt + dB tiene generador ½Δ + ∇ln φ_T·∇, y

  φ(x) = φ_T(x) E^T_x[exp(−∫_0^∞ E_L(X_t) dt)].  (2)

(Es la transformada h de Doob con h = φ_T; la identidad se obtiene con el martingala φ_T(B_t) exp(∫_0^t q_T) hasta la
salida de bolas grandes y el límite. Damos solo el esbozo; la validación numérica está en 04.)

**Segundo momento (derivado, con el mismo cambio de medida).** E^T[Y²] = φ_T(x) E_x[exp ∫(2q − q_T)] para la guía
φ_T de un Yukawa con δ_T, porque entonces E_L = q_T − q. Es la gauge del potencial con signo 2q − q_T: por el teorema
de Zhao (1992) es finita si y solo si −½Δ − (2q − q_T) es subcrítico. Más en general, E^T[Y^p] es finito si y solo si
(1 − p)q_T + p q es subcrítico. Esta afirmación descansa en Zhao 1992, del que solo verificamos el resumen.

**Proposición 4 (demostrada, elemental).** Si φ_T es supersolución (E_L ≥ 0 en todo punto), el peso exp(−∫E_L) está en
(0, 1], el estimador Y = φ_T(x) e^{−∫E_L} cumple 0 < Y ≤ φ_T(x) y todos sus momentos son finitos. Además
E[Y²] ≤ φ_T(x) E[Y] = φ_T(x) φ(x), así que

  varianza relativa ≤ φ_T(x)/φ(x) − 1.

Para la partida Γ: varianza relativa ≤ E[φ_T φ]/E[φ]² − 1.

**Elección (regla fijada antes de correr):** φ_T = solución de energía cero del Yukawa con δ_T tal que a_T = 1.25a. Como
δ_c < δ_T < δ, q_T > q y E_L = q_T − q = e^{−δ_T r}(1 − e^{−(δ−δ_T)r})/r ∈ [0, δ − δ_T]: es supersolución. La cota de
varianza relativa resultante va de 0.0988 (δ = 3) a 0.5548 (δ = 1.192): **acotada uniformemente cuando δ → δ_c⁺.**

**Mapa de finitud para guías que no son supersoluciones.** Con δ_T > δ (E_L < 0, pesos > 1), la varianza sigue finita
mientras 2q_δ − q_{δT} sea subcrítico. El δ_T máximo crece de 1.2095 (δ = 1.2) a 5.133 (δ = 2.0) y diverge en
δ → 2δ_c. Cerca del umbral la ventana δ_T ∈ (δ_c, δ_T^max) se cierra: hay que acertar la guía con precisión creciente
por encima de δ, pero cualquier δ_T ∈ (δ_c, δ) funciona.

**El ansatz 1 + A/(r + b).** Su energía local es E_L = Ab/[r(r + b)²(r + b + A)] − q. Es supersolución solo si
b e^{δr} ≥ (r + b)²(1 + (r + b)/A) para todo r; con A → ∞ el mínimo en r de ln b + δr − 2ln(r + b) es
ln b + 2 − δb − 2 ln(2/δ), máximo en b = 1/δ, donde vale ln δ + 1 − 2 ln 2. **Por tanto este ansatz puede ser
supersolución solo si δ ≥ 4/e ≈ 1.4715.** Con la cúspide de Kato (b² + Ab = A) y A = c|a|, el criterio de 01 da varianza
finita en δ = 3 y 1.5 para c ∈ {0.8, 1, 1.25, 2}, pero **infinita en δ = 1.3 para c ≤ 1.25** (solo c = 2 queda finita).
Un ansatz sencillo no basta cerca del umbral; la guía tiene que ser una supersolución.

**Costo.** Fuera del potencial φ_T ≈ 1 + A/r con A = |a_T|; para r ≪ A la deriva de la guía (≈ −1/r) cancela la de
Bessel-3 (+1/r) y el proceso radial se comporta como un browniano 1D, que tiene que llegar a r ∼ A para escapar. Con
dt = η²r², el número de pasos por camino es ∝ |a_T|/η² ∝ 1/(δ − δ_c). Es el análogo, a energía cero, del tiempo de
proyección ∝ 1/|E_0| ∝ (δ_c − δ)^{−2} de PIGS o de la transferencia del lado ligado.

**Discretización de la difusión guiada.** E_L es acotada, así que el trapecio no tiene el problema de la sección 6. El
paso es híbrido: imagen 3D (Bessel exacto + Euler de la deriva acotada ∇ ln φ_T) para r < 1/δ_T e imagen radial 1D
(Euler con la deriva total u_T'/u_T, pequeña) para r ≥ 1/δ_T, para no aplicar Euler por separado a dos derivas grandes
que se cancelan. El sesgo es O(η²) y se mide en 04.

## 8. ¿Es el peso real, positivo y normalizable? (pedido del curso)

| Variante | Medida muestreada | Peso | ¿Real y positivo? | ¿Normalizable? |
|---|---|---|---|---|
| Libre exacto | Wiener (browniano 3D, transitorio) | W = e^{Λ} ≥ 1 | Sí | La medida, sí; el peso tiene media finita para todo δ > δ_c, pero **varianza infinita para δ_c < δ ≤ 2δ_c** y momento p infinito si p ≥ δ/δ_c |
| Libre con trapecio | Malla de Bessel-3 exacta | exp(Σ dt(q + q')/2) | Sí | **No**: media infinita para todo η > 0 (Proposición 3) |
| Libre con puente | Malla de Bessel-3 exacta | exp(Σ E[∫q \| extremos]) | Sí | Sí, con E[W_disc^p] ≤ E[W^p] (hereda la misma ventana de varianza infinita) |
| MI con supersolución (δ_c < δ_T < δ) | Difusión guiada (transitoria) | e^{−∫E_L} ∈ (0, 1] | Sí | Sí, acotado: todos los momentos finitos, varianza relativa ≤ φ_T/φ − 1 |
| MI con δ_T > δ | Difusión guiada | e^{+∫\|E_L\|} > 1 | Sí | Media finita; varianza finita solo si δ_T < δ_T^max(δ) (mapa de 01) |

## 9. Comparación con PIGS, la transferencia y el Monte Carlo de línea de mundo

- **PIGS y transferencia (Fases 2 y 3).** Proyectan el fundamental con e^{−τH}: el tiempo de proyección necesario es
  τ ≫ 1/|E_1 − E_0|, y en el umbral E_0 → 0 como (δ_c − δ)² (Fase 3: κ ≈ 0.741(δ_c − δ)), así que τ ∝ (δ_c − δ)^{−2};
  en δ = 1.19, |E_0| ≈ 1e-7 y τ ∼ 1e7. Además necesitan una caja que contenga el estado (R ∼ 1/κ).
- **La gauge** trabaja a energía cero, sin caja y sin τ. El precio es el costo por camino ∝ |a| ∝ 1/(δ − δ_c) del lado
  no ligado, y la varianza infinita del estimador libre en δ_c < δ ≤ 2δ_c. La pendiente c = −d(1/a)/dδ en δ_c, medida
  con la EDO, es 0.7413, la misma que la pendiente de κ de la Fase 3: 1/a pasa de forma analítica por el umbral y es
  κ del lado ligado.
- **Edwards et al., arXiv:1903.00536 [V-arXiv]** (leído en arXiv): calculan E_0 del Yukawa con línea de mundo para
  μ = 0, 0.1, 0.15, 0.2, 0.25 y 0.5 (en unidades m = α = 1), con partida y = x = (0.001, 0, 0); no calculan el
  apantallamiento crítico (solo citan μ_c ≈ 1.19 αm). Llaman "undersampling" al fenómeno por el que "our numerical
  simulations cease to measure the potential of the system in a representative manner": los lazos crecen como √t y, para
  potenciales localizados, dejan la región donde el potencial es fuerte; en el Yukawa esperan que eso subestime el núcleo
  a t ≫ 1. Ajustan E_0 en una ventana de t (t ∈ [7, 15] para casi todos los μ) y notan que esa ventana se achica al
  crecer el apantallamiento. Suavizan la singularidad sustituyendo los valores puntuales del potencial por integrales de
  línea entre puntos consecutivos de la discretización (para el Yukawa, por cuadratura numérica). Nuestro esquema de
  puente es la versión exacta de esa idea: en vez de la integral sobre la recta usa la media sobre el puente browniano,
  y con eso el estimador queda dominado por el exacto (sección 6).
- **Qué cambia a energía cero.** El "undersampling" desaparece: el camino que se va ya no aporta nada (q ≈ 0), el cierre
  en R_in es exacto y no hay que elegir ventana de tiempo. Lo que aparece en su lugar es la cola de potencias del peso,
  que hace al estimador libre inútil cerca del umbral, y que la transformada h corrige.

## 10. Qué queda demostrado, qué derivado y qué conjeturado

- **Demostrado:** Teorema 1 (finitud de los momentos si y solo si p < δ/δ_c; ventana de varianza infinita
  δ_c < δ ≤ 2δ_c con la igualdad incluida), con la fórmula de Kac [V] y argumentos estándar de operadores compactos;
  covarianza de escala; Proposición 3 (trapecio con media infinita); dominación del esquema de puente; Proposición 4
  (pesos acotados con supersolución y cota de la varianza relativa).
- **Derivado con un paso abierto:** Proposición 2 (ley de mezcla de exponenciales y prefactor de la cola), suponiendo
  Σ|w_k| < ∞; comprobada exactamente en Ciesielski–Taylor y numéricamente contra el Monte Carlo (03).
- **Apoyado solo en el resumen de Zhao 1992 / Chen 2002:** el criterio general de finitud de la varianza para guías con
  E_L de signo variable (mapa y ansatz).
- **Argumento físico, no demostrado:** escalas de la ley estable (n^{1/θ − 1}, n^{2/θ − 1}); orden η⁴ del sesgo; costo
  ∝ |a_T|/η² de la difusión guiada.

