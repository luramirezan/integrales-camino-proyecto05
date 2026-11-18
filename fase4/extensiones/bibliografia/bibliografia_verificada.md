# Bibliografía verificada del proyecto (umbral de enlace del Yukawa)

**Fecha de la verificación:** 17-11-2026. **Quién:** agente verificador de bibliografía (Claude).

**Método.** Cada referencia se comprobó en al menos una fuente primaria o en un índice bibliográfico:
la API de Crossref (`api.crossref.org/works`), la API de INSPIRE-HEP (`inspirehep.net/api/literature`), las páginas
de resumen de APS (`journals.aps.org/.../abstract/...`), Springer, OUP (redirección del DOI), arXiv/ar5iv, Scilit,
Open Library y el PDF publicado alojado en INSPIRE. Desde el contenedor, curl no llegaba a ninguno de estos sitios
y APS rechazaba WebFetch, así que las consultas a Crossref, INSPIRE y APS se hicieron abriéndolas en Chrome
(solo lectura, en una pestaña nueva). Wikipedia no se usó.

**Marcas** (regla 8 de `CONTEXTO_COMUN.md`):
- **[V]**: autores, título, revista, volumen, página o número de artículo, año y DOI confirmados en el editor, en el
  DOI o en un índice con DOI (Crossref, INSPIRE).
- **[V-arXiv]**: solo existe la versión de arXiv; se confirmaron sus metadatos allí (y que ni INSPIRE ni Crossref
  registran una publicación).
- **[V-doc]**: documento oficial que no es un artículo (tabla de constantes, formulario), abierto en la URL indicada.
- **[no verificada]**: no se pudo confirmar. **No debe citarse en el artículo final.**

En la columna "Qué se comprobó", **"metadatos"** son los datos bibliográficos. Cuando además se leyó el contenido
(resumen, ecuación o tabla) se dice qué afirmación concreta se comprobó. Cuando la afirmación la comprobó otro agente
(E1, E2, E4) y yo no la volví a leer, se indica "afirmación: según E*".

Resumen: **86 entradas**. **75 [V]**, **5 [V-arXiv]**, **4 [V-doc]** y **2 [no verificada]**
(Debye–Hückel 1923 y la tabla de bariones del PDG 2024 para $r_n^2$). Las erratas encontradas en los documentos del
proyecto están en `discrepancias.md`; el BibTeX de todas las entradas citables está en `referencias.bib`.

---

## A. Valor de $\delta_c$ y espectro del Yukawa

| Clave | Referencia completa | Estado | Qué se comprobó | Enlace usado |
|---|---|---|---|---|
| Yukawa1935 | H. Yukawa, "On the Interaction of Elementary Particles. I", *Proc. Phys.-Math. Soc. Japan* **17**, 48–57 (1935); reimpreso en *Prog. Theor. Phys. Suppl.* **1**, 1–10 (1955), doi:10.1143/PTPS.1.1 | [V] | Metadatos de las dos versiones (INSPIRE 32148; Crossref, solo la reimpresión de 1955). El DOI es el de la reimpresión; la versión de 1935 no tiene DOI en Crossref | inspirehep.net/api/literature?q=…Yukawa…1935 ; api.crossref.org (10.1143/ptps.1.1) |
| Rogers1970 | F. J. Rogers, H. C. Graboske, Jr. y D. J. Harwood, "Bound Eigenstates of the Static Screened Coulomb Potential", *Phys. Rev. A* **1**(6), 1577–1586 (1970), doi:10.1103/PhysRevA.1.1577 | [V] | Metadatos (APS, Crossref). **Afirmación:** el resumen da $D_0 = 0.83991\,a_0/Z$ para el estado fundamental del potencial "de Debye o de Yukawa" ($1/0.83991 = 1.19060$) y 45 estados calculados. Así queda verificada la cifra 0.83991, que la Fase 1 marcaba como no verificada | journals.aps.org/pra/abstract/10.1103/PhysRevA.1.1577 |
| LamVarshni1971 | C. S. Lam y Y. P. Varshni, "Energies of $s$ Eigenstates in a Static Screened Coulomb Potential", *Phys. Rev. A* **4**(5), 1875–1881 (1971), doi:10.1103/PhysRevA.4.1875 | [V] | Metadatos (Crossref, Scilit). No se leyó el texto. La afirmación del borrador de que "los métodos aproximados fallan cerca de $\delta_c$" no se comprobó en el artículo | scilit.com/publications/a8c066fc77a217702efda164473f92d5 ; Crossref |
| Varshni1990 | Y. P. Varshni, "Eigenenergies and oscillator strengths for the Hulthén potential", *Phys. Rev. A* **41**(9), 4682–4689 (1990), doi:10.1103/PhysRevA.41.4682 | [V] | Metadatos (Crossref, OUCI). **Ojo:** el artículo trata el potencial de **Hulthén**, no el de Yukawa (ver `discrepancias.md`, D9) | ouci.dntb.gov.ua/works/4YYxxy64 ; Crossref |
| Stubbins1993 | C. Stubbins, "Bound states of the Hulthén and Yukawa potentials", *Phys. Rev. A* **48**(1), 220 (1993), doi:10.1103/PhysRevA.48.220 | [V] | Metadatos y resumen (APS): método variacional generalizado con combinación lineal de funciones, energías de Yukawa y Hulthén para $n\le6$ | journals.aps.org/pra/abstract/10.1103/PhysRevA.48.220 |
| Gomes1994 | O. A. Gomes, H. Chacham y J. R. Mohallem, "Variational calculations for the bound-unbound transition of the Yukawa potential", *Phys. Rev. A* **50**(1), 228–231 (1994), doi:10.1103/PhysRevA.50.228 | [V] | Metadatos (Crossref, Scilit). **Afirmación:** el resumen da $q_c = 1.19061227 \pm 0.00000004$ (LCAO). **Es la fuente original del número que el borrador atribuye a Roy** (D2). Ese valor difiere en $1.5\times10^{-7}$ (unas 3.8 veces la barra declarada) del valor de alta precisión | scilit.com/publications/b1826ad4b884b2b864d95c2b506b4398 ; Crossref |
| Roy2005 | A. K. Roy, "The generalized pseudospectral approach to the bound states of the Hulthén and the Yukawa potentials", *Pramana – J. Phys.* **65**(1), 1–15 (2005), doi:10.1007/BF02704371; arXiv:1312.5900 | [V] | Metadatos (Springer, INSPIRE 3023234). **Revista confirmada:** el preprint de arXiv es de 2013, pero el artículo se publicó en 2005. **Afirmación:** la introducción cita $1.19061227 \pm 0.00000004$ **tomado de su ref. [12]** (Gomes et al. 1994), y en la tabla IV el valor crítico del 1s es 1.1906, citado de Rogers et al. Roy no calcula su propio $\delta_c$ del 1s | link.springer.com/article/10.1007/BF02704371 ; arxiv.org/pdf/1312.5900 |
| Edwards2017 | J. P. Edwards, U. Gerber, C. Schubert, M. A. Trejo y A. Weber, "The Yukawa potential: ground state energy and critical screening", *Prog. Theor. Exp. Phys.* **2017**(8), 083A01 (2017), doi:10.1093/ptep/ptx107; arXiv:1706.09979 | [V] | Metadatos (INSPIRE 1608215; el DOI lleva a academic.oup.com/ptep/article/2017/8/083A01). **Afirmación:** ec. (1.3), $\mu_c/(\alpha m) = 1.1906122105(5)$ (ar5iv) | ar5iv.labs.arxiv.org/html/1706.09979 ; doi.org/10.1093/ptep/ptx107 |
| delValle2018 | J. C. del Valle y D. J. Nader, "Toward the theory of the Yukawa potential", *J. Math. Phys.* **59**(10), 102103 (2018), doi:10.1063/1.5050621; arXiv:1807.11898 | [V] | Metadatos (Crossref). En la tabla II de Song y Zhou figura con 1.19061242106061770 (PT + Padé). No se leyó el original | api.crossref.org (issn 0022-2488, del Valle Nader) |
| Jiao2021 | L. G. Jiao, H. H. Xie, A. Liu, H. E. Montgomery, Jr. y Y. K. Ho, "Critical screening parameters and critical behaviors of one-electron systems with screened Coulomb potentials", *J. Phys. B* **54**(17), 175002 (2021), doi:10.1088/1361-6455/ac259c | [V] | Metadatos (Crossref). En la tabla II de Song y Zhou figura con 1.190612421060617705342777106362 (GPS). No se leyó el original | api.crossref.org (issn 0953-4075, Jiao) |
| Napsuciale2021PLB | M. Napsuciale y S. Rodríguez, "Complete analytical solution to the quantum Yukawa potential", *Phys. Lett. B* **816**, 136218 (2021), doi:10.1016/j.physletb.2021.136218; arXiv:2012.12969 | [V] | Metadatos (cabecera del PDF publicado en INSPIRE; INSPIRE 1838204; zbMATH 1480.81125 vía MaRDI). **Afirmación:** da $\delta_{10} = 1.1906124207(2)$ para el estado fundamental | inspirehep.net/files/a6ca8c42b1f8da1a199b8941bec53d8e |
| Napsuciale2021PTEP | M. Napsuciale y S. Rodríguez, "Bound states of the Yukawa potential from hidden supersymmetry", *Prog. Theor. Exp. Phys.* **2021**(7), 073B03 (2021), doi:10.1093/ptep/ptab070; arXiv:2102.07160 | [V] | Metadatos (INSPIRE 1846700; el DOI lleva a academic.oup.com/ptep/article/2021/7/073B03). **Afirmación (resumen de arXiv):** serie en $\delta = a_0/D$ con Padé, cruces de niveles para $n\ge4$ y mención de estados ligados de materia oscura | arxiv.org/abs/2102.07160 ; doi.org/10.1093/ptep/ptab070 |
| Gebremedhin2023 | D. Gebremedhin y C. Weatherford, "First-order differential equations for single-particle quantum mechanical systems", *Phys. Rev. E* **108**(4), 045301 (2023), publicado el 4-10-2023, doi:10.1103/PhysRevE.108.045301; corrección del 9-5-2024 | [V] | Metadatos (APS; lista de publicaciones de UC Merced CFHEDS). **Afirmación comprobada en la fuente primaria (resumen de APS):** "critical screening parameter $\alpha = 1.19061242106061770534277710636105$", con precisión cuádruple, coincidente en las primeras 30 cifras significativas con cálculos previos. Así se cierra la reserva de la Fase 1. Nombres correctos: **Daniel** Gebremedhin y **Charles** Weatherford. La corrección de 2024 afecta solo a la ec. (22) (potencial HP) | journals.aps.org/pre/abstract/10.1103/PhysRevE.108.045301 |
| Song2026 | L.-Q. Song y H.-Q. Zhou, "Critical properties of bound states with one-boson-exchange potential", *Chin. Phys. C* **50**(9), 093107 (2026), doi:10.1088/1674-1137/ae7702; arXiv:2510.10420 | [V] | Metadatos (INSPIRE 3068490): **ya está publicado**. **Afirmación:** tabla II de arXiv v2 (14-10-2026) con los valores de las refs. [39]–[47]; Gebremedhin y Weatherford son ahora la ref. [47] (no la "ref. 11") | arxiv.org/pdf/2510.10420 ; INSPIRE |
| Luo2006 | X.-Q. Luo, Y.-Y. Li y H. Kröger, "Bound states and critical behavior of the Yukawa potential", *Sci. China G* **49**, 60 (2006), doi:10.1007/s11433-004-0020-5; ed. china *Sci. China G* **35**, 631–642 (2005); arXiv:hep-ph/0407258 | [V] | Metadatos (INSPIRE 655012; arXiv). El ajuste $A_1 + A_2 = 1.190$ es lo que verificó la Fase 1 en arXiv; no lo volví a leer | arxiv.org/abs/hep-ph/0407258 ; INSPIRE |
| Roy2015 | A. K. Roy, "Spherical confinement of Coulombic systems inside an impenetrable box: H atom and the Hulthén potential", *Int. J. Quantum Chem.* **115**(15), 937–947 (2015), doi:10.1002/qua.24929; arXiv:1802.04373 | [V] | Metadatos (Crossref; INSPIRE 3040596). **Publicado**, no solo arXiv. Afirmación (radio crítico de caja con $E=0$): según E2 | api.crossref.org (Roy Spherical confinement) |
| Roy2016 | A. K. Roy, "Critical parameters and spherical confinement of H atom in screened Coulomb potential", *Int. J. Quantum Chem.* **116**(12), 953–960 (2016), doi:10.1002/qua.25108; arXiv:1904.11166 | [V] | Metadatos (Crossref). **Publicado**, no solo arXiv. Afirmación (críticos de Hulthén, Yukawa y ECSC; ECSC confinado): según E2 | api.crossref.org (Roy Critical parameters) |
| HulthenLaurikainen1951 | L. Hulthén y K. V. Laurikainen, "Approximate Eigensolutions of $\frac{d^2\varphi}{dx^2} + [a + b\,\frac{e^{-x}}{x}]\varphi = 0$", *Rev. Mod. Phys.* **23**(1), 1–9 (1951), doi:10.1103/RevModPhys.23.1 | [V] | Metadatos (Crossref, Scilit). El título es la propia ecuación | Crossref |

## B. Cotas y matemática del umbral

| Clave | Referencia completa | Estado | Qué se comprobó | Enlace usado |
|---|---|---|---|---|
| Bargmann1952 | V. Bargmann, "On the Number of Bound States in a Central Field of Force", *Proc. Natl. Acad. Sci. USA* **38**(11), 961–966 (1952), doi:10.1073/pnas.38.11.961 | [V] | Metadatos (Crossref): el fascículo es el 11. La desigualdad $n_l < \frac{1}{2l+1}\int r|U|\,dr$ la verificó la Fase 1; yo no volví a leer el texto | Crossref |
| Schwinger1961 | J. Schwinger, "On the Bound States of a Given Potential", *Proc. Natl. Acad. Sci. USA* **47**(1), 122–129 (1961), doi:10.1073/pnas.47.1.122 | [V] | Metadatos (Crossref). **Es la referencia de la cota 1.24305** que el borrador atribuye a Bargmann (D3) | Crossref |
| Calogero1965 | F. Calogero, "Upper and lower limits for the number of bound states in a given central potential", *Commun. Math. Phys.* **1**(1), 80–88 (1965), doi:10.1007/BF01649591 | [V] | Metadatos (Crossref) | Crossref |
| KlausSimon1980 | M. Klaus y B. Simon, "Coupling constant thresholds in nonrelativistic quantum mechanics. I. Short-range two-body case", *Ann. Phys.* **130**(2), 251–281 (1980), doi:10.1016/0003-4916(80)90338-3 | [V] | Metadatos (Crossref). La afirmación de que $e(\lambda)\sim c(\lambda-\lambda_0)^\alpha$ con un $\alpha$ que depende de la dimensión la leyó E4 en el resumen (CaltechAUTHORS). $\alpha = 2$ ($\ell=0$) y $\alpha = 1$ ($\ell\ge1$) en 3D está confirmado en Serra et al. 1998, no en este texto | Crossref |
| Bethe1949 | H. A. Bethe, "Theory of the Effective Range in Nuclear Scattering", *Phys. Rev.* **76**(1), 38–50 (1949), doi:10.1103/PhysRev.76.38 | [V] | Metadatos (Crossref). La definición de $r_e$ no se leyó en el original (E2 la comprobó numéricamente) | Crossref |

## C. Escalamiento de tamaño finito

| Clave | Referencia completa | Estado | Qué se comprobó | Enlace usado |
|---|---|---|---|---|
| Serra1998 | P. Serra, J. P. Neirotti y S. Kais, "Finite-size scaling approach for the Schrödinger equation", *Phys. Rev. A* **57**(3), R1481–R1484 (1998), doi:10.1103/PhysRevA.57.R1481 | [V] | Metadatos (Crossref). Afirmación según E2 y E4 (PDF del grupo de Kais): el "tamaño" es el de la base; $\lambda_c = 0.8399039(1)$ ($\ell=0$, $\alpha=2$) y $4.540980(3)$ ($\ell=1$, $\alpha=1$) | Crossref |
| KaisSerra2000 | S. Kais y P. Serra, "Quantum critical phenomena and stability of atomic and molecular ions", *Int. Rev. Phys. Chem.* **19**(1), 97–121 (2000), doi:10.1080/014423500229873 | [V] | Metadatos (Crossref) | Crossref |
| KaisSerra2003 | S. Kais y P. Serra, "Finite-Size Scaling for Atomic and Molecular Systems", *Adv. Chem. Phys.* **125**, 1–99 (2003), doi:10.1002/0471428027.ch1 | [V] | Metadatos (Crossref: páginas 1–99, 2003, DOI). El volumen 125 viene de E2 (Crossref no lo da para el capítulo) | Crossref |
| dosSantos1981 | R. R. dos Santos y L. Sneddon, "Finite-size rescaling transformations", *Phys. Rev. B* **23**(7), 3541–3546 (1981), doi:10.1103/PhysRevB.23.3541 | [V] | Metadatos (Crossref) | Crossref |
| Nightingale1976 | M. P. Nightingale, "Scaling theory and finite systems", *Physica A* **83**(3), 561–572 (1976), doi:10.1016/0378-4371(75)90021-7 | [V] | Metadatos (Crossref: año 1976 aunque el DOI diga 75) | Crossref |
| Kais2010arXiv | S. Kais, "Finite size scaling for criticality of the Schrödinger equation", arXiv:1009.4393 | [V-arXiv] | Según E2 (no reabierto aquí) | arxiv.org/abs/1009.4393 (E2) |
| Alharbi2013arXiv | F. H. Alharbi y S. Kais, "Quantum criticality analysis by finite size scaling and exponential basis sets", arXiv:1304.7433 | [V-arXiv] | Según E2 (no reabierto aquí) | arxiv.org/abs/1304.7433 (E2) |
| SerraSpatial | P. Serra, "A spatial finite size scaling method for calculation of critical parameters for weakly bound states", PDF en famaf.unc.edu.ar/~serra/serra28.pdf | [V-doc] | Según E2. **No se sabe dónde se publicó**: citarlo como manuscrito o no citarlo | famaf.unc.edu.ar/~serra/serra28.pdf (E2) |

## D. Volumen finito, caja con pared y trampas

| Clave | Referencia completa | Estado | Qué se comprobó | Enlace usado |
|---|---|---|---|---|
| Luscher1986 | M. Lüscher, "Volume dependence of the energy spectrum in massive quantum field theories", *Commun. Math. Phys.* **105**(2), 153–188 (1986), doi:10.1007/BF01211097 | [V] | Metadatos (Crossref) | Crossref |
| Luscher1991 | M. Lüscher, "Two-particle states on a torus and their relation to the scattering matrix", *Nucl. Phys. B* **354**(2–3), 531–578 (1991), doi:10.1016/0550-3213(91)90366-6 | [V] | Metadatos (Crossref) | Crossref |
| Konig2011 | S. König, D. Lee y H.-W. Hammer, "Volume Dependence of Bound States with Angular Momentum", *Phys. Rev. Lett.* **107**, 112001 (2011), doi:10.1103/PhysRevLett.107.112001; arXiv:1103.4468 | [V] | Metadatos (INSPIRE 893699). Afirmación (caja periódica; onda s reforzada, onda p debilitada): según E2 | INSPIRE |
| Borasoy2007 | B. Borasoy, E. Epelbaum, H. Krebs, D. Lee y U.-G. Meißner, "Two-particle scattering on the lattice: Phase shifts, spin-orbit coupling, and mixing angles", *Eur. Phys. J. A* **34**, 185–196 (2007), doi:10.1140/epja/i2007-10500-9; arXiv:0708.1780 | [V] | Metadatos (INSPIRE 758235). Afirmación (método de la pared esférica): según E2 | INSPIRE |
| Drut2013 | J. E. Drut y A. N. Nicholson, "Lattice methods for strongly interacting many-body systems", *J. Phys. G* **40**, 043101 (2013), doi:10.1088/0954-3899/40/4/043101; arXiv:1208.6556 | [V] | Metadatos (INSPIRE 1184028): la revista y el volumen ya están confirmados | INSPIRE |
| Busch1998 | T. Busch, B.-G. Englert, K. Rzążewski y M. Wilkens, "Two Cold Atoms in a Harmonic Trap", *Found. Phys.* **28**(4), 549–559 (1998), doi:10.1023/A:1018705520999 | [V] | Metadatos (Crossref) | Crossref |
| Stetcu2010 | I. Stetcu, J. Rotureau, B. R. Barrett y U. van Kolck, "An effective field theory approach to two trapped particles", *Ann. Phys.* **325**, 1644–1666 (2010), doi:10.1016/j.aop.2010.02.008; arXiv:1001.5071 | [V] | Metadatos (INSPIRE 844132): **publicado**, no solo arXiv. Afirmación: según E2 | INSPIRE |
| Djajaputra2000 | D. Djajaputra y B. R. Cooper, "Hydrogen atom in a spherical well: linear approximation", *Eur. J. Phys.* **21**(3), 261–267 (2000), doi:10.1088/0143-0807/21/3/309; arXiv:physics/9912031 | [V] | Metadatos (Crossref): revista, volumen y páginas confirmados | Crossref |

## E. Halos y extensión cerca del umbral

| Clave | Referencia completa | Estado | Qué se comprobó | Enlace usado |
|---|---|---|---|---|
| Riisager2013 | K. Riisager, "Halos and related structures", *Phys. Scr.* **T152**, 014001 (2013), doi:10.1088/0031-8949/2013/T152/014001; arXiv:1208.6415 | [V] | Metadatos (INSPIRE 1184052: Phys. Scripta T 152, artid 014001, 2013, DOI). Afirmación (ec. (4), $\langle r^n\rangle$): según E4 | INSPIRE |
| Jensen2004 | A. S. Jensen, K. Riisager, D. V. Fedorov y E. Garrido, "Structure and reactions of quantum halos", *Rev. Mod. Phys.* **76**(1), 215–261 (2004), doi:10.1103/RevModPhys.76.215 | [V] | Metadatos (Crossref) | Crossref |
| Misu1997 | T. Misu, W. Nazarewicz y S. Åberg, "Deformed nuclear halos", *Nucl. Phys. A* **614**, 44–70 (1997), doi:10.1016/S0375-9474(96)00458-7; arXiv:nucl-th/9612016 | [V] | Metadatos (INSPIRE 426999): la revista ya está confirmada. Afirmación ($\langle r^2\rangle \sim (-\varepsilon)^{-1}$ en s y $(-\varepsilon)^{-1/2}$ en p): según E4 | INSPIRE |
| Riisager1992 | K. Riisager, A. S. Jensen y P. Møller, "Two-body halos", *Nucl. Phys. A* **548**(3), 393–413 (1992), doi:10.1016/0375-9474(92)90691-C | [V] | Metadatos (Scilit). Es la referencia de 1992 que citan arXiv:1705.08718 y nucl-th/9612016 (según E4/R4); probablemente es la que E4 buscaba como "EPL 19 (1992)" | scilit.com/publications/775860813b50a11351643f8662991e34 |
| Riisager2000 | K. Riisager, D. V. Fedorov y A. S. Jensen, "Quantum halos", *Europhys. Lett.* **49**(5), 547–553 (2000), doi:10.1209/epl/i2000-00180-y | [V] | Metadatos (Crossref). **E4 la tenía como *EPL* 19 (1992), no verificada: el año correcto es 2000** (D14). No se cita en ninguna sección | Crossref |

## F. Integrales de camino y Monte Carlo

| Clave | Referencia completa | Estado | Qué se comprobó | Enlace usado |
|---|---|---|---|---|
| FeynmanHibbs1965 | R. P. Feynman y A. R. Hibbs, *Quantum Mechanics and Path Integrals* (McGraw-Hill, Nueva York, 1965), xiv + 365 págs. | [V] | Catálogo de Open Library (ISBN 9780070206502) | openlibrary.org/isbn/9780070206502 |
| PollockCeperley1984 | E. L. Pollock y D. M. Ceperley, "Simulation of quantum many-body systems by path-integral methods", *Phys. Rev. B* **30**(5), 2555–2568 (1984), doi:10.1103/PhysRevB.30.2555 | [V] | Metadatos (Crossref) | Crossref |
| Ceperley1995 | D. M. Ceperley, "Path integrals in the theory of condensed helium", *Rev. Mod. Phys.* **67**(2), 279–355 (1995), doi:10.1103/RevModPhys.67.279 | [V] | Metadatos (Crossref) | Crossref |
| Cai1986 | J. M. Cai, P. Y. Cai y A. Inomata, "Path-integral treatment of the Hulthén potential", *Phys. Rev. A* **34**(6), 4621–4628 (1986), doi:10.1103/PhysRevA.34.4621 | [V] | Metadatos (Crossref, Scilit). Resumen (link.aps.org): tratamiento exacto por integral de camino de los estados s del Hulthén | scilit.com/publications/5dac4989d03574af5fdc42b6b5c81cff ; link.aps.org/doi/10.1103/PhysRevA.34.4621 |
| Kole2001 | J. S. Kole y H. De Raedt, "Quantum Monte Carlo method for attractive Coulomb potentials", *Phys. Rev. E* **64**(1), 016704 (2001), publicado el 22-6-2001, doi:10.1103/PhysRevE.64.016704; arXiv:physics/0102015 | [V] | Metadatos y resumen (APS): **revista confirmada**. **Afirmación:** el método parte de "an exact lower bound on the imaginary-time propagator", con pruebas en H y He. **No es un suavizado del potencial** (D11) | journals.aps.org/pre/abstract/10.1103/PhysRevE.64.016704 |
| Myrheim2003 | J. Myrheim, "Numerical path integration with Coulomb potential", arXiv:physics/0306168 (2003) | [V-arXiv] | Metadatos y método (arXiv y ar5iv): promedio gaussiano del potencial con desviación constante a lo largo del camino. **No se encontró publicación en revista** (ni en INSPIRE ni en Crossref, búsqueda por autor) | arxiv.org/abs/physics/0306168 ; Crossref |
| Dluhy2011 | P. Dluhy y A. Gangopadhyaya, "Sharp and Infinite Boundaries in the Path Integral Formalism", arXiv:1112.3674 (2011) | [V-arXiv] | Metadatos y resumen (arXiv): método de imágenes para paredes infinitas. INSPIRE 3002241 no registra revista | arxiv.org/abs/1112.3674 |
| Edwards2019 | J. P. Edwards, U. Gerber, C. Schubert, M. A. Trejo, T. Tsiftsi y A. Weber, "Applications of the worldline Monte Carlo formalism in quantum mechanics", *Ann. Phys.* **411**, 167966 (2019), doi:10.1016/j.aop.2019.167966; arXiv:1903.00536 | [V] | Metadatos (INSPIRE 1723250; portal de investigación de Plymouth): **ya está publicado**. **Afirmación (PDF de arXiv):** "smoothing" de potenciales singulares; *undersampling* (los caminos dejan de muestrear el potencial a tiempo largo, sec. 4.1.2); Yukawa en la sec. 7.2 con $\mu_c\approx1.19\,\alpha m$ (ec. 59) | arxiv.org/pdf/1903.00536 ; INSPIRE |
| Ahumada2025 | I. Ahumada, M. Badcott, J. P. Edwards, C. McNeile, F. Ricchetti, F. Grasselli, G. Goldoni, O. Corradini y M. Palomino, "Multi-particle quantum systems within the Worldline Monte Carlo formalism", arXiv:2512.24942 (2025) | [V-arXiv] | Metadatos (INSPIRE 3096694, sin revista). La afirmación sobre el Yukawa no se releyó | INSPIRE |

## G. Representación probabilística (Feynman–Kac, *gauge*)

| Clave | Referencia completa | Estado | Qué se comprobó | Enlace usado |
|---|---|---|---|---|
| ChungZhao1995 | K. L. Chung y Z. Zhao, *From Brownian Motion to Schrödinger's Equation*, Grundlehren der mathematischen Wissenschaften **312** (Springer, Berlín, 1995), doi:10.1007/978-3-642-57856-4 | [V] | Metadatos (Springer: serie GL vol. 312, 1995, ISBN 978-3-540-57030-1; Crossref) | link.springer.com/book/10.1007/978-3-642-57856-4 |
| Cranston2002 | M. Cranston, "Book Review: From Brownian motion to Schrödinger's equation", *Bull. Amer. Math. Soc.* **39**(1), 109–112 (2002), doi:10.1090/S0273-0979-01-00925-9 | [V] | Metadatos (Crossref; en línea el 11-10-2001, fascículo de 2002) | Crossref |
| Chung1985 | K. L. Chung, "The gauge and conditional gauge theorem", en J. Azéma y M. Yor (eds.), *Séminaire de Probabilités XIX 1983/84*, Lecture Notes in Mathematics **1123** (Springer, 1985), págs. 496–503, doi:10.1007/BFb0075868 | [V] | Metadatos (Springer, Crossref) | link.springer.com/chapter/10.1007/BFb0075868 |
| KacLuttinger1975 | M. Kac y J. M. Luttinger, "Scattering length and capacity", *Ann. Inst. Fourier* **25**(3–4), 317–321 (1975), doi:10.5802/aif.586 | [V] | Metadatos (Crossref) | Crossref |
| He2011 | P. He, "A formula on scattering length of dual Markov processes", *Proc. Amer. Math. Soc.* **139**(5), 1871–1877 (2011), doi:10.1090/S0002-9939-2010-10618-4 | [V] | Metadatos (Crossref; en línea en 2010, fascículo de 2011) | Crossref |

## H. Contexto físico: plasmas

| Clave | Referencia completa | Estado | Qué se comprobó | Enlace usado |
|---|---|---|---|---|
| Huba2004 | J. D. Huba, *NRL Plasma Formulary*, NRL/PU/6790--04-477 (Naval Research Laboratory, Washington, revisión 2004) | [V-doc] | **Afirmación:** p. 29, $\lambda_D = (kT/4\pi ne^2)^{1/2} = 7.43\times10^2\,(T/n)^{1/2}$ cm; número de informe y año en la portada | courses.grainger.illinois.edu/ece350/PlasmaFormulary.pdf |
| StewartPyatt1966 | J. C. Stewart y K. D. Pyatt, Jr., "Lowering of Ionization Potentials in Plasmas", *Astrophys. J.* **144**, 1203 (1966), doi:10.1086/148714 | [V] | Metadatos (Crossref) | Crossref |
| Crowley2014 | B. J. B. Crowley, "Continuum lowering – A new perspective", *High Energy Density Phys.* **13**, 84–102 (2014), doi:10.1016/j.hedp.2014.04.003; arXiv:1309.1456 | [V] | Metadatos (Crossref): volumen 13 y páginas confirmados. Afirmación del resumen: según E1 | Crossref |
| Janev2016 | R. K. Janev, S. Zhang y J. Wang, "Review of quantum collision dynamics in Debye plasmas", *Matter Radiat. Extremes* **1**(5), 237–248 (2016), doi:10.1016/j.mre.2016.10.002; arXiv:1606.00163 | [V] | Metadatos (Crossref). Afirmación (tabla 1: 0.839907): según E1 | Crossref |
| MurilloWeisheit1998 | M. S. Murillo y J. C. Weisheit, "Dense plasmas, screened interactions, and atomic ionization", *Phys. Rep.* **302**(1), 1–65 (1998), doi:10.1016/S0370-1573(98)00017-9 | [V] | Metadatos (Crossref; Crossref solo lista al primer autor). E1 la tenía como no verificada; ahora se puede citar | Crossref |
| DebyeHuckel1923 | P. Debye y E. Hückel, *Phys. Z.* **24**, 185 (1923) | [no verificada] | No tiene DOI y no se encontró en un índice abierto en esta sesión. **No citar** sin abrir una copia | — |

## I. Contexto físico: materia oscura

| Clave | Referencia completa | Estado | Qué se comprobó | Enlace usado |
|---|---|---|---|---|
| Tulin2013 | S. Tulin, H.-B. Yu y K. M. Zurek, "Beyond Collisionless Dark Matter: Particle Physics Dynamics for Dark Matter Halo Structure", *Phys. Rev. D* **87**(11), 115007 (2013), doi:10.1103/PhysRevD.87.115007; arXiv:1302.3898 | [V] | Metadatos (INSPIRE 1219968). **Afirmación (PDF de arXiv, sec. IV.B):** "s-wave resonance for b=1.68" y antirresonancia en $b = 4.52$, con $b\equiv\alpha_X m_X/m_\phi$. Coincide con $2/\delta_c = 1.6798$ | arxiv.org/pdf/1302.3898 ; INSPIRE |
| Feng2010 | J. L. Feng, M. Kaplinghat y H.-B. Yu, "Sommerfeld Enhancements for Thermal Relic Dark Matter", *Phys. Rev. D* **82**, 083525 (2010), doi:10.1103/PhysRevD.82.083525; arXiv:1005.4678 | [V] | Metadatos (INSPIRE 856344). Afirmación (ecs. 6–7, Hulthén con $\pi^2/6$): según E1 | INSPIRE |
| Petraki2017 | K. Petraki, M. Postma y J. de Vries, "Radiative bound-state-formation cross-sections for dark matter interacting via a Yukawa potential", *JHEP* **04** (2017) 077, doi:10.1007/JHEP04(2017)077; arXiv:1611.01394 | [V] | Metadatos (INSPIRE 1495853). Según E1, la cifra 1.68 **no** aparece en el texto principal (D7) | INSPIRE |
| TulinYu2018 | S. Tulin y H.-B. Yu, "Dark Matter Self-interactions and Small Scale Structure", *Phys. Rep.* **730**, 1–57 (2018), doi:10.1016/j.physrep.2017.11.004; arXiv:1705.02358 | [V] | Metadatos (INSPIRE 1598408): **publicado**; E1 la tenía como solo arXiv | INSPIRE |

## J. Contexto físico: deuterón y masa del pion

| Clave | Referencia completa | Estado | Qué se comprobó | Enlace usado |
|---|---|---|---|---|
| Epelbaum2003 | E. Epelbaum, U.-G. Meißner y W. Glöckle, "Nuclear forces in the chiral limit", *Nucl. Phys. A* **714**, 535–574 (2003), doi:10.1016/S0375-9474(02)01393-3; arXiv:nucl-th/0207089 | [V] | Metadatos (INSPIRE 591690): **volumen 714, págs. 535–574, año 2003**. Afirmación del resumen ($B_D^{CL} = 9.6\pm1.9^{+1.8}_{-1.0}$ MeV): según E1 | INSPIRE |
| BeaneSavage2003 | S. R. Beane y M. J. Savage, "The quark mass dependence of two-nucleon systems", *Nucl. Phys. A* **717**, 91–103 (2003), doi:10.1016/S0375-9474(02)01586-5; arXiv:nucl-th/0208021 | [V] | Metadatos (INSPIRE 592504): **volumen 717, págs. 91–103, año 2003**. Afirmación del resumen: según E1 | INSPIRE |
| NPLQCD2013 | S. R. Beane, E. Chang, S. D. Cohen, W. Detmold, H. W. Lin, T. C. Luu, K. Orginos, A. Parreño, M. J. Savage y A. Walker-Loud (NPLQCD), "Light nuclei and hypernuclei from quantum chromodynamics in the limit of SU(3) flavor symmetry", *Phys. Rev. D* **87**(3), 034506 (2013), publicado el 11-2-2013, doi:10.1103/PhysRevD.87.034506; arXiv:1206.5219 | [V] | Metadatos y resumen (APS, INSPIRE 1119407): **año 2013**; tres volúmenes de red (3.4, 4.5 y 6.7 fm) y $b\sim0.145$ fm. Las cifras $m_\pi\approx806$ MeV y $B_d = 19.5$ MeV son según E1 (texto de arXiv) | journals.aps.org/prd/abstract/10.1103/PhysRevD.87.034506 |
| Berengut2013 | J. C. Berengut, E. Epelbaum, V. V. Flambaum, C. Hanhart, U.-G. Meißner, J. Nebreda y J. R. Peláez, "Varying the light quark mass: impact on the nuclear force and Big Bang nucleosynthesis", *Phys. Rev. D* **87**(8), 085018 (2013), doi:10.1103/PhysRevD.87.085018; arXiv:1301.1738 | [V] | Metadatos (INSPIRE 1209840): **número de artículo 085018 confirmado**. Afirmación: según E1 | INSPIRE |
| Filin2020 | A. A. Filin, V. Baru, E. Epelbaum, H. Krebs, D. Möller y P. Reinert, "Extraction of the neutron charge radius from a precision calculation of the deuteron structure radius", *Phys. Rev. Lett.* **124**(8), 082501 (2020), doi:10.1103/PhysRevLett.124.082501; arXiv:1911.04877 | [V] | Metadatos (INSPIRE 1764337). Afirmación (ecs. 2 y 9): según E1 | INSPIRE |

## K. Constantes

| Clave | Referencia completa | Estado | Qué se comprobó | Enlace usado |
|---|---|---|---|---|
| CODATA2022 | P. J. Mohr, D. B. Newell, B. N. Taylor y E. Tiesinga, "CODATA recommended values of the fundamental physical constants: 2022", *Rev. Mod. Phys.* **97**(2), 025002 (2025), doi:10.1103/RevModPhys.97.025002; arXiv:2409.03787 | [V] | Metadatos (INSPIRE 2826045). **Afirmación (tabla del NIST, "2022 CODATA adjustment"):** $a_0 = 5.29177210544(82)\times10^{-11}$ m; $r_d = 2.12778(27)$ fm; $r_p = 0.84075(64)$ fm; $m_d c^2 = 1875.61294500(58)$ MeV; $m_p c^2 = 938.27208943(29)$ MeV; $m_n c^2 = 939.56542194(48)$ MeV; $\hbar c = 197.3269804$ MeV fm | physics.nist.gov/cuu/Constants/Table/allascii.txt |
| CODATA2018 | E. Tiesinga, P. J. Mohr, D. B. Newell y B. N. Taylor, "CODATA recommended values of the fundamental physical constants: 2018", *Rev. Mod. Phys.* **93**(2), 025010 (2021), doi:10.1103/RevModPhys.93.025010 | [V] | Metadatos (Crossref). Está superada por CODATA 2022 (D12) | Crossref |
| PDG2025 | Particle Data Group (S. Navas et al.), *Review of Particle Physics* (2025): tablas de constantes y de mesones ligeros | [V-doc] | Según E1: $m_{\pi^\pm} = 139.57039(18)$ MeV y $m_{\pi^0} = 134.9768(5)$ MeV. No reabierto aquí; la referencia de revista del PDG 2025 no se comprobó | pdg.lbl.gov/2025/reviews/rpp2025-rev-phys-constants.pdf (E1) |
| PDG2024n | Particle Data Group, tabla de bariones N (2024), $r_n^2 = -0.1161(22)$ fm² | [no verificada] | E1 tomó el valor de Filin et al., no del PDG. **No citar el PDG para $r_n^2$**: citar Filin et al. o abrir la tabla | — |

---

## L. Referencias añadidas por E3 (otros perfiles) y E5 (Feynman–Kac)

`E3_otros_perfiles/fuentes.md` apareció durante la segunda pasada. E5 todavía no tiene `fuentes.md`; sus citas se
tomaron de `E5_feynman_kac/teoria.md` (sección 2 y sección 9).

| Clave | Referencia completa | Estado | Qué se comprobó | Enlace usado |
|---|---|---|---|---|
| LamVarshni1972 | C. S. Lam y Y. P. Varshni, "Bound Eigenstates of the Exponential Cosine Screened Coulomb Potential", *Phys. Rev. A* **6**(4), 1391–1399 (1972), doi:10.1103/PhysRevA.6.1391 | [V] | Metadatos (Crossref). **Esta**, y no Lam y Varshni 1971, es la referencia original del ECSC (D25) | Crossref |
| SinghVarshni1983 | D. Singh y Y. P. Varshni, "Accurate eigenvalues and oscillator strengths for the exponential-cosine screened Coulomb potential", *Phys. Rev. A* **28**(5), 2606–2610 (1983), doi:10.1103/PhysRevA.28.2606 | [V] | Metadatos (Crossref). El valor 0.72052408 para el ECSC 1s solo se leyó en Roy 2016 (según E3) | Crossref |
| Nasser2011 | I. Nasser, M. S. Abdelmonem y A. Abdel-Hady, "$J$-Matrix approach for the exponential-cosine-screened Coulomb potential", *Phys. Scr.* **84**(4), 045001 (2011), doi:10.1088/0031-8949/84/04/045001 | [V] | Metadatos (Crossref). El valor 0.72055425 está según Roy (E3) | Crossref |
| Roy2013 | A. K. Roy, "Studies on some exponential-screened Coulomb potentials", *Int. J. Quantum Chem.* **113**(10), 1503–1510 (2013), doi:10.1002/qua.24351; arXiv:1304.6928 | [V] | Metadatos (Crossref; en línea el 23-10-2012). **Publicado**; E3 lo tenía como solo arXiv | Crossref |
| Zhao1992 | Z. Zhao, "Subcriticality and gaugeability of the Schrödinger operator", *Trans. Amer. Math. Soc.* **334**(1), 75–96 (1992), doi:10.1090/S0002-9947-1992-1068934-5 | [V] | Metadatos (Crossref). Afirmación (equivalencia entre subcriticidad y gaugeabilidad en $\mathbb R^d$, $d\ge3$): según E5 (resumen) | Crossref |
| Chen2002 | Z.-Q. Chen, "Gaugeability and conditional gaugeability", *Trans. Amer. Math. Soc.* **354**(11), 4639–4679 (2002), doi:10.1090/S0002-9947-02-03059-3 | [V] | Metadatos (Crossref) | Crossref |
| FitzsimmonsPitman1999 | P. J. Fitzsimmons y J. Pitman, "Kac's moment formula and the Feynman–Kac formula for additive functionals of a Markov process", *Stoch. Process. Appl.* **79**(1), 117–134 (1999), doi:10.1016/S0304-4149(98)00081-7 | [V] | Metadatos (Crossref). Afirmación ($E[A^n] = n!\,\mu(GM_v)^n1$): según E5 | Crossref |
| CiesielskiTaylor1962 | Z. Ciesielski y S. J. Taylor, "First passage times and sojourn times for Brownian motion in space and the exact Hausdorff measure of the sample path", *Trans. Amer. Math. Soc.* **103**(3), 434– (1962), doi:10.1090/S0002-9947-1962-0143257-8 | [V] | Título, volumen, fascículo, página inicial 434 y DOI (Crossref). La página final no está en Crossref | Crossref |
| Esry2007 | B. D. Esry, AMO-2, tarea 1, problema 2 (Kansas State University, 2007): potencial estático $e^-$ + H(1s) | [V-doc] | Según E3 (material docente en phys.ksu.edu). Para el artículo es mejor dar el potencial como "potencial estático (de Hartree) del H(1s)" sin citar una tarea | phys.ksu.edu (E3) |

**Referencias de E3 que ya estaban en la tabla:** Roy2016 (= "Roy 2019", arXiv:1904.11166; ver D26), LamVarshni1971,
Gomes1994, Stubbins1993 (ver D27), Roy2005 (= arXiv:1312.5900) y Bethe1949. **De E5:** Chung1985, Cranston2002 (D28),
ChungZhao1995, KacLuttinger1975, He2011 y Edwards2019.

## Orden recomendado para el artículo final (núcleo, unas 20 referencias)

Yukawa1935; Bargmann1952; Schwinger1961; Calogero1965; Rogers1970; LamVarshni1971; Stubbins1993; Gomes1994;
Edwards2017; Napsuciale2021PLB; Gebremedhin2023; Song2026; Roy2005; Roy2016; LamVarshni1972 (si entra E3); KlausSimon1980; Serra1998; Konig2011;
Borasoy2007; Riisager2013; FeynmanHibbs1965; PollockCeperley1984; Ceperley1995; Cai1986; Kole2001; Myrheim2003;
Dluhy2011; Edwards2019; ChungZhao1995; KacLuttinger1975; y, para el contexto físico, Huba2004, Tulin2013,
Epelbaum2003, BeaneSavage2003, NPLQCD2013, CODATA2022.
