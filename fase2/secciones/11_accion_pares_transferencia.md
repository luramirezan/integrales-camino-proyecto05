# 11. Acción de pares de Coulomb y matriz de transferencia en banda

**Proyecto 05, umbral de ligadura en el potencial de Yukawa** · Fase 2 · Bloque 11 · 27 de octubre de 2026
Implementación: Luis Felipe Ramírez (rol de implementación en la Fase 2, con Claude como asistente). Verifica: Juan Sebastián Calixto.
Tareas 2, 3 y 7 de `fase1/que_sigue_fase2.md`.

Código (en `fase2/codigo/`):

- `pares.py`: tabla de $U_C$.
- `transferencia.py`: matriz de transferencia.
- `test_transferencia.py`: pruebas con `assert`. Las cinco pasan.
- `11_transferencia_controles.py`: controles de este bloque.

Resultados en `fase2/resultados/11_transferencia.json`. Figuras: `fase2/figuras/11_trotter.png` y `fase2/figuras/11_proyeccion.png`. Las tablas de $U_C$ quedan en caché en `fase2/resultados/tablas/UC_*.npz`. Todas las cifras de este bloque salen de la ejecución del 27-10-2026 del script 11. El script es determinista, no usa números aleatorios y tarda 27 s con la carga de la máquina entre 0.5 y 0.9.

La referencia radial es `fase2/codigo/radial.py` (`resolver_rich`, diferencias finitas con Richardson), que ya estaba escrito. Se usó con $h=1/80$ y $1/160$:

| $\delta$ | $R$ | $E_0$ radial | $\langle r\rangle$ radial | diferencia con $h=1/40$ y $1/80$ |
|---|---|---|---|---|
| 0.2 | 40 | −0.32680851098 | 1.5497219 | $5.8\times10^{-9}$ |
| 1.0 | 174 | −0.01028578963 | 4.3667048 | $5.4\times10^{-9}$ |

## 11.1 Formulación

Unidades $\hbar=m=g=1$ y $V=-e^{-\delta r}/r$. Sector $\ell=0$, con $u(0)=0$. Se separa $V=V_C+W$, donde $V_C=-1/r$ y
$$W(r)=\frac{1-e^{-\delta r}}{r}\in[0,\delta].$$
El eslabón de la integral de camino es
$$T(r,r';\epsilon)=K_D(r,r';\epsilon)\,e^{-U_C(r,r';\epsilon)}\,e^{-\epsilon[W(r)+W(r')]/2},\qquad
K_D=\frac{e^{-(r-r')^2/2\epsilon}-e^{-(r+r')^2/2\epsilon}}{\sqrt{2\pi\epsilon}},\qquad U_C=-\ln\frac{\rho_C}{K_D}.$$
Aquí $\rho_C$ es el núcleo exacto $\langle r|e^{-\epsilon H_C}|r'\rangle$ del Coulomb puro. Toda la singularidad $-1/r$ queda dentro de $\rho_C$, y el resto $W$ es acotado y suave. Por eso la factorización simétrica tiene sesgo $O(\epsilon^2)$, y en $\delta=0$ el método es exacto para todo $\epsilon$.

**Tabla de $U_C$ (`pares.py`).** Sigue la receta de la parte C de `09_prueba_costos.py`:

- Se calcula de forma espectral: se diagonaliza el hamiltoniano de Coulomb tridiagonal en una caja de Dirichlet $R_B=14$ con paso $h_{\rm tab}$.
- El resultado se divide por el núcleo libre de la **misma** red.
- Se tabula en $r,r'\le R_{\rm TAB}=10$, dentro de la banda $|r-r'|\le7\sqrt\epsilon$. Fuera de la banda, el peso gaussiano es menor que $e^{-24.5}$ del valor en la diagonal.
- Se usan $h_{\rm tab}=0.01$ y $0.005$ y se combinan con Richardson en los nodos comunes: $U_R=(4U_{0.005}-U_{0.01})/3$.
- Para $r>10$ se usa (desde V3) la aproximación de extremos **con el término de Wigner-Kirkwood**, $U_C\approx\frac\epsilon2[V_C(r)+V_C(r')]+\frac{V_C''(m)}{12}[\epsilon^2-\epsilon(r-r')^2]$, con $m=(r+r')/2$ y $V_C''=-2/m^3$. En $r=r'=9$ la tabla da $-0.0111134$, frente a $-\epsilon/9=-0.0111111$ con $\epsilon=0.1$: la diferencia, $-2.29\times10^{-6}$, es exactamente $-\epsilon^2/(6r^3)$ (hallazgo H2 de V2; la versión anterior decía "error $<10^{-7}$ en $r\ge10$", y era falso). Con el término nuevo el error en la diagonal baja a $8.1\times10^{-9}$ ($r=9$, $\epsilon=0.1$) y a $6.5\times10^{-8}$ ($\epsilon=0.2$); prueba `test_extremos_wk` en `test_transferencia.py`. Efecto en la energía: en $\delta=0.2$ ($R=40$) nada visible ($<10^{-11}$); en $\delta=1.0$ ($R=174$) sube $E(\epsilon)$ en $+1.5\times10^{-7}$, $+5.0\times10^{-8}$ y $+1.7\times10^{-8}$ ($\epsilon=0.2,0.1,0.05$), lo mismo que V1 midió con el núcleo exacto (H3 de V1).
- Fuera de la banda no se tabula: esos valores son NaN.

La tabla guarda solo la banda y se lee de la caché en 0.1 s. Calcularla de nuevo cuesta 0.5 s con $h_{\rm tab}=0.01$ y 2.1 s con $0.005$, para $\epsilon=0.1$. Hay dos interpolaciones en $r$ continuo para el PIGS, `bilineal` y `bicubica` (spline bicúbico interpolante). Por debajo del primer nodo ($r<0.01$) se extrapola de forma lineal.

**Transferencia (`transferencia.py`).** Se aplica la regla del trapecio (Nyström) en $r_i=ih$, con $T_{ij}=h\,T(r_i,r_j;\epsilon)$:

- $U_C$ se toma en los nodos de la tabla, sin interpolar. Por eso $h$ tiene que ser múltiplo de 0.01.
- Los elementos fuera de la banda o no finitos valen **cero** (corrección (iii) del registro de la Fase 1).
- La matriz es simétrica y está en banda. $E_0(\epsilon)=-\ln\lambda_0/\epsilon$ sale de `eigsh`.
- El autovector da $\langle r\rangle$, $\langle r^2\rangle$, $F_{1/2}$ (con medio peso en $r=R/2$) y $\langle r\rangle/R$.
- La opción sin $U_C$ (argumento `V=`) usa $h\,K_D\,e^{-\epsilon[V_i+V_j]/2}$ con el potencial completo. Es para potenciales sin singularidad.
- `proyeccion_mixta` calcula $E_{\rm mixto}(\tau)=\langle Hu_T|T^M|u_T\rangle/\langle u_T|T^M|u_T\rangle$, con $Hu_T$ evaluado con el hamiltoniano **continuo**.

## 11.2 Declaración del peso

Se pide declarar si el peso muestreado es real, positivo y normalizable. El peso es

$$P[r_0,\dots,r_M]=u_T(r_0)\prod_k T(r_k,r_{k+1};\epsilon)\,u_T(r_M),$$

y cumple las tres condiciones:

- **Real.** No hay fases: todos los factores son exponenciales reales.
- **Positivo.** $K_D>0$ para $r,r'>0$, y $e^{-U_C}$ y $e^{-\epsilon W/2}$ son positivos. En la matriz de $\delta=0.2$ con $R=40$ y $h=0.02$ hay 0 elementos negativos y 0 no finitos. El menor elemento no nulo está entre $3\times10^{-13}$ y $8\times10^{-13}$, en el borde de la banda.
- **Normalizable.** $U_C$ es finita y acotada en el origen (tabla siguiente), así que $e^{-U_C}\le e^{1.14}$ y cada eslabón es un núcleo integrable. La mayor suma de fila de $T$ es 1.191, 1.123 y 1.081 para $\epsilon=0.2$, $0.1$ y $0.05$. La acción primitiva con $1/r$ desnudo daría en $r=0.01$ el factor $e^{\epsilon/r}=e^{20},e^{10},e^{5}$, y diverge en $r\to0$ (sección 8.4.2). Por eso queda prohibida.

**Valores de $U_C$ cerca del origen** (tabla con Richardson):

| $\epsilon$ | $U(0.01,0.01)$ | $U(0.02,0.02)$ | $U(0.05,0.05)$ | $U(0.1,0.1)$ | $U(0.01,0.5)$ | mín. de la tabla |
|---|---|---|---|---|---|---|
| 0.2 | −1.132354 | −1.112839 | — | −0.967488 | −0.792800 | −1.132354 |
| 0.1 | −0.788269 | −0.768975 | −0.713749 | −0.629703 | −0.491808 | −0.788269 |
| 0.05 | −0.548446 | −0.529460 | — | −0.398042 | −0.297280 | −0.548446 |

Con $\epsilon=0.1$, $U(0.02,0.02)=-0.76898$ coincide con el $-0.7689$ de la Fase 1. La mayor diferencia entre las dos redes, $|U_{0.01}-U_{0.005}|$ en $|r-r'|\le1$, es $4.4\times10^{-5}$, $5.2\times10^{-5}$ y $1.0\times10^{-4}$ para $\epsilon=0.2$, $0.1$ y $0.05$. Ese es el error de tabulación que elimina Richardson. Ningún elemento de $\rho$ sale $\le0$ dentro de la banda.

## 11.3 Controles

$R=40$ salvo que se diga otra cosa. Las energías usan la tabla con Richardson en $h_{\rm tab}$.

| # | Control | Criterio | Valor | ¿Pasa? |
|---|---|---|---|---|
| 1a | Coulomb $\delta=0$, $h=0.02$, $\epsilon=0.2$ | $\|E+0.5\|<10^{-6}$ | $5.4\times10^{-8}$ | sí |
| 1b | ídem, $\epsilon=0.1$ | ídem | $1.09\times10^{-7}$ | sí |
| 1c | ídem, $\epsilon=0.05$ | ídem | $2.18\times10^{-7}$ | sí |
| 1d | Coulomb, $\langle r\rangle$, $\epsilon=0.2,0.1,0.05$ | $\|\langle r\rangle-1.5\|<10^{-4}$ | $1.7\times10^{-7}$, $3.3\times10^{-7}$, $6.6\times10^{-7}$ | sí |
| 2a | $\delta=0.2$, $h=0.02$, $E$, con $\epsilon=0.2,0.1,0.05$ | $\|E-E_{\rm rad}\|<10^{-6}$ | $-4.0\times10^{-7}$, $-1.0\times10^{-8}$, $+1.8\times10^{-7}$ | sí |
| 2b | $\delta=0.2$, $h=0.02$, $\langle r\rangle$ | $<10^{-3}$ | $5.4\times10^{-5}$, $1.4\times10^{-5}$, $4.1\times10^{-6}$ | sí |
| 2c | $\delta=0.2$, $h=0.04$ (control), $E$ | $<10^{-6}$ | $+3.6\times10^{-7}$, $+1.51\times10^{-6}$, $+3.22\times10^{-6}$ | **no** con $\epsilon=0.1$ y $0.05$ (ver 11.4) |
| 2d | $\delta=0.2$, $h=0.04$, $\langle r\rangle$ | $<10^{-3}$ | $5.7\times10^{-5}$, $1.9\times10^{-5}$, $1.5\times10^{-5}$ | sí |
| 2e | Ley $\epsilon^2$ en $\delta=0.2$ con $h=0.02$ sin Richardson en $h$ | orden en $[1.8,2.2]$ | 1.05 | **no** (ver 11.4) |
| 2f | Ley $\epsilon^2$ en $\delta=0.2$ con Richardson en $h$ ($h^4$, 0.02 y 0.04) | orden en $[1.8,2.2]$; extrapolado a $<10^{-6}$ | 1.958; $+4.4\times10^{-9}$ | sí |
| 2g | Ley $\epsilon^2$ en $\delta=1.0$, $R=174$, $h=0.02$ | ídem | 1.978; $+4.5\times10^{-8}$ (antes de V3: 1.976; $+3.9\times10^{-8}$) | sí |
| 2h | Ley $\epsilon^2$ en $\delta=1.0$ con Richardson en $h$ | ídem | 1.983; $-1.2\times10^{-8}$ (antes de V3: 1.981; $-1.8\times10^{-8}$) | sí |
| 3 | Estabilidad de Nyström: $\|E(0.04)-E(0.02)\|$ ($\delta=0$; $0.2$; $1.0$), con $\epsilon=0.2,0.1,0.05$ | $<10^{-6}$ | $\delta=0$: $0.80$, $1.60$, $3.20\times10^{-6}$; $\delta=0.2$: $0.76$, $1.52$, $3.04\times10^{-6}$; $\delta=1.0$: $0.17$, $0.36$, $0.73\times10^{-6}$ | **no** con $\epsilon\le0.1$ en $\delta=0$ y $0.2$; sí en los otros cinco casos |
| 4a | Proyección: $\|E_{\rm mixto}(30)-E_{\rm mixto}(20)\|$ | $<10^{-6}$ | $2.5\times10^{-7}$ | sí |
| 4b | Límite del mixto frente a $E_0(T)$ | $<10^{-6}$ | $1.05\times10^{-7}$ con $h=0.02$; $1.3\times10^{-9}$ con Richardson en $h$ (V3: es error de malla de $E_0(T)$, no del estimador) | sí |

En total pasan 28 de 35 criterios (en el json se cuentan uno por uno). Los 7 que fallan son:

- 2c con $\epsilon=0.1$ y $0.05$ (2 criterios);
- 2e (1 criterio);
- 3 en $\delta=0$ y $\delta=0.2$ con $\epsilon=0.1$ y $0.05$ (4 criterios).

Los siete tienen la misma causa, explicada en 11.4. Ninguno afecta a la malla de producción $h=0.02$ en $\delta=0.2$, donde 2a y 2b pasan para los tres $\epsilon$.

**Valores con $\delta=0.2$ y $h=0.02$** (tabla con Richardson):

| $\epsilon$ | $E$ | $\langle r\rangle$ | $F_{1/2}$ |
|---|---|---|---|
| 0.2 | −0.3268089106 | 1.549776 | 1.000000 |
| 0.1 | −0.3268085215 | 1.549736 | 1.000000 |
| 0.05 | −0.3268083330 | 1.549726 | 1.000000 |

Hacer Richardson sobre $E$ en lugar de sobre la tabla cambia el resultado en $\le1.3\times10^{-9}$. Sin Richardson en $h_{\rm tab}$, Coulomb falla por $2.6$ a $3.1\times10^{-5}$ con $h_{\rm tab}=0.01$ y por $6.5$ a $8.0\times10^{-6}$ con $0.005$.

**Trotter en $\delta=1.0$.** Con $\epsilon=0.2$, $0.1$ y $0.05$ y $h=0.02$, se obtiene:

| $\epsilon$ | $E$ | $E-E_{\rm rad}$ | $\langle r\rangle-\langle r\rangle_{\rm rad}$ |
|---|---|---|---|
| 0.2 | −0.0103194084 | $-3.36\times10^{-5}$ | $-5.3\times10^{-3}$ |
| 0.1 | −0.0102942585 | $-8.47\times10^{-6}$ | $-1.4\times10^{-3}$ |
| 0.05 | −0.0102878731 | $-2.08\times10^{-6}$ | $-3.3\times10^{-4}$ |

Antes de V3 esto reproducía la Fase 1 ($-0.01031956$, $-0.01029431$, $-0.01028789$; orden 1.98). Con el término de Wigner-Kirkwood de V3 los tres valores suben $+1.5\times10^{-7}$, $+5.0\times10^{-8}$ y $+1.7\times10^{-8}$, como predijo V1 (H3), y el orden queda en 1.978 (tabla actualizada desde `11_transferencia.json` en la revisión final del 27-10-2026). Ojo: en $\delta=1.0$ el sesgo de Trotter de $\langle r\rangle$ pasa de $10^{-3}$ con $\epsilon\ge0.1$. Para $\langle r\rangle$ cerca del umbral habrá que extrapolar también en $\epsilon$.

## 11.4 Lo que no pasa: error de Nyström $\propto h^4/\epsilon$ que nace en la cúspide del origen

El control 3 (estabilidad de la tabulación de 0.02 a 0.04 a $10^{-6}$) **no se cumple** con $\epsilon\le0.1$ en $\delta=0$ y $0.2$. Lo medido es lo siguiente:

1. **La diferencia escala como $1/\epsilon$.** $\epsilon\,[E(0.04)-E(0.02)]$ vale $1.60\times10^{-7}$ en $\delta=0$, $1.52\times10^{-7}$ en $\delta=0.2$ y $3.6\times10^{-8}$ en $\delta=1.0$, igual para los tres $\epsilon$. Es decir, el error es un error **por eslabón**, independiente de $\epsilon$. Al dividir por $\epsilon$ para pasar de $\lambda$ a $E$, crece cuando $\epsilon$ baja.
2. **Es de orden $h^4$.** Con $h=0.04$, $0.02$ y $0.01$, el orden aparente en $h$ es 4.00 en los seis casos ($\delta=0$ y $0.2$; tres $\epsilon$). En Coulomb con $\epsilon=0.1$ el error baja de $1.7\times10^{-6}$ a $1.1\times10^{-7}$ y luego a $8.8\times10^{-9}$.
3. **Nace en el origen.** El error por eslabón dividido por $u'(0)^2$ (tomado del radial) es casi el mismo en los tres $\delta$: $4.00$, $3.99$ y $3.86\times10^{-8}$. (V3, hallazgo H6 de V1: antes se tomaba $u'(0)^2\approx(u_1/r_1)^2$ con $r_1=1/160$, que está sesgado por $(1-r_1)^2=0.9875$; daba 3.9502 en Coulomb y los cocientes 4.05, 4.04 y $3.91\times10^{-8}$. Ahora $u'(0)=\lim u/r$ por ajuste cúbico de $u/r$ en los 6 primeros nodos: $u'(0)^2=3.99992$ en Coulomb, exacto 4; 3.80321 en $\delta=0.2$ y 0.92904 en $\delta=1.0$, como el disparo de V1.) Para comparar, el oscilador armónico con la opción sin $U_C$, cuya $u$ es impar y suave en el origen, no cambia con $h$ (variación $4.7\times10^{-13}$ entre $h=0.08$, $0.04$ y $0.02$).

**Interpretación.** El trapecio con $u(0)=0$ es espectral si el integrando se extiende de forma suave e impar a $r<0$. La función de Coulomb $u\approx r-r^2+\dots$ tiene un término par, la cúspide ($\rho_C$ la hereda), y eso deja un error de extremo de orden $h^4$, proporcional al peso en el origen $u'(0)^2$.

**Consecuencias.**

- (a) En la malla de producción $h=0.02$, el error es $1.1\times10^{-7}/(\epsilon/0.1)$ en $\delta\le0.2$. Está por debajo de $10^{-6}$ para los tres $\epsilon$, y por eso 1 y 2a pasan.
- (b) $h=0.04$ es mala malla de control para $\epsilon\le0.1$: es 16 veces peor.
- (c) **Remedio:** Richardson en $h$ con exponente 4, $E_h^{(R)}=(16E_{h}-E_{2h})/15$. Con eso el orden de Trotter en $\delta=0.2$ sale 1.958 y el extrapolado queda a $4.4\times10^{-9}$ del radial (2f).
- (d) El control 2e falla por la misma razón. En $\delta=0.2$ el sesgo de Trotter es pequeño ($-4.5\times10^{-7}$ a $\epsilon=0.2$ tras Richardson en $h$) y del mismo tamaño que el error de Nyström a $h=0.02$, que crece como $1/\epsilon$. Sin quitar este último, la serie no muestra la ley $\epsilon^2$: el orden aparente sale 1.05. Por eso, como se pidió, el orden se midió también en $\delta=1.0$ con $R=174$, donde el sesgo de Trotter es 70 veces mayor: 1.978 sin Richardson en $h$ y 1.983 con él (1.976 y 1.981 antes de la corrección de Wigner-Kirkwood de V3).

**Propuesta para que la valide quien verifica.** Redefinir el control de tabulación de 9.7 como: "Richardson en $h$ con exponente 4 entre 0.02 y 0.04 (o 0.01 y 0.02, como prevé 9.4 para la Fase 3), y estabilidad $<10^{-6}$ del valor extrapolado". Mientras no se apruebe, el control de 9.7 tal como está escrito **no pasa** en $\delta\le0.2$ con $\epsilon\le0.1$.

## 11.5 Proyección determinista desde $u_T=r\,e^{-r}$

Datos: $\delta=0.2$, $\epsilon=0.1$, $h=0.02$, $R=40$, tabla con Richardson. $Hu_T=(W-\tfrac12)u_T$ es exacto porque $u_T$ cumple la cúspide. La función de prueba no es exacta para $\delta>0$. La transferencia da $E_0(T)=-0.3268085215$ y $E_1(T)=-0.012107$, con brecha 0.31470. El límite del mixto, $\tau\to\infty$, es $-0.3268086269$: queda a $-1.05\times10^{-7}$ de $E_0(T)$ y a $-1.16\times10^{-7}$ del radial.

| $\tau$ | 1 | 2 | 3 | 4 | 5 | 6 | 8 | 10 | 15 | 20 | 30 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| $E_{\rm mixto}-$límite | $2.27\times10^{-4}$ | $1.48\times10^{-4}$ | $9.91\times10^{-5}$ | $6.71\times10^{-5}$ | $4.60\times10^{-5}$ | $3.18\times10^{-5}$ | $1.54\times10^{-5}$ | $7.64\times10^{-6}$ | $1.38\times10^{-6}$ | $2.62\times10^{-7}$ | $1.0\times10^{-8}$ |

- La serie es monótona decreciente: el mixto llega a su límite desde arriba.
- De $\tau=20$ a $30$ cambia $2.52\times10^{-7}$, menos que $10^{-6}$. Por eso $\tau=20$ basta en $\delta=0.2$, como en 9.5 D.
- La diferencia entre el límite del mixto y $E_0(T)$, que en la Fase 1 era $4.9\times10^{-5}$ (error de malla del núcleo de Coulomb sin tabla Richardson), baja ahora a $1.05\times10^{-7}$. **Ese residuo es error de malla de $E_0(T)$, no una propiedad del estimador mixto** (V3, hallazgo H7 de V1, reproducido): con $h=0.04$ la diferencia es $-1.67\times10^{-6}$, y con Richardson $h^4$ (0.02 y 0.04) baja a $-1.3\times10^{-9}$; $E_0(T)$ con $h=0.02$ está $+1.01\times10^{-7}$ por encima de su valor extrapolado, mientras que el límite del mixto (que usa $Hu_T$ continuo) solo se mueve $2.9\times10^{-9}$. V1 obtuvo $8\times10^{-10}$ con el operador continuo. Cifras en `11_transferencia.json`, `proyeccion/V3_malla`.

Figura: `fase2/figuras/11_proyeccion.png`.

## 11.6 Interpolación de $U_C$ para el PIGS

Para medir el error de interpolación se tomó la red $h_{\rm tab}=0.005$ submuestreada a la malla 0.01. Se interpoló en los puntos medios y se comparó con los valores reales de la red 0.005, con $\epsilon=0.1$:

| zona | bilineal (máx.; rms) | bicúbica (máx.; rms) |
|---|---|---|
| $r\in[0.05,9]$, $\|r-r'\|\le1$ | $5.1\times10^{-5}$; $5.3\times10^{-6}$ | $9.2\times10^{-9}$; $3.8\times10^{-10}$ |
| $r\in[0.01,0.1]$, $\|r-r'\|\le0.1$ | $5.8\times10^{-5}$; $4.0\times10^{-5}$ | $1.3\times10^{-8}$; $2.7\times10^{-9}$ |
| $r=r'=0.005$ (por debajo del primer nodo, extrapolación lineal) | $1.7\times10^{-4}$ | $1.7\times10^{-4}$ |

La bilineal comete un error del mismo tamaño que el de tabulación que Richardson elimina. **Recomendación para el PIGS:** usar la bicúbica (`TablaPares.valor(a, b, "bicubica")`). La zona $r<0.01$ tiene probabilidad de orden $r^3\sim10^{-6}$.

## 11.7 Opción sin $U_C$ con el pozo cuadrado (informativo, no es criterio)

Caso: $V_0=2$, $a=1$, $R=20$, convención de valor medio en el salto. El radial da $E_0=-0.20355074$. La transferencia sin $U_C$ da:

| $h$ | $E$ con $\epsilon=0.2$ | $\epsilon=0.1$ | $\epsilon=0.05$ | orden aparente en $\epsilon$ | extrapolado (ley $\epsilon^2$) | diferencia con el radial |
|---|---|---|---|---|---|---|
| 0.02 | −0.22279726 | −0.21014307 | −0.20575596 | 1.53 | −0.20429359 | $-7.4\times10^{-4}$ |
| 0.01 | — | — | — | 1.51 | −0.20443912 | $-8.9\times10^{-4}$ |

Con el salto, la ley $\epsilon^2$ no se cumple: sale orden 1.5, y la extrapolación $\epsilon^2$ falla en $\sim10^{-3}$. **Así como está, la opción sirve para el pozo solo como control cualitativo.** Para usarlo como control cuantitativo en la tarea 5 haría falta otro tratamiento del salto, por ejemplo la acción de pares exacta del pozo o un ajuste con $\epsilon^{3/2}$. Se lo dejo a quien verifica; no lo resolví aquí.

## 11.8 Registro de IA (implementación)

- *Consulta*: Lucho pidió, vía el flujo de agentes del 27-10-2026, implementar las tareas 2, 3 y 7.
- *Errores propios detectados y corregidos al ejecutar*:
  - (i) El primer `pares.py` tenía el desplazamiento espectral con el signo cambiado ($U$ salía $+2\epsilon(w_0^{\rm libre}-w_0^C)$ desplazada). Lo detectó la comparación con la Fase 1: $U(9,9)$ daba $+0.0939$ frente a $-0.0111$. Se corrigió antes de cualquier resultado.
  - (ii) Con $\epsilon=0.05$, el redondeo de la banda dejaba sin pareja en $h_{\rm tab}=0.005$ la última columna de la tabla Richardson (NaN). Se recorta la banda común.
  - (iii) El spline de FITPACK no extrapola: por debajo del primer nodo devolvía el valor del borde, con error $9.8\times10^{-3}$ en $r=0.005$. Se añadió la extrapolación lineal, y el error bajó a $1.7\times10^{-4}$.
- *Comprobación*: todas las cifras salen del script 11 y de `test_transferencia.py`.
- *Decisión humana pendiente*: la redefinición del control de tabulación (11.4) y el tratamiento del pozo (11.7).


## 11.9 Correcciones tras la verificación (V3, 27-10-2026)

Detalle en `fase2/verificacion/V3_respuesta_hallazgos.md`. Cambios en el código: `pares.U_extremos` con el término de Wigner-Kirkwood (H2 de V2 / H3 de V1); `transferencia.resolver` estima el sesgo de la pared en $R$ sin imagen, $\Delta E\approx-\beta\sqrt\epsilon\,u'(R)^2/2$ con $\beta=0.5826$ y $u'(R)$ tomada a $2\sqrt\epsilon$ de la pared, lo guarda como `sesgo_pared_est` y avisa (`RuntimeWarning`) cuando pasa de $\min(10^{-7},10^{-3}|E_0|)$ (H3 de V2). Comprobación: con $\delta=0.2$, $\epsilon=0.1$, el sesgo real (radial en $R+\beta\sqrt\epsilon$ menos radial en $R$) es $-1.08\times10^{-3}$, $-5.5\times10^{-7}$ en $R=5$ y 10, y la estimación da $-1.31\times10^{-3}$, $-7.2\times10^{-7}$; en $\delta=1.18$, $R=50$: $-3.22\times10^{-6}$ real frente a $-3.20\times10^{-6}$. En $R=40$ no hay aviso. Prueba `test_aviso_pared`. **No se puso imagen en $R$** (cambiaría el método aprobado; decisión del equipo). `11_transferencia_controles.py` se volvió a ejecutar: siguen pasando 28 de 35 criterios, los mismos.
