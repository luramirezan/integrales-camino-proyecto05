# Verificación de E5: comprobaciones independientes y relectura del código

Todas las cifras salen de `resultados/*.json` (entre paréntesis, el archivo).

## 1. Segundos métodos y casos exactos

| Qué se comprueba | Cómo | Resultado |
|---|---|---|
| a(δ) | Tres métodos independientes: disparo lineal DOP853 (M1), fase variable de Calogero (Riccati, M2), Nyström de la ecuación integral (M3), más `comun3.long_dispersion` de la Fase 3 | M2 y M3 coinciden con M1 a ≤ 1.7e-11 relativo en los 7 δ; a(1.20) = −142.9349, frente a −142.9 de la Fase 3 (01) |
| Perfil φ(r) | Disparo frente a Nyström | Diferencia relativa 1.0e-6 en δ = 1.2 con 600 paneles, 1.4e-7 con 1200 (08): el control C3 no pasa en δ = 1.2 y 1.3 por el método de control, que converge al refinar |
| Ley de Λ | Caso exacto de Ciesielski–Taylor (pozo cuadrado, φ(0) = 1/cos√(2p)), derivado aquí | p_k y w_k (k = 1…5) con error ≤ 9.9e-12 (01) |
| Polos | δ/p_1 y δ/p_2 frente a δ_c(1s) y δ_c(2s) | 1.190612421060 y 0.3102092827 en los 7 δ (01) |
| Identidad del estimador | a = −(2/δ²) E_Γ[φ] por Gauss–Laguerre | ≤ 4.7e-12 (01) |
| Pendiente c = −d(1/a)/dδ en δ_c | Diferencias finitas de la EDO | 0.7413, igual a la pendiente 0.741 de κ de la Fase 3 (01): 1/a es analítica a través del umbral |
| E[Λ] exacto | S(r) en forma cerrada (G_0 q); E_Γ[δΛ] = 1 | MC con η ≤ 0.4: compatible (02, 03); partida r_0 = 1 en δ = 2: 0.43211 ± 0.00053 frente a 0.43233 (08) |
| E[W²] (δ = 4) | Gauge de 2q por EDO | MC 2.2053 ± 0.0058 frente a 2.2069 (08); varianza relativa 0.2054 frente a 0.2071 |
| Covarianza de escala | Misma semilla, δ = 1 y 2.7 | δΛ idénticos hasta 5.6e-15 (08) |
| Pesos del MI ≤ φ_T(r_0) | Partida fija r_0 = 0.5, δ = 1.5, η = 0.1 | máx Y = 6.668289 ≤ φ_T = 6.693432; varianza relativa 0.0234 ≤ cota 0.1927; media 5.60619 ± 0.00271 frente a 5.61188 (08) |
| θ independiente de la partida | Partida fija r_0 = 1 en δ = 1.5 | θ = 1.2557 ± 0.0089 frente a 1.2599 (03) |
| C11 a tamaño finito | El mismo estadístico sobre 10 muestras de la ley exacta | δ = 1.5: +0.616 ± 0.086 (MC +0.784, z = +1.97); δ = 2: +0.262 ± 0.039 (MC +0.343, z = +2.06) (03). El MC es compatible con la ley exacta a ~2σ; lo que falla es la comparación con la pendiente asintótica |

## 2. Lo que encontramos al revisar (y cambió el trabajo)

1. **El trapecio da media infinita.** El primer simulador usaba dt[q(r) + q(r')]/2. En δ = 3 dio a ≈ −10^{239}. La
   causa (Proposición 3 de `teoria.md`) es que el extremo r' cae cerca del origen con densidad ∼ r'² y e^{C/r'} no es
   integrable. Se cambió a la media exacta sobre el puente browniano (forma cerrada del Yukawa promediado sobre una
   gaussiana), que además da un estimador dominado por el exacto (Jensen condicional). La forma cerrada se comprobó
   contra cuadratura numérica en una prueba de desarrollo (no guardada en JSON): diferencia ≤ 1e-14 en seis puntos,
   salvo 1e-7 en R/σ = 7e-4 con el primer umbral del límite R → 0; desde entonces ese límite se usa solo si R/σ < 1e-5.
2. **Euler 3D en la difusión guiada.** Con el Euler de la deriva ∇ ln φ_T en 3D, las dos derivas grandes (+1/r de
   Bessel-3 y ≈ −1/r de la guía) se discretizan por separado. Se pasó a un paso híbrido (imagen radial 1D con la deriva
   total pequeña para r ≥ 1/δ_T).
3. **Orden de la extrapolación del MI.** La regla de 04 promedió órdenes preasintóticos (p = 3.20); el extrapolado de
   δ = 3 quedó a +3.85σ. El par más fino (η = 0.1/0.05) da 1.93 y el error de Euler es O(η²); con p = 2 (`04b`) los
   seis extrapolados quedan entre −0.19σ y +1.78σ. Esta revisión se hizo después de ver los datos; la tabla de
   controles evalúa C13 con la regla original (σ = estadística + sesgo medido) y pasa en los cinco δ.
4. **Guías que no son supersoluciones amplifican el sesgo.** Con δ_T = 1.8 > δ = 1.5, el sesgo de a con η = 0.2 es
   +3.9 %, y el exponente de la cola sale 2.30 ± 0.07 frente a 2.47 predicho; con η = 0.1 baja a +0.70 % y θ = 2.43 ± 0.08
   (08). Con la supersolución el sesgo de η = 0.2 es ≈ 0.5 %. Lo atribuimos a que los pesos > 1 hacen la media sensible
   a la cercanía de la criticidad efectiva del esquema discreto.
5. **Marca de camino truncado.** El núcleo guiado marcaba los caminos truncados con L = −1, que es un valor legítimo
   cuando E_L < 0 (guías con δ_T > δ). Se cambió a NaN. No afecta a 04 (allí E_L ≥ 0 y no hubo truncados).
6. **C15 en δ = 1.2 con η = 0.1:** N = 7007 no alcanza para 10 bloques de 2000; se usa la corrida con η = 0.2.

## 3. Relectura del código (17-11-2026)

Se releyó `fk_comun.py` y los scripts 01 a 08 línea por línea. Puntos comprobados:

- Frobenius: u = r − p r² + … para q ∼ 1/r; con r_0 = 1e-10 el error es despreciable también para el pozo cuadrado y
  para q_eff con coeficiente distinto en 1/r.
- `Guia`: b = (u/r)'/(u/r) = u'/u − 1/r y b1 = u'/u; en r = 0 se copia el valor del segundo nodo (la cancelación en
  r = 1e-9 da ruido). Fuera de R_in se usa la forma analítica 1 + A/r; el índice de la tabla nunca pasa de n_tab porque
  r ≤ R_in siempre (los caminos que salen se reinyectan exactamente en R_in o terminan).
- Cierre: probabilidad de volver R_in/r (libre) y (R_in + A)/(r + A) (guiado, función armónica de la transformada h).
- E_L = e^{−δ_T r}(1 − e^{−(δ−δ_T) r})/r con `expm1`: estable en r → 0 (límite δ − δ_T) y válida para δ_T > δ.
- Semillas: todas fijas y distintas por corrida (tabla en los JSON); el piloto que fija N en 04 y 05 también es
  determinista.
- Unidades: dt = η²r² con η adimensional; R_in = 36/δ (q(R_in) < 1e-16/R_in).

## 4. Cifras citadas en LEEME.md y seccion_articulo.md

Se comprobaron una por una contra los JSON después de la última corrida (17-11-2026). Las de la tabla de controles las
escribe `07_controles.py` directamente.
