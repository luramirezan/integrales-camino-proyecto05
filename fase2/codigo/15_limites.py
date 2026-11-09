"""15_limites.py -- Proyecto 05 (Yukawa), Fase 2: limites fisicos L01-L19 (fase1/secciones/07_limites_fisicos.md)
comprobados con la INTEGRAL DE CAMINO (matriz de transferencia con la accion de pares de Coulomb), y comparados
con el solucionador radial. Respuesta al hallazgo H5 de V2 (L04, L05, L06 y L09 no se habian comprobado con la
integral de camino) y base de la tabla de controles de la seccion 15.

Unidades hbar = m = g = 1, V = -e^{-delta r}/r = -1/r + W, W = (1 - e^{-delta r})/r.
Metodo (aprobado, 9.3-9.4): T_ij = h K_D e^{-U_C} e^{-eps(W_i+W_j)/2}, tablas U_C con Richardson en h_tab
(pares.py), Nystrom h = 0.02 y 0.04 con Richardson h^4, eps = 0.2/0.1/0.05 con extrapolacion eps^2.
Determinista (sin numeros aleatorios; semilla 20262000 fijada solo por convencion).

Criterios (fijados ANTES de ejecutar este script, 27-10-2026):
  L03  serie: residuo E_ext - E_(4) en delta = 0.05 y 0.1; orden aparente log2(res(0.1)/res(0.05)) en [4.5, 5.5]
       y |res_tr - res_rad| < 1e-8 en los dos delta.
  L04  cotas: -1/2 <= E_ext <= -1/2 + delta en delta = 0.05, 0.1, 0.2, 0.5, 1.0.
  L05  Hellmann-Feynman (9.7): |dE/ddelta - <e^{-delta r}>| < 1e-4 con el autovector de la transferencia
       (delta = 0.2, 0.5, 1.0; eps = 0.1, h = 0.02; derivada centrada con +-0.005).
  L06  virial (9.7): residuo 2E - <V> - delta<e^{-delta r}> -> 0 al extrapolar h y eps: |res_ext| < 1e-5 (delta = 0.2).
  L07  cuspide: ajuste cubico de u/r en r <= 0.2 del autovector; |a2/a1 + 1| < 0.02 (delta = 0, 0.2, 1.0).
  L08  cola: r (d ln u/dr + kappa) en r = 10 y 20: Coulomb -> 1/kappa = 1 a 2e-2; delta = 0.5: |.| < 1e-2 en r = 20.
  L09  sin nodos: min(v)/max(v) >= -1e-10 (delta = 0, 0.2, 0.5, 1.0).
  L12  caja: E_ext(R) decreciente en R y >= E_ext(R = 174) en delta = 1.0, R = 10, 20, 40, 80.
  L14  2s: E1 de la transferencia (delta = 0.2, R = 161) a < 1e-6 del radial y negativo; delta = 0.35: E1 > 0 como el radial.
  L16  propagador libre: sum_j h K_D(r_i, r_j) = erf(r_i/sqrt(2 eps)) a 1e-10; K_D >= 0; K_D(0, r') = 0.
  L19  delta = 2: E_ext(R = 200) > 0 y a menos del 5 % de pi^2 / (2 (R - a_s)^2).
Salida: fase2/resultados/15_limites.json, fase2/figuras/15_limites.png.
"""
import json
import os
import sys
import time
import warnings

import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import erf
from scipy.sparse.linalg import eigsh

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import pares                      # noqa: E402
import transferencia as tr        # noqa: E402
import radial                     # noqa: E402

np.random.seed(20262000)
T0 = time.perf_counter()
BASE = os.path.dirname(AQUI)
RES = os.path.join(BASE, "resultados")
FIG = os.path.join(BASE, "figuras")
EPSS = (0.2, 0.1, 0.05)
TAB = {e: pares.tabla_richardson(e) for e in EPSS}
print(f"Carga (loadavg): {os.getloadavg()}")
out = dict(script="15_limites.py", fecha="2026-10-27", unidades="hbar=m=g=1",
           metodo="transferencia (accion de pares de Coulomb, tablas Richardson), h 0.02/0.04 Richardson h^4, "
                  "eps 0.2/0.1/0.05 extrapolacion eps^2", criterios=[])


def C(lim, nombre, valor, pasa, criterio):
    out["criterios"].append(dict(limite=lim, control=nombre, criterio=criterio, valor=valor,
                                 pasa=None if pasa is None else bool(pasa)))
    et = "MEDIDO" if pasa is None else ("PASA" if pasa else "NO PASA")
    print(f"  [{et}] {lim} {nombre}: {valor}  (criterio: {criterio})", flush=True)


def resolver(delta, R, h, eps, nev=1, E_guess=None):
    """Autovalores mayores de T (Lanczos con R <= 60; shift-invert con R grande) y autovector."""
    T, r = tr.matriz_T(R, h, eps, W=tr.W_yukawa(delta), tabla=TAB[eps])
    if R <= 60 or E_guess is None:
        lam, v = eigsh(T, k=nev, which="LA", tol=0)
    else:
        sigma = float(np.exp(-eps * (E_guess - 2e-4)))
        lam, v = eigsh(T, k=nev, sigma=sigma, which="LM", tol=0)
    o = np.argsort(lam)[::-1]
    lam, v = lam[o], v[:, o]
    v0 = v[:, 0] * np.sign(v[:, 0].sum())
    E = [float(-np.log(x) / eps) for x in lam]
    return dict(E=E, v=v0, r=r, T=T, sesgo_pared=tr.sesgo_pared(r, v0, h, eps))


def extrap(delta, R, E_guess=None, nev=1, k=0):
    """E_k extrapolado: Richardson h^4 (0.02, 0.04) y eps^2 con (0.1, 0.05); error = |ext - ext(0.2,0.1)| +
    |ext - ext sin Richardson en h|."""
    E = {}
    for h in (0.02, 0.04):
        for e in EPSS:
            E[(h, e)] = resolver(delta, R, h, e, nev=nev, E_guess=E_guess)["E"][k]
    EhR = {e: (16 * E[(0.02, e)] - E[(0.04, e)]) / 15 for e in EPSS}
    ext = EhR[0.05] + (EhR[0.05] - EhR[0.1]) / 3
    gru = EhR[0.1] + (EhR[0.1] - EhR[0.2]) / 3
    sin = E[(0.02, 0.05)] + (E[(0.02, 0.05)] - E[(0.02, 0.1)]) / 3
    return float(ext), float(abs(ext - gru) + abs(ext - sin)), {f"h{h:g}_eps{e:g}": x for (h, e), x in E.items()}


def E_rad(delta, R, h=1 / 80):
    return radial.resolver_rich(radial.V_yukawa(delta) if delta > 0 else radial.V_coulomb(), R, h=h)


# ============================================================ L03 y L04
print("=== L03 (serie) y L04 (cotas) ===")
serie = lambda d: -0.5 + d - 0.75 * d**2 + 0.5 * d**3 - 11.0 / 16.0 * d**4
L03 = {}
for d in (0.05, 0.1, 0.2, 0.5, 1.0):
    ext, err, crudo = extrap(d, 40.0 if d < 1.0 else 80.0)
    rr = E_rad(d, 40.0 if d < 1.0 else 80.0)["E0"]
    L03[f"{d:g}"] = dict(E_ext=ext, err=err, E_radial=rr, dif_radial=ext - rr, E_serie4=serie(d),
                         res_tr=ext - serie(d), res_rad=rr - serie(d), crudo=crudo)
    print(f"delta={d}: E_ext={ext:.11f} +- {err:.1e}  radial={rr:.11f}  dif={ext-rr:+.2e}  "
          f"residuo serie: tr {ext-serie(d):+.3e}, radial {rr-serie(d):+.3e}", flush=True)
p03 = float(np.log2(L03["0.1"]["res_tr"] / L03["0.05"]["res_tr"]))
p03r = float(np.log2(L03["0.1"]["res_rad"] / L03["0.05"]["res_rad"]))
out["L03"] = dict(por_delta=L03, orden_tr=p03, orden_rad=p03r)
dmax = max(abs(L03[k]["res_tr"] - L03[k]["res_rad"]) for k in ("0.05", "0.1"))
C("L03", "serie perturbativa", f"orden aparente {p03:.3f} (radial {p03r:.3f}); cociente res(0.1)/res(0.05) = "
  f"{2**p03:.2f}; max |res_tr - res_rad| = {dmax:.1e}", 4.5 <= p03 <= 5.5 and dmax < 1e-8,
  "orden en [4.5, 5.5] y |res_tr - res_rad| < 1e-8")
viol = [k for k, v in L03.items() if not (-0.5 <= v["E_ext"] <= -0.5 + float(k))]
marg = min(min(v["E_ext"] + 0.5, -0.5 + float(k) - v["E_ext"]) for k, v in L03.items())
out["L04"] = dict(violaciones=viol, margen_minimo=marg)
C("L04", "cotas -1/2 <= E0 <= -1/2 + delta", f"{len(viol)} violaciones en 5 delta; margen minimo {marg:.3e}",
  not viol, "0 violaciones")

# ============================================================ L05 Hellmann-Feynman
print("\n=== L05 Hellmann-Feynman (eps = 0.1, h = 0.02, R = 40/80) ===")
L05 = {}
for d in (0.2, 0.5, 1.0):
    R = 40.0 if d < 1.0 else 80.0
    o = resolver(d, R, 0.02, 0.1)
    u2 = o["v"]**2 / (o["v"]**2).sum()
    hf = float((u2 * np.exp(-d * o["r"])).sum())
    Ep = resolver(d + 0.005, R, 0.02, 0.1)["E"][0]
    Em = resolver(d - 0.005, R, 0.02, 0.1)["E"][0]
    dEdd = (Ep - Em) / 0.01
    # derivada con paso mitad (para ver el error O(dd^2) de la diferencia centrada)
    Ep2 = resolver(d + 0.0025, R, 0.02, 0.1)["E"][0]
    Em2 = resolver(d - 0.0025, R, 0.02, 0.1)["E"][0]
    dEdd2 = (Ep2 - Em2) / 0.005
    L05[f"{d:g}"] = dict(dE_ddelta=dEdd, dE_ddelta_paso_mitad=dEdd2, exp_media=hf, dif=dEdd - hf, dif_paso_mitad=dEdd2 - hf)
    print(f"delta={d}: dE/ddelta={dEdd:.9f} (paso mitad {dEdd2:.9f})  <e^(-delta r)>={hf:.9f}  dif={dEdd-hf:+.2e} "
          f"({dEdd2-hf:+.2e})", flush=True)
    C("L05", f"Hellmann-Feynman delta={d}", f"{dEdd:.8f} frente a {hf:.8f} (dif {dEdd-hf:+.1e})",
      abs(dEdd - hf) < 1e-4, "|dE/ddelta - <e^{-delta r}>| < 1e-4")
out["L05"] = L05

# ============================================================ L06 virial
print("\n=== L06 virial, delta = 0.2, R = 40: residuo 2E - <V> - delta <e^{-delta r}> ===")
d = 0.2
L06 = {}
for e in (0.1, 0.05):
    for h in (0.04, 0.02, 0.01):
        o = resolver(d, 40.0, h, e)
        u2 = o["v"]**2 / (o["v"]**2).sum()
        Vm = float((u2 * (-np.exp(-d * o["r"]) / o["r"])).sum())
        Xm = float((u2 * np.exp(-d * o["r"])).sum())
        L06[(e, h)] = dict(E=o["E"][0], V_media=Vm, exp_media=Xm, residuo=2 * o["E"][0] - Vm - d * Xm)
        print(f"  eps={e} h={h}: E={o['E'][0]:.10f} <V>={Vm:.8f} residuo={L06[(e, h)]['residuo']:+.3e}", flush=True)
vir = {}
for e in (0.1, 0.05):
    x = [L06[(e, h)]["residuo"] for h in (0.04, 0.02, 0.01)]
    p = float(np.log2(abs(x[0] - x[1]) / abs(x[1] - x[2])))
    vir[e] = dict(residuos_h=x, orden_h=p, rich_h=float(x[2] + (x[2] - x[1]) / (2**p - 1)))
res_ext = vir[0.05]["rich_h"] + (vir[0.05]["rich_h"] - vir[0.1]["rich_h"]) / 3
rv = radial.resolver_rich(radial.V_yukawa(d), 40.0, h=1 / 40)
rad_vir = {}
for hh in (1 / 40, 1 / 80):
    ob = radial.resolver(radial.V_yukawa(d), 40.0, h=hh, nev=1)
    u2 = ob["h"] * ob["u"]**2
    rad_vir[f"h=1/{round(1/hh)}"] = float(2 * ob["E0"] - (u2 * (-np.exp(-d * ob["r"]) / ob["r"])).sum()
                                          - d * (u2 * np.exp(-d * ob["r"])).sum())
out["L06"] = dict(por_eps_h={f"eps{e:g}_h{h:g}": v for (e, h), v in L06.items()},
                  extrapolacion_h={f"{e:g}": v for e, v in vir.items()}, residuo_extrapolado=float(res_ext),
                  radial_mismo_residuo=rad_vir)
print(f"  orden en h: eps=0.1 {vir[0.1]['orden_h']:.3f}, eps=0.05 {vir[0.05]['orden_h']:.3f}; extrapolado h->0, eps->0: "
      f"{res_ext:+.2e}; radial: {rad_vir}")
C("L06", "virial delta=0.2", f"h=0.02, eps=0.05: {L06[(0.05, 0.02)]['residuo']:+.2e}; h=0.01: "
  f"{L06[(0.05, 0.01)]['residuo']:+.2e} (orden en h {vir[0.05]['orden_h']:.2f}); extrapolado {res_ext:+.2e}",
  abs(res_ext) < 1e-5, "|residuo extrapolado en h y eps| < 1e-5")

# ============================================================ L07 cuspide, L08 cola, L09 nodos
print("\n=== L07 cuspide, L08 cola, L09 nodos (eps = 0.05, h = 0.02) ===")
L07, L08, L09 = {}, {}, {}
for d, R in ((0.0, 40.0), (0.2, 40.0), (0.5, 40.0), (1.0, 174.0)):
    Eg = E_rad(d, R, h=1 / 40)["E0"]
    o = resolver(d, R, 0.02, 0.05, E_guess=Eg)
    v, r = o["v"], o["r"]
    L09[f"{d:g}"] = float(v.min() / v.max())
    sel = r <= 0.2 + 1e-9
    a = np.polyfit(r[sel], v[sel] / r[sel], 3)[::-1]          # a0 + a1 r + ...
    L07[f"{d:g}"] = dict(a1=float(a[0]), a2=float(a[1]), cociente=float(a[1] / a[0]))
    kap = float(np.sqrt(-2 * o["E"][0]))
    lu = np.log(np.abs(v) + 1e-300)
    fila = {}
    for rc in (10.0, 20.0):
        i = int(round(rc / 0.02)) - 1
        dl = (lu[i + 1] - lu[i - 1]) / 0.04
        fila[f"r={rc:g}"] = float(rc * (dl + kap))
    L08[f"{d:g}"] = dict(kappa=kap, valores=fila, uno_sobre_kappa=1 / kap)
    print(f"delta={d}: cuspide a2/a1={a[1]/a[0]:+.5f}; cola r(dlnu/dr+kappa): {fila} (1/kappa={1/kap:.4f}); "
          f"min/max v = {v.min()/v.max():+.1e}", flush=True)
    if d != 0.5:
        C("L07", f"cuspide delta={d}", f"a2/a1 = {a[1]/a[0]:+.5f}", abs(a[1] / a[0] + 1) < 0.02, "|a2/a1 + 1| < 0.02")
    C("L09", f"sin nodos delta={d}", f"min/max = {v.min()/v.max():+.1e}", v.min() / v.max() >= -1e-10,
      "min(v)/max(v) >= -1e-10")
out["L07"], out["L08"], out["L09"] = L07, L08, L09
C("L08", "cola Coulomb", f"r(dlnu/dr+kappa) en r=10, 20: {L08['0']['valores']['r=10']:.4f}, "
  f"{L08['0']['valores']['r=20']:.4f} (1/kappa = {L08['0']['uno_sobre_kappa']:.4f})",
  abs(L08["0"]["valores"]["r=20"] - L08["0"]["uno_sobre_kappa"]) < 2e-2, "a 2e-2 de 1/kappa en r = 20")
C("L08", "cola delta=0.5 (sin factor r^{1/kappa})", f"{L08['0.5']['valores']['r=10']:.4f}, "
  f"{L08['0.5']['valores']['r=20']:.4f}", abs(L08["0.5"]["valores"]["r=20"]) < 1e-2, "|.| < 1e-2 en r = 20")

# ============================================================ L12 caja
print("\n=== L12 caja: delta = 1.0, R = 10, 20, 40, 80 (y R = 174 como referencia) ===")
L12 = {}
for R in (10.0, 20.0, 40.0, 80.0, 174.0):
    Eg = E_rad(1.0, R, h=1 / 40)["E0"]
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        ext, err, _ = extrap(1.0, R, E_guess=Eg)
    pr = resolver(1.0, R, 0.02, 0.05, E_guess=Eg)["sesgo_pared"]
    L12[f"R{R:g}"] = dict(E_ext=ext, err=err, E_radial=Eg, sesgo_pared_eps005=pr)
    print(f"R={R:g}: E_ext={ext:+.10e} +- {err:.1e}  radial={Eg:+.10e}  dif={ext-Eg:+.2e}  sesgo pared (eps=0.05) "
          f"{pr:+.1e}", flush=True)
Es = [L12[f"R{R:g}"]["E_ext"] for R in (10.0, 20.0, 40.0, 80.0, 174.0)]
dec = all(Es[i + 1] < Es[i] for i in range(len(Es) - 1))
sobre = all(x >= Es[-1] - 1e-12 for x in Es)
out["L12"] = dict(por_R=L12, decreciente=dec, mayor_que_R174=sobre)
C("L12", "caja delta=1.0", "E_ext(R) = " + ", ".join(f"{x:+.6e}" for x in Es) + f"; decreciente {dec}",
  dec and sobre, "decreciente en R y >= E(R=174)")

# ============================================================ L14 estado 2s
print("\n=== L14 estado 2s ===")
L14 = {}
for d, R in ((0.2, 161.0), (0.35, 161.0)):
    rr = E_rad(d, R, h=1 / 40)
    # shift-invert justo por encima de lambda0 (E_guess = E0): k = 2 devuelve E0 y E1. (En la primera ejecucion
    # se puso E_guess = E1 y eigsh devolvio E1 y E2: E1 salia mal; error del script, corregido.)
    E1, err1, _ = extrap(d, R, E_guess=rr["E0"], nev=2, k=1)
    L14[f"{d:g}"] = dict(R=R, E1_ext=E1, err=err1, E1_radial=rr["E1"], dif=E1 - rr["E1"])
    print(f"delta={d} R={R:g}: E1_ext={E1:+.10f} +- {err1:.1e}  radial={rr['E1']:+.10f}  dif={E1-rr['E1']:+.2e}", flush=True)
out["L14"] = L14
C("L14", "2s ligado delta=0.2", f"E1 = {L14['0.2']['E1_ext']:+.9f} (radial {L14['0.2']['E1_radial']:+.9f}, "
  f"dif {L14['0.2']['dif']:+.1e})", L14["0.2"]["E1_ext"] < 0 and abs(L14["0.2"]["dif"]) < 1e-6, "E1 < 0 y |dif| < 1e-6")
C("L14", "2s no ligado delta=0.35", f"E1 = {L14['0.35']['E1_ext']:+.3e} (radial {L14['0.35']['E1_radial']:+.3e})",
  L14["0.35"]["E1_ext"] > 0 and L14["0.35"]["E1_radial"] > 0, "E1 > 0, igual que el radial")

# ============================================================ L16 propagador libre
print("\n=== L16 propagador libre con imagen ===")
L16 = {}
for e in EPSS:
    h = 0.02
    r = h * np.arange(1, 2000)
    K = np.exp(pares.logKD(r[:, None], r[None, :], e))
    suma = h * K.sum(1)
    sel = r < 30
    d16 = float(np.abs(suma[sel] - erf(r[sel] / np.sqrt(2 * e))).max())
    K0 = float(np.exp(pares.logKD(1e-12, 1.0, e)))
    # misma suma con h = 0.01: el error del trapecio viene del extremo r' = 0 (K_D se anula alli con pendiente
    # finita ~1/eps), es O(h^2); se mide el orden (informativo, anadido tras la primera ejecucion)
    r1 = 0.01 * np.arange(1, 4000)
    s1 = 0.01 * np.exp(pares.logKD(r1[:, None], r1[None, :], e)).sum(1)
    d16b = float(np.abs(s1[r1 < 30] - erf(r1[r1 < 30] / np.sqrt(2 * e))).max())
    L16[f"{e:g}"] = dict(max_dif_erf=d16, max_dif_erf_h001=d16b, orden_h=float(np.log2(d16 / d16b)),
                         K_min=float(K.min()), K_en_0=K0)
    print(f"eps={e}: max|h sum K - erf| = {d16:.1e} (h=0.02), {d16b:.1e} (h=0.01), orden {np.log2(d16/d16b):.2f}; "
          f"min K = {K.min():.1e}; K(1e-12, 1) = {K0:.1e}")
out["L16"] = L16
C("L16", "propagador libre", "max |h sum_j K_D - erf| = " + ", ".join(f"{v['max_dif_erf']:.1e}" for v in L16.values()),
  all(v["max_dif_erf"] < 1e-10 and v["K_min"] >= 0 and v["K_en_0"] < 1e-10 for v in L16.values()),
  "a 1e-10; K_D >= 0; K_D(0, r') = 0")
C("L16", "propagador libre: orden del error de la suma (informativo)",
  "orden en h " + ", ".join(f"{v['orden_h']:.2f}" for v in L16.values()) + "; h=0.01: "
  + ", ".join(f"{v['max_dif_erf_h001']:.1e}" for v in L16.values()), None, "medido (error de extremo del trapecio)")

# ============================================================ L19 delta = 2
print("\n=== L19 delta = 2 (sin ligado) ===")


def long_dispersion(delta, Rf=80.0):
    f = lambda r, s: [s[1], -2.0 * np.exp(-delta * r) / r * s[0]]
    s = solve_ivp(f, [1e-10, Rf], [1e-10, 1.0], method="DOP853", rtol=1e-13, atol=1e-18)
    return float(Rf - s.y[0, -1] / s.y[1, -1])


a_s = long_dispersion(2.0)
L19 = dict(a_s=a_s)
for R in (100.0, 200.0):
    rr = E_rad(2.0, R, h=1 / 40)["E0"]
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        ext, err, _ = extrap(2.0, R, E_guess=rr)
    ley = np.pi**2 / (2 * (R - a_s)**2)
    L19[f"R{R:g}"] = dict(E_ext=ext, err=err, E_radial=rr, ley=ley, dev_ley=(ext - ley) / ley, dev_ley_radial=(rr - ley) / ley)
    print(f"R={R:g}: E_ext={ext:+.6e} radial={rr:+.6e} ley={ley:+.6e}; desviacion tr {(ext-ley)/ley:+.3e}, "
          f"radial {(rr-ley)/ley:+.3e}  (a_s = {a_s:.4f})", flush=True)
out["L19"] = L19
C("L19", "delta=2 sin ligado", f"E(R=200) = {L19['R200']['E_ext']:+.4e}; desviacion de la ley de caja "
  f"{L19['R200']['dev_ley']:+.2e} (radial {L19['R200']['dev_ley_radial']:+.2e})",
  L19["R200"]["E_ext"] > 0 and abs(L19["R200"]["dev_ley"]) < 0.05, "E > 0 y a < 5 % de pi^2/(2(R-a_s)^2)")

# ============================================================ resumen y json
crit = out["criterios"]
out["n_pasa"] = sum(1 for c in crit if c["pasa"] is True)
out["n_no_pasa"] = sum(1 for c in crit if c["pasa"] is False)
out["tiempo_total_s"] = time.perf_counter() - T0
print(f"\nCriterios: {out['n_pasa']} pasan, {out['n_no_pasa']} no pasan, de {len(crit)}.")
for c in crit:
    if c["pasa"] is False:
        print("  NO PASA:", c["limite"], c["control"], c["valor"])
with open(os.path.join(RES, "15_limites.json"), "w") as f:
    json.dump(out, f, indent=1, ensure_ascii=False, default=float)

# ============================================================ figura
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
fig, ax = plt.subplots(1, 3, figsize=(14, 4.3))
ds = np.array([0.05, 0.1, 0.2])
ax[0].loglog(ds, [abs(L03[f"{x:g}"]["res_tr"]) for x in ds], "o", ms=8, mfc="none", label="transferencia")
ax[0].loglog(ds, [abs(L03[f"{x:g}"]["res_rad"]) for x in ds], "-", label="radial")
ax[0].loglog(ds, abs(L03["0.1"]["res_rad"]) * (ds / 0.1)**5, ":", color="k", label=r"pendiente 5 ($\delta^5$)")
ax[0].set_xlabel(r"$\delta$"); ax[0].set_ylabel(r"$|E_0-E_{(4)}|$"); ax[0].set_title("L03: residuo de la serie")
ax[0].legend(fontsize=8)
hs = np.array([0.04, 0.02, 0.01])
for e, mk in ((0.1, "s"), (0.05, "o")):
    ax[1].loglog(hs, [abs(L06[(e, h)]["residuo"]) for h in hs], marker=mk, label=fr"transferencia $\epsilon={e}$")
ax[1].loglog(hs, abs(L06[(0.05, 0.02)]["residuo"]) * (hs / 0.02)**2, ":", color="k", label=r"pendiente 2 ($h^2$)")
ax[1].set_xlabel("paso de la malla $h$"); ax[1].set_ylabel(r"$|2E-\langle V\rangle-\delta\langle e^{-\delta r}\rangle|$")
ax[1].set_title(r"L06: virial, $\delta=0.2$"); ax[1].legend(fontsize=8)
for d, R in ((0.0, 40.0), (0.2, 40.0), (1.0, 174.0)):
    Eg = E_rad(d, R, h=1 / 40)["E0"]
    o = resolver(d, R, 0.02, 0.05, E_guess=Eg)
    sel = o["r"] <= 0.5
    y = o["v"][sel] / o["r"][sel]
    ax[2].plot(o["r"][sel], y / L07[f"{d:g}"]["a1"], label=fr"$\delta={d}$ (pendiente {L07[f'{d:g}']['cociente']:+.3f})")
xx = np.linspace(0, 0.5, 10)
ax[2].plot(xx, 1 - xx, "k:", label="$1-r$ (cúspide de Kato)")
ax[2].set_xlabel("$r$"); ax[2].set_ylabel(r"$u(r)/(r\,u'(0))$"); ax[2].set_title("L07: cúspide en el origen")
ax[2].legend(fontsize=8)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "15_limites.png"), dpi=150); plt.close(fig)
print(f"guardado; tiempo total {time.perf_counter()-T0:.1f} s; carga {os.getloadavg()}")
