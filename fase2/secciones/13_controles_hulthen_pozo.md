# 13. Controles exactos: Hulthén y pozo esférico cuadrado por la misma integral de camino

**Proyecto 05, umbral de ligadura en el potencial de Yukawa** · Fase 2 · Bloque 13 · 27 de octubre de 2026
Equipo: Juan Sebastián Calixto y Luis Felipe Ramírez (con Claude como asistente). Tarea 5 de `fase1/que_sigue_fase2.md`, ampliada a pedido del profesor después de la presentación de la Fase 1: controles con solución exacta, pasados por la **misma** formulación de tiempo imaginario que se usa para el Yukawa.

Código: `fase2/codigo/13_controles_hulthen_pozo.py`. Usa los módulos `transferencia.py`, `pares.py` y `radial.py`.
Resultados: `fase2/resultados/13_controles.json`. Salida completa de la ejecución: `fase2/verificacion/13_controles_salida.txt`. Figura: `fase2/figuras/13_controles.png`.
Todas las cifras salen de la ejecución del 27-10-2026. El script es determinista: no usa números aleatorios, así que las semillas 20262000+k no hacen falta. Tardó 110 s con la máquina compartida (carga entre 3 y 6), usando 3 procesos para el pozo.
Los criterios de aceptación se fijaron en el script (`CRIT_DECL`) **antes** de ejecutarlo. Resultado: **21 criterios pasan, 0 fallan y 5 se miden sin criterio** (los órdenes de Trotter del pozo y el de Hulthén en δ=0.2).

## 13.1 Por qué estos dos controles

Las fuentes se citan con el estado que tienen en `fase2/fuentes_control/fuentes_control.md`. En este bloque no se cambió ningún estado: no se volvió a consultar ninguna fuente.

- **Hulthén**, $V_H=-\delta/(e^{\delta r}-1)$. Es el control "gemelo" del Yukawa: igual que él, se comporta como $-1/r$ en el origen y cae como $e^{-\delta r}$ lejos. Hulthén y Laurikainen ya lo usaban para aproximar la ecuación del Yukawa [H4, VERIFICADA (APS, metadatos)].
  - Sus estados $s$ son exactos: $E_n=-\tfrac12(1/n-n\delta/2)^2$, con umbral $\delta_c(1s)=2$ [H8, VERIFICADA (PDF de arXiv); H9, VERIFICADA (PDF de arXiv), revista NO confirmada]. El origen histórico del potencial es [H5, CITA SECUNDARIA], y el libro de problemas que trae la solución $s$ es [H6, CITA SECUNDARIA; el número de problema, NO VERIFICADO].
  - Además es exacto **dentro de la propia integral de camino** [H1, Cai, Cai e Inomata 1986, VERIFICADA (APS, resumen)].
  - Los métodos aproximados fallan cerca del umbral [H2, VERIFICADA (APS, resumen); H7, VERIFICADA (APS, resumen)]. Por eso se incluye δ=1.5, que ya está a 3/4 del camino hacia el umbral exacto 2.
- **Pozo esférico cuadrado**, $V=-V_0$ para $r<1$. No tiene singularidad, pero sí un **salto** en $r=1$.
  - La condición de empalme es $k\cot k=-\kappa$ [P2, VERIFICADA (página web)] y el umbral es $V_0=\pi^2/8$. Este umbral lo comprueba numéricamente P1 [VERIFICADA (PDF de arXiv), revista NO confirmada]; la fuente de texto clásica es [P4, NO VERIFICADA].
  - En el umbral $s$ el estado no es normalizable [P3, VERIFICADA (PDF de arXiv), revista NO confirmada].
  - `fuentes_control.md` (2.2) deja dicho que el orden de convergencia en el paso de tiempo con el salto es **"algo a medir, no a afirmar"**. Aquí se mide (13.3).
- **Técnicas.** Las paredes de la caja con imágenes [PI3, VERIFICADA (PDF de arXiv)] no tratan escalones finitos. Los suavizados de Coulomb [PI1, PI2, VERIFICADAS] no se usan aquí: la singularidad la absorbe la acción de pares exacta.

## 13.2 Hulthén con la acción de pares de Coulomb

**Formulación (sin cambiar nada del método aprobado).** Se separa $V_H=V_C+W_H$, con $V_C=-1/r$ y
$$W_H(r)=\frac1r-\frac{\delta}{e^{\delta r}-1}=\frac{\delta}{2}-\frac{\delta^2 r}{12}+\frac{\delta^4r^3}{720}+\dots$$
El eslabón es el mismo de la sección 11: $T=K_D\,e^{-U_C}\,e^{-\epsilon[W_H(r)+W_H(r')]/2}$, con la tabla $U_C$ con Richardson en $h_{\rm tab}$. Solo cambia la función $W$ que recibe `transferencia.resolver`. Para $\delta r<10^{-3}$, $W_H$ se evalúa con la serie para evitar la cancelación.

**El resto está acotado (control A0).**
- sympy da $\lim_{r\to0}W_H=\delta/2$ y $\lim_{r\to\infty}W_H=0$.
- En una malla de $r\in[10^{-8},400]$, $W_H$ es decreciente (incremento máximo 0) y queda dentro de $[0,\delta/2]$ para δ = 0.2, 1.0, 1.5 y 2.0. Por ejemplo, el máximo es $0.749999998$ en δ=1.5.
- Entonces $W_H\in[0,\delta/2]$: el peso sigue siendo real, positivo y normalizable. El menor elemento no nulo de $T$ es $\sim10^{-13}$ y ninguno es negativo.

**Exactos.** $E=-\tfrac12(1-\delta/2)^2$ y $\langle r\rangle=(12-\delta^2)/[2(4-\delta^2)]$. Los da `radial.hulthen_exacto` con sympy, con residuo simbólico 0. La caja es $R=\max(60,25/\kappa)$, con $\kappa=1-\delta/2$.

**Parámetros.**
- $\epsilon\in\{0.2,0.1,0.05\}$ para la extrapolación del plan (ley $\epsilon^2$), y además $\epsilon=0.025$ para comprobar el orden. La tabla $U_C$ de $\epsilon=0.025$ es nueva y quedó en la caché.
- Mallas Nyström $h=0.04,\ 0.02,\ 0.01$.

**El error de Nyström vuelve a ser $h^4$ (lo mismo que en la sección 11.4).** El orden aparente en $h$ de $E$ es 3.99 a 4.00 en las 12 combinaciones de δ y ε. Por eso $E$ se combina con Richardson en $h$ de exponente 4: $(16E_{0.02}-E_{0.04})/15$. Hacerlo con $h=0.01$ y $0.02$ cambia el resultado en $\le10^{-10}$. El orden en $h$ de $\langle r\rangle$ también es 4.0.

| δ | $R$ | $E$ exacta | radial − exacta | $E(\epsilon)-E_{\rm ex}$, ε = 0.2 / 0.1 / 0.05 / 0.025 (Richardson en $h$) | orden de Trotter (ε 0.2/0.1/0.05) | extrapolado − exacta |
|---|---|---|---|---|---|---|
| 0.2 | 60 | −0.405 | $+3.8\times10^{-10}$ | $-1.71\times10^{-8}$ / $-2.4\times10^{-9}$ / $+3.2\times10^{-9}$ / $+8.6\times10^{-9}$ | 1.38 (no significativo) | $+5.1\times10^{-9}$ |
| 1.0 | 60 | −0.125 | $+4.1\times10^{-10}$ | $-8.31\times10^{-6}$ / $-2.09\times10^{-6}$ / $-5.20\times10^{-7}$ / $-1.24\times10^{-7}$ | **1.990** (con ε .1/.05/.025: 1.985) | $+2.5\times10^{-9}$ |
| 1.5 | 100 | −0.03125 | $+4.0\times10^{-10}$ | $-2.42\times10^{-5}$ / $-6.08\times10^{-6}$ / $-1.52\times10^{-6}$ / $-3.77\times10^{-7}$ | **1.991** (1.994) | $-1.8\times10^{-9}$ (antes de V3: $-3.3\times10^{-9}$) |

| δ | $\langle r\rangle$ exacto | radial: error relativo | transferencia ($h\to0$), $\langle r\rangle-\langle r\rangle_{\rm ex}$ con ε = 0.2 / 0.1 / 0.05 | orden en ε | extrapolado − exacto |
|---|---|---|---|---|---|
| 0.2 | 1.5101010101 | $-2.5\times10^{-10}$ | $+1.10\times10^{-5}$ / $+2.8\times10^{-6}$ / $+7.0\times10^{-7}$ | 2.00 | $+1.7\times10^{-8}$ |
| 1.0 | 1.8333333333 | $-1.8\times10^{-10}$ | $+2.08\times10^{-4}$ / $+5.2\times10^{-5}$ / $+1.3\times10^{-5}$ | 1.99 | $+5.5\times10^{-8}$ |
| 1.5 | 2.7857142857 | $-2.6\times10^{-9}$ | $-3.25\times10^{-4}$ / $-8.1\times10^{-5}$ / $-2.0\times10^{-5}$ | 2.00 | $+4.3\times10^{-7}$ |

**Lectura.**
- En δ=1.0 y 1.5 la ley $\epsilon^2$ sale limpia (orden 1.99), y la extrapolación cae a unos $3\times10^{-9}$ de la energía exacta. Pasan A2 y A3.
- El sesgo de Trotter crece hacia el umbral: en ε=0.2 es $8.3\times10^{-6}$ con δ=1.0 y $2.4\times10^{-5}$ con δ=1.5. En términos relativos son $7\times10^{-5}$ y $8\times10^{-4}$ de $|E|$. Cerca del umbral del Yukawa (Fase 3 y 4), la extrapolación $\epsilon\to0$ es imprescindible.
- En δ=0.2 el sesgo de Trotter ($\lesssim2\times10^{-8}$) es del tamaño del residuo de tabulación y de Nyström. Ese residuo crece como $1/\epsilon$, porque es un error por eslabón: de $-2.4\times10^{-9}$ en ε=0.1 pasa a $+8.6\times10^{-9}$ en ε=0.025. Por eso el orden aparente no significa nada en δ=0.2. Aun así la extrapolación queda a $5\times10^{-9}$. Lo mismo pasaba con el Yukawa en δ=0.2 (sección 11).
- $\langle r\rangle$ también tiene sesgo de Trotter de orden $\epsilon^2$: hasta $3\times10^{-4}$ en δ=1.5 con ε=0.2. Extrapolado, queda a $\le4.3\times10^{-7}$ del exacto. Pasa A4. Un $\langle r\rangle$ sin extrapolar en ε no vale como observable de localización fina cerca del umbral.
- **Conclusión del control.** La acción de pares de Coulomb, con un resto acotado $W\in[0,\delta/2]$, reproduce las energías exactas de Hulthén a unos $10^{-9}$ cuando se extrapola $h\to0$ y $\epsilon\to0$. Es la misma clase de resto que $W_Y\in[0,\delta]$ del Yukawa. Esto prueba que el método aprobado no tiene sesgo propio en un potencial con la misma singularidad y la misma cola, aun cerca de su umbral.

## 13.3 Pozo esférico cuadrado: transferencia sin $U_C$ y orden de Trotter medido

**Formulación.** Se usa la opción sin $U_C$ de `transferencia.py`: $T_{ij}=h\,K_D(r_i,r_j;\epsilon)\,e^{-\epsilon[V(r_i)+V(r_j)]/2}$. Es la factorización simétrica del potencial completo, con el núcleo libre con imagen.
- El salto en $r=1$ cae en un nodo de todas las mallas.
- Convención principal: $V(1)=-V_0/2$ (valor medio, "media"). Control: $V(1)=0$ ("estricta").
- Cajas: $R=60$ para $V_0=2$ ($\kappa=0.638$) y $R=385$ para $V_0=1.3$ ($\kappa=0.0650$, receta $25/\kappa=384.4$ redondeada hacia arriba).
- Exactos por brentq (`radial.pozo_exacto`): $E=-0.20355074182$ ($V_0=2$) y $-0.00211469915$ ($V_0=1.3$). El umbral es $\pi^2/8=1.2337$, así que $V_0=1.3$ está apenas un 5 % por encima.
- El autovalor se calcula por desplazamiento-inversión ($\sigma$ por encima del espectro). En los 60 casos se comprobó que $\sigma>\lambda_0$ y que el autovector no cambia de signo. Frente al Lanczos de `tr.resolver` la diferencia es $-2\times10^{-14}$ y $+1.5\times10^{-12}$ (B4).

**Radial (B1).** Con la convención media, el error frente a brentq es $-1.0\times10^{-10}$ ($V_0=2$) y $+1.7\times10^{-10}$ ($V_0=1.3$). Con la estricta es $+2.9\times10^{-3}$ y $+3.3\times10^{-4}$: el orden 1 que ya señaló la sección 10.

**Lo que se midió.**

1. **Error de malla Nyström del orden de $h^1$, no $h^2$ ni $h^4$.**
   - Convención media: órdenes aparentes en $h$ de 1.02 a 1.53 ($V_0=2$; crecen al bajar ε) y de 0.89 a 0.92 ($V_0=1.3$) con $h=0.04,0.02,0.01$; **con $h=0.02,0.01,0.005$ (V3) bajan a 1.01–1.37 y 0.95–0.96**, es decir, se acercan a 1.
   - Convención estricta: 0.98 a 0.99 ($V_0=2$) y 0.29 a 0.59 ($V_0=1.3$, sin asintótica clara); con las mallas de V3, 0.99–1.00 y 0.75–0.84.
   - El salto del potencial dentro de la regla del trapecio rompe el orden alto de Nyström. Por eso, para cada ε, primero se extrapola $h\to0$ con el orden medido. **Desde V3 (hallazgo H2 de V1) se usan las mallas $h=0.02,\,0.01,\,0.005$**; con $0.04,0.02,0.01$ el valor "$h\to0$" no estaba convergido: en $V_0=2$ el nuevo $E_{h0}$ difiere del anterior en $-0.86$, $-1.60$, $-1.70$, $-1.34$ y $-0.84\times10^{-5}$ (ε de 0.2 a 0.0125), en la dirección y en el 60–85 % del tamaño que V1 midió con el operador continuo ($-1.15$ a $-2.42\times10^{-5}$). Todavía no está convergido del todo.
2. **Orden de Trotter aparente con la discontinuidad.** Es $\approx1.5$ ($E-E_{\rm ex}\propto\epsilon^{3/2}$), no 2. Se dan los órdenes locales con ε = (0.2, 0.1, 0.05), (0.1, 0.05, 0.025) y (0.05, 0.025, 0.0125), tras $h\to0$:

| caso | órdenes locales de Trotter ($h\to0$) | con $h=0.01$ fijo |
|---|---|---|
| $V_0=2$, media | 1.497, 1.499, 1.502 (antes de V3: 1.497, 1.502, 1.511) | 1.513, 1.520, 1.530 |
| $V_0=2$, estricta | 1.497, 1.498, 1.500 (antes: 1.498, 1.500, 1.502) | 1.498, 1.499, 1.500 |
| $V_0=1.3$, media | 1.672, 1.567, 1.523 (antes: 1.671, 1.564, 1.517) | 1.684, 1.587, 1.555 |
| $V_0=1.3$, estricta | 1.684, 1.575, 1.529 (antes: 4.24, −1.64, 0.86, sin sentido) | 1.712, 1.586, 1.532 |

   En $V_0=1.3$ el orden se acerca a 1.5 desde arriba al bajar ε (régimen preasintótico). Es razonable: el estado casi todo está fuera del pozo y siente poco el salto. Una explicación plausible del 3/2, **no demostrada aquí**: en un paso ε el camino libre recorre una distancia $\sim\sqrt\epsilon$, así que el error de la factorización se concentra en una capa de anchura $\sqrt\epsilon$ alrededor del salto. Eso da un error por unidad de tiempo $\sim\epsilon\cdot\sqrt\epsilon$. Es un resultado **medido**, como pedía la fuente; no hemos encontrado una referencia que lo dé.

3. **Extrapolación y comparación con brentq (B3, convención media).**

| $V_0$ | $E(\epsilon)-E_{\rm ex}$ ($h\to0$), ε = 0.2 / 0.1 / 0.05 / 0.025 / 0.0125 | extrapolado con el orden medido | con ley $\epsilon^{3/2}$ | con ley $\epsilon^2$ (incorrecta) | plan (ε 0.2/0.1/0.05, ley $\epsilon^2$) |
|---|---|---|---|---|---|
| 2.0 | $-2.067\times10^{-2}$ / $-7.31\times10^{-3}$ / $-2.58\times10^{-3}$ / $-9.10\times10^{-4}$ / $-3.19\times10^{-4}$ | $+3.5\times10^{-6}$ (antes $+6.2\times10^{-6}$) | $+4.3\times10^{-6}$ (antes $+1.0\times10^{-5}$) | $-1.22\times10^{-4}$ | $-1.0\times10^{-3}$ |
| 1.3 | $-1.77\times10^{-3}$ / $-5.71\times10^{-4}$ / $-1.95\times10^{-4}$ / $-6.82\times10^{-5}$ / $-2.40\times10^{-5}$ | $-4.2\times10^{-7}$ (antes $-2.6\times10^{-7}$) | $+1.7\times10^{-7}$ | $-9.3\times10^{-6}$ | $-7.0\times10^{-5}$ |

   Pasan los dos (criterio $10^{-5}$). **V3:** con las mallas antiguas el $+6.2\times10^{-6}$ de $V_0=2$ era sobre todo error de la extrapolación en $h$ (H2 de V1); con $h=0.005$ baja a $+3.5\times10^{-6}$, y el ajuste $E_0+a\epsilon^{3/2}$ a los cinco puntos pasa de $+1.5\times10^{-5}$ a $+9.7\times10^{-7}$ (V1, con el operador continuo: $-5.8\times10^{-6}$). El control de robustez B3b (ajuste a 5 puntos, $<10^{-5}$), añadido en V3 antes de ejecutar, pasa en $V_0=2$ y **no pasa en $V_0=1.3$** ($+2.2\times10^{-5}$): allí el orden aún no es 1.5 (1.67 → 1.52) y la ley fija $\epsilon^{3/2}$ no vale para los ε grandes. El error de B3 lo domina la extrapolación en $h$, que sigue con orden ~1 no estabilizado. La exactitud alcanzable con el salto es de unos $10^{-5}$, tres a cuatro órdenes peor que con Hulthén. **Si se hubiera usado la receta del plan** (ε 0.2/0.1/0.05 con ley $\epsilon^2$), el error sería de $10^{-3}$ ($V_0=2$) y $7\times10^{-5}$ ($V_0=1.3$, es decir, 3 % de $|E|$).
   Con la convención estricta, $V_0=2$ queda a $-1.1\times10^{-4}$ y $V_0=1.3$ falla del todo ($-2.0\times10^{-3}$, del tamaño de $E$) con las mallas antiguas. **Con las de V3 los errores bajan a $-2.5\times10^{-5}$ y $-1.2\times10^{-4}$**: era error de Nyström, no una propiedad de la integral de camino, como dijo V1 (en el continuo el valor del potencial en un solo nodo no cuenta). Los $E_{h0}$ de las dos convenciones aún difieren en $2$–$3\times10^{-5}$ ($V_0=2$) y $\sim10^{-4}$ ($V_0=1.3$), así que la igualdad de los dos límites no está comprobada todavía con estas mallas.

4. **$\langle r\rangle$ del pozo (informativo, sin criterio).** El sesgo de Trotter de $\langle r\rangle$ cerca del umbral es enorme. En $V_0=1.3$ vale $-2.0$ en ε=0.2 (25 % de $\langle r\rangle=8.188$) y $-0.043$ en ε=0.0125. Extrapolado ($h\to0$, órdenes en ε 1.10, 1.34, 1.43), queda a $+2.6\times10^{-3}$. En $V_0=2$ queda a $+7.0\times10^{-6}$ de 1.28364.

**Conclusión del control.** El pozo no sirve para validar la ley $\epsilon^2$ del método aprobado, porque el salto la rompe: sale $\epsilon^{3/2}$, y además el error de Nyström es $O(h)$. Sí sirve para dos cosas:
- (i) Confirma que el problema está en la **regularidad del potencial** y no en la caja ni en la detección del umbral. El Yukawa y el Hulthén tienen un resto $W$ suave y acotado, y dan orden 2 y Nyström $h^4$.
- (ii) Con los órdenes medidos y $\epsilon$ hasta 0.0125, la transferencia reproduce el exacto de brentq a $\le10^{-5}$, también a un 5 % del umbral.

## 13.4 Tabla de criterios

| Control | Criterio (fijado antes de ejecutar) | Valor | ¿Pasa? |
|---|---|---|---|
| A0 resto $W_H$ (δ = 0.2, 1.0, 1.5, 2.0) | en $[0,\delta/2]$ y decreciente | máx. entre $\delta/2-3\times10^{-11}$ y $\delta/2-3\times10^{-9}$; incremento máx. 0 | sí (4/4) |
| A1 radial Hulthén | $\lvert E_0-E\rvert<10^{-8}$; $\langle r\rangle$ relativo $<2\times10^{-7}$ | $\le4.1\times10^{-10}$; $\le2.6\times10^{-9}$ | sí (3/3) |
| A2 transferencia Hulthén, extrapolada | $<10^{-6}$ | $+5.1\times10^{-9}$, $+2.5\times10^{-9}$, $-1.8\times10^{-9}$ | sí (3/3) |
| A3 orden de Trotter Hulthén | [1.8, 2.2] en δ = 1.0 y 1.5 | 1.990, 1.991 (δ=0.2: 1.38, informativo) | sí (2/2) |
| A4 $\langle r\rangle$ Hulthén extrapolado | $<10^{-4}$ | $1.7\times10^{-8}$, $4.9\times10^{-8}$, $-3.4\times10^{-8}$ | sí (3/3) |
| B1 radial pozo (media) | $<10^{-8}$ / $2\times10^{-8}$ | $-1.0\times10^{-10}$, $+1.7\times10^{-10}$ | sí (2/2) |
| B2 orden de Trotter del pozo | medir y declarar | ≈1.50 ($V_0=2$); 1.67 → 1.52 ($V_0=1.3$) | medido |
| B3 pozo extrapolado (orden medido; V3: mallas 0.02/0.01/0.005) | $<10^{-5}$ | $+3.5\times10^{-6}$, $-4.2\times10^{-7}$ | sí (2/2) |
| B3b (V3) ajuste $E_0+a\epsilon^{3/2}$ a 5 puntos | $<10^{-5}$ | $+9.7\times10^{-7}$, $+2.2\times10^{-5}$ | **no** (1/2) |
| B4 desplazamiento-inversión frente a Lanczos | $<10^{-10}$ | $2\times10^{-14}$, $1.5\times10^{-12}$ | sí (2/2) |

## 13.5 Limitaciones y lo que queda

- **PIGS de Hulthén (opcional): no se hizo.** Cuando se hizo este bloque `pigs.py` no existía; ya existe y queda para la Fase 3. El caso natural es δ=1.0 con $u_T=re^{-r}$, que no es exacta para Hulthén. Su energía local es $W_H-\tfrac12$, acotada.
- Las tablas $U_C$ dentro de $r\le10$ dependen de la misma discretización por diferencias finitas que el radial (la circularidad de 9.10). Los exactos de Hulthén y de brentq son independientes de las dos, y eso es justamente lo que aporta este bloque.
- En el pozo, el resultado depende de dos extrapolaciones seguidas con órdenes medidos con solo tres puntos cada una. La de $h$ tiene órdenes entre 0.9 y 1.5 que no son constantes. La cota de $10^{-5}$ en $V_0=2$ es justa, como se dijo en 13.3.
- El orden 3/2 del pozo está medido, no demostrado, y no tiene fuente.
- No se tocó nada de `fase1/` ni de `enunciado/`. No se cambió ningún estado de `fuentes_control.md`.

## Registro de IA de este bloque

| Campo | Valor |
|---|---|
| Fecha | 27-10-2026 |
| IA | Claude (Anthropic), agente de verificación del flujo de la Fase 2 |
| Qué hizo | Escribió y ejecutó `13_controles_hulthen_pozo.py`, la figura y esta sección |
| Errores propios corregidos | (1) La primera ejecución falló por un nombre de clave con puntos (`orden_trotter_eps_0.1_...`), que es un error de sintaxis en Python; se renombró. (2) La exploración del pozo con Lanczos (`tr.resolver`) en $R=385$ tardaba más de 95 s por malla, porque la brecha relativa es muy pequeña. Se cambió a desplazamiento-inversión y se comprobó contra Lanczos (B4). (3) El $\langle r\rangle$ del pozo se reportaba al principio solo en un punto ($h=0.01$, ε=0.0125). Se añadió su extrapolación con los órdenes medidos y se volvió a ejecutar el script entero |
| Decisión humana | Pendiente de revisión por Juan Sebastián (verificación) |


## 13.6 Correcciones tras la verificación (V3, 27-10-2026)

Detalle en `fase2/verificacion/V3_respuesta_hallazgos.md`. (1) Pozo: se añadió $h=0.005$ (con factorización de Cholesky en banda como inverso del desplazamiento, porque la LU de SuperLU no cabía en memoria con $V_0=1.3$, $N=76999$), $E_{h0}$ se extrapola con $0.02/0.01/0.005$ y el valor anterior queda en el JSON como `E_h0_anterior`. (2) Hulthén: los números cambian en $\le2\times10^{-9}$ por la corrección de Wigner-Kirkwood de $U_C$ fuera de $r=10$ (sección 11.9). (3) Erratas: en la tabla de Hulthén δ = 1.5, ε = 0.05 decía $-1.53\times10^{-6}$ cuando el JSON daba $-1.5249\times10^{-6}$ (H11 de V2); ahora el valor es $-1.521\times10^{-6}$. (4) El hallazgo H10 de V2 (parte del JSON guardada como texto) **no se reprodujo**: `A_hulthen/<δ>/transferencia` es un objeto JSON en los tres δ, en el archivo anterior y en el nuevo. (5) El script tarda ahora 133 s (80 autovalores del pozo en 108 s con 3 procesos). Pasan 22 criterios, falla 1 (B3b, nuevo) y 5 se miden.
