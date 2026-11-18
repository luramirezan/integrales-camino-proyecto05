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
