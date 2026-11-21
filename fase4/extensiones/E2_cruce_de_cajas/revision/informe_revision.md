# Revisión adversarial R2 de la extensión E2 (criterio de cruce de cajas)

*Revisor independiente (agente de Claude, 17-11-2026). No escribí E2; busqué errores. Todo el código de la revisión está en
`revision/` y no usa `e2comun` ni DOP853. Un proceso, `OMP_NUM_THREADS=1`. Cifras de `revision/resultados/*.json`.*

## Cómo reproducir (desde `revision/`)

| Script | Qué hace | Tiempo |
|---|---|---|
| `espectral.py` | Solucionador propio: elementos espectrales de Chebyshev (N = 32, 28 elementos) en [0, 40] marchando u(0) = 0, u'(0) = 1, cuadratura de Clenshaw-Curtis; fuera, solución libre exacta sin/sinh(k(R − r)); E₀ por brentq sobre el empalme | módulo |
| `r01_recalculo.py` | 24 celdas E₀ y ⟨r⟩/R; los 12 cruces sin rejilla (brentq directo en δ); δ_c, r_e, m₁, c; ajuste α, β; corrimiento de los cruces por una pared en R + c_w | 88 s |
| `r02_series_sympy.py` | Series de `teoria.md` con sympy | 5 s |
| `r03_transferencia_celdas.py` | 3 celdas crudas con `comun3.resolver_tr` y 1 completa con `comun3.celda`, frente a los JSON | 4 s |
| `r04_mecanismo_trotter.py` | El error de Trotter como corrimiento del umbral | 15 s |
| `r05_impacto.py` | Método B de ⟨r⟩/R con término de pared; δ = 1.19 con pocas cajas | 1 s |

## Lo verificado (sin hallazgo)

- **Teoría, a mano y con sympy (`r02`).** y(z, ε) = 1/4 − 2z/π² + ε/4 − 4z²/π⁴ − zε/π² + 3ε²/16; z* = −π²ε/16 − 3π²ε²/32;
  y* = 1/4 + 3ε/8 + 27ε²/64; G(0) = 1/2 − 2/π², dG/dz = 2(π² − 12)/π⁴, K = 1/4 + 1/π², k₁ = π²(4 + π²)/(16(π² − 12)) =
  −4.0159. Todo coincide con `teoria.md`. Los signos de la condición (u ∝ sin(kr + η), k cot η = −1/a + r_e k²/2,
  a > 0 ligado) son correctos.
- **¿Por qué 1/R² y no 1/R?** El cruce fija z* = R/a* = O(r_e/R), así que 1/a* = O(r_e/R²) y δ* − δ_c = O(R⁻²); el término
  r_e/(4R) de y no se cancela, pero se compensa con un z de orden 1/R. Correcto.
- **Comparación con E3.** Para R₁, R₂ = qR₁ sympy da R₁/a* = −π²ε/(8q), es decir 1/a* = −π²r_e/(8R₁R₂), la fórmula de E3. Con
  R₂ = 2R₁ es exactamente π²r_e/(16cR²). Son la misma.
- **Constantes (`r01`, otro método).** δ_c = 1.1906124210736 (a 1.3×10⁻¹¹ de la referencia); r_e = 1.7806319 (E2:
  1.7806317); c = 0.7411917 (E2: 0.7411918); m₁ = 0.6501843; a(1.19) = 2203.81. α_y = 1.48192, β_y = 3.9581, α_ρ = 9.6478.
  El coeficiente 9.648 de ⟨r⟩/R es correcto.
- **Celdas (`r01`).** 24 celdas (δ de 1.185 a 1.196, R = 50 a 3200): |ΔE₀|/|E₀| ≤ 8.2×10⁻⁸ (el peor, δ = 1.19, R = 3200,
  donde E₀ ≈ −7×10⁻⁸ cruza el cero; en las demás ≤ 3×10⁻⁸) y |Δρ| ≤ 1.7×10⁻⁹ frente al disparo de E2.
- **Los seis cruces del disparo, sin rejilla.** y: 1.191237549734, 1.190764615805, 1.190649966576, 1.190621745069,
  1.190614744311, 1.190613000909; diferencia con E2 entre +1.1×10⁻¹¹ y +2.0×10⁻¹¹. ρ: diferencia ≤ 3.5×10⁻¹¹. Cocientes
  4.125, 4.062, 4.031, 4.016 (y) y 4.039, 4.021, 4.011, 4.005 (ρ). Ajuste α/R² + β/R³ (R ≥ 100): δ_c = 1.1906124213
  (α = 1.4817, β = 4.026) y 1.1906124202 (α = 9.6485). Idénticos a E2.
- **Pared de la transferencia.** Con el cruce exacto en cajas R + c_w (c_w = 0.11229) el corrimiento en 400/800 es
  −1.183×10⁻⁶; la fórmula de primer orden da −1.168×10⁻⁶. Confirmada. Lo medido por el método B es 79 % a 92 % de lo
  predicho en los pares 50 a 400 (resto de Trotter y malla, dentro de la barra B).
- **Integral de camino (`r03`).** Las tres celdas crudas (δ = 1.1906, R = 50, h = 0.04, ε = 0.1; δ = 1.19, R = 200, h = 0.02,
  ε = 0.05; δ = 1.1912, R = 400, h = 0.04, ε = 0.2) y la celda completa δ = 1.1903, R = 100 (E_mejor y barra) son idénticas
  bit a bit a los JSON de E2; ⟨r⟩/R a 4×10⁻¹³.
- **Controles que no pasan.** K2: causa en R = 50 correcta (pared); en R = 3200 correcta pero incompleta (ver R2-03). K7: el
  añadido de 8 nodos está fechado en `criterios_previos.md` (21:20), el umbral 10⁻⁸ no cambió y K7 con la rejilla inicial
  sigue en la tabla como "no pasa". Los nodos no cambian el umbral físico: mis cruces sin rejilla coinciden con los de E2 a
  2×10⁻¹¹. K11: la causa (a δ fijo z crece con R; en el lado ligado la corrección es −z³r_e/(π²R)) la rehice:
  q coth q ≈ q da q ≈ z + εz²/2 y y − F ≈ −εz³/π², 0.1318 en δ = 1.185, R = 3200. Se reporta como "no pasa" con la frase
  "el criterio estaba mal planteado; no se cambia", que es la forma honesta.
- **Diez intervalos.** Todos contienen la referencia y, por par, las barras cubren la diferencia con el cruce exacto en
  disparo, radial, A y B de y. Los del disparo (1.6×10⁻⁹, 2.0×10⁻⁹) los confirma mi ajuste independiente (desvíos
  +2.7×10⁻¹⁰, −8.2×10⁻¹⁰). Excepción: B de ⟨r⟩/R (R2-01).

## Hallazgos

| ID | Gravedad | Descripción | Evidencia numérica | Corrección |
|---|---|---|---|---|
| R2-01 | Media | El método B de ⟨r⟩/R no tiene término de pared (la receta de la Fase 3 para ⟨r⟩/R tampoco lo tiene), pero la pared sin imagen sí corre el cruce de ⟨r⟩/R, y hacia arriba | Corrimiento exacto por la pared: +2.27×10⁻⁴, +5.40×10⁻⁵, +1.32×10⁻⁵, +3.3×10⁻⁶ (pares 50 a 400). B − exacto: +2.07×10⁻⁴, +4.89×10⁻⁵, +1.17×10⁻⁵, +2.6×10⁻⁶. Las barras B por par (1.24×10⁻⁴, 3.73×10⁻⁵) **no cubren** los pares 50/100 y 100/200 | `r05`: sumando el término, la barra final pasa de 1.47×10⁻⁵ a 1.57×10⁻⁵ e intervalo [1.19059638, 1.19062781] (contiene la referencia). Anotado en `seccion_articulo.md` y `LEEME.md`. No se tocó `05_cruces.py` para no mover las 43 cifras clave del texto; hay que integrarlo si B de ⟨r⟩/R se usa en el artículo <br>**Estado: corregido** (E2-09 en `registro_ia.md`): `codigo/04b_pared_rho.py` + `05_cruces.py` integran el término con la receta de la Fase 3 (solo en la barra); el JSON nuevo da barra 1.57×10⁻⁵ e intervalo [1.19059638, 1.19062781], igual a este recálculo a 1.0×10⁻⁹; barras por par 3.51×10⁻⁴ y 9.12×10⁻⁵ en 50/100 y 100/200, que ya cubren |
| R2-02 | Media (ya corregida en paralelo) | "La prueba de cruce clasifica δ = 1.19 como ligado con R = 50 y 100": con r_e > 0 cada cruce es una cota superior de δ_c, y δ < δ* no implica ligado | La encontré yo y, a la vez, la auditoría con Gemini; el otro agente añadió `13_cruce_corregido.py` (δ* − α/R² − β/R³). Comprobé por otra vía (`r05`): Richardson con R = 50, 100, 200: B 1.190608 ± 7.4×10⁻⁵, A 1.190608 ± 2.3×10⁻⁴, los dos > 1.19 | Sin acción extra. Matiz: para la integral de camino el α correcto es α − π²c_w/(8c) = 1.295 (pared), que da 1.190644 en vez de 1.190537 en el par 50/100; las dos sirven |
| R2-03 | Baja (explicación) | El texto explicaba por qué A es unas 10 veces más ancho que B sin el mecanismo. Lo medí: el error de Trotter es un corrimiento del umbral s_ε = 6.09×10⁻⁴, 1.53×10⁻⁴, 3.78×10⁻⁵ (ε = 0.2, 0.1, 0.05; ley ε²). E₀ exacto en δ − s_ε reproduce el E₀ crudo a ≤ 0.4 % de \|E₀\| aunque el error crudo sea −165 %. En E₀ entra a través de z (c R s_ε = 1.44 en R = 3200), en la zona curva de F(z): la ley ε² de cada celda se rompe (K2 en R = 3200) y la barra crece como R². En el cruce es un corrimiento lineal e independiente de R | `r04_mecanismo_trotter.json` | Párrafo añadido en `seccion_articulo.md`. Conclusión: **B es legítimo** (la expansión de δ*(h, ε) tiene los mismos órdenes y además es lineal) y sus barras por par de y cubren el error real en los seis pares (cociente \|B − exacto\|/σ_B ≤ 0.77, en el par 200/400). B no subestima. A es honesto pero muy pesimista: suma \|σ_R\| + \|σ_2R\| de errores casi enteramente correlacionados, y su valor central se sesga en R grande (−4.7×10⁻⁶ en 1600/3200) por la misma no linealidad |
| R2-04 | Baja | El Monte Carlo del cruce sortea ruido independiente en cada nodo de δ, aunque los errores de la receta son suaves y casi enteramente correlacionados en δ y entre cajas | σ_MC < σ_lineal en todos los pares de A | Sin efecto: la barra usada es la mayor de las dos (la lineal). Se documenta aquí |
| R2-05 | Baja | Criterios laxos: K6 (\|y* − 1/4\| < 0.01 cuando lo esperado en el par mayor es 4×10⁻⁴: 25 veces de holgura); K7 de la transferencia y del radial (0.2 veces una barra que ya está inflada; la transferencia da "0.00 veces el límite"); K9 con las barras de A y del radial h = 1/160 (unas 1000 veces el error real del radial). Pasar estos controles es poca evidencia | Tabla de controles | No se cambian (se fijaron antes). Se señalan; los controles fuertes son K4, K10 y el acuerdo a 10⁻¹¹ con mi cálculo |
| R2-06 | Baja | "En cambio y ya está por debajo de 1/4": en δ = 1.19, R = 50, y = 0.2544 > 1/4 | Tabla 3 | Corregido: "por debajo de su valor en el umbral, (1/4)(1 + r_e/R) (0.2589 en R = 50)" |
| R2-07 | Baja | K11b (añadido después de ver K11, sin criterio) aparecía como "sí" en la columna "¿Pasa?". Además no es monótono (R·máx\|y − F\| = 0.50 en 800 y 1.26 en 1600) | `controles.md` | `07_controles.py` ahora escribe "informativo (sin criterio)"; tabla regenerada (sigue 27 de 31) |
| R2-08 | Baja | En el radial h = 1/160 el cruce 1600/3200 se aleja del exacto (−1.96×10⁻⁷ frente a ≤ 3×10⁻⁸ en los demás pares; cociente K6 0.887) | `05_cruces_salida.txt` | Dentro de su barra (1.2×10⁻⁵); probablemente redondeo con N = 512 000. Solo se documenta |
| R2-09 | Baja (fuentes) | Serra "spatial FSS" sin revista | La lista de publicaciones del autor da *Phys. Lett. A* **303**, 20 (2002); el editor y Crossref no abrieron desde aquí | Actualizado en `fuentes.md`, `seccion_articulo.md` y `LEEME.md` como [V-web] |

## Fuentes (comprobadas por R2)

- Borasoy et al., *Eur. Phys. J. A* **34**, 185–196 (2007) [V] (página de Springer): "we impose a hard spherical wall at some
  fixed large radius". Correcto lo que dice `fuentes.md`.
- Serra, Neirotti y Kais, *Phys. Rev. A* **57**, R1481–R1484 (1998), DOI 10.1103/PhysRevA.57.R1481 [V] (Scilit).
- König, Lee y Hammer, *Phys. Rev. Lett.* **107**, 112001 (2011) [V] (manuscrito aceptado de APS); caja periódica.
- Busch, Englert, Rzażewski y Wilkens, *Found. Phys.* **28**(4), 549–559 (1998) [V] (Springer). El resumen visible no da la
  energía en la unitariedad, como ya advierte `fuentes.md` (se tomó de Stetcu et al.).
- Drut y Nicholson: arXiv:1208.6556, DOI 10.1088/0954-3899/40/4/043101, "topical review for J. Phys. G" [V-arXiv]; el
  volumen 40 sigue deducido del DOI.
- Serra, PDF serra28: R es un radio de corte del potencial con condición de Siegert, pozo cuadrado ℓ = 1, sin Yukawa ni
  punto fijo 1/4. Revista: *Phys. Lett. A* **303**, 20 (2002) según la lista del autor [V-web].
- Lüscher (1986, 1991): no los reverifiqué (E2 los marcó [V] por Scilit y ADS).
- Búsqueda adicional (dos búsquedas extendidas: "critical screening Yukawa spherical box hard wall finite-size scaling
  crossing", "hard spherical wall two-body unitarity 1/4 coupling"): solo aparecieron Roy (confinamiento con el radio en el
  que la energía cambia de signo; un buscador da *Int. J. Quantum Chem.* 2016, DOI 10.1002/qua.25108, que no abrió) y
  Serra-Kais 2012 (FSS con el tamaño de la base de B-splines, sin caja dura). No encontré el cruce de R²E₀ en una esfera
  dura usado para un umbral de acoplamiento o de apantallamiento.

**Qué queda original, con honestidad.** No lo son la condición de cuantización (pared esférica), el valor universal en la
unitariedad (Lüscher y las redes; Busch et al. en trampa armónica), el cruce de dos tamaños (Nightingale) ni el FSS del
Yukawa (base: Serra-Neirotti-Kais; radio de corte: Serra 2002). Sí parecen nuevos, dentro de buscadores abiertos: su
combinación en una esfera dura para δ_c del Yukawa; la ley δ* − δ_c = π²r_e/(16cR²) + 3π²r_e²/(32cR³), con coeficientes que
predicen los cruces a 10⁻⁹; el punto fijo 1/2 − 2/π² de ⟨r⟩/R y su α_ρ; el corrimiento de la pared sin imagen en el cruce;
y (de esta revisión) la lectura del error de Trotter como corrimiento del umbral, que explica por qué el cruce es más
robusto que E₀. La ley de primer orden es un cálculo de una línea a partir de la condición de la pared esférica, así que
el aporte es de aplicación y de comprobación, no un resultado teórico profundo.

## Veredicto

La extensión es correcta en lo esencial: teoría, constantes, cruces y predicción de la pared se reproducen con otro método a
10⁻¹¹. Los diez intervalos contienen la referencia. El método B es legítimo y sus barras de y son honestas. Hay que corregir
el término de pared que faltaba en B de ⟨r⟩/R (R2-01, ya corregido en el código: E2-09) y tener presentes los criterios laxos (R2-05).
