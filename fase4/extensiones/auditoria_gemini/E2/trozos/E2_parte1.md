# Material para auditoría (parte 1 de 3)

Responde solo "Recibido" hasta la parte 3, que trae el encargo.

## Contexto

Proyecto de física teórica (curso universitario de integrales de camino). Potencial de Yukawa V(r) = −e^{−δr}/r en unidades ħ = m = g = 1, δ = μħ²/(mg); el estado 1s deja de existir en δ_c = 1.1906124210606.

## seccion_articulo.md

# Cruce de cajas: una prueba que separa un estado débil de un artefacto

*Sección para el artículo final (proyecto 05). Cálculo y redacción: Claude (IA), extensión E2 de la Fase 4. Todas las cifras
salen de `resultados/*.json`; la teoría completa está en `teoria.md`.*

## Motivación

En las Fases 2 y 3 decidimos "ligado o no ligado" por el signo de E₀ en cajas cada vez mayores. Ese criterio es correcto
pero lento cerca del umbral: en una caja de Dirichlet la energía nunca baja de la del espacio libre, así que el signo solo
puede equivocarse en una dirección, diciendo "no ligado" cuando sí hay ligado, y lo hace hasta que R supera la longitud de
dispersión a_s. En δ = 1.19, donde a_s = 2203.8, E₀ es positiva en todas las cajas hasta R = 1600 con los tres métodos
(tabla 3) y la Fase 3 necesitó R = 12800 para concluir 1.19 < δ_c < 1.20. Aquí proponemos otra prueba de caja que no
depende del signo: buscar dónde se cruzan las curvas de dos cajas.

## Idea y teoría

Fuera del alcance del potencial, la solución de onda s es sin(kr + η₀(k)) con el corrimiento de fase del espacio libre. La
pared dura en R impone, con x = kR y el desarrollo de rango efectivo k cot η₀ = −1/a + r_e k²/2,

$$x\cot x = \frac{R}{a} - \frac{r_e}{2R}x^2, \qquad y \equiv \frac{2R^2E_0}{\pi^2} = \frac{x^2}{\pi^2}.$$

Es la condición del método de la pared esférica de Borasoy et al. (2007). En el umbral (1/a = 0) y con alcance cero,
x = π/2: **y = 1/4 para toda caja**, mientras que y baja con R si hay ligado y sube hacia 1 si no lo hay. Con la función
de onda exterior cos(πr/2R), la extensión tiene también un punto fijo, **⟨r⟩/R = 1/2 − 2/π² = 0.2974**. Las curvas de
cajas distintas se cruzan, entonces, cerca de δ_c.

Desarrollando en r_e/R (`teoria.md`, sección 3), el cruce de las cajas R y 2R está en

$$\delta^*(R,2R) - \delta_c = \frac{\pi^2 r_e}{16\,c\,R^2} + \frac{3\pi^2 r_e^2}{32\,c\,R^3} + O(R^{-4}),$$

con r_e = 1.78063 (rango efectivo en el umbral) y c = −d(1/a)/dδ = 0.741192, los dos calculados a energía cero, sin
ajustar. Es decir, α = 1.4819 y β = 3.958: **la convergencia es en 1/R², no en 1/R**, aunque y(δ_c, R) = (1/4)(1 + r_e/R)
tenga una corrección 1/R. Para ⟨r⟩/R el coeficiente es α_ρ = 9.648, seis veces y media mayor. En la integral de camino la
pared sin imagen actúa como una pared en R + 0.1123 (tras la extrapolación en ε), lo que mueve el cruce en
−π²c_w/(8cR²): −1.18×10⁻⁶ en el par 400/800.

## Método

Rejilla: 23 valores de δ en [1.185, 1.196], más densos cerca de 1.1906, y R = 50, 100, 200, 400, 800, 1600 y 3200
(161 celdas). En cada celda se calcularon E₀ y ⟨r⟩ con tres métodos:

1. **Integral de camino** (matriz de transferencia con la acción de pares de Coulomb, `comun3.celda` de la Fase 3, sin
   cambios): h = 0.02 y 0.04 con Richardson h⁴, ε = 0.2, 0.1 y 0.05 con ley ε², y la barra de la Fase 3 (malla + Trotter +
   pared). Reproduce bit a bit las celdas de δ = 1.19 de la Fase 3 (control K14).
2. **Radial** de diferencias finitas con Richardson, h = 1/40 (la malla de la Fase 3) y h = 1/160.
3. **Disparo sin malla** (DOP853, tolerancia 10⁻¹², barra = diferencia con 10⁻¹³), como referencia casi exacta.

El cruce de cada par (R, 2R) es la raíz de y(δ, R) − y(δ, 2R) interpolada con un spline cúbico; se comparó con PCHIP, con un
cúbico local y con un cálculo sin interpolar (el disparo evaluado en cada δ pedido). La barra del cruce es la mayor entre un
Monte Carlo de 20240 réplicas gaussianas de cada celda (semilla fija) y la propagación lineal (σ_R + σ_2R)/|D′(δ*)|. Para la
integral de camino hay dos variantes, fijadas antes de calcular: **A**, la receta de la Fase 3 aplicada a E₀ y las barras
propagadas al cruce; **B**, la misma receta aplicada al cruce (se cruza con cada (h, ε) crudo y se extrapola), que mide
cuánto se mueve el cruce en vez de cuánto se mueve E₀. La extrapolación en R es un ajuste ponderado
δ* = δ_c + α/R² + β/R³ con los pares de R ≥ 100; a la barra se le suma la diferencia con el Richardson de los dos pares
mayores. Los umbrales de los controles se escribieron antes de correr (`criterios_previos.md`).

## Resultados

![Figura A](figuras/A_y_vs_delta.png)

*Figura A. 2R²E₀/π² frente a δ para siete cajas: integral de camino (puntos con barras) y radial h = 1/160 (líneas). Todas
pasan cerca de 1/4 en el mismo δ. A la derecha, ampliación cerca de δ_c.*

**Tabla 1. Cruces δ*(R, 2R) de 2R²E₀/π².**

| Par | Integral de camino, A | Integral de camino, B | Radial h = 1/160 | Disparo sin malla | Teoría (modelo ERE) | y en el cruce (disparo) |
|---|---|---|---|---|---|---|
| 50/100 | 1.1911616 ± 3.5e-4 | 1.1911617 ± 1.2e-4 | 1.1912376 ± 1.2e-5 | 1.191237550 | 1.191238046 | 0.26390 |
| 100/200 | 1.1907465 ± 8.4e-5 | 1.1907468 ± 2.6e-5 | 1.1907646 ± 1.2e-5 | 1.190764616 | 1.190764645 | 0.25681 |
| 200/400 | 1.1906452 ± 2.4e-5 | 1.1906458 ± 5.5e-6 | 1.1906500 ± 1.2e-5 | 1.190649967 | 1.190649968 | 0.25337 |
| 400/800 | 1.1906197 ± 2.5e-5 | 1.1906208 ± 3.1e-6 | 1.1906218 ± 1.2e-5 | 1.190621745 | 1.190621745 | 0.25168 |
| 800/1600 | 1.1906124 ± 5.4e-5 | 1.1906145 ± 2.6e-6 | 1.1906147 ± 1.1e-5 | 1.190614744 | 1.190614744 | 0.25084 |
| 1600/3200 | 1.1906083 ± 1.3e-4 | 1.1906128 ± 2.5e-6 | 1.1906128 ± 1.2e-5 | 1.190613001 | 1.190613001 | 0.25042 |

Tres hechos se leen en la tabla. Primero, **la teoría predice los cruces sin parámetros libres**: el modelo de rango
efectivo coincide con el disparo a 5×10⁻⁷ en el par 50/100 y a 2×10⁻⁹ o mejor desde el 200/400. Segundo, los cocientes de
diferencias sucesivas del disparo son 4.125, 4.062, 4.031 y 4.016, la ley 1/R², y el valor en el cruce baja hacia 1/4 como
1/4 + 3r_e/(8R) (cocientes medido/predicho entre 1.040 y 1.001). Tercero, la integral de camino queda sistemáticamente por
debajo del disparo; con el método B la diferencia es −7.6×10⁻⁵, −1.8×10⁻⁵, −4.2×10⁻⁶ y −9.4×10⁻⁷ en los pares 50 a 400,
frente a −8.3×10⁻⁵, −2.0×10⁻⁵, −4.8×10⁻⁶ y −1.18×10⁻⁶ que predice el corrimiento de la pared. Al restar ese corrimiento, el
cruce de la integral de camino coincide con el exacto a 2.4×10⁻⁷ o mejor desde el par 400/800.

![Figura B](figuras/B_cruces_vs_R.png)

*Figura B. Izquierda: δ* − δ_c,ref frente a 1/R² en escala logarítmica (pendiente 1, ley 1/R²) para los cuatro métodos y la
teoría. Derecha: ampliación lineal con los ajustes α/R² + β/R³ y las bandas finales en R infinito (azul: integral de camino
A; violeta: B; naranja: radial).*

**Tabla 2. Extrapolación en R e intervalo final** (pares con R ≥ 100).

| Fuente | Observable | δ_c | barra | intervalo | α ajustado (teoría) |
|---|---|---|---|---|---|
| integral de camino, A | 2R²E₀/π² | 1.1906106662 | 6.66e-5 | [1.19054410, 1.19067723] | 1.416 (1.482) |
| integral de camino, A | ⟨r⟩/R | 1.1906108583 | 6.04e-5 | [1.19055049, 1.19067123] | 10.198 (9.648) |
| integral de camino, B | 2R²E₀/π² | 1.1906123995 | 3.81e-6 | [1.19060859, 1.19061621] | 1.334 (1.482) |
| integral de camino, B | ⟨r⟩/R | 1.1906120950 | 1.47e-5 | [1.19059739, 1.19062680] | 10.117 (9.648) |
| radial h = 1/160 | 2R²E₀/π² | 1.1906123326 | 1.52e-5 | [1.19059710, 1.19062756] | 1.490 (1.482) |
| radial h = 1/160 | ⟨r⟩/R | 1.1906124177 | 1.52e-5 | [1.19059722, 1.19062761] | 9.649 (9.648) |
| disparo sin malla | 2R²E₀/π² | 1.1906124213 | 1.56e-9 | (barra solo del modelo de extrapolación) | 1.482 (1.482) |
| disparo sin malla | ⟨r⟩/R | 1.1906124202 | 2.00e-9 | (ídem) | 9.648 (9.648) |

Los diez intervalos contienen la referencia 1.1906124210606 (control K9). **El resultado de la integral de camino es
1.19054 < δ_c < 1.19068 con la receta de la Fase 3 (método A), y 1.190609 < δ_c < 1.190616 aplicando la receta al cruce
(método B).** Con solo cajas R ≤ 800 los intervalos son [1.19055557, 1.19066686] (A) y [1.19060344, 1.19062166] (B). Para
comparar: el signo de E₀ dio 1.19 < δ_c < 1.20 con R hasta 12800 (Fase 3), y la longitud de dispersión a energía cero dio
1.1906 < δ_c < 1.1907.

La barra del método A es grande por cómo escala. Desde R = 800, la barra de la receta en E₀ queda casi constante (en
δ = 1.1906 vale 9.1×10⁻⁹, 1.0×10⁻⁸ y 1.2×10⁻⁸ en R = 800, 1600 y 3200), mientras E₀ cae como R⁻². Al pasar a y se
multiplica por R², y la pendiente que separa las dos curvas solo crece como R; por eso la barra del cruce crece con R en
los pares grandes (tabla 1). Pero ese error es suave en δ y casi no mueve el cruce, que es lo que
mide el método B; la comparación con el disparo (diferencias de 2.4×10⁻⁷ o menos tras restar la pared) indica que A es muy
conservador.

![Figura C](figuras/C_rho_vs_delta.png)

*Figura C. ⟨r⟩/R frente a δ: las curvas se cruzan cerca de 1/2 − 2/π² = 0.2974, con un corrimiento mayor que el de la
energía (α_ρ ≈ 9.65 frente a 1.48).*

![Figura D](figuras/D_colapso.png)

*Figura D. Izquierda: 2R²E₀/π² de 32 valores de δ y 7 cajas (disparo) frente a z = R/a_s(δ), sobre la función de escala de
alcance cero x cot x = z. Derecha: el residuo multiplicado por R colapsa en una sola curva y vale r_e/4 en z = 0: la
corrección es de rango efectivo y de orden 1/R a z fijo.*

**Tabla 3. δ = 1.19: el signo engaña, el cruce no.**

| R | E₀ disparo | E₀ radial 1/160 | E₀ integral de camino | 2R²E₀/π² |
|---|---|---|---|---|
| 50 | +5.0224e-04 | +5.0224e-04 | +5.0012e-04 ± 3.3e-6 | 0.2544 |
| 200 | +2.8797e-05 | +2.8797e-05 | +2.8766e-05 ± 4.8e-8 | 0.2334 |
| 800 | +1.3199e-06 | +1.3199e-06 | +1.3200e-06 ± 1.0e-8 | 0.1712 |
| 1600 | +1.5224e-07 | +1.5223e-07 | +1.5300e-07 ± 1.3e-8 | 0.0790 |
| 3200 | -7.2582e-08 | -7.2582e-08 | -7.1475e-08 ± 1.8e-8 | -0.1506 |

Hasta R = 1600 los tres métodos dan E₀ > 0, que leído por el signo es "no ligado". En cambio y ya está por debajo de 1/4
y baja con R desde el primer par, y todos los cruces medidos (el menor es 1.1906083) están por encima de 1.19: la prueba de
cruce clasifica δ = 1.19 como ligado con las cajas R = 50 y 100. Como controles negativos, con el Yukawa repulsivo, con
δ ∈ [1.4, 2.0] (sin ligado) y con δ ∈ [0.8, 1.0] (ligado profundo), y(R) − y(2R) no cambia de signo en ningún par (K12).
El repulsivo enseña además que "y baja con R" no basta: ahí a > 0 es pequeño, como en una esfera dura, e y baja hacia 1
desde arriba sin acercarse a 1/4.

**Controles** (`controles.md`): pasan 27 de 31. Perron-Frobenius (mínimo +1.2×10⁻⁹), transferencia frente a radial y frente
a disparo (161 de 161 celdas compatibles), sensibilidad a h, ley 1/R², valor en el cruce y controles negativos pasan. No
pasan: el orden de Trotter (75.2 % de las celdas en [1.8, 2.2]; en R = 50 es la pared, y al restarla las 23 celdas vuelven
al rango; en R = 3200 son términos de orden superior en ε = 0.2), la independencia de la interpolación en el disparo para
el par 50/100 de ⟨r⟩/R (PCHIP y el cúbico local se separan 4.6×10⁻⁷; el spline coincide con el cruce sin interpolar) y el
colapso evaluado en la rejilla de δ (el criterio estaba mal planteado: la corrección es 1/R a z fijo, no a δ fijo).

## Discusión

El cruce de cajas responde a lo que pide la guía para la segunda presentación: separa un estado débil de un artefacto con
cajas finitas, sin esperar a que R supere a_s, y con un número exacto (1/4) como referencia. Un artefacto que suma a E₀ un
error suave (malla, Trotter, pared) mueve el cruce en una cantidad que se puede medir y que cae como 1/R²; el caso de la
pared lo muestra cuantitativamente. La teoría de rango efectivo convierte la extrapolación en R en una comprobación: el α
ajustado del radial y del disparo coincide con el de la teoría a 0.6 % o mejor (1.490 y 1.4817 frente a 1.4819; 9.649 y 9.6485 frente a 9.648).

Sobre la originalidad hay que ser honestos (`fuentes.md`). La condición de cuantización es la del método de la pared
esférica; el valor universal de la energía de dos cuerpos en una caja en la unitariedad se usa en redes (caja periódica)
para ajustar acoplamientos, y en una trampa armónica es la fórmula de Busch et al.; el cruce de curvas de dos tamaños es la
renormalización fenomenológica de Nightingale; el escalamiento de tamaño finito del Yukawa se hizo con el tamaño de la base
(Serra, Neirotti y Kais 1998) y, para pozos con ℓ = 1, con un radio de corte del potencial (Serra). Lo que no encontramos es
el uso del cruce en una esfera dura para el apantallamiento crítico del Yukawa, la ley de convergencia con coeficientes
predichos por r_e y c, el punto fijo de la extensión con su coeficiente propio, ni su uso con una integral de camino como
prueba de artefacto.

Límites: la ley depende del signo de r_e (para r_e < 0 los cruces llegarían desde abajo); para ℓ ≥ 1 el estado no se va a
la pared y el punto fijo cambia (extensión E4); la barra de la receta de la Fase 3 es muy conservadora para este uso.

## Referencias

- B. Borasoy, E. Epelbaum, H. Krebs, D. Lee y U.-G. Meißner, *Eur. Phys. J. A* **34**, 185 (2007), arXiv:0708.1780.
- T. Busch, B.-G. Englert, K. Rzażewski y M. Wilkens, *Found. Phys.* **28**, 549 (1998).
- R. R. dos Santos y L. Sneddon, *Phys. Rev. B* **23**, 3541 (1981).
- J. E. Drut y A. N. Nicholson, arXiv:1208.6556, DOI 10.1088/0954-3899/40/4/043101.
- S. König, D. Lee y H.-W. Hammer, *Phys. Rev. Lett.* **107**, 112001 (2011).
- M. Lüscher, *Commun. Math. Phys.* **105**, 153 (1986); *Nucl. Phys. B* **354**, 531 (1991).
- M. P. Nightingale, *Physica A* **83**, 561 (1976).
- P. Serra, J. P. Neirotti y S. Kais, *Phys. Rev. A* **57**, R1481 (1998).
- P. Serra, "A spatial finite size scaling method for calculation of critical parameters for weakly bound states" (PDF en la
  página del autor; revista no identificada).
- I. Stetcu, J. Rotureau, B. R. Barrett y U. van Kolck, arXiv:1001.5071.
- H. A. Bethe, *Phys. Rev.* **76**, 38 (1949) [no verificada en esta búsqueda].


## teoria.md

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


## fuentes.md

# Fuentes de E2 y estado de verificación

Búsqueda hecha el 17-11-2026 con WebSearch y WebFetch. Marcas: **[V]** verificada en la página del editor, en el DOI o en un
índice bibliográfico (Scilit, ADS, OSTI); **[V-arXiv]** verificada solo en arXiv; **[V-web]** verificada solo en la página
del autor; **[no verificada]** citada de memoria o por otra fuente. Para cada una se dice qué se comprobó y qué no.

## Escalamiento de tamaño finito en mecánica cuántica (la comparación principal)

| Referencia | Estado | Qué se comprobó |
|---|---|---|
| P. Serra, J. P. Neirotti y S. Kais, "Finite-size scaling approach for the Schrödinger equation", *Phys. Rev. A* **57**, R1481 (1998) | [V] (PDF en la web del grupo de Kais; Scilit) | El "tamaño" es el número de funciones de base N, **no** una caja espacial ("the finite size corresponds to the number of elements in the truncated basis set"). Ejemplo: Yukawa escalado, λ_c = 0.8399039(1) para ℓ = 0 (es 1/δ_c) y 4.540980(3) para ℓ = 1; exponentes α = 2 y 1. Las curvas D_O(λ; N, N′) se cruzan en el punto crítico. |
| S. Kais y P. Serra, "Quantum critical phenomena and stability of atomic and molecular ions", *Int. Rev. Phys. Chem.* **19**, 97–121 (2000), DOI 10.1080/014423500229873 | [V] (Scilit) | Solo los datos bibliográficos. |
| S. Kais y P. Serra, "Finite-size scaling for atomic and molecular systems", *Adv. Chem. Phys.* **125** (2003) | [V-web] (PDF en la web del grupo; páginas no visibles) | En mecánica cuántica el tamaño es otra vez el de la base; el Yukawa es el ejemplo resuelto (sección IV.C, colapso con N = 20 a 100). La sección VII ("Spatial finite-size scaling") usa un **radio de corte del potencial**; el PDF accesible se corta antes de esa sección. |
| S. Kais, "Finite size scaling for criticality of the Schrödinger equation", arXiv:1009.4393 | [V-arXiv] | Tamaño = dimensión del espacio de la base; no usa una caja espacial. |
| F. H. Alharbi y S. Kais, "Quantum criticality analysis by finite size scaling and exponential basis sets", arXiv:1304.7433 | [V-arXiv] | Tamaño = número de funciones de base; potencial de Hulthén; sin caja. |
| P. Serra, "A spatial finite size scaling method for calculation of critical parameters for weakly bound states" (PDF en famaf.unc.edu.ar/~serra/serra28.pdf) | [V-web] (sin revista ni año en el PDF; la referencia más reciente que cita es de 2002) | **Es el antecedente más cercano que encontramos.** Escala con una longitud R, pero R es un **radio de corte del potencial** (V = 0 para r > R) con condición de Siegert, no una pared dura. Las curvas Γ(R, R+1; λ) se cruzan cerca de λ_c y se extrapola en 1/R. El ejemplo es un pozo cuadrado con ℓ = 1; el método supone un exponente α ≠ 2, así que no se aplica tal cual a la onda s. No menciona el Yukawa ni un punto fijo 1/4. No pudimos identificar dónde se publicó. |
| R. R. dos Santos y L. Sneddon, "Finite-size rescaling transformations", *Phys. Rev. B* **23**, 3541–3546 (1981), DOI 10.1103/PhysRevB.23.3541 | [V] (Scilit) | Teoría de las transformaciones de reescalamiento de tamaño finito; muestra que la renormalización fenomenológica de Nightingale es un caso particular. Es el origen del "cruce de curvas de dos tamaños". |
| M. P. Nightingale, "Scaling theory and finite systems", *Physica A* **83**, 561–572 (1976), DOI 10.1016/0378-4371(75)90021-7 | [V] (Scilit) | Datos bibliográficos; es la renormalización fenomenológica original. |

## Volumen finito y caja con pared

| Referencia | Estado | Qué se comprobó |
|---|---|---|
| M. Lüscher, "Volume dependence of the energy spectrum in massive quantum field theories", *Commun. Math. Phys.* **105**, 153–188 (1986), DOI 10.1007/BF01211097 | [V] (Scilit) | Datos bibliográficos. |
| M. Lüscher, "Two-particle states on a torus and their relation to the scattering matrix", *Nucl. Phys. B* **354**, 531 (1991), DOI 10.1016/0550-3213(91)90366-6 | [V] (ADS) | Resumen: en una caja periódica mayor que el alcance, los niveles de dos partículas los fijan los corrimientos de fase, en las dos direcciones. Es la versión periódica de nuestra ecuación x cot x = R/a. |
| S. König, D. Lee y H.-W. Hammer, "Volume dependence of bound states with angular momentum", *Phys. Rev. Lett.* **107**, 112001 (2011), arXiv:1103.4468 | [V] (OSTI, arXiv) | Caja **periódica**: el ligado s se refuerza en volumen finito y el p se debilita; para ℓ ≥ 2 depende de la representación cúbica. No trata la pared dura ni el umbral. |
| B. Borasoy, E. Epelbaum, H. Krebs, D. Lee y U.-G. Meißner, "Two-particle scattering on the lattice: phase shifts, spin-orbit coupling, and mixing angles", *Eur. Phys. J. A* **34**, 185–196 (2007), arXiv:0708.1780 | [V] (Springer, arXiv) | **Método de la pared esférica**: una pared dura a un radio grande fijo y los corrimientos de fase salen de las energías de las ondas estacionarias. Es exactamente la condición de cuantización de nuestra sección 1 de `teoria.md`; no es nuestra. |
| J. E. Drut y A. N. Nicholson, "Lattice methods for strongly interacting many-body systems", DOI 10.1088/0954-3899/40/4/043101, arXiv:1208.6556 | [V-arXiv] (la revista, J. Phys. G **40** (2013), se deduce del DOI y no se comprobó en el editor) | En redes para el gas de Fermi unitario, el acoplamiento se **ajusta a la unitariedad** haciendo que el espectro de dos cuerpos en la caja periódica coincida con los niveles universales de Lüscher en p cot δ = 0 (primera raíz η² ≈ −0.0959). Es la versión periódica de "y = 1/4 en el umbral". Reduce la originalidad del punto fijo. |
| T. Busch, B.-G. Englert, K. Rzażewski y M. Wilkens, "Two cold atoms in a harmonic trap", *Found. Phys.* **28**, 549–559 (1998), DOI 10.1023/A:1018705520999 | [V] (Springer, solo resumen) | Datos bibliográficos y resumen. La fórmula con funciones Γ y el valor E = ħω/2 en la unitariedad se leyeron en Stetcu et al. (siguiente fila), no en el original. |
| I. Stetcu, J. Rotureau, B. R. Barrett y U. van Kolck, "An effective field theory approach to two trapped particles", arXiv:1001.5071 | [V-arXiv] | Escriben la relación de Busch et al., Γ(3/4 − ε/2)/Γ(1/4 − ε/2) = b/(2a), y su corrección de rango efectivo; en la unitariedad el estado base de la trampa armónica tiene ε = 1/2. Es el análogo en trampa armónica de nuestro punto fijo, incluida la corrección por r_e. |

## Confinamiento esférico de potenciales apantallados

| Referencia | Estado | Qué se comprobó |
|---|---|---|
| A. K. Roy, "Spherical confinement of Coulombic systems inside an impenetrable box: H atom and the Hulthén potential", arXiv:1802.04373 | [V-arXiv] (sin journal-ref en arXiv) | Método pseudoespectral; H y Hulthén dentro de una esfera impenetrable; "radio crítico de la jaula" donde la energía cambia de signo. Mira la caja pequeña que desliga, no el cruce de cajas grandes cerca de un umbral de apantallamiento. |
| A. K. Roy, "Critical parameters and spherical confinement of H atom in screened Coulomb potential", arXiv:1904.11166 | [V-arXiv] (sin journal-ref visible) | Parámetros críticos de Hulthén, Yukawa y ECSC **sin caja** (por cambio de signo de la energía); la parte confinada usa solo el ECSC en δ = 0.02 a 1 y radios de jaula hasta 50. No hay R²E, ni π²/8, ni cruces de cajas. |
| D. Djajaputra y B. R. Cooper, "Hydrogen atom in a spherical well: linear approximation", DOI 10.1088/0143-0807/21/3/309 (la revista, Eur. J. Phys., se deduce del DOI), arXiv:physics/9912031 | [V-arXiv] | H confinado; dependencia asintótica de la energía con el radio. Sin apantallamiento ni umbral. |
| "Sen et al." sobre confinamiento | [no verificada] | No encontramos en esta búsqueda un trabajo de Sen y colaboradores sobre el Yukawa confinado cerca del umbral; no se cita. |

## Rango efectivo y umbral

| Referencia | Estado | Qué se comprobó |
|---|---|---|
| H. A. Bethe, "Theory of the effective range in nuclear scattering", *Phys. Rev.* **76**, 38 (1949) | [no verificada] (referencia estándar, no se abrió) | Se usa la definición r_e = 2∫(ψ₀² − u₀²) dr; la comprobamos numéricamente con el pozo cuadrado (r_e = b en resonancia, `01_teoria.json`). |
| M. Klaus y B. Simon, *Ann. Phys.* **130**, 251 (1980) | [V] en `fase4/propuesta_originalidad/ideas_fase4_y_final.md`; no se volvió a abrir aquí | E ∝ (λ − λ_c)² en onda s, usado solo como contexto. |

## Qué se concluye sobre la originalidad (honesto)

1. **No es original**: la condición de cuantización en la esfera dura (método de la pared esférica, Borasoy et al. 2007), el
   uso de la energía de dos cuerpos en una caja en la unitariedad como valor universal para ajustar un acoplamiento (caja
   periódica, Lüscher y las redes del gas unitario; trampa armónica, Busch et al.), el cruce de curvas de dos tamaños como
   estimador del punto crítico (Nightingale; dos Santos y Sneddon), y el escalamiento de tamaño finito del umbral del
   Yukawa (con el tamaño de la base, Serra, Neirotti y Kais 1998) y con un radio de corte del potencial (Serra, PDF sin
   revista identificada).
2. **No lo encontramos en la búsqueda** (lo que puede ser nuevo, con esa salvedad): usar el cruce de 2R²E₀/π² y de ⟨r⟩/R
   en una **esfera de pared dura** para acotar el **apantallamiento crítico del Yukawa**; la ley δ*(R, 2R) − δ_c =
   π²r_e/(16cR²) + 3π²r_e²/(32cR³), que predice los cruces sin parámetros libres a partir de r_e y c a energía cero; el
   punto fijo 1/2 − 2/π² de la extensión y su coeficiente k₁; y su uso con una integral de camino como prueba de
   "artefacto o estado débil", con el corrimiento de la pared sin imagen incluido en la teoría.
3. La afirmación del documento de ideas ("no encontramos este uso para el Yukawa") se mantiene, pero hay que **matizar**
   "el punto fijo exacto 1/4 no apareció en nuestra búsqueda": su análogo periódico y el de la trampa armónica son
   conocidos y se usan para lo mismo (ubicar la unitariedad), y la ecuación que lo da es la del método de la pared esférica.

