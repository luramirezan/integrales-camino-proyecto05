# 24. Tabla de controles de la Fase 3

Fecha: 10-11-2026. Generada por `fase3/codigo/24_tabla_controles.py` desde los JSON de los scripts 20 a 26; ninguna cifra está escrita a mano. **Estado: SIN FIRMAR.** En la Fase 3 verifica Luis Felipe Ramírez (rotación de roles 9.12).

**Resumen:** 40 controles distintos (sin filas repetidas): **28 pasan**, **3 no pasan**, 9 medidos.

| # | Control | Criterio | Valor | ¿Pasa? | Script |
|---|---|---|---|---|---|
| A1 | Transferencia frente a radial en cada caja (5 δ × 7 R) | \|E_tr − E_rad\| ≤ 2(err_tr + err_rad) (Fase 2, 14) | 35/35 compatibles; máx \|dif\| = 3.8e-06 | sí | `20_cajas_fase3.py` |
| A2 | Perron-Frobenius: autovector de signo constante (35 celdas × 6) | min v/max\|v\| ≥ −1e-8 | -2.8e-16 | sí | `20_cajas_fase3.py` |
| A3 | Veredicto del criterio 9.6 + (c) en δ = 1.15 | ligado (δ_c ref = 1.19061; umbral ley de caja 0.1 fijado antes) | ligado (terna [50, 100, 200]) | sí | `20_cajas_fase3.py` |
| A4 | Veredicto del criterio 9.6 + (c) en δ = 1.18 | ligado (δ_c ref = 1.19061; umbral ley de caja 0.1 fijado antes) | ligado (terna [200, 400, 800]) | sí | `20_cajas_fase3.py` |
| A5 | Veredicto del criterio 9.6 + (c) en δ = 1.2 | no ligado (δ_c ref = 1.19061; umbral ley de caja 0.1 fijado antes) | no ligado (terna [200, 400, 800]) | sí | `20_cajas_fase3.py` |
| A6 | Veredicto del criterio 9.6 + (c) en δ = 1.25 | no ligado (δ_c ref = 1.19061; umbral ley de caja 0.1 fijado antes) | no ligado (terna [50, 100, 200]) | sí | `20_cajas_fase3.py` |
| A7 | Veredicto en δ = 1.19 con R ≤ 3200 | medido (a 6e-4 del umbral; a_s = +2204) | indeterminado; E0 cambia de signo entre R = 1600 y 3200 | medido | `20_cajas_fase3.py` |
| A8 | Condición (c): mismo signo y tendencia radial / transferencia en cada terna | todas las ternas | 24/25 | **no** | `20_cajas_fase3.py` |
| A9 | Orden de Trotter en las cajas | en [1.8, 2.2] (Fase 2, C4) | 23/35; fuera: 1.18/R50: 1.65; 1.19/R50: 1.57; 1.19/R3200: 2.33; 1.2/R50: 1.49; 1.2/R100: 1.79; 1.25/R50: 1.14; 1.25/R100: 1.32; 1.25/R200: 1.39; 1.25/R400: 1.42; 1.25/R800: 1.42; 1.25/R1600: 1.37; 1.25/R3200: 1.07 | **no** | `20_cajas_fase3.py` |
| A10 | Diagnóstico de A9: orden de Trotter frente al radial en R + 0.5826√ε (celdas fuera de rango con R ≤ 800) | en [1.8, 2.2] si la causa es la pared sin imagen | 9/9; 1.18_R50: 1.984; 1.19_R50: 1.984; 1.2_R50: 1.984; 1.2_R100: 1.991; 1.25_R50: 1.983; 1.25_R100: 1.988; 1.25_R200: 1.992; 1.25_R400: 1.993; 1.25_R800: 1.975 | sí | `20d_diagnostico_pared.py` |
| B1 | δ = 1.19, radial h = 1/160, R = 3200 … 25600 (criterio 9.6 con el radial solo) | ligado en alguna terna | ligado en (3200, 6400, 12800), (6400, 12800, 25600) | sí | `20c_umbral_119_fino.py` |
| B2 | δ = 1.19: E0 en la caja más grande | medido | E0(25600) = -1.0299e-07 ± 1.3e-09; ⟨r⟩ = 1102 | medido | `20c_umbral_119_fino.py` |
| B3 | δ = 1.19: transferencia frente a radial en R = 1600 y 3200 | compatibles | R1600: +1.53e-07±1e-08 (rad +1.54e-07); R3200: -7.15e-08±2e-08 (rad -6.99e-08) | sí | `20b_umbral_119.py` |
| B4 | δ = 1.19: transferencia (LU en banda, N hasta 640000) frente a radial h = 1/160 en R = 6400 y 12800 | compatibles | R6400: -1.003e-07±2e-08 (rad -1.017e-07); R12800: -1.014e-07±2e-08 (rad -1.030e-07) | sí | `26_transferencia_grande.py` |
| B5 | δ = 1.19, terna 3200/6400/12800: criterio 9.6 con los dos métodos y condición (c) | ligado con ambos y (c) se cumple | radial ligado=True, transferencia ligado=True, (c)=True | sí | `26_transferencia_grande.py` |
| C1 | Barrido δ ∈ {0.2 … 1.19}: transferencia frente a radial | compatibles (como A1) | 8/8; máx \|dif\| = 1.8e-08 | sí | `21_barrido_delta.py` |
| C2 | Cotas analíticas −1/2 ≤ E0 ≤ −1/2 + δ (L04) | 0 violaciones | 0 violaciones en 13 δ | sí | `21_barrido_delta.py` |
| C3 | E0(δ) creciente (Hellmann-Feynman: dE/dδ = ⟨e^{−δr}⟩ > 0, L05) | estrictamente creciente | True | sí | `21_barrido_delta.py` |
| C4 | ⟨r⟩κ → 1/2 al acercarse al umbral (cola e^{−κr}) | medido | 1.15: 0.5268; 1.16: 0.5202; 1.17: 0.5136; 1.175: 0.5103; 1.18: 0.5069; 1.185: 0.5033; 1.188: 0.5016; 1.19: 0.5003 | medido | `21_barrido_delta.py` |
| C5 | Ajuste κ = AΔ + BΔ², Δ = δ_c − δ (δ ≥ 1.15) | medido (avance de la Fase 4) | A = 0.7411, B = +0.0585, residuo máx 7.4e-07 | medido | `21_barrido_delta.py` |
| D1 | Orden de Trotter, δ = 0.2, ε 0.2/0.1/0.05 y 0.1/0.05/0.025 | en [1.8, 2.2] | 1.959, 1.767 | **no** | `22_convergencia.py` |
| D2 | Orden de Trotter, δ = 0.8, ε 0.2/0.1/0.05 y 0.1/0.05/0.025 | en [1.8, 2.2] | 1.983, 1.991 | sí | `22_convergencia.py` |
| D3 | Orden de Trotter, δ = 1, ε 0.2/0.1/0.05 y 0.1/0.05/0.025 | en [1.8, 2.2] | 1.983, 1.991 | sí | `22_convergencia.py` |
| D4 | Orden de Trotter, δ = 1.15, ε 0.2/0.1/0.05 y 0.1/0.05/0.025 | en [1.8, 2.2] | 1.989, 1.993 | sí | `22_convergencia.py` |
| D5 | Orden de la malla Nyström, δ = 0.2 (h 0.04/0.02/0.01) | 4 ± 0.2 (Fase 2, 11.4) | 4.00, 4.00, 4.00, 4.00 | sí | `22_convergencia.py` |
| D6 | Orden de la malla Nyström, δ = 0.8 (h 0.04/0.02/0.01) | 4 ± 0.2 (Fase 2, 11.4) | 4.00, 4.00, 4.00, 4.00 | sí | `22_convergencia.py` |
| D7 | Orden de la malla Nyström, δ = 1 (h 0.04/0.02/0.01) | 4 ± 0.2 (Fase 2, 11.4) | 4.00, 4.00, 4.00, 4.00 | sí | `22_convergencia.py` |
| D8 | Orden de la malla Nyström, δ = 1.15 (h 0.04/0.02/0.01) | 4 ± 0.2 (Fase 2, 11.4) | 4.02, 4.00, 4.00, 4.00 | sí | `22_convergencia.py` |
| D9 | Extrapolado (h → 0, ε → 0) frente al radial, δ = 0.2 | \|dif\| < 1e-6 (Fase 2, 9.7) | +3.6e-09 (1.1e-08 de \|E0\|) | sí | `22_convergencia.py` |
| D10 | Extrapolado (h → 0, ε → 0) frente al radial, δ = 0.8 | \|dif\| < 1e-6 (Fase 2, 9.7) | -2.9e-09 (6.5e-08 de \|E0\|) | sí | `22_convergencia.py` |
| D11 | Extrapolado (h → 0, ε → 0) frente al radial, δ = 1 | \|dif\| < 1e-6 (Fase 2, 9.7) | -4.7e-09 (4.5e-07 de \|E0\|) | sí | `22_convergencia.py` |
| D12 | Extrapolado (h → 0, ε → 0) frente al radial, δ = 1.15 | \|dif\| < 1e-6 (Fase 2, 9.7) | -4.4e-09 (9.7e-06 de \|E0\|) | sí | `22_convergencia.py` |
| D13 | Presupuesto de errores en \|E0\|, δ = 0.2 | medido | Trotter(ε=0.1) 3.7e-07; malla(h=0.02) 6.2e-07; pared 1.4e-11; final 1.1e-08 | medido | `22_convergencia.py` |
| D14 | Presupuesto de errores en \|E0\|, δ = 0.8 | medido | Trotter(ε=0.1) 1.7e-04; malla(h=0.02) 2.2e-06; pared 3.5e-11; final 6.5e-08 | medido | `22_convergencia.py` |
| D15 | Presupuesto de errores en \|E0\|, δ = 1 | medido | Trotter(ε=0.1) 8.3e-04; malla(h=0.02) 4.7e-06; pared 8.8e-11; final 4.5e-07 | medido | `22_convergencia.py` |
| D16 | Presupuesto de errores en \|E0\|, δ = 1.15 | medido | Trotter(ε=0.1) 6.6e-03; malla(h=0.02) 2.3e-05; pared 2.4e-09; final 9.7e-06 | medido | `22_convergencia.py` |
| E1 | E0 en caja infinita por disparo DOP853 desde Frobenius (sin malla ni caja) | coincide con el radial en la caja mayor | δ = 1.18: -3.098591e-05; δ = 1.19: -1.030320e-07 | medido | `25_respuesta_gemini.py` |
| E2 | Sturm a energía cero: signo de a_s (ligado ⇔ a_s > 0 con un nodo) | δ_c entre 1.19 y 1.20 | δ = 1.18: a_s = +127.9; δ = 1.19: a_s = +2203.8; δ = 1.1906: a_s = +108621.0; δ = 1.1907: a_s = -15404.5; δ = 1.2: a_s = -142.9 | sí | `25_respuesta_gemini.py` |
| E3 | Orden de la malla del radial en δ = 1.19, R = 3200 (h = 1/40 … 1/640) y signo del sesgo | ≈ 2 y sesgo hacia arriba | 1.84, 1.96, 2.11; E(1/40) = +1.90e-08 → E(1/640) = -7.21e-08 | sí | `25_respuesta_gemini.py` |
| E4 | Auditoría adversarial con Gemini 3.1 Pro (7 hallazgos), cada uno verificado calculando | ninguno cambia el veredicto | G1–G6 refutados con cálculo; G7 (falta (c) en R > 3200) era válido y se resolvió con B4–B5 | sí | `25_respuesta_gemini.py, 26_transferencia_grande.py` |

## Lo que no pasa y por qué

- **A8 (24/25).** La terna que falla es δ = 1.15, R = 800/1600/3200: el estado ya cabe entero en las tres cajas y F_1/2 vale 1 a 1e-10 en las tres; la "tendencia" que compara la condición (c) es ruido de redondeo (diferencias de 1e-16) y su signo es arbitrario. El veredicto de δ = 1.15 sale de la terna 50/100/200, que sí pasa (c).
- **A9.** El orden de Trotter sale fuera de [1.8, 2.2] en las cajas donde la densidad toca la pared: las pequeñas cerca del umbral y todas las de δ = 1.25 (no ligado: el estado más bajo es un estado de caja). La causa es la pared en R sin imagen (decisión 5): **A10** muestra que, comparando con el radial en R + 0.5826√ε, el orden vuelve a 1.98–1.99 en las 9 celdas que se pudieron probar. El efecto ya está sumado a la barra de error y no cambia ningún signo ni veredicto. En δ = 1.19, R = 3200 (2.33) el sesgo de Trotter es del tamaño del error de la tabla (|E0| ~ 1e-7).
- **D1.** En δ = 0.2 el sesgo de Trotter con ε ≤ 0.05 es ~1e-9, del tamaño del residuo de la tabla U_C: la segunda terna de ε no mide un orden (como B9 en la Fase 2). La primera da 1.959 y el extrapolado queda a 3.6e-9 del radial.

## Lo que esta tabla no cubre (queda para después del 11-11)

- PIGS cerca del umbral (δ = 0.8 a 1.0), cierre de la anomalía de τ = 5 y PIGS de Hulthén (tareas 5 a 7 de `que_sigue_fase3.md`).
- La transferencia en R ≥ 25600 (N > 10⁶). No hace falta para el veredicto: la terna 3200/6400/12800 ya decide "ligado" con los dos métodos (B5).

## Auditoría adversarial (E4)

El chat literal con Gemini 3.1 Pro está en `fase3/auditoria_gemini/conversaciones/G.md` y la respuesta con los números en `auditoria_gemini/respuestas/G_r2.md`. Ninguna cifra de Gemini entra en esta tabla sin recalcularla.
