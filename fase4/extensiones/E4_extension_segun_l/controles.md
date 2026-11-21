# Tabla de controles de E4 (generada por `codigo/47_tabla_controles.py` desde los JSON)

129 controles: 105 pasan, 16 no pasan, 8 medidos sin criterio previo. Las causas medidas de los que no pasan están en `verificacion.md`, sección 3.

| # | control | criterio fijado antes | valor | ¿pasa? | script |
|---|---|---|---|---|---|
| 1 | FD con V_ef, Coulomb 1s: E frente a −1/(2n²) y orden de malla | |ΔE| < 1e-8 y orden 1.8–2.2 | ΔE = +6.1e-09; orden 2.000 | sí | 40 |
| 2 | FD con V_ef, Coulomb 2s: E frente a −1/(2n²) y orden de malla | |ΔE| < 1e-8 y orden 1.8–2.2 | ΔE = +9.7e-11; orden 2.000 | sí | 40 |
| 3 | FD con V_ef, Coulomb 2p: E frente a −1/(2n²) y orden de malla | |ΔE| < 1e-8 y orden 1.8–2.2 | ΔE = +3.9e-11; orden 2.000 | sí | 40 |
| 4 | FD con V_ef, Coulomb 3d: E frente a −1/(2n²) y orden de malla | |ΔE| < 1e-8 y orden 1.8–2.2 | ΔE = -9.1e-13; orden 2.004 | sí | 40 |
| 5 | Disparo (Frobenius + Whittaker), Coulomb 1s | |ΔE| < 1e-12, |Δ⟨r⟩| < 1e-9, nodos | ΔE = +3.7e-15; Δ⟨r⟩ = -3.0e-12; nodos 0 | sí | 40 |
| 6 | Disparo (Frobenius + Whittaker), Coulomb 2s | |ΔE| < 1e-12, |Δ⟨r⟩| < 1e-9, nodos | ΔE = +7.2e-16; Δ⟨r⟩ = -1.5e-12; nodos 1 | sí | 40 |
| 7 | Disparo (Frobenius + Whittaker), Coulomb 2p | |ΔE| < 1e-12, |Δ⟨r⟩| < 1e-9, nodos | ΔE = +3.3e-16; Δ⟨r⟩ = -6.4e-14; nodos 0 | sí | 40 |
| 8 | Disparo (Frobenius + Whittaker), Coulomb 3d | |ΔE| < 1e-12, |Δ⟨r⟩| < 1e-9, nodos | ΔE = -5.6e-17; Δ⟨r⟩ = +8.3e-14; nodos 0 | sí | 40 |
| 9 | δ_c(1s) = 1.1906124210606: frente al encargo, convergencia numérica y ajuste FD de E(δ) | encargo < 1e-8; numérica < 1e-11; ajuste FD < 1e-6 | -5.8e-15; 3.6e-12; ajuste FD -3.8e-05 | **no pasa** | 40 |
| 10 | δ_c(2s) = 0.3102092827139: frente al encargo, convergencia numérica y ajuste FD de E(δ) | encargo < 1e-8; numérica < 1e-11; ajuste FD < 1e-6 | +2.7e-09; 2.0e-13; ajuste FD -6.4e-07 | sí | 40 |
| 11 | δ_c(2p) = 0.2202168066066: frente al encargo, convergencia numérica y ajuste FD de E(δ) | encargo < 1e-8; numérica < 1e-11; ajuste FD < 1e-6 | -3.4e-09; 3.0e-14; ajuste FD +1.0e-06 | **no pasa** | 40 |
| 12 | δ_c(3d) = 0.0913451207717: frente al encargo, convergencia numérica y ajuste FD de E(δ) | encargo < 1e-8; numérica < 1e-11; ajuste FD < 1e-6 | +7.7e-10; 2.1e-15; ajuste FD -1.6e-07 | sí | 40 |
| 13 | FD (h = 1/40) frente a disparo, 2p δ = 0.1, R = 98 | E rel < 1e-6; ⟨r⟩ rel < 1e-5 | E rel +6.6e-10; ⟨r⟩ rel +4.2e-10 | sí | 40 |
| 14 | FD (h = 1/40) frente a disparo, 2p δ = 0.2, R = 331 | E rel < 1e-6; ⟨r⟩ rel < 1e-5 | E rel +3.5e-09; ⟨r⟩ rel +4.6e-10 | sí | 40 |
| 15 | FD (h = 1/40) frente a disparo, 2p δ = 0.219997, R = 3928 | E rel < 1e-6; ⟨r⟩ rel < 1e-5 | E rel +5.2e-07; ⟨r⟩ rel -9.9e-07 | sí | 40 |
| 16 | FD (h = 1/40) frente a disparo, 3d δ = 0.05, R = 163 | E rel < 1e-6; ⟨r⟩ rel < 1e-5 | E rel -3.0e-12; ⟨r⟩ rel +6.0e-12 | sí | 40 |
| 17 | FD (h = 1/40) frente a disparo, 3d δ = 0.085, R = 520 | E rel < 1e-6; ⟨r⟩ rel < 1e-5 | E rel +1.0e-09; ⟨r⟩ rel +5.8e-12 | sí | 40 |
| 18 | FD (h = 1/40) frente a disparo, 3d δ = 0.0912538, R = 4702 | E rel < 1e-6; ⟨r⟩ rel < 1e-5 | E rel +5.1e-08; ⟨r⟩ rel -2.1e-10 | sí | 40 |
| 19 | FD (h = 1/40) frente a disparo, 2s δ = 0.2, R = 193 | E rel < 1e-6; ⟨r⟩ rel < 1e-5 | E rel +8.4e-09 | sí | 40 |
| 20 | FD (h = 1/40) frente a disparo, 2s δ = 0.309899, R = 20000 | E rel < 1e-6; ⟨r⟩ rel < 1e-5 | E rel +7.7e-04 | **no pasa** | 40 |
| 21 | FD (h = 1/40) frente a disparo, 1s δ = 0.8, R = 100 | E rel < 1e-6; ⟨r⟩ rel < 1e-5 | E rel +1.5e-07; ⟨r⟩ rel -9.7e-09 | sí | 40 |
| 22 | FD (h = 1/40) frente a disparo, 1s δ = 1.18942, R = 20000 | E rel < 1e-6; ⟨r⟩ rel < 1e-5 | E rel +1.1e-02; ⟨r⟩ rel -1.4e-02 | **no pasa** | 40 |
| 23 | δ_c(1s) por la recurrencia de energía cero de las FD (Richardson doble) | |dif| < 1e-9, orden 1.8–2.2 | dif -1.0e-11; orden 2.000 | sí | 40b |
| 24 | δ_c(2s) por la recurrencia de energía cero de las FD (Richardson doble) | |dif| < 1e-9, orden 1.8–2.2 | dif -2.2e-11; orden 2.000 | sí | 40b |
| 25 | δ_c(2p) por la recurrencia de energía cero de las FD (Richardson doble) | |dif| < 1e-9, orden 1.8–2.2 | dif +1.8e-13; orden 2.000 | sí | 40b |
| 26 | δ_c(3d) por la recurrencia de energía cero de las FD (Richardson doble) | |dif| < 1e-9, orden 1.8–2.2 | dif -1.3e-13; orden 2.000 | sí | 40b |
| 27 | Diagnóstico: FD h = 1/160 en 2s δ = 0.309899 (fallo de la fila D) | rel < 1e-4 y cociente de errores > 50 | rel +2.8e-04; cociente 3 | **no pasa** | 40b |
| 28 | Diagnóstico: FD h = 1/160 en 1s δ = 1.18942 (fallo de la fila D) | rel < 1e-4 y cociente de errores > 50 | rel +6.7e-05; cociente 162 | sí | 40b |
| 29 | Integral universal I_N (mpmath) frente a su forma cerrada | sin criterio previo | -1.500000000000000 frente a -1.500000000000000 | medido | 41 |
| 30 | Integral universal I_2 (mpmath) frente a su forma cerrada | sin criterio previo | -0.972222222222222 frente a -0.972222222222222 | medido | 41 |
| 31 | Integral universal M_1 (mpmath) frente a su forma cerrada | sin criterio previo | 1.250000000000000 frente a 1.250000000000000 | medido | 41 |
| 32 | Integral universal K_1 (mpmath) frente a su forma cerrada | sin criterio previo | -0.020362845461478 frente a -0.020362845461478 | medido | 41 |
| 33 | 1s: exponente de E (ventana 1e-07–1e-05) | |p − 2| < 0.01 | p = +2.00000 ± 6.9e-07 | sí | 42 |
| 34 | 1s: exponente de r_med (ventana 1e-07–1e-05) | |p − -1| < 0.01 | p = -1.00000 ± 6.0e-06 | sí | 42 |
| 35 | 1s: exponente de r2_med (ventana 1e-07–1e-05) | |p − -2| < 0.01 | p = -2.00000 ± 6.0e-06 | sí | 42 |
| 36 | 1s: coeficiente kappa_sobre_Delta en el último punto | rel < 1e-3 | 0.74119177 frente a 0.74119177 (rel +1.1e-09) | sí | 42 |
| 37 | 1s: coeficiente r_kappa en el último punto | rel < 1e-3 | 0.50000008 frente a 0.5 (rel +1.6e-07) | sí | 42 |
| 38 | 1s: coeficiente r2_kappa2 en el último punto | rel < 1e-3 | 0.50000008 frente a 0.5 (rel +1.6e-07) | sí | 42 |
| 39 | 1s: Hellmann–Feynman, Δ/δ_c = 3e-02 | rel < 1e-6 | rel +3.0e-09 | sí | 42 |
| 40 | 1s: Hellmann–Feynman, Δ/δ_c = 1e-04 | rel < 1e-6 | rel +3.7e-10 | sí | 42 |
| 41 | 1s: Hellmann–Feynman, Δ/δ_c = 1e-07 | rel < 1e-6 | rel +1.2e-06 | **no pasa** | 42 |
| 42 | 1s: FD (h = 1/40, R = 3396) frente a disparo, Δ/δ_c = 1e-02 | E rel < 1e-5; ⟨r⟩ rel < 1e-4 | E rel +1.1e-04; ⟨r⟩ rel -1.0e-04 | **no pasa** | 42 |
| 43 | 1s: FD (h = 1/40, R = 33992) frente a disparo, Δ/δ_c = 1e-03 | E rel < 1e-5; ⟨r⟩ rel < 1e-4 | E rel +1.1e-02; ⟨r⟩ rel -1.4e-02 | **no pasa** | 42 |
| 44 | 2s: exponente de E (ventana 1e-07–1e-05) | |p − 2| < 0.01 | p = +2.00000 ± 1.6e-06 | sí | 42 |
| 45 | 2s: exponente de r_med (ventana 1e-07–1e-05) | |p − -1| < 0.01 | p = -0.99999 ± 2.0e-05 | sí | 42 |
| 46 | 2s: exponente de r2_med (ventana 1e-07–1e-05) | |p − -2| < 0.01 | p = -1.99999 ± 2.0e-05 | sí | 42 |
| 47 | 2s: coeficiente kappa_sobre_Delta en el último punto | rel < 1e-3 | 1.3169557 frente a 1.3169557 (rel +4.7e-08) | sí | 42 |
| 48 | 2s: coeficiente r_kappa en el último punto | rel < 1e-3 | 0.50000026 frente a 0.5 (rel +5.2e-07) | sí | 42 |
| 49 | 2s: coeficiente r2_kappa2 en el último punto | rel < 1e-3 | 0.50000026 frente a 0.5 (rel +5.2e-07) | sí | 42 |
| 50 | 2s: Hellmann–Feynman, Δ/δ_c = 3e-02 | rel < 1e-6 | rel +6.4e-09 | sí | 42 |
| 51 | 2s: Hellmann–Feynman, Δ/δ_c = 1e-04 | rel < 1e-6 | rel -1.1e-10 | sí | 42 |
| 52 | 2s: Hellmann–Feynman, Δ/δ_c = 1e-07 | rel < 1e-6 | rel -5.2e-07 | sí | 42 |
| 53 | 2s: FD (h = 1/40, R = 7328) frente a disparo, Δ/δ_c = 1e-02 | E rel < 1e-5; ⟨r⟩ rel < 1e-4 | E rel +7.9e-06 | sí | 42 |
| 54 | 2s: FD (h = 1/40, R = 40000) frente a disparo, Δ/δ_c = 1e-03 | E rel < 1e-5; ⟨r⟩ rel < 1e-4 | E rel +7.8e-04 | **no pasa** | 42 |
| 55 | 2p: exponente de E (ventana 1e-09–1e-07) | |p − 1| < 0.01 | p = +1.00009 ± 1.1e-04 | sí | 42 |
| 56 | 2p: exponente de potencia de ⟨r⟩ (ventana 1e-09–1e-07) | no es potencia (ver fila del logaritmo) | p = -0.1165 ± 1.7e-02 | medido | 42 |
| 57 | 2p: exponente de r2_med (ventana 1e-09–1e-07) | |p − -1| < 0.01 | p = -0.99992 ± 9.8e-05 | sí | 42 |
| 58 | 2p: coeficiente menos_E_sobre_Delta en el último punto | rel < 1e-3 | 0.12602232 frente a 0.12601591 (rel +5.1e-05) | sí | 42 |
| 59 | 2p: coeficiente r2_kappa en el último punto | rel < 1e-3 | 8.2628919 frente a 8.2627105 (rel +2.2e-05) | sí | 42 |
| 60 | 2p: crecimiento logarítmico de ⟨r⟩ | exponente local monótono; pendiente ±1 % de A²; fórmula refinada < 1e-3 | monótono True; pendiente 6.59696 (A² 6.61017, rel -2.0e-03); fórmula 2.3e-07 | sí | 42 |
| 61 | 2p: Hellmann–Feynman, Δ/δ_c = 3e-02 | rel < 1e-6 | rel -1.1e-08 | sí | 42 |
| 62 | 2p: Hellmann–Feynman, Δ/δ_c = 1e-05 | rel < 1e-6 | rel +6.3e-09 | sí | 42 |
| 63 | 2p: Hellmann–Feynman, Δ/δ_c = 1e-09 | rel < 1e-6 | rel -3.9e-05 | **no pasa** | 42 |
| 64 | 2p: FD (h = 1/40, R = 1177) frente a disparo, Δ/δ_c = 1e-02 | E rel < 1e-5; ⟨r⟩ rel < 1e-4 | E rel +3.1e-08; ⟨r⟩ rel -1.0e-08 | sí | 42 |
| 65 | 2p: FD (h = 1/40, R = 3928) frente a disparo, Δ/δ_c = 1e-03 | E rel < 1e-5; ⟨r⟩ rel < 1e-4 | E rel +4.2e-07; ⟨r⟩ rel -9.8e-07 | sí | 42 |
| 66 | 3d: exponente de E (ventana 1e-09–1e-07) | |p − 1| < 0.01 | p = +1.00000 ± 5.3e-07 | sí | 42 |
| 67 | 3d: exponente de r_med (ventana 1e-09–1e-07) | |p − 0| < 0.01 | p = -0.00000 ± 4.7e-06 | sí | 42 |
| 68 | 3d: exponente de r2_med (ventana 1e-09–1e-07) | |p − 0| < 0.01 | p = -0.00050 ± 6.0e-04 | sí | 42 |
| 69 | 3d: coeficiente menos_E_sobre_Delta en el último punto | rel < 1e-3 | 0.22191705 frente a 0.22191684 (rel +9.8e-07) | sí | 42 |
| 70 | 3d: coeficiente r_med en el último punto | rel < 1e-3 | 21.616079 frente a 21.616081 (rel -8.8e-08) | sí | 42 |
| 71 | 3d: coeficiente r2_med en el último punto | rel < 1e-3 | 766.78254 frente a 766.88525 (rel -1.3e-04) | sí | 42 |
| 72 | 3d: coeficiente r2_pendiente_kappa en el último punto | sin criterio previo | -16130.818 frente a -16132.871 (rel +1.3e-04) | medido | 42 |
| 73 | 3d: Hellmann–Feynman, Δ/δ_c = 3e-02 | rel < 1e-6 | rel -4.2e-09 | sí | 42 |
| 74 | 3d: Hellmann–Feynman, Δ/δ_c = 1e-05 | rel < 1e-6 | rel -2.8e-09 | sí | 42 |
| 75 | 3d: Hellmann–Feynman, Δ/δ_c = 1e-09 | rel < 1e-6 | rel +1.6e-04 | **no pasa** | 42 |
| 76 | 3d: FD (h = 1/40, R = 1465) frente a disparo, Δ/δ_c = 1e-02 | E rel < 1e-5; ⟨r⟩ rel < 1e-4 | E rel +7.5e-09; ⟨r⟩ rel -1.4e-12 | sí | 42 |
| 77 | 3d: FD (h = 1/40, R = 4702) frente a disparo, Δ/δ_c = 1e-03 | E rel < 1e-5; ⟨r⟩ rel < 1e-4 | E rel +5.1e-08; ⟨r⟩ rel -2.2e-10 | sí | 42 |
| 78 | 1s en δ_c: y = 2R²E/π² tiende a 1/4 | |y(R_max) − 1/4| < 0.01 | y(2560) = 0.25017 | sí | 43 |
| 79 | 2p en δ_c: Y = 2R^(2l+1)E/((2l+1)A²) tiende a 1, |Y − 1| decrece | |Y(R_max) − 1| < 0.01 | Y(2560) = 1.004665; y(2560) = 7.89e-04 | sí | 43 |
| 80 | 3d en δ_c: Y = 2R^(2l+1)E/((2l+1)A²) tiende a 1, |Y − 1| decrece | |Y(R_max) − 1| < 0.01 | Y(2560) = 1.000006; y(2560) = 5.01e-07 | sí | 43 |
| 81 | FD (h = 1/160) frente a disparo en la caja, 2p R = 10 | |ΔE| < 1e-9 | +8.9e-12 | sí | 43 |
| 82 | FD (h = 1/160) frente a disparo en la caja, 2p R = 20 | |ΔE| < 1e-9 | -1.7e-11 | sí | 43 |
| 83 | FD (h = 1/160) frente a disparo en la caja, 2p R = 40 | |ΔE| < 1e-9 | -1.7e-11 | sí | 43 |
| 84 | FD (h = 1/160) frente a disparo en la caja, 2p R = 80 | |ΔE| < 1e-9 | -1.6e-11 | sí | 43 |
| 85 | FD (h = 1/160) frente a disparo en la caja, 2p R = 160 | |ΔE| < 1e-9 | +2.9e-11 | sí | 43 |
| 86 | FD (h = 1/160) frente a disparo en la caja, 3d R = 10 | |ΔE| < 1e-9 | +1.8e-11 | sí | 43 |
| 87 | FD (h = 1/160) frente a disparo en la caja, 3d R = 20 | |ΔE| < 1e-9 | -8.7e-12 | sí | 43 |
| 88 | FD (h = 1/160) frente a disparo en la caja, 3d R = 40 | |ΔE| < 1e-9 | -4.2e-11 | sí | 43 |
| 89 | FD (h = 1/160) frente a disparo en la caja, 3d R = 80 | |ΔE| < 1e-9 | +3.8e-11 | sí | 43 |
| 90 | FD (h = 1/160) frente a disparo en la caja, 3d R = 160 | |ΔE| < 1e-9 | +1.9e-11 | sí | 43 |
| 91 | FD (h = 1/160) frente a disparo en la caja, 1s R = 10 | |ΔE| < 1e-9 | +2.7e-11 | sí | 43 |
| 92 | FD (h = 1/160) frente a disparo en la caja, 1s R = 20 | |ΔE| < 1e-9 | +3.1e-12 | sí | 43 |
| 93 | FD (h = 1/160) frente a disparo en la caja, 1s R = 40 | |ΔE| < 1e-9 | +5.2e-13 | sí | 43 |
| 94 | FD (h = 1/160) frente a disparo en la caja, 1s R = 80 | |ΔE| < 1e-9 | +3.1e-11 | sí | 43 |
| 95 | FD (h = 1/160) frente a disparo en la caja, 1s R = 160 | |ΔE| < 1e-9 | +2.1e-11 | sí | 43 |
| 96 | 1s: radio de cruce R_c(Δ) | R_c frente a a_s < 1e-3 | máx. rel frente a a_s 4.0e-08 | sí | 43 |
| 97 | 2p: radio de cruce R_c(Δ) | R_c frente a ((2l+1)A²/(2SΔ))^(1/(2l+1)) < 1 % | máx. rel (Δ/δ_c ≤ 1e-4) 7.0e-05 | sí | 43 |
| 98 | 3d: radio de cruce R_c(Δ) | R_c frente a ((2l+1)A²/(2SΔ))^(1/(2l+1)) < 1 % | máx. rel (Δ/δ_c ≤ 1e-4) 8.3e-04 | sí | 43 |
| 99 | 2p: cruce de y entre R = 160 y 320 | δ* y y* ±10 % de la predicción | rel δ*: +0.09; rel y*: +0.09 | sí | 43 |
| 100 | 3d: cruce de y entre R = 160 y 320 | δ* y y* ±10 % de la predicción | rel δ*: +0.01; rel y*: +0.01 | sí | 43 |
| 101 | ln K_l con l = 0 igual a pares.logKD | < 1e-12 | 3.3e-14 | sí | 44 |
| 102 | ε = 0.2: núcleo libre de la red l = 1 frente a K_1 exacto | cociente 3.5–4.5 y Richardson < 1e-5 | cociente 4.10; Richardson 6.4e-06 | sí | 44 |
| 103 | ε = 0.2: |U_R − U_0.005| de la tabla l = 1 | < 1e-4 | 8.2e-05 | sí | 44 |
| 104 | ε = 0.2: continuidad tabla / extremos + WK en r = 9–9.9 | < 1e-6 | 4.2e-08 | sí | 44 |
| 105 | ε = 0.2: ρ_1 de la red positivo (peso real y positivo) | 0 elementos ≤ 0 | [0, 0] | sí | 44 |
| 106 | ε = 0.1: núcleo libre de la red l = 1 frente a K_1 exacto | cociente 3.5–4.5 y Richardson < 1e-5 | cociente 4.12; Richardson 1.3e-05 | **no pasa** | 44 |
| 107 | ε = 0.1: |U_R − U_0.005| de la tabla l = 1 | < 1e-4 | 1.0e-04 | **no pasa** | 44 |
| 108 | ε = 0.1: continuidad tabla / extremos + WK en r = 9–9.9 | < 1e-6 | 5.2e-09 | sí | 44 |
| 109 | ε = 0.1: ρ_1 de la red positivo (peso real y positivo) | 0 elementos ≤ 0 | [0, 0] | sí | 44 |
| 110 | ε = 0.05: núcleo libre de la red l = 1 frente a K_1 exacto | cociente 3.5–4.5 y Richardson < 1e-5 | cociente 3.99; Richardson 2.7e-05 | **no pasa** | 44 |
| 111 | ε = 0.05: |U_R − U_0.005| de la tabla l = 1 | < 1e-4 | 1.3e-04 | **no pasa** | 44 |
| 112 | ε = 0.05: continuidad tabla / extremos + WK en r = 9–9.9 | < 1e-6 | 6.6e-10 | sí | 44 |
| 113 | ε = 0.05: ρ_1 de la red positivo (peso real y positivo) | 0 elementos ≤ 0 | [0, 0] | sí | 44 |
| 114 | Camino (a), Coulomb 2p, R = 60: frente al radial | |dif| ≤ 2(err + err_ref) | dif +5.5e-11, err 2.7e-11 | sí | 45 |
| 115 | Camino (a), Coulomb 2p: orden de Trotter | 1.8–2.2 | 2.029 (con la pared corrida: 2.088) | sí | 45 |
| 116 | Camino (a), δ = 0.1, R = 100: frente al radial | |dif| ≤ 2(err + err_ref) | dif +5.8e-11, err 1.3e-11 | sí | 45 |
| 117 | Camino (a), δ = 0.1: orden de Trotter | 1.8–2.2 | 1.997 (con la pared corrida: 1.997) | sí | 45 |
| 118 | Camino (a), δ = 0.16, R = 100: frente al radial | |dif| ≤ 2(err + err_ref) | dif +6.7e-11, err 1.6e-11 | sí | 45 |
| 119 | Camino (a), δ = 0.16: orden de Trotter | 1.8–2.2 | 1.999 (con la pared corrida: 1.998) | sí | 45 |
| 120 | Camino (a), δ = 0.2, R = 100: frente al radial | |dif| ≤ 2(err + err_ref) | dif +6.2e-11, err 2.5e-11 | sí | 45 |
| 121 | Camino (a), δ = 0.2: orden de Trotter | 1.8–2.2 | 1.999 (con la pared corrida: 1.999) | sí | 45 |
| 122 | Camino (a), δ = 0.215, R = 100: frente al radial | |dif| ≤ 2(err + err_ref) | dif -2.7e-09, err 4.3e-09 | sí | 45 |
| 123 | Camino (a), δ = 0.215: orden de Trotter | 1.8–2.2 | 1.935 (con la pared corrida: 1.999) | sí | 45 |
| 124 | Camino (a), δ = 0.219, R = 100: frente al radial | |dif| ≤ 2(err + err_ref) | dif -2.0e-08, err 3.0e-08 | sí | 45 |
| 125 | Camino (a), δ = 0.219: orden de Trotter | 1.8–2.2 | 1.611 (con la pared corrida: 1.998) | **no pasa** | 45 |
| 126 | Camino (a), Coulomb 2p: E frente a −1/8 | < 1e-7 | +5.2e-11 | sí | 45 |
| 127 | Camino (a): autovector de signo constante y T ≥ 0 en todas las corridas | Perron ≥ −1e-12; min T ≥ 0 | Perron mín +6.7e-14; min T 2.9e-14 | sí | 45 |
| 128 | Camino (b) primitivo: orden de Trotter | solo se mide | 1.339, 1.343, 1.349, 1.357, 1.367, 1.375 | medido | 45 |
| 129 | Camino (b) primitivo: error relativo máximo tras extrapolar | solo se mide | 1.0e-03 | medido | 45 |
