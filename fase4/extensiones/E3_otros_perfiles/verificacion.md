# Verificación de E3 (generado por `codigo/09_textos.py` desde los JSON)

## Comprobaciones independientes

1. **Tres métodos para $\delta_c$.** (A) energía cero con DOP853 y brentq sobre $1/a$; (B) raíz de un ajuste de $\kappa(\delta)$
   obtenido de energías de ligado, sin usar energía cero; (C) fase variable para $1/a$ (Calogero), $db/dr=-2V(1-rb)^2$, integrada
   con LSODA. Diferencias A frente a C: Yukawa $1.9\times10^{-12}$, ECSC $1.1\times10^{-12}$, Hulthén $3.1\times10^{-12}$, átomo H estático $2.8\times10^{-12}$. A frente a B (variante
   cercana al umbral): Yukawa $-7.8\times10^{-15}$, ECSC $-7.1\times10^{-12}$, Hulthén $-2.4\times10^{-15}$, átomo H estático $3.1\times10^{-15}$. Estabilidad de A ante $r_f$ y la
   tolerancia: máximo $2.0\times10^{-12}$.
2. **Casos exactos.** Hulthén: $\delta_c=2$ ($-1.3\times10^{-14}$); $\kappa=1-\delta/2$ ($2.4\times10^{-14}$);
   $a(\delta)$ con la función digamma, $a=\delta^{-1}[2\gamma+\psi(1+\sqrt{2/\delta})+\psi(1-\sqrt{2/\delta})]$, deducida aquí
   (error relativo máximo $7.4\times10^{-11}$); $\langle r\rangle=(12-\delta^2)/(2(4-\delta^2))$ en $\delta$ = 1.0, 1.5 y 1.9
   (máximo $5.5\times10^{-13}$); integral de camino en $\delta=1.8$ ($-2.4\times10^{-9}$ con barra
   $7.5\times10^{-8}$). En el umbral $r_e=1.500000000$ y el polo virtual sale en $\kappa_v=\delta/2-1$ ($9.1\times10^{-10}$).
   Las dos cosas son exactas (revisión R3): $u=(1-e^{-\delta r})e^{-\kappa r}$ con $\kappa=1-\delta/2$ resuelve la ecuación para todo $\delta$.
   Para $\delta>2$ es la solución pura $e^{+|\kappa|r}$, es decir, el polo virtual. En $\delta=2$, $\varphi_0=1-e^{-2r}$ y
   $r_e=2\int(2e^{-2r}-e^{-4r})dr=3/2=3/\delta_c$.
3. **Dos caminos para $c$, $a$ y $r_e$.** $c$ por Hellmann–Feynman frente a diferencias centradas con Richardson: máximo
   $1.2\times10^{-11}$ relativo. $1/a$ y $r_e$ de la energía cero frente a desfasajes:
   el primer diseño del ajuste (k hasta $0.1\delta$, grado 3) **no pasa** el criterio de $10^{-9}$ en $1/a$
   (máximo $1.3\times10^{-9}$) por truncación del polinomio; con
   $k\le0.05\delta$ y grado 4 las diferencias bajan a $4.4\times10^{-14}$
   y $1.1\times10^{-9}$. Tercer camino: el ajuste a energías de
   caja da $1/a$ y $r_e$ coherentes (control K4).
4. **Disparo frente a métodos con malla.** Frente al radial de la Fase 3 (Yukawa, 13 valores de $\delta$ con $R\ge25/\kappa$):
   máximo $6.6\times10^{-9}$, dentro del error de malla del radial. Frente al radial de la Fase 2 en $R=200$ y
   $\delta_c$: máximo $6.3\times10^{-9}$.
5. **Integral de camino.** La celda de Yukawa ($\delta=1.18$, $R=200$) reproduce la de la Fase 3, $-2.4076630903\times10^{-5}$, y el
   autovalor crudo coincide bit a bit con `comun3.resolver_tr`. Las barras de la receta son conservadoras: el desvío real frente al
   disparo es de 0.010 a 0.61 barras.

## Lo que encontramos al releer el código

- **Error real corregido (17-11-2026).** El control V3 falló en la primera corrida: $\langle r\rangle$ del Hulthén en $\delta=1$
  salía mal en el segundo decimal (esa primera salida no se conservó). Causa: para estados profundos ($\kappa r_f=30$) la integración hacia afuera amplifica el redondeo como
  $e^{\kappa r_f}$ y contamina la función de onda cerca de $r_f$ (el autovalor no se ve afectado, porque la condición de empalme
  está bien condicionada). Se corrigió en `perfiles._observables_ligado`: si $\kappa r_f>10$, integración hacia adentro de la
  solución decreciente y empalme en $r_m=\min(r_f/2,4/\kappa)$. Cerca del umbral ($\kappa r_f\le10$) nada cambia. Todo se volvió a
  correr después de la corrección.
- **Desbordes.** Al buscar $E_0$ en cajas grandes o $\kappa$ de estados profundos, la solución creciente desborda (avisos de
  numpy). Se trata como signo positivo (`caja`) o se acorta $r_f$ a $600/\kappa$ sin bajar de $40/\delta$ (`ligado`); se
  descartan valores no finitos al buscar cambios de signo.
- **Arranque.** La serie de Frobenius usa $u=r-r^2+c_3r^3$ con $c_3=(2+2W(0)-2E)/6$; el tramo $[0,r_0]$ aporta $2r_0$ a $r_e$ y se
  suma. Cambiar $r_0$ de $10^{-6}$ a $10^{-7}$ movió $r_e$ del Hulthén en el orden de $10^{-12}$ (prueba interactiva durante el desarrollo, sin JSON).
- **Sesgo de pared.** A diferencia de la Fase 3 se estimó con el disparo en $R+0.5826\sqrt\epsilon$ en lugar del radial con
  $h=1/40$; en la celda de Yukawa es la parte dominante de la barra.
- **Criterios añadidos después.** U2b y S1b se añadieron tras ver los fallos de U2 y S1 y se marcan "(posterior)" en `controles.md`;
  no cambian los veredictos originales.
- **Tiempos** (un proceso, `OMP_NUM_THREADS=1`):

```
01_umbrales 66 s
02_dispersion 14 s
03_ligados_virtuales 118 s
03b_curvas_E 381 s
04_cajas_universalidad 340 s
05_transferencia_ecsc 122 s
07_verificacion 35 s
06_figuras 3 s
08_tabla_controles 0 s
02_dispersion (re-ejecutado tras añadir el dato e-H) Tue Nov 17 21:48:45 UTC 2026
```
