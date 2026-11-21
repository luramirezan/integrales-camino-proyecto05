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
