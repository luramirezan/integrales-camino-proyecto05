"""05_transferencia_ecsc.py -- E3: integral de camino (matriz de transferencia con la accion de pares de Coulomb)
para el ECSC, comparada con el disparo en la misma caja y con el radial de la Fase 2.

Por que la accion de pares de Coulomb sigue siendo exacta en el origen para el ECSC:
  V_ECSC = -e^{-x} cos(x)/r (x = delta r) = -1/r + W(r), con W = (1 - e^{-x} cos x)/r = delta (1 - x^2/3 + x^3/6 - ...):
  W es una funcion entera de r (el cociente de una funcion entera que se anula en r = 0 entre r), acotada y positiva
  (1 - e^{-x} cos x >= 1 - e^{-x} > 0 para x > 0). Toda la singularidad esta en el -1/r, que la accion de pares
  U_C trata de forma exacta; W entra con la regla del punto medio simetrica, error O(eps^2) igual que en Yukawa.
  Los elementos de T son h K_D e^{-U_C} e^{-eps (W_i + W_j)/2} > 0: el peso es real, positivo y normalizable.

Receta (identica a fase3/codigo/comun3.celda, decisiones 1 y 5 de la Fase 2):
  h in {0.02, 0.04} (Richardson h^4), eps in {0.2, 0.1, 0.05} (ley eps^2), error = |E_ext(h=0.02) - E_ext(hR)| +
  |E_ext(0.1,0.05) - E_ext(0.2,0.1)| + |sesgo de pared extrapolado|. Unica diferencia: el sesgo de pared se estima con
  el DISPARO en R + BETA sqrt(eps) (sin malla) en lugar del radial h = 1/40 (para Yukawa los dos dan lo mismo).
Casos: ECSC delta in {0.3, 0.5, 0.65, 0.70, 0.715} con R = max(60, 25/kappa) redondeado (0.715: R = 1200, ver abajo);
  controles: Hulthen delta = 1.8 (exacto -0.005), atomo H estatico delta = 1.6, y Yukawa delta = 1.18, R = 200 (debe
  reproducir la celda de la Fase 3, -2.4076630903e-5, en la misma (h, eps) con comun3.resolver_tr).
  Para 0.715, 25/kappa = 1870 y se usa R = 1200 por costo (R kappa = 16): el sesgo de pared entra en la barra.

Criterios fijados ANTES de correr:
  T1 W_ECSC en (0, delta] y finito en r in [1e-8, 400] (los cinco delta)
  T2 |E_tr - E_disparo(R)| <= 2 (err_tr + err_ref) + 1e-12 en todas las celdas (err_ref = 0 para el disparo, se usa
     el mismo criterio de la Fase 3 con el radial: |E_tr - E_rad| <= 2 (err + err_rad))
  T3 orden de Trotter aparente en [1.8, 2.2] (informativo cuando la densidad toca la pared)
  T4 Perron: min(v)/max|v| > -1e-10 y residuo < 1e-8 en todas las corridas
  T5 Hulthen delta = 1.8: |E_tr - (-0.005)| <= 2 err_tr + 1e-12
  T6 Yukawa 1.18, R = 200, h = 0.04, eps = 0.1: |E (este script) - E (comun3.resolver_tr)| < 1e-13
"""
import sys
import time

import numpy as np
from scipy.sparse.linalg import eigsh

import comun_e3 as C
import perfiles as P

sys.path.insert(0, C.F3)
import comun3 as c3          # noqa: E402  (importa pares, radial y transferencia de la Fase 2)
tr, radial = c3.tr, c3.radial

CRIT = {
    "T1": "W_ECSC en (0, delta] y finito en [1e-8, 400]",
    "T2": "|E_tr - E_disparo(R)| <= 2 err_tr + 1e-12 (y frente al radial: <= 2(err + err_rad))",
    "T3": "orden de Trotter en [1.8, 2.2] (informativo si toca la pared)",
    "T4": "Perron min(v)/max|v| > -1e-10 y residuo < 1e-8",
    "T5": "Hulthen 1.8: |E_tr + 0.005| <= 2 err_tr + 1e-12",
    "T6": "Yukawa 1.18 R=200 (h 0.04, eps 0.1): |E - E_comun3| < 1e-13",
}
CASOS = [("ecsc", 0.3, None), ("ecsc", 0.5, None), ("ecsc", 0.65, None), ("ecsc", 0.70, None), ("ecsc", 0.715, 1200.0),
         ("hulthen", 1.8, None), ("hatomo", 1.6, None), ("yukawa", 1.18, 200.0)]


def resolver(perfil, d, R, h, eps, Eg):
    t = time.perf_counter()
    T, r = tr.matriz_T(R, h, eps, W=P.PERFILES[perfil]["W"](d), tabla=c3.tabla(eps))
    sigma = float(np.exp(-eps * (Eg - 2e-4)))
    lam, v = eigsh(T, k=2, sigma=sigma, which="LM", tol=0)
    o = np.argsort(lam)[::-1]
    lam, v = lam[o], v[:, o]
    v0 = v[:, 0] * np.sign(v[:, 0].sum())
    ob = tr._observables(r, v0, R)
    return dict(E0=float(-np.log(lam[0]) / eps), E1=float(-np.log(lam[1]) / eps),
                perron_min=float(v0.min() / np.abs(v0).max()),
                residuo=float(np.linalg.norm(T @ v0 - lam[0] * v0) / np.linalg.norm(v0)),
                r_med=ob["r_med"], r_sobre_R=ob["r_sobre_R"], N=len(r), t=time.perf_counter() - t)


def celda(perfil, d, R, T_):
    Eref = P.caja(perfil, d, R)
    rad = radial.resolver_rich(P.PERFILES[perfil]["V"](d), R, h=1 / 40, nev=1)
    err_rad = abs(rad["E0_h"] - rad["E0_h2"])
    crudo, Eg = {}, Eref
    for h in c3.HS:
        for e in c3.EPSS:
            x = resolver(perfil, d, R, h, e, Eg)
            Eg = x["E0"]
            crudo[f"h{h:g}_eps{e:g}"] = x
    E = {(h, e): crudo[f"h{h:g}_eps{e:g}"]["E0"] for h in c3.HS for e in c3.EPSS}
    EhR = {e: (16 * E[(0.02, e)] - E[(0.04, e)]) / 15 for e in c3.EPSS}
    Eb = c3.ext_eps(EhR[0.1], EhR[0.05])
    Eg_ = c3.ext_eps(EhR[0.2], EhR[0.1])
    Eh = c3.ext_eps(E[(0.02, 0.1)], E[(0.02, 0.05)])
    p_trot = float(np.log2(abs(EhR[0.2] - EhR[0.1]) / abs(EhR[0.1] - EhR[0.05])))
    pared = {e: P.caja(perfil, d, R + c3.BETA * np.sqrt(e)) - Eref for e in c3.EPSS}
    pared_ext = float(c3.ext_eps(pared[0.1], pared[0.05]))
    err = abs(Eh - Eb) + abs(Eb - Eg_) + abs(pared_ext)
    out = dict(perfil=perfil, delta=d, R=R, E_tr=float(Eb), err_tr=float(err), E_disparo=Eref, E_radial=rad["E0"],
               err_radial=err_rad, dif_disparo=float(Eb - Eref), dif_radial=float(Eb - rad["E0"]),
               orden_trotter=p_trot, sesgo_pared=pared_ext, crudo=crudo,
               perron_min=min(x["perron_min"] for x in crudo.values()), residuo_max=max(x["residuo"] for x in crudo.values()),
               r_med_tr=crudo["h0.02_eps0.05"]["r_med"], t=sum(x["t"] for x in crudo.values()))
    T_(f"{perfil:8s} d={d:<6} R={R:<7.0f} E_tr={Eb:+.10e} +- {err:.1e}  disparo={Eref:+.10e} (dif {Eb-Eref:+.1e})  "
       f"radial={rad['E0']:+.10e} (+-{err_rad:.0e})  pTrot={p_trot:.3f} pared={pared_ext:+.1e} perron={out['perron_min']:+.0e} "
       f"t={out['t']:.0f}s")
    return out


def main():
    T_ = C.Tee("05_transferencia_ecsc")
    out = dict(script="05_transferencia_ecsc.py", criterios=CRIT, celdas=[])
    ok = {k: True for k in CRIT}
    rr = np.geomspace(1e-8, 400, 200001)
    Wchk = {}
    for (_, d, _) in [c for c in CASOS if c[0] == "ecsc"]:
        W = P.PERFILES["ecsc"]["W"](d)(rr)
        Wchk[str(d)] = dict(min=float(W.min()), max=float(W.max()))
        ok["T1"] &= bool(np.all(np.isfinite(W)) and W.min() > 0 and W.max() <= d * (1 + 1e-14))
    out["W_ecsc"] = Wchk
    T_("W_ECSC (min, max) en [1e-8, 400]:", Wchk)
    for perfil, d, Rfix in CASOS:
        if Rfix is None:
            kap = P.ligado(perfil, d, observables=False)["kappa"]
            R = float(np.ceil(max(60.0, 25.0 / kap)))
        else:
            R = Rfix
        c = celda(perfil, d, R, T_)
        ok["T2"] &= bool(abs(c["dif_disparo"]) <= 2 * c["err_tr"] + 1e-12 and
                         abs(c["dif_radial"]) <= 2 * (c["err_tr"] + c["err_radial"]))
        ok["T3"] &= bool(1.8 <= c["orden_trotter"] <= 2.2)
        ok["T4"] &= bool(c["perron_min"] > -1e-10 and c["residuo_max"] < 1e-8)
        if perfil == "hulthen":
            c["E_exacta"] = -0.5 * (1 - d / 2)**2
            ok["T5"] = bool(abs(c["E_tr"] - c["E_exacta"]) <= 2 * c["err_tr"] + 1e-12)
        if perfil == "yukawa":
            ref = c3.resolver_tr(d, R, 0.04, 0.1, c["E_disparo"])
            c["E_comun3_h004_eps01"] = ref["E0"]
            ok["T6"] = bool(abs(ref["E0"] - c["crudo"]["h0.04_eps0.1"]["E0"]) < 1e-13)
            T_(f"   T6: comun3.resolver_tr = {ref['E0']:+.13e}, este script = {c['crudo']['h0.04_eps0.1']['E0']:+.13e}")
        out["celdas"].append(c)
        C.guardar("05_transferencia_ecsc", out)
    out["pasa"] = ok
    T_("controles:", ok)
    C.guardar("05_transferencia_ecsc", out)
    T_.cerrar()


if __name__ == "__main__":
    main()
