# V1. Recálculo numérico independiente de la Fase 2

Fecha: 27-10-2026. Verificador independiente (agente de verificación). Proyecto 05: umbral de ligadura del 1s de $V=-e^{-\delta r}/r$ ($\hbar=m=g=1$).

## 1. Qué se hizo y con qué independencia

No se importó ni se copió código de `fase1/codigo` ni de `fase2/codigo`. De los scripts del proyecto solo se leyeron dos definiciones para comparar lo mismo: la desviación de la ley de caja de la sección 14 y la regla de corte $R_{\rm TAB}=10$ de `pares.py`. Todo el código propio está en `fase2/verificacion/codigo_independiente/` y sus resultados en `fase2/verificacion/codigo_independiente/resultados/`.

| Parte | Script | Método propio (distinto del proyecto) | Tiempo |
|---|---|---|---|
| A | `v1a_radial_disparo.py` (`v_disparo.py`, `v_fedvr.py`) | Disparo con `solve_ivp` DOP853 (rtol $10^{-12}$), arranque con la serie $u=r-Zr^2$. Integrales $\int u^2$, $\int ru^2$, $\int r^2u^2$ integradas en la misma EDO. Empalme hacia afuera y hacia adentro en espacio libre, y $u(R)=0$ en caja. Segunda base: FEDVR (elementos finitos de Gauss-Lobatto) | 28 s |
| B | `v1b_trotter_espectral.py` (`v_trotter.py`) | Operador de Trotter $e^{-\epsilon W/2}e^{-\epsilon H_C}e^{-\epsilon W/2}$ construido diagonalizando $H_C$ en la base FEDVR. No usa tabla de $U_C$ ni Nyström: es el límite $h\to0$ exacto de la matriz de transferencia del proyecto. Se usa la forma semejante $B^{1/2}e^{-\epsilon W}B^{1/2}$ (mismo espectro) | 419 s (más 262 s con la base fina) |
| C | `v1c_nystrom_propio.py` | Núcleo $\rho_C(r,r';\epsilon)$ propio, sumando el espectro FEDVR en una caja $R_b=46$ y evaluándolo punto a punto. Nyström propio (trapecio) con $h=0.04$, 0.02 y 0.01 | 61 s |
| D | `v1d_pigs_series.py` | Reanálisis de `12_pigs_series.npz`: medias, binning de Flyvbjerg-Petersen, jackknife entre cadenas y $\tau_{\rm int}$ con ventana automática propia | 2 s |
| E | `v1e_proyeccion.py` | $E_{\rm mixto}(\tau)$ y $\langle r\rangle$, $\langle r^2\rangle$ puros con el operador espectral, más una comprobación de convergencia en $\delta=1.0$ | 7 s |
| F | `v1f_extremos.py` | Efecto de la aproximación de extremos de $U_C$ para $r>10$, aislado con el núcleo exacto propio | 15 s |
| G, H | `v1g_comparacion.py`, `v1h_tau5.py` | Tabla de comparación, criterio 9.6 recalculado y combinación de las cadenas de $\tau=5$ | 1 s |

**Convergencia de lo propio.** La base FEDVR con $n=12$ puntos por elemento y la base fina ($n=14$, elementos de la mitad) dan el mismo $E(\epsilon)$ con diferencias $\le3\times10^{-12}$ en $\delta=0.2$, en Hulthén y en el pozo. En $\delta=1.0$ con $R=174$ la diferencia es $\le3\times10^{-12}$ entre tres bases. El disparo reproduce Coulomb y Hulthén exactos a $10^{-14}$ en $E$ y en $\langle r\rangle$. El núcleo libre de la base reproduce $K_D$ exacto con error relativo $\le7.5\times10^{-11}$. Todas las salidas impresas están en `codigo_independiente/resultados_v1*_salida.txt`. Se usaron como mucho 4 hilos a la vez.

## 2. Resumen

Se recalcularon **252 cifras**: **227 coinciden** dentro de su tolerancia y **25 no**. Todas las discrepancias se reprodujeron y se explican en la sección 3. **Ninguna cambia los veredictos** (sección 4) ni el valor de $\delta_c$.

Lo que se confirma (lista corta):
- **Radial.** Coulomb, $\delta=0.2$, $\delta_c=1.1906124210606$ (diferencia $4\times10^{-14}$), $\delta_c(2s)=0.3102092827$, Hulthén (energías, $\langle r\rangle$ y umbrales) y el pozo. Las 15 celdas de cajas coinciden dentro del error declarado y en 3 cifras de $\langle r\rangle/R$ y $F_{1/2}$. Las tres $a_s$ coinciden a $10^{-11}$ relativo. Se confirma la errata de la tabla 9.6 de la Fase 1: $E_0(1.18,400)$ es $-3.07\times10^{-5}$, no $-3.08\times10^{-5}$.
- **Peso.** $U_C$ coincide a $\sim10^{-9}$ en todos los puntos comparados, por ejemplo $U(0.01,0.01;0.2)=-1.132354446$ frente a $-1.1323544455$.
- **Error de Nyström.** El error $h^4/\epsilon$ (estabilidad 0.02→0.04 de $1.599\times10^{-6}$ en Coulomb con $\epsilon=0.1$, orden 3.9994) **reaparece igual con el núcleo exacto propio**. Por tanto no viene de la tabla de $U_C$ sino del trapecio en la cúspide, como dice la sección 11. El criterio 9.7 de estabilidad sí falla, como reportó el proyecto.
- **Trotter.** En $\delta=0.2$ el orden en el continuo es 1.9895 y el extrapolado $-0.32680851119$ queda a $1.8\times10^{-10}$ del radial exacto. Las $E(\epsilon)$ del proyecto (con Richardson en $h$) difieren de las mías en $+1.0$, $+2.1$ y $+4.2\times10^{-9}$, un residuo $\propto1/\epsilon$ de la tabla.
- **Hulthén.** En $\delta=0.2$ el sesgo de Trotter verdadero vale $-1.8\times10^{-8}$, $-4.6\times10^{-9}$ y $-1.1\times10^{-9}$, con orden 1.99. El "orden 1.38" del proyecto es el residuo de la tabla, como el propio proyecto explicó.
- **Proyección.** $E_{\rm mixto}(\tau)$ y $E_{\rm det}(\tau)$ coinciden a $\le6\times10^{-11}$ en $\tau=2,5,10,20$, y $\langle r\rangle_{\rm det}$ a $\le7\times10^{-9}$.
- **PIGS.** Medias y errores salen idénticos a partir de las series; el $-3.19\sigma$ de $\tau=5$ se reproduce frente a un $E_{\rm det}$ exacto independiente.
- **Hipótesis de la pared corrida $0.5826\sqrt\epsilon$ (sección 14).** Se confirma de forma independiente: con pared Dirichlet verdadera mi transferencia queda a $\le3\times10^{-9}$ del radial en las 15 celdas, con orden 1.99 a 2.04. Con la pared en $R+0.5826\sqrt\epsilon$ reproduce los $E_{h{\rm Rich}}(\epsilon)$ del proyecto a $\le2.2\times10^{-7}$; sin corregir la diferencia llega a $6\times10^{-6}$.

## 3. Hallazgos (discrepancias reproducidas)

**H1 (media). El error declarado de la transferencia en las cajas, `err_tr`, se queda corto en más celdas de las que dice la sección 14.** La sección afirma que $|E_{\rm tr}-E_{\rm rad}|\le$ `err_tr` falla "en R=50 (las tres delta) y en R=100 (delta 1.18 y 1.20)", es decir, en 5 celdas. Con los números del propio JSON (radial del proyecto) falla en **11 de 15**. Frente a mi radial exacto falla en **9 de 15**: además de esas 5, en $\delta=1.18$, $R=200$ ($-1.86\times10^{-8}$ frente a $1.63\times10^{-8}$) y en $\delta=1.20$, $R=200$, 400 y 800 ($-5.15\times10^{-8}$ frente a $2.64\times10^{-8}$; $-8.4\times10^{-9}$ frente a $3.4\times10^{-9}$; $-1.33\times10^{-9}$ frente a $1.6\times10^{-10}$). La causa es la misma pared sin imagen: en los estados de caja de $\delta=1.20$ la densidad llega a la pared en todas las $R$, y el resto $\sqrt\epsilon$ no lo quita la extrapolación $\epsilon^2$. Con pared verdadera mi transferencia queda a $\le3\times10^{-9}$ en todas las celdas. No cambia ningún signo, ninguna tendencia ni ningún veredicto. **Corrección:** sumar a `err_tr` el sesgo de pared estimado (por ejemplo $|E_{\rm tr}(R)-E_{\rm tr}(R+0.58\sqrt\epsilon)|$), o poner la imagen en $R$, y corregir en la sección 14 la lista de celdas que no pasan.

**H2 (media). Pozo cuadrado: los valores "$h\to0$" de la transferencia ($E_{h0}$) no están convergidos a la tolerancia de B3.** Frente al operador de Trotter continuo (con el salto en un borde de elemento, convergido a $10^{-11}$), los $E_{h0}$ del proyecto para $V_0=2$ con borde medio se desvían en $-1.15$, $-2.19$, $-2.42$, $-2.02$ y $-1.37\times10^{-5}$ para $\epsilon=0.2$ a $0.0125$. Eso es más que la cota $10^{-5}$ de B3; para $V_0=1.3$ las desviaciones van de $5.3\times10^{-6}$ a $2.7\times10^{-7}$. Los órdenes en $\epsilon$ sí coinciden: 1.497, 1.498 y 1.499 propios frente a 1.497, 1.502 y 1.511. Mi extrapolación continua con el orden medido queda a $+2.3\times10^{-7}$ ($V_0=2$) y $-4.6\times10^{-7}$ ($V_0=1.3$) del exacto. El $+6.2\times10^{-6}$ del proyecto es, por tanto, casi todo error de la extrapolación de Nyström en $h$ (orden $h^1$ no estabilizado), no de la ley $\epsilon^{3/2}$: B3 pasa en parte por compensación. El ajuste a 5 puntos que según el proyecto "no pasaría" ($1.5\times10^{-5}$) da $-5.8\times10^{-6}$ con el operador continuo. Además, el límite $h\to0$ es el mismo con borde medio y con borde estricto (el valor en un solo nodo no cuenta en el continuo). El $-2.0\times10^{-3}$ del borde estricto es error de Nyström, no una propiedad de la integral de camino. **Corrección:** declarar que el error de B3 lo domina la extrapolación en $h$, y para el pozo usar mallas más finas o poner el salto entre nodos con una cuadratura que lo respete. La conclusión cualitativa (orden $\epsilon^{3/2}$) se mantiene.

**H3 (baja). La aproximación de extremos $U_C\approx\tfrac\epsilon2[V_C(r)+V_C(r')]$ fuera de $r=10$ deja un sesgo de orden $\sim\epsilon^{1.5}$ que la extrapolación $\epsilon^2$ no quita del todo.** Se aisló con el Nyström propio, comparando núcleo exacto y núcleo de extremos ($R=40$, $h=0.02$):
- $\delta=1.0$: $-1.44\times10^{-7}$, $-4.9\times10^{-8}$ y $-1.7\times10^{-8}$;
- $\delta=1.15$: $-2.8\times10^{-7}$, $-9.7\times10^{-8}$ y $-3.4\times10^{-8}$, con $\epsilon=0.2$, 0.1 y 0.05;
- $\delta=0.2$: $<3\times10^{-11}$.

Esto explica, con su valor:
- la diferencia de las $E(\epsilon)$ del proyecto en $\delta=1.0$ frente al continuo: $-1.43\times10^{-7}$, $-4.84\times10^{-8}$ y $-1.58\times10^{-8}$;
- la de Hulthén $\delta=1.5$: $-3.7\times10^{-8}$ con $\epsilon=0.2$;
- el "residuo de volumen" de $-1.35\times10^{-8}$ en $\delta=1.15$, $R\ge200$, que la sección 14 dejó sin causa. Para un término $c\,\epsilon^{1.5}$, la extrapolación $\epsilon^2$ deja $0.0038c\approx1.1\times10^{-8}$.

Todo queda dentro de las tolerancias del plan. **Corrección:** ampliar $R_{\rm TAB}$, o hacer continuo el cambio en $r=10$, o declarar este término en el presupuesto de errores de la Fase 3 y la Fase 4, donde $|E_0|\sim10^{-5}$.

**H4 (baja). El criterio de $\delta=0.2$ en el radial pasa solo frente al valor redondeado.** `10_radial.json` da $E_0=-0.3268085051545$. Frente al exacto $-0.3268085113692$ (disparo y FEDVR coinciden a $5\times10^{-13}$) el error es $6.2\times10^{-9}$, mayor que la tolerancia de $5\times10^{-9}$. El criterio se aplicó contra $-0.32680851$, que tiene él mismo una incertidumbre de $5\times10^{-9}$. **Corrección:** comparar con el valor de $h=1/80$ y $1/160$, o fijar la tolerancia en $10^{-8}$ (el proyecto ya avisa de un residuo de unos $6\times10^{-9}$).

**H5 (baja). La réplica de $\tau=5$ no cierra la anomalía por sí sola.** El $-3.19\sigma$ se reproduce frente a mi $E_{\rm det}(5)=-0.3267626328$, que coincide con el del proyecto a $5\times10^{-11}$, y la réplica da $+0.03\sigma$. Pero la producción y la réplica difieren entre sí en $-2.41\sigma$ ($p=1.6\%$); 7 de las 8 cadenas de producción quedan por debajo de $E_{\rm det}$, y la combinación ponderada de las 24 cadenas queda a $-2.08\sigma$ (a $-1.42\sigma$ con pesos iguales). La fluctuación es una explicación posible, no probada. **Corrección:** reportar la combinación de las 24 cadenas, o correr una segunda réplica.

**H6 (baja). El diagnóstico de la sección 11.4 usa un $u'(0)^2$ sesgado en un 1.25 %.** El JSON da `up0_cuadrado` = 3.9502 en Coulomb, cuando el valor exacto es 4. Para $\delta=0.2$ da 3.7560 frente a mi 3.8033, y para $\delta=1.0$ da 0.91752 frente a 0.92913. El cociente es el mismo (0.9875) en los tres casos, así que la conclusión (error $\propto u'(0)^2$) no cambia, pero el valor de `cociente` (unos $4.0\times10^{-8}$) está inflado en esa misma proporción. **Corrección:** usar el $u'(0)$ del radial.

**H7 (baja, de interpretación).** El "límite del mixto frente a $E_0(T)$ = $1.05\times10^{-7}$" de la sección 11 es el error de Nyström de $E_0(T)$ con $h=0.02$: en el continuo esa diferencia vale $8\times10^{-10}$. El número es correcto y pasa el criterio, pero no es una propiedad del estimador mixto.

**No son hallazgos (cuadran con lo que el proyecto ya declaró):** los órdenes de Trotter en $R=50$ y 100, que la pared rebaja; el orden 1.38 de Hulthén $\delta=0.2$; el borde estricto del pozo; el fallo de estabilidad de Nyström y el de $h=0.04$ en $\delta=0.2$. Todos aparecen como "no" en la tabla porque el valor propio es el del continuo.

## 4. Veredictos de cajas recalculados (criterio 9.6 con números propios)

| $\delta$ | terna | radial propio (disparo) | transferencia propia (espectral, pared verdadera) | proyecto |
|---|---|---|---|---|
| 1.15 | 50/100/200 | ligado (saturación 0.010) | ligado | ligado, 50/100/200 |
| 1.18 | 50/100/200 | no decide ($E(100)>0$) | no decide | igual |
| 1.18 | 100/200/400 | no decide (saturación 0.217) | no decide | igual (0.217) |
| 1.18 | 200/400/800 | **ligado** (saturación 0.008, $F_{1/2}(800)=0.99818$) | **ligado** | ligado, 200/400/800 |
| 1.20 | 100/200/400 | no decide (desviación de la ley 1.235, 0.382, 0.101) | no decide | igual (0.101) |
| 1.20 | 200/400/800 | **no ligado** (desviación 0.382, 0.101, 0.021; $a_s=-142.93486534$) | **no ligado** | no ligado, 200/400/800 |

La condición (c), mismo signo en todas las celdas, se cumple en las 9 ternas. Con esto $\delta_c\in[1.18,1.20]$, y el umbral por energía cero, $1.1906124210606$, queda dentro. El umbral 0.1 de la desviación de la ley de caja lo fijó el proyecto (problema 3 de la sección 14); con él, la terna 100/200/400 de $\delta=1.20$ queda fuera por 0.001 también con mis números.

## 5. Límites de esta verificación

- No corrí una cadena PIGS propia: las series de producción ($\delta=0.2$ y Coulomb) estaban guardadas y se reanalizaron. Para el barrido en $\tau$ ($\tau=2,5,10$) y la réplica solo hay medias por cadena, así que de ellas se recalcularon las desviaciones $\sigma$ frente a mi $E_{\rm det}$, no las medias.
- Mi transferencia de cajas usa pared Dirichlet verdadera, no la convención del proyecto (Dirichlet solo en los nodos), así que compara el límite correcto, no el número crudo; la convención del proyecto solo se probó a través de la hipótesis $R+0.5826\sqrt\epsilon$. El (a′) de mi transferencia se estimó con la diferencia entre dos extrapolaciones en $\epsilon$, no con dos mallas.
- La tabla 5.1 de la Fase 1 y la tabla de órdenes del pozo radial con borde $V(a)=0$ no se recalcularon.
- Las relecturas de los archivos escritos en el montaje se hicieron con `ls` y leyendo el contenido poco después de escribirlos; no fue posible una espera fija de 10 s en primer plano.

## 6. Tabla completa de comparación

Columnas: el bloque, la cifra, el valor del proyecto (leído de `fase2/resultados/*.json`), el valor propio, el método propio, la diferencia (propio − proyecto), la tolerancia usada (la declarada por el proyecto o el plan cuando existe; si no, la indicada) y si coincide. La tabla la genera `v1g_comparacion.py` y también está en `codigo_independiente/resultados/v1_tabla.md` y `v1_comparacion.json`.

| bloque | cifra | valor del proyecto | valor propio | método propio | diferencia | tolerancia | coincide |
|---|---|---|---|---|---|---|---|
| radial | Coulomb E0 | -0.499999993899 | -0.5 | disparo solve_ivp DOP853 (rtol 1e-12) | -6.10e-09 | 1.0e-08 | sí |
| radial | Coulomb E1 | -0.124999999905 | -0.125 | disparo solve_ivp DOP853 (rtol 1e-12) | -9.50e-11 | 1.0e-08 | sí |
| radial | Coulomb <r> | 1.4999999939 | 1.5 | disparo solve_ivp DOP853 (rtol 1e-12) | +6.10e-09 | 1.0e-07 | sí |
| radial | Coulomb <r^2> | 3 | 3 | disparo solve_ivp DOP853 (rtol 1e-12) | +3.59e-13 | 1.0e-07 | sí |
| radial | delta=0.2 E0 (10_radial, h=1/40,1/80) (criterio del proyecto |E0+0.32680851|<5e-9 se cumple frente al valor redondeado, no frente al exacto) | -0.326808505154 | -0.326808511369 | disparo solve_ivp DOP853 (rtol 1e-12) | -6.21e-09 | 5.0e-09 | no |
| radial | delta=0.2 E0 (referencia de 11_transferencia) | -0.326808510981 | -0.326808511369 | disparo solve_ivp DOP853 (rtol 1e-12) | -3.88e-10 | 5.0e-09 | sí |
| radial | delta=0.2 <r> | 1.54972189806 | 1.54972190323 | disparo solve_ivp DOP853 (rtol 1e-12) | +5.17e-09 | 5.0e-05 | sí |
| radial | delta=0.2 <r^2>^1/2 | 1.7960900429 | 1.79609004279 | disparo solve_ivp DOP853 (rtol 1e-12) | -1.08e-10 | 5.0e-05 | sí |
| radial | delta=0.2 E1 (R=60) | -0.0121078621051 | -0.0121078622104 | disparo solve_ivp DOP853 (rtol 1e-12) en caja R=60 | -1.05e-10 | 1.0e-08 | sí |
| radial | delta=1.0 E0 (referencia de 11, R=174) | -0.0102857896314 | -0.01028578999 | disparo solve_ivp DOP853 (rtol 1e-12) | -3.59e-10 | 1.0e-08 | sí |
| radial | delta_c (1s) | 1.19061242106 | 1.19061242106 | disparo solve_ivp DOP853 (rtol 1e-12), E=0, u'(60/delta)=0 | +3.69e-14 | 1.0e-08 | sí |
| radial | delta_c (2s) | 0.310209282714 | 0.310209282714 | disparo solve_ivp DOP853 (rtol 1e-12), E=0 | +1.17e-15 | 1.0e-08 | sí |
| radial | Hulthen 0.2 E0 radial (13) | -0.404999999623 | -0.405 | disparo solve_ivp DOP853 (rtol 1e-12) | -3.77e-10 | 1.0e-08 | sí |
| radial | Hulthen 0.2 <r> exacto (sympy) | 1.5101010101 | 1.5101010101 | disparo solve_ivp DOP853 (rtol 1e-12) | -9.86e-14 | 2.0e-07 rel. | sí |
| radial | Hulthen 1.0 E0 radial (13) | -0.124999999594 | -0.125 | disparo solve_ivp DOP853 (rtol 1e-12) | -4.06e-10 | 1.0e-08 | sí |
| radial | Hulthen 1.0 <r> exacto (sympy) | 1.83333333333 | 1.83333333333 | disparo solve_ivp DOP853 (rtol 1e-12) | -4.31e-14 | 2.0e-07 rel. | sí |
| radial | Hulthen 1.5 E0 radial (13) | -0.0312499995978 | -0.03125 | disparo solve_ivp DOP853 (rtol 1e-12) | -4.02e-10 | 1.0e-08 | sí |
| radial | Hulthen 1.5 <r> exacto (sympy) | 2.78571428571 | 2.78571428571 | disparo solve_ivp DOP853 (rtol 1e-12) | -1.72e-13 | 2.0e-07 rel. | sí |
| radial | Hulthen umbral 1s | 2 | 2 | disparo solve_ivp DOP853 (rtol 1e-12) | +3.29e-14 | 1.0e-08 | sí |
| radial | Hulthen umbral 2s | 0.5 | 0.5 | disparo solve_ivp DOP853 (rtol 1e-12) | -5.50e-15 | 1.0e-08 | sí |
| radial | Hulthen 0.2 E1 | -0.045 | -0.045 | disparo solve_ivp DOP853 (rtol 1e-12) | -7.49e-16 | 1.0e-08 | sí |
| radial | pozo V0=2.0 E exacta | -0.203550741821 | -0.203550741821 | raiz propia de k cot k = -kappa | +2.78e-17 | 1.0e-12 | sí |
| radial | pozo V0=2.0 E radial borde medio | -0.203550741924 | -0.20355074182 | disparo solve_ivp DOP853 (rtol 1e-12) con salto | +1.04e-10 | 2.0e-08 | sí |
| radial | pozo V0=2.0 <r> exacto | 1.28364372758 | 1.28364372758 | disparo solve_ivp DOP853 (rtol 1e-12) | +5.67e-13 | 1.0e-08 | sí |
| radial | pozo V0=1.3 E exacta | -0.00211469914757 | -0.00211469914757 | raiz propia de k cot k = -kappa | -1.95e-17 | 1.0e-12 | sí |
| radial | pozo V0=1.3 E radial borde medio | -0.00211469898117 | -0.00211469914756 | disparo solve_ivp DOP853 (rtol 1e-12) con salto | -1.66e-10 | 2.0e-08 | sí |
| radial | pozo V0=1.3 <r> exacto | 8.1883069057 | 8.18830690571 | disparo solve_ivp DOP853 (rtol 1e-12) | +1.03e-11 | 1.0e-08 | sí |
| radial | pozo umbral pi^2/8 | 1.23370055014 | 1.23370055014 | disparo solve_ivp DOP853 (rtol 1e-12), E=0 | +3.12e-13 | 1.0e-08 | sí |
| radial | a_s delta=1.15 | 34.0200281012 | 34.020028101 | disparo solve_ivp DOP853 (rtol 1e-12), E=0 | -1.77e-10 | 1.0e-06 rel. | sí |
| radial | a_s delta=1.18 | 127.922599609 | 127.922599607 | disparo solve_ivp DOP853 (rtol 1e-12), E=0 | -1.64e-09 | 1.0e-06 rel. | sí |
| radial | a_s delta=1.2 | -142.934865339 | -142.934865341 | disparo solve_ivp DOP853 (rtol 1e-12), E=0 | -2.48e-09 | 1.0e-06 rel. | sí |
| cajas-radial | E0 delta=1.15 R=50 (tol = error declarado del radial) | -3.3081910801e-04 | -3.3082264919e-04 | disparo solve_ivp DOP853 (rtol 1e-12) u(R)=0 | -3.54e-09 | 1.6e-06 | sí |
| cajas-radial | <r>/R delta=1.15 R=50 (3 cifras) | 0.239314417067 | 0.239314381252 | disparo solve_ivp DOP853 (rtol 1e-12) | -3.58e-08 | 5.0e-04 | sí |
| cajas-radial | F_1/2 delta=1.15 R=50 (3 cifras) | 0.895492031183 | 0.895491980698 | disparo solve_ivp DOP853 (rtol 1e-12) (FEDVR si kappa R>10) | -5.05e-08 | 5.0e-04 | sí |
| cajas-radial | E0 delta=1.15 R=100 (tol = error declarado del radial) | -4.5117431711e-04 | -4.5117862061e-04 | disparo solve_ivp DOP853 (rtol 1e-12) u(R)=0 | -4.30e-09 | 1.4e-06 | sí |
| cajas-radial | <r>/R delta=1.15 R=100 (3 cifras) | 0.163935913057 | 0.163936271361 | disparo solve_ivp DOP853 (rtol 1e-12) | +3.58e-07 | 5.0e-04 | sí |
| cajas-radial | F_1/2 delta=1.15 R=100 (3 cifras) | 0.962202433965 | 0.96220180846 | disparo solve_ivp DOP853 (rtol 1e-12) (FEDVR si kappa R>10) | -6.26e-07 | 5.0e-04 | sí |
| cajas-radial | E0 delta=1.15 R=200 (tol = error declarado del radial) | -4.5587346949e-04 | -4.5587807817e-04 | disparo solve_ivp DOP853 (rtol 1e-12) u(R)=0 | -4.61e-09 | 1.3e-06 | sí |
| cajas-radial | <r>/R delta=1.15 R=200 (3 cifras) | 0.0871717697713 | 0.0871724137014 | disparo solve_ivp DOP853 (rtol 1e-12) | +6.44e-07 | 5.0e-04 | sí |
| cajas-radial | F_1/2 delta=1.15 R=200 (3 cifras) | 0.997555048821 | 0.997554696115 | disparo solve_ivp DOP853 (rtol 1e-12) (FEDVR si kappa R>10) | -3.53e-07 | 5.0e-04 | sí |
| cajas-radial | E0 delta=1.15 R=400 (tol = error declarado del radial) | -4.5588440847e-04 | -4.5588902129e-04 | disparo solve_ivp DOP853 (rtol 1e-12) u(R)=0 | -4.61e-09 | 1.3e-06 | sí |
| cajas-radial | <r>/R delta=1.15 R=400 (3 cifras) | 0.0436158181906 | 0.0436161562921 | disparo solve_ivp DOP853 (rtol 1e-12) | +3.38e-07 | 5.0e-04 | sí |
| cajas-radial | F_1/2 delta=1.15 R=400 (3 cifras) | 0.999994004468 | 0.999994000603 | disparo solve_ivp DOP853 (rtol 1e-12) (FEDVR si kappa R>10) | -3.87e-09 | 5.0e-04 | sí |
| cajas-radial | E0 delta=1.15 R=800 (tol = error declarado del radial) | -4.5588440840e-04 | -4.5588902136e-04 | disparo solve_ivp DOP853 (rtol 1e-12) u(R)=0 | -4.61e-09 | 1.3e-06 | sí |
| cajas-radial | <r>/R delta=1.15 R=800 (3 cifras) | 0.021807909467 | 0.0218080781461 | disparo solve_ivp DOP853 (rtol 1e-12) | +1.69e-07 | 5.0e-04 | sí |
| cajas-radial | F_1/2 delta=1.15 R=800 (3 cifras) | 0.999999999966 | 0.999999999966 | disparo solve_ivp DOP853 (rtol 1e-12) (FEDVR si kappa R>10) | -9.16e-14 | 5.0e-04 | sí |
| cajas-radial | E0 delta=1.18 R=50 (tol = error declarado del radial) | 3.3801327469e-04 | 3.3801080309e-04 | disparo solve_ivp DOP853 (rtol 1e-12) u(R)=0 | -2.47e-09 | 1.1e-06 | sí |
| cajas-radial | <r>/R delta=1.18 R=50 (3 cifras) | 0.292449632474 | 0.292449513297 | disparo solve_ivp DOP853 (rtol 1e-12) | -1.19e-07 | 5.0e-04 | sí |
| cajas-radial | F_1/2 delta=1.18 R=50 (3 cifras) | 0.831682437311 | 0.831682525496 | disparo solve_ivp DOP853 (rtol 1e-12) (FEDVR si kappa R>10) | +8.82e-08 | 5.0e-04 | sí |
| cajas-radial | E0 delta=1.18 R=100 (tol = error declarado del radial) | 3.2132958192e-05 | 3.2130373618e-05 | disparo solve_ivp DOP853 (rtol 1e-12) u(R)=0 | -2.58e-09 | 6.3e-07 | sí |
| cajas-radial | <r>/R delta=1.18 R=100 (3 cifras) | 0.267440364066 | 0.26744007157 | disparo solve_ivp DOP853 (rtol 1e-12) | -2.92e-07 | 5.0e-04 | sí |
| cajas-radial | F_1/2 delta=1.18 R=100 (3 cifras) | 0.858870699119 | 0.858870744003 | disparo solve_ivp DOP853 (rtol 1e-12) (FEDVR si kappa R>10) | +4.49e-08 | 5.0e-04 | sí |
| cajas-radial | E0 delta=1.18 R=200 (tol = error declarado del radial) | -2.4059498736e-05 | -2.4062643329e-05 | disparo solve_ivp DOP853 (rtol 1e-12) u(R)=0 | -3.14e-09 | 4.2e-07 | sí |
| cajas-radial | <r>/R delta=1.18 R=200 (3 cifras) | 0.224899488033 | 0.224899649944 | disparo solve_ivp DOP853 (rtol 1e-12) | +1.62e-07 | 5.0e-04 | sí |
| cajas-radial | F_1/2 delta=1.18 R=200 (3 cifras) | 0.904402407946 | 0.904400716268 | disparo solve_ivp DOP853 (rtol 1e-12) (FEDVR si kappa R>10) | -1.69e-06 | 5.0e-04 | sí |
| cajas-radial | E0 delta=1.18 R=400 (tol = error declarado del radial) | -3.0745843193e-05 | -3.0749862271e-05 | disparo solve_ivp DOP853 (rtol 1e-12) u(R)=0 | -4.02e-09 | 3.6e-07 | sí |
| cajas-radial | <r>/R delta=1.18 R=400 (3 cifras) | 0.152663378405 | 0.152670539018 | disparo solve_ivp DOP853 (rtol 1e-12) | +7.16e-06 | 5.0e-04 | sí |
| cajas-radial | F_1/2 delta=1.18 R=400 (3 cifras) | 0.96727272098 | 0.967261973268 | disparo solve_ivp DOP853 (rtol 1e-12) (FEDVR si kappa R>10) | -1.07e-05 | 5.0e-04 | sí |
| cajas-radial | E0 delta=1.18 R=800 (tol = error declarado del radial) | -3.0981182582e-05 | -3.0985485088e-05 | disparo solve_ivp DOP853 (rtol 1e-12) u(R)=0 | -4.30e-09 | 3.5e-07 | sí |
| cajas-radial | <r>/R delta=1.18 R=800 (3 cifras) | 0.0804584938703 | 0.0804688513263 | disparo solve_ivp DOP853 (rtol 1e-12) | +1.04e-05 | 5.0e-04 | sí |
| cajas-radial | F_1/2 delta=1.18 R=800 (3 cifras) | 0.998181341637 | 0.998176565027 | disparo solve_ivp DOP853 (rtol 1e-12) (FEDVR si kappa R>10) | -4.78e-06 | 5.0e-04 | sí |
| cajas-radial | E0 delta=1.2 R=50 (tol = error declarado del radial) | 6.4370300445e-04 | 6.4370114673e-04 | disparo solve_ivp DOP853 (rtol 1e-12) u(R)=0 | -1.86e-09 | 8.2e-07 | sí |
| cajas-radial | <r>/R delta=1.2 R=50 (3 cifras) | 0.323789335901 | 0.323789198465 | disparo solve_ivp DOP853 (rtol 1e-12) | -1.37e-07 | 5.0e-04 | sí |
| cajas-radial | F_1/2 delta=1.2 R=50 (3 cifras) | 0.78993910013 | 0.789939242119 | disparo solve_ivp DOP853 (rtol 1e-12) (FEDVR si kappa R>10) | +1.42e-07 | 5.0e-04 | sí |
| cajas-radial | E0 delta=1.2 R=100 (tol = error declarado del radial) | 1.8686539029e-04 | 1.8686396593e-04 | disparo solve_ivp DOP853 (rtol 1e-12) u(R)=0 | -1.42e-09 | 3.5e-07 | sí |
| cajas-radial | <r>/R delta=1.2 R=100 (3 cifras) | 0.331279001634 | 0.331278529686 | disparo solve_ivp DOP853 (rtol 1e-12) | -4.72e-07 | 5.0e-04 | sí |
| cajas-radial | F_1/2 delta=1.2 R=100 (3 cifras) | 0.776650795168 | 0.776651288529 | disparo solve_ivp DOP853 (rtol 1e-12) (FEDVR si kappa R>10) | +4.93e-07 | 5.0e-04 | sí |
| cajas-radial | E0 delta=1.2 R=200 (tol = error declarado del radial) | 5.7980606431e-05 | 5.7979632543e-05 | disparo solve_ivp DOP853 (rtol 1e-12) u(R)=0 | -9.74e-10 | 1.3e-07 | sí |
| cajas-radial | <r>/R delta=1.2 R=200 (3 cifras) | 0.351937782207 | 0.351936193955 | disparo solve_ivp DOP853 (rtol 1e-12) | -1.59e-06 | 5.0e-04 | sí |
| cajas-radial | F_1/2 delta=1.2 R=200 (3 cifras) | 0.746364088212 | 0.746365919357 | disparo solve_ivp DOP853 (rtol 1e-12) (FEDVR si kappa R>10) | +1.83e-06 | 5.0e-04 | sí |
| cajas-radial | E0 delta=1.2 R=400 (tol = error declarado del radial) | 1.8439147959e-05 | 1.8438643978e-05 | disparo solve_ivp DOP853 (rtol 1e-12) u(R)=0 | -5.04e-10 | 4.1e-08 | sí |
| cajas-radial | <r>/R delta=1.2 R=400 (3 cifras) | 0.38592437562 | 0.385920224253 | disparo solve_ivp DOP853 (rtol 1e-12) | -4.15e-06 | 5.0e-04 | sí |
| cajas-radial | F_1/2 delta=1.2 R=400 (3 cifras) | 0.695910954476 | 0.695916427804 | disparo solve_ivp DOP853 (rtol 1e-12) (FEDVR si kappa R>10) | +5.47e-06 | 5.0e-04 | sí |
| cajas-radial | E0 delta=1.2 R=800 (tol = error declarado del radial) | 5.6685608011e-06 | 5.6683902474e-06 | disparo solve_ivp DOP853 (rtol 1e-12) u(R)=0 | -1.71e-10 | 9.3e-09 | sí |
| cajas-radial | <r>/R delta=1.2 R=800 (3 cifras) | 0.425574265985 | 0.425567826201 | disparo solve_ivp DOP853 (rtol 1e-12) | -6.44e-06 | 5.0e-04 | sí |
| cajas-radial | F_1/2 delta=1.2 R=800 (3 cifras) | 0.633375805578 | 0.633385461127 | disparo solve_ivp DOP853 (rtol 1e-12) (FEDVR si kappa R>10) | +9.66e-06 | 5.0e-04 | sí |
| cajas-radial | errata 9.6: E0(1.18, R=400) a 3 cifras (el valor propio redondea a -3.07e-5: se confirma la errata de la Fase 1) | -3.0800000000e-05 | -3.0700000000e-05 | disparo solve_ivp DOP853 (rtol 1e-12) | +1.00e-07 | 0.0e+00 | no |
| pares | U(0.01,0.01) eps=0.2 | -1.13235444553 | -1.1323544463 | suma espectral FEDVR / K_D exacto | -7.69e-10 | 1.0e-06 | sí |
| pares | U(0.02,0.02) eps=0.2 | -1.11283907816 | -1.11283907859 | suma espectral FEDVR / K_D exacto | -4.35e-10 | 1.0e-06 | sí |
| pares | U(9.0,9.0) eps=0.2 | -0.0222314317465 | -0.0222314317447 | suma espectral FEDVR / K_D exacto | +1.83e-12 | 1.0e-06 | sí |
| pares | U(0.01,0.01) eps=0.1 | -0.788269118394 | -0.788269121278 | suma espectral FEDVR / K_D exacto | -2.88e-09 | 1.0e-06 | sí |
| pares | U(0.02,0.02) eps=0.1 | -0.76897538587 | -0.7689753873 | suma espectral FEDVR / K_D exacto | -1.43e-09 | 1.0e-06 | sí |
| pares | U(9.0,9.0) eps=0.1 | -0.0111134054072 | -0.0111134054062 | suma espectral FEDVR / K_D exacto | +9.77e-13 | 1.0e-06 | sí |
| pares | U(0.01,0.01) eps=0.05 | -0.54844636455 | -0.548446374753 | suma espectral FEDVR / K_D exacto | -1.02e-08 | 1.0e-06 | sí |
| pares | U(0.02,0.02) eps=0.05 | -0.529459949926 | -0.529459954036 | suma espectral FEDVR / K_D exacto | -4.11e-09 | 1.0e-06 | sí |
| pares | U(9.0,9.0) eps=0.05 | -0.00555612812187 | -0.00555612812136 | suma espectral FEDVR / K_D exacto | +5.17e-13 | 1.0e-06 | sí |
| transferencia | Coulomb h=0.02 E+0.5 eps=0.2 (tabla con Richardson del proyecto deja ~1e-9/eps) | 5.4383004544e-08 | 5.3328841565e-08 | Nystrom propio con rho_C espectral FEDVR (Rb=46) | -1.05e-09 | 1.0e-08 | sí |
| transferencia | Coulomb, E de Trotter h->0, eps=0.2 | -0.5 | -0.5 | Trotter espectral FEDVR (h->0 exacto) | -1.52e-13 | 1.0e-09 | sí |
| transferencia | delta=0.2 h=0.02 E eps=0.2 | -0.326808910621 | -0.326808911608 | Nystrom propio con rho_C espectral FEDVR (Rb=46) | -9.87e-10 | 1.0e-08 | sí |
| transferencia | delta=0.2 h=0.04 E eps=0.2 | -0.326808152716 | -0.326808153703 | Nystrom propio con rho_C espectral FEDVR (Rb=46) | -9.88e-10 | 1.0e-08 | sí |
| transferencia | estabilidad Nystrom delta=0 eps=0.2 | 7.9957118027e-07 | 7.9957136201e-07 | Nystrom propio con rho_C espectral FEDVR (Rb=46) | +1.82e-13 | 2.0e-08 | sí |
| transferencia | orden Nystrom delta=0 eps=0.2 | 3.99941126807 | 3.99941939767 | Nystrom propio con rho_C espectral FEDVR (Rb=46) | +8.13e-06 | 1.0e-02 | sí |
| transferencia | delta=0.2 E Richardson h^4 eps=0.2 (tol del plan 1e-6; dif. real ~1e-9/eps (residuo de la tabla)) | -0.326808961148 | -0.326808962158 | Trotter espectral FEDVR (h->0 exacto) | -1.01e-09 | 1.0e-06 | sí |
| transferencia | delta=1.0 E Richardson h^4 eps=0.2 (dif. sistematica = aprox. de extremos r>10 (parte F)) | -0.0103195695374 | -0.0103194260767 | Trotter espectral FEDVR (h->0 exacto) | +1.43e-07 | 1.0e-06 | sí |
| transferencia | Coulomb h=0.02 E+0.5 eps=0.1 (tabla con Richardson del proyecto deja ~1e-9/eps) | 1.0877749529e-07 | 1.0665535116e-07 | Nystrom propio con rho_C espectral FEDVR (Rb=46) | -2.12e-09 | 1.0e-08 | sí |
| transferencia | Coulomb, E de Trotter h->0, eps=0.1 | -0.5 | -0.5 | Trotter espectral FEDVR (h->0 exacto) | -1.53e-13 | 1.0e-09 | sí |
| transferencia | delta=0.2 h=0.02 E eps=0.1 | -0.326808521471 | -0.326808523486 | Nystrom propio con rho_C espectral FEDVR (Rb=46) | -2.02e-09 | 1.0e-08 | sí |
| transferencia | delta=0.2 h=0.04 E eps=0.1 | -0.326807003108 | -0.326807005121 | Nystrom propio con rho_C espectral FEDVR (Rb=46) | -2.01e-09 | 1.0e-08 | sí |
| transferencia | estabilidad Nystrom delta=0 eps=0.1 | 1.5991335797e-06 | 1.5991357062e-06 | Nystrom propio con rho_C espectral FEDVR (Rb=46) | +2.13e-12 | 2.0e-08 | sí |
| transferencia | orden Nystrom delta=0 eps=0.1 | 3.99939709919 | 3.99941345807 | Nystrom propio con rho_C espectral FEDVR (Rb=46) | +1.64e-05 | 1.0e-02 | sí |
| transferencia | delta=0.2 E Richardson h^4 eps=0.1 (tol del plan 1e-6; dif. real ~1e-9/eps (residuo de la tabla)) | -0.326808622695 | -0.326808624755 | Trotter espectral FEDVR (h->0 exacto) | -2.06e-09 | 1.0e-06 | sí |
| transferencia | delta=1.0 E Richardson h^4 eps=0.1 (dif. sistematica = aprox. de extremos r>10 (parte F)) | -0.0102943327957 | -0.0102942843646 | Trotter espectral FEDVR (h->0 exacto) | +4.84e-08 | 1.0e-06 | sí |
| transferencia | Coulomb h=0.02 E+0.5 eps=0.05 (tabla con Richardson del proyecto deja ~1e-9/eps) | 2.1761763036e-07 | 2.1330825711e-07 | Nystrom propio con rho_C espectral FEDVR (Rb=46) | -4.31e-09 | 1.0e-08 | sí |
| transferencia | Coulomb, E de Trotter h->0, eps=0.05 | -0.5 | -0.5 | Trotter espectral FEDVR (h->0 exacto) | -1.56e-13 | 1.0e-09 | sí |
| transferencia | delta=0.2 h=0.02 E eps=0.05 | -0.326808333002 | -0.326808337101 | Nystrom propio con rho_C espectral FEDVR (Rb=46) | -4.10e-09 | 1.0e-08 | sí |
| transferencia | delta=0.2 h=0.04 E eps=0.05 | -0.326805294034 | -0.326805298126 | Nystrom propio con rho_C espectral FEDVR (Rb=46) | -4.09e-09 | 1.0e-08 | sí |
| transferencia | estabilidad Nystrom delta=0 eps=0.05 | 3.1982286196e-06 | 3.1982358477e-06 | Nystrom propio con rho_C espectral FEDVR (Rb=46) | +7.23e-12 | 2.0e-08 | sí |
| transferencia | orden Nystrom delta=0 eps=0.05 | 3.9994271213 | 3.99939845051 | Nystrom propio con rho_C espectral FEDVR (Rb=46) | -2.87e-05 | 1.0e-02 | sí |
| transferencia | delta=0.2 E Richardson h^4 eps=0.05 (tol del plan 1e-6; dif. real ~1e-9/eps (residuo de la tabla)) | -0.3268085356 | -0.326808539789 | Trotter espectral FEDVR (h->0 exacto) | -4.19e-09 | 1.0e-06 | sí |
| transferencia | delta=1.0 E Richardson h^4 eps=0.05 (dif. sistematica = aprox. de extremos r>10 (parte F)) | -0.0102879391114 | -0.010287923312 | Trotter espectral FEDVR (h->0 exacto) | +1.58e-08 | 1.0e-06 | sí |
| transferencia | delta=0.2 orden Trotter h=0.02 sin Richardson | 1.04600176052 | 1.05822269348 | Nystrom propio con rho_C espectral FEDVR (Rb=46) | +1.22e-02 | 5.0e-02 | sí |
| transferencia | delta=0.2 orden Trotter (Richardson h) | 1.95829283593 | 1.98951054981 | Trotter espectral FEDVR (h->0 exacto) | +3.12e-02 | 5.0e-02 | sí |
| transferencia | delta=0.2 E extrapolado eps->0 | -0.326808506568 | -0.326808511191 | Trotter espectral FEDVR (h->0 exacto) | -4.62e-09 | 1.0e-06 | sí |
| transferencia | delta=0.2 E extrapolado frente al radial exacto | -0.326808511369 | -0.326808511191 | Trotter espectral FEDVR (h->0 exacto) vs disparo | +1.78e-10 | 1.0e-09 | sí |
| transferencia | delta=1.0 orden Trotter (Richardson h) | 1.98080624886 | 1.98274547423 | Trotter espectral FEDVR (h->0 exacto) | +1.94e-03 | 5.0e-02 | sí |
| transferencia | delta=1.0 E extrapolado eps->0 | -0.0102858078833 | -0.0102857688088 | Trotter espectral FEDVR (h->0 exacto) | +3.91e-08 | 1.0e-06 | sí |
| proyeccion | E_mixto(tau=1) eps=0.1 (11, h=0.02) | -0.326581358845 | -0.326581357278 | Trotter espectral FEDVR (h->0 exacto) | +1.57e-09 | 1.0e-08 | sí |
| proyeccion | E_mixto(tau=5) eps=0.1 (11, h=0.02) | -0.326762635449 | -0.326762632752 | Trotter espectral FEDVR (h->0 exacto) | +2.70e-09 | 1.0e-08 | sí |
| proyeccion | E_mixto(tau=10) eps=0.1 (11, h=0.02) | -0.326800988014 | -0.326800985109 | Trotter espectral FEDVR (h->0 exacto) | +2.91e-09 | 1.0e-08 | sí |
| proyeccion | E_mixto(tau=20) eps=0.1 (11, h=0.02) | -0.326808365329 | -0.326808362382 | Trotter espectral FEDVR (h->0 exacto) | +2.95e-09 | 1.0e-08 | sí |
| proyeccion | E_mixto(tau=30) eps=0.1 (11, h=0.02) | -0.326808616858 | -0.326808613909 | Trotter espectral FEDVR (h->0 exacto) | +2.95e-09 | 1.0e-08 | sí |
| proyeccion | E_mixto(20)-limite | 2.6153362054e-07 | 2.6153113181e-07 | Trotter espectral FEDVR (h->0 exacto) | -2.49e-12 | 1.0e-08 | sí |
| proyeccion | variacion E_mixto tau 20->30 | 2.5152856653e-07 | 2.5152685224e-07 | Trotter espectral FEDVR (h->0 exacto) | -1.71e-12 | 1.0e-09 | sí |
| proyeccion | limite del mixto - E0(T) (proyecto: 1.05e-7 es error Nystrom de E0(T) con h=0.02; en el continuo es <1e-9) | -1.0539256401e-07 | 8.4182416593e-10 | Trotter espectral FEDVR (h->0 exacto) | +1.06e-07 | 1.0e-06 | sí |
| pigs-det | E_det tau=2 (Richardson h) | -0.326660213794 | -0.326660213759 | Trotter espectral FEDVR (h->0 exacto) | +3.51e-11 | 1.0e-08 | sí |
| pigs-det | <r>_det tau=2 | 1.51764674982 | 1.51764674685 | Trotter espectral FEDVR (h->0 exacto) | -2.97e-09 | 1.0e-06 | sí |
| pigs-det | <r^2>_det tau=2 | 3.07272536218 | 3.07272535243 | Trotter espectral FEDVR (h->0 exacto) | -9.75e-09 | 1.0e-06 | sí |
| pigs-det | sigma E PIGS tau=2 | -0.744397224093 | -0.744397714748 | PIGS del proyecto frente a E_det propio | -4.91e-07 | 5.0e-02 | sí |
| pigs-det | E_det tau=5 (Richardson h) | -0.3267626328 | -0.326762632752 | Trotter espectral FEDVR (h->0 exacto) | +4.79e-11 | 1.0e-08 | sí |
| pigs-det | <r>_det tau=5 | 1.5321364738 | 1.53213646888 | Trotter espectral FEDVR (h->0 exacto) | -4.92e-09 | 1.0e-06 | sí |
| pigs-det | <r^2>_det tau=5 | 3.13810746231 | 3.13810744416 | Trotter espectral FEDVR (h->0 exacto) | -1.82e-08 | 1.0e-06 | sí |
| pigs-det | sigma E PIGS tau=5 | -3.18620229466 | -3.18620308818 | PIGS del proyecto frente a E_det propio | -7.94e-07 | 5.0e-02 | sí |
| pigs-det | E_det tau=10 (Richardson h) | -0.326800985162 | -0.326800985109 | Trotter espectral FEDVR (h->0 exacto) | +5.32e-11 | 1.0e-08 | sí |
| pigs-det | <r>_det tau=10 | 1.54283086704 | 1.54283086072 | Trotter espectral FEDVR (h->0 exacto) | -6.33e-09 | 1.0e-06 | sí |
| pigs-det | <r^2>_det tau=10 | 3.18995521374 | 3.18995518827 | Trotter espectral FEDVR (h->0 exacto) | -2.55e-08 | 1.0e-06 | sí |
| pigs-det | sigma E PIGS tau=10 | 0.188608185228 | 0.188607356071 | PIGS del proyecto frente a E_det propio | -8.29e-07 | 5.0e-02 | sí |
| pigs-det | E_det tau=20 (Richardson h) | -0.326808362437 | -0.326808362382 | Trotter espectral FEDVR (h->0 exacto) | +5.50e-11 | 1.0e-08 | sí |
| pigs-det | <r>_det tau=20 | 1.54855143761 | 1.54855143035 | Trotter espectral FEDVR (h->0 exacto) | -7.26e-09 | 1.0e-06 | sí |
| pigs-det | <r^2>_det tau=20 | 3.21951665474 | 3.21951662345 | Trotter espectral FEDVR (h->0 exacto) | -3.13e-08 | 1.0e-06 | sí |
| pigs-det | sigma E PIGS tau=20 | 1.21596359729 | 1.21596279021 | PIGS del proyecto frente a E_det propio | -8.07e-07 | 5.0e-02 | sí |
| pigs-det | replica tau=5 sigma E (16 semillas) | 0.0334579383029 | 0.0334570397388 | replica frente a E_det propio | -8.99e-07 | 5.0e-02 | sí |
| pigs-series | delta=0.2 PIGS E media | -0.326725455091 | -0.326725455083 | media propia de las series .npz | +7.81e-12 | 1.0e-06 rel. | sí |
| pigs-series | delta=0.2 PIGS E error | 6.8182425002e-05 | 6.8182428673e-05 | max(binning FP, entre cadenas) propio | +3.67e-12 | 1.0e-01 rel. | sí |
| pigs-series | Coulomb PIGS E media | -0.5 | -0.5 | media propia | +0.00e+00 | 1.0e-06 | sí |
| pigs-series | delta=0.2 tau_int E | 5.26690340043 | 5.26771965021 | ventana automatica propia (c=6) | +8.16e-04 | 5.0e-02 rel. | sí |
| pigs-series | delta=0.2 PIGS <r> media | 1.55373561926 | 1.55373561919 | media propia de las series .npz | -6.90e-11 | 1.0e-06 rel. | sí |
| pigs-series | delta=0.2 PIGS <r> error | 0.00711198911925 | 0.00703645668182 | max(binning FP, entre cadenas) propio | -7.55e-05 | 1.0e-01 rel. | sí |
| pigs-series | Coulomb PIGS <r> media | 1.49276591347 | 1.49276591324 | media propia | -2.28e-10 | 1.0e-06 | sí |
| pigs-series | Coulomb PIGS <r> error | 0.0162577440115 | 0.0172333846754 | binning FP propio | +9.76e-04 | 1.0e-01 rel. | sí |
| pigs-series | delta=0.2 tau_int <r> | 11.6689693902 | 11.6730178103 | ventana automatica propia (c=6) | +4.05e-03 | 5.0e-02 rel. | sí |
| pigs-series | delta=0.2 PIGS <r^2> media | 3.24260471556 | 3.24260471579 | media propia de las series .npz | +2.31e-10 | 1.0e-06 rel. | sí |
| pigs-series | delta=0.2 PIGS <r^2> error | 0.038941052165 | 0.0389410521363 | max(binning FP, entre cadenas) propio | -2.87e-11 | 1.0e-01 rel. | sí |
| pigs-series | Coulomb PIGS <r^2> media | 2.97502698811 | 2.97502698736 | media propia | -7.51e-10 | 1.0e-06 | sí |
| pigs-series | Coulomb PIGS <r^2> error | 0.078728762186 | 0.0799860367823 | binning FP propio | +1.26e-03 | 1.0e-01 rel. | sí |
| pigs-series | delta=0.2 tau_int <r^2> | 14.1523190962 | 14.1589034935 | ventana automatica propia (c=6) | +6.58e-03 | 5.0e-02 rel. | sí |
| pigs-series | Coulomb var(E_L) | 0 | 0 | series | +0.00e+00 | 0.0e+00 | sí |
| pigs-series | delta=0.2 sigma E frente al radial | 1.21805676874 | 1.21814795888 | series + disparo | +9.12e-05 | 5.0e-02 | sí |
| pigs-series | delta=0.2 sigma <r> frente al radial | 0.564359862939 | 0.570417206749 | series + disparo | +6.06e-03 | 5.0e-02 | sí |
| pigs-series | delta=0.2 sigma <r^2> frente al radial | 0.427961558365 | 0.427961574557 | series + disparo | +1.62e-08 | 5.0e-02 | sí |
| hulthen | Hulthen 0.2 E(eps=0.2)-E_ex (residuo de la tabla ~1e-9/eps) | -1.7090765358e-08 | -1.8155525361e-08 | Trotter espectral FEDVR (h->0 exacto) | -1.06e-09 | 1.0e-06 | sí |
| hulthen | Hulthen 0.2 E(eps=0.1)-E_ex (residuo de la tabla ~1e-9/eps) | -2.4129642173e-09 | -4.5593403497e-09 | Trotter espectral FEDVR (h->0 exacto) | -2.15e-09 | 1.0e-06 | sí |
| hulthen | Hulthen 0.2 E(eps=0.05)-E_ex (residuo de la tabla ~1e-9/eps) | 3.2169352737e-09 | -1.1416951828e-09 | Trotter espectral FEDVR (h->0 exacto) | -4.36e-09 | 1.0e-06 | sí |
| hulthen | Hulthen 0.2 E(eps=0.025)-E_ex (residuo de la tabla ~1e-9/eps) | 8.5977597819e-09 | -2.8535956931e-10 | Trotter espectral FEDVR (h->0 exacto) | -8.88e-09 | 1.0e-06 | sí |
| hulthen | Hulthen 0.2 orden Trotter (el proyecto lo declara informativo; el orden verdadero es 2) | 1.38245478481 | 1.99212737499 | Trotter espectral FEDVR (h->0 exacto) | +6.10e-01 | 5.0e-02 | no |
| hulthen | Hulthen 0.2 E extrapolado - E_ex | 5.0935684559e-09 | -8.2694961989e-13 | Trotter espectral FEDVR (h->0 exacto) | -5.09e-09 | 1.0e-06 | sí |
| hulthen | Hulthen 0.2 <r> extrapolado - exacto | 1.6907136358e-08 | 7.4726091981e-10 | Trotter espectral FEDVR (h->0 exacto) | -1.62e-08 | 1.0e-04 | sí |
| hulthen | Hulthen 1.0 E(eps=0.2)-E_ex (residuo de la tabla ~1e-9/eps) | -8.3138386476e-06 | -8.3135378217e-06 | Trotter espectral FEDVR (h->0 exacto) | +3.01e-10 | 1.0e-06 | sí |
| hulthen | Hulthen 1.0 E(eps=0.1)-E_ex (residuo de la tabla ~1e-9/eps) | -2.0869565535e-06 | -2.0882404310e-06 | Trotter espectral FEDVR (h->0 exacto) | -1.28e-09 | 1.0e-06 | sí |
| hulthen | Hulthen 1.0 E(eps=0.05)-E_ex (residuo de la tabla ~1e-9/eps) | -5.1988958916e-07 | -5.2309421381e-07 | Trotter espectral FEDVR (h->0 exacto) | -3.20e-09 | 1.0e-06 | sí |
| hulthen | Hulthen 1.0 E(eps=0.025)-E_ex (residuo de la tabla ~1e-9/eps) | -1.2415409026e-07 | -1.3087803624e-07 | Trotter espectral FEDVR (h->0 exacto) | -6.72e-09 | 1.0e-06 | sí |
| hulthen | Hulthen 1.0 orden Trotter | 1.9904431313 | 1.99184531712 | Trotter espectral FEDVR (h->0 exacto) | +1.40e-03 | 5.0e-02 | sí |
| hulthen | Hulthen 1.0 E extrapolado - E_ex | 2.4660656156e-09 | -5.9464189128e-10 | Trotter espectral FEDVR (h->0 exacto) | -3.06e-09 | 1.0e-06 | sí |
| hulthen | Hulthen 1.0 <r> extrapolado - exacto | 5.5362269880e-08 | 1.0146582019e-08 | Trotter espectral FEDVR (h->0 exacto) | -4.52e-08 | 1.0e-04 | sí |
| hulthen | Hulthen 1.5 E(eps=0.2)-E_ex (tol. del plan; en 1.5 queda una dif. sistematica ~eps^1.5 (aprox. de extremos, parte F)) | -2.4234550854e-05 | -2.4197358664e-05 | Trotter espectral FEDVR (h->0 exacto) | +3.72e-08 | 1.0e-06 | sí |
| hulthen | Hulthen 1.5 E(eps=0.1)-E_ex (tol. del plan; en 1.5 queda una dif. sistematica ~eps^1.5 (aprox. de extremos, parte F)) | -6.0899209381e-06 | -6.0783333366e-06 | Trotter espectral FEDVR (h->0 exacto) | +1.16e-08 | 1.0e-06 | sí |
| hulthen | Hulthen 1.5 E(eps=0.05)-E_ex (tol. del plan; en 1.5 queda una dif. sistematica ~eps^1.5 (aprox. de extremos, parte F)) | -1.5249357831e-06 | -1.5226355810e-06 | Trotter espectral FEDVR (h->0 exacto) | +2.30e-09 | 1.0e-06 | sí |
| hulthen | Hulthen 1.5 E(eps=0.025)-E_ex (tol. del plan; en 1.5 queda una dif. sistematica ~eps^1.5 (aprox. de extremos, parte F)) | -3.7844324865e-07 | -3.8096885246e-07 | Trotter espectral FEDVR (h->0 exacto) | -2.53e-09 | 1.0e-06 | sí |
| hulthen | Hulthen 1.5 orden Trotter | 1.99086055762 | 1.99176141014 | Trotter espectral FEDVR (h->0 exacto) | +9.01e-04 | 5.0e-02 | sí |
| hulthen | Hulthen 1.5 E extrapolado - E_ex | -3.2740647277e-09 | -1.7637581326e-09 | Trotter espectral FEDVR (h->0 exacto) | +1.51e-09 | 1.0e-06 | sí |
| hulthen | Hulthen 1.5 <r> extrapolado - exacto | 4.3027989660e-07 | -4.6468711545e-08 | Trotter espectral FEDVR (h->0 exacto) | -4.77e-07 | 1.0e-04 | sí |
| pozo | pozo 2.0 E h->0 eps=0.2 (borde medio) | -0.224209075989 | -0.224220619086 | Trotter espectral FEDVR (h->0 exacto) (salto en borde de elemento) | -1.15e-05 | 1.0e-05 | no |
| pozo | pozo 2.0 E h->0 eps=0.1 (borde medio) | -0.210849215217 | -0.210871101878 | Trotter espectral FEDVR (h->0 exacto) (salto en borde de elemento) | -2.19e-05 | 1.0e-05 | no |
| pozo | pozo 2.0 E h->0 eps=0.05 (borde medio) | -0.206117527278 | -0.206141766621 | Trotter espectral FEDVR (h->0 exacto) (salto en borde de elemento) | -2.42e-05 | 1.0e-05 | no |
| pozo | pozo 2.0 E h->0 eps=0.025 (borde medio) | -0.204447252984 | -0.204467466431 | Trotter espectral FEDVR (h->0 exacto) (salto en borde de elemento) | -2.02e-05 | 1.0e-05 | no |
| pozo | pozo 2.0 E h->0 eps=0.0125 (borde medio) | -0.203861263611 | -0.203874991632 | Trotter espectral FEDVR (h->0 exacto) (salto en borde de elemento) | -1.37e-05 | 1.0e-05 | no |
| pozo | pozo 2.0 orden Trotter local 1 | 1.49747813879 | 1.49707824559 | Trotter espectral FEDVR (h->0 exacto) | -4.00e-04 | 5.0e-02 | sí |
| pozo | pozo 2.0 orden Trotter local 2 | 1.50226988646 | 1.49807920059 | Trotter espectral FEDVR (h->0 exacto) | -4.19e-03 | 5.0e-02 | sí |
| pozo | pozo 2.0 orden Trotter local 3 | 1.51113863519 | 1.49873252118 | Trotter espectral FEDVR (h->0 exacto) | -1.24e-02 | 5.0e-02 | sí |
| pozo | pozo 2.0 E extrapolado (orden medido) - exacta | 6.1694588695e-06 | 2.2619906553e-07 | Trotter espectral FEDVR (h->0 exacto) | -5.94e-06 | 1.0e-05 | sí |
| pozo | pozo 2.0 ajuste 5 puntos eps^1.5 - exacta | 1.4746585197e-05 | -5.7663697621e-06 | Trotter espectral FEDVR (h->0 exacto) | -2.05e-05 | 1.0e-05 | no |
| pozo | pozo 2.0 E h->0 eps=0.2 borde estricto (el proyecto lo declara no convergido) | -0.224288960757 | -0.224220619086 | Trotter espectral FEDVR (h->0 exacto) (el limite h->0 no depende del borde) | +6.83e-05 | 1.0e-05 | no |
| pozo | pozo 2.0 <r> extrapolado - exacto | 7.0385661015e-06 | -7.8863151209e-07 | Trotter espectral FEDVR (h->0 exacto) | -7.83e-06 | 1.0e-03 | sí |
| pozo | pozo 1.3 E h->0 eps=0.2 (borde medio) | -0.00388879100832 | -0.00388353766844 | Trotter espectral FEDVR (h->0 exacto) (salto en borde de elemento) | +5.25e-06 | 1.0e-05 | sí |
| pozo | pozo 1.3 E h->0 eps=0.1 (borde medio) | -0.00268810262526 | -0.00268542189692 | Trotter espectral FEDVR (h->0 exacto) (salto en borde de elemento) | +2.68e-06 | 1.0e-05 | sí |
| pozo | pozo 1.3 E h->0 eps=0.05 (borde medio) | -0.00231099604958 | -0.00230951183835 | Trotter espectral FEDVR (h->0 exacto) (salto en borde de elemento) | +1.48e-06 | 1.0e-05 | sí |
| pozo | pozo 1.3 E h->0 eps=0.025 (borde medio) | -0.00218347021292 | -0.00218270743182 | Trotter espectral FEDVR (h->0 exacto) (salto en borde de elemento) | +7.63e-07 | 1.0e-05 | sí |
| pozo | pozo 1.3 E h->0 eps=0.0125 (borde medio) | -0.00213890406399 | -0.00213863694501 | Trotter espectral FEDVR (h->0 exacto) (salto en borde de elemento) | +2.67e-07 | 1.0e-05 | sí |
| pozo | pozo 1.3 orden Trotter local 1 | 1.67081756187 | 1.67230789507 | Trotter espectral FEDVR (h->0 exacto) | +1.49e-03 | 5.0e-02 | sí |
| pozo | pozo 1.3 orden Trotter local 2 | 1.56418274141 | 1.56778263856 | Trotter espectral FEDVR (h->0 exacto) | +3.60e-03 | 5.0e-02 | sí |
| pozo | pozo 1.3 orden Trotter local 3 | 1.51676936103 | 1.52472014293 | Trotter espectral FEDVR (h->0 exacto) | +7.95e-03 | 5.0e-02 | sí |
| pozo | pozo 1.3 E extrapolado (orden medido) - exacta | -2.6387124721e-07 | -4.6244641876e-07 | Trotter espectral FEDVR (h->0 exacto) | -1.99e-07 | 1.0e-05 | sí |
| pozo | pozo 1.3 ajuste 5 puntos eps^1.5 - exacta | 2.1130181765e-05 | 2.1744693134e-05 | Trotter espectral FEDVR (h->0 exacto) | +6.15e-07 | 1.0e-05 | sí |
| pozo | pozo 1.3 E h->0 eps=0.2 borde estricto (el proyecto lo declara no convergido) | -0.00458952970734 | -0.00388353766844 | Trotter espectral FEDVR (h->0 exacto) (el limite h->0 no depende del borde) | +7.06e-04 | 1.0e-05 | no |
| pozo | pozo 1.3 <r> extrapolado - exacto | 0.00258952976309 | 0.00205983914027 | Trotter espectral FEDVR (h->0 exacto) | -5.30e-04 | 5.0e-03 | sí |
| cajas-transf | E0 transf. delta=1.15 R=50 (E_proy - radial exacto = -9.66e-07; mio - radial = -2.86e-09) | -3.3178892714e-04 | -3.3082550782e-04 | Trotter espectral FEDVR (h->0 exacto), pared Dirichlet verdadera | +9.63e-07 | 5.1e-07 | no |
| cajas-transf | orden Trotter delta=1.15 R=50 | 1.83177536527 | 1.98569841069 | Trotter espectral FEDVR (h->0 exacto) | +1.54e-01 | 1.0e-01 | no |
| cajas-transf | E0 transf. delta=1.15 R=100 (E_proy - radial exacto = -4.39e-08; mio - radial = -2.37e-09) | -4.5122247663e-04 | -4.5118099510e-04 | Trotter espectral FEDVR (h->0 exacto), pared Dirichlet verdadera | +4.15e-08 | 6.9e-08 | sí |
| cajas-transf | orden Trotter delta=1.15 R=100 | 1.9740348895 | 1.98860277289 | Trotter espectral FEDVR (h->0 exacto) | +1.46e-02 | 1.0e-01 | sí |
| cajas-transf | E0 transf. delta=1.15 R=200 (E_proy - radial exacto = -1.36e-08; mio - radial = -2.32e-09) | -4.5589167828e-04 | -4.5588039884e-04 | Trotter espectral FEDVR (h->0 exacto), pared Dirichlet verdadera | +1.13e-08 | 5.3e-08 | sí |
| cajas-transf | orden Trotter delta=1.15 R=200 | 1.98104835686 | 1.98944860594 | Trotter espectral FEDVR (h->0 exacto) | +8.40e-03 | 1.0e-01 | sí |
| cajas-transf | E0 transf. delta=1.15 R=400 (E_proy - radial exacto = -1.35e-08; mio - radial = -2.32e-09) | -4.5590254984e-04 | -4.5589134145e-04 | Trotter espectral FEDVR (h->0 exacto), pared Dirichlet verdadera | +1.12e-08 | 5.3e-08 | sí |
| cajas-transf | orden Trotter delta=1.15 R=400 | 1.98107414156 | 1.98945942747 | Trotter espectral FEDVR (h->0 exacto) | +8.39e-03 | 1.0e-01 | sí |
| cajas-transf | E0 transf. delta=1.15 R=800 (E_proy - radial exacto = -1.35e-08; mio - radial = -2.32e-09) | -4.5590254990e-04 | -4.5589134171e-04 | Trotter espectral FEDVR (h->0 exacto), pared Dirichlet verdadera | +1.12e-08 | 5.3e-08 | sí |
| cajas-transf | orden Trotter delta=1.15 R=800 | 1.98107413944 | 1.98945948642 | Trotter espectral FEDVR (h->0 exacto) | +8.39e-03 | 1.0e-01 | sí |
| cajas-transf | E0 transf. delta=1.18 R=50 (E_proy - radial exacto = -1.82e-06; mio - radial = -2.05e-09) | 3.3618774970e-04 | 3.3800875185e-04 | Trotter espectral FEDVR (h->0 exacto), pared Dirichlet verdadera | +1.82e-06 | 8.8e-07 | no |
| cajas-transf | orden Trotter delta=1.18 R=50 | 1.64491189744 | 1.98636957229 | Trotter espectral FEDVR (h->0 exacto) | +3.41e-01 | 1.0e-01 | no |
| cajas-transf | E0 transf. delta=1.18 R=100 (E_proy - radial exacto = -1.89e-07; mio - radial = -1.18e-09) | 3.1941778676e-05 | 3.2129190871e-05 | Trotter espectral FEDVR (h->0 exacto), pared Dirichlet verdadera | +1.87e-07 | 1.1e-07 | no |
| cajas-transf | orden Trotter delta=1.18 R=100 | 1.91035504726 | 1.99229478825 | Trotter espectral FEDVR (h->0 exacto) | +8.19e-02 | 1.0e-01 | sí |
| cajas-transf | E0 transf. delta=1.18 R=200 (E_proy - radial exacto = -1.86e-08; mio - radial = -7.94e-10) | -2.4081286570e-05 | -2.4063437087e-05 | Trotter espectral FEDVR (h->0 exacto), pared Dirichlet verdadera | +1.78e-08 | 1.6e-08 | no |
| cajas-transf | orden Trotter delta=1.18 R=200 | 1.98347855879 | 2.00280775449 | Trotter espectral FEDVR (h->0 exacto) | +1.93e-02 | 1.0e-01 | sí |
| cajas-transf | E0 transf. delta=1.18 R=400 (E_proy - radial exacto = -4.28e-09; mio - radial = -6.61e-10) | -3.0754145800e-05 | -3.0750523072e-05 | Trotter espectral FEDVR (h->0 exacto), pared Dirichlet verdadera | +3.62e-09 | 5.3e-09 | sí |
| cajas-transf | orden Trotter delta=1.18 R=400 | 2.0032314975 | 2.01435719675 | Trotter espectral FEDVR (h->0 exacto) | +1.11e-02 | 1.0e-01 | sí |
| cajas-transf | E0 transf. delta=1.18 R=800 (E_proy - radial exacto = -3.70e-09; mio - radial = -6.40e-10) | -3.0989182721e-05 | -3.0986124977e-05 | Trotter espectral FEDVR (h->0 exacto), pared Dirichlet verdadera | +3.06e-09 | 7.2e-09 | sí |
| cajas-transf | orden Trotter delta=1.18 R=800 | 2.00633715357 | 2.01711794438 | Trotter espectral FEDVR (h->0 exacto) | +1.08e-02 | 1.0e-01 | sí |
| cajas-transf | E0 transf. delta=1.2 R=50 (E_proy - radial exacto = -2.45e-06; mio - radial = -1.64e-09) | 6.4125035355e-04 | 6.4369950870e-04 | Trotter espectral FEDVR (h->0 exacto), pared Dirichlet verdadera | +2.45e-06 | 1.2e-06 | no |
| cajas-transf | orden Trotter delta=1.2 R=50 | 1.49243978303 | 1.98653611657 | Trotter espectral FEDVR (h->0 exacto) | +4.94e-01 | 1.0e-01 | no |
| cajas-transf | E0 transf. delta=1.2 R=100 (E_proy - radial exacto = -3.39e-07; mio - radial = -7.02e-10) | 1.8652512730e-04 | 1.8686326431e-04 | Trotter espectral FEDVR (h->0 exacto), pared Dirichlet verdadera | +3.38e-07 | 1.7e-07 | no |
| cajas-transf | orden Trotter delta=1.2 R=100 | 1.78059432217 | 1.99263078923 | Trotter espectral FEDVR (h->0 exacto) | +2.12e-01 | 1.0e-01 | no |
| cajas-transf | E0 transf. delta=1.2 R=200 (E_proy - radial exacto = -5.15e-08; mio - radial = -2.66e-10) | 5.7928095049e-05 | 5.7979366129e-05 | Trotter espectral FEDVR (h->0 exacto), pared Dirichlet verdadera | +5.13e-08 | 2.6e-08 | no |
| cajas-transf | orden Trotter delta=1.2 R=200 | 1.90527672937 | 2.00376269428 | Trotter espectral FEDVR (h->0 exacto) | +9.85e-02 | 1.0e-01 | sí |
| cajas-transf | E0 transf. delta=1.2 R=400 (E_proy - radial exacto = -8.41e-09; mio - radial = -8.40e-11) | 1.8430233554e-05 | 1.8438560023e-05 | Trotter espectral FEDVR (h->0 exacto), pared Dirichlet verdadera | +8.33e-09 | 3.4e-09 | no |
| cajas-transf | orden Trotter delta=1.2 R=400 | 1.96250442541 | 2.02132571777 | Trotter espectral FEDVR (h->0 exacto) | +5.88e-02 | 1.0e-01 | sí |
| cajas-transf | E0 transf. delta=1.2 R=800 (E_proy - radial exacto = -1.33e-09; mio - radial = -1.89e-11) | 5.6670610692e-06 | 5.6683713342e-06 | Trotter espectral FEDVR (h->0 exacto), pared Dirichlet verdadera | +1.31e-09 | 1.6e-10 | no |
| cajas-transf | orden Trotter delta=1.2 R=800 | 1.99613527372 | 2.04175051067 | Trotter espectral FEDVR (h->0 exacto) | +4.56e-02 | 1.0e-01 | sí |
| pared | E_hRich(0.2) delta=1.15 R=50 | -3.4800155023e-04 | -3.4782912810e-04 | Trotter espectral FEDVR (h->0 exacto) en R+0.5826 sqrt(eps) | +1.72e-07 | 2.0e-07 | sí |
| pared | E_hRich(0.1) delta=1.15 R=50 | -3.3620676257e-04 | -3.3620160723e-04 | Trotter espectral FEDVR (h->0 exacto) en R+0.5826 sqrt(eps) | +5.16e-09 | 2.0e-07 | sí |
| pared | E_hRich(0.05) delta=1.15 R=50 | -3.3289338600e-04 | -3.3294651675e-04 | Trotter espectral FEDVR (h->0 exacto) en R+0.5826 sqrt(eps) | -5.31e-08 | 2.0e-07 | sí |
| pared | E_hRich(0.2) delta=1.15 R=100 | -4.6373515462e-04 | -4.6351884715e-04 | Trotter espectral FEDVR (h->0 exacto) en R+0.5826 sqrt(eps) | +2.16e-07 | 2.0e-07 | no |
| pared | E_hRich(0.1) delta=1.15 R=100 | -4.5439306058e-04 | -4.5431953156e-04 | Trotter espectral FEDVR (h->0 exacto) en R+0.5826 sqrt(eps) | +7.35e-08 | 2.0e-07 | sí |
| pared | E_hRich(0.05) delta=1.15 R=100 | -4.5201512261e-04 | -4.5199127159e-04 | Trotter espectral FEDVR (h->0 exacto) en R+0.5826 sqrt(eps) | +2.39e-08 | 2.0e-07 | sí |
| pared | E_hRich(0.2) delta=1.18 R=50 | 3.2300114323e-04 | 3.2307504323e-04 | Trotter espectral FEDVR (h->0 exacto) en R+0.5826 sqrt(eps) | +7.39e-08 | 2.0e-07 | sí |
| pared | E_hRich(0.1) delta=1.18 R=50 | 3.3224611416e-04 | 3.3216748602e-04 | Trotter espectral FEDVR (h->0 exacto) en R+0.5826 sqrt(eps) | -7.86e-08 | 2.0e-07 | sí |
| pared | E_hRich(0.05) delta=1.18 R=50 | 3.3520234081e-04 | 3.3507042488e-04 | Trotter espectral FEDVR (h->0 exacto) en R+0.5826 sqrt(eps) | -1.32e-07 | 2.0e-07 | sí |
| pared | E_hRich(0.2) delta=1.18 R=100 | 2.5460406179e-05 | 2.5587846389e-05 | Trotter espectral FEDVR (h->0 exacto) en R+0.5826 sqrt(eps) | +1.27e-07 | 2.0e-07 | sí |
| pared | E_hRich(0.1) delta=1.18 R=100 | 3.0244756443e-05 | 3.0278795159e-05 | Trotter espectral FEDVR (h->0 exacto) en R+0.5826 sqrt(eps) | +3.40e-08 | 2.0e-07 | sí |
| pared | E_hRich(0.05) delta=1.18 R=100 | 3.1517523118e-05 | 3.1519019102e-05 | Trotter espectral FEDVR (h->0 exacto) en R+0.5826 sqrt(eps) | +1.50e-09 | 2.0e-07 | sí |
| pared | E_hRich(0.2) delta=1.2 R=50 | 6.2933343217e-04 | 6.2933314134e-04 | Trotter espectral FEDVR (h->0 exacto) en R+0.5826 sqrt(eps) | -2.91e-10 | 2.0e-07 | sí |
| pared | E_hRich(0.1) delta=1.2 R=50 | 6.3741883305e-04 | 6.3727803892e-04 | Trotter espectral FEDVR (h->0 exacto) en R+0.5826 sqrt(eps) | -1.41e-07 | 2.0e-07 | sí |
| pared | E_hRich(0.05) delta=1.2 R=50 | 6.4029247342e-04 | 6.4010251855e-04 | Trotter espectral FEDVR (h->0 exacto) en R+0.5826 sqrt(eps) | -1.90e-07 | 2.0e-07 | sí |
| pared | E_hRich(0.2) delta=1.2 R=100 | 1.8236704063e-04 | 1.8243727508e-04 | Trotter espectral FEDVR (h->0 exacto) en R+0.5826 sqrt(eps) | +7.02e-08 | 2.0e-07 | sí |
| pared | E_hRich(0.1) delta=1.2 R=100 | 1.8536259767e-04 | 1.8536793096e-04 | Trotter espectral FEDVR (h->0 exacto) en R+0.5826 sqrt(eps) | +5.33e-09 | 2.0e-07 | sí |
| pared | E_hRich(0.05) delta=1.2 R=100 | 1.8623449490e-04 | 1.8621714184e-04 | Trotter espectral FEDVR (h->0 exacto) en R+0.5826 sqrt(eps) | -1.74e-08 | 2.0e-07 | sí |
