# Apéndice E2: teoría del criterio de cruce de cajas

*Proyecto 05, Fase 4, extensión E2. Unidades ħ = m = g = 1, V(r) = −e^{−δr}/r, onda s, esfera de pared dura de radio R
(u(0) = u(R) = 0). Todas las cifras de este apéndice salen de `resultados/01_teoria.json` (script `codigo/01_teoria.py`) salvo
que se diga otra cosa.*

## 1. La condición de cuantización exacta fuera del alcance

Fuera del alcance del potencial (r mayor que unas pocas veces 1/δ), la solución radial de energía E = k²/2 > 0 es
exactamente

$$u(r) \propto \sin\big(kr + \eta_0(k)\big),$$

donde η₀(k) es el corrimiento de fase de onda s del potencial **en el espacio libre**. Esto no es una aproximación: la caja
solo impone la condición en r = R. La única corrección es la cola del Yukawa en r = R, del orden de e^{−δR}; en R = 50 vale
1.4×10⁻²⁶ (`cola_exp_R50`), así que no se ve en ninguna cifra de este trabajo.

La pared pide sin(kR + η₀) = 0, es decir η₀ = nπ − kR, de donde cot η₀ = −cot(kR). Con la convención del proyecto
(a > 0 cuando hay ligado, u ≈ r − a a energía cero), el desarrollo de rango efectivo de Bethe es

$$k\cot\eta_0 = -\frac{1}{a} + \frac{r_e}{2}k^2 + O(k^4).$$

Igualando, y llamando x = kR, z = R/a y ε = r_e/R:

$$\boxed{\;x\cot x = z - \frac{\varepsilon}{2}\,x^2 + O(x^4/R^3)\;}\qquad y \equiv \frac{2R^2E_0}{\pi^2} = \frac{x^2}{\pi^2}.$$

Para E < 0 se pone x = iq y la misma ecuación se lee q coth q = z + (ε/2) q², que es la continuación analítica. La
función x cot x es continua en x = 0 (vale 1), de modo que la rama del estado base pasa sin saltos de E > 0 a E < 0.

## 2. La función de escala de alcance cero y sus puntos fijos

Con ε = 0 (alcance cero) la energía en la caja depende de δ y R **solo a través de z = R/a(δ)**:

$$E_0R^2 = \frac{\pi^2}{2}F(R/a),\qquad x\cot x = z,\qquad F(z) = x^2/\pi^2 .$$

Casos que se leen sin calcular:

- **Umbral** (1/a = 0, z = 0): cot x = 0, x = π/2, **F(0) = 1/4**, para todo R. Este es el punto fijo.
- **Sin interacción** (a pequeño y negativo, z tiende a menos infinito): x tiende a π, F tiende a 1 (el modo libre sin²).
- **z = 1** (R = a): x = 0 y E₀ = 0 exactamente. Es el radio en el que el autovalor cambia de signo; la Fase 3 (G4)
  midió R_c(h) convergiendo a a_s = 2203.8 en δ = 1.19, que es esta misma afirmación.
- **Ligado** (z > 1): q coth q = z; para z grande q ≈ z y y ≈ −z²/π², es decir E₀ ≈ −1/(2a²) = −κ²/2 con κ = 1/a.

La pendiente en el umbral es dF/dz = −2/π² (de x ≈ π/2 − 2z/π); el script la reproduce con 10 cifras (`pendiente_F_en_0`).

**La extensión.** Fuera del alcance, u = sin(x(1 − r/R)). Con t = 1 − r/R,

$$\rho \equiv \frac{\langle r\rangle}{R} = G(z) = 1 - \frac{\int_0^1 t\,\sin^2(xt)\,dt}{\int_0^1\sin^2(xt)\,dt}.$$

En el umbral, u = cos(πr/2R), ∫₀^R u² dr = R/2 y ∫₀^R r u² dr = R²(1/4 − 1/π²), así que

$$G(0) = \frac{1}{2} - \frac{2}{\pi^2} = 0.297358\ldots$$

Los otros límites son G = 1/2 (modo libre, z tiende a menos infinito), G = 1/4 en z = 1 (u = 1 − r/R) y G tendiendo a 0
como 1/(2z) para el ligado. La pendiente en el umbral es dG/dz = 2(π² − 12)/π⁴ = −0.04374.

**Por qué las curvas se cruzan.** Si δ < δ_c, a > 0 y z = R/a crece con R, así que y baja con R (hacia −∞). Si δ > δ_c,
a < 0 y y sube con R (hacia 1). En δ = δ_c, y = 1/4 para todo R. Por eso las curvas y(δ; R) de cajas distintas se cruzan, y
en alcance cero se cruzan **exactamente** en δ_c y en y = 1/4. Lo mismo vale para ρ con el punto fijo 0.2974.

**Comprobación exacta (pozo cuadrado).** Para un pozo de alcance b dentro de la esfera, con a fijo y b/R pequeño, la
condición de empalme es exacta y no usa el desarrollo de rango efectivo. Con R = 100 y z = −2, 0, 0.5 y 2, la diferencia
y − F(z) baja a la mitad cada vez que b se divide por 2 (razones 2.031, 2.015, 2.008, 2.004 en z = 0), y en z = 0 vale
r_e/(4R) con r_e = b, el rango efectivo del pozo en resonancia. Esto confirma la función de escala y el signo y tamaño de
la corrección de orden 1/R (tabla en `pozo_cuadrado`).

## 3. Correcciones de alcance finito

**Rango efectivo.** Con ε = r_e/R ≠ 0 se resuelve la ecuación del recuadro por series (se hizo con sympy y se comprobó
numéricamente):

$$y = \frac14 - \frac{2z}{\pi^2} + \frac{\varepsilon}{4} - \frac{4z^2}{\pi^4} - \frac{z\varepsilon}{\pi^2} + \frac{3\varepsilon^2}{16} + O(3).$$

En δ_c (z = 0): y(δ_c, R) = (1/4)(1 + r_e/R) + O(R⁻²). Para el Yukawa en el umbral, r_e = 2∫₀^∞(1 − u₀²/C²) dr con u₀ la
solución a energía cero (que tiende a la constante C):

$$r_e(\delta_c) = 1.78063,\qquad c \equiv -\frac{d(1/a)}{d\delta}\Big|_{\delta_c} = 0.741192 .$$

El valor de c es la pendiente κ ≈ 0.741(δ_c − δ) que la Fase 3 encontró ajustando; aquí sale de la energía cero, sin
ajustar.

**Dónde se cruzan dos cajas.** El par (R, 2R) cambia z por 2z y ε por ε/2. Imponiendo y(z, ε) = y(2z, ε/2) y despejando
z* como serie en ε:

$$z^* = -\frac{\pi^2}{16}\varepsilon - \frac{3\pi^2}{32}\varepsilon^2 + O(\varepsilon^3).$$

Como z* = R/a* y 1/a ≈ c(δ_c − δ), resulta

$$\boxed{\;\delta^*(R,2R) - \delta_c = \frac{\pi^2 r_e}{16\,c\,R^2} + \frac{3\pi^2 r_e^2}{32\,c\,R^3} + O(R^{-4})\;}$$

con α_y = π² r_e/(16c) = 1.4819 y β_y = 3π² r_e²/(32c) = 3.958. **La convergencia es en 1/R², no en 1/R**, aunque el valor
de y en el umbral sí tenga una corrección 1/R: en la diferencia de dos cajas, el término r_e/(4R) se resta a sí mismo a
medias, y lo que queda se compensa con un corrimiento de 1/a del orden de 1/R². El término O(R⁻⁴) recoge el parámetro de
forma del desarrollo de rango efectivo y la variación de r_e(δ) entre δ_c y δ*; ninguno de los dos se calcula aquí.

El valor de y en el cruce es

$$y^* = \frac14 + \frac{3r_e}{8R} + \frac{27r_e^2}{64R^2} + O(R^{-3}),$$

con R la caja menor del par. Como r_e > 0 para el Yukawa, el cruce cae **por encima** de δ_c y el valor en el cruce
**por encima** de 1/4; un perfil con r_e < 0 los daría por debajo (es lo que el prototipo vio en el ECSC, que E3 estudia).

**La extensión.** Para ρ hace falta además lo que pasa dentro del alcance. La función verdadera es igual a la exterior
u_ext(r) = sin(x(1 − r/R))/sin x (normalizada a u_ext(0) = 1) salvo cerca del origen, y la diferencia de normas es, a
energía cero, exactamente la que define r_e: ∫(u_ext² − u²) dr = r_e/2. Con m₁ = ∫₀^∞ r(1 − u₀²/C²) dr = 0.6502,

$$\rho = \frac{I_1(x) - m_1/R^2}{I_0(x) - r_e/(2R)},\qquad I_n(x) = \int_0^1 t^n u_{\rm ext}^2\,dt .$$

A primer orden, ρ(δ_c, R) = 1/2 − 2/π² + (1/4 + 1/π²) r_e/R, y el cruce es

$$\delta^*_\rho(R,2R) - \delta_c = -\frac{k_1 r_e}{c R^2},\qquad k_1 = \frac{\pi^2(4+\pi^2)}{16(\pi^2-12)} = -4.0159,$$

o sea α_ρ = 9.648: **también 1/R², pero con un coeficiente 6.5 veces mayor que el de y**. La extensión es un observable de
localización con punto fijo exacto, pero converge más despacio que la energía.

## 4. Modelo de rango efectivo completo y comparación con lo medido

El "modelo ERE" resuelve la ecuación del recuadro sin desarrollar en series, con a(δ) y r_e(δ) calculados a energía cero
en cada δ. Sus cruces (sección `modelo_ERE`) y la serie de dos términos coinciden a 10⁻⁹ o mejor para R ≥ 200, y los
cocientes de diferencias sucesivas son 4.13, 4.06, 4.03, 4.02, el valor 4 de una ley 1/R² con corrección 1/R³.

La comparación con los cruces medidos está en `resultados/05_cruces.json` y en la sección del artículo. Con el disparo sin
malla el acuerdo con el modelo ERE es de 5×10⁻⁷ en el par 50/100 y de unos 10⁻⁹ desde el par 200/400: **la teoría predice
los cruces, sin parámetros libres, a partir de dos números de energía cero (r_e y c)**.

## 5. Lo que cambia con la integral de camino: el corrimiento de la pared

En la matriz de transferencia la pared en R no tiene imagen; la Fase 3 (decisión 5) mostró que actúa como una pared en
R + β√ε con β = −ζ(1/2)/√(2π) = 0.5826, y la dejó solo en el error. Tras la extrapolación ε² de la receta, el radio
efectivo es R + c_w con c_w = β[√0.05 + (√0.05 − √0.1)/3] = 0.1123. Un corrimiento uniforme de la pared equivale a cambiar
r_e por r_e − 2c_w en el término 1/R de y, y por tanto mueve el cruce de la transferencia en

$$\Delta\delta^*_{\rm pared} \approx -\frac{\pi^2 c_w}{8 c R^2},$$

que vale −1.17×10⁻⁶ en el par 400/800 (el modelo completo da −1.18×10⁻⁶). Es otra corrección de orden 1/R², así que la
extrapolación en R la absorbe, pero conviene saber su tamaño: es la que explica que los cruces de la transferencia queden
un poco por debajo de los del disparo.

## 6. Qué no puede hacer un artefacto de caja

- En una caja de Dirichlet, el autovalor es una función decreciente de R (dE/dR = −u'(R)²/2 < 0) y siempre mayor que la
  energía del espacio libre. Un E₀ < 0 en la caja implica un ligado en el espacio libre; el signo solo puede engañar en una
  dirección: decir "no ligado" cuando sí lo hay. Es lo que pasa en δ = 1.19 hasta R ≈ a_s = 2204.
- Que y baje con R no basta para decir "ligado". En el Yukawa repulsivo (control K12) a también es positivo, pero pequeño
  (del orden del alcance, como una esfera dura), y la rama que se ve es y = R²/(R − a)², que baja hacia 1 desde arriba. Lo
  que distingue al umbral es que y pase cerca de 1/4 y que las curvas de cajas distintas se crucen ahí; en el repulsivo
  y(R) − y(2R) no cambia de signo en todo el barrido y y > 1 siempre.
- El cruce no depende del signo. Para que dos cajas den el mismo y en el mismo δ hace falta que E₀ escale como R⁻² con
  coeficiente π²/8, y eso solo ocurre cuando la longitud de dispersión es mucho mayor que R. Un artefacto que suma un error
  suave a E₀ (malla, Trotter, pared) mueve el cruce en una cantidad que se puede medir (sección 5 y método B) y que cae con R.

## 7. Resumen de predicciones que se comprueban en el código

| Predicción | Valor | Dónde se comprueba |
|---|---|---|
| y en el umbral, alcance cero | 1/4 | 01 (`F0`) |
| ρ en el umbral, alcance cero | 1/2 − 2/π² = 0.29736 | 01 (`G0`) |
| Ley de convergencia del cruce | δ* − δ_c = α/R² + β/R³ | 05 (cocientes cercanos a 4) |
| α_y, β_y | 1.4819, 3.958 | 05 (ajuste) frente a 01 |
| α_ρ | 9.648 | 05 frente a 01 |
| y en el cruce | 1/4 + 3r_e/(8R) | 05 y control K6 |
| Colapso y = F(R/a) con corrección r_e/(4R) | | 02, figura D, control K11 |
| Corrimiento por la pared de la transferencia | −π²c_w/(8cR²) | 05 (transferencia frente a disparo) |
