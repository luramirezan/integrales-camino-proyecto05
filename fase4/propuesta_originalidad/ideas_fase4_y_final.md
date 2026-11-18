---
title: "Proyecto 05 · Qué se ha hecho y qué podemos hacer original en la Fase 4 y la fase final"
---

# Qué se ha hecho sobre el umbral del Yukawa y qué podemos aportar de original

*Búsqueda bibliográfica y propuestas para la Fase 4 y la entrega final · 15-11-2026 · preparado con Claude (IA) para el equipo (Juan Sebastián Calixto y Luis Felipe Ramírez).*

## Resumen en cinco líneas

1. El valor de $\delta_c\approx1.19061$ y los métodos para calcularlo (perturbación, Padé, supersimetría, variacional, pseudoespectral, Monte Carlo hamiltoniano y de línea de mundo) están muy trabajados. **Otra cifra de $\delta_c$ no sería original.**
2. Lo que casi no encontramos es justo lo que pide la guía: **una prueba de caja que decida "ligado o artefacto"** usando solo cajas finitas, y un estudio de **cómo crece la extensión** que distinga los casos.
3. Propuesta principal (ya probada aquí en 15 minutos de cómputo): **el criterio de cruce de cajas.** En el umbral, $2R^2E_0(R)/\pi^2\to1/4$ para cualquier potencial de corto alcance. Las curvas de distintas $R$ se cruzan en $\delta_c$. Con $R\le800$ da $\delta_c=1.190622\to1.1906124$ tras extrapolar, cuando el signo de $E_0$ necesitó $R=12800$ para decir solo $1.19<\delta_c<1.20$.
4. Segunda línea: **la extensión depende de $\ell$.** En $s$, $\langle r\rangle\propto1/\kappa$. En $p$, $\langle r\rangle$ crece solo como $\ln(1/\kappa)$. En $d$, queda finita. La prueba de caja tiene que cambiar con $\ell$, y eso se puede mostrar con el mismo código.
5. Opción ambiciosa para la final: un **criterio de umbral sin caja hecho con caminos brownianos** (la *gauge* de Feynman–Kac, que da la longitud de dispersión). Encontramos una obstrucción que, hasta donde buscamos, nadie ha señalado para este problema: **la varianza del estimador es infinita en toda la ventana $\delta_c<\delta<2\delta_c$.** Sirve tanto de resultado como de motivación para un muestreo por importancia.

---

## 1. Qué piden la Fase 4 y la entrega final

De la guía del curso (`enunciado/guia_texto.txt`, proyecto 05 y párrafo general de fases):

- **Fase 4:** "acotar el umbral y examinar cómo crece la extensión espacial; escribir el artículo". La Fase 4 también "permite responder objeciones, ejecutar una ampliación y corregir el texto".
- **Punto de llegada:** "un intervalo defendible para $\mu_c$ y gráficas de energía y radio característico".
- **Segunda presentación:** "debe mostrar la prueba de caja que separa un estado débil de un artefacto".
- **Ampliación sugerida:** "cambiar el perfil de apantallamiento o comparar un criterio variacional".
- **Entregables:** curvas de energía y extensión frente al apantallamiento, comparación de varias cajas y cota documentada para el umbral. Artículo final de 10 a 12 páginas, repositorio y defensa individual.
- **Advertencia de la guía:** no reclamar "una cifra universal desligada de las unidades y parámetros"; un potencial suavizado lleva su parámetro declarado.

Lo que ya tenemos (Fases 1 a 3): cotas $1.19055\le\delta_c\le1.24305$; radial e integral de camino con acción de pares coincidiendo a $10^{-8}$; barrido en $\delta$; 35 celdas de cajas; $1.19<\delta_c<1.20$ con dos métodos; $1.1906<\delta_c<1.1907$ por energía cero; $\kappa\simeq0.741\,(\delta_c-\delta)$ y $\langle r\rangle\kappa\to1/2$; auditoría adversarial con Gemini.

**Conclusión para elegir:** la Fase 4 obligatoria ya está casi cubierta en números. Lo que falta, y donde cabe lo original, es **(i) una prueba de caja más fina que el signo del autovalor y (ii) un estudio de la extensión que diga algo más que $\langle r\rangle\kappa\to1/2$.**

---

## 2. Estado del arte (lo que encontramos y verificamos)

Marcamos cada fuente: **[V]** = verificada en la página del editor, arXiv o un índice bibliográfico durante esta búsqueda; **[V-arXiv]** = verificada en arXiv, revista por confirmar; **[conocida]** = referencia estándar que no volvimos a abrir hoy.

### 2.1 El valor de $\delta_c$ y el espectro del Yukawa

| Trabajo | Qué hace | Por qué nos importa |
|---|---|---|
| Rogers, Graboske y Harwood, *Phys. Rev. A* **1**, 1577 (1970) [V] | Espectro numérico del Coulomb apantallado estático y apantallamientos críticos | Es la referencia clásica de $\delta_c$ para muchos estados |
| Lam y Varshni, *Phys. Rev. A* **4**, 1875 (1971) [ya citada] | Energías y críticos, también del ECSC | Referencia del perfil "coseno" |
| Luo, Li y Kröger, *Sci. China G* **49**, 60 (2006), arXiv:hep-ph/0407258 [V, en nuestra Fase 1] | Monte Carlo hamiltoniano; ajuste $\delta_c(\ell)$ | Ya hay Monte Carlo del umbral, pero sin prueba de caja |
| Napsuciale y Rodríguez, *Phys. Lett. B* (2021), DOI 10.1016/j.physletb.2021.136218, arXiv:2012.12969 [V-arXiv] | Solución "analítica" con supersimetría y expansión de superpotenciales; $\delta_c$ con muchas cifras | Cierra la carrera por cifras de $\delta_c$ |
| Napsuciale y Rodríguez, arXiv:2102.07160 [V-arXiv] | Serie en $\delta$ + Padé para todos los estados; cruces de niveles para $n\ge4$; motivación de materia oscura | Muestra que la radial cambia sobre todo cerca del crítico |
| Edwards, Gerber, Schubert, Trejo y Weber, *PTEP* **2017**, 083A01, arXiv:1706.09979 [V] | Perturbación de 5.º orden, variacional y un método nuevo para $\delta_c$ con 10 cifras | Ya citada; el propio grupo luego usa Monte Carlo de línea de mundo |
| A. K. Roy, arXiv:1904.11166 [V-arXiv] | Críticos de Hulthén, Yukawa y ECSC para $n\le10$, y H confinado en una esfera con ECSC | Tabla de referencia para el perfil ECSC (propuesta 4) |
| A. K. Roy, arXiv:1802.04373 [V-arXiv] | H y Hulthén dentro de una esfera impenetrable: radio crítico de caja donde $E=0$ | Lo más cercano a nuestra "prueba de caja", pero mira el caso opuesto (caja pequeña que *desliga*), no el umbral por apantallamiento |

### 2.2 Matemática del umbral

| Trabajo | Resultado |
|---|---|
| Klaus y Simon, *Ann. Phys.* **130**, 251 (1980), DOI 10.1016/0003-4916(80)90338-3 [V] | Cerca de la constante crítica, $e(\lambda)\sim c(\lambda-\lambda_0)^\alpha$. En 3D: $\alpha=2$ para $\ell=0$ (no analítico, el estado se pierde en el continuo) y $\alpha=1$ para $\ell\ge1$ (en el umbral hay un autovalor genuino, normalizable). "Los resultados dependen mucho de la dimensión." |
| Bargmann, *PNAS* **38**, 961 (1952) [ya citada] | Cota que usamos en la Fase 1 |

Esto ya explica nuestro $\kappa\propto(\delta_c-\delta)$. Lo que **no** está hecho para el Yukawa es convertir la diferencia entre $\ell=0$ y $\ell\ge1$ en una prueba de caja práctica (propuesta 2).

### 2.3 Escalamiento de tamaño finito en mecánica cuántica

| Trabajo | Qué hace |
|---|---|
| Serra, Neirotti y Kais, *Phys. Rev. A* **57**, R1481 (1998) [V] | Aplican escalamiento de tamaño finito al Yukawa, pero el "tamaño" es **el número de funciones de base $N$**, no una caja. Obtienen $\lambda_c=1/\delta_c=0.8399039$ y los exponentes $\alpha=2$ (para $\ell=0$) y $\alpha=1$ (para $\ell=1$) |
| Kais y Serra, revisiones del grupo de Purdue (2000, 2003) [V, enlaces en la búsqueda] | Extienden el método a átomos y moléculas, con bases gaussianas y elementos finitos |
| dos Santos y Sneddon, *Phys. Rev. B* **23**, 3541 (1981) [V] | Transformaciones de reescalamiento de tamaño finito (renormalización fenomenológica): las curvas de dos tamaños se cruzan en el punto crítico |

**Hueco:** el escalamiento se hizo en el tamaño de la base, que no es un observable físico. Con **el radio de la caja como tamaño**, el punto fijo es un número exacto y físico ($2R^2E/\pi^2=1/4$), y el cruce responde directamente a la pregunta de la guía. No encontramos este uso para el Yukawa.

### 2.4 Volumen finito y estados ligados débiles

| Trabajo | Qué hace |
|---|---|
| König, Lee y Hammer, *Phys. Rev. Lett.* **107**, 112001 (2011), arXiv:1103.4468 [V] | Corrimiento de la energía de un ligado en una caja **periódica**: en onda $s$ el ligado se refuerza; en onda $p$, se debilita; para $\ell\ge2$ depende de la representación cúbica |
| Riisager, *Phys. Scr.* T152, 014001 (2013), arXiv:1208.6415 [V-arXiv] | Halos de dos cuerpos: $\langle r^2\rangle$ diverge al ligar a cero para $\ell=0$ y $\ell=1$, y queda finito para $\ell\ge2$ |
| Jensen, Riisager, Fedorov y Garrido, *Rev. Mod. Phys.* **76**, 215 (2004) [V, DOI] | Revisión de halos cuánticos: universalidad de la extensión cerca del umbral |

**Hueco:** las fórmulas de volumen finito son para cajas periódicas cúbicas (redes de QCD). Nuestra caja es una esfera con pared dura, donde el análogo es más sencillo y cerrado (sección 3). Además, nadie lo usa como "detector de artefactos" en el Yukawa.

### 2.5 Integrales de camino y Monte Carlo para Yukawa y Coulomb

| Trabajo | Qué hace |
|---|---|
| Pollock y Ceperley, *Phys. Rev. B* **30**, 2555 (1984) [V]; Ceperley, *Rev. Mod. Phys.* **67**, 279 (1995) [conocida] | Acción de pares para Coulomb, la base de nuestra Fase 2 |
| Edwards, Gerber, Schubert, Trejo, Tsiftsi y Weber, arXiv:1903.00536 [V-arXiv] | Monte Carlo de línea de mundo (caminos brownianos) para Coulomb y **Yukawa**. Reportan dos dificultades: la singularidad obliga a "suavizar" y, a tiempos largos, los caminos se escapan y dejan de muestrear el potencial ("undersampling") |
| Ahumada et al., arXiv:2512.24942 [V-arXiv] | Línea de mundo para varias partículas; cita el Yukawa como problema cuyo $\delta_c$ y estado no tienen forma cerrada |
| Kole y De Raedt; Myrheim [ya citadas] | Suavizado del Coulomb en integrales de camino |

**Hueco:** los Monte Carlo de línea de mundo tienen problemas justo cerca del umbral, porque el tiempo de proyección necesario crece como $1/|E_0|\sim10^7$. Una formulación a **energía cero** (sin tiempo de proyección) evitaría eso. No encontramos que se haya hecho para el Yukawa.

### 2.6 Representación probabilística (Feynman–Kac)

| Trabajo | Qué hace |
|---|---|
| Chung y Zhao, *From Brownian Motion to Schrödinger's Equation*, Springer, Grundlehren **312** (1995) [V]; reseña de Cranston, *Bull. AMS* **39**, 109 (2002) [V] | Teorema de la *gauge*: $g(x)=E_x\big[\exp\int_0^\tau q(B_s)\,ds\big]$ es acotada o idénticamente infinita, y si es finita resuelve $(\tfrac12\Delta+q)u=0$ |
| K. L. Chung, *Sém. Probab.* **19**, 496 (1985) [V] | Teorema de la gauge y de la gauge condicional |
| Kac y Luttinger, *Ann. Inst. Fourier* **25**, 317 (1975) [V] | Fórmula de la longitud de dispersión como integral de Wiener y su relación con la capacidad electrostática |
| P. He, *Proc. AMS* **139**, 1871 (2011) [V] | Prueba de la fórmula de Kac para la longitud de dispersión en procesos de Markov |

**Hueco:** esta maquinaria está en la literatura de probabilidad, casi siempre para potenciales **repulsivos** o acotados. Para un potencial **atractivo** cerca de su umbral, la gauge diverge justo en $\delta_c$, y eso da un criterio de umbral sin caja. No encontramos que se use como método numérico para el Yukawa ni que se discuta su varianza (propuesta 3).

### 2.7 Dónde aparece el umbral en la física (para la introducción del artículo)

| Contexto | Fuente | Qué aporta |
|---|---|---|
| Plasmas (Debye–Hückel) | Rogers et al. 1970 [V] | Ionización por apantallamiento: no hay 1s si la longitud de Debye es menor que $a_0/1.1906\approx0.840\,a_0$ |
| Materia oscura con mediador ligero | Petraki, Postma y de Vries, *JHEP* **04** (2017) 077, arXiv:1611.01394 [V]; Napsuciale y Rodríguez 2021 | Con masa reducida $m_\chi/2$: hay ligado si $\alpha m_\chi/m_\phi>1.680$ (nota *) |
| Deuterón y masa del pion | Epelbaum, Meißner y Glöckle, *Nucl. Phys. A* (2002), arXiv:nucl-th/0207089 [V-arXiv]; Beane y Savage, *Nucl. Phys. A* (2002), arXiv:nucl-th/0208021 [V-arXiv]; NPLQCD, *Phys. Rev. D* **87**, 034506 (2013), arXiv:1206.5219 [V] | ¿Sigue ligado el deuterón si cambia la masa del pion? En el límite quiral EMG lo encuentran ligado; NPLQCD lo encuentra ligado con $m_\pi\approx806$ MeV |

(*) Cuenta: con masa reducida $m_\chi/2$ y $g=\alpha$, $\delta=2m_\phi/(\alpha m_\chi)$. Hay ligado si $\delta<\delta_c$, es decir, si $\alpha m_\chi/m_\phi>2/\delta_c=1.680$. No comprobamos que esa cifra aparezca tal cual en Petraki et al.; es nuestra cuenta. Es una buena forma de mostrar que nuestro número adimensional tiene sentido físico sin reclamarlo como "cifra universal".

---

## 3. Resultado preliminar que respalda la propuesta principal

Para comprobar que la idea 1 funciona, la probamos con un disparo de alta precisión (`prototipos/cruce_de_cajas_yukawa.py`, menos de 10 minutos en un núcleo). No usa el código de las fases anteriores. En el artículo se rehace con el radial y la integral de camino del grupo.

**Por qué funciona.** Fuera del alcance del potencial, la solución de energía casi cero es $u\propto\sin(kr+\eta)$, con $k\cot\eta\approx-1/a$. La pared dura pide $kR+\eta=\pi$. En el umbral $a\to\pm\infty$, así que $\eta=\pi/2$, y queda $kR=\pi/2$:
$$\frac{2R^2E_0(R)}{\pi^2}\;\xrightarrow{\;\delta=\delta_c\;}\;\frac14\quad\text{para todo }R\text{ grande}.$$

- Con un ligado verdadero, $2R^2E_0/\pi^2\to-\infty$ (como $-\kappa^2R^2/\pi^2$).
- Si no hay ligado, tiende a $1$ (el modo libre).

Las curvas de dos cajas se cruzan, entonces, cerca de $\delta_c$. **Un artefacto de caja no puede fabricar el cruce**, porque el cruce exige que la energía escale exactamente como $R^{-2}$ con coeficiente $\pi^2/8$.

**Tabla A.** $2R^2E_0/\pi^2$ (Yukawa, $\ell=0$):

| $\delta$ | $R=50$ | 100 | 200 | 400 | 800 |
|---|---|---|---|---|---|
| 1.18 | 0.171 | 0.065 | −0.195 | −0.997 | −4.019 |
| 1.19 | 0.254 | 0.245 | 0.233 | 0.213 | 0.171 |
| 1.1906 | 0.259 | 0.254 | 0.252 | 0.250 | 0.249 |
| 1.20 | 0.326 | 0.379 | 0.470 | 0.598 | 0.735 |

**Tabla B.** Cruces de curvas consecutivas:

| Par de cajas | $\delta^\ast$ | valor en el cruce |
|---|---|---|
| 50 / 100 | 1.1912375 | 0.2639 |
| 100 / 200 | 1.1907646 | 0.2568 |
| 200 / 400 | 1.1906500 | 0.2534 |
| 400 / 800 | 1.1906217 | 0.2517 |

Las diferencias bajan un factor ≈4 en cada duplicación (corrección $\propto R^{-2}$). Richardson con los dos últimos pares da $\delta_c\approx1.1906123$, frente a la referencia $1.1906124$. El valor del cruce tiende a $1/4$.

Hay tres comprobaciones más, en `prototipos/cruce_extension_y_ecsc.py`:

- **La extensión también cruza.** En el umbral, $u=\cos(\pi r/2R)$ fuera del potencial, así que $\langle r\rangle/R\to\tfrac12-\tfrac{2}{\pi^2}=0.2974$. Medido en $\delta_c$: 0.3005, 0.2989 y 0.2981 en $R=200$, 400 y 800. Es una **segunda observable de localización con punto fijo exacto**, como pide la guía ("comparar varias cajas y una observable de localización").
- **No es exclusivo del Yukawa.** Para el ECSC, $V=-e^{-\delta r}\cos(\delta r)/r$, los cruces dan 0.7205140, 0.7205215 y 0.7205234, frente a $\delta_c=0.7205241$ por energía cero. El valor del cruce se acerca a $1/4$ **desde abajo**, mientras que en el Yukawa lo hace desde arriba. El signo de la corrección lo fija el rango efectivo, otra cosa que se puede medir.
- **Umbrales de referencia por energía cero** (`prototipos/umbrales_energia_cero.py`): Yukawa 1s 1.19061242, 2s 0.31020928, 2p 0.22021681 ($1/\delta=4.5410$, igual que Serra et al.), 3d 0.09134512; ECSC 1s 0.72052409; Hulthén 1s 2.00000000 (exacto).

---

## 4. Propuestas

Ordenadas de la más recomendada a la más arriesgada. Para cada una: qué es, por qué es original, qué cuesta y qué figura deja.

### Propuesta 1 (recomendada para la Fase 4): criterio de cruce de cajas

- **Qué es:** sustituir "¿el autovalor es negativo?" por "¿dónde se cruzan $2R^2E_0(R)/\pi^2$ y $\langle r\rangle/R$ para pares de cajas?", y extrapolar los cruces en $1/R^2$.
- **Por qué es original:** el escalamiento de tamaño finito para el Yukawa se hizo con el tamaño de base [Serra, Neirotti y Kais 1998]. Las fórmulas de volumen finito son para cajas periódicas [König, Lee y Hammer 2011]. El punto fijo exacto $1/4$ de la caja esférica dura, su par $\tfrac12-\tfrac2{\pi^2}$ para la extensión y su uso para separar estado débil de artefacto no aparecieron en nuestra búsqueda.
- **Qué responde de la guía:** es literalmente "la prueba de caja que separa un estado débil de un artefacto" de la segunda presentación. Además mejora la cota del umbral **solo con cajas** y con $R\le800$, en vez de $R=12800$.
- **Con nuestros dos métodos:** las energías de caja ya salen de la integral de camino (transferencia) y del radial. Basta con añadir pares de $R$ más finos en $\delta\in[1.185,1.195]$. El cruce en la integral de camino es la prueba fuerte, porque usa solo tiempo imaginario.
- **Costo:** bajo (días). Lo más caro es repetir la transferencia en $R=400$–800 para unos 10 valores de $\delta$.
- **Riesgos:** el error de Trotter y de malla se suma al de caja. Hay que propagarlos al cruce (dos derivadas de $R^2E$). Preparar la objeción "¿el cruce no es otra forma del signo?": la respuesta es que no, porque en $\delta=1.19$ el signo cambia recién en $R\approx2200$, mientras que el cruce ya ubica $\delta_c$ con $R=200$.
- **Figura central de la segunda presentación:** las curvas $2R^2E_0/\pi^2$ contra $\delta$ para 5 cajas, cruzándose en 1/4; recuadro con los $\delta^\ast$ contra $1/R^2$.

### Propuesta 2 (recomendada para la extensión espacial): cómo crece el estado según $\ell$

- **Qué es:** repetir la Fase 3 para los umbrales 2p ($\delta_c=0.22022$) y 3d ($0.09135$) y comparar con 1s.
- **Predicción** (se deriva del comportamiento $u\sim r^{-\ell}e^{-\kappa r}$ en el umbral; Klaus y Simon 1980; Riisager 2013):

| | $E_0$ cerca del umbral | $\langle r\rangle$ | $\langle r^2\rangle$ | ¿Qué ve la caja? |
|---|---|---|---|---|
| $\ell=0$ | $\propto-(\delta_c-\delta)^2$ | $\propto1/\kappa$ | $\propto1/\kappa^2$ | El estado se va a la pared; cruce en 1/4 |
| $\ell=1$ | $\propto-(\delta_c-\delta)$ | $\propto\ln(1/\kappa)$ | $\propto1/\kappa$ | Casi localizado; el signo de $E$ en caja es fiable mucho antes |
| $\ell=2$ | $\propto-(\delta_c-\delta)$ | finito | finito | El estado sigue siendo $L^2$ en el umbral |

- **Por qué es original:** la tabla se conoce por pedazos (matemática del umbral, halos nucleares), pero no la hemos visto **medida** para el Yukawa con una prueba de caja. El crecimiento logarítmico de $\langle r\rangle$ en onda $p$ es una predicción fina, fácil de equivocar y comprobable.
- **Qué responde:** "examinar cómo crece la extensión espacial", con algo más que $\langle r\rangle\kappa\to1/2$.
- **Costo:** bajo en el radial (añadir $\ell(\ell+1)/2r^2$). En la integral de camino es medio: hace falta la acción de pares en la onda parcial $\ell$, o un nodo fijo exacto ($z=0$ para el estado $p$), que es exacto por simetría. Buen tema de discusión: el peso con nodo fijo sigue siendo positivo.
- **Bonus:** en onda $p$, el punto fijo de la caja no es 1/4, porque el estado no se va a la pared. Esa diferencia es otra prueba de que el cruce detecta física y no la caja.

### Propuesta 3 (ambiciosa, para la fase final): umbral sin caja con caminos brownianos

- **Qué es:** para $\delta>\delta_c$, la solución de energía cero normalizada a 1 en el infinito es (Feynman–Kac, con $\hbar=m=1$)
$$\varphi(\mathbf x)=E_{\mathbf x}\Big[\exp\Big(-\!\int_0^\infty V(\mathbf B_t)\,dt\Big)\Big],\qquad \varphi(r)\to1-\frac{a}{r},\qquad a=2\!\int_0^\infty r^2V(r)\varphi(r)\,dr .$$
Los caminos brownianos en 3D son transitorios y escapan al infinito, así que **no hay caja ni tiempo de proyección**. Cuando $\delta\to\delta_c^+$, $a\to-\infty$ y la gauge diverge: es el umbral. Esto es el teorema de la gauge [Chung y Zhao 1995] y la fórmula de Kac–Luttinger para la longitud de dispersión, aplicados a un potencial atractivo. **Hay que verificar el enunciado exacto en el libro antes de usarlo en el artículo.**
- **La obstrucción que encontramos:** el segundo momento del estimador es la gauge del potencial $2V$, es decir, de un Yukawa con acoplamiento $2g$, o sea con $\delta/2$. Es finito solo si $\delta/2>\delta_c$. **La varianza es infinita para $\delta_c<\delta<2\delta_c\approx2.381$**, justo donde se necesita. Es la versión, en este método, de la exigencia de la guía de decir si "el peso que se muestrea es real, positivo y normalizable": aquí es real y positivo, pero de varianza no normalizable.
- **Plan:**
  1. Comprobar el método en $\delta=3$ (varianza finita) contra el $a_s$ del disparo.
  2. Mostrar en $\delta=1.5$ las colas pesadas (histograma de pesos y media que no se estabiliza).
  3. Arreglarlo con muestreo por importancia (transformada $h$ de Doob con una función de prueba $\varphi_T$, por ejemplo la variacional de la Fase 1). Es la "difusión guiada a energía cero".
- **Por qué es original:** los Monte Carlo de línea de mundo del Yukawa [Edwards et al. 2019] trabajan a tiempo finito y sufren "undersampling" a tiempos largos. A energía cero ese problema desaparece y aparece otro, la varianza infinita, que no encontramos discutido.
- **Costo:** medio-alto (2–3 semanas). Riesgo moderado: si el muestreo por importancia no alcanza, el resultado negativo (ventana de varianza infinita, demostrada y medida) ya es defendible.
- **Conexión con lo que tenemos:** el $a_s$ que ya calculamos (+2204 en 1.19, −142.9 en 1.20) es el número a reproducir.

### Propuesta 4 (la ampliación que sugiere la guía): otro perfil de apantallamiento

- **Qué es:** el mismo análisis con el ECSC ($\delta_c=0.72052$, cruce ya comprobado) y con Hulthén (exacto, $\delta_c=2$). Ver qué es universal y qué no:
  - es universal el punto fijo 1/4, $\kappa a\to1$ y $\langle r\rangle\kappa\to1/2$;
  - no lo son la pendiente $c$ en $\kappa\simeq c(\delta_c-\delta)$ ni el signo de la corrección del cruce, que dependen del rango efectivo.
- **Extra barato:** $c=-d(1/a)/d\delta$ en $\delta_c$, y se calcula con la solución de energía cero. Así se predice el $0.741$ de la Fase 3 sin ajustar. Con el rango efectivo $r_e$ [Bethe, *Phys. Rev.* **76**, 38 (1949), conocida], $\kappa=(1-\sqrt{1-2r_e/a})/r_e$ sigue el polo **al otro lado** del umbral, donde se vuelve estado virtual. Lo puede ver la caja y no la integral de camino.
- **Por qué cuenta:** es la ampliación que ofrece la guía, y Hulthén es un control con solución exacta que ya tenemos implementado.
- **Costo:** bajo.

### Propuesta 5 (para la introducción y la discusión): qué significa físicamente $\delta_c$

- **Deuterón de juguete** (`prototipos/deuteron_juguete.py`): con masa reducida $m_N/2$, rango $1/m_\pi$ y $g$ ajustado para que la energía de enlace sea 2.2246 MeV, sale $\delta_d=0.830$ (70 % de $\delta_c$) y $g/\hbar c=0.354$. Con $g$ fijo, el deuterón se desligaría con $m_\pi\approx198$ MeV. Pero la red (NPLQCD) lo encuentra ligado con $m_\pi\approx806$ MeV. **Eso muestra justo lo que la guía pide no hacer:** una cifra adimensional no se traslada sin decir qué parámetro se mantiene fijo, porque $g$ también depende de $m_\pi$ (Epelbaum et al.; Beane y Savage).
- **Materia oscura y plasmas:** $\alpha m_\chi/m_\phi>1.680$ y $\lambda_D>0.840\,a_0$, como ejemplos de la misma condición en unidades distintas.
- **Costo:** muy bajo. Sirve para la introducción y para la defensa individual.

### Ideas que miramos y no recomendamos

- **Otra cifra de $\delta_c$ con más dígitos:** ya hay 10 o más (Edwards et al. 2017; Napsuciale y Rodríguez 2021).
- **Transformación de Kustaanheimo–Stiefel o Duru–Kleinert** para quitar la singularidad: es elegante (y la guía la sugiere en el proyecto 04), pero ya resolvimos la singularidad con la acción de pares y el Yukawa no se vuelve exactamente soluble.
- **Dimensión $d=2$**, donde todo pozo liga y $E\sim e^{-1/\text{algo}}$: muy buena para mostrar una caja que miente, pero cambia el problema del proyecto.

---

## 5. Recomendación y plan

**Fase 4: propuestas 1 + 2 (y la 5 en el texto).** Así se cumple todo lo que pide la guía (intervalo defendible, curvas de energía y extensión, varias cajas, prueba de caja para la presentación) y se le da al profesor algo original, concreto y ya probado.

**Fase final: añadir la 4 (la ampliación oficial) y, si queda tiempo, la 3.** La 3 es la apuesta: tiene un resultado negativo seguro (la varianza infinita), que ya es original, y un resultado positivo posible (el muestreo por importancia).

Plan sugerido (para ajustar entre los dos):

| Semana | Tarea | Entregable |
|---|---|---|
| 1 | Cruce de cajas con radial y transferencia, $R=50$–800, $\delta\in[1.185,1.195]$; propagación de errores | Figura de cruces, tabla de $\delta^\ast(R)$ |
| 1 | Extensión: cruce de $\langle r\rangle/R$; $\langle r\rangle$ y $\langle r^2\rangle$ frente a $\kappa$ | Figura de extensión |
| 2 | $\ell=1,2$ en el radial; nodo fijo o acción de onda parcial en la integral de camino | Tabla de la propuesta 2, medida |
| 2 | Artículo de 10 a 12 páginas: insertar las secciones nuevas en el borrador de la Fase 3 | Artículo |
| 3 | ECSC/Hulthén y $c=-d(1/a)/d\delta$ | Figura de universalidad |
| 3–4 | (Opcional) gauge de Feynman–Kac: $\delta=3$, $\delta=1.5$ y muestreo por importancia | Sección o apéndice |
| — | Bitácora de IA: registrar esta búsqueda como F4-01 (fecha, consulta, respuesta, decisión, comprobación) | Bitácora |

**Para la bitácora (formato del curso):** *F4-01 · 15-11-2026 · Consulta: "búsqueda extensa de qué se ha hecho para proponer algo original en la Fase 4 y final" · Respuesta: este documento y 4 prototipos · Decisión humana: pendiente · Comprobación: cruces y umbrales recalculados (tablas A y B, sección 3); referencias abiertas en editor o arXiv (marcas [V]) · Corrección posterior: —.*

**Dos cosas que deben comprobar ustedes antes de usarlas en el artículo:**

1. el enunciado exacto del teorema de la gauge en $\mathbb R^3$, en Chung y Zhao 1995;
2. el volumen y la página de las referencias marcadas [V-arXiv].

---

## 6. Bibliografía (con estado de verificación)

- V. Bargmann, *Proc. Natl. Acad. Sci. USA* **38**, 961 (1952). [ya en el borrador]
- H. A. Bethe, *Phys. Rev.* **76**, 38 (1949). [conocida]
- S. R. Beane y M. J. Savage, "The quark-mass dependence of two-nucleon systems", *Nucl. Phys. A*, DOI 10.1016/S0375-9474(02)01586-5, arXiv:nucl-th/0208021. [V-arXiv]
- S. R. Beane et al. (NPLQCD), "Light nuclei and hypernuclei from QCD in the limit of SU(3) flavor symmetry", *Phys. Rev. D* **87**, 034506 (2013), arXiv:1206.5219. [V]
- D. M. Ceperley, *Rev. Mod. Phys.* **67**, 279 (1995). [conocida]
- K. L. Chung, "The gauge and conditional gauge theorem", *Séminaire de Probabilités* XIX, LNM 1123, 496–503 (1985). [V]
- K. L. Chung y Z. Zhao, *From Brownian Motion to Schrödinger's Equation*, Grundlehren **312**, Springer (1995), DOI 10.1007/978-3-642-57856-4. [V]; reseña: M. Cranston, *Bull. AMS* **39**, 109 (2002). [V]
- R. R. dos Santos y L. Sneddon, "Finite-size rescaling transformations", *Phys. Rev. B* **23**, 3541 (1981). [V]
- J. P. Edwards, U. Gerber, C. Schubert, M. A. Trejo y A. Weber, "The Yukawa potential: ground state energy and critical screening", *PTEP* **2017**, 083A01, arXiv:1706.09979. [V]
- J. P. Edwards, U. Gerber, C. Schubert, M. A. Trejo, T. Tsiftsi y A. Weber, "Applications of the worldline Monte Carlo formalism in quantum mechanics", arXiv:1903.00536. [V-arXiv]
- I. Ahumada et al., "Multi-particle quantum systems within the Worldline Monte Carlo formalism", arXiv:2512.24942. [V-arXiv]
- E. Epelbaum, U.-G. Meißner y W. Glöckle, "Nuclear forces in the chiral limit", *Nucl. Phys. A*, DOI 10.1016/S0375-9474(02)01393-3, arXiv:nucl-th/0207089. [V-arXiv]
- P. He, "A formula on scattering length of dual Markov processes", *Proc. AMS* **139**, 1871 (2011). [V]
- A. S. Jensen, K. Riisager, D. V. Fedorov y E. Garrido, "Structure and reactions of quantum halos", *Rev. Mod. Phys.* **76**, 215 (2004). [V, DOI]
- M. Kac y J. M. Luttinger, "Scattering length and capacity", *Ann. Inst. Fourier* **25**, 317 (1975). [V]
- M. Klaus y B. Simon, "Coupling constant thresholds in nonrelativistic quantum mechanics. I. Short-range two-body case", *Ann. Phys.* **130**, 251 (1980). [V]
- S. König, D. Lee y H.-W. Hammer, "Volume dependence of bound states with angular momentum", *Phys. Rev. Lett.* **107**, 112001 (2011), arXiv:1103.4468. [V]
- C. S. Lam y Y. P. Varshni, *Phys. Rev. A* **4**, 1875 (1971). [ya en el borrador]
- X.-Q. Luo, Y.-Y. Li y H. Kröger, *Sci. China G* **49**, 60 (2006), arXiv:hep-ph/0407258. [ya en la Fase 1]
- M. Napsuciale y S. Rodríguez, "Complete analytical solution to the quantum Yukawa potential", *Phys. Lett. B* (2021), DOI 10.1016/j.physletb.2021.136218, arXiv:2012.12969. [V-arXiv]
- M. Napsuciale y S. Rodríguez, "Bound states of the Yukawa potential from hidden supersymmetry", arXiv:2102.07160. [V-arXiv]
- K. Petraki, M. Postma y J. de Vries, *JHEP* **04** (2017) 077, arXiv:1611.01394. [V]
- E. L. Pollock y D. M. Ceperley, *Phys. Rev. B* **30**, 2555 (1984). [V]
- K. Riisager, "Halos and related structures", *Phys. Scr.* T152, 014001 (2013), arXiv:1208.6415. [V-arXiv]
- F. J. Rogers, H. C. Graboske y D. J. Harwood, "Bound eigenstates of the static screened Coulomb potential", *Phys. Rev. A* **1**, 1577 (1970). [V]
- A. K. Roy, "Critical parameters and spherical confinement of H atom in screened Coulomb potential", arXiv:1904.11166. [V-arXiv]
- A. K. Roy, "Spherical confinement of Coulombic systems inside an impenetrable box: H atom and the Hulthén potential", arXiv:1802.04373. [V-arXiv]
- P. Serra, J. P. Neirotti y S. Kais, "Finite-size scaling approach for the Schrödinger equation", *Phys. Rev. A* **57**, R1481 (1998). [V]

**Prototipos** (carpeta `prototipos/`, Python con numpy y scipy, deterministas):

- `cruce_de_cajas_yukawa.py`: tablas A y B;
- `cruce_extension_y_ecsc.py`: $\langle r\rangle/R$ en el umbral y cruces del ECSC;
- `umbrales_energia_cero.py`: $\delta_c$ de 1s, 2s, 2p, 3d, ECSC y Hulthén;
- `deuteron_juguete.py`: propuesta 5.
