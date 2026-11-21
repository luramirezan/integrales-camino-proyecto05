"""07_verificacion.py -- E3: comprobaciones independientes de los resultados de 01-05.

V1 Tercer metodo para delta_c, sin la funcion de onda: metodo de fase variable (Calogero) para b(r) = 1/a(r),
   la inversa de la longitud de dispersion del potencial truncado en r:  db/dr = -2 V(r) (1 - r b)^2.
   Se integra con LSODA (otro integrador) desde r0 = 1e-8 con a(r0) = -r0^2 (Born con V ~ -1/r).
V2 Disparo con empalme frente al radial de la Fase 3 (fase3/resultados/21_barrido.json, Yukawa, cajas grandes).
V3 Hulthen <r> exacto (radial.hulthen_exacto, sympy) frente al disparo, delta = 1.0, 1.5, 1.9.
V4 Hulthen: polo virtual exacto? Se compara kappa_v (03) con delta/2 - 1 (imagen especular del ligado 1 - delta/2).
V5 Yukawa: c frente a A = 0.7411 y B_pred frente a B = 0.059 de la Fase 3.
Criterios fijados ANTES de correr:
  V1 |delta_c(fase variable) - delta_A| < 1e-9 (cuatro perfiles)
  V2 |E_disparo - E_radial| < 2 err_radial + 1e-9 (err_radial de la Fase 3, |E_h - E_h/2|) en los delta de la Fase 3
     con R >= 25/kappa
  V3 |<r> - <r>_exacto|/<r>_exacto < 1e-9
  V4 informativo (no se conocia de antemano): max |kappa_v - (delta/2 - 1)|/kappa_v
  V6 informativo (anadido despues): maximo de phi0 en delta_c (explica el signo de r_e)
  V5 |c - 0.7411| < 5e-4 y |B_pred - 0.059| < 0.01 (la Fase 3 da A y B con 4 y 2 cifras)
"""
import json
import os
import sys

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

import comun_e3 as C
import perfiles as P

sys.path.insert(0, C.F2)
import radial  # noqa: E402

CRIT = {
    "V1": "|delta_c(fase variable, LSODA) - delta_A| < 1e-9",
    "V2": "|E_disparo - E_radial(Fase 3)| < 2 err_radial + 1e-9",
    "V3": "Hulthen |<r> - exacto|/exacto < 1e-9",
    "V4": "informativo: kappa_v de Hulthen frente a delta/2 - 1",
    "V5": "|c - 0.7411| < 5e-4 y |B_pred - 0.059| < 0.01 (Yukawa, Fase 3)",
}


def b_inf(perfil, d):
    V = P.PERFILES[perfil]["V"](d)
    r0 = 1e-8
    f = lambda r, b: [-2.0 * V(r) * (1.0 - r * b[0])**2]
    s = solve_ivp(f, [r0, P.rmax(d)], [-1.0 / r0**2], method="LSODA", rtol=1e-12, atol=1e-14)
    return float(s.y[0, -1])


def main():
    T = C.Tee("07_verificacion")
    U = C.cargar("01_umbrales")["perfiles"]
    D2 = C.cargar("02_dispersion")["perfiles"]
    D3 = C.cargar("03_ligados_virtuales")["perfiles"]
    out = dict(script="07_verificacion.py", criterios=CRIT)
    ok = {}
    # V1
    v1 = {}
    for k in C.ORDEN:
        a, b = P.PERFILES[k]["bracket"]
        dv = brentq(lambda d: b_inf(k, d), a, b, xtol=1e-14, rtol=1e-15)
        v1[k] = dict(delta_fase_variable=float(dv), delta_A=U[k]["delta_A"], dif=float(dv - U[k]["delta_A"]),
                     b_vs_inv_a_en_1p01=float(b_inf(k, 1.01 * U[k]["delta_A"]) - P.inv_a(k, 1.01 * U[k]["delta_A"])))
        T(f"V1 {k:8s} fase variable {dv:.13f}  delta_A {U[k]['delta_A']:.13f}  dif {dv - U[k]['delta_A']:+.1e}  "
          f"(b - 1/a en 1.01 dc: {v1[k]['b_vs_inv_a_en_1p01']:+.1e})")
    ok["V1"] = all(abs(x["dif"]) < 1e-9 for x in v1.values())
    out["V1"] = v1
    # V2
    with open(os.path.join(C.PROY, "fase3", "resultados", "21_barrido.json")) as fh:
        F3 = json.load(fh)
    v2 = []
    for pt in F3["puntos"]:
        d = pt["delta"]; rad = pt["radial"]
        L = P.ligado("yukawa", d, observables=False)
        if pt["R_radial"] * L["kappa"] < 25 - 1e-9:
            continue
        err = rad["err"]          # |E_h - E_h/2| del radial de la Fase 3 (comun3.radial_ref)
        v2.append(dict(delta=d, R=pt["R_radial"], E_radial=rad["E0"], err_radial=err, E_disparo=L["E0"],
                       dif=float(L["E0"] - rad["E0"])))
        T(f"V2 yukawa d={d:<7} R={pt['R_radial']:<8.0f} radial={rad['E0']:+.12e} (err {err:.1e})  disparo={L['E0']:+.12e}  "
          f"dif={L['E0'] - rad['E0']:+.1e}")
    ok["V2"] = bool(len(v2) > 0 and all(abs(x["dif"]) < 2 * x["err_radial"] + 1e-9 for x in v2))
    out["V2"] = v2
    # V3
    v3 = []
    for d in (1.0, 1.5, 1.9):
        ex = radial.hulthen_exacto(d)
        L = P.ligado("hulthen", d)
        v3.append(dict(delta=d, r_med=L["r_med"], r_med_exacto=ex["r_med"], dif_rel=float((L["r_med"] - ex["r_med"]) / ex["r_med"]),
                       r_med_formula=(12 - d**2) / (2 * (4 - d**2))))
        T(f"V3 hulthen d={d}: <r> disparo {L['r_med']:.12f}  exacto {ex['r_med']:.12f}  formula {(12-d**2)/(2*(4-d**2)):.12f}")
    ok["V3"] = all(abs(x["dif_rel"]) < 1e-9 for x in v3)
    out["V3"] = v3
    # V4
    vir = D3["hulthen"]["virtuales"]
    dmax = max(abs(x["kappa_v_dir"] - (x["delta"] / 2 - 1)) / x["kappa_v_dir"] for x in vir)
    out["V4"] = dict(max_dif_rel=float(dmax))
    T(f"V4 hulthen: max |kappa_v - (delta/2 - 1)|/kappa_v = {dmax:.1e}")
    # V5
    c, Bp = D2["yukawa"]["c_HF"], D2["yukawa"]["B_pred"]
    ajF3 = F3["ajuste_kappa"]
    out["V5"] = dict(c=c, A_fase3=ajF3["A"], B_pred=Bp, B_fase3=ajF3["B"])
    ok["V5"] = bool(abs(c - C.A_FASE3) < 5e-4 and abs(Bp - 0.059) < 0.01)
    T(f"V5 yukawa: c = {c:.6f} (Fase 3 A = {ajF3['A']:.6f});  B_pred = {Bp:.5f} (Fase 3 B = {ajF3['B']:.5f})")
    # V6 (informativo, anadido al redactar la explicacion de r_e < 0 del ECSC): maximo de la solucion de energia cero
    # en delta_c, normalizada a phi -> 1. r_e = 2 int (1 - phi^2) dr en el umbral: r_e < 0 exige phi > 1 en buena parte.
    v6 = {}
    for k in C.ORDEN:
        d = U[k]["delta_A"]; p = P.PERFILES[k]; rf = P.rmax(d)
        s = P._integrar(p["V"](d), p["W0"](d), 0.0, rf, dense=True)
        al = s.y[0, -1] - rf * s.y[1, -1]
        rr = np.linspace(1e-6, rf, 200001); phi = s.sol(rr)[0] / al
        i = int(np.argmax(phi))
        v6[k] = dict(phi_max=float(phi[i]), r_max=float(rr[i]), delta_r_max=float(rr[i] * d))
        T(f"V6 {k:8s} max phi0 = {phi[i]:.6f} en r = {rr[i]:.4f} (delta r = {rr[i]*d:.4f})")
    out["V6"] = v6
    out["pasa"] = ok
    T("controles:", ok)
    C.guardar("07_verificacion", out)
    T.cerrar()


if __name__ == "__main__":
    main()
