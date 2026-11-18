"""08_verificacion.py -- E5: comprobaciones independientes adicionales (para verificacion.md).

(a) Convergencia del Nystrom (C3) en delta = 1.2 y 1.3: paneles 300, 600, 1200 frente al disparo.
(b) Covarianza de escala camino a camino: misma semilla, delta = 1 y delta = 2.7 -> delta*Lambda identicos.
(c) Segundo momento del MC libre en delta = 4 frente a la EDO (E[W^2] = gauge de 2q): N = 2e6, eta = 0.2.
(d) MI con partida fija r0 = 0.5 en delta = 1.5: Y <= phi_T(r0) camino a camino y varianza relativa <= phi_T/phi - 1.
(e) E[Lambda] con partida fija r0 = 1 en delta = 2: frente a S(1) en forma cerrada.
(f) Guia subsolucion delta_T = 1.8 en delta = 1.5 (05 la corrio con eta = 0.2): sesgo y exponente de la cola del peso
    con eta = 0.2, 0.1, 0.05.
Salida: resultados/08_verificacion.json, resultados/08_verificacion_salida.txt.
"""
import json
import os
import sys
import time

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import fk_comun as fk  # noqa: E402

RES = os.path.join(AQUI, "../resultados")
REF = json.load(open(os.path.join(RES, "01_referencia_edo.json")))
LOG = []
T0 = time.perf_counter()


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


out = {}
# (a)
rg = REF["perfil"]["1.2"]["r"]
na = {}
for d in [1.2, 1.3]:
    ref = fk.phi_edo(d, rg)[0]
    filas = []
    for npan in [300, 600, 1200]:
        ph, a = fk.phi_nystrom(d, rg, n_pan=npan)
        filas.append(dict(n_pan=npan, dif_max_abs=float(np.max(np.abs(ph - ref))),
                          dif_max_rel=float(np.max(np.abs(ph / ref - 1))), dif_rel_a=float(a / fk.a_disparo(d) - 1)))
        log(f"(a) delta={d} n_pan={npan}: max|dphi| = {filas[-1]['dif_max_abs']:.2e} (rel {filas[-1]['dif_max_rel']:.2e}); "
            f"a rel {filas[-1]['dif_rel_a']:.1e}")
    na[f"{d:g}"] = filas
out["nystrom"] = na

# (b)
rng = np.random.default_rng(1)
y0 = rng.gamma(2, 1.0, 2000)
X1 = 1.0 * fk.simular_libre(y0 / 1.0, 1.0, 0.2, 36.0, 77)
X2 = 2.7 * fk.simular_libre(y0 / 2.7, 2.7, 0.2, 36.0 / 2.7, 77)
out["escala"] = dict(max_dif_rel=float(np.max(np.abs(X2 / X1 - 1))))
log(f"(b) covarianza de escala: max |X(2.7)/X(1) - 1| = {out['escala']['max_dif_rel']:.1e} en 2000 caminos")

# (c)
d = 4.0
N = 2_000_000
rng = np.random.default_rng(2026081)
r0 = rng.gamma(2, 1 / d, N)
W = np.exp(fk.simular_libre(r0, d, 0.2, 36 / d, 2026082))
EW2 = REF["momentos_libre"]["4"]["E_W2_gamma"]
b = (W * W)[: (N // 50) * 50].reshape(50, -1).mean(1)
out["segundo_momento"] = dict(delta=d, N=N, E_W2_mc=float((W * W).mean()), err_bloques=float(b.std(ddof=1) / np.sqrt(50)),
                              E_W2_edo=EW2, var_rel_mc=float(W.var() / W.mean() ** 2),
                              var_rel_edo=REF["momentos_libre"]["4"]["var_rel_gamma"])
log(f"(c) delta=4: E[W^2] MC = {(W*W).mean():.4f} +- {b.std(ddof=1)/np.sqrt(50):.4f} (bloques; W^2 tiene varianza "
    f"infinita porque 4 > theta = 3.36) frente a EDO {EW2:.4f}; var_rel {W.var()/W.mean()**2:.4f} frente a "
    f"{REF['momentos_libre']['4']['var_rel_gamma']:.4f}")
del W, r0

# (d)
d, r00 = 1.5, 0.5
dT = fk.dT_para_razon(d, 1.25)
g = fk.Guia(d, dT, 36 / dT)
N = 100_000
L = fk.simular_guiado(np.full(N, r00), g, 0.1, 2026090)
Y = float(g.phiT(r00)) * np.exp(-L)
ph = float(fk.phi_edo(d, [r00])[0][0])
phT = float(g.phiT(r00))
out["mi_partida_fija"] = dict(delta=d, r0=r00, N=N, eta=0.1, Y_max=float(Y.max()), phiT_r0=phT, phi_edo=ph,
                              media=float(Y.mean()), err=float(Y.std(ddof=1) / np.sqrt(N)),
                              var_rel=float(Y.var(ddof=1) / Y.mean() ** 2), cota=phT / ph - 1)
log(f"(d) MI delta=1.5 r0=0.5 (eta=0.1): max Y = {Y.max():.6f} <= phi_T(r0) = {phT:.6f}; media {Y.mean():.5f} +- "
    f"{Y.std(ddof=1)/np.sqrt(N):.5f} frente a phi = {ph:.5f}; var_rel {Y.var(ddof=1)/Y.mean()**2:.4f} <= cota {phT/ph-1:.4f}")

# (e)
d = 2.0
N = 1_000_000
Lam = fk.simular_libre(np.ones(N), d, 0.2, 36 / d, 2026095)
S1 = REF["momentos_libre"]["2"]["E_Lambda_r"]["1"]
out["E_Lambda_r1"] = dict(delta=d, N=N, media=float(Lam.mean()), err=float(Lam.std(ddof=1) / np.sqrt(N)), exacto=S1)
log(f"(e) delta=2, r0=1: E[Lambda] = {Lam.mean():.5f} +- {Lam.std(ddof=1)/np.sqrt(N):.5f} frente a S(1) = {S1:.5f}")

# (f)
d, dT = 1.5, 1.8
g = fk.Guia(d, dT, 36 / d)
a_edo = fk.a_disparo(d)
filas = []
for k, (eta, N) in enumerate([(0.2, 100_000), (0.1, 100_000), (0.05, 40_000)]):
    rng = np.random.default_rng(2026100 + k)
    r0 = rng.gamma(2, 1 / d, N)
    L = fk.simular_guiado(r0, g, eta, 2026110 + k)
    Y = g.phiT(r0) * np.exp(-L)
    a = -(2 / d ** 2) * Y.mean()
    e = 2 / d ** 2 * Y.std(ddof=1) / np.sqrt(N)
    G = -L
    u = np.quantile(G, 0.99)
    th = 1 / (G[G > u] - u).mean()
    filas.append(dict(eta=eta, N=N, a=float(a), err=float(e), dif_rel=float(a / a_edo - 1), theta=float(th),
                      err_theta=float(th / np.sqrt((G > u).sum()))))
    log(f"(f) subsolucion delta_T=1.8, eta={eta}: a = {a:+.5f} +- {e:.5f} (dif_rel {a/a_edo-1:+.2e}); theta cola = "
        f"{th:.3f} +- {th/np.sqrt((G > u).sum()):.3f}")
out["subsolucion_eta"] = filas

out["tiempo_s"] = time.perf_counter() - T0
log(f"tiempo total {out['tiempo_s']:.1f} s")
json.dump(out, open(os.path.join(RES, "08_verificacion.json"), "w"), indent=1)
open(os.path.join(RES, "08_verificacion_salida.txt"), "w").write("\n".join(LOG) + "\n")
