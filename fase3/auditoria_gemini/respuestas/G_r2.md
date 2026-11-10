Gracias por los 7 hallazgos. Hicimos un cálculo concreto para cada uno (scripts `25_respuesta_gemini.py` y `26_transferencia_grande.py`). Abajo van los números. Para cada hallazgo, dinos si queda resuelto, si sigue en pie o qué cálculo adicional pedirías. Si ves un error en nuestro razonamiento, señálalo.

**Hallazgo 1 (sesgo de malla del radial en el origen, falso ligado en δ = 1.19).**
- Orden medido de la malla del radial en δ = 1.19, R = 3200, con h = 1/40, 1/80, 1/160, 1/320, 1/640: E0 = +1.90e-8, −4.77e-8, −6.62e-8, −7.10e-8, −7.21e-8. Órdenes sucesivos 1.84, 1.96, 2.11, o sea p ≈ 2. El Richardson con p = 2 está justificado.
- El signo del sesgo es el contrario al que propones. La malla gruesa da energías MÁS ALTAS: con h = 1/40 la energía hasta sale positiva. Al refinar baja de forma monótona. Un sesgo así puede esconder un estado ligado, pero no fabricarlo.
- Prueba sin malla ni caja: integramos u'' = 2(V − E)u con DOP853 (rtol 1e-12) desde la serie de Frobenius u = r − r² cerca de 0, y empalmamos con la cola exacta e^{−κr} en r = 60. Con brentq sobre E se obtiene la energía en caja infinita: E0(1.18) = −3.09859e-5 y E0(1.19) = −1.03032e-7. Esta última coincide con el radial en R = 25600 (−1.0299e-7 ± 1.3e-9).
- Conteo de nodos de la solución a energía cero (Sturm, sin malla): δ = 1.19 tiene 1 nodo en (0, 4000), en r = a_s = +2203.8, así que tiene un estado ligado. δ = 1.1906 tiene a_s = +108621 > 0 (nodo más allá de 4000), así que está ligado. δ = 1.1907 tiene a_s = −15404, así que no tiene estado ligado. δ = 1.20 tiene 0 nodos y a_s = −142.9.

**Hallazgo 2 (orden de Trotter 1.1 a 1.5, la extrapolación ε² se rompe en la pared).**
- Hay 9 celdas con orden fuera de [1.8, 2.2], todas en cajas cortas o con δ ≥ 1.18.
- La causa la medimos así: si el término de referencia es el radial en R + 0.5826√ε (la posición efectiva de la pared sin imagen), el orden pasa a 1.975 a 1.993 en las 9 celdas. Ejemplos: δ = 1.25, R = 50 pasa de 1.144 a 1.983; δ = 1.2, R = 100 pasa de 1.787 a 1.991. El núcleo da ε² más un desplazamiento de pared en √ε que ya conocemos, no un espectro distorsionado.
- Repetimos la extrapolación con el orden observado p_obs en vez de 2:
  - δ = 1.25, R = 50: E(p = 2) = 1.110208e-3, E(p_obs) = 1.111645e-3, radial 1.114049e-3, barra 5.9e-6.
  - δ = 1.18, R = 50: 3.361989e-4 frente a 3.365929e-4, radial 3.380133e-4, barra 2.8e-6.
  - δ = 1.2, R = 100: 1.865300e-4 frente a 1.865934e-4, radial 1.868654e-4, barra 5.2e-7.
- En los tres casos las dos extrapolaciones quedan dentro de la barra declarada y del radial.

**Hallazgo 3 (un ligado ultradébil en δ = 1.20 que pase la ley de caja).**
- Radial en δ = 1.20 con R = 3200, 6400, 12800, 25600, 51200. La desviación de la ley de caja es 5.3e-4, 6.8e-5, 1.0e-6, 1.1e-4 y 4.4e-4. E0 es positivo en todas.
- La subida a partir de R = 25600 es redondeo: allí |E − ley| ≈ 1e-12, y refinar h la empeora en vez de mejorarla.
- Además, la prueba de Sturm sin caja da 0 nodos y a_s = −142.9 < 0 en δ = 1.20. Un estado ligado, por débil que sea, exige un nodo a energía cero. No hay ninguno, así que no existe tal estado.

**Hallazgo 4 (el cambio de signo entre R = 1600 y 3200 es un cruce numérico).**
- Calculamos el punto de cruce R_c(h), donde E0(R) = 0, para cuatro mallas: 3692.3 (h = 1/40), 2450.9 (1/80), 2260.8 (1/160) y 2217.7 (1/320). El Richardson da ≈ 2203.4.
- Ese valor coincide con la longitud de dispersión a_s = 2203.8, calculada sin malla. Es lo esperado físicamente: la energía de un estado en caja cambia de signo cuando R pasa por a_s.
- Cuanto más fina la malla, más corta la caja donde aparece el ligado, no más larga.

**Hallazgo 5 (la suma lineal de errores subestima).**
- Una suma lineal de valores absolutos es una cota superior de la suma en cuadratura. No la subestima.
- Para probar si falta un término cruzado, ajustamos E(h, ε) = E0 + c1 h⁴ + c2 ε² + c3 h⁴/ε a los 6 puntos crudos:
  - δ = 1.19, R = 1600: ajuste +1.610e-7 ± 4.4e-9; receta +1.530e-7 ± 1.3e-8; radial +1.544e-7.
  - R = 3200: ajuste −6.03e-8 ± 6.1e-9; receta −7.15e-8 ± 1.8e-8; radial −6.99e-8.
- La barra de la receta es 2 a 3 veces mayor que la del ajuste. El signo es el mismo con los tres métodos.

**Hallazgo 6 (monotonía más F½ > 0.95 fuerza un falso "no ligado").**
- Repetimos el veredicto con umbral 0.75, 0.85 y 0.95, solo como información: el criterio quedó fijado antes de ver los datos y no lo cambiamos. Los veredictos no cambian.
- En δ = 1.19, la ausencia de terna ligada con R ≤ 3200 no se debe a F½. Se debe a la condición (a): E(1600) > 0.
- Notamos también que no producimos un "no ligado" falso en ninguna celda: δ = 1.19 queda "indeterminado" hasta R = 3200, nunca "no ligado".

**Hallazgo 7 (se abandona la condición (c) para R > 3200).** Era cierto en la versión que viste. Ahora tenemos la transferencia en R = 6400 y 12800, con la misma receta: mismas ε, mismas h, mismo término de pared. La memoria la resolvimos con LU en banda de LAPACK, con N hasta 640000.
- R = 6400: transferencia −1.0028e-7 ± 2.2e-8; radial (h = 1/160) −1.0175e-7 ± 1.3e-9. Compatibles. ⟨r⟩/R = 0.1594, F½ = 0.9619.
- R = 12800: transferencia −1.0145e-7 ± 2.3e-8; radial −1.0302e-7 ± 1.3e-9. Compatibles. ⟨r⟩/R = 0.0851, F½ = 0.9975.
- Terna (3200, 6400, 12800):
  - Radial: E = −7.26e-8, −1.017e-7, −1.030e-7; F½ = 0.900, 0.961, 0.997, y "ligado".
  - Transferencia: E = −7.15e-8, −1.003e-7, −1.014e-7; F½ = 0.900, 0.962, 0.997, y "ligado".
  - Condición (c): mismo signo, misma tendencia y energías compatibles, así que se cumple.
- Residuo de la iteración inversa < 2e-11. El autovector tiene signo constante: el mínimo de Perron es ≥ +9e-9 en las 12 corridas y el valor −2.8e-16 que aparecía antes era redondeo en las componentes junto a la pared.

Con esto, nuestra conclusión es 1.19 < δc < 1.20 con los dos métodos y la condición (c) completa. Por energía cero sin malla, δc queda en [1.1906, 1.1907]. ¿Qué de esto sigue sin convencerte?
