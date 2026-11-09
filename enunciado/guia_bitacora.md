

# Guía para la bitácora

Criterios que pidió el profesor para las bitácoras, traducidos a qué debe aparecer en el documento y cómo se ve en la práctica. Los ejemplos salen de la Bitácora 1 (longitud máxima de la trayectoria de un proyectil).

**Instrucción de uso:** al redactar cualquier bitácora de este proyecto, seguir esta guía. Cada criterio debe dejar huella visible en el documento, no solo aplicarse mentalmente.

---

## Notas originales del profesor

- **Estrategias:** examinar límites; inconsistencias formales; formalismo.

- **Consejos:** toy models; recalcular; definir bien el punto de salida.

- **Pensamiento:** crítico, investigativo, creativo.

- **Además:** definir objetivo claro; régimen de validez; definir el criterio de cierre.

---

## 1. Antes de escribir nada

Estas tres cosas deben quedar fijadas al principio de la bitácora. Si alguna falta, el resto del trabajo no tiene contra qué medirse.

| Criterio | Pregunta que debe responder | Ejemplo (Bitácora 1) |

|---|---|---|

| **Objetivo claro** | ¿Qué pregunta exacta se responde y qué magnitud se calcula? | Hallar el ángulo θ que maximiza la longitud de la trayectoria, no el alcance. |

| **Régimen de validez** | ¿Bajo qué hipótesis vale el resultado y dónde deja de valer? | Sin aire, g uniforme, alcances mucho menores que el radio terrestre. |

| **Criterio de cierre** | ¿Qué tiene que cumplirse para dar el problema por terminado? | θ* con cuatro decimales, confirmado por dos métodos independientes y demostrado como máximo global. |

---

## 2. Tres modos de pensamiento

### Crítico

- **Verificar y cuestionar supuestos implícitos.** Listar lo que la solución da por hecho sin decirlo.

 *Ejemplo:* la solución oficial suponía un máximo único sin demostrarlo.

- **Consistencia.** Dimensiones, signos, casos particulares y coherencia entre pasos.

 *Ejemplo:* L tiene unidades de v²/g; L(0) = 0, como debe ser.

- **Desconfiar de cancelaciones milagrosas.** Cuando algo se simplifica demasiado bien, revisar por qué.

 *Ejemplo:* sustituir θ = π/2 en la fórmula cerrada da 0·∞; hay que volver a la integral original.

### Investigativo

- **Genealogía de las ideas.** De dónde viene el problema, quién lo resolvió antes y qué se sabe ya.

 *Ejemplo:* búsqueda de anterioridad (Sarafian 1999, Cooper y Swifton, Chudinov).

- **Pensar modelos y experimentos mentales.** Preguntar qué pasaría si se cambia una condición, antes de calcular.

 *Ejemplo:* ¿qué ocurre si se quita la atmósfera o se aplana el planeta?

- **Identificar anomalías y discrepancias.** Registrar todo lo que no cuadra, aunque parezca menor.

 *Ejemplo:* θ* no depende de ningún parámetro, lo que revela un modelo degenerado.

### Creativo

- **Traslapar campos.** Conectar el problema con áreas que en principio no están relacionadas.

 *Ejemplo:* del tiro parabólico a la entrada atmosférica y la aerocaptura.

- **Variar o usar restricciones y modelos simples.** Quitar o añadir una hipótesis a la vez y ver qué cambia.

 *Ejemplo:* atmósfera homogénea y plana como paso intermedio.

- **Visualizar el espacio de parámetros.** Graficar cómo cambia el resultado al mover los parámetros, no solo un caso.

 *Ejemplo:* mapa de S según el ángulo de entrada y la disipación.

---

## 3. Estrategias y consejos

### Estrategias

- **Examinar límites.** Llevar cada parámetro a 0 o ∞ y comprobar que se recupera algo conocido.

- **Inconsistencias formales.** Buscar errores de notación, pasos que no se siguen y errores tipográficos en las fuentes.

- **Formalismo.** Hipótesis numeradas, notación fija y derivaciones paso a paso, sin saltos.

### Consejos

- **Toy models.** Resolver primero la versión más simple posible del problema.

- **Recalcular.** Cada resultado importante, por un segundo camino independiente.

- **Definir bien el punto de salida.** Dejar explícito qué se da por conocido y desde dónde arranca el cálculo.

---

## 4. Estructura sugerida de la bitácora

Entre corchetes, el criterio que cubre cada sección.

1\. **Objetivo, régimen de validez y criterio de cierre.** Fijados antes de cualquier cálculo. [marco]

2\. **Punto de salida e hipótesis numeradas.** Qué se da por conocido y en qué formalismo se trabaja. [consejo, formalismo]

3\. **Genealogía del tema.** Origen del problema y lo que ya está publicado. [investigativo]

4\. **Toy model.** La versión más simple, resuelta completa. [consejo, creativo]

5\. **Desarrollo principal.** Derivación paso a paso con el formalismo elegido. [formalismo]

6\. **Límites y consistencia.** Límites, dimensiones, casos particulares. [crítico, estrategia]

7\. **Recálculo independiente.** Segundo método, numérico o analítico. [consejo, crítico]

8\. **Auditoría de la IA y de las fuentes.** Supuestos implícitos, cancelaciones sospechosas, anomalías y errores encontrados. [crítico, investigativo]

9\. **Extensión o conexión con otro campo.** Qué hipótesis se relaja y qué parámetro aparece. [creativo]

10\. **Cierre.** Verificar contra el criterio de cierre definido al inicio. [marco]

---

## 5. Revisión final antes de entregar

- [ ] El objetivo está escrito como una pregunta concreta.

- [ ] El régimen de validez está explícito, con sus límites.

- [ ] El criterio de cierre está definido y se comprueba al final.

- [ ] El punto de salida y las hipótesis están numerados.

- [ ] Hay al menos un toy model resuelto.

- [ ] Se examinaron los límites de cada parámetro.

- [ ] Se hizo análisis dimensional.

- [ ] El resultado principal se recalculó por un camino independiente.

- [ ] Se listaron los supuestos implícitos de la IA y de las fuentes.

- [ ] Se revisó cualquier simplificación sospechosa.

- [ ] Se registraron las anomalías y discrepancias encontradas.

- [ ] Está la genealogía del tema, con fuentes verificadas.

- [ ] Hay una conexión con otro campo o una extensión planteada.

- [ ] Hay al menos una gráfica que recorre el espacio de parámetros.

---

## Nota sobre interpretación

Dos puntos de las notas del profesor eran breves y se interpretaron así:

- **"Formalismo"**: hipótesis numeradas, notación fija y derivaciones sin saltos.

- **"Definir bien el punto de salida"**: dejar explícito qué se da por conocido y desde dónde arranca el cálculo.

Si el profesor los usó en otro sentido, ajustar estas dos entradas.

