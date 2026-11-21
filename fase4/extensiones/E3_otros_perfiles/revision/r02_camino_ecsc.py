"""r02_camino_ecsc.py -- Revision R3: integral de camino del ECSC con otra pareja (h, eps).

E3 usa h in {0.02, 0.04} y eps in {0.2, 0.1, 0.05}. Aqui: h in {0.01, 0.03} (Richardson h^4, factor 81) y
eps in {0.05, 0.025} (ley eps^2), con las tablas de pares YA guardadas en fase2/resultados/tablas (solo lectura:
eps = 0.05 y 0.025 existen en la cache, asi que no se escribe nada fuera de E3). W del ECSC escrito aqui de nuevo.
Referencia: E0 de la caja por Numerov (r01_numerov.caja), independiente del disparo de E3.
Tambien comprueba W = (1 - e^{-x} cos x)/r en (0, delta] en una malla fina de x en [1e-10, 1e4].
"""
import json
import os
import sys
import time

import numpy as np
from scipy.sparse.linalg import eigsh

AQUI = os.path.dirname(os.path.abspath(__file__))
PROY = os.path.abspath(os.path.join(AQUI, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(PROY, "fase2", "codigo"))
sys.path.insert(0, AQUI)
import pares            # noqa: E402
import transferencia as tr  # noqa: E402
import r01_numerov as NV  # noqa: E402


def W_ecsc(d):
    def W(r):
        x = d * np.asarray(r, float)
        # -expm1 y cos: 1 - e^{-x} cos x = -expm1(-x) + e^{-x} (1 - cos x) = -expm1(-x) + 2 e^{-x} sin^2(x/2)
        return d * (-np.expm1(-x) + 2 * np.exp(-x) * np.sin(x / 2)**2) / x
    return W


def E_tr(d, R, h, eps, Eg):
    tab = pares.tabla_richardson(eps)
    T, r = tr.matriz_T(R, h, eps, W=W_ecsc(d), tabla=tab)
    lam, v = eigsh(T, k=1, sigma=float(np.exp(-eps * (Eg - 2e-4))), which="LM", tol=0)
    v0 = v[:, 0] * np.sign(v[:, 0].sum())
    return float(-np.log(lam[0]) / eps), float(v0.min() / np.abs(v0).max())


def main():
    out = {}
    x = np.concatenate([np.geomspace(1e-10, 1e-2, 2000), np.linspace(1e-2, 50, 2_000_001), np.geomspace(50, 1e4, 2000)])
    f = (-np.expm1(-x) + 2 * np.exp(-x) * np.sin(x / 2)**2) / x     # W/delta
    out["W_sobre_delta"] = dict(min=float(f.min()), max=float(f.max()), x_min=float(x[np.argmin(f)]))
    # g(x) = x - 1 + e^{-x} cos x >= 0 (equivale a W <= delta) en la malla
    g = x - 1 + np.exp(-x) * np.cos(x)
    out["g_min"] = float(g.min())
    print(out, flush=True)
    E3 = json.load(open(os.path.join(AQUI, "..", "resultados", "05_transferencia_ecsc.json")))["celdas"]
    cel = []
    for d, R in ((0.5, 64.0), (0.7, 522.0)):
        t0 = time.perf_counter()
        ref = [c for c in E3 if c["perfil"] == "ecsc" and abs(c["delta"] - d) < 1e-12][0]
        En, eEn = NV.caja("ecsc", d, R, ref["E_disparo"], h=0.01)
        E = {}
        per = []
        for h in (0.01, 0.03):
            for eps in (0.05, 0.025):
                E[(h, eps)], p = E_tr(d, R, h, eps, ref["E_disparo"]); per.append(p)
                print(d, R, h, eps, E[(h, eps)], flush=True)
        Eh = {eps: (81 * E[(0.01, eps)] - E[(0.03, eps)]) / 80 for eps in (0.05, 0.025)}
        Eext = Eh[0.025] + (Eh[0.025] - Eh[0.05]) / 3
        # sesgo de pared (misma receta de E3: caja en R + beta sqrt(eps), extrapolada en eps^2), con Numerov
        pw = {eps: NV.caja("ecsc", d, R + tr.BETA_PARED * np.sqrt(eps), En, h=0.01)[0] - En for eps in (0.05, 0.025)}
        pared = pw[0.025] + (pw[0.025] - pw[0.05]) / 3
        err = abs(Eh[0.025] - Eh[0.05]) / 3 + abs(E[(0.01, 0.025)] - Eh[0.025]) + abs(pared)
        c = dict(delta=d, R=R, E_tr_R3=Eext, err_R3=err, E_numerov=En, E_tr_E3=ref["E_tr"], err_E3=ref["err_tr"],
                 E_disparo_E3=ref["E_disparo"], dif_R3_numerov=Eext - En, dif_R3_E3=Eext - ref["E_tr"],
                 perron_min=min(per), crudo={f"h{h}_eps{e}": v for (h, e), v in E.items()}, t=time.perf_counter() - t0)
        print(c, flush=True)
        cel.append(c)
    out["celdas"] = cel
    json.dump(out, open(os.path.join(AQUI, "r02_camino_ecsc.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
