# 9. Plan de cómputo para las Fases 2 a 4

**Proyecto 05, Umbral de enlace en el potencial de Yukawa** · Fase 1 · Bloque 09
Script de prueba de costos: `fase1/codigo/09_prueba_costos.py` (numpy, scipy). Todas las cifras de este bloque que no se atribuyen a otra sección salen de ese script, con las semillas que se indican.

**Sobre los tiempos.** Los tiempos de reloj dependen de la carga de la máquina (4 núcleos, compartida) y no son reproducibles a mejor que un factor 2 a 3. Por eso se dan como rangos sobre cuatro ejecuciones: la de la primera versión de este bloque, una de la revisión adversarial (máquina cargada) y dos de la versión actual del script (12 de octubre de 2026, carga media de 1.0 a 2.5 según `os.getloadavg`, que el script imprime al empezar y al terminar). Con la versión actual (que añade la malla triple en B, el barrido en $h$ y $\epsilon$ de D y la parte G) el script tarda de 105 a 107 s de reloj, de ellos 40 a 42 s en las 9 cadenas de Monte Carlo; la revisión adversarial midió 145 s y 66 s con la versión anterior, que en la primera ejecución tardó unos 80 s y 39 s. Los presupuestos de 9.9 se proyectan con el valor **alto** de cada rango.

## 9.0 Objetivo, régimen de validez y criterio de cierre

**Objetivo.** Convertir lo hecho en la Fase 1 (secciones 1 a 8) en un plan ejecutable: qué se calcula, con qué método, con qué parámetros, qué controles deben pasar, cuánto cuesta y quién responde por cada parte, hasta llegar a lo que pide la guía para el proyecto 05: "un intervalo defendible para $\mu_c$ y gráficas de energía y radio característico", con "comparación de varias cajas y cota documentada para el umbral".

**Régimen.** Estado fundamental $1s$ ($\ell=0$) de $V(r)=-e^{-\delta r}/r$ en 3D, unidades $\hbar=m=g=1$, $\delta=\mu\hbar^2/(mg)$ (sección 1). Toda afirmación sobre $\mu_c$ se dará como afirmación sobre $\delta_c$, es decir, a $g$ y $m$ fijos en estas unidades, como pide la guía ("sin reclamar una cifra universal desligada de las unidades").

**Criterio de cierre del plan.** El plan está completo si cada observable tiene (i) un método de tiempo imaginario y una referencia independiente, (ii) parámetros numéricos concretos, (iii) un criterio de aceptación cuantitativo, (iv) al menos dos fuentes de error con su forma de estimarlas, y (v) un costo medido en esta máquina, no supuesto.

## 9.1 Pregunta y observables

**Pregunta.** ¿En qué intervalo de $\delta$ deja de existir el estado fundamental ligado, y cómo crece la extensión del estado al acercarse a ese intervalo?

| Símbolo | Definición | Para qué sirve |
|---|---|---|
| $E_0(\delta)$ | menor autovalor; en tiempo imaginario, límite de proyección del estimador mixto o autovalor de la matriz de transferencia | observable principal; su signo **no** basta para decidir enlace (9.6) |
| $\langle r\rangle$ | $\int r\,u^2dr/\int u^2dr$ | radio característico; diverge como $(\delta_c-\delta)^{-1}$ (secciones 5.5 y 7, L11) |
| $\langle r^2\rangle^{1/2}$ | raíz del segundo momento | segunda medida de extensión; más sensible a la cola |
| $\langle r\rangle/R$ | radio relativo a la caja de radio $R$ | ligado: tiende a 0 al crecer $R$; estado de caja: tiende a $1/2$ |
| $F_{1/2}(R)$ | $\int_0^{R/2}u^2dr\big/\int_0^R u^2dr$, fracción de densidad en la mitad interior de la caja | observable de localización: ligado, $F_{1/2}\to1$; estado de caja (sen$^2$ casi uniforme), $F_{1/2}\to1/2$ |
| $\kappa$ | $\sqrt{-2E_0}$ | ley lineal $\kappa\simeq c(\delta_c-\delta)$, $c\approx0.741$ (sección 7, L10), para extrapolar $\delta_c$ |

En el método de tiempo imaginario, $E_0$ se mide con el estimador mixto en los extremos del camino y $\langle r\rangle$, $\langle r^2\rangle$ con el eslabón central, que muestrea $|e^{-\tau\hat H/2}u_T|^2$ y es por tanto un estimador **puro**, no mixto. Esta distinción la exige la guía en el proyecto vecino 04 ("un promedio mixto de $r$ no se presentará automáticamente como valor puro") y se adopta aquí.

## 9.2 Referencia independiente

El solucionador radial de la sección 5 (diferencias finitas con Richardson, más Numerov y la condición de energía cero). Costo medido (parte A del script):

| $\delta$ | $R$ | $N$ | $E_0$ | $E_1$ | $\langle r\rangle$ | $\langle r^2\rangle^{1/2}$ | $\lvert E_h-E_{h/2}\rvert$ | tiempo |
|---|---|---|---|---|---|---|---|---|
| 0.2 | 60 | 2400 | −0.32680851 | −0.012108 | 1.5497 | 1.7961 | 5.7e−5 | 0.01 s |
| 1.1 | 370 | 14800 | −0.00228724 | +0.000039 | 8.2776 | 11.1202 | 8.8e−6 | 0.05 s |

Un punto $(\delta,R,h)$ sin Richardson cuesta 0.004 a 0.010 s (parte B; el valor depende de $h$ y de la carga). El solucionador radial es, por tanto, gratis frente a todo lo demás y se corre en cada punto donde se corra la integral de camino. $\delta_c=1.1906124211$ por la condición de energía cero (sección 5.3) es la referencia para el umbral, coincidente con Gebremedhin y Weatherford (2023) en las cifras citadas.

**Advertencia sobre independencia.** La tabla de la acción de pares de Coulomb (9.3) se calcula con la misma discretización por diferencias finitas que el solucionador radial, aunque solo para $\delta=0$ y en una caja pequeña. Para que la comparación no sea circular: (a) la tabla no contiene $\delta$; (b) se extrapola en su paso de malla $h_{\rm tab}$ (Richardson); (c) la integral de camino usa después otra discretización (cuadratura de Nyström en $r$ continuo, o Monte Carlo en $r$ continuo). El plan B para esta objeción está en 9.10.

## 9.3 Formulación de tiempo imaginario elegida y trato de la singularidad

Se adopta la recomendación de la sección 8.5 (R1 en el marco radial R5), y el peso se declara explícitamente, como exige la guía para problemas con singularidades.

**Acción por eslabón** (sector $\ell=0$, $u(0)=0$, $\epsilon=\tau/M$):
$$T(r,r';\epsilon)=K_D(r,r';\epsilon)\,e^{-U_C(r,r';\epsilon)}\,e^{-\epsilon[W(r)+W(r')]/2},\qquad W(r)=\frac{1-e^{-\delta r}}{r}\in[0,\delta],$$
con $K_D$ el núcleo libre con imagen (sección 8.3) y $U_C=-\ln(\rho_C/K_D)$ la acción de pares **exacta** del Coulomb puro. La singularidad $-1/r$ entera vive en $\rho_C$, que es un núcleo exacto y normalizable (sección 8.4.4); el resto $W$ es acotado y suave, de modo que la factorización simétrica tiene sesgo $O(\epsilon^2)$ y en $\delta=0$ el método es exacto para todo $\epsilon$.

**Peso.** Real (no hay fases), positivo ($K_D>0$ para $r,r'>0$, exponenciales positivas) y **normalizable** ($U_C$ es finita en $r\to0$: $U_C(0.02,0.02;0.1)=-0.7689$, parte C). La acción primitiva con $1/r$ desnudo queda prohibida por la sección 8.4.2 (no normalizable para todo $\epsilon>0$). El suavizado (R3) solo se usa como control cruzado, con $a_s$ declarado y extrapolado.

**Tabla de $U_C$** (parte C). Espectral en una caja $R_{\rm tab}=14$, tabulada en $r,r'\le10$ y $|r-r'|\le\max(2,7\sqrt\epsilon)$; fuera de $r=10$ se usa $U_C\approx\tfrac\epsilon2[V_C(r)+V_C(r')]$, que en $r=r'=9$ coincide con la tabla en las cinco cifras impresas ($-0.01111$). Se divide por el núcleo libre **de la misma red** para que el error de red se cancele en lo posible.

| $h_{\rm tab}$ | tabla | tiempo (rango de cuatro ejecuciones) | $E_0$ Coulomb de la red |
|---|---|---|---|
| 0.01 | 1000×1000 | 0.57 a 2.03 s | −0.4999875 |
| 0.005 | 2000×2000 | 1.73 a 6.52 s | −0.4999969 |

Diferencia máxima entre ambas tablas en $|r-r'|\le1$: $5.3\times10^{-5}$. Ese es el error de tabulación, y se elimina con Richardson en $h_{\rm tab}$ (ver F en 9.5).

**Dos evaluaciones de la misma integral de camino.**

1. **Determinista (matriz de transferencia en banda, Nyström).** Se discretiza la integral sobre cada coordenada intermedia con la regla del trapecio en una malla $h=0.02$ (control $h=0.04$); $T_{ij}=h\,T(r_i,r_j;\epsilon)$ es una matriz dispersa en banda y su mayor autovalor da $E_0(\epsilon)=-\ln\lambda_0/\epsilon$, que es el límite $\tau\to\infty$ de la proyección. Es la integral de camino discretizada calculada sin muestreo, y es la que escala a cajas grandes.
2. **Estocástica (PIGS, path integral ground state).** Caminos abiertos $r_0,\dots,r_M$ con peso $u_T(r_0)\prod_k T(r_k,r_{k+1})\,u_T(r_M)$, $u_T=r\,e^{-r}$. Esta prueba cumple la cúspide $u'/u\to1/r-1$ (sección 7, L07), así que su energía local $E_L=W(r)-\tfrac12$ es acotada, pero tiene la cola equivocada para $\delta>0$: es una función tentativa no exacta, como pide la guía. Movimientos: rebrote de segmentos de $L=10$ eslabones por puente browniano, rebrote de extremos y un cambio global de escala $r\to\lambda r$ (con jacobiano $\lambda^{M+1}$). $r$ es continuo y $U_C$ se interpola bilinealmente en la tabla.

**Por qué no $Z(\beta)$.** En volumen infinito la traza diverge por el continuo (sección 8.2.6). No se usa el estimador termodinámico; todo se hace por proyección (PIGS) o por el autovalor de la transferencia en una caja declarada.

## 9.4 Parámetros

| Parámetro | Fase 2 | Fase 3 | Fase 4 |
|---|---|---|---|
| Puntos de $\delta$ | 0 (control Coulomb); **0.2** (punto fuertemente ligado de la primera exposición: $E_0=-0.32680851$, $\langle r\rangle=1.5497$, brecha al $2s$: 0.3147) | 0.4, 0.6, 0.8, 1.0, 1.1 (los de la tabla 5.1) | 1.15, 1.17, 1.18, 1.185, 1.19, 1.195, 1.20, 1.22, 1.25 (los que rodean $\delta_c$) y bisección para cerrar el intervalo |
| Caja $R$ (transferencia y radial) | 40 | $R=\max(60,25/\kappa)$ (receta 5.1) y además $R\in\{50,100,200,400,800\}$ para $\delta\ge0.8$ | $R\in\{50,100,200,400,800\}$ en la transferencia; hasta 1600 en el solucionador radial |
| Paso $\epsilon$ | 0.1 (y 0.2, 0.05 en $\delta=0.2$) | $\{0.2,0.1,0.05\}$ en cada $\delta$, extrapolación $\epsilon\to0$ con ley $\epsilon^2$ | igual que en la Fase 3; PIGS con $\epsilon\in\{0.4,0.2\}$ si se usa |
| Longitud $\tau$ (PIGS) | 10 ($\delta=0$), 20 ($\delta=0.2$), $M=100$ y 200 | $\tau\ge\max(20,\,9/\lvert E_0\rvert)$ (sección 7, L15); PIGS solo hasta $\delta=1.0$ | la transferencia da directamente $\tau\to\infty$ |
| Malla $h$ (Nyström) | 0.02; control 0.04 | 0.02 y 0.01 (Richardson en $h$) | 0.02 y 0.01 (Richardson en $h$), 0.04 solo como control |
| Malla $h$ (solucionador radial) | $1/40$ y $1/80$, Richardson | igual | igual; nunca $h=1/20$ sin Richardson cerca del umbral (9.6) |
| Tabla $U_C$ | $h_{\rm tab}=0.01$ y $0.005$, Richardson | igual | igual |
| Cadenas PIGS | 8 cadenas independientes de $5\times10^4$ barridos + 500 de termalización, 20 bloques por cadena | 8 cadenas por punto | solo si queda tiempo (9.10) |
| Semillas | $\delta=0$: 20261012; $\delta=0.2$: 20261013 a 20261020 (las de la prueba); producción: 20262000+$k$ | 20263000+$k$ | 20264000+$k$ |

Para $\delta=1.185$ y $1.19$, la ley $\kappa\simeq0.741(\delta_c-\delta)$ y $\langle r\rangle\simeq1/(2\kappa)$ de la sección 7 dan $\kappa\approx0.0042$ y $0.00045$, y $\langle r\rangle\approx120$ y $1100$ (parte G): en $\delta=1.19$ ni la caja de 800 ni la de 1600 bastan, y el veredicto puede quedar "indeterminado" (9.6), lo que se reportará como tal. $\delta=1.195$ está del lado no ligado ($\delta>\delta_c=1.19061$): ahí no hay $\kappa$, y lo que crece es la longitud de dispersión, $a_{sc}=-307$ (parte G, solución de energía cero; $-143$ en $\delta=1.20$ y $-22$ en $\delta=1.25$). La ley de estado de caja $\pi^2/[2(R-a_{sc})^2]$ solo distingue ese caso de un ligado débil si $R\gg|a_{sc}|$.

## 9.5 Prueba de concepto ejecutada (lo que ya funciona)

**F. Transferencia en banda, $\epsilon=0.1$, $h=0.02$, tablas $h_{\rm tab}=0.01$ y $0.005$ con Richardson.**

| $\delta$ | $R$ | $N$ | $E$ (Richardson) | referencia radial | diferencia | $\langle r\rangle$ | tiempo |
|---|---|---|---|---|---|---|---|
| 0.0 | 40 | 2000 | −0.49999989 | −0.5 | $+1.1\times10^{-7}$ | 1.50000 | 0.1 s |
| 0.2 | 40 | 2000 | −0.32680852 | −0.32680851 | $-1.5\times10^{-8}$ | 1.54974 | 0.1 s |
| 1.0 | 174 | 8700 | −0.01029431 | −0.01028578 | $-8.5\times10^{-6}$ | 4.36537 | 2.2 a 2.3 s |
| 1.1 | 370 | 18500 | −0.00229304 | −0.00228724 | $-5.8\times10^{-6}$ | 8.26847 | 15.9 a 16.9 s |

Sin Richardson en la tabla, $\delta=0$ da $-0.49997116$ (error $2.9\times10^{-5}$) con $h_{\rm tab}=0.01$ y $-0.49999271$ ($7.3\times10^{-6}$) con $0.005$: el error de tabulación baja como $h_{\rm tab}^2$. En $\delta=1.0$ y $1.1$ la diferencia que queda es sesgo de Trotter: con $\epsilon\in\{0.2,0.1,0.05\}$, $E=-0.01031956,\ -0.01029431,\ -0.01028789$, orden aparente **1.98**, y la extrapolación $\epsilon\to0$ da $-0.01028575$, a $3.4\times10^{-8}$ del solucionador radial (de 15.2 a 43.4 s para las seis tablas y los tres autovalores, según la carga).

**D. Duración de la proyección.** Con la transferencia en red ($h=0.02$, $R=40$, $\delta=0.2$, $\epsilon=0.1$) y $u_T=r e^{-r}$, el estimador mixto menos **su propio límite** $\tau\to\infty$ vale $+2.3\times10^{-4}$, $+1.5\times10^{-4}$, $+9.9\times10^{-5}$, $+6.7\times10^{-5}$, $+4.6\times10^{-5}$, $+3.2\times10^{-5}$, $+1.5\times10^{-5}$, $+7.7\times10^{-6}$, $+1.4\times10^{-6}$, $+2.6\times10^{-7}$, $+1.0\times10^{-8}$ para $\tau=1,2,3,4,5,6,8,10,15,20,30$: es positivo y decrece de forma monótona, es decir, el mixto llega a su límite desde arriba sin cruzarlo. Entre $\tau=20$ y $30$ cambia $2.5\times10^{-7}$, por lo que $\tau=20$ basta en $\delta=0.2$.

El límite del mixto ($-0.32680947$) queda $4.9\times10^{-5}$ por debajo del autovalor $E_0(T)=-0.32676029$ de la matriz de transferencia, y por eso la serie $E_{\rm mixto}-E_0(T)$ cambia de signo cerca de $\tau=5$. Esa diferencia **no es de Trotter**: no cambia con $\epsilon$ ($-4.918\times10^{-5}$ para $\epsilon=0.2$, $0.1$ y $0.05$ con $h=0.02$) y baja a $-1.23\times10^{-5}$ con $h=0.01$, un factor 4 al dividir $h$ entre 2. Es el error de malla, de orden $h^2$, del núcleo de Coulomb de diferencias finitas que se usa en esta parte sin la tabla con Richardson: el Coulomb de la red con $h=0.02$ da $E_0=-0.49995001$ (error $5.0\times10^{-5}$), y ese error lo hereda $E_0(T)$, que queda $4.8\times10^{-5}$ por encima del radial. El estimador mixto usa la energía local del hamiltoniano continuo, $E_L=W-\tfrac12$, y su límite queda a $1.3\times10^{-6}$ o menos del radial para los seis pares $(h,\epsilon)$ probados. **Regla adoptada:** el mixto y el autovalor de $T$ solo se comparan tras eliminar el error de malla (Richardson en $h$ o en $h_{\rm tab}$) y el de $\epsilon$. En la parte F, con Richardson en $h_{\rm tab}$, el autovalor en $\delta=0.2$, $\epsilon=0.1$ queda a $1.5\times10^{-8}$ del radial, de modo que el sesgo de Trotter del autovalor es ahí de ese orden o menor.

**E. PIGS.** 9 cadenas, 4 procesos, de 39 a 66 s de reloj según la carga; de 1.3 a 3.25 ms por barrido ($M=100$ a 200; 1.36 a 1.71 ms en las dos ejecuciones de la versión actual, 1.61 a 3.25 ms en la de la revisión adversarial); aceptación 0.80 a 0.82 en puentes y 0.71 a 0.72 en escala.

- *Control $\delta=0$* ($u_T$ exacta, $\tau=10$): $E_L=-0.5$ con varianza nula, como debe; $\langle r\rangle=1.4600\pm0.0380$ y $\langle r^2\rangle=2.830\pm0.173$ frente a 1.5 y 3 ($-1.1\sigma$ y $-1.0\sigma$).
- *Punto fuertemente ligado $\delta=0.2$* ($\tau=20$, 8 semillas × 8000 barridos): $E=-0.32687$, $\langle r\rangle=1.539$, $\langle r^2\rangle=3.169$, frente a $-0.32680851$, $1.5497$ y $3.2259$ del solucionador radial: $-0.3\sigma$, $-0.4\sigma$, $-0.4\sigma$.
- *Errores.* El error de la media entre semillas ($2.1\times10^{-4}$ en $E$, 0.029 en $\langle r\rangle$) es mayor que el combinado por bloques ($1.3\times10^{-4}$ y 0.014): el error por bloques subestima la varianza en un factor $(2.1/1.3)^2=2.69$ en $E$. **Regla adoptada:** siempre al menos 8 cadenas independientes, y se reporta el mayor de los dos errores.

## 9.6 Criterio para declarar "ligado" (sin depender solo del signo de un autovalor)

La guía exige comparar varias cajas y una observable de localización. El barrido corto de la parte B (solucionador radial con $h=1/40$ y $1/80$; $E_0$ con Richardson en $h$, $\langle r\rangle/R$ y $F_{1/2}$ con $h=1/80$) muestra por qué:

| $\delta$ | $R$ | 50 | 100 | 200 | 400 | 800 |
|---|---|---|---|---|---|---|
| 1.15 (ligado) | $E_0$ | $-3.31\times10^{-4}$ | $-4.51\times10^{-4}$ | $-4.56\times10^{-4}$ | $-4.56\times10^{-4}$ | $-4.56\times10^{-4}$ |
| | $\langle r\rangle/R$; $F_{1/2}$ | 0.239; 0.895 | 0.164; 0.962 | 0.087; 0.998 | 0.044; 1.000 | 0.022; 1.000 |
| 1.18 (ligado) | $E_0$ | $+3.38\times10^{-4}$ | $+3.21\times10^{-5}$ | $-2.41\times10^{-5}$ | $-3.08\times10^{-5}$ | $-3.10\times10^{-5}$ |
| | $\langle r\rangle/R$; $F_{1/2}$ | 0.293; 0.832 | 0.268; 0.859 | 0.225; 0.904 | 0.153; 0.967 | 0.081; 0.998 |
| 1.20 (no ligado) | $E_0$ | $+6.44\times10^{-4}$ | $+1.87\times10^{-4}$ | $+5.80\times10^{-5}$ | $+1.84\times10^{-5}$ | $+5.67\times10^{-6}$ |
| | $\langle r\rangle/R$; $F_{1/2}$ | 0.324; 0.790 | 0.331; 0.776 | 0.352; 0.746 | 0.386; 0.695 | 0.426; 0.633 |
| 1.25 (no ligado) | $\langle r\rangle/R$; $F_{1/2}$ | 0.381; 0.706 | 0.416; 0.650 | 0.450; 0.592 | 0.473; 0.551 | 0.486; 0.527 |

Los valores saturados coinciden con la ley $\kappa=0.7421(\delta_c-\delta)$ de la sección 7: $-4.54\times10^{-4}$ en $\delta=1.15$ y $-3.10\times10^{-5}$ en $\delta=1.18$.

**Error de malla cerca del umbral.** La primera versión de esta tabla usaba $h=1/20$ sin Richardson, y ese sesgo es del orden de $|E_0|$ cerca del umbral: en $R=800$, $\delta=1.18$ da $E_0=-2.553\times10^{-5}$ con $h=1/20$, $-2.957\times10^{-5}$ con $h=1/40$ y $-3.063\times10^{-5}$ con $h=1/80$, frente a $-3.10\times10^{-5}$ con Richardson (sesgo del 18 % con $h=1/20$); en $\delta=1.15$ el sesgo es del 5 %. Un $E_0$ que "satura" con $R$ no está por eso convergido en $h$. Con la ley $\kappa$, el $E_0$ de $h=1/20$ en $\delta=1.18$ sitúa el umbral efectivo de esa red en $\delta\approx1.1896$, unos $10^{-3}$ por debajo de $\delta_c$ (estimación de la parte B, no un cálculo de umbral).

En $\delta=1.18$, que está ligado ($\delta_c=1.1906$), las cajas de 50 y 100 dan $E_0>0$: con el signo como único criterio se declararía "no ligado". Lo que sí separa los casos es la **tendencia con $R$**: en los ligados $\langle r\rangle/R$ baja y $F_{1/2}$ sube hacia 1; en los no ligados $\langle r\rangle/R$ sube hacia $1/2$ y $F_{1/2}$ baja hacia $1/2$, y esto ya se ve desde $R=50$. Criterio propuesto, aplicado a una sucesión de al menos tres cajas $R_1<R_2<R_3$ con razón 2:

- **Ligado** si se cumplen las cuatro: (a) $E_0(R_2)<0$, $E_0(R_3)<0$ y $|E_0(R_3)-E_0(R_2)|<0.1|E_0(R_3)|$ (saturación); (a') convergencia en la malla: en cada caja, $|E_0(h)-E_0(h/2)|<0.1|E_0|$, y se usa el valor con Richardson en $h$ (en la parte B el cociente es como mucho 0.06 con $h=1/40$ y $1/80$); (b) $\langle r\rangle/R$ decrece y $F_{1/2}$ crece en las tres cajas, con $F_{1/2}(R_3)>0.95$; (c) la integral de camino (transferencia) da el mismo signo y la misma tendencia en las mismas cajas, dentro de sus errores.
- **No ligado** si $E_0(R)>0$ en todas las cajas, $\langle r\rangle/R$ crece y $F_{1/2}$ decrece en las tres, y $E_0(R)$ sigue la ley de estado de caja $\pi^2/[2(R-a_s)^2]$ con la longitud de dispersión $a_s$ (sección 7.4, corrección L13).
- **Indeterminado** en otro caso; se agranda $R$ (factor 2) hasta un máximo de 1600 en el radial y 800 en la transferencia. Si sigue indeterminado, el punto se reporta así y no entra en el intervalo.

Aplicado a la tabla (solo con el solucionador radial, sin la condición (c)): $\delta=1.15$ ya pasa (a), (a') y (b) con $R=50,100,200$; $\delta=1.18$ solo las pasa con la terna $R=200,400,800$ (con $R=100,200,400$ falla (a): $E_0(100)>0$, y $E_0$ cambia $6.7\times10^{-6}$ entre 200 y 400 frente a un umbral de $3.1\times10^{-6}$); $\delta=1.20$ cumple ya con $R=50,100,200$ las dos tendencias de "no ligado", y queda por comprobar la ley de caja con $a_s$. El intervalo para $\delta_c$ de la Fase 4 será $[\delta_{\rm lig},\delta_{\rm no\,lig}]$, el par más cercano de puntos decididos, refinado por bisección con meta de ancho $\le0.005$. Se contrasta con dos estimaciones que no usan el signo: la extrapolación de $\kappa(\delta)\to0$ (sección 5.4) y el umbral de caja corregido con la ley $\delta_c-\delta_c(R)\simeq1.35/R$ (sección 7, L12).

## 9.7 Controles y criterios de aceptación

| Control | Criterio | Estado en la prueba |
|---|---|---|
| Coulomb $\delta=0$, transferencia (L02) | $|E+0.5|<10^{-6}$ para todo $\epsilon$ tras Richardson en $h_{\rm tab}$; $\langle r\rangle=1.5$ a $10^{-4}$ | $1.1\times10^{-7}$; 1.50000 |
| Coulomb $\delta=0$, PIGS | $E_L\equiv-0.5$; $\langle r\rangle$, $\langle r^2\rangle$ a menos de $2\sigma$ de 1.5 y 3 | $-1.1\sigma$, $-1.0\sigma$ |
| Punto fuertemente ligado $\delta=0.2$, transferencia | $|E-E_{\rm rad}|<10^{-6}$, $|\langle r\rangle-\langle r\rangle_{\rm rad}|<10^{-3}$ | $1.5\times10^{-8}$; $2\times10^{-5}$ |
| Punto fuertemente ligado $\delta=0.2$, PIGS | $E$, $\langle r\rangle$, $\langle r^2\rangle$ a menos de $2\sigma$ del radial, con $\sigma$ el mayor entre bloques y semillas | $-0.3\sigma$, $-0.4\sigma$, $-0.4\sigma$ |
| Ley $\epsilon^2$ | orden aparente en $[1.8,2.2]$ con $\epsilon\in\{0.2,0.1,0.05\}$; extrapolado a menos de $10^{-6}$ del radial (lejos del umbral) | 1.98; $3.4\times10^{-8}$ en $\delta=1.0$ |
| Tabulación | resultado con Richardson en $h_{\rm tab}$ estable a $10^{-6}$ al cambiar la malla Nyström de 0.02 a 0.04 | por hacer en Fase 2 |
| Proyección (L15) | variación $<10^{-6}$ al pasar de $\tau$ a $1.5\tau$ | $2.5\times10^{-7}$ entre 20 y 30 en $\delta=0.2$ |
| Malla espacial $h$ | $|E_0(h)-E_0(h/2)|<0.1|E_0|$ en cada caja, y se reporta el valor con Richardson en $h$ (radial) o en $h$ y $h_{\rm tab}$ (transferencia) | radial: $\le0.06$ con $h=1/40$ y $1/80$ en la parte B |
| Caja | $E_0(R)$ decreciente en $R$ (Dirichlet, L12); criterio de 9.6 | ver 9.6 |
| Hellmann-Feynman (L05) | $dE_0/d\delta=\langle e^{-\delta r}\rangle$ con el autovector de la transferencia, a $10^{-4}$ | por hacer en Fase 3 |
| Virial (L06) | $2\langle T\rangle-\langle rV'\rangle\to0$ al extrapolar $\epsilon$ y $h$ | por hacer en Fase 3 |
| Cotas (L04, L19) | $-\tfrac12\le E_0\le-\tfrac12+\delta$; sin ligado para $\delta\ge2$ | por hacer en Fase 3 |
| Umbral | intervalo final compatible con $\delta_c=1.1906124211$ y dentro de $[1.19055,1.24305]$ (cotas de las secciones 3 y 4) | Fase 4 |
| Errores por bloques | si (error entre semillas / error por bloques)$^2>2$, se reporta el error entre semillas | 2.69 en $\delta=0.2$: se aplica |

## 9.8 Presupuesto de errores

| Fuente | Cómo se estima | Tamaño medido en la prueba | Cómo se controla |
|---|---|---|---|
| Estadística (PIGS) | bloques (20 por cadena) y dispersión entre 8 cadenas | $\delta=0.2$, $6.4\times10^4$ barridos: $2.1\times10^{-4}$ en $E$, 0.029 en $\langle r\rangle$ | más barridos; escala $1/\sqrt N$ |
| Trotter ($\epsilon$) | barrido $\epsilon\in\{0.2,0.1,0.05\}$, ajuste $a+b\epsilon^2$ | $8.6\times10^{-6}$ en $\delta=1.0$, $\epsilon=0.1$ ($E(0.1)$ menos extrapolado) | extrapolación; residuo $3.4\times10^{-8}$ |
| Tabulación de $U_C$ | $h_{\rm tab}=0.01$ frente a $0.005$ | $2.9\times10^{-5}$ y $7.3\times10^{-6}$ en $\delta=0$ | Richardson; residuo $1.1\times10^{-7}$ |
| Caja ($R$) | sucesión de cajas | $e^{-2\kappa R}$ lejos del umbral; cerca, algebraico: $\delta_c(R)\simeq\delta_c-1.35/R$ (sección 7) | criterio de 9.6; corrección $1/R$ del umbral |
| Proyección ($\tau$) | $\tau$ y $1.5\tau$ | $2.5\times10^{-7}$ en $\delta=0.2$, $\tau=20$ | $\tau\ge\max(20,9/|E_0|)$ |
| Malla espacial $h$ (radial y Nyström) | $h$ y $h/2$ | radial, $R=800$: con $h=1/20$ sin Richardson, 18 % de $|E_0|$ en $\delta=1.18$ y 5 % en $\delta=1.15$; con $h=1/80$, 1.1 % y 0.3 % (frente a Richardson). Núcleo de Coulomb de diferencias finitas con $h=0.02$ (parte D): $5.0\times10^{-5}$ en $\delta=0$ y $4.8\times10^{-5}$ en $E_0(T)$ en $\delta=0.2$; con $h=0.01$, $1.2\times10^{-5}$. Nyström de la parte F: no medido aún por separado (en $\delta=1.0$ la extrapolación en $\epsilon$ queda a $3.4\times10^{-8}$ del radial, lo que lo acota en ese punto) | Richardson en $h$; criterio (a') de 9.6 |
| Interpolación bilineal de $U_C$ en PIGS | PIGS frente a transferencia en el mismo $\epsilon$ | no resuelta a la precisión estadística actual | comparar con la transferencia; si hace falta, interpolación bicúbica |

A la precisión estadística de la prueba ($\sim2\times10^{-4}$ en $E$), el PIGS está dominado por la estadística: los sesgos deterministas suman $\lesssim10^{-5}$. La transferencia no tiene error estadístico y está dominada, tras las dos extrapolaciones, por el error de caja cerca del umbral.

## 9.9 Costo estimado (medido)

Rangos de cuatro ejecuciones (ver el encabezado); las proyecciones usan el valor alto de cada rango.

| Tarea | Costo medido (rango) | Proyección (con el valor alto) |
|---|---|---|
| Solucionador radial, un punto $(\delta,R,h)$ | 0.004 a 0.05 s | barrido completo de Fase 4 (10 $\delta$ × 6 cajas × 3 mallas): segundos para $R\le800$; $R=1600$ con $h=1/80$ no se ha cronometrado |
| Tabla $U_C$ (dos $h_{\rm tab}$) por cada $\epsilon$ | de 0.57 + 1.73 s a 2.03 + 6.52 s | 3 valores de $\epsilon$: hasta unos 26 s, reutilizables para todos los $\delta$ |
| Transferencia en banda | 0.1 s ($N=2000$), 2.2 a 2.3 s ($N=8700$), 15.9 a 16.9 s para las dos tablas en $N=18500$; barrido de tres $\epsilon$ en $\delta=1.0$: 15.2 a 43.4 s | Fase 3 (5 $\delta$ × 3 $\epsilon$ × 2 tablas × 5 cajas, más la segunda malla $h$): de decenas de minutos a una hora con la máquina cargada (estimación a partir de los tiempos de la fila, no medida); las cajas de 800 con $h=0.02$ ($N=4\times10^4$) no se han cronometrado |
| PIGS, $\delta=0.2$, $M=200$ | 1.54 a 3.25 ms por barrido | error $10^{-4}$ en $E$: $1.0\times10^5$ barridos según bloques, unos 15 min de un núcleo con el factor 2.69 (7.2 a 7.6 min en las ejecuciones de carga baja); error 0.01 en $\langle r\rangle$: unos 27 min (12.8 a 13.4 min con carga baja). Producción de Fase 2 ($8\times5\times10^4$ barridos): unos 22 min de CPU, unos 6 min de reloj en 4 procesos |
| PIGS cerca del umbral, $\epsilon=0.1$, $\tau=9/|E_0|$ (lo que exige 9.4, sección 7, L15) | $M=8750$ en $\delta=1.0$ y $M=39349$ en $\delta=1.1$: de 67 a 141 ms por barrido en $\delta=1.0$ y de 302 a 636 ms en $\delta=1.1$, extrapolados linealmente en $M$ desde $M=200$ | sin contar el aumento de la autocorrelación con $M$, que **no se midió** y crece con $M$; por eso PIGS se limita a $\delta\le1.0$. Con $\tau=5/|E_0|$ ($M=4861$ y 21860) costaría 1.8 veces menos, pero no cumpliría el control de proyección de 9.7 |

## 9.10 Riesgos principales y plan B

1. **PIGS impracticable cerca del umbral** (tiempo de proyección $\propto|E_0|^{-1}$ y autocorrelación). *Plan B:* el resultado de tiempo imaginario cerca del umbral es la transferencia en banda (la misma acción sin muestreo); el PIGS se reporta en $\delta\le1.0$, y en $\delta=1.0$ con $\epsilon\in\{0.4,0.2\}$ y extrapolación si $\epsilon=0.1$ resulta caro.
2. **Subestimación de errores estadísticos.** Ya ocurrió (factor 2.69). *Plan:* 8 cadenas como mínimo y la regla de 9.7. Además se registró que el primer muestreador de esta revisión, con solo movimientos de una cuenta, daba en $\delta=0$ $\langle r\rangle=1.30\pm0.08$ con autocorrelación de unos 150 barridos: un falso acuerdo o desacuerdo por mal muestreo es un riesgo real, y por eso hay control con $u_T$ exacta.
3. **Circularidad de la tabla de pares** (misma red que el solucionador radial). *Plan B:* comparar con una tabla obtenida por otra vía (cuadrado de matrices a partir de la primitiva suavizada con extrapolación $a_s\to0$, sección 8.5 R3), o con las tablas de Pollock (1988) (referencia **no verificada**).
4. **Artefacto de caja cerca de $\delta_c$.** Es la razón de ser de 9.6. *Plan:* un punto que siga indeterminado con $R=1600$ no entra en el intervalo; el intervalo se ensancha antes que forzar un veredicto.
5. **Función de prueba con la cola equivocada.** $u_T=re^{-r}$ tiene $\kappa_T=1$ frente a $\kappa\to0$; la superposición cae y la proyección se alarga. *Plan B:* $u_T=re^{-\alpha r}$ con $\alpha$ del variacional de la sección 3 (no usa el solucionador radial, así que no hay circularidad).
6. **Tiempo de máquina compartida.** El script del bloque 08 tardó 50 s con carga baja y 217 s con la máquina cargada; el de este bloque, de 80 a 145 s en su versión anterior. Los tiempos varían en un factor 2 a 3. *Plan:* scripts por partes, resultados guardados en `.npz` con semilla y versión.

## 9.11 Calendario por fase y semana

La guía fija para la cohorte B (proyectos 02, 05, 08, 11, 14) la primera presentación en la **semana 7** y la segunda en la **semana 14**, y reserva la última semana del semestre para el artículo, la comprobación de reproducibilidad y las entrevistas. No fija las semanas de cada fase; la división siguiente la propuso la IA y la aprobó Lucho el 21-10-2026 (decisión 5 de `decisiones_pendientes.md`).

| Fase | Semanas | Tareas | Entregables |
|---|---|---|---|
| 2 | hasta la 7 | código de la tabla $U_C$, transferencia en banda y PIGS como módulos con prueba propia; controles $\delta=0$ y $\delta=0.2$ de 9.7; figura de $E_{\rm mixto}(\tau)$ (la guía pide en la primera exposición la comparación de ambos métodos en un punto fuertemente ligado) | código ejecutable, primer gráfico ($\delta=0.2$: radial frente a PIGS y transferencia, con barras de error), bitácora de IA, **presentación de la semana 7** (pregunta, acción, caso de referencia, cálculo preliminar, riesgo principal) |
| 3 | 8 a 11 | barrido de $\delta\le1.1$ y de cajas; convergencia en $\epsilon$, $\tau$, $h_{\rm tab}$; Hellmann-Feynman, virial y cotas; **auditoría adversarial por IA de autovalores cercanos a cero** (consulta del tipo "auditoría" de la guía con la tabla de 9.6 y la pregunta: qué explicación alternativa haría que un $E_0(R)<0$ fuera artefacto) | borrador del artículo, figuras con barras de error, tabla de controles (9.7 completa), resultados congelados para la segunda ronda |
| 4 | 12 a 16 | puntos de $\delta$ junto al umbral, criterio de 9.6, bisección, intervalo para $\delta_c$; crecimiento de $\langle r\rangle$ y $\langle r^2\rangle^{1/2}$; ampliación (otro perfil de apantallamiento o comparación con el criterio variacional de la sección 3) | **presentación de la semana 14** (prueba de caja que separa un estado débil de un artefacto, comparación independiente, conclusión proporcional a la evidencia), artículo final, repositorio, defensa individual |

## 9.12 Reparto de roles (aprobado el 21-10-2026)

La guía pide rotar al inicio de las Fases 2 y 3 las responsabilidades de formulación física, implementación y verificación, cada una con su pregunta de auditoría. La guía supone equipos de tres; este equipo es de dos (Juan Sebastián Calixto y Luis Felipe Ramírez, desde el 13-10-2026), así que en cada fase uno de los dos lleva dos responsabilidades. Para que la verificación siga siendo independiente, quien implementa no verifica en la misma fase. En la bitácora 2 del grupo, cuando era de tres, los roles fueron: prompts y línea principal, la integrante que después se retiró; cuestionador, Sebastián; revisor y verificador, Luis. **Roles de la Fase 1** (confirmados por Lucho el 21-10-2026, decisión 6 de `decisiones_pendientes.md`): Juan Sebastián Calixto, formulación física; Luis Felipe Ramírez, implementación y verificación. **Rotación** para que cada integrante pase por las tres responsabilidades, rotando al inicio de las Fases 2 y 3 (propuesta de la IA, aprobada por Lucho el 21-10-2026, decisión 6):

| Responsabilidad | Pregunta de auditoría (guía) | Fase 2 | Fase 3 | Fase 4 |
|---|---|---|---|---|
| Formulación física: hamiltoniano, acción, medida, peso, predicción de referencia | ¿El cálculo representa realmente la magnitud que se anuncia? | Juan Sebastián Calixto | Luis Felipe Ramírez | Juan Sebastián Calixto |
| Implementación: tabla $U_C$, transferencia, PIGS, semillas, perfiles de tiempo | ¿La discretización aproxima la formulación declarada? | Luis Felipe Ramírez | Juan Sebastián Calixto | Luis Felipe Ramírez |
| Verificación: solucionador radial, controles de 9.7, errores, registro de decisiones | ¿Qué resultado podría refutar la conclusión? | Juan Sebastián Calixto | Luis Felipe Ramírez | ambos |

En la Fase 4 los dos integran el artículo y preparan respuestas individuales, como pide la guía; la columna de la Fase 4 solo indica quién responde por defecto por cada parte. Cada responsable deja su huella en la bitácora (entradas firmadas en el registro de IA y en la tabla de controles).

## 9.13 Límites, consistencia y anomalías

- **Límites.** $\delta\to0$: la transferencia es exacta para todo $\epsilon$ (comprobado a $10^{-7}$). $\epsilon\to0$: orden 1.98. $R\to\infty$: $\langle r\rangle/R\to0$ y $F_{1/2}\to1$ si está ligado, $\to1/2$ si no. $\tau\to\infty$: estimador mixto constante a $2.5\times10^{-7}$ entre $\tau=20$ y 30. $h\to0$: error de malla $\propto h^2$ (parte D y parte B).
- **Dimensiones.** $\epsilon$ en $\hbar^3/(mg^2)$, $r$ en $\hbar^2/(mg)$, $E$ en $mg^2/\hbar^2$; $\epsilon E$ y $(\Delta r)^2/\epsilon$ son adimensionales.
- **Anomalía resuelta.** La primera tanda de 4 semillas en $\delta=0.2$ daba $E=-0.32728$ ($-2.5\sigma$ con el error por bloques); con 8 semillas el desacuerdo baja a $-0.3\sigma$ y aparece la subestimación del error por bloques. Era estadística, no sesgo; lo confirmó además el cálculo determinista del mismo estimador.
- **Anomalía resuelta (revisión adversarial).** La primera versión decía que el estimador mixto no era monótono en $\tau$ y que cruzaba su límite cerca de $\tau=5$. Era una lectura equivocada: el script imprimía $E_{\rm mixto}-E_0(T)$, no $E_{\rm mixto}$ menos su límite. El mixto decrece de forma monótona hacia su límite (9.5 D); lo que cruza cerca de $\tau=5$ es el autovalor $E_0(T)$, que difiere del límite del mixto por el error de malla $O(h^2)$ del núcleo de Coulomb de la parte D, no por Trotter.

## Registro de IA

**Entrada 1.**
- *Fecha*: 12 de octubre de 2026. *IA*: Claude (Anthropic).
- *Consulta*: tarea asignada a Claude por el flujo de revisión: escribir el plan de cómputo de las Fases 2 a 4 a partir de las secciones 5, 7 y 8 y de la guía del profesor, con observables, referencia, formulación, parámetros, controles, presupuesto de errores, criterio de enlace, costo medido, calendario, riesgos y roles.
- *Respuesta utilizada*: esta sección 9 y el script `09_prueba_costos.py` (partes A a F).
- *Decisión humana*: aprobado por Lucho el 21-10-2026 (`decisiones_pendientes.md`): la formulación R1 con transferencia en banda y PIGS (decisión 4); el punto $\delta=0.2$, la rejilla de cajas y el criterio de enlace de 9.6, los controles de 9.7 con Hulthén y el calendario de 9.11 (decisión 5); el reparto de roles de 9.12 (decisión 6).
- *Comprobación*: cada cifra salió del script; la transferencia se contrastó con el solucionador radial en cuatro $\delta$ y con el límite exacto de Coulomb; el PIGS con la función de prueba exacta en $\delta=0$ y con el radial en $\delta=0.2$; la ley $\epsilon^2$ con tres $\epsilon$; los errores estadísticos por dos vías (bloques y semillas).
- *Corrección posterior* (errores de Claude detectados al ejecutar): (i) el primer PIGS movía una cuenta a la vez y en $\delta=0$ daba $\langle r\rangle=1.30\pm0.08$ y $\langle r^2\rangle=2.11\pm0.24$ con autocorrelación de unos 150 barridos; se cambió a puentes brownianos más un movimiento global de escala. (ii) Con 4 semillas, $E(\delta=0.2)$ quedaba a $-2.5\sigma$; con 8 semillas queda a $-0.3\sigma$, y el error por bloques resultó subestimado en un factor 2.69; se adoptó la regla de reportar el mayor de los dos errores. (iii) La matriz en banda tomaba valores NaN de la tabla fuera de su banda y ARPACK fallaba; esos elementos se ponen a cero (su peso gaussiano es menor que $e^{-20}$). (iv) Sin Richardson en $h_{\rm tab}$ el control de Coulomb fallaba en $2.9\times10^{-5}$; se añadió la segunda tabla. (v) El estimador mixto tiende a un valor distinto del autovalor de la transferencia ($4.9\times10^{-5}$ a $\epsilon=0.1$). La primera versión lo atribuyó a sesgos $O(\epsilon^2)$ distintos y leyó como "no monótona" una serie que era $E_{\rm mixto}-E_0(T)$. La revisión adversarial (ronda 2, 12 de octubre de 2026) mostró, y el script re-ejecutado confirma, que la diferencia no depende de $\epsilon$ y baja como $h^2$: es error de malla del núcleo de Coulomb de diferencias finitas en $h=0.02$; el mixto es monótono. Corregido en 9.5 D y 9.13. (vi) La tabla de 9.6 usaba $h=1/20$ sin Richardson, con sesgo del 18 % de $|E_0|$ en $\delta=1.18$; se rehízo con Richardson en $h$ y se añadió el criterio (a'). (vii) El costo de PIGS cerca del umbral se calculaba con $\tau=5/|E_0|$ en lugar del $9/|E_0|$ que exige 9.4; se recalculó. (viii) Los tiempos se daban como cifras únicas; ahora son rangos de cuatro ejecuciones.
