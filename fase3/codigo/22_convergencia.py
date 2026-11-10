"""22_convergencia.py -- Proyecto 05, Fase 3: convergencia temporal y espacial de la integral de camino.
delta in {0.2, 0.8, 1.0, 1.15}; eps in {0.2, 0.1, 0.05, 0.025}; h in {0.04, 0.02, 0.01}.
Mide el orden de Trotter (con Richardson h^4 entre h = 0.02 y 0.01) y el orden de la malla Nystrom en cada delta,
y el presupuesto de errores en unidades de |E0|: Trotter, malla, pared en R (radial en R + 0.5826 sqrt(eps)),
y la diferencia final con el radial. Cajas: R tal que el estado quede bien dentro (R >= 25/kappa).
Salida: fase3/resultados/22_convergencia.json, fase3/figuras/22_convergencia.png.
"""
import json, os, sys, time
from multiprocessing import Pool
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comun3 as c  # noqa: E402

CASOS = {0.2: 40, 0.8: 100, 1.0: 174, 1.15: 600}
EPSS = (0.2, 0.1, 0.05, 0.025)
HS = (0.04, 0.02, 0.01)


def trabajo(arg):
    d, R, h, e = arg
    import warnings; warnings.simplefilter("ignore")
    ref = c.radial_ref(d, R)
    x = c.resolver_tr(d, R, h, e, ref["E0"])
    return (d, h, e, x)


if __name__ == "__main__":
    T0 = time.perf_counter()
    tareas = [(d, R, h, e) for d, R in CASOS.items() for h in HS for e in EPSS]
    tareas.sort(key=lambda t: -t[1] / t[2])
    with Pool(int(os.environ.get("NPROC", "1"))) as p:
        res = p.map(trabajo, tareas, chunksize=1)
    E = {(d, h, e): x["E0"] for d, h, e, x in res}
    rm = {(d, h, e): x["r_med"] for d, h, e, x in res}
    out = dict(script="22_convergencia.py", fecha="2026-11-10", casos={})
    for d, R in CASOS.items():
        ref = c.radial_ref(d, R)
        ref_fina = c.radial_ref(d, R, h=1 / 80)
        absE = abs(ref["E0"])
        orden_h = {}
        for e in EPSS:
            a, b, cc = E[(d, 0.04, e)], E[(d, 0.02, e)], E[(d, 0.01, e)]
            orden_h[f"{e:g}"] = float(np.log2(abs(a - b) / abs(b - cc)))
        EhR = {e: (16 * E[(d, 0.01, e)] - E[(d, 0.02, e)]) / 15 for e in EPSS}
        ordenes_t = [float(np.log2(abs(EhR[EPSS[i]] - EhR[EPSS[i + 1]]) / abs(EhR[EPSS[i + 1]] - EhR[EPSS[i + 2]])))
                     for i in range(2)]
        E_ext = c.ext_eps(EhR[0.05], EhR[0.025])
        E_ext_g = c.ext_eps(EhR[0.1], EhR[0.05])
        pared = {e: c.radial.resolver_rich(c.radial.V_yukawa(d), R + c.BETA * np.sqrt(e), h=1 / 40, nev=1)["E0"]
                 - ref["E0"] for e in EPSS}
        pared_ext = c.ext_eps(pared[0.05], pared[0.025])
        presupuesto = dict(
            trotter_eps01=abs(EhR[0.1] - E_ext) / absE, trotter_eps005=abs(EhR[0.05] - E_ext) / absE,
            malla_h002_eps005=abs(E[(d, 0.02, 0.05)] - EhR[0.05]) / absE,
            pared_eps01=abs(pared[0.1]) / absE, pared_extrapolada=abs(pared_ext) / absE,
            extrapolacion_eps=abs(E_ext - E_ext_g) / absE,
            final_menos_radial=abs(E_ext - ref["E0"]) / absE,
            radial_malla=abs(ref["E0"] - ref_fina["E0"]) / absE)
        out["casos"][f"{d:g}"] = dict(R=R, E_radial=ref["E0"], E_radial_h80=ref_fina["E0"], r_radial=ref["r_med"],
                                      E={f"h{h:g}_eps{e:g}": E[(d, h, e)] for h in HS for e in EPSS},
                                      r_med={f"h{h:g}_eps{e:g}": rm[(d, h, e)] for h in HS for e in EPSS},
                                      E_hRich={f"{e:g}": EhR[e] for e in EPSS}, orden_malla=orden_h,
                                      orden_trotter=ordenes_t, E_ext=E_ext, dif_radial=E_ext - ref["E0"],
                                      pared={f"{e:g}": pared[e] for e in EPSS}, pared_ext=pared_ext,
                                      presupuesto_rel=presupuesto)
        print(f"delta={d} R={R}: radial {ref['E0']:+.10e}; ext {E_ext:+.10e} (dif {E_ext-ref['E0']:+.1e}, "
              f"{abs(E_ext-ref['E0'])/absE:.1e} de |E0|); orden malla {[round(v,2) for v in orden_h.values()]}; "
              f"orden Trotter {[round(v,3) for v in ordenes_t]}", flush=True)
        print("   presupuesto/|E0|: " + ", ".join(f"{k}={v:.1e}" for k, v in presupuesto.items()), flush=True)
    out["tiempo_total_s"] = time.perf_counter() - T0
    json.dump(out, open(os.path.join(c.RES3, "22_convergencia.json"), "w"), indent=1, default=float)
