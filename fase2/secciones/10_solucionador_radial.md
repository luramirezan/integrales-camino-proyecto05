# 10. Solucionador radial de referencia (módulo `radial.py`)

**Fase 2, tarea 1 de `fase1/que_sigue_fase2.md`.** 27-10-2026. Rol: verificación y referencia.
Código: `fase2/codigo/radial.py` (módulo), `fase2/codigo/test_radial.py` (pruebas con `assert`), `fase2/codigo/10_radial_controles.py` (cifras de referencia).
Resultados: `fase2/resultados/10_radial.json` (todas las cifras), `fase2/resultados/10_radial_u_delta02.npz` (u(r) de δ = 0.2), `fase2/figuras/10_radial_convergencia.png`. Salida de las pruebas: `fase2/verificacion/test_radial_salida.txt`.
Todas las cifras de esta sección salen de esos dos scripts (unos 4 s y 6 s en un núcleo).

## 10.1 Qué hace

Es el método A de la sección 5 de la Fase 1, convertido en un módulo que sirve para **cualquier** potencial V(r) (se le pasa como función). Resuelve, para ℓ = 0 y en unidades ħ = m = 1,

$$-\tfrac12 u''(r) + V(r)\,u(r) = E\,u(r),\qquad u(0)=0,\quad u(R)=0 .$$

- **Malla y matriz.** $r_j = j\,h$, $j=1,\dots,N$, $h=R/(N+1)$. La segunda derivada con tres puntos da una matriz tridiagonal simétrica: diagonal $1/h^2+V(r_j)$, fuera de la diagonal $-1/(2h^2)$. Sus menores autovalores son $E_0, E_1$ (`scipy.linalg.eigh_tridiagonal`).
- **Richardson.** Se resuelve con $h$ y con $h/2$ (N y 2N+1 puntos, mismo R) y se extrapola: $X = (2^p X_{h/2} - X_h)/(2^p-1)$, con $p=2$ por defecto. Se aplica a $E_0$, $E_1$, $\langle r\rangle$, $\langle r^2\rangle$, $F_{1/2}$ y $\langle r\rangle/R$. Por defecto $h = 1/40$ y $1/80$, como en el plan (9.4).
- **Autovector.** $u$ normalizado con $\int_0^R u^2\,dr = 1$ (trapecio; como $u(0)=u(R)=0$ es $h\sum u_j^2$).
- **Observables.** $\langle r\rangle$, $\langle r^2\rangle$, $\langle r^2\rangle^{1/2}$, $\langle r\rangle/R$ y $F_{1/2}=\int_0^{R/2}u^2/\int_0^R u^2$. Cambio respecto a la Fase 1: el punto $r=R/2$ entra con medio peso (trapecio) y no con peso entero, para que $F_{1/2}$ también tenga error $O(h^2)$ y Richardson tenga sentido. Las cifras de la tabla 9.6 no cambian a la precisión impresa (prueba 7).
- **Condición de energía cero.** `pendiente_energia_cero(V, R)` integra $u''=2V(r)u$ a $E=0$ desde $r_0=10^{-8}$ ($u=r_0$, $u'=1$) con DOP853 (rtol $10^{-13}$) y devuelve $u'(R)$. Fuera del alcance del potencial $u=A+Br$; un nuevo estado ligado aparece cuando $B=u'(\infty)=0$. `umbral(familia, a, b, R)` busca con `brentq` el parámetro donde $u'(R)=0$. Si V tiene saltos se le dan los puntos (`quiebres`) y se integra por tramos.
- **Soluciones exactas incluidas** para las pruebas: `hulthen_exacto(δ, n)` y `pozo_exacto(V0, a)` (sympy para los momentos).
- **Caja.** `caja_recomendada(E0)` = $\max(60, 25/\kappa)$, $\kappa=\sqrt{-2E_0}$ (receta 5.1); con `entera=True` redondea R hacia arriba a un entero para que $r=1$ sea nodo de todas las mallas (se usa en el pozo).

Uso mínimo:
```python
import radial as rd
o = rd.resolver_rich(rd.V_yukawa(0.2), R=40.0)        # h=1/40 y 1/80, Richardson
o["E0"], o["E1"], o["r_med"], o["r_rms"], o["F12"], o["r_sobre_R"], o["dE"]
dc = rd.umbral(rd.V_yukawa, 1.1, 1.3, R=200.0)          # 1.1906124210606
```

## 10.2 Controles exactos usados

- **Coulomb** ($\delta=0$): $E_n=-1/(2n^2)$, $\langle r\rangle_{1s}=3/2$, $\langle r^2\rangle_{1s}=3$.
- **Hulthén**, $V=-\delta/(e^{\delta r}-1)$ (se comporta como $-1/r+\delta/2$ cerca de 0): $E_n=-\tfrac12(1/n-n\delta/2)^2$, umbral del estado $n$ en $\delta=2/n^2$ (2 para el 1s, 0.5 para el 2s). Estado base $u_1=(1-e^{-\delta r})e^{-\kappa r}$ con $\kappa=1-\delta/2$; sympy confirma que el residuo de la ecuación es 0 y da
  $$\langle r\rangle = \frac{12-\delta^2}{2\,(4-\delta^2)}$$
  (en $\delta=0$ da 3/2, el de Coulomb). $\langle r^2\rangle$ también se calcula en forma cerrada (en el JSON).
- **Pozo esférico cuadrado**, $V=-V_0$ para $r<a$, $a=1$: $E$ exacta por $k\cot(ka)=-\kappa$ con $k=\sqrt{2(V_0+E)}$, $\kappa=\sqrt{-2E}$ (`brentq`); umbral $V_0a^2=\pi^2/8=1.2337005501$. $\langle r\rangle$, $\langle r^2\rangle$ con $u=\sin kr$ dentro y $\sin(ka)\,e^{-\kappa(r-a)}$ fuera (sympy).

## 10.3 Tabla de pruebas (`test_radial.py`: 7 de 7 pasan; la prueba 3 tiene un control más desde V3)

Las cifras numéricas son las de Richardson con h = 1/40 y 1/80, salvo que se diga otra cosa.

| # | Prueba | Numérico | Referencia | Diferencia | Tolerancia | Resultado |
|---|---|---|---|---|---|---|
| 1 | Coulomb, R=60: $E_0$ | −0.4999999939 | −0.5 | 6.1e−9 | 1e−8 | pasa |
| | $E_1$ | −0.1249999999 | −0.125 | 9.5e−11 | 1e−8 | pasa |
| | $\langle r\rangle$; $\langle r^2\rangle$ | 1.4999999939; 3.0000000000 | 1.5; 3 | 6.1e−9; 7e−13 | 1e−7 | pasa |
| | orden aparente de $E_0$ (h = 1/20 … 1/160) | 1.9986, 1.9997, 1.9999 | 2 | | ±0.01 | pasa |
| 2 | Tabla 5.1 de la Fase 1 (7 filas, δ = 0 a 1.1, misma receta de R y N) | las 7 filas iguales en las 9 cifras de $E_0$, las 5 de $\langle r\rangle$ y las 2 de $\lvert E_h-E_{h/2}\rvert$ | tabla 5.1 | ≤ media unidad de la última cifra | idem | pasa |
| 3 | δ = 0.2, R=60: $E_0$ | −0.3268085052 | −0.32680851 | 4.8e−9 | 5e−9 | pasa (solo frente a la referencia redondeada; ver 10.7) |
| | $E_0$ frente al exacto −0.3268085113692 (V3) | −0.3268085052 (h=1/40) | exacto | 6.2e−9 | 5e−9 | **no pasa** con h=1/40, 1/80 |
| | ídem con h=1/80, 1/160 (V3) | −0.3268085110 | exacto | 3.9e−10 | 1e−9 | pasa |
| | $E_1$ (R=60) | −0.0121078621 | −0.012108 | 1.4e−7 | 5e−7 | pasa |
| | $\langle r\rangle$; $\langle r^2\rangle^{1/2}$ | 1.5497218981; 1.7960900429 | 1.5497; 1.7961 | 2.2e−5; 1.0e−5 (redondeo) | 5e−5 | pasa |
| 4 | $\delta_c$ por energía cero, R = 200 y 400 | 1.1906124210606 | 1.1906124211 | 3.9e−11 | 1e−8 | pasa |
| | $\delta_c(2s)$, R=400 | 0.3102092827 | 0.310209 | 2.8e−7 (redondeo) | 5e−7 | pasa |
| 5 | Hulthén δ=0.2, R=60: $E_0$; $\langle r\rangle$; $\langle r^2\rangle$ | −0.4049999939; 1.5101010042; 3.0456586062 | −0.405; 1.5101010101; 3.0456586063 | 6.1e−9; 5.9e−9; 2e−11 | 1e−8; 2e−7 rel. | pasa |
| | Hulthén δ=1.0, R=60 | −0.1249999936; 1.8333333280; 4.7222221795 | −0.125; 1.8333333333; 4.7222222222 | 6.4e−9; 5.3e−9; 4.3e−8 | idem | pasa |
| | Hulthén δ=1.5, R=100 | −0.0312499936; 2.7857141688; 12.0918347332 | −0.03125; 2.7857142857; 12.0918367347 | 6.4e−9; 1.2e−7; 2.0e−6 | idem (2.4e−6 en $\langle r^2\rangle$) | pasa (justo en $\langle r^2\rangle$) |
| | Hulthén 2s, δ=0.2, R=84: $E_1$ | −0.0449999999 | −0.045 | 9.9e−11 | 1e−8 | pasa |
| | umbrales 1s y 2s por energía cero | 2.0000000000000; 0.5000000000000 | 2; 0.5 | 3e−14; 5e−15 | 1e−8 | pasa |
| 6 | Pozo: umbral por energía cero (R=50) | 1.2337005501362 | π²/8 | 2e−14 | 1e−8 | pasa |
| | $V_0=2$, R=60, borde medio: $E_0$; $\langle r\rangle$ | −0.2035507435; 1.2836437153 | −0.2035507418; 1.2836437276 | 1.7e−9; 1.2e−8 | 1e−8; 1e−5 | pasa |
| | $V_0=1.3$, R=385, borde medio: $E_0$; $\langle r\rangle$ | −0.0021146965; 8.1882959 | −0.0021146991; 8.1883069 | 2.6e−9; 1.1e−5 | 2e−8; 1e−4 | pasa |
| | orden aparente (ver 10.4) | | | | | pasa |
| 7 | Tabla 9.6 de la Fase 1 (15 celdas, δ = 1.15, 1.18, 1.20; R = 50 a 800) | todas iguales en las 3 cifras de $E_0$ y de $\langle r\rangle/R$, $F_{1/2}$ (h = 1/80) | tabla 9.6 | | media unidad de la última cifra | pasa con **una errata** (abajo) |

**Sobre las tolerancias.** El residuo después de Richardson es de orden $h^4$: en Hulthén, al pasar de h = 1/40 a 1/80 el error de $\langle r\rangle$ y $\langle r^2\rangle$ baja 16.0 veces (la prueba exige más de 8). Con h = 1/40 ese residuo es unos $6\times10^{-9}$ en $E_0$ en todos los casos, y llega a $1.7\times10^{-7}$ relativo en $\langle r^2\rangle$ de Hulthén δ = 1.5, donde la función es más extendida. La tolerancia de 2e−7 relativo de la prueba 5 se fijó **después** de ver ese número (con 1e−6 absoluto la prueba fallaba en $\langle r^2\rangle$ por $2.0\times10^{-6}$). Lo que la justifica es que el error baja como $h^4$, no un ajuste a ojo. Si alguien necesita más cifras en $\langle r^2\rangle$, debe usar h = 1/80 y 1/160 (error 16 veces menor).

**Errata en la Fase 1 (tabla 9.6).** En δ = 1.18, R = 400 la tabla 9.6 dice $E_0=-3.08\times10^{-5}$. El código de la propia Fase 1 (`09_prueba_costos.py`, función `radial`) y este módulo dan $-3.0746\times10^{-5}$, que redondea a $-3.07\times10^{-5}$. El código está bien; el error está en el redondeo del documento. No se tocó `fase1/`; la prueba usa el valor corregido y lo avisa en pantalla. El texto de 9.6 ("cambia $6.7\times10^{-6}$ entre 200 y 400") sí es correcto: $3.0746-2.4060=0.669$.

## 10.4 Orden de convergencia medido

Error de $E_0$ **sin** Richardson frente al exacto, con h = 1/20, 1/40, 1/80, 1/160 (y 1/320 en el pozo). Orden aparente $p=\log_2(\text{err}_h/\text{err}_{h/2})$. Figura: `fase2/figuras/10_radial_convergencia.png`.

| Caso | Orden aparente | Comentario |
|---|---|---|
| Coulomb δ = 0 (R = 60) | 1.9986, 1.9997, 1.9999 | la singularidad $-1/r$ en el origen **no** degrada el orden 2 de $E_0$ |
| Yukawa δ = 0.2 (sin exacto, tres mallas) | 1.9982, 1.9996 | orden 2 |
| Pozo $V_0=2$, $V(a)=0$ (convención $r<a$) | 0.974, 0.987, 0.994, 0.997 | **orden 1**: el salto en $r=a$ degrada el orden |
| Pozo $V_0=1.3$, $V(a)=0$ | 0.468, 0.798, 0.910, 0.957 | orden 1, todavía lejos del régimen asintótico con h = 1/20 |
| Pozo $V_0=2$ y $1.3$, $V(a)=-V_0/2$ ($a$ nodo de la malla) | 2.000 (todos); 2.005, 2.001, 2.000, 2.000 | poner el valor medio del salto en el nodo devuelve el **orden 2** |

**Qué significa para el pozo.** Con la convención estricta $V(a)=0$ la red ve un pozo efectivo más angosto (el salto queda, en promedio, media celda antes), y el error es $O(h)$. Con $h=1/40$ es $1.7\times10^{-2}$ en $V_0=2$. Richardson con $p=2$ entonces **empeora** el resultado ($5.8\times10^{-3}$ en $V_0=2$; $6.6\times10^{-4}$ en $V_0=1.3$). Con $p=1$ queda $1.5\times10^{-4}$ y $2.3\times10^{-4}$, todavía malo. Cerca del umbral ($V_0=1.3$) la convención estricta con h = 1/40 da $E_0=-5.9\times10^{-4}$ frente a $-2.1\times10^{-3}$ exacto, y aun con Richardson $p=1$ el $\langle r\rangle$ sale 6.02 frente a 8.19 exacto, porque la red está más cerca de su propio umbral que el pozo real. Con el valor medio en el nodo y Richardson $p=2$ el error es $1.7\times10^{-9}$ ($V_0=2$) y $2.6\times10^{-9}$ ($V_0=1.3$) en $E_0$. **Regla:** para un V con saltos, el salto debe caer en un nodo y llevar el valor medio, o bien medir el orden y usar el $p$ medido. El Yukawa no tiene saltos, así que esto no afecta al problema principal; sí afectaría a cualquier control con el pozo en la matriz de transferencia.

## 10.5 Cifras de referencia para los demás módulos (`10_radial.json`)

Richardson con h = 1/40 y 1/80. Lista completa con todas las cifras en el JSON.

| Caso | R | $E_0$ | $E_1$ | $\langle r\rangle$ | $\langle r^2\rangle^{1/2}$ |
|---|---|---|---|---|---|
| Coulomb | 40 | −0.499999993900 | — | 1.4999999939 | — |
| Coulomb | 60 | −0.499999993899 | −0.124999999905 | 1.4999999939 | 1.7320508 |
| Yukawa δ = 0.2 | 40 | −0.326808505154 | −0.0121063582 | 1.5497218981 | 1.7960900429 |
| Yukawa δ = 0.2 | 60 | −0.326808505156 | −0.0121078621 | 1.5497218981 | 1.7960900429 |
| Yukawa δ = 0.2 | 161 (caja del 2s) | −0.326808505155 | −0.012107865091 | | |
| Hulthén δ = 0.2 (exacto) | ∞ | −0.405 | −0.045 | 1.510101010101 | 1.745181540 |
| Hulthén δ = 1.0 (exacto) | ∞ | −0.125 | — | 1.833333333333 | 2.173067468 |
| Hulthén δ = 1.5 (exacto) | ∞ | −0.03125 | — | 2.785714285714 | 3.477331841 |
| Hulthén δ = 0.2 / 1.0 / 1.5 (numérico) | 40 | −0.404999993880 / −0.124999993567 / −0.031249993233 | | | |
| Pozo $V_0=2$ (exacto) | ∞ | −0.2035507418207 | — | 1.2836437276 | 1.5191300 |
| Pozo $V_0=1.3$ (exacto) | ∞ | −0.0021146991476 | — | 8.1883069057 | 11.2341281 |

Brecha 1s–2s en δ = 0.2: 0.3147006 (R = 60 y R = 161). En R = 40 el 2s todavía siente la caja ($E_1$ cambia en el sexto decimal, 0.3147021), pero el $E_0$ de R = 40 y R = 60 coincide en $2\times10^{-12}$, así que R = 40 basta para el estado base, que es el que compara la transferencia.

**Cajas cerca del umbral** (tabla 9.6, ahora con más cifras y con δ = 1.25). $E_0$ con Richardson; $\langle r\rangle/R$ y $F_{1/2}$ también con Richardson (los de h = 1/80 están en el JSON):

| δ | | R = 50 | 100 | 200 | 400 | 800 |
|---|---|---|---|---|---|---|
| 1.15 | $E_0$ | −3.308191e−4 | −4.511743e−4 | −4.558735e−4 | −4.558844e−4 | −4.558844e−4 |
| | $\langle r\rangle/R$; $F_{1/2}$ | 0.23931; 0.89549 | 0.16394; 0.96220 | 0.08717; 0.99756 | 0.04362; 0.99999 | 0.02181; 1.00000 |
| 1.18 | $E_0$ | +3.380133e−4 | +3.213296e−5 | −2.405950e−5 | −3.074584e−5 | −3.098118e−5 |
| | $\langle r\rangle/R$; $F_{1/2}$ | 0.29245; 0.83168 | 0.26744; 0.85887 | 0.22490; 0.90440 | 0.15266; 0.96727 | 0.08046; 0.99818 |
| 1.20 | $E_0$ | +6.437030e−4 | +1.868654e−4 | +5.798061e−5 | +1.843915e−5 | +5.668561e−6 |
| | $\langle r\rangle/R$; $F_{1/2}$ | 0.32379; 0.78994 | 0.33128; 0.77665 | 0.35194; 0.74636 | 0.38592; 0.69591 | 0.42557; 0.63338 |
| 1.25 | $E_0$ | +1.114049e−3 | +3.444757e−4 | +1.008586e−4 | +2.774569e−5 | +7.305354e−6 |
| | $\langle r\rangle/R$; $F_{1/2}$ | 0.38128; 0.70618 | 0.41600; 0.64988 | 0.45004; 0.59250 | 0.47332; 0.55097 | 0.48639; 0.52655 |

El cociente $|E_h-E_{h/2}|/|E_0|$ queda entre 0.000 y 0.057 en todas las celdas, por debajo del 0.1 del criterio (a') de 9.6. Ley $\kappa=0.7421(\delta_c-\delta)$: $-4.5416\times10^{-4}$ (δ = 1.15) y $-3.1012\times10^{-5}$ (δ = 1.18), frente a los valores saturados −4.5588e−4 y −3.0981e−5.

**Umbral.** $\delta_c=1.1906124210606$ con R = 200, 400 y 800 (igual en las 13 cifras), a $3.9\times10^{-11}$ del 1.1906124211 de la Fase 1; $\delta_c(2s)=0.3102092827$.

## 10.6 Limitaciones

- El residuo de Richardson es $\sim6\times10^{-9}$ en $E_0$ con h = 1/40 y 1/80. Para comparar con la transferencia a $10^{-6}$ (criterio 9.7) sobra; para pedirle más cifras al radial hay que bajar a h = 1/80 y 1/160.
- $E_1$ con R = 40 o 60 todavía depende de la caja en el sexto o séptimo decimal; para el 2s hay que usar la caja propia ($R=161$ en δ = 0.2).
- El pozo cuadrado solo da orden 2 con el salto en un nodo y valor medio (10.4).
- Las pruebas comparan contra la propia Fase 1 (tablas 5.1 y 9.6) y contra soluciones exactas (Coulomb, Hulthén, pozo). Las exactas son la parte independiente; las de la Fase 1 solo comprueban que el módulo reproduce lo que ya había.


## 10.7 Correcciones tras la verificación (V3, 27-10-2026)

Respuesta a los hallazgos de `fase2/verificacion/V1_recalculo_independiente.md` y `V2_auditoria_adversarial.md`; el detalle está en `fase2/verificacion/V3_respuesta_hallazgos.md`.

- **H4 de V1 (reproducido).** El criterio $|E_0+0.32680851|<5\times10^{-9}$ pasaba solo frente a la referencia redondeada a 8 cifras. Con Richardson en mallas más finas ($R=40$; `10_radial.json`, clave `yukawa_0.2/V3_referencia_fina`) el valor converge a $-0.3268085113851$ ($h=1/320$), a $1.6\times10^{-11}$ del exacto de V1 ($-0.3268085113692$, disparo y FEDVR). Frente a él, el error con $h=1/40,1/80$ es $6.2\times10^{-9}$: **ese criterio no pasa** frente al valor exacto. Con $h=1/80,1/160$ el error baja a $4.0\times10^{-10}$ y pasa. No se cambió la tolerancia; se añadió la prueba con $h=1/80$ a `test_radial.py`. Para cifras de $10^{-9}$ hay que usar $h=1/80$ y $1/160$ (ya se decía en el problema 5).
- **H9 de V2 (corregido).** `10_radial_controles.py` tenía la ruta del proyecto fija; ahora es relativa a `__file__`. Se volvió a ejecutar: las claves `cajas_9_6` y `yukawa_0.2/R40` son idénticas a las de antes (comparadas con la copia en `resultados/archivo_pre_V3/`).
