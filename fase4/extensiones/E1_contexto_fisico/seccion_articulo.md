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
