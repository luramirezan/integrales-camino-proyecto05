"""21_barrido_delta.py -- Proyecto 05, Fase 3: barrido en el apantallamiento (mu a g fijo, delta = mu hbar^2/(m g)).
(1) Radial en caja grande (R >= 25/kappa, iterado) para delta in {0.2, 0.5, 0.8, 1.0, 1.1, 1.15, 1.18, 1.19} y puntos
    extra cerca del umbral: curvas E0(delta), <r>(delta), kappa(delta).
(2) Integral de camino (transferencia extrapolada en h y eps, receta comun3.celda) en la misma caja, con tope R = 3200;
    si R necesaria > 3200 se marca "caja insuficiente" (el estado no cabe: el veredicto lo da 20_cajas).
(3) Ley cerca del umbral (avance de la Fase 4): ajuste kappa = A (delta_c - delta) + B (delta_c - delta)^2 con
    delta_c de referencia, y <r> kappa -> 1/2 (estado de cola e^{-kappa r}).
Salida: fase3/resultados/21_barrido.json, fase3/figuras/21_barrido.png.
"""
import json, os, sys, time
from multiprocessing import Pool
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comun3 as c  # noqa: E402

DELTAS = (0.2, 0.5, 0.8, 1.0, 1.1, 1.15, 1.18, 1.19)
EXTRA = (1.16, 1.17, 1.175, 1.185, 1.188)
RMAX_TR = 3200
H = {1.19: 1 / 160, 1.188: 1 / 80}   # malla del radial: con h = 1/40 el error de malla es > 10 % de |E0| (20c)


def caja_grande(d):
    R = 200.0
    for _ in range(12):
        x = c.radial_ref(d, R, h=H.get(d, 1 / 40))
        if x["E0"] >= 0:            # la caja aun no contiene el estado (cerca del umbral): se duplica R
            R *= 2
            continue
        Rn = c.radial.caja_recomendada(x["E0"], Rmin=40.0, factor=25.0, entera=True)
        if Rn <= R * 1.0001:
            return R, x
        R = Rn
    return R, c.radial_ref(d, R, h=H.get(d, 1 / 40))


def trabajo(d):
    import warnings; warnings.simplefilter("ignore")
    R, x = caja_grande(d)
    kappa = float(np.sqrt(-2 * x["E0"]))
    res = dict(delta=d, R_radial=R, radial=x, kappa=kappa, r_kappa=x["r_med"] * kappa)
    if d in DELTAS:
        Rt = min(R, RMAX_TR)
        res["R_tr"] = Rt
        res["caja_insuficiente"] = bool(R > RMAX_TR)
        res["tr"] = c.celda(d, Rt, verbose=True)
    print(f"delta={d}: R={R:.0f} E0={x['E0']:+.10e} <r>={x['r_med']:.4f} kappa={kappa:.4e} <r>kappa={res['r_kappa']:.4f}",
          flush=True)
    return res


if __name__ == "__main__":
    T0 = time.perf_counter()
    with Pool(int(os.environ.get("NPROC", "2"))) as p:
        res = p.map(trabajo, sorted(DELTAS + EXTRA, reverse=True), chunksize=1)
    res = sorted(res, key=lambda r: r["delta"])
    cerca = [r for r in res if r["delta"] >= 1.15]
    x = np.array([c.DELTA_C_REF - r["delta"] for r in cerca]); y = np.array([r["kappa"] for r in cerca])
    A = np.vstack([x, x**2]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    out = dict(script="21_barrido_delta.py", fecha="2026-11-10", delta_c_ref=c.DELTA_C_REF, puntos=res,
               ajuste_kappa=dict(forma="kappa = A (dc - d) + B (dc - d)^2", A=float(coef[0]), B=float(coef[1]),
                                 residuo_max=float(np.max(np.abs(A @ coef - y))), puntos=[r["delta"] for r in cerca]),
               tiempo_total_s=time.perf_counter() - T0)
    for r in res:
        r["radial"].pop("u", None)
    json.dump(out, open(os.path.join(c.RES3, "21_barrido.json"), "w"), indent=1, default=float)
    print(f"ajuste kappa: A={coef[0]:.5f} B={coef[1]:.5f}; tiempo {out['tiempo_total_s']:.0f} s")
