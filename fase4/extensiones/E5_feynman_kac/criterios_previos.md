# Criterios fijados ANTES de correr los Monte Carlo (E5, 17-11-2026)

Este archivo se escribió antes de ejecutar los scripts de Monte Carlo (02 a 04; la numeración final de los scripts quedó 01 a 06). Los criterios no se cambian después de ver los datos.
Si un control no pasa, se reporta como "no pasa" con su causa medida.

| # | Control | Criterio fijado antes |
|---|---|---|
| C1 | Dos métodos deterministas de a(δ) (disparo lineal DOP853 y fase variable de Calogero) | diferencia relativa < 1e-8 en los 7 valores de δ |
| C2 | a(1.20) frente a la Fase 3 (−142.9, `comun3.long_dispersion`) | coincide a 4 cifras (|Δa| < 0.05) |
| C3 | Perfil φ(r): disparo frente a Nyström de la ecuación integral | diferencia máxima < 1e-5 en r ≤ 10 |
| C4 | Identidad del estimador de a: −(2/δ²) E_{r∼Γ(2,1/δ)}[φ(r)] = a (cuadratura) | diferencia relativa < 1e-8 |
| C5 | Máquina de pesos de la mezcla de exponenciales frente al caso exacto de Ciesielski y Taylor (pozo cuadrado, tiempo de estancia en la bola unidad) | p_k y w_k de k = 1..5 con error relativo < 1e-6 |
| C6 | p_1 = δ/δ_c(1s) y p_2 = δ/δ_c(2s) medidos por el cero de la pendiente α(p) | error relativo < 1e-7 frente a δ_c(1s) = 1.1906124 y δ_c(2s) = 0.3102093 |
| C7 | MC libre en δ = 3 y 4, valor extrapolado a η → 0, frente a la EDO: φ(r) en la rejilla y a | |MC − EDO| < 3σ (σ = estadística más la incertidumbre de la extrapolación) |
| C8 | Sesgo de discretización: orden observado en η | entre 1.5 y 2.5 (esperado 2) con el trapecio simple |
| C9 | θ medido (estimador de máxima verosimilitud de la cola exponencial de Λ = ln W en el 1 % superior) frente a δ/δ_c, para δ = 1.5, 2, 3, 4 | |θ̂ − δ/δ_c| < 3σ_θ |
| C10 | Ley completa de Λ: supervivencia MC frente a Σ_k w̄_k e^{−p_k λ} | estadístico de Kolmogorov–Smirnov √N·D < 1.63 (nivel 1 %) en δ = 3 y 4 con el η más fino; en 1.5 y 2 se informa |
| C11 | Varianza muestral que crece con n en δ = 1.5 y 2 | pendiente log-log (mediana de 20 réplicas) dentro de ±0.15 de 2/θ − 1; en δ = 3 y 4 pendiente compatible con 0 (|pendiente| < 0.1) |
| C12 | Muestreo por importancia (φ_T = solución de energía cero en δ_T < δ): pesos acotados por 1 | max(peso) ≤ 1 exactamente (se verifica en todas las trayectorias) |
| C13 | MI: a_MI frente a la EDO en δ = 3, 1.5, 1.3, 1.25, 1.2 | |a_MI − a_EDO| < 3σ (σ estadística más el sesgo medido en η) |
| C14 | MI: varianza relativa medida frente a la cota φ_T/φ − 1 (promediada en la distribución de partida) | medida ≤ cota (más 3σ de la estimación de la varianza) |
| C15 | MI: varianza estable con n (sin colas) | pendiente log-log de la varianza muestral |pendiente| < 0.1 |

Regla para δ_T (fijada antes): 1/a_T = 0.8/a, es decir δ_T se elige para que a_T = 1.25 a (más cerca del umbral que δ).
Esto da una cota de varianza relativa del orden de 0.25 cerca del origen.

## Adenda (17-11-2026, escrita después de pruebas preliminares y ANTES de correr 02, 03 y 04)

Durante el desarrollo del simulador se hicieron pruebas cortas en δ = 3 (no forman parte de los resultados). Lo que se
vio, y cómo cambia la lista de controles:

1. **El trapecio simple no sirve.** Con dt (q(r) + q(r'))/2, el extremo r' puede caer muy cerca del origen y q(r') dt
   explota; en las pruebas, a(δ = 3) salió del orden de −10^{37} y −10^{239} con η = 0.4 y 0.8. Se demuestra en
   `teoria.md` que la media del estimador discretizado es infinita para todo η > 0. El control C8, como estaba escrito
   (orden de η con el trapecio), queda **no aplicable**, y se informa así. Se cambió el esquema: la integral de q en
   cada paso es la media exacta sobre el puente browniano 3D (Yukawa promediado sobre una gaussiana, forma cerrada).
2. **C8b (nuevo).** Con el esquema de puente, el único sesgo es la desigualdad de Jensen E[e^I] ≥ e^{E[I]} paso a
   paso, que el argumento de `teoria.md` da de orden η^4. Las pruebas preliminares (η = 0.4, 0.2, 0.1, con partidas
   comunes) ya sugerían un orden mayor que 2. Criterio: orden observado entre 3 y 5. **Este criterio se fijó después de
   ver esa prueba preliminar**, y se dice así.
3. **C16 (nuevo).** E[Λ] es exactamente insesgado con el esquema de puente (transición exacta y media exacta del
   puente; solo quedan la cuadratura de 3 nodos y el corte en R_in). Criterio: |E_MC[δΛ] − 1| < 3σ para todos los η
   (con la partida Γ(2, 1/δ), E[Λ] = 1/δ exactamente).
4. **C10 (precisión).** La serie de la mezcla con 14 polos suma 0.99742; para no confundir el truncamiento con un
   desacuerdo, el estadístico de Kolmogorov–Smirnov se calcula para x = δΛ ≥ x_min, con x_min el menor valor en que el
   término despreciado de la serie es < 1e-4 (se calcula en el script desde la teoría, antes de mirar la muestra).
5. **Escala exacta.** Con dt = η² r², R_in = 36/δ y partida Γ(2, 1/δ), el esquema es covariante: δΛ tiene la misma
   ley para todo δ, camino a camino con la misma semilla (comprobado). Una sola muestra de X = δΛ da W = e^{X/δ}
   para todos los δ. Por eso θ̂(δ) = δ κ̂ con un único κ̂ (tasa de la cola de X); los C9 de distintos δ no son
   independientes. Se añade un control independiente de la partida (C9b): una corrida con partida fija r0 = 1 en
   δ = 1.5, con su propio θ̂; criterio |θ̂ − δ/δ_c| < 3σ.
