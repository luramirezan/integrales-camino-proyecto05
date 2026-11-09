"""V1 parte A: cifras radiales recalculadas por disparo (solve_ivp DOP853, rtol 1e-12) y por FEDVR.
Imprime y guarda resultados/v1a_radial.json."""
import json, time, os
import numpy as np
from scipy.optimize import brentq
from scipy.linalg import eigh
import v_disparo as D
import v_fedvr as F

t0 = time.time()
os.makedirs("resultados", exist_ok=True)
out = {}

def fed_E(Vf, R, extra=(), n=12, k=2, l3=4.0, saltos_Z=None):
    B = F.bordes_graduados(R, l3=l3, extra=tuple(extra) + (R / 2,))
    f = F.FEDVR(B, n)
    ev = eigh(f.T + np.diag(f.diag_funcion(Vf)), eigvals_only=True, subset_by_index=[0, k - 1])
    return ev

# ---- Coulomb ----
c1 = D.ligado(D.yukawa(0.0), -0.55, -0.45, 1.5)
c2 = D.ligado(D.yukawa(0.0), -0.13, -0.12, 6.5)
out["coulomb"] = dict(E0=c1["E0"], r=c1["r"], r2=c1["r2"], E1=c2["E0"], up0=c1["up0"],
                      E0_fedvr_R40=float(fed_E(lambda r: -1 / r, 40.0)[0]))
print("Coulomb", out["coulomb"])

# ---- Yukawa delta = 0.2 ----
y = D.ligado(D.yukawa(0.2), -0.35, -0.30, 1.5)
y2 = D.ligado(D.yukawa(0.2), -0.013, -0.011, 7.0)
E1_R60 = D.autovalor_caja(D.yukawa(0.2), 60.0, -0.0122, -0.0118)
fe = fed_E(D.yukawa(0.2), 60.0)
out["yukawa_0.2"] = dict(E0=y["E0"], r=y["r"], r2=y["r2"], rrms=y["rrms"], up0=y["up0"],
                         E1_libre=y2["E0"], E1_R60=E1_R60, E0_fedvr_R60=float(fe[0]), E1_fedvr_R60=float(fe[1]))
print("delta=0.2", out["yukawa_0.2"])
# delta=1.0 (referencia de Trotter con R=174)
y1 = D.ligado(D.yukawa(1.0), -0.0105, -0.0100, 4.0)
out["yukawa_1.0"] = dict(E0=y1["E0"], r=y1["r"], r2=y1["r2"], up0=y1["up0"])
print("delta=1.0", out["yukawa_1.0"])

# ---- umbrales por energia cero ----
rmax = lambda d: 60.0 / d
dc = D.umbral(D.yukawa, 1.18, 1.20, rmax)
# 2s: el umbral del segundo estado es donde la solucion de E=0 con un nodo tiene u'(inf)=0
dc2 = D.umbral(D.yukawa, 0.30, 0.32, rmax)
dcH = D.umbral(D.hulthen, 1.9, 2.1, lambda d: 80.0 / d)
dcH2 = D.umbral(D.hulthen, 0.45, 0.55, lambda d: 80.0 / d)
out["umbrales"] = dict(delta_c_1s=dc, delta_c_2s=dc2, hulthen_1s=dcH, hulthen_2s=dcH2,
                       dc_rmax_2x=D.umbral(D.yukawa, 1.18, 1.20, lambda d: 120.0 / d))
print("umbrales", out["umbrales"])

# ---- Hulthen ----
out["hulthen"] = {}
for d in (0.2, 1.0, 1.5):
    Eex = -0.5 * (1 - d / 2) ** 2
    k = np.sqrt(-2 * Eex)
    h = D.ligado(D.hulthen(d), Eex * 1.05, Eex * 0.95, 1.0 / k)
    h2 = D.ligado(D.hulthen(d), -0.5 / 4 * (1 - 2 * d) ** 2 * 1.05, -0.5 / 4 * (1 - 2 * d) ** 2 * 0.95, 4.5) if d < 0.5 else None
    rex = (12 - d**2) / (2 * (4 - d**2))
    out["hulthen"][str(d)] = dict(E0=h["E0"], E_exacta=Eex, dE=h["E0"] - Eex, r=h["r"], r_exacto=rex,
                                  dr_rel=(h["r"] - rex) / rex, r2=h["r2"],
                                  E1=(h2["E0"] if h2 else None), E1_exacta=(-0.125 * (1 - 2 * d) ** 2 if d < 0.5 else None))
    print("Hulthen", d, out["hulthen"][str(d)])

# ---- pozo cuadrado V=-V0 en r<1 ----
def pozo(V0):
    return lambda r: np.where(r < 1.0, -V0, 0.0)
out["pozo"] = {}
for V0, R in ((2.0, 60.0), (1.3, 385.0)):
    g = lambda E: np.sqrt(2 * (V0 + E)) / np.tan(np.sqrt(2 * (V0 + E))) + np.sqrt(-2 * E)
    Eex = brentq(g, -V0 + 1e-9 if V0 < 2.4 else -2.0, -1e-12, xtol=1e-16, rtol=1e-15)
    # cerca de -V0 g puede no cambiar de signo; se acota con un rastreo
    Es = np.linspace(-V0 + 1e-6, -1e-9, 20001); gs = g(Es)
    i = np.where(np.sign(gs[:-1]) != np.sign(gs[1:]))[0]
    raices = [brentq(g, Es[j], Es[j + 1], xtol=1e-17, rtol=1e-15) for j in i if abs(gs[j]) < 50]
    Eex = min(raices)
    s = D.ligado(pozo(V0), Eex * 1.02 - 1e-6, Eex * 0.98, 1.0 - 1e-9 + 0.5, Z=0.0, saltos=(1.0,))
    fe = fed_E(pozo(V0), R, extra=(1.0,))
    out["pozo"][str(V0)] = dict(E_exacta=Eex, E_disparo=s["E0"], r_disparo=s["r"], E_fedvr=float(fe[0]))
    print("pozo", V0, out["pozo"][str(V0)])
# umbral del pozo: V0 con energia cero ligada  (k a = pi/2)
out["pozo"]["umbral_disparo"] = brentq(lambda V0: D.cero(pozo(V0), 50.0, Z=0.0)[1], 1.1, 1.4, xtol=1e-15, rtol=1e-15)
out["pozo"]["umbral_exacto"] = np.pi**2 / 8
print("umbral pozo", out["pozo"]["umbral_disparo"] - np.pi**2 / 8)

# ---- cajas 9.6 ----
out["cajas"] = {}
for d in (1.15, 1.18, 1.20):
    V = D.yukawa(d)
    for R in (50, 100, 200, 400, 800):
        R = float(R)
        # FEDVR da el autovalor de caja (base independiente); el disparo lo refina y da observables
        Bf = F.bordes_graduados(R, l3=2.0, extra=(R / 2,))
        ff = F.FEDVR(Bf, 12)
        evf, vf = eigh(ff.T + np.diag(ff.diag_funcion(V)), subset_by_index=[0, 0])
        Ef = float(evf[0]); psi = vf[:, 0]
        dE = 1e-4 * abs(Ef) + 1e-10
        E0 = D.autovalor_caja(V, R, Ef - dE, Ef + dE)
        x = ff.x
        wl = [we[-1] for a, c, xe, we, idx in ff.elems if abs(c - R / 2) < 1e-9][0]
        j = np.argmin(abs(x - R / 2))
        fed = dict(E0=Ef, r_sobre_R=float(np.sum(psi**2 * x)) / R,
                   F12=float(np.sum(psi[x < R / 2 - 1e-9]**2) + psi[j]**2 * wl / ff.w[j]))
        kap = np.sqrt(max(-2 * E0, 0.0))
        if kap * R > 10:   # disparo hacia afuera pierde precision en la cola: estado libre
            o = D.ligado(V, E0 - 1e-6 * abs(E0), E0 + 1e-6 * abs(E0), 20.0)
            o = dict(E0=E0, r_sobre_R=o["r"] / R, F12=fed["F12"], r=o["r"], nota_F12="FEDVR")
        else:
            o = D.observables_caja(V, E0, R); o.pop("uR")
        o = {k: (float(v) if not isinstance(v, str) else v) for k, v in o.items()}
        o["fedvr"] = fed
        out["cajas"][f"{d:g}_R{int(R)}"] = o
        print("caja", d, R, out["cajas"][f"{d:g}_R{int(R)}"])
    u, up, a_s = D.cero(V, 60.0 / d)
    out["cajas"][f"a_s_{d:g}"] = a_s
    print("a_s", d, a_s)
out["tiempo_s"] = time.time() - t0
json.dump(out, open("resultados/v1a_radial.json", "w"), indent=1, default=float)
print("tiempo", out["tiempo_s"])
