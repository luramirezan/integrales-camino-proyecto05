"""13_cruce_corregido.py -- añadido tras la auditoría externa (Gemini, ronda 2, 17-11-2026; ver
fase4/extensiones/auditoria_gemini/E2/informe.md, hallazgo E2-G4).

Con r_e > 0 cada cruce delta*(R, 2R) queda POR ENCIMA de delta_c, así que el cruce crudo es una cota superior: un delta
entre delta_c y delta* también da y(R) > y(2R). La clasificación de delta = 1.19 como ligado debe usar el cruce corregido
por la ley predicha, delta* - alpha_y/R^2 - beta_y/R^3 (alpha_y, beta_y de 01_teoria.json, sin ajuste).
Este script lo calcula para los cruces del disparo, del radial y de la transferencia de 06_artefacto.json.
Salida: resultados/13_cruce_corregido.json y _salida.txt.
"""
import json, os
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R_ = os.path.join(B, "resultados")
T = json.load(open(os.path.join(R_, "01_teoria.json")))
A = json.load(open(os.path.join(R_, "06_artefacto.json")))["delta_119"]
a, b = T["constantes"]["alpha_y"], T["constantes"]["beta_y"]
Rs = [50, 100, 200, 400, 800, 1600]
out, lines = {"alpha_y": a, "beta_y": b, "delta": 1.19, "pares": {}}, []
for metodo, cr in A["cruces"].items():
    filas = []
    for R, d in zip(Rs, cr):
        corr = a / R**2 + b / R**3
        filas.append(dict(R=R, cruce=d, correccion=corr, cruce_corregido=d - corr, margen=d - corr - 1.19))
        lines.append(f"{metodo:13s} R={R:5d}  cruce={d:.9f}  correccion={corr:.3e}  corregido={d - corr:.9f}  margen sobre 1.19={d - corr - 1.19:+.3e}")
    out["pares"][metodo] = filas
out["todos_los_corregidos_mayores_que_119"] = all(f["margen"] > 0 for v in out["pares"].values() for f in v)
lines.append(f"todos los cruces corregidos > 1.19: {out['todos_los_corregidos_mayores_que_119']}")
json.dump(out, open(os.path.join(R_, "13_cruce_corregido.json"), "w"), indent=2)
open(os.path.join(R_, "13_cruce_corregido_salida.txt"), "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
