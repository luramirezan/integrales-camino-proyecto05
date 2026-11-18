# Fuentes de E2 y estado de verificación

Búsqueda hecha el 17-11-2026 con WebSearch y WebFetch. Marcas: **[V]** verificada en la página del editor, en el DOI o en un
índice bibliográfico (Scilit, ADS, OSTI); **[V-arXiv]** verificada solo en arXiv; **[V-web]** verificada solo en la página
del autor; **[no verificada]** citada de memoria o por otra fuente. Para cada una se dice qué se comprobó y qué no.

## Escalamiento de tamaño finito en mecánica cuántica (la comparación principal)

| Referencia | Estado | Qué se comprobó |
|---|---|---|
| P. Serra, J. P. Neirotti y S. Kais, "Finite-size scaling approach for the Schrödinger equation", *Phys. Rev. A* **57**, R1481 (1998) | [V] (PDF en la web del grupo de Kais; Scilit) | El "tamaño" es el número de funciones de base N, **no** una caja espacial ("the finite size corresponds to the number of elements in the truncated basis set"). Ejemplo: Yukawa escalado, λ_c = 0.8399039(1) para ℓ = 0 (es 1/δ_c) y 4.540980(3) para ℓ = 1; exponentes α = 2 y 1. Las curvas D_O(λ; N, N′) se cruzan en el punto crítico. |
| S. Kais y P. Serra, "Quantum critical phenomena and stability of atomic and molecular ions", *Int. Rev. Phys. Chem.* **19**, 97–121 (2000), DOI 10.1080/014423500229873 | [V] (Scilit) | Solo los datos bibliográficos. |
| S. Kais y P. Serra, "Finite-size scaling for atomic and molecular systems", *Adv. Chem. Phys.* **125** (2003) | [V-web] (PDF en la web del grupo; páginas no visibles) | En mecánica cuántica el tamaño es otra vez el de la base; el Yukawa es el ejemplo resuelto (sección IV.C, colapso con N = 20 a 100). La sección VII ("Spatial finite-size scaling") usa un **radio de corte del potencial**; el PDF accesible se corta antes de esa sección. |
| S. Kais, "Finite size scaling for criticality of the Schrödinger equation", arXiv:1009.4393 | [V-arXiv] | Tamaño = dimensión del espacio de la base; no usa una caja espacial. |
| F. H. Alharbi y S. Kais, "Quantum criticality analysis by finite size scaling and exponential basis sets", arXiv:1304.7433 | [V-arXiv] | Tamaño = número de funciones de base; potencial de Hulthén; sin caja. |
| P. Serra, "A spatial finite size scaling method for calculation of critical parameters for weakly bound states" (PDF en famaf.unc.edu.ar/~serra/serra28.pdf) | [V-web] (sin revista ni año en el PDF; según la lista del autor, Phys. Lett. A 303, 20 (2002)) | **Es el antecedente más cercano que encontramos.** Escala con una longitud R, pero R es un **radio de corte del potencial** (V = 0 para r > R) con condición de Siegert, no una pared dura. Las curvas Γ(R, R+1; λ) se cruzan cerca de λ_c y se extrapola en 1/R. El ejemplo es un pozo cuadrado con ℓ = 1; el método supone un exponente α ≠ 2, así que no se aplica tal cual a la onda s. No menciona el Yukawa ni un punto fijo 1/4. No pudimos identificar dónde se publicó. **Revisión R2:** la lista de publicaciones del autor (famaf.unc.edu.ar/~serra/list.html) da *Physics Letters A* **303**, 20 (2002); no se pudo abrir la página del editor ni Crossref, así que queda [V-web]. |
| R. R. dos Santos y L. Sneddon, "Finite-size rescaling transformations", *Phys. Rev. B* **23**, 3541–3546 (1981), DOI 10.1103/PhysRevB.23.3541 | [V] (Scilit) | Teoría de las transformaciones de reescalamiento de tamaño finito; muestra que la renormalización fenomenológica de Nightingale es un caso particular. Es el origen del "cruce de curvas de dos tamaños". |
| M. P. Nightingale, "Scaling theory and finite systems", *Physica A* **83**, 561–572 (1976), DOI 10.1016/0378-4371(75)90021-7 | [V] (Scilit) | Datos bibliográficos; es la renormalización fenomenológica original. |

## Volumen finito y caja con pared

| Referencia | Estado | Qué se comprobó |
|---|---|---|
| M. Lüscher, "Volume dependence of the energy spectrum in massive quantum field theories", *Commun. Math. Phys.* **105**, 153–188 (1986), DOI 10.1007/BF01211097 | [V] (Scilit) | Datos bibliográficos. |
| M. Lüscher, "Two-particle states on a torus and their relation to the scattering matrix", *Nucl. Phys. B* **354**, 531 (1991), DOI 10.1016/0550-3213(91)90366-6 | [V] (ADS) | Resumen: en una caja periódica mayor que el alcance, los niveles de dos partículas los fijan los corrimientos de fase, en las dos direcciones. Es la versión periódica de nuestra ecuación x cot x = R/a. |
| S. König, D. Lee y H.-W. Hammer, "Volume dependence of bound states with angular momentum", *Phys. Rev. Lett.* **107**, 112001 (2011), arXiv:1103.4468 | [V] (OSTI, arXiv) | Caja **periódica**: el ligado s se refuerza en volumen finito y el p se debilita; para ℓ ≥ 2 depende de la representación cúbica. No trata la pared dura ni el umbral. |
| B. Borasoy, E. Epelbaum, H. Krebs, D. Lee y U.-G. Meißner, "Two-particle scattering on the lattice: phase shifts, spin-orbit coupling, and mixing angles", *Eur. Phys. J. A* **34**, 185–196 (2007), arXiv:0708.1780 | [V] (Springer, arXiv) | **Método de la pared esférica**: una pared dura a un radio grande fijo y los corrimientos de fase salen de las energías de las ondas estacionarias. Es exactamente la condición de cuantización de nuestra sección 1 de `teoria.md`; no es nuestra. |
| J. E. Drut y A. N. Nicholson, "Lattice methods for strongly interacting many-body systems", DOI 10.1088/0954-3899/40/4/043101, arXiv:1208.6556 | [V-arXiv] (la revista, J. Phys. G **40** (2013), se deduce del DOI y no se comprobó en el editor) | En redes para el gas de Fermi unitario, el acoplamiento se **ajusta a la unitariedad** haciendo que el espectro de dos cuerpos en la caja periódica coincida con los niveles universales de Lüscher en p cot δ = 0 (primera raíz η² ≈ −0.0959). Es la versión periódica de "y = 1/4 en el umbral". Reduce la originalidad del punto fijo. |
| T. Busch, B.-G. Englert, K. Rzażewski y M. Wilkens, "Two cold atoms in a harmonic trap", *Found. Phys.* **28**, 549–559 (1998), DOI 10.1023/A:1018705520999 | [V] (Springer, solo resumen) | Datos bibliográficos y resumen. La fórmula con funciones Γ y el valor E = ħω/2 en la unitariedad se leyeron en Stetcu et al. (siguiente fila), no en el original. |
| I. Stetcu, J. Rotureau, B. R. Barrett y U. van Kolck, "An effective field theory approach to two trapped particles", arXiv:1001.5071 | [V-arXiv] | Escriben la relación de Busch et al., Γ(3/4 − ε/2)/Γ(1/4 − ε/2) = b/(2a), y su corrección de rango efectivo; en la unitariedad el estado base de la trampa armónica tiene ε = 1/2. Es el análogo en trampa armónica de nuestro punto fijo, incluida la corrección por r_e. |

## Confinamiento esférico de potenciales apantallados

| Referencia | Estado | Qué se comprobó |
|---|---|---|
| A. K. Roy, "Spherical confinement of Coulombic systems inside an impenetrable box: H atom and the Hulthén potential", arXiv:1802.04373 | [V-arXiv] (sin journal-ref en arXiv) | Método pseudoespectral; H y Hulthén dentro de una esfera impenetrable; "radio crítico de la jaula" donde la energía cambia de signo. Mira la caja pequeña que desliga, no el cruce de cajas grandes cerca de un umbral de apantallamiento. |
| A. K. Roy, "Critical parameters and spherical confinement of H atom in screened Coulomb potential", arXiv:1904.11166 | [V-arXiv] (sin journal-ref visible) | (Revisión R2: un buscador da una versión en *Int. J. Quantum Chem.* (2016), DOI 10.1002/qua.25108, con el mismo título; la página del editor no abrió, [no verificada].) Parámetros críticos de Hulthén, Yukawa y ECSC **sin caja** (por cambio de signo de la energía); la parte confinada usa solo el ECSC en δ = 0.02 a 1 y radios de jaula hasta 50. No hay R²E, ni π²/8, ni cruces de cajas. |
| D. Djajaputra y B. R. Cooper, "Hydrogen atom in a spherical well: linear approximation", DOI 10.1088/0143-0807/21/3/309 (la revista, Eur. J. Phys., se deduce del DOI), arXiv:physics/9912031 | [V-arXiv] | H confinado; dependencia asintótica de la energía con el radio. Sin apantallamiento ni umbral. |
| "Sen et al." sobre confinamiento | [no verificada] | No encontramos en esta búsqueda un trabajo de Sen y colaboradores sobre el Yukawa confinado cerca del umbral; no se cita. |

## Rango efectivo y umbral

| Referencia | Estado | Qué se comprobó |
|---|---|---|
| H. A. Bethe, "Theory of the effective range in nuclear scattering", *Phys. Rev.* **76**, 38 (1949) | [no verificada] (referencia estándar, no se abrió) | Se usa la definición r_e = 2∫(ψ₀² − u₀²) dr; la comprobamos numéricamente con el pozo cuadrado (r_e = b en resonancia, `01_teoria.json`). |
| M. Klaus y B. Simon, *Ann. Phys.* **130**, 251 (1980) | [V] en `fase4/propuesta_originalidad/ideas_fase4_y_final.md`; no se volvió a abrir aquí | E ∝ (λ − λ_c)² en onda s, usado solo como contexto. |

## Qué se concluye sobre la originalidad (honesto)

1. **No es original**: la condición de cuantización en la esfera dura (método de la pared esférica, Borasoy et al. 2007), el
   uso de la energía de dos cuerpos en una caja en la unitariedad como valor universal para ajustar un acoplamiento (caja
   periódica, Lüscher y las redes del gas unitario; trampa armónica, Busch et al.), el cruce de curvas de dos tamaños como
   estimador del punto crítico (Nightingale; dos Santos y Sneddon), y el escalamiento de tamaño finito del umbral del
   Yukawa (con el tamaño de la base, Serra, Neirotti y Kais 1998) y con un radio de corte del potencial (Serra, PDF sin
   revista identificada).
2. **No lo encontramos en la búsqueda** (lo que puede ser nuevo, con esa salvedad): usar el cruce de 2R²E₀/π² y de ⟨r⟩/R
   en una **esfera de pared dura** para acotar el **apantallamiento crítico del Yukawa**; la ley δ*(R, 2R) − δ_c =
   π²r_e/(16cR²) + 3π²r_e²/(32cR³), que predice los cruces sin parámetros libres a partir de r_e y c a energía cero; el
   punto fijo 1/2 − 2/π² de la extensión y su coeficiente k₁; y su uso con una integral de camino como prueba de
   "artefacto o estado débil", con el corrimiento de la pared sin imagen incluido en la teoría.
3. La afirmación del documento de ideas ("no encontramos este uso para el Yukawa") se mantiene, pero hay que **matizar**
   "el punto fijo exacto 1/4 no apareció en nuestra búsqueda": su análogo periódico y el de la trampa armónica son
   conocidos y se usan para lo mismo (ubicar la unitariedad), y la ecuación que lo da es la del método de la pared esférica.
