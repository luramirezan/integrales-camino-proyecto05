# Material para auditoría (parte 1 de 3)

Responde solo "Recibido" hasta la parte 3, que trae el encargo.

## Contexto

Proyecto de física teórica (curso universitario de integrales de camino). Potencial de Yukawa V(r) = −e^{−δr}/r en unidades ħ = m = g = 1, δ = μħ²/(mg); el estado 1s deja de existir en δ_c = 1.1906124210606.

## seccion_articulo.md

# Sección para el artículo: qué significa físicamente $\delta_c$

*(Generada por `E1_contexto_fisico/codigo/07_documentos.py` a partir de los JSON de `resultados/`. Figuras:
`figuras/05_mapa_delta.png`, `figuras/02_plasma_diagrama.png`, `figuras/02_plasma_energia.png`.)*

## Motivación

Todo el trabajo se hizo en unidades $\hbar = m = g = 1$, donde el único parámetro es
$\delta = \mu\hbar^2/(mg)$, con $\mu$ el inverso del alcance del apantallamiento, $m$ la masa reducida y $g$ la
intensidad del potencial. La guía del curso advierte que no se debe reclamar "una cifra universal desligada de las
unidades y parámetros". Esta sección hace lo contrario de esa cifra suelta: traduce $\delta_c = 1.1906124211$ a tres
sistemas físicos y en cada uno declara qué cantidad se mantiene fija. La condición es siempre la misma,
$\delta < \delta_c$, pero lo que dice en el laboratorio depende de cómo cambian $m$, $g$ y $\mu$ juntos.

## Método

Las tres traducciones usan la misma relación, $\delta = \mu_\text{fís}\,\hbar^2/(m\,g)$:

| sistema | $m$ (masa reducida) | $g$ | $\mu_\text{fís}$ | $\delta$ |
|---|---|---|---|---|
| hidrógeno en un plasma | $m_e$ (núcleo infinito) | $e^2/4\pi\varepsilon_0$ | $1/\lambda_D$ | $a_0/\lambda_D$ |
| materia oscura con mediador $\phi$ | $m_\chi/2$ | $\alpha\hbar c$ | $m_\phi c/\hbar$ | $2m_\phi/(\alpha m_\chi)$ |
| deuterón de juguete | $m_pm_n/(m_p+m_n)$ | $g$ (ajustada) | $m_\pi c/\hbar$ | $m_\pi/(\mu\,g/\hbar c)$ |

Cada cifra se calculó con dos métodos independientes: un disparo sin caja (`solve_ivp`, empalme de la solución
regular con la que decae) y el solucionador de caja con Richardson de la Fase 2. Para el umbral se usaron la
condición de energía cero de la Fase 2 y un Numerov propio. Coinciden a 1e-10
en $\delta_c$ y a 3e-08 en el $\delta$ del deuterón (detalles en `verificacion.md`). Los
errores numéricos son despreciables frente a las incertidumbres físicas de las entradas, que son las que se discuten.

## Resultados

**Plasma de Debye.** El 1s deja de existir cuando $\lambda_D < a_0/\delta_c = 0.8399039\,a_0 =
44.45$ pm (con la masa reducida del hidrógeno, 0.8403613 $a_0$). Es la longitud
crítica que ya daban Rogers, Graboske y Harwood en 1970 ($0.83991\,a_0$ en su resumen; nuestra cifra difiere en la
quinta decimal, ver `controles.md`). Con la longitud de Debye electrónica del NRL Plasma Formulary,
$\lambda_D = (\varepsilon_0k_BT/n_ee^2)^{1/2}$, la curva de desaparición es
$n_e = 2.798\times10^{22}\ \text{cm}^{-3}\,(k_BT/\text{eV})$ (si también apantallan los
protones a la misma temperatura, la densidad es la mitad). La figura del diagrama muestra la curva en el plano
$(n_e, T)$: a 1 eV hacen falta $n_e \approx 2.80\times10^{22}$ cm$^{-3}$; a 100 eV,
$2.80\times10^{24}$ cm$^{-3}$. La energía del 1s sube de forma continua hasta cero
(figura de energía): con $\lambda_D = a_0$ queda en -0.280 eV.

La misma figura muestra por qué esa curva hay que leerla con cuidado. Sobre ella, el número de electrones en la
esfera de Debye es $N_D = 0.0103\,(k_BT/\text{eV})$: vale 1 recién a 97 eV, y la
teoría de Debye y Hückel supone $N_D \gg 1$. A 13.6 eV el acoplamiento es $\Gamma_e = 1.24$
y $k_BT/E_F = 0.71$ (electrones parcialmente degenerados), y el radio de Wigner y Seitz es
1.9 veces la longitud de Debye. Es decir, donde el modelo estático predice que el
1s desaparece, el propio modelo deja de ser válido: el plasma no es débilmente acoplado, el apantallamiento de los
iones y la dinámica importan, y la frontera entre electrones ligados y libres deja de ser nítida. Por
eso la literatura de "descenso del continuo" (*ionization potential depression*) usa modelos que interpolan entre
Debye y la esfera iónica, como el de Stewart y Pyatt (1966), y discute todavía cuál describe los experimentos
(Crowley 2014). Nuestro $\lambda_D/a_0$ crítico es el resultado exacto **del modelo de Yukawa estático**, no una
predicción de la ionización por presión real.

**Materia oscura con mediador ligero.** Con masa reducida $m_\chi/2$ y $g = \alpha\hbar c$, hay 1s si
$\alpha m_\chi/m_\phi > 2/\delta_c = 1.679808$; los siguientes estados s aparecen en
6.4473 y 14.3420. La cifra es compatible con la literatura: Tulin, Yu y Zurek
(2013, Sec. IV B), que usan las mismas variables ($b = \alpha_X m_X/m_\phi$, masa reducida $m_X/2$), escriben que
la primera resonancia s aparece en $b = 1.68$, y explican que las resonancias de onda s corresponden a estados
ligados de energía cero. Hay que leer ese 1.68 como la etiqueta de una curva ilustrativa de su figura 3, con dos
decimales, y no como un umbral calculado con precisión: nuestro valor lo afina, no lo contradice.
La aproximación de Hulthén, muy usada en este campo porque da la amplificación de Sommerfeld en forma cerrada, pone
el primer umbral en $b = \kappa$: con $\kappa = 1.6$ (Tulin et al.) se equivoca en
-4.8% y con $\kappa = \pi^2/6$ (Feng, Kaplinghat y Yu 2010) en
-2.1%. Petraki, Postma y de Vries (2017) dan en el texto principal solo la
condición aproximada $\xi = \mu\alpha/m_\phi \gtrsim n^2$; en esa variable el umbral exacto del 1s es
$\xi > 1/\delta_c = 0.839904$. Como ejemplo: con $\alpha = 0.01$ y $m_\phi = 10$ MeV, hay
estado ligado si $m_\chi > 1.680$ GeV.
También calculamos la antirresonancia s (el cero de la longitud de dispersión entre los umbrales 1s y 2s): sale en
$b = 4.4657$, algo por debajo del $b = 4.52$ que Tulin et al. usan como ejemplo (otra curva
ilustrativa) y del $b = 4.575$ que da su fórmula de Hulthén; a velocidad finita el cero se
desplaza hacia arriba (4.518 con $v/\alpha = 0.06$), ver `controles.md`, C9.

**Deuterón de juguete.** Un único Yukawa en onda s con el alcance del pion, ajustado para que la energía de enlace
sea $B_d = 2.224566$ MeV (CODATA 2022), da con el promedio de isospin
$m_\pi = 138.0392$ MeV:
$\delta_d = 0.83046 = 0.698\,\delta_c$, $g/\hbar c = 0.3541$,
$\langle r\rangle = 3.200$ fm y $\langle r^2\rangle^{1/2} = 3.941$ fm para la
distancia entre nucleones. El radio de nucleones puntuales del modelo, $\tfrac12\langle r^2\rangle^{1/2} =
1.9706$ fm, se compara con el radio de estructura experimental $r_\text{str} = (r_d^2 - r_p^2 - r_n^2 -
3/4m_p^2)^{1/2} = 1.9756 \pm 0.0004$ fm ($r_d$ y $r_p$ de CODATA 2022 y $r_n^2 = -0.1155(17)$
fm$^2$ del PDG 2024; la incertidumbre usa la diferencia isotópica $r_d^2 - r_p^2$, porque $r_d$ y $r_p$ de CODATA
están casi totalmente correlacionados; la relación es la Ec. 2 de Filin et al. 2020, que calculan
1.9731 fm con fuerzas quirales). Las dos cantidades no son idénticas: el $r_\text{str}$ de Filin et
al. incluye, además del radio de la función de onda, operadores de carga de dos cuerpos y correcciones
relativistas, que el modelo no tiene. El acuerdo, de 0.2%, es en parte casual: la
cola $e^{-\kappa r}$, con $1/\kappa = 4.318$ fm, la impone el ajuste a $B_d$, pero sola no
basta (el límite de alcance cero da 1.527 fm): el resto lo pone el alcance del pion, y el
modelo no tiene fuerza tensorial ni onda D. Con $\pi^0$ o $\pi^\pm$ en vez
del promedio, $\delta_d$ va de 0.8249 a 0.8332.

**La lección: qué se mantiene fijo.** Si se mantienen $g$ y $\mu$ y solo se sube $m_\pi$, el deuterón se
desliga en $m_\pi^c = m_\pi\delta_c/\delta_d = 197.9$ MeV (entre
194.8 y 199.4 MeV según el pion elegido). Pero la QCD en red dice otra
cosa: NPLQCD (2013) encuentra el deuterón ligado con $B_d = 19.5(3.6)(3.1)(0.2)$ MeV a $m_\pi = 805.9$ MeV, con
bariones de 1634 MeV. Con el $g$ físico y la masa reducida de la red ($M_B/2$), ese punto tendría $\delta = 2.786 =
2.34\,\delta_c$, muy lejos de cualquier ligado. Para reproducirlo, el mismo modelo
necesita $\delta_L = 0.9212$ (entre 0.8982 y
0.9488 con la incertidumbre de $B_d$) y $g/\hbar c = 1.071$, es
decir, una intensidad 3.02 veces la física. Cerca del punto físico pasa lo mismo de forma local: a
$g$ fijo el modelo da $d\ln B_d/d\ln m_\pi = -4.76$, mientras que la teoría quiral de
Berengut et al. (2013), $K^q_\text{deut}/K^q_\pi = -0.86/0.494$, da -1.74 (entre
-2.75 y -0.83, solo con la incertidumbre de $K^q_\text{deut}$). El
modelo a $g$ fijo exagera la sensibilidad unas 2.7 veces. La comparación justa
tiene en cuenta que el $K^q_\text{deut}$ de Berengut et al. contiene también la variación de la masa del nucleón
($K^q_N = 0.048$, su Ec. 2.4): si el modelo a $g$ fijo deja variar $\mu$ igual, da
$K^q_\text{deut} = -2.07$ frente a $-0.86$, unas 2.4 veces (sin esa
variación, -2.35). En el límite quiral ($m_\pi \to 0$) el modelo a $g$ fijo se
vuelve un Coulomb y da $B_d = \mu (g/\hbar c)^2/2 = 29.4$ MeV; Epelbaum, Meißner y
Glöckle (2002) obtienen con fuerzas quirales $B_d = 9.6 \pm 1.9^{+1.8}_{-1.0}$ MeV (la misma dirección, otra
magnitud), y Beane y Savage (2002) concluyen que con las incertidumbres de entonces no se puede decir si sigue
ligado. Ninguno de los dos números del modelo a $g$ fijo, ni el $m_\pi^c$ ni el límite quiral, es una predicción.

## Discusión

El número adimensional $\delta_c$ es exacto y universal **para el potencial de Yukawa**, pero una frase como "el
deuterón se desliga si $m_\pi$ sube un 43%" no lo es: depende de
suponer que $g$ y la masa reducida no cambian con $m_\pi$, y esa suposición es falsa (la red y la teoría quiral
muestran que la fuerza nuclear entera cambia con la masa de los quarks). Lo mismo en el plasma: la curva de
desaparición del 1s es exacta para el Yukawa estático, pero cae en una región donde el apantallamiento estático de
Debye no se aplica. Donde la traducción sí funciona tal cual es en materia oscura, porque allí el Yukawa es el
modelo de partida y no una aproximación de algo más complicado: la cifra $2/\delta_c = 1.680$ es
compatible con el valor que usa la literatura ($b = 1.68$), y la aproximación de Hulthén la reproduce solo a unos
pocos por ciento.
La regla práctica que dejamos para el resto del artículo es declarar siempre qué se mantiene fijo al mover $\delta$.

## Referencias de esta sección

- F. J. Rogers, H. C. Graboske y D. J. Harwood, *Phys. Rev. A* **1**, 1577 (1970).
- J. D. Huba, *NRL Plasma Formulary* (Naval Research Laboratory, edición revisada 2004), p. 29.
- J. C. Stewart y K. D. Pyatt, *Astrophys. J.* **144**, 1203 (1966).
- B. J. B. Crowley, *High Energy Density Phys.* **13**, 84 (2014), DOI 10.1016/j.hedp.2014.04.003, arXiv:1309.1456.
- R. K. Janev, S. Zhang y J. Wang, *Matter Radiat. Extremes* **1**, 237 (2016), DOI 10.1016/j.mre.2016.10.002.
- S. Tulin, H.-B. Yu y K. M. Zurek, *Phys. Rev. D* **87**, 115007 (2013), arXiv:1302.3898.
- J. L. Feng, M. Kaplinghat y H.-B. Yu, *Phys. Rev. D* **82**, 083525 (2010), arXiv:1005.4678.
- K. Petraki, M. Postma y J. de Vries, *JHEP* **04** (2017) 077, arXiv:1611.01394.
- S. R. Beane et al. (NPLQCD), *Phys. Rev. D* **87**, 034506 (2013), arXiv:1206.5219.
- E. Epelbaum, U.-G. Meißner y W. Glöckle, *Nucl. Phys. A*, DOI 10.1016/S0375-9474(02)01393-3, arXiv:nucl-th/0207089.
- S. R. Beane y M. J. Savage, *Nucl. Phys. A*, DOI 10.1016/S0375-9474(02)01586-5, arXiv:nucl-th/0208021.
- J. C. Berengut et al., *Phys. Rev. D* **87**, 085018 (2013), DOI 10.1103/PhysRevD.87.085018, arXiv:1301.1738.
- A. A. Filin et al., *Phys. Rev. Lett.* **124**, 082501 (2020), arXiv:1911.04877.
- P. J. Mohr et al. (CODATA 2022), *Rev. Mod. Phys.* **97**, 025002 (2025); Particle Data Group, *Review of Particle
  Physics* (2025), tablas de constantes y de mesones ligeros; tabla de bariones N del PDG 2024 ($r_n^2$).


## verificacion.md

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


## fuentes.md

# Fuentes de la extensión E1 y su estado de verificación (17-11-2026)

Marcas: **[V]** verificada en la página del editor, en un índice bibliográfico con DOI (Scilit, OSTI, repositorio
institucional) o en el documento oficial; **[V-arXiv]** solo en arXiv; **[no verificada]** no la pudimos abrir.
Las búsquedas se hicieron con WebSearch y WebFetch. No pudimos usar las API de Crossref ni de arXiv (el proxy las
rechaza), así que los datos de volumen y página salen de las páginas indicadas.

## Constantes y datos

| Fuente | Estado | Qué se comprobó |
|---|---|---|
| CODATA 2022: P. J. Mohr et al., *Rev. Mod. Phys.* **97**, 025002 (2025); tabla de constantes del PDG 2025 (`pdg.lbl.gov/2025/reviews/rpp2025-rev-phys-constants.pdf`) | [V] | $m_p$ = 938.27208943(29) MeV, $m_n$ = 939.56542194(48) MeV, $m_d$ = 1875.61294500(58) MeV, $m_e$, $\hbar c$ = 197.3269804 MeV fm, $a_0$ = 0.529177210544(82) × 10⁻¹⁰ m, $\varepsilon_0$, $e$, $k_B$, Ry = 13.605693122990 eV |
| NIST, `physics.nist.gov/cuu/Constants/Table/allascii.txt` (CODATA 2022) | [V] | $r_d$ = 2.12778(27) fm, $r_p$ = 0.84075(64) fm |
| CODATA 2022, arXiv:2409.03787, Sec. II.2 | [V-arXiv] | Dato de entrada $E_B(d)$ = 2224.56640(38) keV (coincide con $m_p+m_n-m_d$, control C10) |
| Particle Data Group 2025, tabla de mesones ligeros (`rpp2025-tab-mesons-light.pdf`, espejo de KEK) | [V] | $m_{\pi^\pm}$ = 139.57039(18) MeV, $m_{\pi^0}$ = 134.9768(5) MeV |
| Particle Data Group 2024, tabla de bariones N (`ccwww.kek.jp/pdg/2024/tables/rpp2024-tab-baryons-N.pdf`) y pdgLive (`pdglive.lbl.gov/view/S017MCR`) | [V] (revisión, 17-11-2026) | $\langle r_n^2\rangle$ = −0.1155 ± 0.0017 fm² (pdgLive da el mismo valor en su edición actual) |
| A. A. Filin, V. Baru, E. Epelbaum, H. Krebs, D. Möller y P. Reinert, *Phys. Rev. Lett.* **124**, 082501 (2020), DOI 10.1103/PhysRevLett.124.082501, arXiv:1911.04877 | [V-arXiv] (DOI en arXiv) | Ec. (2): $r_\text{str}^2 = r_d^2 - r_p^2 - r_n^2 - 3/(4m_p^2)$; Ec. (9): $r_\text{str} = 1.9731^{+0.0013}_{-0.0018}$ fm; valor PDG que citan: $r_n^2 = -0.1161(22)$ fm² (no lo abrimos en el PDG) . **Revisión (R1-01, R1-02):** el $r_n^2$ = −0.1161(22) es el promedio antiguo que Filin et al. citan solo para comparar (ellos despejan $r_n^2$ = −0.106 de su Ec. 2); el PDG 2024 da −0.1155(17) fm², que es el que usamos ahora. Su $r_\text{str}$ incluye operadores de carga de dos cuerpos y correcciones relativistas, no es solo el radio de la función de onda. Citan $r_d^2 - r_p^2$ = 3.82070(31) fm² (desplazamiento isotópico, su Ec. 1), que usamos para la incertidumbre |

## Plasma

| Fuente | Estado | Qué se comprobó |
|---|---|---|
| F. J. Rogers, H. C. Graboske y D. J. Harwood, "Bound eigenstates of the static screened Coulomb potential", *Phys. Rev. A* **1**, 1577–1586 (1970), DOI 10.1103/PhysRevA.1.1577 | [V] (Scilit, resumen del editor) | El resumen da $D_0(1s) = 0.83991\,a_0/Z$ y 45 estados. Nuestro 0.8399039 difiere en la quinta decimal (C6). El resumen no menciona plasmas; habla del potencial "de Debye o de Yukawa" . Revisión: resumen releído en Scilit, "0.83991 a0/Z in agreement with certain previous studies" |
| J. D. Huba, *NRL Plasma Formulary*, NRL/PU/6790--04-477 (revisión 2004), copia en `courses.grainger.illinois.edu/ece350/PlasmaFormulary.pdf` | [V] (copia del documento, no el sitio del NRL) | p. 29: $\lambda_D = (kT/4\pi ne^2)^{1/2} = 7.43\times10^2\,(T/n)^{1/2}$ cm, $T$ en eV; p. 30: $(4\pi/3)n\lambda_D^3 = 1.72\times10^9\,T^{3/2}n^{-1/2}$. Es la longitud **de una especie** (usamos la electrónica). No da la versión con varias especies |
| J. C. Stewart y K. D. Pyatt, "Lowering of ionization potentials in plasmas", *Astrophys. J.* **144**, 1203 (1966), DOI 10.1086/148714 | [V] (Scilit) | Título, revista, volumen, página, DOI. No leímos el texto (sin resumen disponible); lo citamos solo como el modelo estándar de descenso del continuo |
| B. J. B. Crowley, "Continuum lowering: a new perspective", *High Energy Density Phys.* (2014), DOI 10.1016/j.hedp.2014.04.003, arXiv:1309.1456 | [V-arXiv] (DOI y referencia de revista en arXiv: *High Energy Density Phys.* **13**, 84–102 (2014); comprobado en la revisión) | El resumen dice que aplicar Stewart y Pyatt a la fotoionización es un error frecuente y discute la discrepancia con medidas espectroscópicas recientes |
| R. K. Janev, S. Zhang y J. Wang, "Review of quantum collision dynamics in Debye plasmas", *Matter Radiat. Extremes* **1**, 237 (2016), DOI 10.1016/j.mre.2016.10.002, arXiv:1606.00163 | [V] (DOAJ/UTM; volumen y página por la URL del PDF del editor) | Tabla 1: longitud crítica escalada del 1s, 0.839907; el modelo de Debye y Hückel se presenta para plasmas débilmente acoplados, el de esfera iónica para los fuertemente acoplados . Revisión: ese 0.839907 queda 3 ppm por encima de nuestro 0.8399039 (que confirman tres métodos); como el de Rogers et al., es menos preciso que su número de cifras. Define $D$ con $T_e$ y $n_e$ (solo electrones) |
| M. S. Murillo y J. C. Weisheit, "Dense plasmas, screened interactions, and atomic ionization", *Phys. Rep.* **302**, 1 (1998) | [no verificada] | Solo la vimos citada en Janev et al.; no la incluimos en las referencias de la sección |

## Materia oscura

| Fuente | Estado | Qué se comprobó |
|---|---|---|
| S. Tulin, H.-B. Yu y K. M. Zurek, "Beyond collisionless dark matter: particle physics dynamics for dark matter halo structure", *Phys. Rev. D* **87**, 115007 (2013), DOI 10.1103/PhysRevD.87.115007, arXiv:1302.3898 | [V] (OSTI para la revista) | Sec. III, Ec. (10): masa reducida $\mu = m_X/2$; Sec. IV A: $b \equiv \alpha_X m_X/m_\phi$; Sec. IV B: "we first see the appearance of an s-wave resonance for b=1.68" y "an s-wave antiresonance for b=4.52"; Sec. VI, Ec. (17), (24): Hulthén con $\delta = \kappa m_\phi$, $\kappa = 1.6$, resonancias en $\alpha_X m_X/(\kappa m_\phi) = n^2$, y "s-wave resonances correspond to bound states at zero energy". **Es la única fuente donde encontramos la cifra 1.68.** El artículo no tiene números de página en la versión de arXiv . **Revisión (R1-03):** 1.68 y 4.52 son etiquetas de curvas de la figura 3 (sección eficaz frente a velocidad, $\alpha_X = 10^{-2}$), no umbrales ni ceros calculados; la Sec. VI da la antirresonancia de Hulthén en $\alpha_X m_X/(\kappa m_\phi) = r^2$ con $2\gamma + \psi(1+r) + \psi(1-r) = 0$, $r \approx 1.69, 2.75, \ldots$ |
| J. L. Feng, M. Kaplinghat y H.-B. Yu, "Sommerfeld enhancements for thermal relic dark matter", *Phys. Rev. D* **82**, 083525 (2010), DOI 10.1103/PhysRevD.82.083525, arXiv:1005.4678 | [V-arXiv] (DOI en arXiv) | Ec. (6): Hulthén con la combinación $\pi^2\epsilon_\phi/6$; Ec. (7): resonancias en $m_\phi \simeq 6\alpha_X m_X/(\pi^2 n^2)$, es decir $b = \pi^2 n^2/6$ (1.645 para $n=1$). No da la cifra 1.68 |
| K. Petraki, M. Postma y J. de Vries, "Radiative bound-state-formation cross-sections for dark matter interacting via a Yukawa potential", *JHEP* **04** (2017) 077, DOI 10.1007/JHEP04(2017)077, arXiv:1611.01394 | [V-arXiv] (DOI en arXiv) | Sec. 2 (p. 6): ligado "roughly if the mediator mass is less than the inverse Bohr radius", $m_\phi \lesssim \mu\alpha$; Sec. 2.2 (p. 8): existencia $\gamma_{n\ell}(\xi) > 0$, "roughly $\xi = \mu\alpha/m_\phi \gtrsim n^2$"; Sec. 3.5: cada nivel tiene un $\xi$ mínimo. **No encontramos 1.68, 0.84 ni 1.19 en el texto leído.** El apéndice A.2 ("Bound states"), donde remiten las condiciones precisas, no lo pudimos leer: el texto que devuelven arXiv y ar5iv se corta antes |
| S. Tulin y H.-B. Yu, "Dark matter self-interactions and small scale structure", arXiv:1705.02358 | [V-arXiv], leída en parte | En la parte que pudimos leer (introducción y Sec. II) no aparece la condición de resonancia. No buscamos más |
| M. Napsuciale y S. Rodríguez, "Bound states of the Yukawa potential from hidden supersymmetry", *PTEP* **2021**, 073B03, DOI 10.1093/ptep/ptab070, arXiv:2102.07160 | [V] (página del editor) | Revista, número y DOI. El resumen visible no menciona materia oscura (solo la etiqueta de categoría) |

## Deuterón y masa del pion

| Fuente | Estado | Qué se comprobó |
|---|---|---|
| S. R. Beane et al. (NPLQCD), "Light nuclei and hypernuclei from quantum chromodynamics in the limit of SU(3) flavor symmetry", *Phys. Rev. D* **87**, 034506 (2013), DOI 10.1103/PhysRevD.87.034506, arXiv:1206.5219 | [V-arXiv] (DOI en arXiv) | Sec. III (p. 8): $m_\pi$ = 805.9(0.6)(0.4)(8.9) MeV, bariones del octete 1.634(0)(0)(18) GeV; Tabla VII (p. 11) y Sec. IV (p. 12): $B_d$ = 19.5(3.6)(3.1)(0.2) MeV; dineutrón 15.9(2.7)(2.7)(0.2) MeV. Sin electromagnetismo, una sola separación de red . Revisión: cifras releídas en el PDF de arXiv; separación de red 0.1453(16) fm |
| E. Epelbaum, U.-G. Meißner y W. Glöckle, "Nuclear forces in the chiral limit", *Nucl. Phys. A*, DOI 10.1016/S0375-9474(02)01393-3, arXiv:nucl-th/0207089 | [V-arXiv] | Resumen: en el límite quiral "no hay nuevos estados ligados" y $B_D^{CL} = 9.6 \pm 1.9^{+1.8}_{-1.0}$ MeV. Volumen y página no comprobados |
| S. R. Beane y M. J. Savage, "The quark-mass dependence of two-nucleon systems", *Nucl. Phys. A*, DOI 10.1016/S0375-9474(02)01586-5, arXiv:nucl-th/0208021 | [V-arXiv] | Resumen: con las incertidumbres actuales "it is unclear whether the deuteron is bound or unbound in the chiral limit". Volumen y página no comprobados |
| J. C. Berengut, E. Epelbaum, V. V. Flambaum, C. Hanhart, U.-G. Meißner, J. Nebreda y J. R. Peláez, "Varying the light quark mass: impact on the nuclear force and Big Bang nucleosynthesis", *Phys. Rev. D* **87**, 085018 (2013), DOI 10.1103/PhysRevD.87.085018, arXiv:1301.1738 | [V] revista y número (repositorio UCM); número de artículo 085018 por el DOI que da arXiv (revisión) | Ec. (3.14): $K^q_\text{deut} = (\delta E_\text{deut}/\delta m_q)/(E_\text{deut}/m_q)$; Ec. (4.1): $K^q_\text{deut} = -0.86^{+0.45}_{-0.50}$; Tabla I: $K^q_\pi = 0.494^{+0.009}_{-0.013}$; "the deuteron is found to remain bound for all values of the quark masses considered". El cociente $-0.86/0.494$ es cuenta nuestra . Revisión: Ec. (2.4) $K^q_N = 0.048^{+0.002}_{-0.006}$; el texto dice que la dependencia de $E_\text{deut}$ "emerges from both the nucleon mass entering the NN Green's function and the potential", es decir, $K^q_\text{deut}$ incluye la variación de la masa del nucleón |

## Fuentes que la revisión adversarial consultó y no se citan en la sección

- "Critical parameters and spherical confinement of H atom in screened Coulomb potential", arXiv:1904.11166 (leída en arXiv; autores no anotados): cita a Gomes et al. con $\delta_c(1s) = 1.19061227 \pm 4\times10^{-8}$,
  1.5e-07 por debajo del nuestro (más que su barra). No abrimos Gomes et al.; nuestro valor lo confirman tres métodos
  independientes a 1e-10, así que no lo usamos [no verificada la fuente primaria].

## Cifras que sacamos de la propuesta y corregimos o confirmamos

- La propuesta (`ideas_fase4_y_final.md`, nota *) decía que no se había comprobado que 1.680 apareciera en Petraki
  et al. Confirmamos que **no aparece en el texto principal** de Petraki et al. y que **sí aparece como 1.68 en Tulin,
  Yu y Zurek (2013)**.
- La propuesta marcaba Petraki et al. y NPLQCD como [V]; nosotros solo los abrimos en arXiv (con DOI), así que aquí
  quedan [V-arXiv].
- La propuesta daba $\delta_d = 0.830$, $g/\hbar c = 0.354$ y $m_\pi^c \approx 198$ MeV; con masas verificadas y la
  masa reducida exacta se confirman (ver `verificacion.md`).

