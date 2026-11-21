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
exacto en todos sus momentos; su sesgo es negativo y, según un argumento heurístico, de orden η⁴ (los datos excluyen el orden 2 a unos 2 a 3σ; los órdenes medidos, entre 3.25 y 4.58, tienen incertidumbres grandes en el par 0.4/0.2).

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
1/(δ − δ_c). Es el análogo, a energía cero, del tiempo de proyección de PIGS: el tiempo físico de difusión hasta
r ∼ |a_T| crece como |a_T|² ∝ (δ − δ_c)^{−2}, igual que τ ∝ (δ_c − δ)^{−2}, pero el paso adaptativo dt = η²r² reduce el
número de pasos a ∝ (δ − δ_c)^{−1} (argumento de escala, no una comparación medida). Para δ = 1.1907 (a ≈ −1.5×10⁴), 621 caminos de 2.2×10⁶ pasos dan a con 2.3 %
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
- Z. Ciesielski y S. J. Taylor, *Trans. AMS* 103, 434–450 (1962), DOI 10.1090/S0002-9947-1962-0143257-8. [V]
- J. P. Edwards, U. Gerber, C. Schubert, M. A. Trejo, T. Tsiftsi y A. Weber, arXiv:1903.00536. [V-arXiv]
