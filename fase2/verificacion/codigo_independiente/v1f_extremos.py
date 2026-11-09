"""V1 parte F: efecto de la aproximacion de extremos U_C ~ (eps/2)[V_C(r)+V_C(r')] para r o r' > 10
(la que usa el proyecto fuera de su tabla) frente al nucleo exacto propio (FEDVR, Rb=46).
Nystrom propio, R=40, h=0.02. Guarda resultados/v1f_extremos.json."""
import json, time
import numpy as np
from scipy.linalg import eigh
import v_fedvr as F

t0 = time.time()
Rb = 46.0
B = F.bordes_graduados(Rb, finos=((0.0, 0.05), (0.05, 0.125), (0.125, 0.25)), l1=0.25, r1=Rb)
fed = F.FEDVR(B, 14)
lamC, UC = eigh(fed.T + np.diag(fed.diag_funcion(lambda r: -1.0 / r)))
h, R = 0.02, 40.0
r = h * np.arange(1, int(round(R / h)))
Ph = fed.evalua(UC, r)
KD = lambda a, b, e: (np.exp(-(a - b)**2 / (2 * e)) - np.exp(-(a + b)**2 / (2 * e))) / np.sqrt(2 * np.pi * e)
A, Bm = np.meshgrid(r, r, indexing="ij")
out = {}
for eps in (0.2, 0.1, 0.05):
    rho = (Ph * np.exp(-eps * lamC)) @ Ph.T
    rho_ext = rho.copy()
    m = (A > 10) | (Bm > 10)
    rho_ext[m] = KD(A[m], Bm[m], eps) * np.exp(-0.5 * eps * (-1 / A[m] - 1 / Bm[m]))
    for d in (0.2, 1.0, 1.15):
        W = -np.expm1(-d * r) / r
        w = np.exp(-0.5 * eps * W)
        res = []
        for rr in (rho, rho_ext):
            Tm = h * rr * np.outer(w, w); Tm = 0.5 * (Tm + Tm.T)
            l = eigh(Tm, eigvals_only=True, subset_by_index=[len(r) - 1, len(r) - 1])[0]
            res.append(float(-np.log(l) / eps))
        out[f"d{d:g}_eps{eps:g}"] = dict(E_exacto=res[0], E_extremos=res[1], dif=res[1] - res[0])
        print(d, eps, out[f"d{d:g}_eps{eps:g}"], round(time.time() - t0, 1))
json.dump(out, open("resultados/v1f_extremos.json", "w"), indent=1)
