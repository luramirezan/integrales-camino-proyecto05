# Verificación de la extensión E1 (generado por `codigo/07_documentos.py`)

## 1. Dos métodos independientes para cada cifra

- **Método A (sin caja):** disparo con `solve_ivp` (DOP853, tolerancia relativa 10^-12) hacia afuera desde
  $r_0 = 10^{-8}$ y hacia adentro desde $R_\text{lejos} = r_m + 40/\kappa$ con la solución que decae; se empalma
  el wronskiano normalizado en $r_m$ y se integran $u^2$, $r u^2$, $r^2u^2$ junto con la ecuación
  (`codigo/comun_e1.py`). Para el umbral: pendiente de la solución de energía cero (`fase2/codigo/radial.py:umbral`).
- **Método B (caja):** diferencias finitas en caja de Dirichlet con Richardson ($h = 1/40$ y $h/2$),
  `fase3/codigo/comun3.py:radial_ref`, importado sin copiarlo. Para el umbral: un Numerov propio a energía cero,
  escrito para esta extensión, que no usa `solve_ivp`.

| cantidad | A | B | diferencia |
|---|---|---|---|
| $\delta_c(1s)$ | 1.1906124210606 | 1.1906124209256 | 1.3e-10 |
| $\delta_c(2s)$ | 0.31020928271 | 0.31020928263 | 8.4e-11 |
| $\delta_c(3s)$ | 0.13945029406 | 0.13945029400 | 6.5e-11 |
| $\delta_d$ (deuterón, $m_\pi$ promedio) | 0.8304583940 | 0.8304583730 | 2.1e-08 |
| $\langle r\rangle$ deuterón (unidades $L$) | 2.69558211 | 2.69558207 | rel. 1.5e-08 |
| $\langle r^2\rangle$ deuterón (unidades $L^2$) | 11.0223113 | 11.0223104 | rel. 8.1e-08 |
| $\delta_L$ (punto de NPLQCD) | 0.92122154 | 0.92122151 | 3.0e-08 |
| $a_s = 0$ (antirresonancia) | 0.4478572850 | 0.4478572834 | 1.6e-09 |
| $d\ln B/d\ln m_\pi$ ($g$ fijo) | -4.758790 | -4.758791 | 7.7e-07 |

Referencia de las Fases 1 a 3: $\delta_c$ = 1.1906124210606. El Numerov propio da, con $h$ = 1/200, 1/400 y 1/800,
1.1906124211209, 1.1906124210329, 1.1906124209256: la dispersión
(2.0e-10) no baja con $h$, así que está dominada por redondeo y no por truncamiento (la revisión lo
confirmó repitiendo el Numerov en aritmética extendida, donde el error con $h$ = 1/400 baja a $6\times10^{-13}$; el
error no depende de $R$, así que no es acumulación a lo largo de la malla); no aplicamos Richardson y damos la de
$h$ = 1/800, aunque la de $h$ = 1/400 está más cerca de la referencia. El método A con caja de integración
$R = 200$ y $R = 100$ cambia 0.0e+00.

## 2. Casos exactos

- Coulomb ($\delta = 0$): A da $E_0 + 1/2$ = 1.7e-16, $\langle r\rangle - 3/2$ =
  -5.8e-15, $\langle r^2\rangle - 3$ = -1.6e-14;
  B ($R = 60$) da $E_0 + 1/2$ = 6.1e-09.
- Hulthén ($\delta = 1$, solución exacta de `radial.hulthen_exacto`): A da $E_0 - E_\text{ex}$ =
  -1.6e-15 y $\langle r\rangle$ con error
  -6.7e-15.
- Longitud de dispersión: $a_s(1.19)$ = 2203.8 y $a_s(1.20)$ = -142.93, como en la Fase 3
  (+2204 y −142.9).

## 3. Convergencia y diagnóstico del método de caja (V1)

| $\delta$ | $R$ | $|E_A - E_B|$, $h=1/40$ | $|E_A - E_B|$, $h=1/80$ | cociente |
|---|---|---|---|---|
| 0.20 | 60 | 6.21e-09 | 3.91e-10 | 15.9 |
| 0.40 | 60 | 6.47e-09 | 3.99e-10 | 16.2 |
| 0.60 | 70 | 6.66e-09 | 4.12e-10 | 16.2 |
| 0.80 | 110 | 6.53e-09 | 4.07e-10 | 16.0 |
| 1.00 | 210 | 5.77e-09 | 3.59e-10 | 16.1 |
| 1.10 | 450 | 5.07e-09 | 3.18e-10 | 16.0 |
| 1.15 | 1000 | 4.61e-09 | 2.87e-10 | 16.1 |
| 1.18 | 3820 | 4.30e-09 | 2.76e-10 | 15.6 |

El cociente cercano a 16 confirma que la diferencia es el error de orden 4 del método B tras Richardson. En el
deuterón, la energía de la caja con $R$ y $2R$ cambia 1.5e-11 en relativo (caja suficiente).

## 4. Conversión de unidades y entradas

- Deuterón: $\varepsilon\,\mu\,(g/\hbar c)^2$ = -2.2245663700 MeV, que es $-B_d$ (diferencia
  -1.8e-15 MeV).
- $B_d$ desde las masas de CODATA 2022 ($m_p + m_n - m_d$) = 2.22456637 MeV, frente al dato de entrada de
  CODATA $E_B(d)$ = 2.22456640 MeV.
- Plasma: la fórmula SI $\lambda_D = (\varepsilon_0 k_BT/n_ee^2)^{1/2}$ da el coeficiente
  743.394 cm, frente a 743 cm del NRL Plasma Formulary (tres cifras); con el coeficiente
  redondeado la densidad crítica cambia -1.1e-03 en relativo.
- Elección de $m_\pi$: entre $\pi^0$ y $\pi^\pm$, $\delta_d$ varía 1.0%,
  $g$ y $m_\pi$ crítico 2.4%, y el radio del modelo
  0.6%.
- El prototipo (`propuesta_originalidad/prototipos/deuteron_juguete.py`) se reproduce con sus mismas entradas a
  2e-13 (C11). Con las masas verificadas cambia poco:
  $\delta_d$ = 0.830458 frente a 0.830460 y $m_\pi^c$ = 197.90 MeV frente a
  197.91 MeV del prototipo.

## 5. Relectura del código (17-11-2026)

Releímos los siete scripts y `comun_e1.py` contra los JSON. Encontramos y corregimos durante el trabajo:

1. La primera versión del barrido en energía del método A empezaba en $E = -0.5 + 10^{-12}$; con $\delta = 0$ el
   fundamental está justo en $-1/2$ y el barrido devolvía el 2s ($-0.125$). Se cambió el inicio a $-0.52$
   (cota inferior válida porque el Yukawa nunca baja del Coulomb). El control C2 lo detecta si vuelve a pasar.
2. `brentq` no acepta `rtol` menor que $4\epsilon$; se dejó en 10^-15.
3. El Hulthén se desborda en `expm1` para $\delta r > 700$; se acotó el argumento (el potencial ya es cero allí).
4. En la relectura final encontramos que el primer paso del Numerov usaba el coeficiente cúbico $(2+\delta)/3$ de la
   serie de $u$ cerca del origen; el correcto es $(1+\delta)/3$ (de $u'' = -2e^{-\delta r}u/r$ con
   $u = r - r^2 + br^3$). Es un cambio de orden $h^3$ en $u(h)$; se corrigió y se volvieron a correr todos los
   scripts. Las cifras de esta página son las de después de la corrección.

Cosas que revisamos y están bien: (i) la masa reducida del deuterón es $m_pm_n/(m_p+m_n)$, no $m_N/2$ (la
diferencia es de 3e-07); (ii) el radio del modelo es la mitad del radio
cuadrático medio de la coordenada relativa, es decir, el radio de nucleones puntuales respecto del centro de masa
(corregido en la revisión, R1-02: no es exactamente el $r_\text{str}$ de Filin et al., que incluye además operadores
de carga de dos cuerpos y correcciones relativistas; es su contribución principal); (iii) el diagrama del plasma usa solo la longitud de Debye electrónica, como el NRL
Plasma Formulary, y dibuja aparte la variante con protones ($\lambda_D/\sqrt2$, densidad a la mitad);
(iv) $\delta = 2m_\phi/(\alpha m_\chi)$ usa la masa reducida $m_\chi/2$, igual que Tulin, Yu y Zurek.

La auditoría externa con Gemini (decisión D4) no se hizo dentro de este agente; queda para el paso de revisión.
