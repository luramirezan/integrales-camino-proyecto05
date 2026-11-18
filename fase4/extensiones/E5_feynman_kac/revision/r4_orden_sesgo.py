"""r4_orden_sesgo.py -- Revision: orden del sesgo del esquema de puente SIN el error de cuadratura (n_gl = 12).
Usa el simulador propio de r3 (delta = 1, muestra universal X = delta Lambda), eta = 0.8 y 0.4, N = 1e6 cada uno.
a(delta) = -(2/delta^2) mean(exp(X/delta)) para delta = 3, 4; orden 0.8/0.4 frente a la EDO de E5 (01)."""
import json, os, sys, time
import numpy as np
AQ = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQ)
from r3_caminos_lib import simula
A_EDO = {3.0: -0.3432409669, 4.0: -0.1690173658}
out = {}; t0 = time.time()
res = {}
for k, eta in enumerate([0.8, 0.4]):
    rng = np.random.default_rng(88201 + k); N = 1_000_000
    X = simula(rng.gamma(2.0, 1.0, N), 1.0, eta, 12, rng)
    res[eta] = {}
    for d in A_EDO:
        W = np.exp(X / d); a = -(2 / d**2) * W.mean(); e = 2 / d**2 * W.std(ddof=1) / np.sqrt(N)
        res[eta][d] = (a, e)
        print(f"eta={eta} n_gl=12 delta={d}: a = {a:+.6f} +- {e:.6f}; sesgo rel {(a-A_EDO[d])/abs(A_EDO[d]):+.2e}  [{time.time()-t0:.0f} s]", flush=True)
for d in A_EDO:
    s8 = res[0.8][d][0] - A_EDO[d]; s4 = res[0.4][d][0] - A_EDO[d]
    p = np.log2(abs(s8) / abs(s4)); ep = np.sqrt((res[0.8][d][1]/s8)**2 + (res[0.4][d][1]/s4)**2) / np.log(2)
    out[f"{d:g}"] = dict(a_08=res[0.8][d], a_04=res[0.4][d], orden=float(p), err_orden=float(ep))
    print(f"delta={d}: orden 0.8/0.4 con n_gl=12 = {p:.2f} +- {ep:.2f}")
json.dump(out, open(os.path.join(AQ, "r4_orden_sesgo.json"), "w"), indent=1)
