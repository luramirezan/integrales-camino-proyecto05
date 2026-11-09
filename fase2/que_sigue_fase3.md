# Qué sigue: Fase 3 del proyecto 05 (umbral de ligadura en el potencial de Yukawa)

Juan Sebastián Calixto y Luis Felipe Ramírez · 27 de octubre de 2026 · Propuesta escrita por la IA (Claude) al cerrar la Fase 2; **todo es propuesta, pendiente de confirmar por el equipo** (ver `decisiones_fase2.md`).

## Lo que pide el profesor (`enunciado/guia_texto.txt`)

- **Tarea del proyecto 05 en la Fase 3:** "barrer μ y tamaño de caja, estudiar convergencia temporal, y solicitar a la IA una auditoría adversarial de autovalores cercanos a cero".
- **Evidencia común de la Fase 3:** borrador del artículo, figuras con barras de error y tabla de controles. Se congelan los resultados principales de la segunda ronda (presentación de la cohorte B en la semana 14).
- **Calendario aprobado (9.11 de la Fase 1):** Fase 3, semanas 8 a 11.
- **Roles (9.12, aprobados el 21-10-2026):** en la Fase 3 se invierten: formulación física y verificación, Luis Felipe Ramírez; implementación, Juan Sebastián Calixto. Quien implementa no verifica en la misma fase.

## Lo que deja la Fase 2

- Módulos probados: `radial.py` (7/7 pruebas), `pares.py` y `transferencia.py` (7/7), `pigs.py` (14/14).
- δ = 0.2: transferencia extrapolada a 4.4×10⁻⁹ del radial; PIGS a +1.22σ (E), +0.56σ (⟨r⟩), +0.43σ (⟨r²⟩).
- Hulthén por la misma acción: energías exactas a ~10⁻⁹ hasta δ = 1.5 (3/4 del camino al umbral exacto 2).
- Criterio de cajas con la condición (c): δ = 1.15 y 1.18 ligados, δ = 1.20 no ligado, por los dos métodos: δ_c ∈ [1.18, 1.20].
- Riesgos medidos que pasan a esta fase: pared en R sin imagen (0.5826√ε), orden de la malla Nyström que no es 4 cerca del umbral, sesgo de Trotter de hasta 20 % de |E0| con ε = 0.2 sin extrapolar, τ_int del PIGS que crece con M, anomalía de τ = 5 abierta (p ≈ 1 %).

## Lista de tareas, en orden

| # | Tarea | Responsable propuesto | Entregable |
|---|---|---|---|
| 0 | Firmar `decisiones_fase2.md` (decisiones 1 a 10); decidir la imagen en R (decisión 5) **antes** de producir | los dos | hoja firmada |
| 1 | Si se aprueba: imagen en R (o R_ef = R − 0.5826√ε) en `transferencia.py`; prueba contra el radial en R = 50 y 100 (el orden de Trotter debe volver a [1.8, 2.2]) | Juan Sebastián (implementa) | módulo y prueba |
| 2 | Barrido en δ (μ a g fijo): δ ∈ {0.2, 0.5, 0.8, 1.0, 1.1, 1.15, 1.18, 1.19, 1.20, 1.25} con transferencia extrapolada en ε y h, y radial; curvas E0(δ) y ⟨r⟩(δ) con barras de error | Juan Sebastián | figura y JSON |
| 3 | Barrido de caja R ∈ {50, …, 1600} en los δ cercanos al umbral, con el criterio 9.6 completo y la condición (c); umbral de la ley de caja fijado **antes** (decisión 3) | Juan Sebastián | tabla de veredictos |
| 4 | Convergencia temporal: ε ∈ {0.2, 0.1, 0.05, 0.025} y h ∈ {0.02, 0.01}; orden de Trotter y de malla medidos en cada δ; presupuesto de errores en unidades de \|E0\| | Juan Sebastián (ejecuta), Luis Felipe (verifica) | tabla y figura |
| 5 | PIGS cerca del umbral (δ = 0.8 a 1.0): τ_int frente a M, tamaño de bloque, costo; decidir si PIGS sigue más allá de δ = 1.0 (riesgo 1 de 9.10) | Juan Sebastián | figura de autocorrelación |
| 6 | Cerrar la anomalía de τ = 5 con una corrida más larga (o dejarla abierta con su p) | Juan Sebastián | entrada en la tabla de controles |
| 7 | PIGS de Hulthén en δ = 1.0 (opcional de la Fase 2, no hecho) | Juan Sebastián | control con exacto |
| 8 | **Auditoría adversarial de autovalores cercanos a cero con otro modelo** (no Claude), siguiendo `fuentes_control/auditor_otra_ia.md`: guardar prompt y respuesta literales, verificar cada hallazgo calculando | Luis Felipe (verifica) | fichas A-01… en el registro de IA |
| 9 | Fuentes: bajar con la biblioteca H1 (Cai, Cai e Inomata 1986) y los demás de pago; confirmar revistas de H9, H10, P1, P3, PI1, PI2, Y1 (Y1: DOI 10.1063/1.5050621 visto en arXiv el 27-10-2026); leer el δ_c de Y1; buscar una fuente para la corrección 0.5826√ε (Broadie, Glasserman y Kou) y para el orden ε^{3/2} del pozo | Luis Felipe | tabla de fuentes actualizada |
| 10 | Borrador del artículo (introducción, método, controles, resultados de la Fase 3) | los dos | borrador |
| 11 | Tabla de controles de la Fase 3 y bitácora de IA (con prompts literales guardados) | Luis Felipe la consolida | tabla firmada y registro |

**Abierto, sin bloquear la Fase 3:** cotejar con los PDF Kleinert (2.376) y Saporiti (24) (supuesto S11 de la Fase 1); verificar en la fuente primaria el δ_c de Gebremedhin y Weatherford; aplicar en el texto la notación a_sc para la longitud de dispersión (decisión 2 de la Fase 1); errata de la tabla 9.6 de la Fase 1 (E0(1.18, 400) = −3.07×10⁻⁵, no −3.08×10⁻⁵).
