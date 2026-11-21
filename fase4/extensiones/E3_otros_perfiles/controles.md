# Controles de E3 (generado por `codigo/08_tabla_controles.py` desde `resultados/*.json`)

Los criterios se fijaron antes de correr cada script (están en su docstring). Las filas marcadas "(posterior)" se añadieron después de ver un fallo y no cambian el veredicto de la fila original.

Resumen: 32 filas; 29 pasan, 2 no pasan, el resto medido.

| # | control | criterio fijado antes | valor | ¿pasa? | script |
|---|---|---|---|---|---|
| U1 | δ_c por energía cero estable ante r_f y rtol | estabilidad de delta_A: rf 60/d vs 80/d < 1e-11; rtol 1e-13 vs 1e-11 < 1e-10 | máx 2.0e-12 | pasa | `01_umbrales.py` |
| U2 | δ_c por energía cero (A) frente a extrapolación de κ(δ) (B, cúbico, s = 0.002..0.03) | |delta_A - delta_B| < 1e-8 (cuatro perfiles) | Yukawa 1.5e-10; ECSC -5.5e-07; Hulthén -1.0e-14; átomo H estático -1.1e-10 | **no pasa** (ECSC: el cúbico no sigue la curvatura de κ(δ); residuo 3.5e-07) | `01_umbrales.py` |
| U2b | (posterior) B con s = 1e-4..2e-3 | mismo umbral 1e-8 (añadido después de ver U2) | Yukawa -7.8e-15; ECSC -7.1e-12; Hulthén -2.4e-15; átomo H estático 3.1e-15 | pasa | `01_umbrales.py` |
| U3 | Hulthén exacto y Yukawa de referencia | Hulthen |delta_A - 2| < 1e-10; Yukawa |delta_A - 1.1906124210606| < 1e-10 | -1.3e-14; 2.4e-15 | pasa | `01_umbrales.py` |
| U4 | Hulthén: κ del disparo = 1 − δ/2 | Hulthen: |kappa_disparo - (1 - delta/2)| < 1e-11 | 2.4e-14 | pasa | `01_umbrales.py` |
| S1 | 1/a y r_e: energía cero frente a desfasajes (k ≤ 0.1δ, grado 3) | |1/a_1 - 1/a_2| < 1e-9 y |r_e1 - r_e2| < 1e-5 (energia cero frente a desfasajes) | máx |Δ(1/a)| 1.3e-09, máx |Δr_e| 1.5e-06 | **no pasa** (truncación del polinomio en k²) | `02_dispersion.py` |
| S1b | (posterior) igual con k = (0.005..0.05)δ, grado 4 | (posterior) igual que S1 con k = (0.005..0.05) delta y grado 4 | máx |Δ(1/a)| 4.4e-14, máx |Δr_e| 1.1e-09 | pasa | `02_dispersion.py` |
| S2 | Hulthén: a(δ) frente a la fórmula con digamma | Hulthen: |a - a_exacto|/|a_exacto| < 1e-9 (|a| < 1e6) | 7.4e-11 | pasa | `02_dispersion.py` |
| S3 | c = −d(1/a)/dδ: Hellmann–Feynman frente a diferencias | |c_HF - c_dif|/c < 1e-7 | máx 1.2e-11 | pasa | `02_dispersion.py` |
| S5 | 1/a monótona y con un solo cero | 1/a monotona decreciente en delta y con un solo cambio de signo, en delta_c | 4 perfiles | pasa | `02_dispersion.py` |
| L1 | κ = (1 − √(1 − 2r_e/a))/r_e | |kappa_ERE - kappa|/kappa < 1e-4 para s <= 0.01 | máx 1.2e-05 | pasa | `03_ligados_virtuales.py` |
| L2 | pendiente medida A frente a c predicha | |A - c|/c < 1e-5 | Yukawa 5.2e-10; ECSC -4.6e-06; Hulthén -3.9e-12; átomo H estático -2.6e-10 | pasa | `03_ligados_virtuales.py` |
| L3 | κa → 1 y ⟨r⟩κ → 1/2 | s = 1e-5: |kappa a - 1| < 1e-3 y |<r> kappa - 1/2| < 1e-3 | máx 7.9e-06 | pasa | `03_ligados_virtuales.py` |
| L4 | pendiente de ⟨r⟩κ frente a κ = r_e/2 | pendiente d(<r>kappa)/dkappa (s <= 1e-3) frente a r_e/2: diferencia relativa < 2e-2 | Yukawa -3.2e-08; ECSC -6.9e-05; Hulthén -2.2e-08; átomo H estático -2.5e-08 | pasa | `03_ligados_virtuales.py` |
| L5 | polo virtual: rango efectivo frente a cálculo directo | |kappa_v(ERE) - kappa_v(directo)|/kappa_v < 1e-4 para s <= 0.01 | máx 1.4e-05 | pasa | `03_ligados_virtuales.py` |
| L6 | un solo ligado s, sin nodos | ligados sin nodos y una sola raiz | 64 puntos | pasa | `03_ligados_virtuales.py` |
| K1 | punto fijo 1/4 y su corrección (1/4)(1 + r_e/R) | |2R^2E0/pi^2 - pred(*)|/(1/4) < 1e-3 (R >= 200) y signo(valor - 1/4) = signo(r_e) (todo R) | máx 2.0e-10 | pasa | `04_cajas_universalidad.py` |
| K2 | sentido del cruce = signo de r_e | signo(delta* - delta_c) = signo(r_e) (todos los pares); |cruce - pred(*)| < 0.1|cruce - delta_c| (R1 >= 200) | máx |δ*−pred|/|δ*−δ_c| (R₁ ≥ 200) 1.9e-07 | pasa | `04_cajas_universalidad.py` |
| K3 | ⟨r⟩/R → 1/2 − 2/π² en δ_c | |<r>/R - (1/2 - 2/pi^2)| < 0.02 en R = 1600 | máx 3.9e-04 | pasa | `04_cajas_universalidad.py` |
| K4 | polo virtual desde las cajas | |kappa_v(caja) - kappa_v(directo)|/kappa_v < 1e-3 | máx 8.0e-04 | pasa | `04_cajas_universalidad.py` |
| K5 | radial (Fase 2) frente al disparo, R = 200 | |E0 radial - E0 disparo| < 2 err_radial + 1e-10 (R = 200) | máx 6.3e-09 | pasa | `04_cajas_universalidad.py` |
| T1 | W del ECSC acotado y positivo | W_ECSC en (0, delta] y finito en [1e-8, 400] | mín 2.50e-03 | pasa | `05_transferencia_ecsc.py` |
| T2 | integral de camino frente al disparo y al radial | |E_tr - E_disparo(R)| <= 2 err_tr + 1e-12 (y frente al radial: <= 2(err + err_rad)) | máx |dif|/σ 0.61 | pasa | `05_transferencia_ecsc.py` |
| T3 | orden de Trotter | orden de Trotter en [1.8, 2.2] (informativo si toca la pared) | 1.975 a 2.009 | pasa | `05_transferencia_ecsc.py` |
| T4 | Perron y residuo | Perron min(v)/max|v| > -1e-10 y residuo < 1e-8 | mín -1.9e-17, residuo máx 8.6e-16 | pasa | `05_transferencia_ecsc.py` |
| T5 | Hulthén 1.8 exacto por la integral de camino | Hulthen 1.8: |E_tr + 0.005| <= 2 err_tr + 1e-12 | -2.4e-09 (σ 7.5e-08) | pasa | `05_transferencia_ecsc.py` |
| T6 | reproduce comun3 (Fase 3) | Yukawa 1.18 R=200 (h 0.04, eps 0.1): |E - E_comun3| < 1e-13 | 0.0e+00 | pasa | `05_transferencia_ecsc.py` |
| V1 | tercer método (fase variable, LSODA) | |delta_c(fase variable, LSODA) - delta_A| < 1e-9 | máx 3.1e-12 | pasa | `07_verificacion.py` |
| V2 | disparo frente al radial de la Fase 3 (Yukawa) | |E_disparo - E_radial(Fase 3)| < 2 err_radial + 1e-9 | máx |dif| 6.6e-09 | pasa | `07_verificacion.py` |
| V3 | Hulthén ⟨r⟩ exacto | Hulthen |<r> - exacto|/exacto < 1e-9 | máx 5.5e-13 | pasa | `07_verificacion.py` |
| V4 | Hulthén: polo virtual κ_v = δ/2 − 1 (observación) | informativo: kappa_v de Hulthen frente a delta/2 - 1 | 9.1e-10 | medido | `07_verificacion.py` |
| V5 | Yukawa: c y B frente a la Fase 3 | |c - 0.7411| < 5e-4 y |B_pred - 0.059| < 0.01 (Yukawa, Fase 3) | c = 0.741192 (A = 0.741131); B = 0.0565 (0.0585) | pasa | `07_verificacion.py` |
