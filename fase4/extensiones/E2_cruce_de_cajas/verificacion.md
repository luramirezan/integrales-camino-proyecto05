# Verificación de E2

Comprobaciones independientes de los resultados propios (script `codigo/10_verificacion.py`, `resultados/10_verificacion.json`,
salvo que se diga otro) y lo que se encontró al releer el código.

## 1. Segundo método y caso exacto

- **Cruces sin interpolar (V1).** Se recalculó cada cruce del disparo con brentq en δ, evaluando el disparo en cada δ
  pedido (sin rejilla ni spline). La diferencia con el cruce interpolado con spline es de 1.1×10⁻¹¹ o menos en y y de
  4.5×10⁻¹¹ o menos en ⟨r⟩/R, en los seis pares. La interpolación no aporta error visible; el control K7 que no pasa en el
  disparo compara con PCHIP y con el cúbico local, que son menos precisos que el spline en el par 50/100 de ⟨r⟩/R.
- **Teoría frente a cálculo (V1).** El modelo de rango efectivo (sin parámetros libres: a(δ) y r_e(δ) a energía cero) se
  separa del cruce exacto en −5.0×10⁻⁷, −2.9×10⁻⁸, −1.7×10⁻⁹, −1.1×10⁻¹⁰ en y (pares 50 a 400) y en −6.1×10⁻⁶,
  −3.5×10⁻⁷, −2.1×10⁻⁸, −1.3×10⁻⁹ en ⟨r⟩/R. La diferencia baja más rápido que 1/R³, como se espera del término O(R⁻⁴).
- **Caso exacto (01).** Pozo cuadrado de alcance b dentro de la esfera, a fijo: y − F(R/a) baja a la mitad cada vez que b
  se divide por 2 (razones 2.031, 2.015, 2.008, 2.004 en z = 0) y en z = 0 coincide con r_e/(4R) con r_e = b.
- **δ_c por energía cero (V2).** brentq sobre 1/a(δ) da 1.1906124210606, a 1.6×10⁻¹⁵ de la referencia del proyecto.
- **Reproducción de la Fase 3 (K14).** Las seis celdas de δ = 1.19 (R = 50 a 1600) de la transferencia son idénticas, bit
  a bit, a las de `fase3/resultados/20_cajas.json`.
- **Integral de camino frente a disparo, celda a celda (K4).** 161 de 161 celdas dentro de 2 barras; el cociente máximo
  |dif|/barra es 0.818.

## 2. Convergencia y sensibilidad

- **Disparo (V3).** Cambiar r₀ de 10⁻⁷ a 10⁻⁶ mueve y en 6.9×10⁻¹⁴, 1.9×10⁻¹³ y −3.6×10⁻¹⁴ en las tres celdas probadas;
  cambiar la tolerancia de 10⁻¹² a 10⁻¹³ (barra del disparo, script 02) da barras del cruce de 6×10⁻¹⁵ o menos.
- **Radial en la malla (V4).** En δ = 1.1906, R = 800, sin Richardson, la diferencia con el disparo es +2.23×10⁻⁷,
  +5.71×10⁻⁸, +1.43×10⁻⁸, +3.61×10⁻⁹ y +8.56×10⁻¹⁰ para h = 1/40 a 1/640: orden 1.968, 1.992, 1.989 y 2.078.
- **Monotonía de Dirichlet (V5).** E₀(R) decrece con R en todas las celdas de las cuatro fuentes; ninguna violación.
- **Barra Monte Carlo (V6).** En el par 1600/3200 de la transferencia, la desviación del Monte Carlo es 1.70×10⁻⁵ en el
  script 05 y 1.73×10⁻⁵ y 1.67×10⁻⁵ con otras dos semillas (4000 réplicas). La barra final de ese par la fija la
  propagación lineal, que es mayor.
- **Pesos del ajuste en R (V7, decisión E2-04).** Sin pesos, δ_c de la transferencia (y) sería 1.1906091755 en vez de
  1.1906106662, una diferencia de 1.5×10⁻⁶, muy por debajo de la barra (6.7×10⁻⁵). En el radial la diferencia es de 2×10⁻⁹.
- **Orden de Trotter (scripts 12 y 12b).** Las 23 celdas de R = 50 fuera de [1.8, 2.2] vuelven al rango al restar el
  corrimiento de la pared medido con el radial. Las 17 de R = 3200 no cambian al restar la pared; con ε = 0.025 añadido
  (tabla de pares de la cache de la Fase 2), el orden de la terna (0.1, 0.05, 0.025) en δ = 1.1906 es 2.084 frente a 2.384
  con (0.2, 0.1, 0.05): son términos de orden superior en ε = 0.2. En esa celda, el valor extrapolado con (0.05, 0.025)
  difiere del de la receta en 4.7×10⁻³ relativo (dentro de la barra de la receta; ver `12b_trotter_eps0025.json`).
- **Corrimiento de la pared en el cruce (05 frente a 01).** El cruce de la integral de camino (método B) menos el exacto es
  −7.6×10⁻⁵, −1.8×10⁻⁵, −4.2×10⁻⁶, −9.4×10⁻⁷, −2.0×10⁻⁷ y −1.6×10⁻⁷ (pares 50 a 1600), y la teoría de la pared en
  R + c_w predice −8.3×10⁻⁵, −2.0×10⁻⁵, −4.8×10⁻⁶, −1.18×10⁻⁶, −2.9×10⁻⁷ y −7.3×10⁻⁸. Es una comprobación cuantitativa,
  hecha antes de restar nada, de que la diferencia entre la integral de camino y el disparo es la pared sin imagen.
- **Pared en el método B de ⟨r⟩/R (añadido tras la revisión R2, hallazgo R2-01).** El término de pared de ⟨r⟩/R
  (`04b_pared_rho.py`, misma receta que el de E₀) corre el cruce en +2.27×10⁻⁴, +5.39×10⁻⁵, +1.32×10⁻⁵ y +3.25×10⁻⁶
  (pares 50 a 400), los mismos que obtuvo la revisión con su solucionador espectral en R + c_w. Con él en la barra, el
  cociente |B − disparo|/σ_B de ⟨r⟩/R es 0.59, 0.54, 0.39, 0.17, 0.04 y 0.01 (antes 1.67 y 1.31 en los dos primeros pares),
  y el intervalo final [1.19059638, 1.19062781] coincide con el de la revisión a 1.0×10⁻⁹ (la revisión usó el
  corrimiento exacto en R + c_w; aquí sale de la receta con el radial h = 1/40).
- **Pared en el método A de ⟨r⟩/R (a pedido del coordinador, después de R2-01).** La barra de cada celda de ⟨r⟩/R suma
  |pared_rho| (el valor central de la celda no cambia), igual que la barra de E₀ de la receta. Los cruces por par son
  idénticos; las barras por par pasan a 1.05×10⁻³, 2.45×10⁻⁴, 7.80×10⁻⁵, 4.34×10⁻⁵, 4.36×10⁻⁵ y 5.29×10⁻⁵, y el
  cociente |A − disparo|/σ_A de ⟨r⟩/R es 0.20 o menos en los seis pares (antes hasta 0.63, ya cubierto). El intervalo
  final es [1.19054141, 1.19068003] (barra 6.93×10⁻⁵, antes 6.04×10⁻⁵) y con R ≤ 800 [1.19048891, 1.19073401]; el
  centro con todas las R pasa de 1.1906108583 a 1.1906107238 por los pesos 1/σ del ajuste (V7); con R ≤ 800 el ajuste
  de tres pares es exacto y el centro no cambia. Ningún control cambia de estado (27 de 31).

## 3. Lo que se encontró al releer el código

Se releyeron los scripts 01 a 12 completos después de la corrida final. Hallazgos:

1. **`06_artefacto.py` (corregido):** el comentario decía que en el Yukawa repulsivo y(R) < y(2R); el cálculo da lo
   contrario (a > 0 pequeño, y > 1 baja hacia 1). Solo era texto; el control usa el número de cambios de signo y no
   cambia. Corregido también en `teoria.md` (sección 6).
2. **`07_controles.py` (corregido antes de la versión final):** el control K6 de la transferencia aplicaba el criterio del
   cociente, que `criterios_previos.md` fija solo para disparo y radial. Se ajustó el código al criterio escrito antes, no
   al revés. Las barras "|" de los criterios rompían la tabla markdown; ahora se escapan.
3. **`05_cruces.py`:** la variante "transferencia con la pared restada" usa como barra la de la receta menos el término de
   pared; es una variante de sensibilidad y no entra en ningún intervalo final. La extrapolación con R ≤ 800 se calcula
   antes de borrar las réplicas Monte Carlo (en un primer borrador se calculaba después y perdía el Monte Carlo).
4. **`04_transferencia.py`:** dos cadenas de cálculo en segundo plano fallaron al importar `e2comun` (montaje de red). El
   script ahora guarda tras cada celda y solo calcula las que faltan; 05 y 07 exigen las 23 celdas en cada caja.
5. **`e2comun.disparo_E0`:** para ligados profundos con κR grande, el disparo hacia afuera pierde la cola (aparecen nodos
   espurios cerca de R). Solo pasa en los δ añadidos para el colapso (δ = 1.16 con R ≥ 800); esas celdas tienen
   `nodos` > 0, la figura D las excluye y no se usan en ningún cruce. En la rejilla principal todas tienen 0 nodos.
6. **`e2comun.G_escala`:** el caso z = 1 devolvía al principio 1/3 por un error de borrador; se corrigió a 1/4 antes de
   cualquier corrida (u = 1 − r/R da ⟨r⟩/R = 1/4) y `01_teoria.json` lo comprueba (`G1`).

## 4. Cifras del texto

Dos scripts:

- `codigo/11_cifras_texto.py` busca cada cifra de 3 o más cifras significativas de `seccion_articulo.md`, `teoria.md`,
  `LEEME.md` y este archivo en los valores numéricos de los JSON. Mide además su propia tasa de coincidencias casuales con
  números al azar: 0.505 con 3 cifras, 0.1425 con 4, 0.0325 con 5 y 0.0025 con 7. Es decir, solo es una prueba fuerte para
  cifras de 5 o más dígitos; por eso existe el segundo script.
- `codigo/11b_cifras_clave.py` comprueba de forma explícita 50 cifras clave (intervalos, cruces, constantes de la teoría,
  diferencias con el disparo, barras, cocientes): lee el valor del JSON, lo formatea como en el texto y verifica que la
  cadena aparece. Resultado: 50 de 50 (7 añadidas tras la revisión R2 para los métodos A y B de ⟨r⟩/R).

Lo que `11_cifras_texto.py` no encuentra en los JSON (`resultados/11_cifras_texto_salida.txt`) se revisó a mano: años y
números de las referencias; R = 12800 y el intervalo [1.19, 1.20], que son de la Fase 3; β = 0.5826 = −ζ(1/2)/√(2π), una
constante de la Fase 2 (`transferencia.BETA_PARED`); 1/640 y 4000 réplicas, que son parámetros de los scripts; y los
cocientes de K6 (1.040 a 1.001) y el 75.2 % de K2, que están en `07_controles.json` como texto de la columna "valor".
Las cifras de 2 dígitos significativos (diferencias como −7.6×10⁻⁵) no las revisa el primer script; las de la sección del
artículo están en la lista explícita del segundo.
