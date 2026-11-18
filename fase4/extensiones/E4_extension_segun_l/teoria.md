# Teoría de E4: cómo crece la extensión espacial cerca del umbral según el momento angular ℓ

Unidades ħ = m = g = 1, potencial de Yukawa V(r) = −e^{−δr}/r, onda parcial ℓ con u(r) = r R(r):

  −u''/2 + [V(r) + ℓ(ℓ+1)/(2r²)] u = E u,  u(0) = 0,  κ = (−2E)^{1/2},  Δ = δ_c − δ > 0 (lado ligado).

Las constantes numéricas que aparecen al final de cada apartado salen de `resultados/41_constantes_umbral.json`; la comparación con los barridos está en `seccion_articulo.md` y `controles.md`.

## 1. La solución fuera del potencial

El potencial de Yukawa decae como e^{−δr}; a partir de r_ext = 42/δ vale menos de 6×10⁻¹⁹ en unidades del problema y se puede despreciar. Allí la ecuación es la libre con barrera centrífuga, cuyas soluciones son r i_ℓ(κr) y r k_ℓ(κr) (Bessel esféricas modificadas). La que decae es

  u(r) ∝ r k_ℓ(κr) ∝ e^{−κr} Σ_{j=0}^{ℓ} b_j (κr)^{−j},  b_j = (ℓ+j)! / [j! (ℓ−j)! 2^j].

Para ℓ = 0, 1, 2 da e^{−x}, e^{−x}(1 + 1/x) y e^{−x}(1 + 3/x + 3/x²), con x = κr. Normalizada para que coincida con A r^{−ℓ} cuando κr ≪ 1, escribimos

  u(r) = A r^{−ℓ} f_ℓ(κr),  f_0 = e^{−x},  f_1 = (1 + x) e^{−x},  f_2 = (1 + x + x²/3) e^{−x}.   (1)

## 2. La solución de energía cero y el umbral

A E = 0, lejos del potencial, u = A r^{−ℓ} + B r^{ℓ+1}. El coeficiente B depende de δ; el umbral δ_c es la raíz B(δ_c) = 0, porque entonces la solución regular solo tiene la parte que decae (para ℓ = 0, la parte "constante" A; es la condición de longitud de dispersión infinita de las Fases 1 a 3). El script 40 calcula δ_c así para 1s, 2s (segundo cero de B, con un nodo), 2p y 3d.

La diferencia central entre ℓ = 0 y ℓ ≥ 1 está aquí: ∫ u₀² dr = ∫ A² r^{−2ℓ} dr converge en infinito si y solo si ℓ ≥ 1. Para ℓ ≥ 1 en el umbral hay un **autoestado normalizable de energía cero**; para ℓ = 0 solo hay una resonancia de energía cero (u₀ → constante). El marco general (umbrales de constante de acoplamiento para potenciales de corto alcance, con resultados que dependen de la dimensión) es el de Klaus y Simon (1980), cuyo texto completo no pudimos leer; los exponentes α = 2 (ℓ = 0) y α = 1 (ℓ ≠ 0) del Yukawa los da explícitamente Serra, Neirotti y Kais (1998) (ver `fuentes.md`). [Corregido en la revisión R4, hallazgo R4-06.]

Para ℓ ≥ 1 definimos la solución de energía cero normalizada u₀ (∫u₀² = 1), su amplitud de cola A² ≡ An2 (u₀ → A r^{−ℓ}) y

  S = ∫₀^∞ e^{−δ_c r} u₀² dr.

Para ℓ = 0 definimos ū₀ con ū₀ → 1 lejos y Σ = ∫₀^∞ e^{−δ_c r} ū₀² dr.

## 3. La energía cerca del umbral (Hellmann–Feynman)

Como ∂V/∂δ = e^{−δr} > 0, el teorema de Hellmann–Feynman da

  dE/dδ = ⟨e^{−δr}⟩ > 0.   (2)

**ℓ ≥ 1.** En el umbral el estado normalizado tiende a u₀, de modo que dE/dδ → S, que es finito y positivo. Integrando,

  E(δ) = −S Δ + o(Δ),  exponente α = 1.   (3)

La pendiente S no se ajusta: es una integral de la solución de energía cero.

**ℓ = 0.** El estado normalizado tiene casi todo su peso en la cola e^{−κr}, con amplitud u ≈ (2κ)^{1/2} ū₀ dentro del potencial (apartado 4), así que dE/dδ ≈ 2κΣ → 0: la pendiente se anula en el umbral. La identidad del wronskiano entre las soluciones de energía cero en δ y δ + dδ, W' = 2(V₂ − V₁) u₁u₂, integrada de 0 a ∞ con u_i → 1 − r/a_i, da

  d(1/a_s)/dδ = −2Σ,

con a_s > 0 del lado ligado (la convención de las Fases 1 a 3). Como κ = 1/a_s + O(1/a_s²), κ ≈ c₀Δ con

  c₀ = 2Σ,  E ≈ −(c₀Δ)²/2,  α = 2.   (4)

Las dos cuentas son coherentes: con E = −κ²/2, dE/dδ = −κ dκ/dδ = κc₀ = 2κΣ.

**Corrección siguiente para ℓ = 1.** La norma del estado con κ > 0 difiere de la de u₀ en la cola: N_κ − 1 = A² ∫ r^{−2}[f₁(κr)² − 1] dr = A² κ I_N, con

  I_N = ∫₀^∞ [(1+x)² e^{−2x} − 1]/x² dx = −3/2

(integrando por partes: el término de borde se anula y queda ∫₀^∞ −2(1+x) e^{−2x} dx = −3/2). Así ⟨e^{−δr}⟩ = S(1 + (3/2)A²κ) + O(κ²), y con −κ dκ/dδ = S(1 + (3/2)A²κ):

  |E| = S Δ + (A²/2)(2SΔ)^{3/2} + O(Δ²).   (5)

El término Δ^{3/2} es el κ³ del desarrollo de alcance efectivo de la onda p. Para ℓ = 2 la corrección de la norma es O(κ²) y |E| = SΔ + O(Δ²).

## 4. Los momentos ⟨r⟩ y ⟨r²⟩

Separamos el interior (r < L, con L más allá del alcance del potencial pero κL ≪ 1), donde u ≈ u₀, de la cola (1).

**ℓ = 0.** La norma la domina la cola: A_κ² ∫ e^{−2κr} dr = A_κ²/(2κ) ≈ 1, así que A_κ² ≈ 2κ y

  ⟨r⟩ ≈ 2κ ∫₀^∞ r e^{−2κr} dr = 1/(2κ),  ⟨r²⟩ ≈ 2κ ∫₀^∞ r² e^{−2κr} dr = 1/(2κ²).   (6)

Con κ ∝ Δ: ⟨r⟩ ∝ Δ^{−1}, ⟨r²⟩ ∝ Δ^{−2}. Es el ⟨r⟩κ → 1/2 de la Fase 3.

**ℓ = 1.** La norma es finita (A² en la cola es un número fijo), pero ⟨r⟩ = ∫ r u² dr recibe de la cola ∫ A² f₁(κr)²/r dr, que es logarítmica:

  ∫_L^∞ A² f₁(κr)²/r dr = A² [E₁(2κL) + e^{−2κL}(1 + …) + 1/4 + …] → A² [ln(1/(κL)) − γ − ln 2 + 5/4],

usando ∫(1+x)² e^{−2x}/x dx = E₁(2x₀) + 1 + 1/4 + O(x₀) y E₁(z) = −γ − ln z + O(z). Con el interior ∫₀^L r u₀² dr = C₀ + A² ln L, donde

  C₀ = lim_{L→∞} [∫₀^L r u₀² dr − A² ln L],

el ln L se cancela y queda

  ⟨r⟩ = C₀ + A² [ln(1/κ) + 5/4 − γ − ln 2] + O(κ ln κ).   (7)

El **coeficiente del logaritmo es la amplitud de la cola de la solución de energía cero normalizada**, A². La corrección O(κ ln κ) viene de la norma: dividiendo por N_κ = 1 − (3/2)A²κ,

  ⟨r⟩ ≈ {C₀ + A²[ln(1/κ) + 5/4 − γ − ln 2]} (1 + (3/2)A²κ).   (7')

Para ⟨r²⟩ la cola da A² ∫ f₁(κr)² dr = (A²/κ) ∫₀^∞ (1+x)² e^{−2x} dx = 5A²/(4κ), luego

  ⟨r²⟩ = 5A²/(4κ) + D₀ + (15/8)A⁴ + O(κ ln κ),  D₀ = lim [∫₀^L r² u₀² dr − A² L].   (8)

Con κ ∝ Δ^{1/2}: ⟨r²⟩ ∝ Δ^{−1/2}, pero ⟨r⟩ no es una potencia de κ: su exponente local d ln⟨r⟩/d ln(1/κ) = A²/⟨r⟩ baja a cero como 1/ln(1/κ). Un ajuste de potencia en una ventana finita da un "exponente" que depende de la ventana; eso es lo que se comprueba en el script 42.

**ℓ = 2.** La cola A² r^{−4} hace finitos ⟨r⟩₀ = ∫ r u₀² y ⟨r²⟩₀ = ∫ r² u₀² (⟨r^n⟩ diverge para n ≥ 3: como logaritmo en n = 3 y como κ^{3−n} para n > 3; corregido en la revisión R4, hallazgo R4-05). Las correcciones salen de la cola:

  ⟨r²⟩ = ⟨r²⟩₀ + A² κ I₂ + O(κ²),  I₂ = ∫₀^∞ [f₂² − 1]/x² dx = −35/36,   (9)

(por partes: f₂' = −(x/3)(1+x)e^{−x}, I₂ = −(2/3)∫₀^∞ (1+x)(1+x+x²/3) e^{−2x} dx = −(2/3)(35/24)), y ⟨r⟩ = ⟨r⟩₀ − (A²/3) κ² ln(1/κ) + O(κ²), porque f₂² − 1 ≈ −x²/3 cerca de x = 0.

**Resumen de la predicción:**

| | E cerca del umbral | ⟨r⟩ | ⟨r²⟩ |
|---|---|---|---|
| ℓ = 0 | −(c₀Δ)²/2, c₀ = 2Σ | 1/(2κ) | 1/(2κ²) |
| ℓ = 1 | −SΔ − (A²/2)(2SΔ)^{3/2} | A² ln(1/κ) + C₀ + A²(5/4 − γ − ln 2) | 5A²/(4κ) |
| ℓ = 2 | −SΔ + O(Δ²) | ⟨r⟩₀ − (A²/3)κ² ln(1/κ) | ⟨r²⟩₀ − (35/36)A²κ |

Constantes calculadas en el umbral (script 41, en las unidades del problema): 1s: Σ = 0.37060, c₀ = 0.74119; 2s: Σ = 0.65848, c₀ = 1.31696; 2p: A² = 6.6102, S = 0.12602, C₀ = −13.428, D₀ = −57.577; 3d: A² = 16594, S = 0.22192, ⟨r⟩₀ = 21.616, ⟨r²⟩₀ = 766.89. El 3d tiene una cola enorme (A² grande) porque es un estado extendido; aun así sus momentos son finitos.

**Relación con la fórmula de Riisager (2013), ec. (4).** Allí ⟨r^n⟩ ∝ (μB)^{(2ℓ−1−n)/2} para n > 2ℓ − 1, logaritmo para n = 2ℓ − 1 y constante para n < 2ℓ − 1. Es la integral de la cola con la amplitud interior fija. Para ℓ ≥ 1 la norma es finita y la fórmula da directamente ⟨r²⟩ ∝ B^{−1/2} (ℓ = 1), ⟨r⟩ ∝ ln (ℓ = 1, n = 1 = 2ℓ − 1) y valores finitos para ℓ = 2. Para ℓ = 0 la propia norma (n = 0) diverge como B^{−1/2} y hay que dividir por ella: ⟨r^n⟩ ∝ B^{−n/2}, es decir ⟨r²⟩ ∝ 1/κ². Lo comprobamos en el barrido 1s y 2s.

## 5. Qué ve una caja de Dirichlet

Sea E(R) el nivel de la caja [0, R] con u(R) = 0. Para u normalizada,

  dE/dR = −u'(R)²/2   (fórmula de Hadamard, ħ = m = 1).   (10)

**En el umbral, ℓ ≥ 1.** Para R grande el estado de la caja es casi la solución de energía cero que se anula en R: fuera del potencial, u ≈ A (r^{−ℓ} − r^{ℓ+1}/R^{2ℓ+1}), y la norma sigue siendo 1 hasta O(R^{−(2ℓ−1)}). Entonces u'(R) = −(2ℓ+1) A R^{−ℓ−1} y, integrando (10) desde R hasta infinito (donde E = 0):

  E(R) = (2ℓ+1) A² / (2 R^{2ℓ+1}) [1 + O(R^{1−2ℓ})].   (11)

ℓ = 1 da 3A²/(2R³) y ℓ = 2 da 5A²/(2R⁵). Por tanto:

- la variable de la Fase 2, y = 2R²E/π², **no** tiene punto fijo 1/4 en el umbral para ℓ ≥ 1: tiende a 0 como R^{1−2ℓ};
- la variable con punto fijo es Y = 2R^{2ℓ+1}E/[(2ℓ+1)A²] → 1, con corrección O(1/R) para ℓ = 1 (la energía de la caja, O(1/R³), corrige la forma exterior en O(ER²) = O(1/R)). La revisión R4 calculó el coeficiente: la norma de u ≈ A(r^{−1} − r²/R³) dentro de la caja es 1 − (9/5)A²/R, y la corrección de energía de la forma exterior, u ≈ A[r^{−1}(1 + k²r²/2) − βr²(1 − k²r²/10)], añade a u'(R)² un factor 1 + (3/5)A²/R; integrando (10), Y = 1 + (9/5)A²/R + O(R^{−2}). Con A² = 6.6102 da Y(2560) = 1.004648, frente a 1.004665 medido (`revision/r43_cajas.json`);
- para ℓ = 0, en cambio, u₀ → constante, la caja impone sen(kr + π/2) y E(R) = π²/(8R²) (y → 1/4).

**Radio de caja en el que el nivel cruza E = 0.** Por el teorema de oscilación, el nivel de la caja vale E = 0 exactamente cuando R coincide con el último nodo de la solución regular de energía cero. Del lado ligado:

- ℓ = 0: u₀ ∝ r − a_s, el nodo está en R_c = a_s ≈ 1/(c₀Δ);
- ℓ ≥ 1: u₀ = A r^{−ℓ} + B r^{ℓ+1}, con B/A = −2SΔ/[(2ℓ+1)A²] (wronskiano entre δ_c y δ, igual que en el apartado 3), y el nodo está en

  R_c^{2ℓ+1} = (2ℓ+1) A² / (2SΔ),   (12)

que coincide con poner −SΔ + (2ℓ+1)A²/(2R^{2ℓ+1}) = 0 en (3) + (11). Con R > R_c la caja ya da E < 0 (signo correcto). Así R_c ∝ Δ^{−1} para ℓ = 0, ∝ Δ^{−1/3} para ℓ = 1 y ∝ Δ^{−1/5} para ℓ = 2: **el signo de la energía en una caja moderada es fiable mucho más cerca del umbral para ℓ ≥ 1**. Del lado no ligado la caja solo sube la energía, así que E(R) > 0 siempre: allí el signo nunca engaña.

**Cruce de las curvas y(δ) de dos cajas (R y 2R).** Con E(R, δ) ≈ −SΔ + c R^{−(2ℓ+1)}, c = (2ℓ+1)A²/2, igualar R²E(R) = (2R)²E(2R) da

  δ* − δ_c = c (1 − 2^{1−2ℓ}) / (3 S R^{2ℓ+1}),  y* = (2c/π²) R^{1−2ℓ} [1 + (1 − 2^{1−2ℓ})/3].   (13)

El cruce converge a δ_c como R^{−(2ℓ+1)} (desde el lado no ligado) y el valor del cruce tiende a 0, no a 1/4. Que el valor del cruce dependa de ℓ es otra señal de que el cruce mide la física del estado y no un artefacto de la caja.

## 6. Integral de camino para ℓ ≥ 1: el núcleo libre de la onda parcial y el peso

El propagador libre en 3D, (2πε)^{−3/2} e^{−|x−x'|²/(2ε)}, se desarrolla en ondas parciales con e^{z cos θ} = Σ (2ℓ+1) i_ℓ(z) P_ℓ(cos θ), z = rr'/ε. Para u = rR con medida dr, el núcleo libre de la onda ℓ es

  K_ℓ(r, r'; ε) = 4π r r' (2πε)^{−3/2} e^{−(r²+r'²)/(2ε)} i_ℓ(rr'/ε) = (rr')^{1/2} ε^{−1} Ĩ_{ℓ+1/2}(rr'/ε) e^{−(r−r')²/(2ε)},

con Ĩ_ν(z) = I_ν(z) e^{−z} (la función `ive` de scipy). Para ℓ = 0 se reduce al núcleo con imagen K_D de la Fase 2 (se comprueba en el script 44 a 3×10⁻¹⁴). K_ℓ lleva la barrera centrífuga **exacta**: ningún error de Trotter viene de ella. La acción de pares U_ℓ = −ln(ρ_ℓ/K_ℓ) del Coulomb en la onda ℓ se calcula en una red fina dividiendo por el núcleo libre de la misma red (con el mismo centrífugo), como en `pares.py`.

**¿El peso es real, positivo y normalizable?** Sí. El operador −½d² + ℓ(ℓ+1)/(2r²) − 1/r en la semirrecta genera un semigrupo cuyo núcleo es positivo (fórmula de Feynman–Kac para el proceso radial con muerte por −V; en la red, porque la matriz tridiagonal tiene elementos fuera de la diagonal negativos). K_ℓ > 0 y e^{−U_ℓ} > 0, de modo que T_ij ≥ 0, real y simétrica; su autovector dominante tiene signo constante. La singularidad r^{−2} del centrífugo es **repulsiva**: no hace crecer el peso, lo suprime cerca del origen (K_ℓ ∝ (rr')^{ℓ+1}), así que la normalización no tiene problema. La singularidad −1/r ya se trataba con la acción de pares en la Fase 2.

**La aproximación primitiva para el centrífugo** (opción (b): K_D e^{−U_0} e^{−ε[ℓ(ℓ+1)/(2r²)]/2} en cada extremo) también da un peso real, positivo y acotado (e^{−εc/r²} ≤ 1), pero es mala cerca del origen: e^{−ε/r²} suprime la región r ≲ ε^{1/2} de golpe, cuando el comportamiento correcto es la potencia r^{ℓ+1}. Los conmutadores de 1/r² con la cinética no están acotados y el error de Trotter deja de ser O(ε²); medimos un orden de 1.34 a 1.37 (script 45) entre ε = 0.2 y 0.05. [Corregido en la revisión R4, hallazgo R4-03: la versión anterior decía "compatible con ε^{4/3}" sin derivarlo.] Un argumento heurístico da ε^{3/2}: el núcleo primitivo solo se equivoca en r ≲ ε^{1/2}, donde la densidad de la onda p pesa ∫₀^{√ε} r⁴ dr ∝ ε^{5/2} por paso, es decir ε^{3/2} por unidad de tiempo. Con ε = 0.1, 0.05, 0.025 y 0.0125 la revisión mide órdenes locales de 1.37, 1.39 y 1.41, que crecen hacia 3/2 (`revision/r45_camino_independiente.json`).

**Opción (c), nodo fijo en z = 0 en 3D.** Restringir los caminos a z > 0 da el estado fundamental del sector impar en z, que para un potencial central es el ℓ = 1 más bajo: el nodo es exacto por simetría y el peso restringido es positivo. No la implementamos porque exige muestreo en 3D (barras estadísticas de 10⁻⁴ o peores, que no resuelven energías de 10⁻⁴ a 10⁻⁸ cerca del umbral) y la reducción radial (a) ya hace la misma restricción de forma exacta y determinista.
