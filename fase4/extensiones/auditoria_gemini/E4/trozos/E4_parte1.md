# Material para auditoría (parte 1 de 3)

Responde solo "Recibido" hasta la parte 3, que trae el encargo.

## Contexto

Proyecto de física teórica (curso universitario de integrales de camino). Potencial de Yukawa V(r) = −e^{−δr}/r en unidades ħ = m = g = 1, δ = μħ²/(mg). Esta parte del trabajo estudia cómo crece la extensión espacial de los estados 1s, 2s, 2p y 3d cerca de su umbral de enlace δ_c(n,ℓ), y una integral de camino en tiempo imaginario para la onda p. Te paso la teoría y la sección del artículo.

## teoria.md

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

La diferencia central entre ℓ = 0 y ℓ ≥ 1 está aquí: ∫ u₀² dr = ∫ A² r^{−2ℓ} dr converge en infinito si y solo si ℓ ≥ 1. Para ℓ ≥ 1 en el umbral hay un **autoestado normalizable de energía cero**; para ℓ = 0 solo hay una resonancia de energía cero (u₀ → constante). Esto es lo que Klaus y Simon (1980) formalizan para potenciales de corto alcance en 3D (ver `fuentes.md`).

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

**ℓ = 2.** La cola A² r^{−4} hace finitos ⟨r⟩₀ = ∫ r u₀² y ⟨r²⟩₀ = ∫ r² u₀² (solo ⟨r³⟩ diverge, y lo hace como logaritmo). Las correcciones salen de la cola:

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
- la variable con punto fijo es Y = 2R^{2ℓ+1}E/[(2ℓ+1)A²] → 1, con corrección O(1/R) para ℓ = 1 (la energía de la caja, O(1/R³), corrige la forma exterior en O(ER²) = O(1/R));
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

**La aproximación primitiva para el centrífugo** (opción (b): K_D e^{−U_0} e^{−ε[ℓ(ℓ+1)/(2r²)]/2} en cada extremo) también da un peso real, positivo y acotado (e^{−εc/r²} ≤ 1), pero es mala cerca del origen: e^{−ε/r²} suprime la región r ≲ ε^{1/2} de golpe, cuando el comportamiento correcto es la potencia r^{ℓ+1}. Los conmutadores de 1/r² con la cinética no están acotados y el error de Trotter deja de ser O(ε²); medimos un orden de 1.34 a 1.37 (script 45), compatible con ε^{4/3}.

**Opción (c), nodo fijo en z = 0 en 3D.** Restringir los caminos a z > 0 da el estado fundamental del sector impar en z, que para un potencial central es el ℓ = 1 más bajo: el nodo es exacto por simetría y el peso restringido es positivo. No la implementamos porque exige muestreo en 3D (barras estadísticas de 10⁻⁴ o peores, que no resuelven energías de 10⁻⁴ a 10⁻⁸ cerca del umbral) y la reducción radial (a) ya hace la misma restricción de forma exacta y determinista.

## seccion_articulo.md

# Extensión espacial cerca del umbral según el momento angular

## Motivación

En la Fase 3 medimos, para el estado 1s, que cerca de δ_c la energía cae como E ∝ −(δ_c − δ)² y que ⟨r⟩κ → 1/2: el estado se escapa al infinito. La pregunta de la guía, "examinar cómo crece la extensión espacial", tiene otra respuesta cuando el estado que se desliga tiene momento angular. La barrera centrífuga ℓ(ℓ+1)/(2r²) cambia la cola de la función de onda en el umbral de una constante a A r^{−ℓ}. Para ℓ ≥ 1 esa cola es de cuadrado integrable, de modo que en el umbral queda un estado normalizable de energía cero (Klaus y Simon, 1980). Las consecuencias son tres: la energía se anula linealmente en Δ = δ_c − δ; el radio medio de la onda p crece solo como un logaritmo; y una caja de Dirichlet da el signo correcto de E con radios mucho menores. Las medimos aquí para los umbrales 2s, 2p y 3d del Yukawa, con 1s como referencia.

## Método

**Umbrales.** δ_c es la raíz del coeficiente B de r^{ℓ+1} en la solución regular de energía cero (integrador DOP853, rtol = 10⁻¹³, arranque con 10 términos de la serie de Frobenius). Obtenemos δ_c(2s) = 0.3102092827139, δ_c(2p) = 0.2202168066066 y δ_c(3d) = 0.0913451207717, además de δ_c(1s) = 1.1906124210606. Los tres primeros coinciden con los valores de partida del encargo dentro de su redondeo a 8 decimales. Un segundo método, la recurrencia de energía cero de las mismas diferencias finitas con Richardson doble, los reproduce con diferencias de 1.8×10⁻¹³ (2p), 1.3×10⁻¹³ (3d) y 2.2×10⁻¹¹ (2s). Serra, Neirotti y Kais (1998) dan λ_c = 1/δ_c = 4.540980(3) para ℓ = 1; nuestro valor es 1/0.2202168066 = 4.5409800.

**Solucionadores.** (i) El de diferencias finitas de la Fase 2 (`radial.py`, sin modificar), al que basta pasarle el potencial efectivo V + ℓ(ℓ+1)/(2r²). En Coulomb da E(2p) y E(3d) con errores de 3.9×10⁻¹¹ y 9×10⁻¹³ (h = 1/40 con Richardson) y orden de malla 2.000. (ii) Un disparo sin caja: integración hacia afuera desde la serie de Frobenius y hacia adentro desde r_ext = 42/δ, donde se impone la solución exterior exacta e^{−κr} Σ_j c_j r^{−j} (Bessel esférica modificada). Las colas de ⟨r⟩ y ⟨r²⟩ más allá de r_ext se suman en forma cerrada. En Coulomb reproduce E_n = −1/(2n²) a 10⁻¹⁵ y ⟨r⟩ a 10⁻¹². Los barridos usan (ii), que no tiene caja ni malla; (i) los confirma en puntos sueltos.

**Integral de camino para ℓ = 1.** Ampliamos la matriz de transferencia de la Fase 2 a la onda p:

  T_ij = h K₁(r_i, r_j; ε) e^{−U₁(r_i, r_j; ε)} e^{−ε[W(r_i) + W(r_j)]/2}.

Aquí K₁ es el núcleo libre exacto de la onda p, √(rr′)/ε · Ĩ_{3/2}(rr′/ε) e^{−(r−r′)²/(2ε)}, y lleva la barrera centrífuga sin aproximación. U₁ es la acción de pares exacta del Coulomb en la onda p, tabulada como en la Fase 2 (red fina con el mismo centrífugo y Richardson entre h_tab = 0.01 y 0.005). W = (1 − e^{−δr})/r es el resto acotado. El peso es real, positivo y normalizable: K₁ > 0, e^{−U₁} > 0, no aparece ningún elemento de la red ≤ 0 y el autovector dominante tiene signo constante en todas las corridas. La singularidad r^{−2} es repulsiva y solo suprime el peso cerca del origen. Comparamos con la alternativa (b), que usa la acción de pares de ℓ = 0 y trata ℓ(ℓ+1)/(2r²) con la aproximación primitiva. La receta de extrapolación y de errores es la de la Fase 3.

## Resultados

**Energía (figura 46_energia_umbral).** En las dos últimas décadas de cada barrido (Δ/δ_c hasta 10⁻⁷ en ℓ = 0 y hasta 10⁻⁹ en ℓ ≥ 1), el exponente de |E| frente a Δ sale 2.0000003 ± 7×10⁻⁷ (1s), 2.0000007 ± 1.6×10⁻⁶ (2s), 1.00009 ± 1.1×10⁻⁴ (2p) y 0.9999999 ± 5×10⁻⁷ (3d). Los coeficientes se predicen sin ajuste a partir de la solución de energía cero:

- ℓ = 0: κ/Δ → c₀ = 2∫e^{−δ_c r}ū₀² dr, que vale 0.741192 (1s, medido 0.741192; es el 0.741 de la Fase 3) y 1.316956 (2s).
- ℓ ≥ 1: −E/Δ → S = ⟨e^{−δ_c r}⟩₀ (Hellmann–Feynman), con S = 0.126016 (2p, medido 0.126022) y 0.221917 (3d, medido 0.221917).

En 2p la diferencia de 5×10⁻⁵ es la corrección (A²/2)(2SΔ)^{3/2} predicha. Con ella, el error en el último punto baja a 1.7×10⁻⁶.

**Extensión (figura 46_extension_vs_kappa).** Para ℓ = 0, ⟨r⟩ ∝ κ^{−1.00000} y ⟨r²⟩ ∝ κ^{−2.00000}, con ⟨r⟩κ = 0.5000001 y ⟨r²⟩κ² = 0.5000001 en 1s. Para ℓ = 1, ⟨r²⟩ ∝ κ^{−0.99992 ± 0.0001} y ⟨r²⟩κ → 5A²/4 = 8.2627 (medido 8.2629). Para ℓ = 2, ⟨r⟩ y ⟨r²⟩ quedan finitos: exponentes de −0.000002 ± 0.000005 y −0.0005 ± 0.0006, ⟨r⟩ → 21.6161 y ⟨r²⟩ → 766.9. La pendiente de ⟨r²⟩ frente a κ, −16131, coincide con −(35/36)A² = −16133.

**El logaritmo de la onda p (figura 46_log_onda_p).** ⟨r⟩ crece de 8.6 a 64.5 mientras κ baja de 0.095 a 7.5×10⁻⁶. No es una potencia: el exponente local d ln⟨r⟩/d ln(1/κ) baja de forma monótona de 0.39 a 0.10, y un ajuste de potencia da 0.29 en la primera mitad del barrido y 0.14 en la segunda. En cambio, ⟨r⟩ es lineal en ln(1/κ), con pendiente 6.597 ± 0.001. La teoría predice que esa pendiente es la amplitud de la cola de la solución de energía cero normalizada, A² = 6.610 (diferencia del 0.2 %, que es la corrección O(κ ln κ) dentro de la ventana). La fórmula completa, ⟨r⟩ = {C₀ + A²[ln(1/κ) + 5/4 − γ − ln 2]}(1 + 3A²κ/2), con C₀ calculado en el umbral y sin ningún parámetro libre, reproduce ⟨r⟩ con un error relativo máximo de 2.3×10⁻⁷ en la ventana asintótica.

**Cajas (figura 46_cajas_l).** Justo en δ_c, la energía de la caja del 1s cumple 2R²E/π² → 1/4 (0.25017 en R = 2560). Para 2p y 3d esa misma variable tiende a 0, porque el estado de energía cero no llega a la pared. La ley derivada, E(R) = (2ℓ+1)A²/(2R^{2ℓ+1}), da Y = 2R^{2ℓ+1}E/[(2ℓ+1)A²] → 1, con valores 1.0047 (2p) y 1.000006 (3d) en R = 2560. La corrección de 2p decae como R^{−1.03} (predicha R^{−1}). El radio de caja en que el nivel cruza E = 0 sigue R_c ∝ Δ^{−1}, Δ^{−1/3} y Δ^{−1/5} para ℓ = 0, 1 y 2. Para ℓ ≥ 1 el coeficiente predicho, ((2ℓ+1)A²/2S)^{1/(2ℓ+1)}, acierta al 8×10⁻⁴ o mejor desde Δ/δ_c = 10⁻⁴. En la práctica, con R = 100 el signo de E es fiable desde Δ/δ_c = 1.1×10⁻² en 1s, pero ya desde 3.6×10⁻⁴ en 2p y 2.0×10⁻⁴ en 3d. Con Δ/δ_c = 10⁻³, R = 100 da E < 0 para 2p y 3d y E > 0 (signo equivocado) para 1s, que necesita R > 1134. El cruce de las curvas y(δ) de las cajas R y 2R converge a δ_c desde el lado no ligado y su valor y* tiende a 0 como R^{1−2ℓ}. Con R = 160 coincide con la predicción asintótica al 9 % (2p) y al 0.5 % (3d).

**Integral de camino (figura 46_integral_camino_l1).** Con el método (a), los seis casos (Coulomb 2p y δ = 0.10, 0.16, 0.20, 0.215 y 0.219) son compatibles con el radial en la misma caja. Coulomb da E = −1/8 + 5×10⁻¹¹. Para δ ≤ 0.20 la diferencia es de 6×10⁻¹¹ con barras de 1 a 3×10⁻¹¹ más el error del radial. El orden de Trotter es 2.00. En δ = 0.215 y 0.219 la barra (4×10⁻⁹ y 3×10⁻⁸) la domina la pared sin imagen en R = 100, como en la Fase 3: el orden aparente baja a 1.94 y 1.61, y vuelve a 2.00 al comparar con el radial en R + 0.5826√ε. El método (b) primitivo converge con orden 1.34 a 1.37. Su sesgo con ε = 0.1 va de 0.18 % (Coulomb) a 23 % (δ = 0.219) de |E|, y tras extrapolar con su orden medido aún difiere del radial hasta un 0.1 %. Las diferencias entre las mallas h = 0.04, 0.02 y 0.01 son de 2×10⁻¹¹ o menos, al nivel de la precisión del autovalor.

## Discusión

La tabla de la propuesta se cumple en todos sus renglones y con los coeficientes, no solo con los exponentes. Todo sale de dos números de la solución de energía cero: la amplitud de su cola A² y su "peso dentro del potencial" S (o Σ para ℓ = 0). El punto fino es el logaritmo de la onda p. Un ajuste de potencia en cualquier ventana daría un exponente entre 0.1 y 0.4 que depende de la ventana; solo la gráfica contra ln(1/κ) y la pendiente A², fijada de antemano, distinguen el logaritmo de una potencia pequeña. La corrección de norma (1 + 3A²κ/2) es necesaria para pasar del 7×10⁻⁴ al 2×10⁻⁷.

Para la prueba de cajas de las Fases 2 y 3, la consecuencia práctica es que el criterio de signo, que para el 1s exige R > a_s ∝ 1/Δ, para ℓ ≥ 1 se cumple con cajas de R ∝ Δ^{−1/(2ℓ+1)}. El punto fijo 1/4 de 2R²E/π² es propio de ℓ = 0; para ℓ ≥ 1 la variable de escala correcta es R^{2ℓ+1}E. En la integral de camino, la barrera centrífuga no exige muestreo especial si se incluye exactamente en el núcleo libre de la onda parcial. Tratarla con la aproximación primitiva degrada el orden de Trotter de 2 a cerca de 4/3.

Limitaciones: el método (a) se probó solo para ℓ = 1, aunque el código admite cualquier ℓ. Las tablas de la onda p tienen un error de red de hasta 1.3×10⁻⁴ en U₁, en el primer nodo (r = 0.01), donde la densidad es ∝ r⁴. La comparación con la integral de camino cerca del umbral (δ = 0.219) queda limitada por la pared.

## Referencias

- M. Klaus y B. Simon, "Coupling constant thresholds in nonrelativistic quantum mechanics. I. Short-range two-body case", Ann. Phys. 130, 251–281 (1980), DOI 10.1016/0003-4916(80)90338-3.
- P. Serra, J. P. Neirotti y S. Kais, "Finite-size scaling approach for the Schrödinger equation", Phys. Rev. A 57, R1481 (1998).
- K. Riisager, "Halos and related structures", Phys. Scr. T152, 014001 (2013), arXiv:1208.6415.
- A. S. Jensen, K. Riisager, D. V. Fedorov y E. Garrido, "Structure and reactions of quantum halos", Rev. Mod. Phys. 76, 215 (2004).
- T. Misu, W. Nazarewicz y S. Åberg, "Deformed nuclear halos", arXiv:nucl-th/9612016, DOI 10.1016/S0375-9474(96)00458-7.
