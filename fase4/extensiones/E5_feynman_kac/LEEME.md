# E5 · Umbral sin caja con caminos brownianos: gauge de Feynman–Kac y longitud de dispersión

*Proyecto 05, Fase 4 / entrega final · 17-11-2026 · hecho por Claude (IA) por delegación de Lucho; pendiente de la
revisión del equipo (Juan Sebastián Calixto y Luis Felipe Ramírez).*

## Qué pregunta responde

¿Se puede decidir "ligado o no ligado" **sin caja y sin tiempo de proyección**, con caminos brownianos? Para δ > δ_c,
la solución de energía cero normalizada a 1 en el infinito es φ(x) = E_x[exp ∫_0^∞ q(B_t) dt], con q = e^{−δr}/r, y la
longitud de dispersión sale de un promedio de pesos: a = −(2/δ²) E[W] con la partida r_0 ∼ Γ(2, 1/δ). Cuando δ → δ_c⁺,
a → −∞. La extensión estudia si esto sirve como método numérico, dónde falla y cómo se arregla.

## Resultados principales

1. **Teorema (demostrado en `teoria.md`).** E[W^p] < ∞ si y solo si p < δ/δ_c. La varianza del estimador libre es
   infinita en toda la ventana **δ_c < δ ≤ 2δ_c ≈ 2.381**, incluida la igualdad. La prueba usa la fórmula de momentos de
   Kac [Fitzsimmons y Pitman 1999, V] y el operador de Birman–Schwinger; no depende del teorema de la gauge en ℝ^d de Zhao
   (1992), del que solo pudimos verificar el resumen.
2. **Ley exacta del funcional (derivada aquí, un paso sin demostrar):** P(Λ > λ) = Σ_k w_k e^{−p_k λ} con
   p_k = δ/δ_c(ks). La cola del peso es P(W > w) ≈ w̄_1 w^{−θ}, **θ = δ/δ_c**, con w̄_1 = 0.80317 universal para la partida Γ.
   El código reproduce el caso exacto de Ciesielski–Taylor (tiempo en la bola, φ(0) = 1/cos√(2p)) a 1e-11.
3. **θ medido frente a δ/δ_c.** Tasa de la cola de X = δΛ: κ̂ = 0.84160 ± 0.00266 frente a 1/δ_c = 0.83990 (+0.64σ);
   como la ley de X no depende de δ, θ̂(δ) = δκ̂: 1.2624 ± 0.0040 en δ = 1.5 (predicho 1.2599), 1.6832 ± 0.0053 en δ = 2
   (1.6798), 2.5248 ± 0.0080 en δ = 3 (2.5197) y 3.3664 ± 0.0106 en δ = 4 (3.3596). Con partida fija r_0 = 1 (corrida
   independiente), θ̂ = 1.2557 ± 0.0089 en δ = 1.5. Kolmogorov–Smirnov de la ley completa: √N·D = 1.11 con N = 10⁷.
4. **Colas pesadas visibles.** En δ = 1.5, un solo camino lleva la media acumulada a 3.70 veces el valor exacto en
   n ≈ 9.4×10⁵ y al final (n = 10⁷) sigue 1.25 veces por encima; la varianza muestral crece con n (pendiente +0.78).
5. **Precisión del MC libre donde la varianza es finita** (N = 10⁷, extrapolado en η con el orden 4 medido):
   a(3) = −0.343302 ± 0.000086 frente a −0.343241 de la EDO (−0.70σ, 2.5×10⁻⁴ relativo) y a(4) = −0.169020 ± 0.000023
   frente a −0.169017 (−0.12σ). φ(r) en 7 radios para δ = 3 y 4: todos dentro de 1.37σ.
6. **Discretización.** El trapecio da media infinita para todo paso (demostrado; en la práctica, a ≈ −2.4×10^{145}). El
   esquema de puente (media exacta de ∫q sobre el puente browniano) está dominado por el estimador exacto; su sesgo es O(η⁴) según un argumento heurístico (los datos excluyen el orden 2, no fijan el 4; revisión R5-03).
7. **Remedio: transformada h de Doob con una supersolución.** Con φ_T = solución de energía cero de δ_T tal que
   a_T = 1.25a, los pesos están en (0, 1] y la varianza relativa queda acotada por φ_T/φ − 1. Medida: 0.026 (δ = 3) a
   0.30 (δ = 1.1907), siempre por debajo de la cota (≤ 0.556). a con importancia frente a la EDO: δ = 1.5, 1.3, 1.25, 1.2
   a +1.32σ, +0.81σ, −0.19σ, +0.66σ (extrapolado con p = 2); y cerca del umbral, con η = 0.2:
   a(1.195) = −306.0 ± 2.4 (EDO −306.7), a(1.192) = −975 ± 9 (−971.5), a(1.1907) = −15890 ± 420 (−15404.5).
8. **Costo.** Pasos por camino ∝ |a_T|^{0.98} ≈ 1/(δ − δ_c): 2.2×10⁶ pasos por camino en δ = 1.1907. Es el análogo, a
   energía cero, del tiempo de proyección ∝ 1/|E_0| de PIGS: el tiempo físico de difusión crece igual, como
   (δ − δ_c)^{−2}, y la reducción a ∝ (δ − δ_c)^{−1} pasos la da el paso adaptativo dt = η²r² (argumento de escala;
   revisión R5-04). La transferencia de la Fase 3 no usa τ: su costo crece con la caja.
9. **Peso real, positivo y normalizable** (pedido del curso), por variante: tabla en `teoria.md`, sección 8.

## Cómo reproducir (desde `codigo/`, un proceso, `OMP_NUM_THREADS=1`)

Necesita numpy, scipy, matplotlib y **numba** (`pip install numba`; los núcleos de Monte Carlo están compilados).

```
python 01_referencia_edo.py      # EDO, ley exacta, mapas de varianza            ~4.5 min
python 02_validacion_mc.py       # MC libre: validación en delta = 3, 4; sesgo   ~11 min
python 03_colas.py               # colas, theta, KS, varianza frente a n          ~4 min
python 04_importancia.py         # muestreo por importancia, sesgo en eta        ~14.5 min
python 04b_extrapolacion.py      # extrapolación revisada con p = 2              < 1 s
python 05_cerca_umbral.py        # delta hasta 1.1907; guías que no son supersol. ~8.5 min
python 08_verificacion.py        # comprobaciones independientes                 ~2.5 min
python 06_figuras.py; python 07_controles.py
```

Todo es determinista (semillas fijas, listadas en los JSON). Los tiempos son de la máquina compartida del 17-11-2026.

## Archivos

- `teoria.md`: enunciados, pruebas, qué está demostrado y qué no; comparación con PIGS y con Edwards et al.
- `seccion_articulo.md`: sección para el artículo final.
- `controles.md`: 43 filas (34 pasan, 4 no pasan con causa medida, 1 no aplicable, 4 informativas).
- `criterios_previos.md`: criterios fijados antes de correr (con su adenda).
- `fuentes.md`, `registro_ia.md`, `verificacion.md`.
- `figuras/`: e5_01 φ(r) MC frente a EDO; e5_02 a(δ); e5_03 histogramas de W; e5_04 θ medido frente a predicho;
  e5_05 varianza y media acumulada frente a n; e5_06 muestreo por importancia; e5_07 mapa de guías; e5_08 ley de X;
  e5_09 sesgo frente a η.

## Decisiones que tomé (para que el equipo las revise)

| # | Decisión | Motivo |
|---|---|---|
| E5-D1 | Estimar a con a = −(2/δ²)E[W], partida Γ(2, 1/δ), y no con φ en un radio grande | Un solo peso por camino; la varianza no crece con el radio |
| E5-D2 | Esquema de puente en vez del trapecio | El trapecio tiene media infinita (demostrado) |
| E5-D3 | Probar la ventana de varianza infinita por Kac + Birman–Schwinger | No pudimos leer el enunciado completo de Zhao 1992 |
| E5-D4 | Guía = solución de energía cero de un δ_T < δ (a_T = 1.25 a) | Es supersolución: pesos ≤ 1 y cota explícita de la varianza |
| E5-D5 | Revisar la extrapolación del MI a p = 2 en `04b` y decirlo | La regla de 04 usaba órdenes preasintóticos (δ = 3 a 3.85σ) |
| E5-D6 | Usar numba | El esquema de puente con numpy era ~8 veces más lento |
| E5-D7 | No hacer aquí la auditoría con Gemini | No estaba en el encargo de E5; D4 la deja para un paso aparte |

## Qué quedó sin hacer

- La convergencia absoluta Σ|w_k| < ∞ de la ley de mezcla (Proposición 2) no está demostrada.
- El criterio general para guías con E_L de signo variable descansa en el resumen de Zhao 1992; no leímos el enunciado.
- La difusión guiada usa Euler en la deriva (sesgo O(η²), 0.5 % con η = 0.2); un paso con aceptación de Metropolis o
  un integrador de orden 2 permitiría pasos mayores cerca del umbral.
- No hay MI del lado ligado (δ < δ_c): allí la gauge es infinita y habría que trabajar con E < 0.
- Auditoría externa con Gemini pendiente.
