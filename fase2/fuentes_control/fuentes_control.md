# Fuentes para los potenciales de control: Hulthén y pozo esférico cuadrado

**Proyecto 05 · Fase 2 · preparado el 26-10-2026 a pedido del profesor (después de la presentación de la Fase 1).**

**Qué pidió el profesor.** Fuentes para los dos potenciales de control que usamos en la sección 0.6 de la Fase 1: Hulthén y pozo esférico cuadrado. En la bitácora de la Fase 1 esos dos modelos aparecen resueltos por nosotros, pero sin ninguna referencia bibliográfica. Este archivo las añade.

**Cómo se verificó.** Cada referencia marcada **VERIFICADA** se contrastó hoy (26-10-2026) en la página del editor (APS) o en el PDF de arXiv: autores, título, revista, volumen, página y año, y el resumen. Lo que solo consta porque otros artículos lo citan se marca **CITA SECUNDARIA**. Lo que viene de memoria se marca **NO VERIFICADA**. Igual que en la Fase 1, no se usa Wikipedia.

**Sobre "descargar".** Desde el entorno de Claude no se pudo bajar ningún PDF: el proxy de red bloquea arXiv y Crossref (tanto en la nube como en la máquina virtual del computador de Lucho). Los artículos se leyeron con la herramienta de consulta web. Para tener los PDF en el computador está el script [`descargar_fuentes.ps1`](descargar_fuentes.ps1), que baja los nueve de acceso abierto (arXiv). Los de APS (Phys. Rev. A, Rev. Mod. Phys.) son de pago: hay que bajarlos con el acceso de la biblioteca de la universidad.

---

## 1. Tabla resumen

### Hulthén

| # | Referencia | Enlace | Qué aporta | Estado |
|---|---|---|---|---|
| H1 | Cai, J. M., Cai, P. Y., Inomata, A., *Path-integral treatment of the Hulthén potential*, Phys. Rev. A **34**(6), 4621 (1986) | doi:10.1103/PhysRevA.34.4621 | **Solución exacta de Hulthén con integral de camino.** Cambio de variable y reescalamiento local del tiempo, luego extensión dimensional a SU(2). Energías por los polos de la función de Green, funciones de onda $s$ normalizadas por los residuos. Discute los límites Yukawa y Coulomb | VERIFICADA (APS, resumen). Pago |
| H2 | Varshni, Y. P., *Eigenenergies and oscillator strengths for the Hulthén potential*, Phys. Rev. A **41**(9), 4682 (1990) | doi:10.1103/PhysRevA.41.4682 | Energías exactas e integración numérica; **parámetro de apantallamiento crítico para varios $l$ con $n\le10$**; variacional de un parámetro que falla en apantallamiento alto | VERIFICADA (APS, resumen). Pago |
| H3 | Stubbins, C., *Bound states of the Hulthén and Yukawa potentials*, Phys. Rev. A **48**(1), 220 (1993) | doi:10.1103/PhysRevA.48.220 | Método variacional generalizado para **Hulthén y Yukawa a la vez**, estados hasta $n=6$, en un rango amplio de apantallamiento | VERIFICADA (APS, resumen). Pago |
| H4 | Hulthén, L., Laurikainen, K. V., *Approximate eigensolutions of $d^2\varphi/dx^2+[a+b(e^{-x}/x)]\varphi=0$*, Rev. Mod. Phys. **23**(1), 1 (1951) | doi:10.1103/RevModPhys.23.1 | El propio Hulthén usando su potencial para aproximar **la ecuación del Yukawa** ($e^{-x}/x$). Es el origen histórico de "Hulthén como control del Yukawa" | VERIFICADA (APS, metadatos; la página no trae resumen). Pago |
| H5 | Hulthén, L., Ark. Mat. Astron. Fys. **28A**, no. 5 (1942); **29B**, no. 1 (1942) | n/d | Artículos originales donde se introduce el potencial | CITA SECUNDARIA (la citan igual H8, H9 y Mancini et al. 2014, Braz. J. Phys. 44, 305, doi:10.1007/s13538-014-0215-9). No se vio el original |
| H6 | Flügge, S., *Practical Quantum Mechanics*, Springer, Berlín (1974) | libro | Libro de problemas con la solución exacta del estado $s$ de Hulthén | CITA SECUNDARIA (citado por H8 y H9). Que sea el problema 67 es de memoria: NO VERIFICADO |
| H7 | Lam, C. S., Varshni, Y. P., *Energies of s eigenstates in a static screened Coulomb potential*, Phys. Rev. A **4**(5), 1875 (1971) | doi:10.1103/PhysRevA.4.1875 | Yukawa $1s$ a $4s$ por perturbaciones y variacional; coincide con Rogers et al. (ref. 3 de la Fase 1) **salvo muy cerca del apantallamiento crítico**. Muestra que los métodos aproximados fallan justo donde nos interesa | VERIFICADA (APS, resumen). Pago |
| H8 | Gönül, B., Özer, O., Cançelik, Y., Koçak, M., *Hamiltonian hierarchy and the Hulthén potential*, Phys. Lett. A **275**, 238 (2000) | arXiv:nucl-th/0106002 | Supersimetría aplicada a Hulthén. Da $E_n=-\frac{me^4}{2\hbar^2}\left[\frac1{n+1}-\frac{(n+1)\beta}{2}\right]^2$, $\beta=\hbar^2\delta/(me^2)$, $n=0,1,\dots$ (estados $s$) | VERIFICADA (PDF de arXiv; revista según el propio PDF). **Abierto** |
| H9 | Roy, A. K., *The generalized pseudospectral approach to the bound states of Hulthén and Yukawa potentials* | arXiv:1312.5900 | 55 estados con $n\le10$ de Hulthén y Yukawa con 13 a 14 cifras. Confirma umbrales exactos de Hulthén $\delta_c(1s)=2$, $\delta_c(2s)=0.5$ y cita para Yukawa $1s$ $\lambda_c=1.19061227\pm4\times10^{-8}$ | VERIFICADA (PDF de arXiv). Revista NO confirmada (arXiv no dejó abrir la página de resumen). **Abierto** |
| H10 | Roy, A. K., *Spherical confinement of Coulombic systems inside an impenetrable box: H atom and the Hulthén potential* | arXiv:1802.04373 | **Hulthén dentro de una caja esférica de paredes duras**: es justo nuestro problema del sesgo de caja de Dirichlet (Fase 1, sección 6, apartado 2(c)). Energías del Hulthén confinado para varios radios | VERIFICADA (ar5iv). Revista NO confirmada. **Abierto** |

### Pozo esférico cuadrado

| # | Referencia | Enlace | Qué aporta | Estado |
|---|---|---|---|---|
| P1 | Jugdutt, B. A., Marsiglio, F., *Solving for three-dimensional central potentials using matrix mechanics* (2013) | arXiv:1211.5236 | Usa **el pozo esférico finito como prueba**, incluida la profundidad crítica (extrapola $V_{0c}=1/4$ en unidades de $(\hbar\pi)^2/(2m b^2)$, "the well known analytical result"), y luego aplica el mismo método a Coulomb y **Yukawa** ($\mu_c\approx1.1906$). Es exactamente el esquema "control exacto, luego Yukawa" | VERIFICADA (PDF de arXiv). Revista NO confirmada. **Abierto**. *Por comprobar en el PDF:* que $b$ sea el radio del pozo, en cuyo caso $V_{0c}=\pi^2\hbar^2/(8mb^2)$, igual a nuestro $\lambda_c=\pi^2/8$ |
| P2 | Branson, J., *Bound States in a Spherical Potential Well*, apuntes de Physics 130A, UC San Diego | quantummechanics.ucsd.edu/ph130a/130_notes/node227.html | Deducción estándar: $j_l$ dentro, $h_l^{(1)}$ fuera; para $l=0$ la condición de empalme $k\cot ka=-\kappa$, la misma de nuestra 0.6.3 | VERIFICADA (página web). La página no deduce explícitamente la profundidad mínima |
| P3 | Daboul, J., Nieto, M. M., *Quantum bound states with zero binding energy* | arXiv:hep-th/9405154 | Estados de energía cero. Dice que "en general las soluciones $E=0$ del pozo esférico no son normalizables" y que solo con $l\ge1$ (en 3D) hay ligado de energía cero. Respalda que en el umbral $s$ el estado se deslocaliza (halo, $\langle r\rangle\to\infty$), que es lo que mide nuestro criterio | VERIFICADA (PDF de arXiv). Revista NO confirmada |
| P4 | Landau, L. D., Lifshitz, E. M., *Quantum Mechanics (Non-relativistic Theory)*, §33 (pozo esférico) | libro | Fuente de texto clásica de la condición $V_0a^2>\pi^2\hbar^2/(8m)$ | NO VERIFICADA (de memoria; hay que mirar el libro en la biblioteca). Alternativa: Sakurai y Napolitano, *Modern Quantum Mechanics*, capítulo de potenciales centrales, también NO VERIFICADA |

### Técnicas de integral de camino útiles para los controles

| # | Referencia | Enlace | Qué aporta | Estado |
|---|---|---|---|---|
| PI1 | Kole, J. S., De Raedt, H., *Quantum Monte Carlo method for attractive Coulomb potentials* | arXiv:physics/0102015 | El Monte Carlo de integral de camino estándar falla con $-1/r$ porque los caminos caen al origen. Proponen una cota inferior exacta del propagador (desigualdad de Jensen) que **suaviza la singularidad** con un potencial efectivo. Prueban con hidrógeno y helio | VERIFICADA (ar5iv). Revista NO confirmada |
| PI2 | Myrheim, J., *Numerical path integration with Coulomb potential* | arXiv:physics/0306168 | Promedio gaussiano del potencial: Coulomb pasa a Coulomb $\times\,\mathrm{erf}(r/\sqrt2\sigma)$, finito en el origen. Hidrógeno con $-13.50\pm0.07$ eV frente a $-13.598$; "unos 50 pasos de tiempo bastan para muchos fines" | VERIFICADA (PDF de arXiv). Revista NO confirmada |
| PI3 | Dluhy, P., Gangopadhyaya, A., *Sharp and infinite boundaries in the path integral formalism* (2011) | arXiv:1112.3674 | Paredes infinitas en la integral de camino con el método de imágenes. Sirve para la caja de Dirichlet de radio $R$. **No** trata escalones finitos como el borde del pozo cuadrado | VERIFICADA (PDF de arXiv) |
| Y1 | del Valle, J. C., Nader, D. J., *Towards the theory of the Yukawa potential* (2018) | arXiv:1807.11898 | Es la ref. 12 de la Fase 1 ("del Valle y Nader 2018"), que estaba NO VERIFICADA. Da apantallamientos críticos y los primeros coeficientes de $E(\delta)$ cerca del umbral, por perturbaciones con Padé, malla de Lagrange y variacional | Existencia, autores y contenido VERIFICADOS (PDF de arXiv). Revista NO confirmada. Su valor de $\delta_c$ no se leyó todavía |

---

## 2. Qué dicen, en corto, y para qué nos sirven

### 2.1 Hulthén

**La fórmula general.** En nuestras unidades ($\hbar=m=g=1$, $V_H=-\delta/(e^{\delta r}-1)$) los estados $s$ son exactos:
$$E_n=-\frac12\left(\frac1n-\frac{n\delta}{2}\right)^2,\qquad \kappa_n=\frac1n-\frac{n\delta}2,\qquad \delta_c(ns)=\frac{2}{n^2}.$$
Coincide con H8 (cambiando $n+1\to n$ y $\beta\to\delta$) y con los umbrales $2$ y $0.5$ de H9. Para $n=1$ es nuestra 0.6.1.

**Cerramos un cabo suelto de la Fase 1.** En 0.6.1 el estado $2s$ solo se había comprobado numéricamente en $\delta=0.1$. Ahora [`verificacion_hulthen_2s.py`](verificacion_hulthen_2s.py) lo comprueba con sympy para todo $\delta$: con $u=(1-e^{-\delta r})(1+Ae^{-\delta r})e^{-\kappa_2r}$ el residuo se anula idénticamente si y solo si
$$A=\frac{1+\delta}{\delta-1},$$
que en $\delta=0.1$ da $-1.2222\ldots$, el valor de la Fase 1. El script también da $\delta_c(ns)=2/n^2$.

**Por qué es el control correcto para la Fase 2 (el argumento para el profesor).**
1. *Mismo comportamiento en los dos extremos*: $-1/r$ en el origen y $e^{-\delta r}$ lejos. Hulthén y Laurikainen (H4) ya lo usaban en 1951 para aproximar la ecuación del Yukawa.
2. *Es exacto dentro de la propia integral de camino* (H1). No solo tiene solución exacta en la ecuación de Schrödinger: Cai, Cai e Inomata obtienen su función de Green por integral de camino y discuten los límites Yukawa y Coulomb. Eso nos da una referencia teórica para el mismo formalismo que vamos a programar.
3. *Tiene umbral exacto*, $\delta_c=2$, y valores exactos de $E_0$ y $\langle r\rangle$ cerca de él. Coulomb ($\delta=0$) no prueba nada cerca del umbral; Hulthén sí.
4. *Se usa en la literatura como pareja del Yukawa* (H3, H9): los mismos métodos se prueban en los dos.
5. *Caja finita*: H10 resuelve Hulthén dentro de una esfera de paredes duras. Podemos comparar nuestro sesgo de caja con esos números.

**Advertencia de la literatura.** H2 y H7 muestran que los métodos aproximados (variacional de un parámetro, perturbaciones) coinciden bien lejos del umbral y fallan cerca de él. Es el mismo aviso de nuestra Fase 1: cerca del umbral la longitud de decaimiento diverge y la caja y la discretización pesan más.

### 2.2 Pozo esférico cuadrado

**El resultado.** Dentro $u=\sin kr$, fuera $u\propto e^{-\kappa r}$, empalme $k\cot kR=-\kappa$ (P2). En el umbral $\kappa=0$, así que $kR=\pi/2$ y $V_0R^2=\pi^2/8$ (en $\hbar=m=1$), como en nuestra 0.6.3. P1 llega al mismo umbral numéricamente con el mismo método que luego usa para Yukawa.

**Para qué sirve como control y en qué se diferencia de Hulthén.**
- *No tiene singularidad en el origen.* Separa dos problemas: si el algoritmo falla con Hulthén y no con el pozo, el problema es la singularidad $-1/r$ (que PI1 y PI2 tratan con potenciales suavizados). Si falla con los dos, el problema es la detección del umbral o la caja.
- *Tiene un salto en $r=R$.* Ese borde es lo contrario de Hulthén: no hay singularidad, pero el potencial es discontinuo. Es razonable esperar que la discretización del tiempo converja más lento que con un potencial suave; no encontramos todavía una fuente que dé el orden exacto, así que **queda como algo a medir, no a afirmar**.
- *Umbral sin halo normalizable* (P3): en $l=0$ la solución de energía cero no es normalizable, así que justo en el umbral el estado se escapa al infinito. Es la prueba más limpia de nuestro criterio de enlace con varias cajas y $\langle r\rangle$.

---

## 3. Qué falta y propuestas

1. Bajar los PDF de pago (H1, H2, H3, H4, H7) con la biblioteca. **H1 es el más importante** para la Fase 2.
2. Confirmar la revista de H9, H10, P1, P3, PI1, PI2 y Y1 en la página de arXiv o en Crossref (desde aquí arXiv limitó las consultas y Crossref está bloqueado).
3. Leer en Y1 su $\delta_c$ y, si coincide con $1.19061242106$, pasar la ref. 12 de la Fase 1 a VERIFICADA.
4. Revisar P4 en el libro antes de citarlo.
5. Añadir a `06_fuentes.md` (o a la sección de fuentes de la Fase 2) las filas H1 a H10, P1 a P4 y PI1 a PI3, y una línea en 0.6.1 que cite la nueva comprobación del $2s$.

---

## 4. BibTeX

```bibtex
@article{Cai1986, author={Cai, J. M. and Cai, P. Y. and Inomata, A.},
  title={Path-integral treatment of the {H}ulth{\'e}n potential}, journal={Phys. Rev. A},
  volume={34}, number={6}, pages={4621}, year={1986}, doi={10.1103/PhysRevA.34.4621}}
@article{Varshni1990, author={Varshni, Y. P.}, title={Eigenenergies and oscillator strengths for the {H}ulth{\'e}n potential},
  journal={Phys. Rev. A}, volume={41}, number={9}, pages={4682}, year={1990}, doi={10.1103/PhysRevA.41.4682}}
@article{Stubbins1993, author={Stubbins, Calvin}, title={Bound states of the {H}ulth{\'e}n and {Y}ukawa potentials},
  journal={Phys. Rev. A}, volume={48}, number={1}, pages={220}, year={1993}, doi={10.1103/PhysRevA.48.220}}
@article{HulthenLaurikainen1951, author={Hulth{\'e}n, Lamek and Laurikainen, K. V.},
  title={Approximate eigensolutions of $d^2\varphi/dx^2+[a+b(e^{-x}/x)]\varphi=0$}, journal={Rev. Mod. Phys.},
  volume={23}, number={1}, pages={1}, year={1951}, doi={10.1103/RevModPhys.23.1}}
@article{Hulthen1942, author={Hulth{\'e}n, L.}, journal={Ark. Mat. Astron. Fys.}, volume={28A}, number={5}, year={1942},
  note={y 29B, no. 1 (1942). Cita secundaria, no vista en el original}}
@book{Flugge1974, author={Fl{\"u}gge, S.}, title={Practical Quantum Mechanics}, publisher={Springer}, address={Berlin}, year={1974}}
@article{LamVarshni1971, author={Lam, C. S. and Varshni, Y. P.}, title={Energies of s eigenstates in a static screened {C}oulomb potential},
  journal={Phys. Rev. A}, volume={4}, number={5}, pages={1875}, year={1971}, doi={10.1103/PhysRevA.4.1875}}
@article{Gonul2000, author={G{\"o}n{\"u}l, B. and {\"O}zer, O. and Can{\c{c}}elik, Y. and Ko{\c{c}}ak, M.},
  title={Hamiltonian hierarchy and the {H}ulth{\'e}n potential}, journal={Phys. Lett. A}, volume={275}, pages={238}, year={2000},
  eprint={nucl-th/0106002}}
@misc{RoyGPS, author={Roy, Amlan K.}, title={The generalized pseudospectral approach to the bound states of {H}ulth{\'e}n and {Y}ukawa potentials},
  eprint={1312.5900}, archivePrefix={arXiv}}
@misc{RoyConfined, author={Roy, Amlan K.}, title={Spherical confinement of {C}oulombic systems inside an impenetrable box: {H} atom and the {H}ulth{\'e}n potential},
  eprint={1802.04373}, archivePrefix={arXiv}}
@misc{Jugdutt2013, author={Jugdutt, B. A. and Marsiglio, F.}, title={Solving for three-dimensional central potentials using matrix mechanics},
  year={2013}, eprint={1211.5236}, archivePrefix={arXiv}}
@misc{DaboulNieto, author={Daboul, Jamil and Nieto, Michael Martin}, title={Quantum bound states with zero binding energy},
  eprint={hep-th/9405154}, archivePrefix={arXiv}}
@misc{KoleDeRaedt, author={Kole, J. S. and De Raedt, H.}, title={Quantum {M}onte {C}arlo method for attractive {C}oulomb potentials},
  eprint={physics/0102015}, archivePrefix={arXiv}}
@misc{Myrheim, author={Myrheim, Jan}, title={Numerical path integration with {C}oulomb potential}, eprint={physics/0306168}, archivePrefix={arXiv}}
@misc{Dluhy2011, author={Dluhy, Phillip and Gangopadhyaya, Asim}, title={Sharp and infinite boundaries in the path integral formalism},
  year={2011}, eprint={1112.3674}, archivePrefix={arXiv}}
@misc{delValleNader2018, author={del Valle, J. C. and Nader, D. J.}, title={Towards the theory of the {Y}ukawa potential},
  year={2018}, eprint={1807.11898}, archivePrefix={arXiv}}
```

## Registro de IA de esta búsqueda

| Campo | Valor |
|---|---|
| Fecha | 26-10-2026 |
| Consulta | Lucho: "descargar esa base" de fuentes para los potenciales de control (Hulthén y pozo esférico cuadrado) que pidió el profesor |
| IA | Claude (Anthropic), con búsqueda web y lectura de páginas de APS y arXiv |
| Respuesta utilizada | Este archivo, `verificacion_hulthen_2s.py` y `descargar_fuentes.ps1` |
| Comprobación | Metadatos y resúmenes leídos en la fuente (APS o arXiv) el mismo día; estado de cada uno en las tablas. El $2s$ de Hulthén, con sympy (residuo 0) |
| Decisión humana | Pendiente de revisión por el equipo |
| Limitaciones | No se pudieron descargar PDF desde el entorno de la IA. Lo que se dice de cada artículo sale de su resumen o de una lectura automática del PDF, no de una lectura completa; antes de citar un número concreto, verificarlo en el PDF |
