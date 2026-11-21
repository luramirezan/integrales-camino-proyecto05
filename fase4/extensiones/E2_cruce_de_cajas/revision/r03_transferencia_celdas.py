"""r03_transferencia_celdas.py -- revision R2: recalcula 3 celdas crudas con comun3.resolver_tr y 1 celda completa con
comun3.celda, y las compara con los JSON de E2 (04_transferencia_R*.json). Salida: resultados/r03_transferencia_celdas.json"""
import json, os, sys, time, warnings
warnings.simplefilter("ignore")
sys.path.insert(0, "/mnt/project-files/fase3/codigo")
import comun3
out = []
casos = [(1.1906, 50, 0.04, 0.1), (1.19, 200, 0.02, 0.05), (1.1912, 400, 0.04, 0.2)]
for d, R, h, e in casos:
    J = json.load(open(f"../resultados/04_transferencia_R{R}.json"))["celdas"][f"{d:g}"]["crudo"][f"h{h:g}_eps{e:g}"]
    r = comun3.resolver_tr(d, R, h, e, J["E0"])
    fila = dict(delta=d, R=R, h=h, eps=e, E0=r["E0"], E0_json=J["E0"], dif_rel=(r["E0"] - J["E0"]) / abs(J["E0"]),
                rho=r["r_sobre_R"], rho_json=J["r_sobre_R"], perron=r["perron_min"], t=r["t"])
    out.append(fila); print(fila, flush=True)
d, R = 1.1903, 100
J = json.load(open(f"../resultados/04_transferencia_R{R}.json"))["celdas"][f"{d:g}"]
t = time.perf_counter(); C = comun3.celda(d, R, verbose=False)
comp = dict(delta=d, R=R, E_mejor=C["E_mejor"], E_mejor_json=J["E_mejor"], err=C["err"], err_json=J["err"],
            rho=C["obs"]["r_sobre_R"]["mejor"], rho_json=J["obs"]["r_sobre_R"]["mejor"], t=time.perf_counter() - t)
print(comp)
json.dump(dict(crudas=out, completa=comp), open("resultados/r03_transferencia_celdas.json", "w"), indent=1, default=float)
