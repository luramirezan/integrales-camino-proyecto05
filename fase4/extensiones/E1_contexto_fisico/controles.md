# Controles de la extensión E1 (generado por `codigo/07_documentos.py` desde los JSON)

Los criterios se escribieron en la cabecera de cada script **antes** de correrlo (17-11-2026) y no se cambiaron
después. Pasan 9 de 12.

| # | control | criterio fijado antes | valor | ¿pasa? | script |
|---|---|---|---|---|---|
| C1 | delta_c(1s) con dos metodos frente a la referencia | \|A-ref\| < 1e-9 y \|B-ref\| < 1e-9 | A-ref = 4.0e-15; B-ref = -1.3e-10 | pasa | `01_umbral_y_controles.py` |
| C2 | Coulomb exacto (delta = 0), metodos A y B | A: \|E0+1/2\|<1e-9, \|<r>-3/2\|<1e-7, \|<r2>-3\|<1e-6; B: \|E0+1/2\|<1e-6 | A: 1.7e-16, -5.8e-15, -1.6e-14; B: 6.1e-09 | pasa | `01_umbral_y_controles.py` |
| C3 | Hulthen exacto (delta = 1), metodo A | \|E0-E_ex\| < 1e-10, \|<r>-<r>_ex\| < 1e-8 | -1.6e-15; -6.7e-15 | pasa | `01_umbral_y_controles.py` |
| C4 | delta_c(2s) y delta_c(3s), A frente a B | \|A-B\| < 1e-8 | 2s: 8.4e-11; 3s: 6.5e-11 | pasa | `01_umbral_y_controles.py` |
| C5 | Formula de Debye en SI frente al coeficiente del NRL Plasma Formulary | \|coef/743 - 1\| < 1e-3 | 743.394 cm (rel 5.3e-04) | pasa | `02_plasma.py` |
| C6 | Longitud critica frente a Rogers, Graboske y Harwood 1970 (D0 = 0.83991 a0) | \|1/delta_c - 0.83991\| < 5e-6 (ultima cifra publicada) | 0.8399039 | **no pasa** | `02_plasma.py` |
| C7 | Energia del 1s en 8 valores de delta: disparo (A) frente a caja (B) | max \|E_A - E_B\|/\|E_A\| < 1e-6 | 1.4e-04 | **no pasa** | `02_plasma.py` |
| C8 | Primera resonancia s de Tulin, Yu y Zurek (b = 1.68) frente a 2/delta_c | \|2/delta_c - 1.68\| <= 0.005 | 2/delta_c = 1.67981 | pasa | `03_materia_oscura.py` |
| C9 | Antirresonancia s (a_s = 0) frente a Tulin, Yu y Zurek (b = 4.52); A frente a B | \|b - 4.52\| <= 0.005 y \|delta_A - delta_B\| < 1e-6 | b = 4.4657; dif A-B = 1.6e-09 | **no pasa** | `03_materia_oscura.py` |
| C10 | Energia de enlace: m_p + m_n - m_d frente al dato E_B(d) de CODATA 2022 | \|dif\| < 1e-6 MeV | -0.03 eV | pasa | `04_deuteron.py` |
| C11 | Reproduccion del prototipo con sus mismas entradas | \|delta - 0.8304596701595315\| < 1e-9 | 1.9e-13 | pasa | `04_deuteron.py` |
| C12 | Deuteron central: disparo (A) frente a caja (B); caja R frente a 2R | delta: <1e-7 rel; <r>, <r2>: <1e-5 rel; E(R) vs E(2R): <1e-9 rel | 2.5e-08; 1.5e-08, 8.1e-08; 1.5e-11 | pasa | `04_deuteron.py` |

## Controles que no pasan y su causa medida

- **C6** (Rogers, Graboske y Harwood 1970). Nuestro $1/\delta_c$ = 0.8399039 redondea a 0.83990, y el resumen
  del artículo de 1970 da 0.83991. La diferencia, 6.1e-06, es mayor que media unidad de la
  última cifra publicada, que fue el criterio fijado. Nuestro valor coincide con las Fases 1 a 3 y con dos métodos
  independientes a 10^-10 (C1), así que atribuimos la diferencia a la precisión de 1970 (integración numérica de la
  época); la revisión adversarial lo confirmó con un tercer método (fase de Prüfer, `revision/`). La tabla 1 de
  Janev et al. (2016) da 0.839907, que también redondea a 0.83991 y queda 3 ppm por encima del nuestro. No cambia
  ninguna conclusión física: es una diferencia de 7 partes por millón en la longitud crítica.
- **C7** (energía del 1s, disparo frente a caja). El criterio relativo de 10^-6 se fijó antes de correr y falla
  cerca del umbral: la diferencia **absoluta** entre los dos métodos es casi constante, entre
  4.3e-09 y 6.7e-09 hartree, y al dividir
  por una energía que tiende a cero crece hasta 1.4e-04 en $\delta = 1.18$.
  La verificación V1 muestra la causa: con $h = 1/80$ en el método de caja la diferencia absoluta baja en un factor
  15.6 a 16.2 (el 16 esperado para el
  error de orden 4 que deja Richardson), así que el error es de discretización del método B con $h=1/40$, no del
  disparo. Con $h = 1/80$ la diferencia relativa máxima es 8.9e-06, todavía
  por encima de 10^-6 en $\delta = 1.18$; no damos el control por aprobado.
- **C9** (antirresonancia de Tulin, Yu y Zurek). Encontramos $a_s = 0$ en $\delta = 0.44785728$,
  es decir, $b = \alpha m_\chi/m_\phi = 4.4657$, con dos métodos que coinciden a
  2e-09. El artículo menciona una
  antirresonancia en $b = 4.52$ (1.2% más arriba). La causa es de
  definición, no un error nuestro ni de la fuente: 4.52 es la etiqueta de una de las curvas ilustrativas de su
  figura 3 (sección eficaz frente a velocidad con $\alpha_X = 0.01$), elegida para mostrar la supresión, y el
  artículo no dice que sea el cero de $a_s$ a velocidad nula. La revisión midió dos cosas que lo explican: la
  fórmula de Hulthén del mismo artículo (Sec. VI, $b = \kappa r^2$ con $r = 1.6909$) pone la
  antirresonancia en $b = 4.575$ con $\kappa = 1.6$, y el cero de la fase s del Yukawa
  se mueve con la velocidad: con $kL = v/\alpha = 0.05$ y 0.06 sale en $b = 4.502$ y
  4.518 (`revision/r03_antirresonancia_y_extras.py`). El control, tal como lo fijamos, no
  pasa; el criterio estaba mal planteado porque comparaba un cero exacto con un valor ilustrativo.
