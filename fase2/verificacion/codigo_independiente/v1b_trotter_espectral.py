"""V1 parte B: operador de Trotter construido espectralmente en base FEDVR (sin tabla U_C, sin Nystrom).
E(eps), orden de Trotter, extrapolacion, Hulthen, pozo, proyeccion E_mixto(tau) y cajas 9.6.
Guarda resultados/v1b_trotter.json."""
import json, time, sys
import numpy as np
import v_fedvr as F
import v_trotter as T
import v_disparo as D

t0 = time.time()
out = {}
n_el = int(sys.argv[1]) if len(sys.argv) > 1 else 12
l1 = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
sufijo = sys.argv[3] if len(sys.argv) > 3 else ""
solo_basico = len(sys.argv) > 4
coul = lambda r: -1.0 / r
Wy = lambda d: (lambda r: -np.expm1(-d * r) / r)
def WH(d):
    def f(r):
        x = d * r
        return np.where(x < 1e-3, d * (0.5 - x / 12 + x**3 / 720), 1.0 / r - d / np.expm1(np.minimum(x, 700)))
    return f
EPS3 = (0.2, 0.1, 0.05)
EPS4 = (0.2, 0.1, 0.05, 0.025)

def serie(S, W, epss):
    res = [S.trotter(W, e) for e in epss]
    d = dict(eps=list(epss), E=[r["E"] for r in res], r=[r["r"] for r in res], r2=[r["r2"] for r in res],
             F12=[r["F12"] for r in res], perron_min=min(r["perron_min"] for r in res))
    d["orden"], d["ext_orden"] = T.orden_y_ext(d["E"][:3])
    d["ext_eps2"], d["ext_eps2_2pts"] = T.ext_eps2(d["E"][:3])
    d["orden_r"], d["r_ext_orden"] = T.orden_y_ext(d["r"][:3])
    d["r_ext_eps2"], _ = T.ext_eps2(d["r"][:3])
    if len(epss) >= 4:
        d["orden_fino"], d["ext_orden_fino"] = T.orden_y_ext(d["E"][1:4])
        d["r_ext_eps2_fino"], _ = T.ext_eps2(d["r"][1:4])
    return d

def esp(R, Vc, extra=(), l3=4.0, finos=None, l1_=None):
    kw = {} if finos is None else dict(finos=finos)
    B = F.bordes_graduados(R, l1=(l1_ or l1), l3=l3, extra=tuple(extra) + (R / 2,), **kw)
    return T.Espectral(F.FEDVR(B, n_el), Vc)

# --- Coulomb y Yukawa ---
S40 = esp(40.0, coul)
out["coulomb"] = serie(S40, lambda r: 0.0 * r, EPS3)
print("Coulomb", out["coulomb"]["E"], out["coulomb"]["r"])
out["yukawa_0.2"] = serie(S40, Wy(0.2), EPS4)
print("d=0.2", out["yukawa_0.2"]["E"], out["yukawa_0.2"]["orden"], out["yukawa_0.2"]["ext_orden"], out["yukawa_0.2"]["ext_eps2"])
print("     r", out["yukawa_0.2"]["r"])
if not solo_basico:
    S174 = esp(174.0, coul)
    out["yukawa_1.0"] = serie(S174, Wy(1.0), EPS4)
    print("d=1.0", out["yukawa_1.0"]["E"], out["yukawa_1.0"]["orden"], out["yukawa_1.0"]["ext_orden"], out["yukawa_1.0"]["ext_eps2"])
    print("     r", out["yukawa_1.0"]["r"])

# --- Hulthen ---
out["hulthen"] = {}
for d, R in ((0.2, 60.0), (1.0, 60.0), (1.5, 100.0)):
    S = esp(R, coul)
    out["hulthen"][str(d)] = serie(S, WH(d), EPS4)
    h = out["hulthen"][str(d)]
    Eex = -0.5 * (1 - d / 2)**2
    print("Hulthen", d, "E-Eex", [e - Eex for e in h["E"]], "orden", h["orden"], "ext_eps2-Eex", h["ext_eps2"] - Eex,
          "r_ext-rex", h["r_ext_eps2"] - (12 - d**2) / (2 * (4 - d**2)))

# --- pozo cuadrado: kinetica libre exacta en FEDVR, V completo en e^{-eps V} (salto en un borde) ---
out["pozo"] = {}
EPSP = (0.2, 0.1, 0.05, 0.025, 0.0125)
finos_p = ((0.0, 0.25), (0.25, 0.5), (0.5, 0.75), (0.75, 0.9), (0.9, 1.0), (1.0, 1.1), (1.1, 1.25), (1.25, 1.5))
for V0, R in ((2.0, 60.0), (1.3, 385.0)):
    S = esp(R, None, extra=(1.0,), finos=finos_p)
    Vp = lambda r, V0=V0: np.where(r < 1.0, -V0, 0.0)
    res = [S.trotter(Vp, e) for e in EPSP]
    E = [r["E"] for r in res]
    ords = [float(np.log2((E[i] - E[i + 1]) / (E[i + 1] - E[i + 2]))) for i in range(len(E) - 2)]
    p = ords[-1]
    ext = E[-1] - (E[-2] - E[-1]) / (2**p - 1)
    ext15 = E[-1] - (E[-2] - E[-1]) / (2**1.5 - 1)
    a, b, c = E[:3]
    ext_plan = float(c + (c - b) / 3)  # ley eps^2 de dos puntos (0.1, 0.05)
    out["pozo"][str(V0)] = dict(eps=list(EPSP), E=E, r=[r["r"] for r in res], ordenes=ords, ext_orden_medido=float(ext),
                                ext_eps15=float(ext15), ext_eps2_plan=ext_plan)
    print("pozo", V0, "E", E, "ordenes", ords, "ext", ext, "ext15", ext15)
    print("      r", [r["r"] for r in res])

# --- proyeccion: E_mixto(tau), <r> y <r^2> puros, delta=0.2, eps=0.1 ---
uT = lambda r: r * np.exp(-r)
out["proyeccion"] = {}
for eps in (0.1,):
    taus = [2.0, 4.0, 6.0, 10.0, 20.0, 30.0] if False else [1.0 * 2, 5.0 * 2 / 2, 10.0, 20.0, 30.0]
pr = S40.pigs_det(Wy(0.2), lambda r: Wy(0.2)(r) - 0.5, uT, 0.1, [2.0, 4.0, 6.0, 10.0, 20.0, 30.0, 60.0])
pr5 = S40.pigs_det(Wy(0.2), lambda r: Wy(0.2)(r) - 0.5, uT, 0.1, [5.0 + 0.0]) if False else None
out["proyeccion"]["eps0.1"] = {str(k): v for k, v in pr.items()}
# tau=1,5,15 requieren n impar o especial: se calculan con mixto sin punto medio exacto
for k, v in pr.items():
    print("tau", k, v)
out["proyeccion"]["E0_T"] = out["yukawa_0.2"]["E"][1]

# --- cajas 9.6 con pared Dirichlet verdadera (imagen tambien en R) ---
if not solo_basico:
    out["cajas"] = {}
    for d in (1.15, 1.18, 1.20):
        for R in (50.0, 100.0, 200.0, 400.0, 800.0):
            S = esp(R, coul, l3=2.0 if R <= 200 else 4.0)
            s = serie(S, Wy(d), EPS3)
            s.pop("perron_min")
            out["cajas"][f"{d:g}_R{int(R)}"] = s
            print("caja", d, R, "E", s["E"], "ext", s["ext_eps2"], "orden", s["orden"], "r/R", s["r_ext_eps2"] / R,
                  "F12", s["F12"][-1])
    # prueba de la pared corrida beta*sqrt(eps) (hipotesis del proyecto, seccion 14)
    beta = 0.5825971579390106
    out["pared"] = {}
    for d in (1.15, 1.18, 1.20):
        for R in (50.0, 100.0):
            Es = []
            for e in EPS3:
                S = esp(R + beta * np.sqrt(e), coul, l3=2.0)
                Es.append(S.trotter(Wy(d), e)["E"])
            out["pared"][f"{d:g}_R{int(R)}"] = Es
            print("pared", d, R, Es)
out["n_el"] = n_el; out["l1"] = l1
out["tiempo_s"] = time.time() - t0
json.dump(out, open(f"resultados/v1b_trotter{sufijo}.json", "w"), indent=1, default=float)
print("tiempo", out["tiempo_s"])
