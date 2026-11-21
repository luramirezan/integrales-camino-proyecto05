# Material para auditoría (parte 2 de 3)

Responde solo "Recibido".

## controles.md

# Controles de E2 (criterio de cruce de cajas)

*Generado por `codigo/07_controles.py` el 2026-11-17 22:12:25 desde los JSON de `resultados/`. Los criterios se fijaron antes de correr la rejilla (`criterios_previos.md`). Pasan 27 de 31 (K11b es informativo y no cuenta).*

| # | Control | Criterio fijado antes | Valor | ¿Pasa? | Script |
|---|---|---|---|---|---|
| K1 | Perron-Frobenius (autovector de signo constante) | min(v)/max\|v\| >= -1e-12 en todas las celdas | mínimo +1.2e-09 en 161 celdas x 6 (h, eps); residuo máximo 8.7e-16 | sí | 04 |
| K2 | Orden de Trotter | 1.8 <= p <= 2.2 en >= 90 % de las celdas | 75.2 % (p entre 1.523 y 2.385); fuera: [(1.185, 50, 1.609), (1.187, 50, 1.593), (1.189, 50, 1.578), (1.19, 50, 1.57), (1.1903, 50, 1.568), (1.1905, 50, 1.566)] ... (Causa medida (scripts 12 y 12b): en R = 50 la pared sin imagen; al restar el corrimiento de la pared medido con el radial, 23 de 23 celdas vuelven a [1.8, 2.2]. En R = 3200 no es la pared: con eps = 0.2 hay términos de orden superior; con la terna (0.1, 0.05, 0.025) el orden en delta = 1.1906 baja de 2.384 a 2.084. La receta solo usa eps = 0.2 en la barra.) | **no pasa** | 04 |
| K3 | Transferencia frente a radial h = 1/40 en cada celda | \|E_tr - E_rad\| <= 2 (err_tr + err_rad) | 161/161 compatibles | sí | 04 |
| K4 | Transferencia frente a disparo sin malla en cada celda | \|E_tr - E_disp\| <= 2 err_tr | 161/161; máximo \|dif\|/err = 0.818; máximo \|dif\|/\|E\| = 2.5e-02 | sí | 02, 04 |
| K5a | Radial 1/40 frente a disparo | \|E_rad - E_disp\| <= 2 err_rad en cada celda | 161/161; máximo \|dif\|/err = 0.126 | sí | 02, 03 |
| K5b | Radial 1/160 frente a disparo | \|E_rad - E_disp\| <= 2 err_rad en cada celda | 161/161; máximo \|dif\|/err = 0.276 | sí | 02, 03 |
| K6-disparo | Valor en el cruce tiende a 1/4 (disparo) | \|y* - 1/4\| < 0.01 en el par mayor; y* decrece con R; (y* - 1/4)/(3 r_e/8R) en [0.8, 1.2] para R >= 200 | y* = 0.26390, 0.25681, 0.25337, 0.25168, 0.25084, 0.25042; cocientes = 1.040, 1.020, 1.010, 1.005, 1.003, 1.001 | sí | 05 |
| K6-radial_h160 | Valor en el cruce tiende a 1/4 (radial_h160) | \|y* - 1/4\| < 0.01 en el par mayor; y* decrece con R; (y* - 1/4)/(3 r_e/8R) en [0.8, 1.2] para R >= 200 | y* = 0.26390, 0.25681, 0.25337, 0.25168, 0.25084, 0.25037; cocientes = 1.040, 1.020, 1.010, 1.006, 1.003, 0.887 | sí | 05 |
| K6-transferencia | Valor en el cruce tiende a 1/4 (transferencia) | \|y* - 1/4\| < 0.01 en el par mayor; y* decrece con R; (y* - 1/4)/(3 r_e/8R) en [0.8, 1.2] para R >= 200 (el criterio de cociente se fijó para disparo y radial; en la transferencia es informativo) | y* = 0.26222, 0.25601, 0.25297, 0.25144, 0.25055, 0.24956; cocientes = 0.915, 0.899, 0.888, 0.860, 0.656, -1.044 | sí | 05 |
| K7-disparo | Independencia de la interpolación (disparo), rejilla final de 23 nodos | máx \|spline - pchip\|, \|spline - local3\| <= 1e-8 | peor caso: rho par 50: 4.6e-07 (46.06 veces el límite) (Causa medida (script 10, V1): el spline coincide con el cruce calculado sin interpolar a 4e-11 o mejor en todos los pares; los que se separan son PCHIP y el cúbico local en el par 50/100 de rho, cuyo cruce (1.1945) cae donde los nodos están a 1e-3. El par 50/100 no entra en la extrapolación.) | **no pasa** | 05 |
| K7-radial_h160 | Independencia de la interpolación (radial_h160), rejilla final de 23 nodos | máx \|spline - pchip\|, \|spline - local3\| <= 0.2 sigma del cruce | peor caso: rho par 50: 4.6e-07 (0.19 veces el límite) | sí | 05 |
| K7-radial_h40 | Independencia de la interpolación (radial_h40), rejilla final de 23 nodos | máx \|spline - pchip\|, \|spline - local3\| <= 0.2 sigma del cruce | peor caso: rho par 50: 4.6e-07 (0.01 veces el límite) | sí | 05 |
| K7-transferencia | Independencia de la interpolación (transferencia), rejilla final de 23 nodos | máx \|spline - pchip\|, \|spline - local3\| <= 0.2 sigma del cruce | peor caso: rho par 50: 2.1e-07 (0.00 veces el límite) | sí | 05 |
| K7-disparo-inicial | Independencia de la interpolación (disparo), rejilla INICIAL de 15 nodos | <= 1e-8 | pares que no cumplen: [('y', 50, 1.4e-07), ('y', 1600, 1.9e-08), ('rho', 50, 3.1e-07), ('rho', 100, 5.8e-07), ('rho', 1600, 2.6e-08)] (Se añadieron 8 nodos; ver K7-disparo.) | **no pasa** | 07 |
| K8a | Sensibilidad a h (transferencia) | \|delta_c(h = 0.02 sola) - delta_c(receta)\| <= barra final (método A) | 2.05e-06 frente a barra 6.66e-05 (h = 0.04 sola: 1.05e-05) | sí | 05 |
| K8b-y | Sensibilidad a h (radial, y) | \|delta_c(1/40) - delta_c(1/160)\| <= barra final del radial 1/160 | 7.33e-06 frente a 1.52e-05 | sí | 05 |
| K8b-rho | Sensibilidad a h (radial, rho) | \|delta_c(1/40) - delta_c(1/160)\| <= barra final del radial 1/160 | 4.21e-06 frente a 1.52e-05 | sí | 05 |
| K9-disparo-y | Intervalo final contiene la referencia (disparo, y) | 1.1906124210606 dentro | [1.1906124198, 1.1906124229]; centro - ref = +2.6e-10 | sí | 05 |
| K9-disparo-rho | Intervalo final contiene la referencia (disparo, rho) | 1.1906124210606 dentro | [1.1906124182, 1.1906124222]; centro - ref = -8.3e-10 | sí | 05 |
| K9-radial_h160-y | Intervalo final contiene la referencia (radial 1/160, y) | 1.1906124210606 dentro | [1.1905971026, 1.1906275626]; centro - ref = -8.8e-08 | sí | 05 |
| K9-radial_h160-rho | Intervalo final contiene la referencia (radial 1/160, rho) | 1.1906124210606 dentro | [1.1905972223, 1.1906276130]; centro - ref = -3.4e-09 | sí | 05 |
| K9-transferencia-y | Intervalo final contiene la referencia (transferencia, método A, y) | 1.1906124210606 dentro | [1.1905440986, 1.1906772338]; centro - ref = -1.8e-06 | sí | 05 |
| K9-transferencia-rho | Intervalo final contiene la referencia (transferencia, método A, rho) | 1.1906124210606 dentro | [1.1905504912, 1.1906712255]; centro - ref = -1.6e-06 | sí | 05 |
| K9-B-y | Intervalo final contiene la referencia (transferencia, método B, y) | 1.1906124210606 dentro | [1.1906085878, 1.1906162112]; centro - ref = -2.2e-08 | sí | 05 |
| K9-B-rho | Intervalo final contiene la referencia (transferencia, método B, rho) | 1.1906124210606 dentro | [1.1905973927, 1.1906267974]; centro - ref = -3.3e-07 | sí | 05 |
| K10-y | Ley 1/R^2 del cruce (disparo, y) | cociente de diferencias sucesivas en [3, 5.5] para R >= 100 | 4.125, 4.062, 4.031, 4.016 | sí | 05 |
| K10-rho | Ley 1/R^2 del cruce (disparo, rho) | cociente de diferencias sucesivas en [3, 5.5] para R >= 100 | 4.039, 4.021, 4.011, 4.005 | sí | 05 |
| K11 | Colapso de datos y = F(R/a_s) (disparo, rejilla principal) | max\|y - F\| < 0.01 para R >= 400 y cociente entre R y 2R en [1.6, 2.5] (ley 1/R) | max\|y - F\| = 50: 9.7e-03, 100: 5.0e-03, 200: 2.5e-03, 400: 2.0e-03, 800: 8.4e-03, 1600: 3.3e-02, 3200: 1.3e-01; cocientes 1.95, 1.97, 1.27, 0.24, 0.25, 0.25 (Causa medida: el criterio se evaluó en la rejilla de delta, donde z = R/a crece con R. La corrección es O(r_e/R) a z fijo (figura D y K11b), pero en el lado ligado vale -z^3 r_e/(pi^2 R) (de q coth q = z + r_e q^2/(2R)); en delta = 1.185 y R = 3200, z = 13.27, la estimación da -0.1315 y lo medido es -0.1327. El criterio estaba mal planteado; no se cambia.) | **no pasa** | 02 |
| K11b | Colapso a z fijo (\|z\| <= 2), informativo | sin criterio previo (añadido después de K11) | max\|y - F\| = 50: 1.0e-02 (n = 32), 100: 5.8e-03 (n = 29), 200: 3.2e-03 (n = 25), 400: 2.0e-03 (n = 23), 800: 6.3e-04 (n = 18), 1600: 7.9e-04 (n = 18), 3200: 1.6e-04 (n = 15); R max\|y - F\| = 0.51, 0.58, 0.65, 0.80, 0.50, 1.26, 0.50 (informativo; no cuenta en el total) | sí | 02 |
| K12 | Controles negativos: sin cruce si nunca liga o si liga profundo | ningún cambio de signo de y(R) - y(2R) | repulsivo [0, 0, 0, 0, 0], no ligado [0, 0, 0, 0, 0], ligado profundo [0, 0, 0, 0, 0] | sí | 06 |
| K13 | Artefacto frente a estado débil (delta = 1.19) | E0 > 0 en R <= 1600 (los tres métodos) y todos los delta* > 1.19 | signo dice no ligado hasta 1600: True; primer E0 < 0 (disparo) en R = 3200; menor delta* = 1.1906083 | sí | 06 |
| K14 | Reproducción de la Fase 3 (adicional, criterio fijado al escribirlo) | E_tr de delta = 1.19 igual al de fase3/resultados/20_cajas.json a 1e-15 | máxima diferencia 0.0e+00 en 6 celdas | sí | 04 |


## verificacion.md

# Verificación de E2

Comprobaciones independientes de los resultados propios (script `codigo/10_verificacion.py`, `resultados/10_verificacion.json`,
salvo que se diga otro) y lo que se encontró al releer el código.

## 1. Segundo método y caso exacto

- **Cruces sin interpolar (V1).** Se recalculó cada cruce del disparo con brentq en δ, evaluando el disparo en cada δ
  pedido (sin rejilla ni spline). La diferencia con el cruce interpolado con spline es de 1.1×10⁻¹¹ o menos en y y de
  4.5×10⁻¹¹ o menos en ⟨r⟩/R, en los seis pares. La interpolación no aporta error visible; el control K7 que no pasa en el
  disparo compara con PCHIP y con el cúbico local, que son menos precisos que el spline en el par 50/100 de ⟨r⟩/R.
- **Teoría frente a cálculo (V1).** El modelo de rango efectivo (sin parámetros libres: a(δ) y r_e(δ) a energía cero) se
  separa del cruce exacto en −5.0×10⁻⁷, −2.9×10⁻⁸, −1.7×10⁻⁹, −1.1×10⁻¹⁰ en y (pares 50 a 400) y en −6.1×10⁻⁶,
  −3.5×10⁻⁷, −2.1×10⁻⁸, −1.3×10⁻⁹ en ⟨r⟩/R. La diferencia baja más rápido que 1/R³, como se espera del término O(R⁻⁴).
- **Caso exacto (01).** Pozo cuadrado de alcance b dentro de la esfera, a fijo: y − F(R/a) baja a la mitad cada vez que b
  se divide por 2 (razones 2.031, 2.015, 2.008, 2.004 en z = 0) y en z = 0 coincide con r_e/(4R) con r_e = b.
- **δ_c por energía cero (V2).** brentq sobre 1/a(δ) da 1.1906124210606, a 1.6×10⁻¹⁵ de la referencia del proyecto.
- **Reproducción de la Fase 3 (K14).** Las seis celdas de δ = 1.19 (R = 50 a 1600) de la transferencia son idénticas, bit
  a bit, a las de `fase3/resultados/20_cajas.json`.
- **Integral de camino frente a disparo, celda a celda (K4).** 161 de 161 celdas dentro de 2 barras; el cociente máximo
  |dif|/barra es 0.818.

## 2. Convergencia y sensibilidad

- **Disparo (V3).** Cambiar r₀ de 10⁻⁷ a 10⁻⁶ mueve y en 6.9×10⁻¹⁴, 1.9×10⁻¹³ y −3.6×10⁻¹⁴ en las tres celdas probadas;
  cambiar la tolerancia de 10⁻¹² a 10⁻¹³ (barra del disparo, script 02) da barras del cruce de 6×10⁻¹⁵ o menos.
- **Radial en la malla (V4).** En δ = 1.1906, R = 800, sin Richardson, la diferencia con el disparo es +2.23×10⁻⁷,
  +5.71×10⁻⁸, +1.43×10⁻⁸, +3.61×10⁻⁹ y +8.56×10⁻¹⁰ para h = 1/40 a 1/640: orden 1.968, 1.992, 1.989 y 2.078.
- **Monotonía de Dirichlet (V5).** E₀(R) decrece con R en todas las celdas de las cuatro fuentes; ninguna violación.
- **Barra Monte Carlo (V6).** En el par 1600/3200 de la transferencia, la desviación del Monte Carlo es 1.70×10⁻⁵ en el
  script 05 y 1.73×10⁻⁵ y 1.67×10⁻⁵ con otras dos semillas (4000 réplicas). La barra final de ese par la fija la
  propagación lineal, que es mayor.
- **Pesos del ajuste en R (V7, decisión E2-04).** Sin pesos, δ_c de la transferencia (y) sería 1.1906091755 en vez de
  1.1906106662, una diferencia de 1.5×10⁻⁶, muy por debajo de la barra (6.7×10⁻⁵). En el radial la diferencia es de 2×10⁻⁹.
- **Orden de Trotter (scripts 12 y 12b).** Las 23 celdas de R = 50 fuera de [1.8, 2.2] vuelven al rango al restar el
  corrimiento de la pared medido con el radial. Las 17 de R = 3200 no cambian al restar la pared; con ε = 0.025 añadido
  (tabla de pares de la cache de la Fase 2), el orden de la terna (0.1, 0.05, 0.025) en δ = 1.1906 es 2.084 frente a 2.384
  con (0.2, 0.1, 0.05): son términos de orden superior en ε = 0.2. En esa celda, el valor extrapolado con (0.05, 0.025)
  difiere del de la receta en 4.7×10⁻³ relativo (dentro de la barra de la receta; ver `12b_trotter_eps0025.json`).
- **Corrimiento de la pared en el cruce (05 frente a 01).** El cruce de la integral de camino (método B) menos el exacto es
  −7.6×10⁻⁵, −1.8×10⁻⁵, −4.2×10⁻⁶, −9.4×10⁻⁷, −2.0×10⁻⁷ y −1.6×10⁻⁷ (pares 50 a 1600), y la teoría de la pared en
  R + c_w predice −8.3×10⁻⁵, −2.0×10⁻⁵, −4.8×10⁻⁶, −1.18×10⁻⁶, −2.9×10⁻⁷ y −7.3×10⁻⁸. Es una comprobación cuantitativa,
  hecha antes de restar nada, de que la diferencia entre la integral de camino y el disparo es la pared sin imagen.

## 3. Lo que se encontró al releer el código

Se releyeron los scripts 01 a 12 completos después de la corrida final. Hallazgos:

1. **`06_artefacto.py` (corregido):** el comentario decía que en el Yukawa repulsivo y(R) < y(2R); el cálculo da lo
   contrario (a > 0 pequeño, y > 1 baja hacia 1). Solo era texto; el control usa el número de cambios de signo y no
   cambia. Corregido también en `teoria.md` (sección 6).
2. **`07_controles.py` (corregido antes de la versión final):** el control K6 de la transferencia aplicaba el criterio del
   cociente, que `criterios_previos.md` fija solo para disparo y radial. Se ajustó el código al criterio escrito antes, no
   al revés. Las barras "|" de los criterios rompían la tabla markdown; ahora se escapan.
3. **`05_cruces.py`:** la variante "transferencia con la pared restada" usa como barra la de la receta menos el término de
   pared; es una variante de sensibilidad y no entra en ningún intervalo final. La extrapolación con R ≤ 800 se calcula
   antes de borrar las réplicas Monte Carlo (en un primer borrador se calculaba después y perdía el Monte Carlo).
4. **`04_transferencia.py`:** dos cadenas de cálculo en segundo plano fallaron al importar `e2comun` (montaje de red). El
   script ahora guarda tras cada celda y solo calcula las que faltan; 05 y 07 exigen las 23 celdas en cada caja.
5. **`e2comun.disparo_E0`:** para ligados profundos con κR grande, el disparo hacia afuera pierde la cola (aparecen nodos
   espurios cerca de R). Solo pasa en los δ añadidos para el colapso (δ = 1.16 con R ≥ 800); esas celdas tienen
   `nodos` > 0, la figura D las excluye y no se usan en ningún cruce. En la rejilla principal todas tienen 0 nodos.
6. **`e2comun.G_escala`:** el caso z = 1 devolvía al principio 1/3 por un error de borrador; se corrigió a 1/4 antes de
   cualquier corrida (u = 1 − r/R da ⟨r⟩/R = 1/4) y `01_teoria.json` lo comprueba (`G1`).

## 4. Cifras del texto

`codigo/11_cifras_texto.py` busca cada cifra de `seccion_articulo.md`, `teoria.md`, `LEEME.md` y este archivo en los JSON
de `resultados/`. Su salida (`resultados/11_cifras_texto_salida.txt`) lista lo que no encuentra; cada caso se revisó a mano
(ver la sección 5).

## 5. Revisión manual de las cifras que el script no encuentra

Ver la última corrida en `resultados/11_cifras_texto_salida.txt`. Las cifras que quedan sin JSON son constantes
matemáticas (π², 0.5826 = −ζ(1/2)/√(2π), que viene de la Fase 2), cifras citadas de la Fase 3 (a_s = 2203.8,
R = 12800, intervalo [1.19, 1.20]), o cocientes y diferencias calculados a mano a partir de cifras que sí están en los JSON;
estos últimos se listan con su origen en la tabla siguiente.


## criterios_previos.md

# Criterios fijados ANTES de correr la rejilla (E2, 17-11-2026, 20:55)

Este archivo se escribió antes de ejecutar los scripts 02 a 07. Los umbrales no se cambian después de ver los datos.
Si un control falla, se reporta como "no pasa" con su causa medida.

| # | Control | Criterio fijado antes |
|---|---|---|
| K1 | Perron-Frobenius | min(v)/max(abs(v)) >= -1e-12 en todos los autovectores de la transferencia |
| K2 | Orden de Trotter | 1.8 <= p_Trotter <= 2.2 en al menos el 90 % de las celdas |
| K3 | Transferencia frente a radial (h = 1/40), cada celda | abs(E_tr - E_rad) <= 2 (err_tr + err_rad) (definición de la Fase 3) |
| K4 | Transferencia frente a disparo sin malla, cada celda | abs(E_tr - E_disp) <= 2 err_tr |
| K5 | Radial (h = 1/40 y 1/160) frente a disparo | abs(E_rad - E_disp) <= 2 err_rad en cada celda |
| K6 | Valor en el cruce | y* = 2R^2E/pi^2 en el cruce del par mayor dentro de 0.01 de 1/4; y* - 1/4 decrece con R; cociente medido/predicho (3 r_e/(8R)) en [0.8, 1.2] para R >= 200 (disparo y radial) |
| K7 | Independencia de la interpolación | máxima diferencia entre spline cúbico, PCHIP y polinomio cúbico local <= 0.2 veces la barra del cruce (transferencia, radial); <= 1e-8 absoluto (disparo) |
| K8 | Sensibilidad a h | delta_c extrapolado con h = 0.02 solo frente a la receta (Richardson h^4): diferencia <= barra final. Radial h = 1/40 frente a 1/160: diferencia <= barra final del radial |
| K9 | Intervalo final | contiene la referencia 1.1906124210606 (cada método y cada observable) |
| K10 | Ley de convergencia | cociente de diferencias sucesivas de delta* entre 3 y 5.5 (ley 1/R^2) para los pares con R >= 100 (disparo) |
| K11 | Colapso de datos | max abs(y - F(R/a_s)) < 0.01 para R >= 400 y baja entre 1.6 y 2.5 veces por duplicación de R (ley 1/R) |
| K12 | Controles negativos | sin cambio de signo de y(R) - y(2R) en un barrido que nunca liga (Yukawa repulsivo; delta en [1.4, 2.0]) ni en uno de ligado profundo (delta en [0.8, 1.0]) |
| K13 | Artefacto frente a estado débil | delta = 1.19: E0 > 0 en todas las cajas R <= 1600 (radial y transferencia) y delta*(R, 2R) > 1.19 en todos los pares |

Error del cruce: Monte Carlo con semilla fija (20240 réplicas gaussianas independientes por celda con sigma = barra de la receta) y,
como cota conservadora, propagación lineal con la derivada (|sigma_y(R)| + |sigma_y(2R)|)/|d(y_R - y_2R)/d delta|. La barra que se
reporta es la mayor de las dos. Extrapolación en R: delta*(R) = delta_c + alpha/R^2 + beta/R^3 (la forma la fija la teoría, teoria.md),
con los pares de R >= 100; la diferencia con el ajuste sin beta (solo los dos pares mayores) se suma a la barra.

Añadido a las 21:05, todavía antes de correr la rejilla (después de una sola celda de prueba, delta = 1.1906, R = 200 y 800,
que mostró que la barra de la receta de la Fase 3 es unas 700 veces mayor que la diferencia con el disparo sin malla):

- **Método A (el que da el intervalo final de la transferencia):** la receta de la Fase 3 se aplica a E0 en cada celda; las barras
  se propagan al cruce como se dijo arriba.
- **Método B (complemento, no sustituye a A):** la misma receta se aplica al cruce: se calcula delta* con cada una de las seis
  combinaciones crudas (h, eps), y después delta*_mejor = Richardson h^4 + extrapolación eps^2, con barra
  |delta*_h0.02 - delta*_mejor| + |delta*_mejor - delta*_gruesa| + |corrimiento por la pared|. Mide cuánto se mueve el cruce, que
  es lo que importa, en vez de cuánto se mueve E0.
- Para el radial se usan dos mallas: h = 1/40 (la de radial_ref, igual que la Fase 3) y h = 1/160. El intervalo final del radial
  es el de h = 1/160.

Añadido a las 21:20, después del primer análisis con R <= 800 en la transferencia y antes de tener la transferencia en
R = 1600 y 3200:

- K7 no pasaba para el disparo con la rejilla inicial (diferencias de 1.4e-7, 5.7e-7 y 1.9e-8 entre interpolaciones en los
  pares 50/100, 100/200 de rho y 1600/3200 de y). Se añaden 8 nodos (1.19061, 1.19062, 1.19063, 1.19065, 1.1911, 1.1914,
  1.1916, 1.195). El umbral de K7 no se cambia; en controles.md se reporta también el resultado con la rejilla inicial.
- La extrapolación en R con barras (transferencia, radial) se hace con mínimos cuadrados PONDERADOS (peso 1/sigma), porque la
  barra de la receta crece con R en los pares grandes. Para el disparo, sin barras, el ajuste no se pondera.
- El disparo no tenía barra numérica propia; se le añade la diferencia entre rtol = 1e-12 y rtol = 1e-13 (script 02).


## codigo/05_cruces.py

```python
"""05_cruces.py -- cruces delta*(R, 2R) de y = 2R^2E0/pi^2 y de rho = <r>/R, propagacion de errores y extrapolacion en R.

Fuentes: disparo sin malla (02), radial h = 1/40 y h = 1/160 (03), integral de camino (transferencia, 04).
Interpolacion en delta de D(delta) = X(delta, R) - X(delta, 2R) sobre los 15 nodos de la rejilla:
  - "spline": spline cubico not-a-knot (metodo principal: suave, lineal en los datos, error O(h^4));
  - "pchip": interpolante monotono por tramos (no lineal, sin oscilaciones);
  - "local3": polinomio cubico por los 4 nodos mas cercanos al cambio de signo.
Errores del cruce (fijados en criterios_previos.md): (i) Monte Carlo con semilla fija, N = 20240 replicas
gaussianas independientes por celda; la misma replica de una celda se usa en los dos pares donde aparece, asi que
la correlacion entre cruces vecinos se conserva; (ii) propagacion lineal conservadora
(|sigma(R)| + |sigma(2R)|)/|D'(delta*)|. La barra es la mayor de las dos.
Transferencia, metodo B: la receta de la Fase 3 aplicada al cruce (se cruza con cada (h, eps) crudo y se extrapola).
Extrapolacion en R (forma fijada por teoria.md): delta*(R) = delta_c + alpha/R^2 + beta/R^3, pares con R >= 100;
se compara con Richardson de los dos pares mayores (solo 1/R^2) y la diferencia se suma a la barra.
Salida: resultados/05_cruces.json
"""
import sys, time
import numpy as np
from scipy.interpolate import CubicSpline, PchipInterpolator
from scipy.optimize import brentq
import e2comun as c

sys.stdout = c.Tee("05_cruces")
T0 = time.perf_counter()
NREP = 20240
SEMILLA = 20261117
DEL = np.array(c.DELTAS)
TEO = c.cargar("01_teoria")


# --------------------------------------------------------------------------- carga de datos
def cargar_fuentes():
    F = {}
    dis = c.cargar("02_disparo")
    Rs = [R for R in c.RS]
    F["disparo"] = dict(Rs=Rs,
                        y=np.array([[dis["celdas"][f"{d:g}"][f"R{R}"]["y"] for R in Rs] for d in DEL]),
                        rho=np.array([[dis["celdas"][f"{d:g}"][f"R{R}"]["r_sobre_R"] for R in Rs] for d in DEL]))
    F["disparo"]["sy"] = np.array([[dis["celdas"][f"{d:g}"][f"R{R}"]["err_y"] for R in Rs] for d in DEL])
    F["disparo"]["srho"] = np.array([[dis["celdas"][f"{d:g}"][f"R{R}"]["err_r"] for R in Rs] for d in DEL])
    rad = c.cargar("03_radial")
    for nm in ("h40", "h160"):
        C = rad["celdas"][nm]
        F["radial_" + nm] = dict(
            Rs=Rs,
            y=np.array([[C[f"{d:g}"][f"R{R}"]["y"] for R in Rs] for d in DEL]),
            sy=np.array([[C[f"{d:g}"][f"R{R}"]["err_y"] for R in Rs] for d in DEL]),
            rho=np.array([[C[f"{d:g}"][f"R{R}"]["r_sobre_R"] for R in Rs] for d in DEL]),
            srho=np.array([[C[f"{d:g}"][f"R{R}"]["err_r"] for R in Rs] for d in DEL]))
    Rt = []
    T = {}
    for R in c.RS:
        try:
            x = c.cargar(f"04_transferencia_R{R}")["celdas"]
        except FileNotFoundError:
            continue
        if all(f"{d:g}" in x for d in DEL) and (not Rt or R == 2 * Rt[-1]):
            T[R] = x; Rt.append(R)
    g = lambda fn: np.array([[fn(T[R][f"{d:g}"], R) for R in Rt] for d in DEL])
    tr = dict(Rs=Rt,
              y=g(lambda x, R: c.y_de(x["E_mejor"], R)), sy=g(lambda x, R: c.y_de(x["err"], R)),
              rho=g(lambda x, R: x["obs"]["r_sobre_R"]["mejor"]), srho=g(lambda x, R: x["obs"]["r_sobre_R"]["err"]),
              pared_y=g(lambda x, R: c.y_de(x["sesgo_pared_extrapolado"], R)),
              E=g(lambda x, R: x["E_mejor"]), sE=g(lambda x, R: x["err"]))
    tr["crudo_y"] = {k: g(lambda x, R, k=k: c.y_de(x["crudo"][k]["E0"], R)) for k in T[Rt[0]]["1.19"]["crudo"]}
    tr["crudo_rho"] = {k: g(lambda x, R, k=k: x["crudo"][k]["r_sobre_R"]) for k in T[Rt[0]]["1.19"]["crudo"]}
    F["transferencia"] = tr
    # variante de sensibilidad: pared restada del valor central (NO es la receta; decision 5 deja la pared en el error)
    F["transferencia_pared_restada"] = dict(Rs=Rt, y=tr["y"] - tr["pared_y"], sy=tr["sy"] - np.abs(tr["pared_y"]),
                                            rho=tr["rho"], srho=tr["srho"])
    return F


# --------------------------------------------------------------------------- interpolacion y raiz
def raiz(D, metodo, guia=None):
    """Cruce: raiz de D(delta) interpolado. Si hay varias, la mas cercana a 'guia' (o al primer cambio de signo
    de los nodos contando desde el lado ligado)."""
    s = np.sign(D)
    idx = np.nonzero(s[1:] != s[:-1])[0]
    if len(idx) == 0:
        return np.nan, 0
    if guia is None:
        i = idx[0]
    else:
        i = idx[np.argmin(np.abs(DEL[idx] - guia))]
    if metodo == "spline":
        f = CubicSpline(DEL, D)
    elif metodo == "pchip":
        f = PchipInterpolator(DEL, D)
    elif metodo == "local3":
        j0 = int(np.clip(i - 1, 0, len(DEL) - 4))
        p = np.polyfit(DEL[j0:j0 + 4] - DEL[i], D[j0:j0 + 4], 3)
        f = lambda x: np.polyval(p, x - DEL[i])
    elif metodo == "lineal":
        return float(DEL[i] - D[i] * (DEL[i + 1] - DEL[i]) / (D[i + 1] - D[i])), len(idx)
    r = brentq(lambda x: float(f(x)), DEL[i], DEL[i + 1], xtol=1e-14)
    return float(r), len(idx)


def deriv_spline(D, x):
    return float(CubicSpline(DEL, D)(x, 1))


def interp_spline(v, x):
    return float(CubicSpline(DEL, v)(x))


def cruces_fuente(Fu, obs, rng_rep=None, con_mc=True):
    """Para cada par (R, 2R) de la fuente: cruce con tres interpolaciones, valor en el cruce, barras MC y lineal."""
    Rs = Fu["Rs"]
    X, S = Fu[obs], Fu["s" + obs]
    pares = [(i, i + 1) for i in range(len(Rs) - 1) if Rs[i + 1] == 2 * Rs[i]]
    res = []
    # replicas MC: una por celda, compartida entre pares
    if con_mc and np.any(S > 0):
        rng = np.random.default_rng(SEMILLA)
        ruido = rng.standard_normal((NREP,) + X.shape)
        Xr = X[None, :, :] + S[None, :, :] * ruido
    else:
        Xr = None
    for (i, j) in pares:
        D = X[:, i] - X[:, j]
        d = {m: raiz(D, m) for m in ("spline", "pchip", "local3", "lineal")}
        ds = d["spline"][0]
        fila = dict(R=Rs[i], R2=Rs[j], delta=ds, n_cambios_signo=d["spline"][1],
                    delta_pchip=d["pchip"][0], delta_local3=d["local3"][0], delta_lineal=d["lineal"][0],
                    dif_interp=float(max(abs(d["pchip"][0] - ds), abs(d["local3"][0] - ds))),
                    valor=interp_spline(X[:, j], ds), valor_R=interp_spline(X[:, i], ds),
                    pendiente=deriv_spline(D, ds))
        if Xr is not None:
            sR, s2R = interp_spline(S[:, i], ds), interp_spline(S[:, j], ds)
            fila["sigma_lineal"] = float((abs(sR) + abs(s2R)) / abs(fila["pendiente"]))
            Dr = Xr[:, :, i] - Xr[:, :, j]                      # (NREP, ndelta)
            w = max(8.0 * fila["sigma_lineal"], 5e-5)
            xf = np.linspace(max(DEL[0], ds - w), min(DEL[-1], ds + w), 1601)
            reps = np.full(NREP, np.nan)
            for k0 in range(0, NREP, 2530):                      # por bloques, para no llenar la memoria
                vf = CubicSpline(DEL, Dr[k0:k0 + 2530].T, axis=0)(xf)   # (nfino, bloque)
                cambio = np.sign(vf[1:]) != np.sign(vf[:-1])
                for kk in range(vf.shape[1]):
                    ii = np.nonzero(cambio[:, kk])[0]
                    if len(ii) == 0:
                        continue
                    m = ii[np.argmin(np.abs(xf[ii] - ds))]
                    reps[k0 + kk] = xf[m] - vf[m, kk] * (xf[m + 1] - xf[m]) / (vf[m + 1, kk] - vf[m, kk])
            ok = np.isfinite(reps)
            fila["mc_validas"] = int(ok.sum())
            fila["sigma_mc"] = float(np.std(reps[ok]))
            fila["mc_p16_p84"] = [float(np.percentile(reps[ok], 16)), float(np.percentile(reps[ok], 84))]
            fila["sigma"] = float(max(fila["sigma_mc"], fila["sigma_lineal"]))
            fila["_reps"] = reps
        else:
            fila["sigma_lineal"] = fila["sigma_mc"] = fila["sigma"] = 0.0
        res.append(fila)
    return res


# --------------------------------------------------------------------------- extrapolacion en R
def ajuste(Rs, ds, w=None, beta=True):
    Rs = np.asarray(Rs, float); ds = np.asarray(ds, float)
    A = np.column_stack([np.ones_like(Rs), Rs**-2] + ([Rs**-3] if beta else []))
    W = np.ones_like(Rs) if w is None else np.asarray(w, float)
    coef, *_ = np.linalg.lstsq(A * W[:, None], ds * W, rcond=None)
    # pesos lineales del valor extrapolado: delta_c = sum_i L_i ds_i
    L = np.linalg.pinv(A * W[:, None])[0] * W
    return coef, L


def extrapolar(filas, Rmin=100, con_mc=True, ponderado=True, Rmax=10**9):
    usa = [f for f in filas if Rmin <= f["R"] <= Rmax and np.isfinite(f["delta"])]
    Rs = [f["R"] for f in usa]; ds = [f["delta"] for f in usa]; sg = [f["sigma"] for f in usa]
    out = dict(R_usados=Rs)
    w = 1.0 / np.asarray(sg) if (ponderado and all(x > 0 for x in sg)) else None
    out["ponderado"] = w is not None
    coef, L = ajuste(Rs, ds, w=w, beta=True)
    out["ajuste_ab"] = dict(delta_c=float(coef[0]), alpha=float(coef[1]), beta=float(coef[2]),
                            sigma_lineal=float(np.sum(np.abs(L) * np.asarray(sg))))
    # Richardson con los dos pares mayores (solo 1/R^2)
    f1, f2 = usa[-2], usa[-1]
    rich = (4 * f2["delta"] - f1["delta"]) / 3
    out["richardson_2_mayores"] = dict(delta_c=float(rich), sigma_lineal=float((4 * f2["sigma"] + f1["sigma"]) / 3))
    # ajuste a + alpha/R^2 con los tres pares mayores (otra variante de modelo)
    if len(usa) >= 3:
        coef3, L3 = ajuste(Rs[-3:], ds[-3:], beta=False)
        out["ajuste_a_3_mayores"] = dict(delta_c=float(coef3[0]), alpha=float(coef3[1]))
    out["sistematico_modelo"] = float(abs(out["ajuste_ab"]["delta_c"] - rich))
    if con_mc and all("_reps" in f for f in usa):
        R = np.array([f["_reps"] for f in usa])           # (npares, NREP)
        ok = np.all(np.isfinite(R), axis=0)
        dcr = L @ R[:, ok]
        out["ajuste_ab"]["sigma_mc"] = float(np.std(dcr))
    s_est = max(out["ajuste_ab"].get("sigma_mc", 0.0), out["ajuste_ab"]["sigma_lineal"])
    out["sigma_estadistica"] = float(s_est)
    out["barra_total"] = float(s_est + out["sistematico_modelo"])
    dc = out["ajuste_ab"]["delta_c"]
    out["intervalo"] = [float(dc - out["barra_total"]), float(dc + out["barra_total"])]
    out["contiene_referencia"] = bool(out["intervalo"][0] <= c.DELTA_C_REF <= out["intervalo"][1])
    out["dif_referencia"] = float(dc - c.DELTA_C_REF)
    out["razones_dif_sucesivas"] = [float((filas[k]["delta"] - filas[k + 1]["delta"]) /
                                          (filas[k + 1]["delta"] - filas[k + 2]["delta"]))
                                    for k in range(len(filas) - 2)]
    return out


# --------------------------------------------------------------------------- metodo B (transferencia)
def metodo_B(tr, obs):
    Rs = tr["Rs"]
    cr = tr["crudo_" + obs]
    pares = [(i, i + 1) for i in range(len(Rs) - 1) if Rs[i + 1] == 2 * Rs[i]]
    filas = []
    for (i, j) in pares:
        dd = {}
        for k, X in cr.items():
            dd[k] = raiz(X[:, i] - X[:, j], "spline")[0]
        g = lambda h, e: dd[f"h{h:g}_eps{e:g}"]
        if obs == "y":
            hR = {e: (16 * g(0.02, e) - g(0.04, e)) / 15 for e in (0.2, 0.1, 0.05)}
            best = c.comun3.ext_eps(hR[0.1], hR[0.05]); grues = c.comun3.ext_eps(hR[0.2], hR[0.1])
            h002 = c.comun3.ext_eps(g(0.02, 0.1), g(0.02, 0.05))
            Xc = tr["y"]; P = tr["pared_y"]
            d_sin = raiz((Xc - P)[:, i] - (Xc - P)[:, j], "spline")[0]
            d_con = raiz(Xc[:, i] - Xc[:, j], "spline")[0]
            pared = abs(d_con - d_sin)
            err = abs(h002 - best) + abs(best - grues) + pared
            filas.append(dict(R=Rs[i], R2=Rs[j], delta=float(best), sigma=float(err), err_malla=float(abs(h002 - best)),
                              err_trotter=float(abs(best - grues)), err_pared=float(pared), crudos=dd,
                              delta_pared_restada=float(best - (d_con - d_sin))))
        else:
            best = c.comun3.ext_eps(g(0.02, 0.1), g(0.02, 0.05))
            e_h = abs(best - c.comun3.ext_eps(g(0.04, 0.1), g(0.04, 0.05)))
            e_t = abs(best - c.comun3.ext_eps(g(0.02, 0.2), g(0.02, 0.1)))
            filas.append(dict(R=Rs[i], R2=Rs[j], delta=float(best), sigma=float(e_h + e_t), err_malla=float(e_h),
                              err_trotter=float(e_t), crudos=dd))
    return filas


# --------------------------------------------------------------------------- principal
F = cargar_fuentes()
out = dict(script="05_cruces.py", fecha=c.ahora(), NREP=NREP, semilla=SEMILLA, deltas=list(c.DELTAS),
           referencia=c.DELTA_C_REF, R_transferencia=F["transferencia"]["Rs"], fuentes={})
pred = {f["R"]: f for f in TEO["modelo_ERE"]}
for nombre in ("disparo", "radial_h40", "radial_h160", "transferencia", "transferencia_pared_restada"):
    Fu = F[nombre]
    out["fuentes"][nombre] = {}
    for obs in ("y", "rho"):
        if nombre == "transferencia_pared_restada" and obs == "rho":
            continue
        filas = cruces_fuente(Fu, obs)
        ex = extrapolar(filas, ponderado=(nombre != "disparo"))
        # variante: solo cajas R <= 800 (pares hasta 400/800), para comparar con lo que da la caja pequena
        ex800 = extrapolar(filas, con_mc=(nombre != "disparo"), ponderado=(nombre != "disparo"), Rmax=400)
        for f in filas:
            f.pop("_reps", None)
            p = pred.get(f["R"])
            if p is not None:
                f["prediccion_ERE"] = p["delta_y" if obs == "y" else "delta_rho"]
        out["fuentes"][nombre][obs] = dict(pares=filas, extrapolacion=ex, extrapolacion_R_hasta_800=ex800)
        print(f"== {nombre} / {obs}")
        for f in filas:
            print(f"   {f['R']:>5}/{f['R2']:<5} delta*={f['delta']:.9f} +- {f['sigma']:.2e} (MC {f['sigma_mc']:.1e}, "
                  f"lin {f['sigma_lineal']:.1e})  valor={f['valor']:.6f}  dif_interp={f['dif_interp']:.1e}  "
                  f"ERE={f.get('prediccion_ERE', float('nan')):.9f}  ncambios={f['n_cambios_signo']}")
        e = ex
        print(f"   ajuste a+b/R^2+c/R^3: delta_c={e['ajuste_ab']['delta_c']:.10f} alpha={e['ajuste_ab']['alpha']:.4f} "
              f"beta={e['ajuste_ab']['beta']:.3f} | Richardson={e['richardson_2_mayores']['delta_c']:.10f} | "
              f"barra={e['barra_total']:.2e} -> [{e['intervalo'][0]:.9f}, {e['intervalo'][1]:.9f}] contiene ref: "
              f"{e['contiene_referencia']}  razones={['%.2f' % r for r in e['razones_dif_sucesivas']]}", flush=True)

# metodo B
out["transferencia_metodo_B"] = {}
for obs in ("y", "rho"):
    filas = metodo_B(F["transferencia"], obs)
    ex = extrapolar(filas, con_mc=False)
    ex800 = extrapolar(filas, con_mc=False, Rmax=400)
    out["transferencia_metodo_B"][obs] = dict(pares=filas, extrapolacion=ex, extrapolacion_R_hasta_800=ex800)
    print(f"== transferencia metodo B / {obs}")
    for f in filas:
        print(f"   {f['R']:>5}/{f['R2']:<5} delta*={f['delta']:.9f} +- {f['sigma']:.2e} (malla {f['err_malla']:.1e}, "
              f"Trotter {f['err_trotter']:.1e}, pared {f.get('err_pared', 0):.1e})")
    print(f"   delta_c={ex['ajuste_ab']['delta_c']:.10f}  barra={ex['barra_total']:.2e} -> [{ex['intervalo'][0]:.9f}, "
          f"{ex['intervalo'][1]:.9f}] contiene ref: {ex['contiene_referencia']}", flush=True)

# sensibilidad a h de la transferencia: cruce y extrapolacion usando solo h = 0.02 (eps extrapolado), sin Richardson h^4
tr = F["transferencia"]
sens = {}
for hh in (0.02, 0.04):
    Xh = c.comun3.ext_eps(tr["crudo_y"][f"h{hh:g}_eps0.1"], tr["crudo_y"][f"h{hh:g}_eps0.05"])
    Fu = dict(Rs=tr["Rs"], y=Xh, sy=tr["sy"])
    fil = cruces_fuente(Fu, "y", con_mc=False)
    ex = extrapolar(fil, con_mc=False)
    sens[f"h{hh:g}"] = dict(cruces=[f["delta"] for f in fil], delta_c=ex["ajuste_ab"]["delta_c"])
    print(f"sensibilidad h={hh}: cruces {['%.9f' % f['delta'] for f in fil]} delta_c={ex['ajuste_ab']['delta_c']:.10f}")
out["sensibilidad_h_transferencia"] = sens
out["tiempo_s"] = time.perf_counter() - T0
c.guardar("05_cruces", out)
print(f"tiempo {out['tiempo_s']:.0f} s")

```
