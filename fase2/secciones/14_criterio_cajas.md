# 14. Criterio de cajas (9.6) con la condición (c): la integral de camino en las mismas cajas

Fecha: 27-10-2026. Equipo: Juan Sebastián Calixto y Luis Felipe Ramírez. Unidades $\hbar=m=g=1$, $V=-e^{-\delta r}/r$, $\delta_c=1.1906124211$.

Script: `fase2/codigo/14_criterio_cajas.py` (95 s en total, determinista, sin números aleatorios). Resultados: `fase2/resultados/14_cajas.json`. Salida completa: `fase2/verificacion/14_criterio_cajas_salida.txt`. Figura: `fase2/figuras/14_cajas.png`.

## 14.1 Qué faltaba

En la Fase 1 el criterio de la sección 9.6 se aplicó solo con el solucionador radial, es decir, con las condiciones (a), (a') y (b). Faltaba la condición (c): *la integral de camino (transferencia) da el mismo signo y la misma tendencia en las mismas cajas, dentro de sus errores*. Aquí se calcula, para $\delta\in\{1.15,1.18,1.20\}$ y $R\in\{50,100,200,400,800\}$, $E_0$, $\langle r\rangle/R$ y $F_{1/2}$ con la matriz de transferencia, y se comparan celda a celda con el radial.

## 14.2 Cómo se calculó

- **Transferencia** (`transferencia.py`, sección 11): núcleo libre con imagen, acción de pares exacta de Coulomb $U_C$ tabulada con Richardson en $h_{\rm tab}=0.01/0.005$ (`pares.py`) y resto $W=(1-e^{-\delta r})/r$ en factorización simétrica.
- Se usaron **todas** las combinaciones $\epsilon\in\{0.2,0.1,0.05\}$ y $h\in\{0.02,0.04\}$ en **todas** las cajas, no solo en las decisivas. Eso suma 90 autovalores.
- **Malla:** Richardson en $h$ con exponente 4, $E_{hR}=(16E_{0.02}-E_{0.04})/15$, como propone la sección 11.4.
- **Trotter:** extrapolación con la ley $\epsilon^2$, $E=E_{hR}(0.05)+[E_{hR}(0.05)-E_{hR}(0.1)]/3$.
- **Error de la transferencia:** $|E_{\rm ext}(h{=}0.02)-E|$ (corrección de malla) más $|E-E_{\rm ext}(0.2,0.1)|$ (estabilidad de la extrapolación en $\epsilon$) **más, desde V3, el sesgo de la pared en $R$** (14.4): $|{\rm ext}_{\epsilon^2}[E_{\rm rad}(R+\beta\sqrt\epsilon)-E_{\rm rad}(R)]|$ con $\epsilon=0.1, 0.05$, $\beta=0.5826$.
- **Observables** $\langle r\rangle/R$ y $F_{1/2}$: se toman del autovector con $h=0.02$ y se extrapolan en $\epsilon^2$. Su error suma la diferencia con $h=0.04$ y la diferencia entre las dos extrapolaciones.
- **Autovalor:** `eigsh` en modo *shift-invert*, con $\sigma=e^{-\epsilon(E_{\rm guess}-2\times10^{-4})}$. `which='LA'` sin desplazamiento no terminó en más de 2 minutos con $R=800$ y se abandonó. Para no depender de $\sigma$ se comprueba Perron-Frobenius: como $T\ge0$, el único autovector de signo constante es el del mayor autovalor. En las 90 soluciones el autovector salió de signo constante (mínimo/máximo $\ge +3.5\times10^{-13}$) y el residuo $\|Tv-\lambda v\|$ quedó $<10^{-15}$.
- **Costo:** con $R=800$ y $h=0.02$ ($N=39999$, $8.8\times10^6$ elementos no nulos con $\epsilon=0.1$), cada autovalor tarda de 2.3 a 8.0 s en la ejecución final (hasta 8.4 s en una anterior, según la carga). **No hizo falta** sustituir $h=0.02$ por $h=0.04$ más Richardson.
- **Referencia:** `10_radial.json` (`cajas_9_6`), diferencias finitas con $h=1/40$ y $1/80$ y Richardson. Como error del radial se toma, de forma conservadora, $|E_{\rm Rich}-E_{1/80}|$.
- **"Compatible"** significa $|E_{\rm tr}-E_{\rm rad}|\le2(\text{err}_{\rm tr}+\text{err}_{\rm rad})$.

## 14.3 Tabla celda a celda

**Tabla rehecha en V3** (corrección de Wigner-Kirkwood de $U_C$ fuera de $r=10$ y sesgo de pared en el error; la tabla anterior está en `resultados/archivo_pre_V3/secciones/`). Columnas: $E_0$ del radial; $E_0$ de la transferencia extrapolada ± su error (que ahora incluye el sesgo de pared); la diferencia; el sesgo de pared extrapolado y la diferencia corregida por él; si $|{\rm dif}|\le{\rm err}_{\rm tr}$ (entre paréntesis, sin el término de pared); la transferencia con $\epsilon=0.1$, $h=0.02$ sin extrapolar y su desviación relativa a $|E_0|$; la misma desviación con $\epsilon=0.2$; la diferencia de malla 0.02→0.04 relativa a $|E_0|$; el orden aparente de Trotter; y $\langle r\rangle/R$ y $F_{1/2}$ (radial / transferencia).

| $\delta$ | $R$ | $E_0$ radial | $E_0$ transf. (extrap.) ± err (V3) | dif. | sesgo de pared extrap. | dif. corregida por la pared | $|$dif$|\le$ err | $E(\epsilon{=}0.1)$ | desv. $\epsilon{=}0.1$ | desv. $\epsilon{=}0.2$ | malla | orden | $\langle r\rangle/R$ | $F_{1/2}$ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1.15 | 50 | −3.3082e−4 | −3.3178e−4 ± 1.5e−6 | −9.6e−7 | −1.0e−6 | +7.5e−8 | sí (no) | −3.3610e−4 | 1.6 % | 5.1 % | 8.4e−4 | 1.837 | 0.2393 / 0.2396 | 0.8955 / 0.8950 |
| 1.15 | 100 | −4.5117e−4 | −4.5121e−4 ± 8.3e−8 | −3.8e−8 | −3.3e−8 | −5.4e−9 | sí (sí) | −4.5431e−4 | 0.69 % | 2.7 % | 3.6e−4 | 1.982 | 0.1639 / 0.1640 | 0.9622 / 0.9621 |
| 1.15 | 200 | −4.5587e−4 | −4.5588e−4 ± 3.5e−8 | −8.2e−9 | −7.4e−11 | −8.1e−9 | sí (sí) | −4.5889e−4 | 0.66 % | 2.6 % | 3.5e−4 | 1.989 | 0.0872 / 0.0872 | 0.9976 / 0.9976 |
| 1.15 | 400 | −4.5588e−4 | −4.5589e−4 ± 3.5e−8 | −8.1e−9 | +3.2e−13 | −8.1e−9 | sí (sí) | −4.5890e−4 | 0.66 % | 2.6 % | 3.5e−4 | 1.989 | 0.0436 / 0.0436 | 1.0000 / 1.0000 |
| 1.15 | 800 | −4.5588e−4 | −4.5589e−4 ± 3.5e−8 | −8.1e−9 | +9.1e−13 | −8.1e−9 | sí (sí) | −4.5890e−4 | 0.66 % | 2.6 % | 3.5e−4 | 1.989 | 0.0218 / 0.0218 | 1.0000 / 1.0000 |
| 1.18 | 50 | +3.3801e−4 | +3.3620e−4 ± 2.8e−6 | −1.8e−6 | −2.0e−6 | +1.5e−7 | sí (no) | +3.3235e−4 | 1.7 % | 4.4 % | 8.7e−4 | 1.647 | 0.2924 / 0.2930 | 0.8317 / 0.8308 |
| 1.18 | 100 | +3.2133e−5 | +3.1949e−5 ± 2.9e−7 | −1.8e−7 | −2.0e−7 | +1.2e−8 | sí (no) | +3.0301e−5 | 5.7 % | 20 % | 2.8e−3 | 1.919 | 0.2674 / 0.2677 | 0.8589 / 0.8585 |
| 1.18 | 200 | −2.4059e−5 | −2.4077e−5 ± 2.3e−8 | −1.7e−8 | −1.5e−8 | −2.5e−9 | sí (no) | −2.5124e−5 | 4.4 % | 17 % | 2.1e−3 | 1.994 | 0.2249 / 0.2250 | 0.9044 / 0.9043 |
| 1.18 | 400 | −3.0746e−5 | −3.0750e−5 ± 1.2e−8 | −4.4e−9 | −4.2e−10 | −3.9e−9 | sí (sí) | −3.1636e−5 | 2.9 % | 12 % | 1.4e−3 | 2.014 | 0.1527 / 0.1527 | 0.9673 / 0.9673 |
| 1.18 | 800 | −3.0981e−5 | −3.0985e−5 ± 1.4e−8 | −4.1e−9 | −7.9e−13 | −4.1e−9 | sí (sí) | −3.1857e−5 | 2.8 % | 11 % | 1.3e−3 | 2.017 | 0.0805 / 0.0805 | 0.9982 / 0.9982 |
| 1.20 | 50 | +6.4370e−4 | +6.4126e−4 ± 3.8e−6 | −2.4e−6 | −2.7e−6 | +2.1e−7 | sí (no) | +6.3752e−4 | 0.96 % | 2.2 % | 5.0e−4 | 1.491 | 0.3238 / 0.3245 | 0.7899 / 0.7888 |
| 1.20 | 100 | +1.8687e−4 | +1.8653e−4 ± 5.2e−7 | −3.4e−7 | −3.6e−7 | +2.7e−8 | sí (no) | +1.8540e−4 | 0.78 % | 2.3 % | 3.8e−4 | 1.787 | 0.3313 / 0.3316 | 0.7767 / 0.7760 |
| 1.20 | 200 | +5.7981e−5 | +5.7930e−5 ± 7.7e−8 | −5.1e−8 | −5.4e−8 | +3.3e−9 | sí (no) | +5.7552e−5 | 0.74 % | 2.6 % | 3.5e−4 | 1.915 | 0.3519 / 0.3521 | 0.7464 / 0.7460 |
| 1.20 | 400 | +1.8439e−5 | +1.8431e−5 ± 1.1e−8 | −8.3e−9 | −8.6e−9 | +2.7e−10 | sí (no) | +1.8319e−5 | 0.65 % | 2.4 % | 3.0e−4 | 1.973 | 0.3859 / 0.3860 | 0.6959 / 0.6957 |
| 1.20 | 800 | +5.6686e−6 | +5.6672e−6 ± 1.6e−9 | −1.4e−9 | −1.4e−9 | +2.4e−11 | sí (no) | +5.6417e−6 | 0.47 % | 1.8 % | 2.1e−4 | 2.007 | 0.4256 / 0.4256 | 0.6334 / 0.6333 |

Las 15 celdas son compatibles con el criterio de arriba (también tras V3). Las cifras con todos sus dígitos están en el JSON.

**Errores comparados con $|E_0|$, que es lo que pedía la Fase 1 (allí, 18 % con $h=1/20$ en el radial):**
- **Malla Nyström** (0.02 frente a 0.04): a lo sumo $2.8\times10^{-3}$ de $|E_0|$, en $\delta=1.18$, $R=100$. El criterio (a'), cociente $<0.1$, se cumple con mucho margen en las 15 celdas.
- **Trotter: este es el error grande cerca del umbral.**
  - Con $\epsilon=0.1$ sin extrapolar, la transferencia queda hasta un **5.7 %** de $|E_0|$ (5.9 % antes de V3) por debajo del radial ($\delta=1.18$, $R=100$).
  - Con $\epsilon=0.2$, hasta un **20 %** (21 % antes de V3).
  - El sesgo tiene siempre el mismo signo: baja la energía.
  - En estas cajas no cambia ningún signo, pero en un $\delta$ apenas por encima de $\delta_c$ un $\epsilon$ grueso sin extrapolar podría dar un "ligado" falso. **Regla:** cerca del umbral solo se usa la transferencia extrapolada en $\epsilon$.
  - Después de extrapolar, la diferencia con el radial es como mucho $5.7\times10^{-3}$ de $|E_0|$ (en $R=50$ y $100$, ver 14.4) y $\le8.7\times10^{-4}$ en $R\ge200$ (antes de V3: $5.9\times10^{-3}$ y $9.1\times10^{-4}$).

## 14.4 Lo que no sale perfecto: la pared en $R$ no tiene imagen

**Corrección V3 (hallazgo H1 de V1 y de V2, reproducido).** La primera versión de este párrafo decía que la diferencia con el radial superaba el error de la transferencia sola solo en 5 celdas ($R=50$ las tres $\delta$; $R=100$ con $\delta=1.18$ y $1.20$). **Era falso:** con los números del propio JSON fallaba en **11 de 15** celdas, también en $R\ge200$ (por ejemplo $\delta=1.20$, $R=800$: $-1.50\times10^{-9}$ frente a $1.63\times10^{-10}$). Tras la corrección de Wigner-Kirkwood (que quita $\sim4$–$10\times10^{-9}$ de la diferencia en $R\ge200$), sin el término de pared fallan 9 de 15 (las mismas 9 que V1 encontró con su radial exacto): $\delta=1.15$ $R=50$; $\delta=1.18$ $R=50,100,200$; $\delta=1.20$ en las cinco cajas. **Con el sesgo de pared incluido en el error pasan las 15**, y la diferencia corregida por la pared queda en $\le2.1\times10^{-7}$ ($R=50$) y $\le8.1\times10^{-9}$ en $R\ge200$. En la versión anterior esas celdas pasaban como "compatibles" solo por el error conservador del radial y el factor 2. El orden de Trotter sigue cayendo a 1.49–1.84 en $R=50$ y 1.79 en $R=100$ ($\delta=1.20$).

**Causa (medida).** $K_D$ tiene imagen solo en $r=0$. En $r=R$ la condición de Dirichlet se impone únicamente en los nodos de tiempo: el camino puede salir y volver entre dos eslabones. Para un movimiento browniano vigilado en tiempos discretos, la pared efectiva se corre hacia afuera $\beta\sqrt\epsilon$, con $\beta=-\zeta(1/2)/\sqrt{2\pi}=0.5826$ (corrección de Broadie, Glasserman y Kou; atribución de memoria de la IA, fuente NO VERIFICADA, Parte XI.3 de la bitácora). Por eso la energía sale más baja y su dependencia en $\epsilon$ trae un término $\sqrt\epsilon$ que la ley $\epsilon^2$ no elimina.

Prueba hecha en el script: se compara $E_{hR}(\epsilon)$ con el radial **en la caja $R+0.5826\sqrt\epsilon$**.

| $\delta$, $R$ | orden sin corregir | orden con la pared corrida | dif. extrapolada sin corregir | con la pared corrida |
|---|---|---|---|---|
| 1.15, 50 | 1.837 | 1.985 | −9.6e−7 | +7.5e−8 |
| 1.18, 50 | 1.647 | 1.984 | −1.8e−6 | +1.5e−7 |
| 1.18, 100 | 1.919 | 1.991 | −1.8e−7 | +1.2e−8 |
| 1.20, 50 | 1.491 | 1.984 | −2.4e−6 | +2.1e−7 |
| 1.20, 100 | 1.787 | 1.991 | −3.4e−7 | +2.7e−8 |
| 1.20, 200 | 1.915 | 2.003 | −5.1e−8 | +3.3e−9 |

Con la pared corrida el orden vuelve a 1.98–2.00 y la diferencia baja de 12 a 16 veces. En $R=50$ queda un residuo de $0.8$–$2.1\times10^{-7}$ ($\le4.6\times10^{-4}$ de $|E_0|$). (Tabla y cifras de este párrafo actualizadas desde `14_cajas.json` en la revisión final del 27-10-2026; la versión anterior tenía las de la ejecución previa a V3.) El efecto decae como $\sim R^{-3}$ en $\delta=1.20$ ($2.4\times10^{-6}\to1.4\times10^{-9}$ de 50 a 800), como se espera de $\partial E/\partial R\cdot\Delta R$. **No cambia ningún signo ni ninguna tendencia**, pero conviene saberlo para la Fase 4:
- (i) aplicar la corrección $R\to R+0.5826\sqrt\epsilon$, o poner una imagen también en $R$;
- (ii) no fiarse de la extrapolación $\epsilon^2$ en cajas donde $u(R/2)$ no es despreciable.

Otros residuos declarados:
- En $R\ge200$ quedaba una diferencia de volumen de $-1.8\times10^{-8}$ ($\delta=1.15$) y $-8\times10^{-9}$ ($\delta=1.18$). **V3:** venía en buena parte de la aproximación de extremos de $U_C$ fuera de $r=10$ (H2 de V2 / H3 de V1); con el término de Wigner-Kirkwood baja a $-8.1\times10^{-9}$ y $-4.1$ a $-4.4\times10^{-9}$ ($\le1.8\times10^{-5}$ de $|E_0|$), dentro del error estimado. Su origen restante no está identificado (el radial de referencia con $h=1/40,1/80$ tiene un residuo de ese orden).
- **Orden de la malla Nyström cerca del umbral** ($\delta=1.18$, $\epsilon=0.1$, $h=0.04,0.02,0.01$): 1.361 en $R=50$ y 2.287 en $R=100$, **no 4** como en $\delta\le1$ (sección 11.4). El exponente 4 de Richardson no está justificado aquí. Como la corrección de malla es $\le3\times10^{-3}$ de $|E_0|$, el error que esto mete es de $\sim10^{-7}$ en $R=50$ y no afecta al veredicto. Para la Fase 4 conviene usar $h=0.02$ y $0.01$.

## 14.5 Criterio completo y veredicto

Se prueban las ternas $(50,100,200)$, $(100,200,400)$ y $(200,400,800)$ con el radial y con la transferencia por separado, y además la condición (c), que pide tres cosas a la vez:
- **mismo signo** de $E_0$ en las tres cajas, con $|E_{\rm tr}|>$ su error;
- **misma dirección** de cambio de $\langle r\rangle/R$ y de $F_{1/2}$;
- $E_0$ **compatible** en las tres cajas.

Para "no ligado" la ley de caja es $E\simeq\pi^2/[2(R-a_s)^2]$, con $a_s$ de la solución a energía cero ($a_s(1.20)=-142.93$; coincide con el $-143$ de la Fase 1). Se exige desviación relativa $<0.1$ en $R_3$ y decreciente.

| $\delta$ | terna | radial (a), (a'), (b) | transf. (a), (a'), (b) | no ligado: signo, tend., ley (rad. / transf.) | (c) | decide |
|---|---|---|---|---|---|---|
| 1.15 | 50, 100, 200 | sí, sí, sí (saturación 0.010) | sí, sí, sí (0.010) | no | sí | **ligado** |
| 1.15 | 100, 200, 400 | sí, sí, sí | sí, sí, sí | no | sí | (ligado) |
| 1.15 | 200, 400, 800 | sí, sí, sí | sí, sí, sí | no | sí | (ligado) |
| 1.18 | 50, 100, 200 | no, sí, no ($E(100)>0$) | no, sí, no | no | sí | – |
| 1.18 | 100, 200, 400 | no (saturación 0.217 > 0.1), sí, sí | no (0.217), sí, sí | no | sí | – |
| 1.18 | 200, 400, 800 | sí, sí, sí (0.008; $F_{1/2}(800)=0.9982$) | sí, sí, sí (0.008; 0.9982) | no | sí | **ligado** |
| 1.20 | 50, 100, 200 | no | no | sí, sí, no (desv. 0.38 en $R_3$) | sí | – |
| 1.20 | 100, 200, 400 | no | no | sí, sí, no (desv. 0.101 en $R_3$) | sí | – |
| 1.20 | 200, 400, 800 | no | no | sí, sí, **sí** (desv. 0.382, 0.101, 0.021) | sí | **no ligado** |

En las nueve ternas la transferencia reproduce **exactamente** el mismo patrón de pasa / no pasa que el radial: (c) se cumple en todas.

**Veredicto:**
- $\delta=1.15$: **ligado**, con la terna $R=50,100,200$.
- $\delta=1.18$: **ligado**, con la terna $R=200,400,800$. Con cajas menores el criterio no decide; con el signo solo en $R=50$ o $100$ se habría concluido "no ligado", el error que el criterio está hecho para evitar.
- $\delta=1.20$: **no ligado**, con la terna $R=200,400,800$. Lo que decide es la ley de caja con $a_s=-142.9$: la desviación cae a 2.1 % en $R=800$. Con la terna $(100,200,400)$ queda al borde (0.101 frente a 0.1) y se declara indeterminado.

Los tres veredictos concuerdan con $\delta_c=1.1906124211$. Queda así $\delta_c\in[1.18,\,1.20]$ con dos métodos independientes.

**Advertencia sobre el umbral de la ley de caja.** El 0.1 para la desviación de la ley de caja **lo fijé yo** en esta tarea, porque 9.6 no da número. Con 0.1 la terna intermedia de $\delta=1.20$ queda fuera por 0.001. El veredicto final no depende de eso (la terna mayor da 0.021), pero lo debe revisar quien verifica.

## 14.6 Figura

`fase2/figuras/14_cajas.png`: $E_0$ (escala symlog), $\langle r\rangle/R$ y $F_{1/2}$ frente a $R$ para los tres $\delta$. Las líneas son el radial y los círculos la transferencia extrapolada; las barras de error de la transferencia son más chicas que los marcadores. Se ve que la transferencia sigue al radial en todas las cajas: $\langle r\rangle/R$ y $F_{1/2}$ van hacia 0 y 1 en los ligados, y hacia 1/2 y 1/2 en $\delta=1.20$.


## 14.7 Correcciones tras la verificación (V3, 27-10-2026)

Detalle en `fase2/verificacion/V3_respuesta_hallazgos.md`.
- **H1 (V1 y V2):** texto de 14.4 corregido; el error de la transferencia incluye ahora el sesgo de pared (`err`; el anterior queda como `err_sin_pared`). Criterio estricto $|{\rm dif}|\le{\rm err}_{\rm tr}$: 15/15 con el término de pared, 6/15 sin él (`V3_criterio_estricto` en el JSON).
- **H2 de V2 / H3 de V1:** $U_C$ fuera de $r=10$ con Wigner-Kirkwood. Las energías extrapoladas suben entre $+1.3\times10^{-10}$ ($\delta=1.20$, $R=800$) y $+1.2\times10^{-8}$ ($\delta=1.15$, $R=50$).
- **H13 de V2:** el radial tiene ahora error de malla en $\langle r\rangle/R$ y $F_{1/2}$ ($|X_{\rm Rich}-X_{1/80}|$): entre $3\times10^{-5}$ y $6.8\times10^{-4}$ en $\langle r\rangle/R$, y hasta $5.9\times10^{-4}$ en $F_{1/2}$. Las diferencias entre radial y transferencia ($\le7\times10^{-4}$) son de ese tamaño. No cambia ninguna tendencia.
- **No cambia nada de 14.5:** los mismos veredictos (1.15 ligado con 50/100/200; 1.18 ligado con 200/400/800; 1.20 no ligado con 200/400/800), (c) en las 9 ternas, saturaciones y desviaciones de la ley de caja (0.382, 0.101, 0.021) iguales en sus tres cifras. El umbral 0.1 de la ley de caja sigue pendiente de aprobación.
- El script tarda ahora 101 s (30 soluciones radiales más).
