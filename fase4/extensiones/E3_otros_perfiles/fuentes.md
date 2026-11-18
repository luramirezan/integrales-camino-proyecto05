# Fuentes de E3 (otros perfiles de apantallamiento) y su verificación

Verificación hecha el 17-11-2026 con búsqueda web y lectura directa de las páginas indicadas.
Marcas: **[V]** verificada en la página del editor, en el registro DOI o en un índice bibliográfico (Scilit) con DOI;
**[V-arXiv]** leída en arXiv, sin referencia de revista en la página; **[citada por Roy]** cifra o referencia que solo leímos
dentro de Roy 2019 (no abrimos el original); **[no verificada]**.

| # | Referencia | Estado | Qué se comprobó |
|---|---|---|---|
| 1 | A. K. Roy, "Critical parameters and spherical confinement of H atom in screened Coulomb potential", arXiv:1904.11166 (enviado el 25-04-2019) | [V-arXiv] | Leído el PDF. Ecuación 3: Hulthén −δe^{−δr}/(1−e^{−δr}), Yukawa −e^{−δr}/r, ECSC −e^{−δr}cos(δr)/r, en unidades atómicas (las nuestras con g = 1). Tabla I, 1s: Hulthén 2.00000000; Yukawa 1.190610; ECSC 0.7205240. El δ_c se obtiene "por el cambio de signo de la energía" al variar δ, así que sus cifras son truncadas. La página de arXiv no da revista ni DOI: no le atribuimos revista. |
| 2 | C. S. Lam y Y. P. Varshni, *Phys. Rev. A* **6**, 1391 (1972), "Bound eigenstates of the exponential cosine screened Coulomb potential", DOI 10.1103/PhysRevA.6.1391 | [V] (Scilit con DOI) | Es la referencia original del ECSC: δ_c del 1s por un variacional de dos parámetros (resumen). La cifra 0.7115 la leímos solo en la tabla de Roy [citada por Roy]. |
| 3 | C. S. Lam y Y. P. Varshni, *Phys. Rev. A* **4**, 1875 (1971), "Energies of s eigenstates in a static screened Coulomb potential", DOI 10.1103/PhysRevA.4.1875 | [V] (Scilit con DOI) | **Corrección:** este artículo es del Yukawa (potencial "estático apantallado"), no del ECSC. El encargo y la propuesta 4 lo citaban como referencia del perfil coseno; la del ECSC es la #2. |
| 4 | D. S. Singh y Y. P. Varshni, "Accurate eigenvalues and oscillator strengths for the exponential-cosine screened Coulomb potential", *Phys. Rev. A* **28**, 2606 (1983), DOI 10.1103/PhysRevA.28.2606 | [V] referencia (página de APS, revisión R3); cifra [citada por Roy] | Roy le atribuye δ_c(ECSC, 1s) = 0.72052408 (Tabla I, nota f, ref. [43]). El resumen de APS dice que da autovalores con 6 a 8 cifras. No abrimos el texto completo. |
| 5 | I. Nasser, M. S. Abdelmonem y A. Abdel-Hady, "J-Matrix approach for the exponential-cosine-screened Coulomb potential", *Phys. Scr.* **84**, 045001 (2011), DOI 10.1088/0031-8949/84/04/045001 | [V] referencia (repositorio KFUPM, revisión R3); cifra [citada por Roy] | Roy le atribuye 0.72055425 para el ECSC 1s (difiere de nuestro valor en 3×10⁻⁵). |
| 6 | O. A. Gomes, H. Chacham y J. R. Mohallem, "Variational calculations for the bound-unbound transition of the Yukawa potential", *Phys. Rev. A* **50**, 228 (1994), DOI 10.1103/PhysRevA.50.228 | [V] (Scilit con DOI, revisión R3) | El resumen da q_c = 1.190 612 27 ± 0.000 000 04, la misma cifra que cita Roy. Queda 1.5×10⁻⁷ por debajo de nuestro δ_c, unas 4 veces su barra. |
| 7 | C. Stubbins, "Bound states of the Hulthén and Yukawa potentials", *Phys. Rev. A* **48**, 220 (1993), DOI 10.1103/PhysRevA.48.220 | [V] (página de APS, revisión R3) | Variacional generalizado para Hulthén y Yukawa, estados hasta n = 6 (resumen). No citamos cifras suyas. |
| 8 | A. K. Roy, "The generalized pseudospectral approach to the bound states of Hulthén and Yukawa potentials", arXiv:1312.5900 | [V-arXiv] | Hulthén escrito igual que el nuestro; umbral 1s δ_c = 2.0 y Yukawa 1.1906. Sin revista en el texto leído. |
| 9 | A. K. Roy, "Studies on some exponential-screened Coulomb potentials", arXiv:1304.6928 | [V-arXiv] | Leído para buscar un cuarto perfil: su "GESC", −(1/r)[1 + (1 + br)e^{−2br}], conserva una cola −1/r y no tiene umbral; por eso no lo usamos. Cita δ_c(ECSC) ≈ 0.72. |
| 10 | H. A. Bethe, "Theory of the effective range in nuclear scattering", *Phys. Rev.* **76**, 38 (1949), DOI 10.1103/PhysRev.76.38 | [V] (Scilit con DOI) | Desarrollo de rango efectivo y fórmula r_e = 2∫(ψ² − φ²)dr que usamos. (Scilit pone por error "Physical Review B"; el DOI es de *Phys. Rev.*) |
| 11 | Potencial estático del átomo de hidrógeno 1s, V = −(1 + 1/r)e^{−2r} (u. a.) | [V], fuente docente | Problema 2 de la tarea 1 del curso AMO-2 (B. D. Esry, Kansas State University, 2007), phys.ksu.edu: "One model for e⁻ + H(1s) elastic scattering uses the following static interaction potential". Es un resultado de texto (potencial de Hartree del 1s); no encontramos en esta búsqueda un valor verificado de su longitud de dispersión. Nuestro perfil "átomo H" es −(1/r + δ/2)e^{−δr}, que en δ = 2 es exactamente ese potencial. |
| 12 | Fases 1–3 de este proyecto (`fase3/resultados/21_barrido.json`, `fase3/LEEME.md`) | interna | δ_c(Yukawa) = 1.1906124210606; ajuste κ = AΔ + BΔ² con A = 0.741131 (texto: 0.7411) y B = 0.05851. |
| 13 | Hulthén exacto: E = −(1/2)(1 − δ/2)², ⟨r⟩ = (12 − δ²)/(2(4 − δ²)) | interna (Fase 2, `radial.hulthen_exacto`, comprobado con sympy) | Lo usamos como control; el a(δ) con la función digamma lo dedujimos aquí y se comprueba numéricamente (control S2). |
| 14 | S. M. Ikhdair y R. Sever, "Bound state energies for the exponential cosine screened Coulomb potential", *Z. Phys. D* **28**, 1–5 (1993), DOI 10.1007/BF01437449 | [V] referencia (índice OUCI con DOI, revisión R3); cifra leída en el PDF del repositorio staff.najah.edu (texto OCR) | Tabla 1: λ_c(1s) = 0.720 524 085 88. Coincide con nuestro δ_c = 0.7205240858820 a 2×10⁻¹²; es la confirmación independiente más fuerte del umbral del ECSC. Cita a Singh y Varshni como ref. [17]. |

## Lo que no pudimos verificar

- Los valores de Singh y Varshni (1983) y Nasser et al. (2011) solo se leyeron en la tabla de Roy. El de Gomes et al. (1994) lo confirmó R3 en su resumen (Scilit).
- La revista donde se publicó Roy 2019 (arXiv:1904.11166): la página de arXiv no la indica.
- (Resuelto por R3) r_e = 3/δ_c del Hulthén: demostración analítica en la revisión.

## Añadido por la revisión R3 (17-11-2026)

- Roy 2019, Tabla I, imprime 1.190610 (Yukawa) y 0.7205240 (ECSC). La tabla 1 de la sección mostraba 1.19061 y 0.720524 porque el script borraba el cero final; ya está corregido. Roy también lista 0.7131 para el ECSC (nota e), que no usamos.
- La revisión no pudo abrir de nuevo la página de APS de Lam y Varshni (1972) ni la de Bethe (1949), porque el sitio respondió con error. Se mantienen las verificaciones por Scilit y DOI de la fila correspondiente, y Lam y Varshni (1971) quedó confirmada en APS como artículo del Yukawa.
- Hulthén: r_e(δ_c) = 3/δ_c y κ_v = δ/2 − 1 ya no necesitan referencia, porque se demuestran en `revision/informe_revision.md` (comprobación simbólica con sympy).

