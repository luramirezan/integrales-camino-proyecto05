# Auditoría adversarial de la Fase 3 con Gemini 3.1 Pro (app)

Lo pide la guía para el proyecto 05 en la Fase 3: *"solicitar a la IA una auditoría adversarial de autovalores cercanos a cero"*. El trabajo lo hace Claude y Gemini audita (es otro modelo, como pide el profesor).

## Cómo hacerlo (unos 20 minutos)

Este método ya funcionó en la Fase 2: material en trozos de 15 KB como máximo, Gemini responde "Recibido" a cada uno, y la auditoría se pide al final por etapas.

1. Abre un **chat nuevo** en gemini.google.com y elige **3.1 Pro** en el selector. Anota el nombre exacto del modelo.
2. Pega o adjunta, uno por mensaje y en orden, `trozos/G_parte1.md`, `trozos/G_parte2.md` y `trozos/G_parte3.md`. A los dos primeros Gemini debe responder solo "Recibido".
3. El tercer trozo termina con el encargo: Gemini devuelve una lista de 8 hallazgos como máximo, de una línea cada uno.
4. Pega la respuesta en el hilo de Claude. Claude verifica cada hallazgo (calculando) y te devuelve la respuesta para pegarla en Gemini.
5. Al final pega `trozos/G_cierre.md` para obtener la tabla de cierre.
6. Exporta o copia el chat completo a `conversaciones/G.md`, que va al registro de IA tal cual.

**Importante:** no le digas a Gemini qué resultado esperas ni que otra IA ya lo revisó. En la app no ejecuta código, así que pídele que declare qué números calculó a mano.
