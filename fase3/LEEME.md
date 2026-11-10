# Fase 3 del proyecto 05: barrido en el apantallamiento, prueba de cajas y convergencia

Juan Sebastián Calixto y Luis Felipe Ramírez · 10 de noviembre de 2026 · cálculo y redacción: Claude (IA), con las decisiones del equipo del 10-11-2026 (todas las recomendaciones de `fase2/decisiones_fase2.md`, sujetas a la firma de Juan Sebastián).

## Lo que pide la guía y dónde está

| Pedido (guía, proyecto 05, Fase 3) | Dónde |
|---|---|
| Barrer μ (δ a g fijo) | `codigo/21_barrido_delta.py` → figura `23_barrido_delta.png` |
| Barrer el tamaño de caja | `codigo/20_cajas_fase3.py`, `20b`, `20c`, `20d` → figuras `23_cajas.png` y `23_delta119.png` |
| Estudiar la convergencia temporal | `codigo/22_convergencia.py` → figura `23_convergencia.png` |
| Auditoría adversarial de autovalores cercanos a cero (otra IA) | `auditoria_gemini/` (Gemini 3.1 Pro en la app) |
| Borrador del artículo | `articulo/borrador_articulo.md` y `.pdf` |
| Figuras con barras de error | `figuras/` (script `codigo/23_figuras.py`) |
| Tabla de controles | `secciones/24_tabla_controles.md` (script `codigo/24_tabla_controles.py`) |
| Presentación de las Fases 2 y 3 | `presentacion/diapositivas_fase2_3.pptx` y `.pdf`, guion `guion_fase2_3.md` |

## Resultados

- **Convergencia:** orden de Trotter de 1.96 a 1.99 y orden de malla de 4.00 en δ = 0.2, 0.8, 1.0 y 1.15. El extrapolado queda a ≤ 5×10⁻⁹ del radial. El sesgo con ε = 0.1 crece de 4×10⁻⁷ a 7×10⁻³ de |E0| hacia el umbral.
- **Barrido:** en 8 valores de δ la integral de camino es igual al radial, con una diferencia máxima de 1.8×10⁻⁸. Cerca del umbral, κ ≈ 0.741 (δc − δ), es decir E0 ∝ −(δc − δ)², y ⟨r⟩κ → 1/2.
- **Cajas** (5 δ × 7 R, de 50 a 3200): las 35 celdas son compatibles. 1.15 y 1.18 salen ligados; 1.20 y 1.25, no ligados. Resultado: **1.18 < δc < 1.20 con los dos métodos y la condición (c)**.
- **δ = 1.19:** E0 cambia de signo entre R = 1600 y 3200. Con el radial (h = 1/160) hasta R = 25600 sale ligado, con E0 = −1.03×10⁻⁷ y ⟨r⟩ = 1102. La transferencia en R = 6400 y 12800 (script 26, LU en banda de LAPACK en vez de shift-invert disperso, N hasta 640 000) da −1.003×10⁻⁷ ± 2.2×10⁻⁸ y −1.014×10⁻⁷ ± 2.3×10⁻⁸, compatibles con el radial. En la terna 3200/6400/12800 los dos métodos dan ligado y la condición (c) se cumple. Resultado: **1.19 < δc < 1.20 con los dos métodos y (c)**.
- **Sin caja ni malla** (script 25): el disparo desde Frobenius da E0(1.19) = −1.0303×10⁻⁷; la longitud de dispersión a energía cero cambia de signo entre δ = 1.1906 (+1.1×10⁵) y 1.1907 (−1.5×10⁴), así que 1.1906 < δc < 1.1907.
- **Controles:** 34 distintos; 23 pasan, 3 no pasan (los tres con causa medida) y 8 medidos.

## Cómo reproducir (desde `fase3/codigo/`; usa los módulos de `fase2/codigo/` sin cambiarlos)

```
export OMP_NUM_THREADS=1
NPROC=3 python 20_cajas_fase3.py      # ~331 s con 3 procesos
python 20b_umbral_119.py               # radial de delta = 1.19 hasta R = 51200 (h = 1/40)
python 20c_umbral_119_fino.py          # idem con h = 1/160, R hasta 25600
python 20d_diagnostico_pared.py
NPROC=3 python 21_barrido_delta.py
python 22_convergencia.py
python 25_respuesta_gemini.py          # comprobaciones de los hallazgos de Gemini (~10 min)
python 26_transferencia_grande.py      # transferencia en R = 6400 y 12800 (LU en banda, ~5 min)
python 23_figuras.py; python 24_tabla_controles.py
python ../presentacion/generar_diapositivas_f23.py
```
Las salidas impresas están en `resultados/*_salida.txt`. Todo es determinista (sin números aleatorios).

## Registro de IA de la Fase 3 (formato del curso)

| ID | Fecha | Consulta | Respuesta utilizada | Decisión humana | Comprobación | Corrección posterior |
|---|---|---|---|---|---|---|
| F3-01 | 10-11-2026 | Lucho: "necesito que hagas la fase 3 y dejes todo listo para la presentación de mañana" (acepta todas las recomendaciones si Juan Sebastián también) | Scripts 20 a 24, figuras, tabla, borrador y diapositivas | Decisiones 1, 3 y 5 de la Fase 2 aprobadas por Lucho; falta la firma de Juan Sebastián | Reproduce bit a bit una celda de la Fase 2 (δ = 1.18, R = 200: −2.4076630903×10⁻⁵); controles de la sección 24 | — |
| F3-02 | 10-11-2026 | (IA) δ = 1.19 indeterminado con R ≤ 3200 | Extender el radial a R = 51200 | Pendiente de confirmar por el equipo | Con h = 1/40 la condición (a') falla por la malla (error de 16 % de \|E0\|); con h = 1/160 baja a 3.7 % y sale ligado | 20c sustituye a 20b para el veredicto |
| F3-03 | 10-11-2026 | (IA) orden de Trotter bajo en cajas que tocan la pared | Diagnóstico 20d | Pared solo en el error (decisión 5) | 9/9 celdas vuelven a 1.98–1.99 comparando con el radial en R + 0.5826√ε | — |
| F3-04 | 10-11-2026 | Auditoría adversarial de autovalores cercanos a cero con Gemini 3.1 Pro (app, selector "Detailed research · 3.1 Pro"), chat nuevo; material en `auditoria_gemini/trozos/`, prompts y respuestas literales en `auditoria_gemini/conversaciones/G.md` | 7 hallazgos (G1 a G7, abajo). Gemini declara que no ejecuta código | Ninguno se acepta sin calcular. Se responde con `respuestas/G_r2.md` y se pide la tabla de cierre (`trozos/G_cierre.md`) | Scripts 25 y 26 (tabla de controles, filas B4, B5 y E1 a E4) | G7 era válido y cambió el trabajo: se añadió la transferencia en R = 6400 y 12800 |

**Supuesto declarado:** la implementación de la Fase 3 la hizo la IA. Por la rotación de roles (9.12), verifica Luis Felipe.

### Hallazgos de la auditoría F3-04 y su comprobación

| ID | Hallazgo de Gemini (resumen) | Gravedad (Gemini) | Comprobación | Estado |
|---|---|---|---|---|
| G1 | El error de malla del radial en el origen fabrica un falso ligado en δ = 1.19 | Alta | Orden de la malla 1.84, 1.96, 2.11 (h = 1/40 a 1/640). El sesgo va hacia arriba: h = 1/40 da E > 0. El disparo sin malla da E0 = −1.0303×10⁻⁷ | Refutado |
| G2 | El orden de Trotter de 1.1 a 1.5 rompe la extrapolación ε² | Alta | Con la pared en R + 0.5826√ε el orden vuelve a 1.975–1.993 (9/9). La extrapolación con p_obs queda dentro de la barra | Refutado |
| G3 | Un ligado ultradébil en δ = 1.20 pasaría la ley de caja | Media | Sturm sin caja: 0 nodos y a_s = −142.9. La desviación de la ley sigue bajando hasta el redondeo (1e-12) | Refutado |
| G4 | El cambio de signo entre R = 1600 y 3200 es un cruce numérico | Media | El cruce R_c(h) = 3692, 2451, 2261, 2218 converge a a_s = 2203.8 (sin malla) | Refutado |
| G5 | La suma lineal de errores subestima | Media | La suma lineal acota la cuadrática. Un ajuste 2D en (h, ε) da barras 2 a 3 veces menores que la receta, con el mismo signo | Refutado |
| G6 | Monotonía y F½ > 0.95 fuerzan un falso "no ligado" | Baja | Con el umbral en 0.75/0.85/0.95 los veredictos no cambian. En δ = 1.19 decide la condición (a), no F½. Ninguna celda da un "no ligado" falso | Refutado |
| G7 | Concluir [1.19, 1.20] abandona la condición (c) para R > 3200 | Baja | Era cierto. Transferencia en R = 6400 y 12800 compatible; terna 3200/6400/12800 ligada con los dos métodos y (c) | Válido, resuelto |

Errores de Gemini, aparte de los hallazgos:
- leyó como violación de Perron un −2.8×10⁻¹⁶, que es redondeo en las componentes junto a la pared;
- supuso una matriz densa para h = 0.04 en R = 12800, cuando es de banda con N = 320 000.

**Cierre (10-11-2026).** Gemini marcó los 7 hallazgos como "resuelto por la respuesta" y no dejó nada pendiente. Las dos respuestas están literales en `conversaciones/G.md` (mensajes 9 y 10).

Números que Gemini dice haber calculado a mano, recalculados aquí:
- F½ de un estado libre en la caja es 0.5. **Correcto**: para sin²(πr/R), la mitad del peso cae en r < R/2.
- Ley de caja en δ = 1.20 con a_s = −142.93: E_ley(800) = 5.55×10⁻⁶ y E_ley(3200) = 4.41×10⁻⁷. **Correcto** (5.5502×10⁻⁶ y 4.4159×10⁻⁷).
- Desviación en R = 800 de 0.021. **Correcto**.
- Desviación en R = 3200 de 0.00045. **Cerca**: medimos 5.3×10⁻⁴ (h = 1/160) y 0.001 (h = 1/40, script 20).
- Con p = 1.144, 1/(2^p − 1) ≈ 0.82. **Correcto** (0.826).
- ΔE ≈ −2.24×10⁻⁷ entre R = 1600 y 3200 en δ = 1.19. **Correcto** (−2.243×10⁻⁷ con el radial).

Errores de Gemini en el cierre, que no se aceptan:
- Dice matrices de 320 000 × 320 000; la mayor es N = 640 000 (R = 12800, h = 0.02).
- Dice que el término de pared "capta la perturbación" en el valor central. En nuestra receta, la pared solo se suma a la barra de error (decisión 5) y el valor central no se corrige.
- Habla de la desviación de δ = 1.20 "estabilizada en ~10⁻⁶". En realidad baja hasta 1.0×10⁻⁶ en R = 12800 y después sube por redondeo.
