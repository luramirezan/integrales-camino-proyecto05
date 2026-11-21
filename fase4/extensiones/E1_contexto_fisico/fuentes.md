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
