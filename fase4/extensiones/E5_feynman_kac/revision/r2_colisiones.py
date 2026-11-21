"""r2_colisiones.py -- Revision independiente de E5: MC SIN caminos (estimador de colisiones de la serie de Neumann).
phi(r) = 1 + int_0^inf K(r,r') phi(r') dr',  K = 2 r'^2 q(r')/max(r,r')  (Green radial de -1/2 Lap).
S(r) = int K(r,r') dr' = E_r[Lambda].  Estimador: Z(r0) = sum_n prod_{j<n} S(r_j),  r_{j+1} ~ K(r_j, .)/S(r_j).
Para delta > 2, S <= S(0) = 2/delta < 1 y Z <= 1/(1 - 2/delta): acotado, sin discretizacion. Semilla propia 777001.
a = -(2/delta^2) E_{r0 ~ Gamma(2,1/delta)}[Z(r0)]."""
import json, os, time
import numpy as np
AQ = os.path.dirname(os.path.abspath(__file__))

def S(r, d):
    return 2 * (-np.expm1(-d * r) - d * r * np.exp(-d * r)) / (d * d * r) + 2 * np.exp(-d * r) / d

def salto(r, d, rng):
    """r' con densidad prop. a r' e^{-d r'}/max(r, r')."""
    M1 = (-np.expm1(-d * r) - d * r * np.exp(-d * r)) / (d * d * r)
    M2 = np.exp(-d * r) / d
    out = np.empty_like(r)
    zona2 = rng.random(r.size) < M2 / (M1 + M2)
    out[zona2] = r[zona2] + rng.exponential(1 / d, zona2.sum())
    idx = np.flatnonzero(~zona2)
    while idx.size:        # r' en (0, r) con densidad prop. a r' e^{-d r'}: propuesta r sqrt(U), acepta e^{-d r'} ...
        rr = r[idx]
        chico = d * rr < 2.0
        prop = np.where(chico, rr * np.sqrt(rng.random(idx.size)), rng.gamma(2.0, 1 / d, idx.size))
        acc = np.where(chico, rng.random(idx.size) < np.exp(-d * prop), prop < rr)
        out[idx[acc]] = prop[acc]
        idx = idx[~acc]
    return out

def Z(r0, d, rng, tol=1e-15):
    r = r0.copy(); prod = np.ones_like(r); tot = np.ones_like(r)
    while prod.max() > tol:
        prod *= S(r, d); tot += prod
        r = salto(r, d, rng)
    return tot

out = {}
t0 = time.time()
rng = np.random.default_rng(777001)
for d in [3.0, 4.0, 2.5]:
    N = 2_000_000
    z = np.concatenate([Z(rng.gamma(2.0, 1 / d, N // 10), d, rng) for _ in range(10)])
    a = -(2 / d**2) * z.mean(); e = 2 / d**2 * z.std(ddof=1) / np.sqrt(N)
    res = dict(N=N, a=a, err=e, Zmax=float(z.max()), cota=1 / (1 - 2 / d), var_rel=float(z.var() / z.mean()**2))
    phis = {}
    for r in [0.05, 0.5, 1.0, 4.0]:
        zz = Z(np.full(400_000, r), d, rng)
        phis[f"{r:g}"] = [float(zz.mean()), float(zz.std(ddof=1) / np.sqrt(zz.size))]
    res["phi"] = phis
    out[f"{d:g}"] = res
    print(f"delta={d}: a_colisiones = {a:+.6f} +- {e:.6f}; Zmax {z.max():.4f} (cota {1/(1-2/d):.4f}); var_rel {res['var_rel']:.4f}; phi {phis}", flush=True)
out["tiempo_s"] = time.time() - t0
json.dump(out, open(os.path.join(AQ, "r2_colisiones.json"), "w"), indent=1)
print("tiempo", out["tiempo_s"])
