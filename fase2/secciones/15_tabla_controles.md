# 15. Tabla de controles de la Fase 2 (consolidada)

Fecha: 27-10-2026. Equipo: Juan Sebastián Calixto (verificación) y Luis Felipe Ramírez (implementación). Unidades $\hbar=m=g=1$, $V=-e^{-\delta r}/r$, $\delta_c=1.1906124211$ (Fase 1).

**Estado: SIN FIRMAR.** Esta tabla la generó `fase2/codigo/16_tabla_controles.py` leyendo los JSON de los scripts 10 a 15 después de las correcciones de la respuesta V3 (`fase2/verificacion/V3_respuesta_hallazgos.md`). Ninguna cifra está escrita a mano: cada fila dice de qué script y de qué JSON sale. La firma de quien verifica (Juan Sebastián) va al final; un agente no puede firmar por él.

**Resumen:** 88 filas; **70 pasan**, **9 no pasan** y 9 son medidas o informativas (sin criterio de aceptación, o con decisión pendiente). Los que no pasan están en negrita en la columna "¿Pasa?" y se explican en la sección "Lo que no pasa".

Leyenda: "sí" = cumple el criterio fijado antes de ejecutar; "**no**" = no lo cumple (no se cambió la tolerancia después); "medido" = magnitud que el plan pide medir y declarar, o informativa.

### A. Criterios de 9.7 aplicables a la Fase 2

| # | Control | Criterio | Valor medido | ¿Pasa? | Script | Fuente (JSON) |
|---|---|---|---|---|---|---|
| A1 | Coulomb delta=0, transferencia (L02) | \|E+0.5\|<1e-6 tras Richardson en h_tab; \|<r>-1.5\|<1e-4 (eps 0.2/0.1/0.05) | 5.44e-08 (Rich en E: 5.49e-08; sin Rich: 2.60e-05, 6.55e-06); 1.71e-07; 1.09e-07 (Rich en E: 1.10e-07; sin Rich: 2.88e-05, 7.29e-06); 3.34e-07; 2.18e-07 (Rich en E: 2.19e-07; sin Rich: 3.12e-05, 7.97e-06); 6.60e-07 | sí | `11_transferencia_controles.py` | `11_transferencia.json (criterios)` |
| A2 | Coulomb delta=0, PIGS, 1 cadena (plan) | E_L = -0.5; <r>, <r^2> a < 2 sigma de 1.5 y 3 | E_L: var=0.0e+00, max\|E_L+0.5\|=0.0e+00 (tautologico: W=0); 1.49277 +- 0.01626 (-0.44 sigma); 2.97503 +- 0.07873 (-0.32 sigma) | sí | `12_pigs_produccion.py` | `12_pigs.json (criterios)` |
| A3 | Coulomb delta=0, PIGS, 8 cadenas + histograma (V3) | <r>, <r^2> a < 2 sigma; histograma de r_{M/2} p > 1e-3 | 1.49027 +- 0.00720 (-1.35 sigma de 1.5); cociente (cadenas/bloques)^2 = 0.45; 2.96787 +- 0.03430 (-0.94 sigma de 3.0); cociente (cadenas/bloques)^2 = 0.59; chi2 = 57.7 con 32 intervalos, p = 0.004 | sí | `12c_pigs_coulomb_tau5.py` | `12c_pigs_coulomb_tau5.json (A_coulomb)` |
| A4 | delta=0.2 transferencia, h=0.02 | \|E-E_rad\|<1e-6, \|<r>-<r>_rad\|<1e-3 | 4.00e-07; 5.41e-05; 1.05e-08; 1.39e-05; 1.78e-07; 4.11e-06 | sí | `11_transferencia_controles.py` | `11_transferencia.json (criterios)` |
| A5 | delta=0.2 transferencia, h=0.04 (control) | idem | 3.58e-07; 5.68e-05; 1.51e-06; 1.92e-05; 3.22e-06; 1.46e-05 | **no** | `11_transferencia_controles.py` | `11_transferencia.json (criterios)` |
| A6 | delta=0.2 PIGS (tau=20, 8 cadenas) | E, <r>, <r^2> a < 2 sigma del radial; sigma = mayor de bloques y cadenas | -0.326725 +- 0.000068 frente a -0.32680851 (+1.22 sigma); 1.55374 +- 0.00711 frente a 1.54972 (+0.56 sigma); 3.24260 +- 0.03894 frente a 3.22594 (+0.43 sigma) | sí | `12_pigs_produccion.py` | `12_pigs.json (criterios)` |
| A7 | Ley eps^2, delta=0.2, h=0.02 sin Richardson en h (L18) | orden en [1.8, 2.2]; extrapolado < 1e-6 del radial | 1.046 | **no** | `11_transferencia_controles.py` | `11_transferencia.json (trotter)` |
| A8 | Ley eps^2, delta=0.2, Richardson h^4 (L18) | orden en [1.8, 2.2]; extrapolado < 1e-6 del radial | 1.958 | sí | `11_transferencia_controles.py` | `11_transferencia.json (trotter)` |
| A9 | Extrapolado eps->0, delta=0.2 (L18) | orden en [1.8, 2.2]; extrapolado < 1e-6 del radial | 4.41e-09 | sí | `11_transferencia_controles.py` | `11_transferencia.json (trotter)` |
| A10 | Ley eps^2, delta=1.0, R=174, h=0.02 (L18) | orden en [1.8, 2.2]; extrapolado < 1e-6 del radial | 1.978 | sí | `11_transferencia_controles.py` | `11_transferencia.json (trotter)` |
| A11 | Ley eps^2, delta=1.0, Richardson h^4 (L18) | orden en [1.8, 2.2]; extrapolado < 1e-6 del radial | 1.983 | sí | `11_transferencia_controles.py` | `11_transferencia.json (trotter)` |
| A12 | Extrapolado eps->0, delta=1.0 (L18) | orden en [1.8, 2.2]; extrapolado < 1e-6 del radial | 1.21e-08 | sí | `11_transferencia_controles.py` | `11_transferencia.json (trotter)` |
| A13 | Tabulacion: estabilidad Nystrom 0.02 -> 0.04 (9 casos) | \|E(0.04)-E(0.02)\| < 1e-6 | 8.00e-07  (eps*dif=1.60e-07); 1.60e-06  (eps*dif=1.60e-07); 3.20e-06  (eps*dif=1.60e-07); 7.58e-07  (eps*dif=1.52e-07); 1.52e-06  (eps*dif=1.52e-07); 3.04e-06  (eps*dif=1.52e-07); 1.72e-07  (eps*dif=3.45e-08); 3.59e-07  (eps*dif=3.59e-08); 7.31e-07  (eps*dif=3.66e-08) | **no** | `11_transferencia_controles.py` | `11_transferencia.json (estabilidad_nystrom)` |
| A14 | Tabulacion: orden de la malla Nystrom (propuesta: Richardson h^4) | medido | delta=0.0,eps=0.2: 4.00, delta=0.0,eps=0.1: 4.00, delta=0.0,eps=0.05: 4.00, delta=0.2,eps=0.2: 4.00, delta=0.2,eps=0.1: 4.00, delta=0.2,eps=0.05: 4.00 | medido | `11_transferencia_controles.py` | `11_transferencia.json (orden_nystrom)` |
| A15 | Proyeccion (L15), transferencia delta=0.2, eps=0.1 | variacion < 1e-6 de tau=20 a 30; limite del mixto - E0(T) < 1e-6 | 2.52e-07; 1.05e-07; con Richardson en h: -1.3e-09 | sí | `11_transferencia_controles.py` | `11_transferencia.json (proyeccion)` |
| A16 | Proyeccion con PIGS frente a la transferencia (tau = 2, 5, 10, 20) | PIGS a menos de 2 sigma de la transferencia en cada tau | tau=2: -0.7/+0.6/+0.6 sigma; tau=5: -3.2/+1.6/+1.6 sigma; tau=10: +0.2/-1.0/-0.9 sigma; tau=20: +1.2/+0.7/+0.6 sigma | **no** | `12_pigs_produccion.py` | `12_pigs.json (criterios)` |
| A17 | Anomalia tau=5: replica 1 (16 cadenas) | < 2 sigma de la transferencia | E +0.03 sigma; <r> -0.76 sigma | sí | `12b_pigs_replica_tau5.py` | `12b_pigs_replica.json (replica)` |
| A18 | Anomalia tau=5: replica 2 (16 cadenas, V3) | < 2 sigma de la transferencia | -0.326718 +- 0.000045 (+0.99 sigma; transferencia -0.326762633); 1.529878 +- 0.005000 (-0.45 sigma; transferencia 1.532136474); 3.123609 +- 0.024123 (-0.60 sigma; transferencia 3.138107461) | sí | `12c_pigs_coulomb_tau5.py` | `12c_pigs_coulomb_tau5.json (B_replica2_tau5)` |
| A19 | Anomalia tau=5: las 40 cadenas (informativo, V3) | se reporta | ponderada -0.83 sigma, pesos iguales -0.61 sigma; chi2 de las 3 corridas 11.13/3 (p=0.011); chi2 por cadena 50.2/39 (p=0.109) | medido | `12c_pigs_coulomb_tau5.py` | `12c_pigs_coulomb_tau5.json (C_tau5_combinado)` |
| A20 | Malla espacial h en cada caja (a') | \|E0(h)-E0(h/2)\| < 0.1\|E0\| | transferencia (0.02 vs 0.04): max 2.8e-03; radial (1/40 vs 1/80): max 0.057 | sí | `14_criterio_cajas.py` | `14_cajas.json (celdas/*/malla_rel; 10_radial.json cajas_9_6)` |
| A21 | Caja: E0(R) decreciente (L12) | decreciente en R (Dirichlet) | cajas 9.6 (15 celdas, transferencia): 3/3 delta decrecientes; delta=1.0: E_ext(R) = -5.964265e-03, -1.010965e-02, -1.028526e-02, -1.028580e-02, -1.028580e-02; decreciente True | sí | `15_limites.py` | `15_limites.json (L12; 14_cajas.json celdas)` |
| A22 | Hellmann-Feynman (L05) delta=0.2 | \|dE/ddelta - <e^{-delta r}>\| < 1e-4 | 0.74485846 frente a 0.74485290 (dif +5.6e-06) | sí | `15_limites.py` | `15_limites.json (L05)` |
| A23 | Hellmann-Feynman (L05) delta=0.5 | \|dE/ddelta - <e^{-delta r}>\| < 1e-4 | 0.46009830 frente a 0.46009558 (dif +2.7e-06) | sí | `15_limites.py` | `15_limites.json (L05)` |
| A24 | Hellmann-Feynman (L05) delta=1.0 | \|dE/ddelta - <e^{-delta r}>\| < 1e-4 | 0.10963014 frente a 0.10962884 (dif +1.3e-06) | sí | `15_limites.py` | `15_limites.json (L05)` |
| A25 | Virial (L06) delta=0.2 | \|residuo extrapolado en h y eps\| < 1e-5 | h=0.02, eps=0.05: -1.33e-04; h=0.01: -3.80e-05 (orden en h 2.00); extrapolado -5.91e-07 | sí | `15_limites.py` | `15_limites.json (L06)` |
| A26 | Cotas (L04) | -1/2 <= E0 <= -1/2 + delta | 0 violaciones en 5 delta; margen minimo 1.816e-03 | sí | `15_limites.py` | `15_limites.json (L04)` |
| A27 | Sin ligado en delta >= 2 (L19) | E > 0 y a < 5 % de pi^2/(2(R-a_s)^2) | E(R=200) = +1.2190e-04; desviacion de la ley de caja -1.02e-03 (radial +4.00e-06) | sí | `15_limites.py` | `15_limites.json (L19)` |
| A28 | Umbral (Fase 4; avance de la Fase 2) | intervalo compatible con 1.1906124211 y dentro de [1.19055, 1.24305] | cajas: 1.15 ligado, 1.18 ligado, 1.2 no ligado => delta_c en [1.18, 1.20]; el intervalo final es de la Fase 4 | medido | `14_criterio_cajas.py` | `14_cajas.json (veredictos)` |
| A29 | Errores por bloques: regla del cociente | si (err cadenas/err bloques)^2 > 2 se usa el de cadenas (siempre se usa el mayor) | cocientes en E: 1.75, 1.17, 1.01, 0.43 (prod, tau 2, 5, 10); se reporta siempre el mayor | sí | `12_pigs_produccion.py` | `12_pigs.json (pigs/*/EL/cociente)` |

### B. Controles exactos: Hulthén y pozo cuadrado (sección 13)

| # | Control | Criterio | Valor medido | ¿Pasa? | Script | Fuente (JSON) |
|---|---|---|---|---|---|---|
| B1 | A0 W_H delta=0.2 | W_H en [0, delta/2] y decreciente en r in [1e-8, 400] (tolerancia 1e-14) | min 2.500e-03, max 0.099999999966667 (delta/2=0.1), max incremento 0.0e+00 | sí | `13_controles_hulthen_pozo.py` | `13_controles.json (criterios)` |
| B2 | A0 W_H delta=1.0 | W_H en [0, delta/2] y decreciente en r in [1e-8, 400] (tolerancia 1e-14) | min 2.500e-03, max 0.499999999166667 (delta/2=0.5), max incremento 0.0e+00 | sí | `13_controles_hulthen_pozo.py` | `13_controles.json (criterios)` |
| B3 | A0 W_H delta=1.5 | W_H en [0, delta/2] y decreciente en r in [1e-8, 400] (tolerancia 1e-14) | min 2.500e-03, max 0.749999998125000 (delta/2=0.75), max incremento 0.0e+00 | sí | `13_controles_hulthen_pozo.py` | `13_controles.json (criterios)` |
| B4 | A0 W_H delta=2.0 | W_H en [0, delta/2] y decreciente en r in [1e-8, 400] (tolerancia 1e-14) | min 2.500e-03, max 0.999999996666667 (delta/2=1.0), max incremento 0.0e+00 | sí | `13_controles_hulthen_pozo.py` | `13_controles.json (criterios)` |
| B5 | A1 radial Hulthen delta=0.2 | radial frente a exacto: \|E0-E\| < 1e-8 y \|<r>-<r>_ex\|/<r>_ex < 2e-7 | dE=+3.77e-10, d<r>/<r>=-2.46e-10 | sí | `13_controles_hulthen_pozo.py` | `13_controles.json (criterios)` |
| B6 | A1 radial Hulthen delta=1.0 | radial frente a exacto: \|E0-E\| < 1e-8 y \|<r>-<r>_ex\|/<r>_ex < 2e-7 | dE=+4.06e-10, d<r>/<r>=-1.81e-10 | sí | `13_controles_hulthen_pozo.py` | `13_controles.json (criterios)` |
| B7 | A1 radial Hulthen delta=1.5 | radial frente a exacto: \|E0-E\| < 1e-8 y \|<r>-<r>_ex\|/<r>_ex < 2e-7 | dE=+4.02e-10, d<r>/<r>=-2.62e-09 | sí | `13_controles_hulthen_pozo.py` | `13_controles.json (criterios)` |
| B8 | A2 Hulthen delta=0.2 E extrapolada | transferencia (Richardson h^4 con h=0.02,0.04), extrapolada eps->0 con eps^2 desde eps 0.2/0.1/0.05: \|E_ext - E_exacta\| < 1e-6 | +5.09e-09 (Rich h 0.01/0.02: +5.00e-09) | sí | `13_controles_hulthen_pozo.py` | `13_controles.json (criterios)` |
| B9 | A3 Hulthen delta=0.2 orden de Trotter | orden de Trotter aparente (eps 0.2/0.1/0.05, Richardson en h) en [1.8, 2.2] para delta=1.0 y 1.5 (en delta=0.2 el sesgo de Trotter es del tamano del residuo de Nystrom: informativo) | 1.382 (eps .1/.05/.025: 0.065) | medido | `13_controles_hulthen_pozo.py` | `13_controles.json (criterios)` |
| B10 | A4 Hulthen delta=0.2 <r> extrapolado | <r> de la transferencia, h->0 y eps->0: \|<r>_ext - <r>_ex\| < 1e-4 | +1.69e-08 (exacto 1.51010101) | sí | `13_controles_hulthen_pozo.py` | `13_controles.json (criterios)` |
| B11 | A2 Hulthen delta=1.0 E extrapolada | transferencia (Richardson h^4 con h=0.02,0.04), extrapolada eps->0 con eps^2 desde eps 0.2/0.1/0.05: \|E_ext - E_exacta\| < 1e-6 | +2.50e-09 (Rich h 0.01/0.02: +2.43e-09) | sí | `13_controles_hulthen_pozo.py` | `13_controles.json (criterios)` |
| B12 | A3 Hulthen delta=1.0 orden de Trotter | orden de Trotter aparente (eps 0.2/0.1/0.05, Richardson en h) en [1.8, 2.2] para delta=1.0 y 1.5 (en delta=0.2 el sesgo de Trotter es del tamano del residuo de Nystrom: informativo) | 1.990 (eps .1/.05/.025: 1.986) | sí | `13_controles_hulthen_pozo.py` | `13_controles.json (criterios)` |
| B13 | A4 Hulthen delta=1.0 <r> extrapolado | <r> de la transferencia, h->0 y eps->0: \|<r>_ext - <r>_ex\| < 1e-4 | +4.90e-08 (exacto 1.83333333) | sí | `13_controles_hulthen_pozo.py` | `13_controles.json (criterios)` |
| B14 | A2 Hulthen delta=1.5 E extrapolada | transferencia (Richardson h^4 con h=0.02,0.04), extrapolada eps->0 con eps^2 desde eps 0.2/0.1/0.05: \|E_ext - E_exacta\| < 1e-6 | -1.78e-09 (Rich h 0.01/0.02: -1.82e-09) | sí | `13_controles_hulthen_pozo.py` | `13_controles.json (criterios)` |
| B15 | A3 Hulthen delta=1.5 orden de Trotter | orden de Trotter aparente (eps 0.2/0.1/0.05, Richardson en h) en [1.8, 2.2] para delta=1.0 y 1.5 (en delta=0.2 el sesgo de Trotter es del tamano del residuo de Nystrom: informativo) | 1.991 (eps .1/.05/.025: 1.994) | sí | `13_controles_hulthen_pozo.py` | `13_controles.json (criterios)` |
| B16 | A4 Hulthen delta=1.5 <r> extrapolado | <r> de la transferencia, h->0 y eps->0: \|<r>_ext - <r>_ex\| < 1e-4 | -3.36e-08 (exacto 2.78571429) | sí | `13_controles_hulthen_pozo.py` | `13_controles.json (criterios)` |
| B17 | B1 radial pozo V0=2.0 | radial (borde medio, r=1 en un nodo) frente a brentq: \|E0-E\| < 1e-8 (V0=2) y < 2e-8 (V0=1.3) | -1.04e-10 (convencion estricta: +2.92e-03) | sí | `13_controles_hulthen_pozo.py` | `13_controles.json (criterios)` |
| B18 | B1 radial pozo V0=1.3 | radial (borde medio, r=1 en un nodo) frente a brentq: \|E0-E\| < 1e-8 (V0=2) y < 2e-8 (V0=1.3) | +1.66e-10 (convencion estricta: +3.30e-04) | sí | `13_controles_hulthen_pozo.py` | `13_controles.json (criterios)` |
| B19 | B4 desplazamiento-inversion V0=2.0 h=0.02 eps=0.1 | desplazamiento-inversion frente a tr.resolver (Lanczos): \|dE\| < 1e-10 | +8.7e-15 | sí | `13_controles_hulthen_pozo.py` | `13_controles.json (criterios)` |
| B20 | B4 desplazamiento-inversion V0=1.3 h=0.04 eps=0.05 | desplazamiento-inversion frente a tr.resolver (Lanczos): \|dE\| < 1e-10 | +2.3e-12 | sí | `13_controles_hulthen_pozo.py` | `13_controles.json (criterios)` |
| B21 | B2 pozo V0=2.0 media orden de Trotter aparente | orden de Trotter aparente del pozo: MEDIDO y declarado (sin criterio de aceptacion) | 1.497, 1.499, 1.502 | medido | `13_controles_hulthen_pozo.py` | `13_controles.json (criterios)` |
| B22 | B3 pozo V0=2.0 E extrapolada (orden medido) | pozo, transferencia h->0 (V3: mallas 0.02/0.01/0.005) y eps->0 con el orden medido: \|E_ext - E_brentq\| < 1e-5 | +3.55e-06 (con ley eps^2: -1.22e-04; ajuste eps^1.5 a 5 puntos: +9.70e-07; antes, mallas .04/.02/.01: +6.17e-06) | sí | `13_controles_hulthen_pozo.py` | `13_controles.json (criterios)` |
| B23 | B3b pozo V0=2.0 ajuste eps^1.5 a 5 puntos (V3) | \|E0_ajuste - E_brentq\| < 1e-5 (control de robustez de B3, V3) | +9.70e-07 | sí | `13_controles_hulthen_pozo.py` | `13_controles.json (criterios)` |
| B24 | B2 pozo V0=2.0 estricta orden de Trotter aparente | orden de Trotter aparente del pozo: MEDIDO y declarado (sin criterio de aceptacion) | 1.497, 1.498, 1.500 | medido | `13_controles_hulthen_pozo.py` | `13_controles.json (criterios)` |
| B25 | B2 pozo V0=1.3 media orden de Trotter aparente | orden de Trotter aparente del pozo: MEDIDO y declarado (sin criterio de aceptacion) | 1.672, 1.567, 1.523 | medido | `13_controles_hulthen_pozo.py` | `13_controles.json (criterios)` |
| B26 | B3 pozo V0=1.3 E extrapolada (orden medido) | pozo, transferencia h->0 (V3: mallas 0.02/0.01/0.005) y eps->0 con el orden medido: \|E_ext - E_brentq\| < 1e-5 | -4.20e-07 (con ley eps^2: -9.27e-06; ajuste eps^1.5 a 5 puntos: +2.16e-05; antes, mallas .04/.02/.01: -2.64e-07) | sí | `13_controles_hulthen_pozo.py` | `13_controles.json (criterios)` |
| B27 | B3b pozo V0=1.3 ajuste eps^1.5 a 5 puntos (V3) | \|E0_ajuste - E_brentq\| < 1e-5 (control de robustez de B3, V3) | +2.16e-05 | **no** | `13_controles_hulthen_pozo.py` | `13_controles.json (criterios)` |
| B28 | B2 pozo V0=1.3 estricta orden de Trotter aparente | orden de Trotter aparente del pozo: MEDIDO y declarado (sin criterio de aceptacion) | 1.684, 1.575, 1.529 | medido | `13_controles_hulthen_pozo.py` | `13_controles.json (criterios)` |

### C. Criterio de cajas 9.6 con la condición (c) (sección 14)

| # | Control | Criterio | Valor medido | ¿Pasa? | Script | Fuente (JSON) |
|---|---|---|---|---|---|---|
| C1 | Condicion (c) en las 9 ternas | mismo signo, misma tendencia, E0 compatibles | 9/9 | sí | `14_criterio_cajas.py` | `14_cajas.json (veredictos)` |
| C2 | E0 transferencia frente al radial, celda a celda | \|dif\| <= 2(err_tr + err_rad) | 15/15 | sí | `14_criterio_cajas.py` | `14_cajas.json (celdas)` |
| C3 | Idem con solo el error de la transferencia (V3, con sesgo de pared) | \|dif\| <= err_tr | 15/15 con el termino de pared; 6/15 sin el (fallan sin el: 1.15_R50, 1.18_R50, 1.18_R100, 1.18_R200, 1.2_R50, 1.2_R100, 1.2_R200, 1.2_R400, 1.2_R800) | sí | `14_criterio_cajas.py` | `14_cajas.json (V3_criterio_estricto)` |
| C4 | Orden de Trotter tras Richardson en h | [1.8, 2.2] | 12/15; fuera: 1.18 R50: 1.65, 1.2 R50: 1.49, 1.2 R100: 1.79 | **no** | `14_criterio_cajas.py` | `14_cajas.json (celdas/*/orden_trotter)` |
| C5 | Orden de la malla Nystrom cerca del umbral (delta=1.18, eps=0.1) | 4, como en 11.4 | R=50: 1.361; R=100: 2.287 | **no** | `14_criterio_cajas.py` | `14_cajas.json (orden_nystrom)` |
| C6 | Veredicto 9.6 delta=1.15 | criterio completo (a), (a'), (b), (c) o no ligado con ley de caja | ligado, terna [50, 100, 200] | sí | `14_criterio_cajas.py` | `14_cajas.json (veredictos)` |
| C7 | Veredicto 9.6 delta=1.18 | criterio completo (a), (a'), (b), (c) o no ligado con ley de caja | ligado, terna [200, 400, 800] | sí | `14_criterio_cajas.py` | `14_cajas.json (veredictos)` |
| C8 | Veredicto 9.6 delta=1.2 | criterio completo (a), (a'), (b), (c) o no ligado con ley de caja | no ligado, terna [200, 400, 800]; desviacion de la ley [0.382, 0.101, 0.021] | sí | `14_criterio_cajas.py` | `14_cajas.json (veredictos)` |

### D. Límites físicos L01–L19 comprobados con la integral de camino (script 15)

| # | Control | Criterio | Valor medido | ¿Pasa? | Script | Fuente (JSON) |
|---|---|---|---|---|---|---|
| D1 | L03 serie perturbativa | orden en [4.5, 5.5] y \|res_tr - res_rad\| < 1e-8 | orden aparente 4.844 (radial 4.862); cociente res(0.1)/res(0.05) = 28.71; max \|res_tr - res_rad\| = 4.7e-09 | sí | `15_limites.py` | `15_limites.json (L03)` |
| D2 | L04 cotas -1/2 <= E0 <= -1/2 + delta | 0 violaciones | 0 violaciones en 5 delta; margen minimo 1.816e-03 | sí | `15_limites.py` | `15_limites.json (L04)` |
| D3 | L05 Hellmann-Feynman delta=0.2 | \|dE/ddelta - <e^{-delta r}>\| < 1e-4 | 0.74485846 frente a 0.74485290 (dif +5.6e-06) | sí | `15_limites.py` | `15_limites.json (L05)` |
| D4 | L05 Hellmann-Feynman delta=0.5 | \|dE/ddelta - <e^{-delta r}>\| < 1e-4 | 0.46009830 frente a 0.46009558 (dif +2.7e-06) | sí | `15_limites.py` | `15_limites.json (L05)` |
| D5 | L05 Hellmann-Feynman delta=1.0 | \|dE/ddelta - <e^{-delta r}>\| < 1e-4 | 0.10963014 frente a 0.10962884 (dif +1.3e-06) | sí | `15_limites.py` | `15_limites.json (L05)` |
| D6 | L06 virial delta=0.2 | \|residuo extrapolado en h y eps\| < 1e-5 | h=0.02, eps=0.05: -1.33e-04; h=0.01: -3.80e-05 (orden en h 2.00); extrapolado -5.91e-07 | sí | `15_limites.py` | `15_limites.json (L06)` |
| D7 | L07 cuspide delta=0.0 | \|a2/a1 + 1\| < 0.02 | a2/a1 = -0.99987 | sí | `15_limites.py` | `15_limites.json (L07)` |
| D8 | L09 sin nodos delta=0.0 | min(v)/max(v) >= -1e-10 | min/max = -1.2e-15 | sí | `15_limites.py` | `15_limites.json (L09)` |
| D9 | L07 cuspide delta=0.2 | \|a2/a1 + 1\| < 0.02 | a2/a1 = -0.99937 | sí | `15_limites.py` | `15_limites.json (L07)` |
| D10 | L09 sin nodos delta=0.2 | min(v)/max(v) >= -1e-10 | min/max = +1.6e-14 | sí | `15_limites.py` | `15_limites.json (L09)` |
| D11 | L09 sin nodos delta=0.5 | min(v)/max(v) >= -1e-10 | min/max = +1.9e-10 | sí | `15_limites.py` | `15_limites.json (L09)` |
| D12 | L07 cuspide delta=1.0 | \|a2/a1 + 1\| < 0.02 | a2/a1 = -0.98740 | sí | `15_limites.py` | `15_limites.json (L07)` |
| D13 | L09 sin nodos delta=1.0 | min(v)/max(v) >= -1e-10 | min/max = +9.5e-13 | sí | `15_limites.py` | `15_limites.json (L09)` |
| D14 | L08 cola Coulomb | a 2e-2 de 1/kappa en r = 20 | r(dlnu/dr+kappa) en r=10, 20: 1.0000, 1.0000 (1/kappa = 1.0000) | sí | `15_limites.py` | `15_limites.json (L08)` |
| D15 | L08 cola delta=0.5 (sin factor r^{1/kappa}) | \|.\| < 1e-2 en r = 20 | 0.0080, 0.0001 | sí | `15_limites.py` | `15_limites.json (L08)` |
| D16 | L12 caja delta=1.0 | decreciente en R y >= E(R=174) | E_ext(R) = -5.964265e-03, -1.010965e-02, -1.028526e-02, -1.028580e-02, -1.028580e-02; decreciente True | sí | `15_limites.py` | `15_limites.json (L12)` |
| D17 | L14 2s ligado delta=0.2 | E1 < 0 y \|dif\| < 1e-6 | E1 = -0.012107865 (radial -0.012107865, dif +2.1e-10) | sí | `15_limites.py` | `15_limites.json (L14)` |
| D18 | L14 2s no ligado delta=0.35 | E1 > 0, igual que el radial | E1 = +1.637e-04 (radial +1.639e-04) | sí | `15_limites.py` | `15_limites.json (L14)` |
| D19 | L16 propagador libre | a 1e-10; K_D >= 0; K_D(0, r') = 0 | max \|h sum_j K_D - erf\| = 8.1e-05, 1.6e-04, 3.2e-04 | **no** | `15_limites.py` | `15_limites.json (L16)` |
| D20 | L16 propagador libre: orden del error de la suma (informativo) | medido (error de extremo del trapecio) | orden en h 2.00, 2.00, 2.00; h=0.01: 2.0e-05, 4.0e-05, 8.1e-05 | medido | `15_limites.py` | `15_limites.json (L16)` |
| D21 | L19 delta=2 sin ligado | E > 0 y a < 5 % de pi^2/(2(R-a_s)^2) | E(R=200) = +1.2190e-04; desviacion de la ley de caja -1.02e-03 (radial +4.00e-06) | sí | `15_limites.py` | `15_limites.json (L19)` |

### E. Referencia radial (sección 10)

| # | Control | Criterio | Valor medido | ¿Pasa? | Script | Fuente (JSON) |
|---|---|---|---|---|---|---|
| E1 | delta=0.2 E0 radial (h=1/40, 1/80) frente al exacto | < 5e-9 | +6.23e-09 | **no** | `10_radial_controles.py / test_radial.py` | `10_radial.json (yukawa_0.2/V3_referencia_fina)` |
| E2 | delta=0.2 E0 radial (h=1/80, 1/160) frente al exacto | < 5e-9 (test: 1e-9) | +4.02e-10 | sí | `10_radial_controles.py / test_radial.py` | `10_radial.json (yukawa_0.2/V3_referencia_fina)` |

## Lo que no pasa y por qué

- **delta=0.2 transferencia, h=0.04 (control)** (3.58e-07; 5.68e-05; 1.51e-06; 1.92e-05; 3.22e-06; 1.46e-05). Criterio: idem.
- **Ley eps^2, delta=0.2, h=0.02 sin Richardson en h (L18)** (1.046). Criterio: orden en [1.8, 2.2]; extrapolado < 1e-6 del radial.
- **Tabulacion: estabilidad Nystrom 0.02 -> 0.04 (9 casos)** (8.00e-07  (eps*dif=1.60e-07); 1.60e-06  (eps*dif=1.60e-07); 3.20e-06  (eps*dif=1.60e-07); 7.58e-07  (eps*dif=1.52e-07); 1.52e-06  (eps*dif=1.52e-07); 3.04e-06  (eps*dif=1.52e-07); 1.72e-07  (eps*dif=3.45e-08); 3.59e-07  (eps*dif=3.59e-08); 7.31e-07  (eps*dif=3.66e-08)). Criterio: |E(0.04)-E(0.02)| < 1e-6.
- **Proyeccion con PIGS frente a la transferencia (tau = 2, 5, 10, 20)** (tau=2: -0.7/+0.6/+0.6 sigma; tau=5: -3.2/+1.6/+1.6 sigma; tau=10: +0.2/-1.0/-0.9 sigma; tau=20: +1.2/+0.7/+0.6 sigma). Criterio: PIGS a menos de 2 sigma de la transferencia en cada tau.
- **B3b pozo V0=1.3 ajuste eps^1.5 a 5 puntos (V3)** (+2.16e-05). Criterio: |E0_ajuste - E_brentq| < 1e-5 (control de robustez de B3, V3).
- **Orden de Trotter tras Richardson en h** (12/15; fuera: 1.18 R50: 1.65, 1.2 R50: 1.49, 1.2 R100: 1.79). Criterio: [1.8, 2.2].
- **Orden de la malla Nystrom cerca del umbral (delta=1.18, eps=0.1)** (R=50: 1.361; R=100: 2.287). Criterio: 4, como en 11.4.
- **L16 propagador libre** (max |h sum_j K_D - erf| = 8.1e-05, 1.6e-04, 3.2e-04). Criterio: a 1e-10; K_D >= 0; K_D(0, r') = 0.
- **delta=0.2 E0 radial (h=1/40, 1/80) frente al exacto** (+6.23e-09). Criterio: < 5e-9.

Lectura (detalle en las secciones 11 a 15 y en V3):
- Los fallos de la sección 11 (estabilidad de Nyström 0.02 → 0.04 y control con $h=0.04$) tienen una causa medida: error de extremo del trapecio en la cúspide de Coulomb, de orden $h^4/\epsilon$. Con Richardson en $h$ (exponente 4) desaparecen. Cerca del umbral el orden de la malla no es 4 (1.36 y 2.29): para la Fase 4 hay que usar $h=0.02$ y $0.01$.
- La ley $\epsilon^2$ sin Richardson en $h$ en $\delta=0.2$ falla porque el sesgo de Trotter es del tamaño del error de Nyström; con Richardson en $h$ pasa, y en $\delta=1.0$ pasa en las dos formas.
- El orden de Trotter en $R=50$ y $100$ lo rebaja la pared en $R$ sin imagen ($R+0.5826\sqrt\epsilon$).
- En el pozo, el ajuste a cinco puntos con la ley fija $\epsilon^{3/2}$ falla en $V_0=1.3$, donde el orden todavía es preasintótico (1.67 → 1.52).
- La anomalía de $\tau=5$ en el PIGS se mantiene en la producción; las réplicas y la combinación se dan en la parte A.
- L16: la suma del núcleo libre en la malla tiene un error $O(h^2)$ de extremo (medido), no $10^{-10}$ como se esperaba al fijar el criterio. Las propiedades exactas de $K_D$ ($K_D\ge0$, $K_D(0,r')=0$) sí se cumplen; el criterio quedó mal planteado y se deja como "no pasa".

## Límites que no se comprueban todavía con la integral de camino

- **L01** (escalamiento): el código trabaja en unidades reducidas; se comprobó con el radial en la Fase 1 (sección 7.3). Probarlo con la transferencia exigiría reintroducir $m$ y $g$.
- **L10** (umbral) y **L11** (extensión cerca del umbral): Fase 4 y Fase 3. Avance: $\delta_c\in[1.18,1.20]$ por cajas (parte C).
- **L13** (no ligado en caja con $a_s$): cubierto por el veredicto de $\delta=1.20$ (parte C) y por L19.
- **L15** con PIGS cerca del umbral y **L17** con suavizado: no se usa suavizado (el método aprobado no lo necesita); el peso de la transferencia es real, positivo y finito (`11_transferencia.json`, `peso`: 0 negativos, 0 no finitos).

## Decisiones pendientes de firma (Juan Sebastián)

1. Redefinir el control de tabulación de 9.7 como Richardson en $h$ con exponente 4 y estabilidad del valor extrapolado (sección 11.4).
2. Si la anomalía de $\tau=5$ queda cerrada con las réplicas y la combinación (parte A; sección 12).
3. El umbral 0.1 de la desviación de la ley de caja para "no ligado" (sección 14.5).
4. El tratamiento del pozo con orden $\epsilon^{3/2}$ y extrapolación en $h$ de orden ~1 (sección 13).
5. Si se corrige la pared en $R$ (imagen en $R$ o $R_{\rm ef}$) en las Fases 3 y 4, o se mantiene el término de pared en el error (sección 14.4).
6. Si se acepta la corrección de Wigner-Kirkwood de $U_C$ fuera de $r=10$ como parte del método (sección 11.9).

## Figuras congeladas (Fase 2)

Huella sha256 de cada figura tal como quedó tras las ejecuciones de V3 (los 16 primeros caracteres; las completas en `resultados/16_tabla_controles.json`). Para regenerar una figura se ejecuta su script; si la huella cambia, la figura cambió.

| Figura | Script que la produce | sha256 |
|---|---|---|
| `figuras/10_radial_convergencia.png` | `10_radial_controles.py / test_radial.py` | `491ff66a7544f608…` |
| `figuras/11_proyeccion.png` | `11_transferencia_controles.py` | `b809c40644529191…` |
| `figuras/11_trotter.png` | `11_transferencia_controles.py` | `476702c17f0e5837…` |
| `figuras/12_pigs_delta02.png` | `12_pigs_produccion.py` | `e3d5f2cca7fff770…` |
| `figuras/12_pigs_tau.png` | `12_pigs_produccion.py` | `7399461fe6fa5c70…` |
| `figuras/13_controles.png` | `13_controles_hulthen_pozo.py` | `75701285ebfd3c6a…` |
| `figuras/14_cajas.png` | `14_criterio_cajas.py` | `034fa76e59c81b8b…` |
| `figuras/15_limites.png` | `15_limites.py` | `9fb3fa2123810162…` |

## Firma

| Rol | Nombre | Fecha | Firma |
|---|---|---|---|
| Verificación | Juan Sebastián Calixto | | (pendiente) |
| Implementación | Luis Felipe Ramírez | | (pendiente) |
