"""45_transferencia_l1.py -- E4, tarea 4: integral de camino en tiempo imaginario para la onda p (l = 1).

Metodo elegido (a): matriz de transferencia radial en la onda parcial l = 1 con
    T_ij = h K_1(r_i, r_j; eps) e^{-U_1(r_i, r_j; eps)} e^{-eps [W(r_i) + W(r_j)]/2},
K_1 el nucleo libre EXACTO de la onda p (lleva el centrifugo exacto), U_1 la accion de pares exacta del Coulomb en la
onda p (tablas del script 44) y W = V_Yukawa - V_Coulomb = (1 - e^{-delta r})/r, acotado en [0, delta].
Comparacion (b): aproximacion primitiva para la barrera centrifuga, con la accion de pares de l = 0 de la Fase 2:
    T_ij = h K_D e^{-U_0} e^{-eps [W + 1/r^2]_i/2 - eps [W + 1/r^2]_j/2}.
Receta de la Fase 3: h = 0.04 y 0.02 con Richardson (exponente medido aqui en Coulomb y en delta = 0.2 con h = 0.01),
eps = 0.2, 0.1, 0.05 con extrapolacion eps -> 0 (ley eps^2 si el orden medido lo confirma), error = suma lineal de
malla + Trotter + sesgo de pared (radial en R + 0.5826 sqrt(eps), solo en el error).
Casos: Coulomb 2p (R = 60, E = -1/8 exacto) y Yukawa delta = 0.10, 0.16, 0.20, 0.215, 0.219 (R = 100) frente al
radial en la misma caja (h = 1/160 con Richardson).
Criterios fijados ANTES de correr (17-11-2026):
  (a): |E_mejor - E_ref| <= 2 (err + err_ref) en los 6 casos; Coulomb: |E - (-1/8)| < 1e-7; orden de Trotter entre 1.8
       y 2.2; autovector de signo constante (Perron, min >= -1e-12 relativo) y T >= 0.
  (b): se mide su orden de Trotter y su sesgo; no se le exige pasar (es la comparacion).
Salida: resultados/45_transferencia_l1.json y _salida.txt.
"""
import math
import sys
import time

import numpy as np

import comun4 as c
import pares_l as pl
import transferencia as tr

sys.path.insert(0, c.F3)
import comun3  # noqa: E402  (tablas l = 0 de la Fase 2, solo lectura de la cache)

T0 = time.time()
c.Tee("45_transferencia_l1")
L = 1
EPSS = (0.2, 0.1, 0.05)
HS = (0.04, 0.02)
BETA = tr.BETA_PARED
TAB1 = {e: pl.tabla_richardson_l(L, e) for e in EPSS}
out = dict(criterios=dict(coulomb=1e-7, trotter=(1.8, 2.2), perron=-1e-12), casos=[])


def W_total(delta, primitiva):
    Wy = tr.W_yukawa(delta) if delta > 0 else (lambda r: np.zeros_like(r))
    if primitiva:
        return lambda r: Wy(r) + 1.0 / r**2          # l(l+1)/2 = 1 para l = 1
    return Wy


def corre(delta, R, h, eps, metodo, Eg):
    if metodo == "a":
        T, r = pl.matriz_T_l(R, h, eps, L, W=W_total(delta, False), tabla=TAB1[eps])
    else:
        T, r = tr.matriz_T(R, h, eps, W=W_total(delta, True), tabla=comun3.tabla(eps))
    return pl.resolver_T(T, r, R, eps, Eg, h)


def radial_ref(delta, R, h=1 / 160):
    V = c.V_yukawa_np(delta) if delta > 0 else (lambda r: -1.0 / r)
    d = c.fd_rich(V, L, R, h=h, nev=1)
    return dict(E0=d["E0"], err=abs(d["E0"] - d["E0_h2"]) / 15 + 2e-11, r_med=d["r_med"], r2_med=d["r2_med"])


# ------------------------------------------------------------------ orden en h (Coulomb y delta = 0.2, eps = 0.1)
print("Orden de la malla h en la transferencia (a), eps = 0.1")
orden_h = {}
for delta, R in ((0.0, 60.0), (0.2, 100.0)):
    ref = radial_ref(delta, R)
    Es = [corre(delta, R, h, 0.1, "a", ref["E0"])["E0"] for h in (0.04, 0.02, 0.01)]
    p = math.log2(abs(Es[0] - Es[1]) / abs(Es[1] - Es[2]))
    orden_h[str(delta)] = dict(E=Es, p=p)
    print(f"  delta = {delta}: E(h=0.04, 0.02, 0.01) = {Es[0]:.12f}, {Es[1]:.12f}, {Es[2]:.12f}; orden aparente {p:.3f}",
          flush=True)
out["orden_h"] = orden_h
# Las diferencias entre mallas son de 1e-11 a 2e-11, al nivel de la precision del autovalor: el orden aparente
# (7.2 en Coulomb, 2.2 en delta = 0.2) no es medible. Se usa el exponente 4 de la receta de la Fase 3 (decision 1)
# y se guarda tambien el resultado con el promedio de los dos ordenes aparentes (4.7, primera corrida) para mostrar
# que la eleccion cambia E en menos de 1e-11 (verificacion.md).
dif_mallas = max(max(abs(v["E"][0] - v["E"][1]), abs(v["E"][1] - v["E"][2])) for v in orden_h.values())
out["dif_mallas_max"] = dif_mallas
ph_usado = 4.0
ph_alt = float(np.mean([v["p"] for v in orden_h.values()]))
out["orden_h_usado"] = ph_usado
out["orden_h_alternativo"] = ph_alt
fh = 2.0**ph_usado
fh_alt = 2.0**ph_alt
print(f"  diferencia maxima entre mallas {dif_mallas:.1e}; exponente de Richardson usado en h: {ph_usado} "
      f"(alternativo {ph_alt:.2f})")


def ext_eps(e1, e2, p=2.0):
    return e2 + (e2 - e1) / (2**p - 1)


CASOS = [(0.0, 60.0), (0.10, 100.0), (0.16, 100.0), (0.20, 100.0), (0.215, 100.0), (0.219, 100.0)]
for delta, R in CASOS:
    t = time.time()
    ref = radial_ref(delta, R)
    caso = dict(delta=delta, R=R, radial=ref, metodos={})
    pared = {e: radial_ref(delta, R + BETA * math.sqrt(e), h=1 / 80)["E0"] - radial_ref(delta, R, h=1 / 80)["E0"]
             for e in EPSS}
    pared_ext = ext_eps(pared[0.1], pared[0.05])
    caso["pared"] = dict(por_eps={str(k): v for k, v in pared.items()}, extrapolado=pared_ext)
    for metodo in ("a", "b"):
        crudo, E = {}, {}
        for h in HS:
            for e in EPSS:
                d = corre(delta, R, h, e, metodo, ref["E0"])
                crudo[f"h{h:g}_eps{e:g}"] = d
                E[(h, e)] = d["E0"]
        EhR = {e: (fh * E[(0.02, e)] - E[(0.04, e)]) / (fh - 1) for e in EPSS}
        EhR_alt = {e: (fh_alt * E[(0.02, e)] - E[(0.04, e)]) / (fh_alt - 1) for e in EPSS}
        den = abs(EhR[0.1] - EhR[0.05])
        p_trot = float(math.log2(abs(EhR[0.2] - EhR[0.1]) / den)) if den > 0 else float("nan")
        p_ext = 2.0 if metodo == "a" else max(p_trot, 0.5)     # (b): con el orden medido
        Eb = ext_eps(EhR[0.1], EhR[0.05], p_ext)
        Eg_ = ext_eps(EhR[0.2], EhR[0.1], p_ext)
        Eh2 = ext_eps(E[(0.02, 0.1)], E[(0.02, 0.05)], p_ext)
        err = abs(Eh2 - Eb) + abs(Eb - Eg_) + abs(pared_ext)
        r_b = {k: ext_eps(crudo[f"h0.02_eps0.1"][k], crudo[f"h0.02_eps0.05"][k], p_ext) for k in ("r_med", "r2_med")}
        m = dict(E_hRich={str(k): v for k, v in EhR.items()}, orden_trotter=p_trot, p_extrapolacion=p_ext, E_mejor=Eb,
                 err=err, dif_radial=Eb - ref["E0"], compatible=bool(abs(Eb - ref["E0"]) <= 2 * (err + ref["err"])),
                 sesgo_eps01_rel=(EhR[0.1] - ref["E0"]) / abs(ref["E0"]), sesgo_eps005=EhR[0.05] - ref["E0"],
                 r_med=r_b["r_med"], r2_med=r_b["r2_med"], dif_r=r_b["r_med"] - ref["r_med"],
                 perron_min=min(d["perron_min"] for d in crudo.values()),
                 min_T=min(d["min_T"] for d in crudo.values()),
                 residuo_max=max(d["residuo"] for d in crudo.values()),
                 crudo={k: {kk: vv for kk, vv in v.items()} for k, v in crudo.items()})
        m["E_mejor_exponente_h_alternativo"] = ext_eps(EhR_alt[0.1], EhR_alt[0.05], p_ext)
        # sesgo de Trotter medido contra el radial con la pared corrida a R + BETA sqrt(eps) (diagnostico de la Fase 3)
        if metodo == "a":
            sp = {e: EhR[e] - (ref["E0"] + pared[e]) for e in EPSS}
            m["sesgo_sin_pared"] = {str(k): v for k, v in sp.items()}
            dd = abs(sp[0.1] - sp[0.05])
            m["orden_trotter_sin_pared"] = float(math.log2(abs(sp[0.2] - sp[0.1]) / dd)) if dd > 0 else float("nan")
        if delta == 0.0:
            m["dif_exacto"] = Eb + 0.125
        caso["metodos"][metodo] = m
        print(f"delta = {delta:<6} R = {R:.0f} metodo ({metodo}): E = {Eb:+.10e} +- {err:.1e}  radial {ref['E0']:+.10e}  "
              f"dif = {Eb - ref['E0']:+.1e}  compatible = {m['compatible']}  pTrot = {p_trot:.3f}  "
              f"sesgo(eps=0.1)/|E| = {m['sesgo_eps01_rel']:+.1e}  <r> dif = {m['dif_r']:+.1e}  perron = {m['perron_min']:+.1e} "
              f"minT = {m['min_T']:.1e}" + (f"  pTrot(pared corrida) = {m['orden_trotter_sin_pared']:.3f}" if metodo == "a" else ""),
              flush=True)
    caso["t"] = time.time() - t
    out["casos"].append(caso)
    c.guardar_json("45_transferencia_l1", out)

ca = [cs["metodos"]["a"] for cs in out["casos"]]
out["resumen_a"] = dict(
    todos_compatibles=bool(all(m["compatible"] for m in ca)),
    coulomb_dif=out["casos"][0]["metodos"]["a"]["dif_exacto"],
    trotter=[m["orden_trotter"] for m in ca],
    max_dif_rel=max(abs(m["dif_radial"]) / abs(cs["radial"]["E0"]) for m, cs in zip(ca, out["casos"])),
    perron_min=min(m["perron_min"] for m in ca), min_T=min(m["min_T"] for m in ca))
cb = [cs["metodos"]["b"] for cs in out["casos"]]
out["resumen_b"] = dict(trotter=[m["orden_trotter"] for m in cb],
                        sesgo_eps01_rel=[m["sesgo_eps01_rel"] for m in cb],
                        max_dif_rel=max(abs(m["dif_radial"]) / abs(cs["radial"]["E0"]) for m, cs in zip(cb, out["casos"])))
out["t_total"] = time.time() - T0
c.guardar_json("45_transferencia_l1", out)
print("\nResumen (a):", {k: v for k, v in out["resumen_a"].items()})
print("Resumen (b):", out["resumen_b"])
print(f"Tiempo total {out['t_total']:.0f} s")
