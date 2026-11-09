"""V1 parte C: nucleo de Coulomb rho_C(r,r';eps) PROPIO, por suma espectral en base FEDVR (caja Rb=46,
distinta de la caja R_tab=14 de diferencias finitas del proyecto), evaluado punto a punto en la malla
de Nystrom; matriz de transferencia propia T_ij = h rho_C(r_i,r_j) e^{-eps(W_i+W_j)/2} (trapecio,
u(0)=0, sin pared en R salvo la de los nodos, como en el proyecto). Comprueba U_C en puntos, Coulomb,
delta=0.2 con h=0.02 y 0.04, estabilidad Nystrom y su orden. Guarda resultados/v1c_nystrom.json."""
import json, time, os
import numpy as np
from scipy.linalg import eigh
import v_fedvr as F

os.environ.setdefault("OMP_NUM_THREADS", "2")
t0 = time.time()
Rb = 46.0
B = F.bordes_graduados(Rb, finos=((0.0, 0.05), (0.05, 0.125), (0.125, 0.25)), l1=0.25, r1=Rb)
fed = F.FEDVR(B, 14)
lamC, UC = eigh(fed.T + np.diag(fed.diag_funcion(lambda r: -1.0 / r)))
lam0, U0 = eigh(fed.T)
print("FEDVR nodos", len(fed.x), "E0 Coulomb base", lamC[0], "t", time.time() - t0)

def KD(r, rp, eps):
    return (np.exp(-(r - rp)**2 / (2 * eps)) - np.exp(-(r + rp)**2 / (2 * eps))) / np.sqrt(2 * np.pi * eps)

out = {"FEDVR_nodos": len(fed.x), "Rb": Rb}
# --- U_C en puntos ---
pts = [(0.01, 0.01), (0.02, 0.02), (0.05, 0.05), (0.1, 0.1), (0.5, 0.5), (1.0, 1.0), (0.01, 0.5), (0.01, 1.0), (9.0, 9.0)]
r_all = np.array(sorted(set([p for q in pts for p in q])))
PhC = fed.evalua(UC, r_all); Ph0 = fed.evalua(U0, r_all)
out["U_C"] = {}
for eps in (0.2, 0.1, 0.05):
    rhoC = (PhC * np.exp(-eps * lamC)) @ PhC.T
    rho0 = (Ph0 * np.exp(-eps * lam0)) @ Ph0.T
    d = {}
    for a, b in pts:
        i, j = np.searchsorted(r_all, a), np.searchsorted(r_all, b)
        d[f"U({a:g},{b:g})"] = float(-np.log(rhoC[i, j] / KD(a, b, eps)))
        d[f"U_libre_red({a:g},{b:g})"] = float(-np.log(rhoC[i, j] / rho0[i, j]))
        d[f"err_rel_libre({a:g},{b:g})"] = float(rho0[i, j] / KD(a, b, eps) - 1)
    out["U_C"][str(eps)] = d
    print("eps", eps, {k: round(v, 9) for k, v in d.items() if k.startswith("U(")})
    print("     error relativo del nucleo libre en la base:", max(abs(v) for k, v in d.items() if k.startswith("err")))

def Wy(d):
    return (lambda r: -np.expm1(-d * r) / r) if d > 0 else (lambda r: 0.0 * r)

cache = {}
def rho_malla(h, R, eps):
    key = (h, R, eps)
    if key not in cache:
        r = h * np.arange(1, int(round(R / h)))
        Ph = fed.evalua(UC, r)
        cache[key] = (r, (Ph * np.exp(-eps * lamC)) @ Ph.T)
    return cache[key]

def E_nystrom(delta, h, eps, R=40.0):
    r, rho = rho_malla(h, R, eps)
    w = np.exp(-0.5 * eps * Wy(delta)(r))
    Tm = h * rho * np.outer(w, w)
    Tm = 0.5 * (Tm + Tm.T)
    N = len(r)
    l, v = eigh(Tm, subset_by_index=[N - 1, N - 1])
    psi = v[:, 0]; psi = psi / np.sqrt(h * np.sum(psi**2)) * np.sign(psi.sum())
    return float(-np.log(l[0]) / eps), float(h * np.sum(r * psi**2))

out["nystrom"] = {}
for delta in (0.0, 0.2):
    for eps in (0.2, 0.1, 0.05):
        row = {}
        for h in (0.04, 0.02, 0.01):
            row[str(h)] = E_nystrom(delta, h, eps)
        E4, E2, E1 = row["0.04"][0], row["0.02"][0], row["0.01"][0]
        row["orden_h"] = float(np.log2((E4 - E2) / (E2 - E1)))
        row["dE_0.02_0.04"] = E4 - E2
        row["rich_h4_002_004"] = float(E2 + (E2 - E4) / 15)
        row["rich_h4_001_002"] = float(E1 + (E1 - E2) / 15)
        out["nystrom"][f"d{delta:g}_eps{eps:g}"] = row
        print(f"delta={delta} eps={eps}", {k: v for k, v in row.items()}, "t", round(time.time() - t0, 1))
        for k in list(cache):
            if k[2] != eps:
                del cache[k]
out["tiempo_s"] = time.time() - t0
json.dump(out, open("resultados/v1c_nystrom.json", "w"), indent=1)
print("tiempo", out["tiempo_s"])
