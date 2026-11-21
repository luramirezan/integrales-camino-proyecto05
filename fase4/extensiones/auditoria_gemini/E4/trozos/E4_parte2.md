# Material para auditoría (parte 2 de 3)

Responde solo "Recibido".

## controles.md (tabla generada por script)

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

## Código: pares_l.py (acción de pares de Coulomb en onda p)

```python
"""pares_l.py -- E4: accion de pares EXACTA del Coulomb en la onda parcial l y matriz de transferencia para l >= 1.

Generaliza fase2/codigo/pares.py y transferencia.py (que son solo l = 0) SIN modificarlos.

Onda parcial l, hbar = m = 1:
    H_l   = -1/2 d^2/dr^2 + l(l+1)/(2 r^2) - 1/r          (Coulomb + centrifugo)
    H_l^0 = -1/2 d^2/dr^2 + l(l+1)/(2 r^2)                 (libre en la onda l)
    K_l(r, r'; eps) = <r| e^{-eps H_l^0} |r'> = 4 pi r r' (2 pi eps)^{-3/2} e^{-(r^2+r'^2)/(2 eps)} i_l(r r'/eps)
                    = sqrt(r r')/eps * Ive(l+1/2, r r'/eps) * e^{-(r-r')^2/(2 eps)}   (exacto; l = 0 da K_D de pares.py)
    U_l(r, r'; eps) = -ln[ rho_l(r, r'; eps) / K_l(r, r'; eps) ],   rho_l = <r| e^{-eps H_l} |r'>.
El centrifugo va EXACTO en K_l; U_l solo contiene el efecto del Coulomb (y su cruce con el centrifugo).
U_l se calcula como en pares.py: red de diferencias finitas de paso h_tab en una caja de Dirichlet R_B = 14,
diagonalizacion del hamiltoniano tridiagonal (con l(l+1)/(2 r_j^2) en la diagonal), exponenciacion espectral y
division por el nucleo libre DE LA MISMA RED (con el mismo centrifugo), para cancelar el error de red; Richardson
entre h_tab = 0.01 y 0.005. Fuera de r = R_TAB = 10 se usa pares.U_extremos (extremos de Coulomb + Wigner-Kirkwood):
alli el centrifugo ya esta en K_l y la correccion cruzada es O(eps^2 l(l+1)/r^5).

Peso: rho_l es el nucleo de un semigrupo de Schrodinger en la semirrecta con potencial acotado inferiormente fuera
del origen y repulsivo en el origen; por Feynman-Kac (y, en la red, porque la matriz tridiagonal tiene fuera de la
diagonal elementos negativos) es real y positivo. K_l > 0 y e^{-U_l} > 0: la matriz T es real, simetrica y de
elementos no negativos; su autovector dominante es de signo constante (Perron-Frobenius).

Contenido: logK_l, tabla_red_l, tabla_richardson_l (cache en E4/resultados/tablas), matriz_T_l, resolver_T.
"""
import os
import time

import numpy as np
import scipy.sparse as sps
from scipy.linalg import eigh_tridiagonal
from scipy.sparse.linalg import eigsh
from scipy.special import ive

import comun4 as c4  # noqa: F401  (anade fase2/codigo a sys.path)
import pares          # fase2 (solo se usan U_extremos y banda_def)
import transferencia as tr

DIR_CACHE = os.path.join(c4.RES, "tablas")
RB_DEF, RTAB_DEF = 14.0, 10.0


def logK_l(a, b, eps, l):
    """ln K_l(a, b; eps) (nucleo libre exacto de la onda parcial l, medida dr)."""
    a = np.asarray(a, float); b = np.asarray(b, float)
    z = a * b / eps
    with np.errstate(divide="ignore"):
        return 0.5 * np.log(a * b) - np.log(eps) + np.log(ive(l + 0.5, z)) - (a - b)**2 / (2 * eps)


def _nombre(l, eps, h, RB, RTAB, banda):
    return os.path.join(DIR_CACHE, f"UCl{l}_eps{eps:.6g}_h{h:.6g}_RB{RB:.6g}_RT{RTAB:.6g}_b{banda:.6g}.npz")


def _calcular(l, eps, h, RB, RTAB, banda):
    N = int(round(RB / h)) - 1
    rr = h * np.arange(1, N + 1)
    off = -0.5 / h**2 * np.ones(N - 1)
    cent = 0.5 * l * (l + 1) / rr**2
    wC, vC = eigh_tridiagonal(1 / h**2 + cent - 1 / rr, off)
    w0, v0 = eigh_tridiagonal(1 / h**2 + cent, off)
    nt = int(round(RTAB / h))
    nb = int(round(banda / h))
    A, B = vC[:nt], v0[:nt]
    rhoC = (A * np.exp(-eps * (wC - wC[0]))) @ A.T
    rho0 = (B * np.exp(-eps * (w0 - w0[0]))) @ B.T
    shift = eps * (wC[0] - w0[0])
    Ub = np.full((nt, nb + 1), np.nan)
    Dlib = np.full((nt, nb + 1), np.nan)     # ln[rho0_red / K_l exacto]: error de red del nucleo libre
    nmalos = 0
    for m in range(nb + 1):
        i = np.arange(nt - m)
        cc, z = rhoC[i, i + m], rho0[i, i + m]
        ok = (cc > 0) & (z > 0)
        nmalos += int((~ok).sum())
        with np.errstate(divide="ignore", invalid="ignore"):
            u = -(np.log(cc) - np.log(z)) + shift
            dl = np.log(z) - eps * w0[0] - np.log(h) - logK_l(rr[i], rr[i + m], eps, l)
        u[~ok] = np.nan
        Ub[i, m] = u
        Dlib[i, m] = dl
    return dict(r=rr[:nt], Ub=Ub, Dlib=Dlib, eps=eps, h=h, RB=RB, RTAB=RTAB, banda=banda, nb=nb, l=l,
                E0_red=float(wC[0]), n_no_positivos=nmalos)


def tabla_red_l(l, eps, h, RB=RB_DEF, RTAB=RTAB_DEF, banda=None, cache=True):
    banda = pares.banda_def(eps) if banda is None else banda
    fn = _nombre(l, eps, h, RB, RTAB, banda)
    if cache and os.path.exists(fn):
        z = np.load(fn)
        d = {k: z[k] for k in z.files}
        for k in ("eps", "h", "RB", "RTAB", "banda", "E0_red"):
            d[k] = float(d[k])
        d["nb"] = int(d["nb"]); d["l"] = int(d["l"]); d["n_no_positivos"] = int(d["n_no_positivos"])
        d["tiempo"] = 0.0; d["cache"] = True
        return d
    t = time.perf_counter()
    d = _calcular(l, eps, h, RB, RTAB, banda)
    d["tiempo"] = time.perf_counter() - t; d["cache"] = False
    if cache:
        os.makedirs(DIR_CACHE, exist_ok=True)
        np.savez(fn, **{k: v for k, v in d.items() if k not in ("cache", "tiempo")})
    return d


def tabla_richardson_l(l, eps, h1=0.01, h2=0.005, RB=RB_DEF, RTAB=RTAB_DEF, banda=None, cache=True):
    """Igual que pares.tabla_richardson, en la onda parcial l."""
    banda = pares.banda_def(eps) if banda is None else banda
    d1 = tabla_red_l(l, eps, h1, RB, RTAB, banda, cache)
    d2 = tabla_red_l(l, eps, h2, RB, RTAB, banda, cache)
    nt = d1["Ub"].shape[0]
    nb = min(d1["Ub"].shape[1] - 1, (d2["Ub"].shape[1] - 1) // 2)
    banda = min(banda, nb * h1)
    k = np.arange(nt)[:, None]; m = np.arange(nb + 1)[None, :]
    k2, m2 = 2 * k + 1, 2 * m
    ok = (k2 + m2 < d2["Ub"].shape[0]) & (m2 < d2["Ub"].shape[1])
    U2 = np.full((nt, nb + 1), np.nan)
    D2 = np.full((nt, nb + 1), np.nan)
    kk, mm = np.broadcast_to(k2, ok.shape)[ok], np.broadcast_to(m2, ok.shape)[ok]
    U2[ok] = d2["Ub"][kk, mm]
    D2[ok] = d2["Dlib"][kk, mm]
    UR = (4 * U2 - d1["Ub"][:, :nb + 1]) / 3
    t = pares.TablaPares(d1["r"], UR, eps, h1, banda, origen=f"l={l} Richardson h_tab={h1},{h2}")
    t.U1, t.U2 = d1["Ub"][:, :nb + 1], U2
    t.D1, t.D2 = d1["Dlib"][:, :nb + 1], D2
    t.l = l
    t.info = dict(E0_red_h1=d1["E0_red"], E0_red_h2=d2["E0_red"],
                  n_no_positivos=(d1["n_no_positivos"], d2["n_no_positivos"]),
                  tiempo=(d1["tiempo"], d2["tiempo"]), cache=(d1["cache"], d2["cache"]))
    return t


def matriz_T_l(R, h, eps, l, W=None, tabla=None):
    """T_ij = h K_l(r_i, r_j) e^{-U_l(r_i, r_j)} e^{-eps [W(r_i) + W(r_j)]/2} (misma estructura que
    transferencia.matriz_T, con K_l y la tabla de la onda l). Sin tabla: U_l = 0 (solo el libre de la onda l)."""
    N = int(round(R / h)) - 1
    r = h * np.arange(1, N + 1)
    if tabla is not None:
        if abs(tabla.eps - eps) > 1e-14 or getattr(tabla, "l", l) != l:
            raise ValueError("la tabla es de otro eps o de otra l")
        step = int(round(h / tabla.h))
        if abs(step * tabla.h - h) > 1e-12:
            raise ValueError("h debe ser multiplo entero del paso de la tabla")
        banda = tabla.banda
    else:
        banda = pares.banda_def(eps)
    Wr = np.zeros(N) if W is None else W(r)
    nb = int(np.floor(banda / h + 1e-9))
    diags, offs = [], []
    for d in range(0, min(nb, N - 1) + 1):
        a, b = r[:N - d], r[d:]
        lk = logK_l(a, b, eps, l)
        if tabla is not None:
            Uv = pares.U_extremos(a, b, eps)
            i = np.arange(N - d)
            k = (i + 1) * step - 1
            m = d * step
            dentro = (k + m) < tabla.nt
            if m <= tabla.nb:
                Uv[dentro] = tabla.Ub[k[dentro], m]
            else:
                Uv[:] = np.nan
        else:
            Uv = np.zeros(N - d)
        val = h * np.exp(lk - Uv - 0.5 * eps * (Wr[:N - d] + Wr[d:]))
        val[~np.isfinite(val)] = 0.0
        diags.append(val); offs.append(d)
        if d:
            diags.append(val); offs.append(-d)
    return sps.diags(diags, offs, shape=(N, N), format="csr"), r


def resolver_T(T, r, R, eps, E_guess, h, k=2):
    """Mayor autovalor por shift-invert (como comun3.resolver_tr) y comprobaciones de Perron y residuo."""
    t = time.perf_counter()
    sigma = float(np.exp(-eps * (E_guess - 2e-4)))
    lam, v = eigsh(T, k=k, sigma=sigma, which="LM", tol=0)
    o = np.argsort(lam)[::-1]
    lam, v = lam[o], v[:, o]
    v0 = v[:, 0] * np.sign(v[:, 0].sum())
    perron = float(v0.min() / np.abs(v0).max())
    res = float(np.linalg.norm(T @ v0 - lam[0] * v0) / np.linalg.norm(v0))
    ob = tr._observables(r, v0, R)
    return dict(E0=float(-np.log(lam[0]) / eps), E1=float(-np.log(lam[1]) / eps), r_med=ob["r_med"],
                r2_med=ob["r2_med"], F12=ob["F12"], perron_min=perron, residuo=res, N=len(r),
                min_T=float(T.data.min()), sesgo_pared_est=tr.sesgo_pared(r, v0, h, eps),
                t=time.perf_counter() - t)
```

## Código: 45_transferencia_l1.py

```python
"""45_transferencia_l1.py -- E4, tarea 4: integral de camino en tiempo imaginario para la onda p (l = 1).

Metodo elegido (a): matriz de transferencia radial en la onda parcial l = 1 con
    T_ij = h K_1(r_i, r_j; eps) e^{-U_1(r_i, r_j; eps)} e^{-eps [W(r_i) + W(r_j)]/2},
K_1 el nucleo libre EXACTO de la onda p (lleva el centrifugo exacto), U_1 la accion de pares exacta del Coulomb en la
onda p (tablas del script 44) y W = V_Yukawa - V_Coulomb = (1 - e^{-delta r})/r, acotado en [0, delta].
Comparacion (b): aproximacion primitiva para la barrera centrifuga, con la accion de pares de l = 0 de la Fase 2:
    T_ij = h K_D e^{-U_0} e^{-eps [W + 1/r^2]_i/2 - eps [W + 1/r^2]_j/2}.
Receta de la Fase 3: h = 0.04 y 0.02 con Richardson (exponente medido aqui en Coulomb y en delta = 0.2 con h = 0.01),
eps = 0.2, 0.1, 0.05 con extrapolacion eps -> 0 (ley eps^2 si el orden medido lo confirma), error = suma lineal de
malla + Trotter + sesgo de pared (radial en R + 0.5826 sqrt(eps), solo en el error).
Casos: Coulomb 2p (R = 60, E = -1/8 exacto) y Yukawa delta = 0.10, 0.16, 0.20, 0.215, 0.219 (R = 100) frente al
radial en la misma caja (h = 1/160 con Richardson).
Criterios fijados ANTES de correr (17-11-2026):
  (a): |E_mejor - E_ref| <= 2 (err + err_ref) en los 6 casos; Coulomb: |E - (-1/8)| < 1e-7; orden de Trotter entre 1.8
       y 2.2; autovector de signo constante (Perron, min >= -1e-12 relativo) y T >= 0.
  (b): se mide su orden de Trotter y su sesgo; no se le exige pasar (es la comparacion).
Salida: resultados/45_transferencia_l1.json y _salida.txt.
"""
import math
import sys
import time

import numpy as np

import comun4 as c
import pares_l as pl
import transferencia as tr

sys.path.insert(0, c.F3)
import comun3  # noqa: E402  (tablas l = 0 de la Fase 2, solo lectura de la cache)

T0 = time.time()
c.Tee("45_transferencia_l1")
L = 1
EPSS = (0.2, 0.1, 0.05)
HS = (0.04, 0.02)
BETA = tr.BETA_PARED
TAB1 = {e: pl.tabla_richardson_l(L, e) for e in EPSS}
out = dict(criterios=dict(coulomb=1e-7, trotter=(1.8, 2.2), perron=-1e-12), casos=[])


def W_total(delta, primitiva):
    Wy = tr.W_yukawa(delta) if delta > 0 else (lambda r: np.zeros_like(r))
    if primitiva:
        return lambda r: Wy(r) + 1.0 / r**2          # l(l+1)/2 = 1 para l = 1
    return Wy


def corre(delta, R, h, eps, metodo, Eg):
    if metodo == "a":
        T, r = pl.matriz_T_l(R, h, eps, L, W=W_total(delta, False), tabla=TAB1[eps])
    else:
        T, r = tr.matriz_T(R, h, eps, W=W_total(delta, True), tabla=comun3.tabla(eps))
    return pl.resolver_T(T, r, R, eps, Eg, h)


def radial_ref(delta, R, h=1 / 160):
    V = c.V_yukawa_np(delta) if delta > 0 else (lambda r: -1.0 / r)
    d = c.fd_rich(V, L, R, h=h, nev=1)
    return dict(E0=d["E0"], err=abs(d["E0"] - d["E0_h2"]) / 15 + 2e-11, r_med=d["r_med"], r2_med=d["r2_med"])


# ------------------------------------------------------------------ orden en h (Coulomb y delta = 0.2, eps = 0.1)
print("Orden de la malla h en la transferencia (a), eps = 0.1")
orden_h = {}
for delta, R in ((0.0, 60.0), (0.2, 100.0)):
    ref = radial_ref(delta, R)
    Es = [corre(delta, R, h, 0.1, "a", ref["E0"])["E0"] for h in (0.04, 0.02, 0.01)]
    p = math.log2(abs(Es[0] - Es[1]) / abs(Es[1] - Es[2]))
    orden_h[str(delta)] = dict(E=Es, p=p)
    print(f"  delta = {delta}: E(h=0.04, 0.02, 0.01) = {Es[0]:.12f}, {Es[1]:.12f}, {Es[2]:.12f}; orden aparente {p:.3f}",
          flush=True)
out["orden_h"] = orden_h
# Las diferencias entre mallas son de 1e-11 a 2e-11, al nivel de la precision del autovalor: el orden aparente
# (7.2 en Coulomb, 2.2 en delta = 0.2) no es medible. Se usa el exponente 4 de la receta de la Fase 3 (decision 1)
# y se guarda tambien el resultado con el promedio de los dos ordenes aparentes (4.7, primera corrida) para mostrar
# que la eleccion cambia E en menos de 1e-11 (verificacion.md).
dif_mallas = max(max(abs(v["E"][0] - v["E"][1]), abs(v["E"][1] - v["E"][2])) for v in orden_h.values())
out["dif_mallas_max"] = dif_mallas
ph_usado = 4.0
ph_alt = float(np.mean([v["p"] for v in orden_h.values()]))
out["orden_h_usado"] = ph_usado
out["orden_h_alternativo"] = ph_alt
fh = 2.0**ph_usado
fh_alt = 2.0**ph_alt
print(f"  diferencia maxima entre mallas {dif_mallas:.1e}; exponente de Richardson usado en h: {ph_usado} "
      f"(alternativo {ph_alt:.2f})")


def ext_eps(e1, e2, p=2.0):
    return e2 + (e2 - e1) / (2**p - 1)


CASOS = [(0.0, 60.0), (0.10, 100.0), (0.16, 100.0), (0.20, 100.0), (0.215, 100.0), (0.219, 100.0)]
for delta, R in CASOS:
    t = time.time()
    ref = radial_ref(delta, R)
    caso = dict(delta=delta, R=R, radial=ref, metodos={})
    pared = {e: radial_ref(delta, R + BETA * math.sqrt(e), h=1 / 80)["E0"] - radial_ref(delta, R, h=1 / 80)["E0"]
             for e in EPSS}
    pared_ext = ext_eps(pared[0.1], pared[0.05])
    caso["pared"] = dict(por_eps={str(k): v for k, v in pared.items()}, extrapolado=pared_ext)
    for metodo in ("a", "b"):
        crudo, E = {}, {}
        for h in HS:
            for e in EPSS:
                d = corre(delta, R, h, e, metodo, ref["E0"])
                crudo[f"h{h:g}_eps{e:g}"] = d
                E[(h, e)] = d["E0"]
        EhR = {e: (fh * E[(0.02, e)] - E[(0.04, e)]) / (fh - 1) for e in EPSS}
        EhR_alt = {e: (fh_alt * E[(0.02, e)] - E[(0.04, e)]) / (fh_alt - 1) for e in EPSS}
        den = abs(EhR[0.1] - EhR[0.05])
        p_trot = float(math.log2(abs(EhR[0.2] - EhR[0.1]) / den)) if den > 0 else float("nan")
        p_ext = 2.0 if metodo == "a" else max(p_trot, 0.5)     # (b): con el orden medido
        Eb = ext_eps(EhR[0.1], EhR[0.05], p_ext)
        Eg_ = ext_eps(EhR[0.2], EhR[0.1], p_ext)
        Eh2 = ext_eps(E[(0.02, 0.1)], E[(0.02, 0.05)], p_ext)
        err = abs(Eh2 - Eb) + abs(Eb - Eg_) + abs(pared_ext)
        r_b = {k: ext_eps(crudo[f"h0.02_eps0.1"][k], crudo[f"h0.02_eps0.05"][k], p_ext) for k in ("r_med", "r2_med")}
        m = dict(E_hRich={str(k): v for k, v in EhR.items()}, orden_trotter=p_trot, p_extrapolacion=p_ext, E_mejor=Eb,
                 err=err, dif_radial=Eb - ref["E0"], compatible=bool(abs(Eb - ref["E0"]) <= 2 * (err + ref["err"])),
                 sesgo_eps01_rel=(EhR[0.1] - ref["E0"]) / abs(ref["E0"]), sesgo_eps005=EhR[0.05] - ref["E0"],
                 r_med=r_b["r_med"], r2_med=r_b["r2_med"], dif_r=r_b["r_med"] - ref["r_med"],
                 perron_min=min(d["perron_min"] for d in crudo.values()),
                 min_T=min(d["min_T"] for d in crudo.values()),
                 residuo_max=max(d["residuo"] for d in crudo.values()),
                 crudo={k: {kk: vv for kk, vv in v.items()} for k, v in crudo.items()})
        m["E_mejor_exponente_h_alternativo"] = ext_eps(EhR_alt[0.1], EhR_alt[0.05], p_ext)
        # sesgo de Trotter medido contra el radial con la pared corrida a R + BETA sqrt(eps) (diagnostico de la Fase 3)
        if metodo == "a":
            sp = {e: EhR[e] - (ref["E0"] + pared[e]) for e in EPSS}
            m["sesgo_sin_pared"] = {str(k): v for k, v in sp.items()}
            dd = abs(sp[0.1] - sp[0.05])
            m["orden_trotter_sin_pared"] = float(math.log2(abs(sp[0.2] - sp[0.1]) / dd)) if dd > 0 else float("nan")
        if delta == 0.0:
            m["dif_exacto"] = Eb + 0.125
        caso["metodos"][metodo] = m
        print(f"delta = {delta:<6} R = {R:.0f} metodo ({metodo}): E = {Eb:+.10e} +- {err:.1e}  radial {ref['E0']:+.10e}  "
              f"dif = {Eb - ref['E0']:+.1e}  compatible = {m['compatible']}  pTrot = {p_trot:.3f}  "
              f"sesgo(eps=0.1)/|E| = {m['sesgo_eps01_rel']:+.1e}  <r> dif = {m['dif_r']:+.1e}  perron = {m['perron_min']:+.1e} "
              f"minT = {m['min_T']:.1e}" + (f"  pTrot(pared corrida) = {m['orden_trotter_sin_pared']:.3f}" if metodo == "a" else ""),
              flush=True)
    caso["t"] = time.time() - t
    out["casos"].append(caso)
    c.guardar_json("45_transferencia_l1", out)

ca = [cs["metodos"]["a"] for cs in out["casos"]]
out["resumen_a"] = dict(
    todos_compatibles=bool(all(m["compatible"] for m in ca)),
    coulomb_dif=out["casos"][0]["metodos"]["a"]["dif_exacto"],
    trotter=[m["orden_trotter"] for m in ca],
    max_dif_rel=max(abs(m["dif_radial"]) / abs(cs["radial"]["E0"]) for m, cs in zip(ca, out["casos"])),
    perron_min=min(m["perron_min"] for m in ca), min_T=min(m["min_T"] for m in ca))
cb = [cs["metodos"]["b"] for cs in out["casos"]]
out["resumen_b"] = dict(trotter=[m["orden_trotter"] for m in cb],
                        sesgo_eps01_rel=[m["sesgo_eps01_rel"] for m in cb],
                        max_dif_rel=max(abs(m["dif_radial"]) / abs(cs["radial"]["E0"]) for m, cs in zip(cb, out["casos"])))
out["t_total"] = time.time() - T0
c.guardar_json("45_transferencia_l1", out)
print("\nResumen (a):", {k: v for k, v in out["resumen_a"].items()})
print("Resumen (b):", out["resumen_b"])
print(f"Tiempo total {out['t_total']:.0f} s")
```
