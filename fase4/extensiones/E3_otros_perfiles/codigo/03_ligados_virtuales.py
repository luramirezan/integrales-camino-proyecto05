"""03_ligados_virtuales.py -- E3: estado ligado del lado ligado (delta < delta_c) y polo virtual del otro lado.

Lado ligado, D = delta_c - delta = delta_c * s, s en geomspace(1e-5, 0.1, 16):
  kappa por disparo con empalme a e^{-kappa r} (sin malla, sin caja), <r> y <r^2> con la cola analitica.
  Se compara kappa con (a) el orden dominante 1/a; (b) la formula de rango efectivo
  kappa_ERE = (1 - sqrt(1 - 2 r_e/a))/r_e con a(delta) y r_e(delta) del mismo delta (script 02, recalculados);
  (c) c D y c D + B_pred D^2 con c, B_pred de 02.
  Pendiente medida: ajuste kappa = A D + B D^2 + C3 D^3 con s <= 0.01 (puntos s >= 1e-4), A frente a c.
  Universalidad: kappa a -> 1, <r> kappa -> 1/2 y la correccion <r> kappa = (1/2)(1 + r_e kappa) + O(kappa^2)
  (se deduce de la normalizacion asintotica A_s^2 = 2 kappa/(1 - kappa r_e)); se mide la pendiente de
  <r> kappa frente a kappa con s <= 1e-3 y se compara con r_e/2.
Lado no ligado (delta > delta_c): polo virtual k = -i kappa_v. Directo: raiz de u'(rf) - kappa u(rf) = 0 (la
  solucion es pura e^{+kappa r}, sin componente e^{-kappa r}); valido porque kappa_v << delta/2 (el potencial
  decae como e^{-delta r}). Prediccion ERE: kappa_v = (-1 + sqrt(1 - 2 r_e/a))/r_e (a < 0). E_virtual = -kappa_v^2/2
  en la segunda hoja.

Criterios fijados ANTES de correr:
  L1 |kappa_ERE - kappa|/kappa < 1e-4 para s <= 0.01 (cuatro perfiles)
  L2 |A - c|/c < 1e-5 (A del ajuste, c de la solucion de energia cero)
  L3 en s = 1e-5: |kappa a - 1| < 1e-3 y |<r> kappa - 1/2| < 1e-3
  L4 pendiente de <r> kappa frente a kappa (s <= 1e-3) frente a r_e/2: diferencia relativa < 2e-2
  L5 polo virtual: |kappa_v(ERE) - kappa_v(directo)|/kappa_v < 1e-4 para s <= 0.01
  L6 todos los ligados sin nodos y con una sola raiz (un solo ligado s en la rejilla)
"""
import numpy as np
from scipy.optimize import brentq

import comun_e3 as C
import perfiles as P

CRIT = {
    "L1": "|kappa_ERE - kappa|/kappa < 1e-4 para s <= 0.01",
    "L2": "|A - c|/c < 1e-5",
    "L3": "s = 1e-5: |kappa a - 1| < 1e-3 y |<r> kappa - 1/2| < 1e-3",
    "L4": "pendiente d(<r>kappa)/dkappa (s <= 1e-3) frente a r_e/2: diferencia relativa < 2e-2",
    "L5": "|kappa_v(ERE) - kappa_v(directo)|/kappa_v < 1e-4 para s <= 0.01",
    "L6": "ligados sin nodos y una sola raiz",
}
SS = np.geomspace(1e-5, 0.1, 16)


def virtual(perfil, d, guess):
    rf = P.rmax(d)
    p = P.PERFILES[perfil]

    def g(k):
        s = P._integrar(p["V"](d), p["W0"](d), -0.5 * k * k, rf)
        u, up = s.y[0, -1], s.y[1, -1]
        return (up - k * u) / np.hypot(u, up)
    ks = np.geomspace(guess / 2, guess * 2, 30)
    v = [g(k) for k in ks]
    for i in range(len(ks) - 1):
        if np.sign(v[i]) != np.sign(v[i + 1]):
            return float(brentq(g, ks[i], ks[i + 1], xtol=1e-16, rtol=1e-15)), float(ks[-1] * rf)
    return None, None


def main():
    T = C.Tee("03_ligados_virtuales")
    D2 = C.cargar("02_dispersion")["perfiles"]
    out = dict(script="03_ligados_virtuales.py", criterios=CRIT, perfiles={})
    ok = {k: True for k in CRIT}
    for k in C.ORDEN:
        dc, c, Bp = D2[k]["delta_c"], D2[k]["c_HF"], D2[k]["B_pred"]
        lig = []
        for s in SS:
            d = dc * (1 - s)
            L = P.ligado(k, d)
            z = P.cero(k, d)
            a, re = z["a"], z["r_e"]
            kE = (1 - np.sqrt(1 - 2 * re / a)) / re
            D = dc - d
            lig.append(dict(s=float(s), delta=float(d), D=float(D), kappa=L["kappa"], r_med=L["r_med"], r2_med=L["r2_med"],
                            nodos=L["nodos"], n_raices=len(L["raices"]), frac_cola=L["frac_cola"], a=a, r_e=re,
                            kappa_ERE=float(kE), kappa_lead=float(1 / a), kappa_cD=float(c * D), kappa_cDB=float(c * D + Bp * D * D),
                            kappa_a=float(L["kappa"] * a), rk=float(L["r_med"] * L["kappa"])))
            ok["L6"] &= bool(L["nodos"] == 0 and len(L["raices"]) == 1)
            if s <= 0.01:
                ok["L1"] &= bool(abs(kE - L["kappa"]) / L["kappa"] < 1e-4)
        # ajuste de la pendiente
        sel = [x for x in lig if 1e-4 <= x["s"] <= 0.01]
        Dv = np.array([x["D"] for x in sel]); kv = np.array([x["kappa"] for x in sel])
        M = np.vstack([Dv, Dv**2, Dv**3]).T
        A, B, C3 = np.linalg.lstsq(M, kv, rcond=None)[0]
        ok["L2"] &= bool(abs(A - c) / c < 1e-5)
        l0 = lig[0]
        ok["L3"] &= bool(abs(l0["kappa_a"] - 1) < 1e-3 and abs(l0["rk"] - 0.5) < 1e-3)
        sel2 = [x for x in lig if x["s"] <= 1.01e-3]
        kk = np.array([x["kappa"] for x in sel2]); rk = np.array([x["rk"] for x in sel2])
        cof = np.polyfit(kk, rk, 2)
        pend = float(cof[1]); ord0 = float(cof[2])
        re_c = D2[k]["r_e_c"]
        ok["L4"] &= bool(abs(pend - re_c / 2) / abs(re_c / 2) < 2e-2)
        # lado virtual
        vir = []
        for s in SS:
            d = dc * (1 + s)
            z = P.cero(k, d)
            a, re = z["a"], z["r_e"]
            kvE = (-1 + np.sqrt(1 - 2 * re / a)) / re
            kvD, krf = virtual(k, d, -1 / a)
            rec = dict(s=float(s), delta=float(d), a=a, r_e=re, kappa_v_ERE=float(kvE), kappa_v_dir=kvD,
                       kappa_v_lead=float(-1 / a), E_virtual=float(-0.5 * kvD**2) if kvD else None,
                       kappa_v_sobre_delta=float(kvD / d) if kvD else None)
            vir.append(rec)
            if s <= 0.01:
                ok["L5"] &= bool(kvD is not None and abs(kvE - kvD) / kvD < 1e-4)
        out["perfiles"][k] = dict(delta_c=dc, c=c, B_pred=Bp, r_e_c=re_c, ligados=lig, ajuste=dict(A=float(A), B=float(B), C3=float(C3),
                                  dif_rel_A_c=float((A - c) / c), puntos=len(sel)),
                                  rk_ajuste=dict(ordenada=ord0, pendiente=pend, r_e_sobre_2=re_c / 2,
                                                 dif_rel=float((pend - re_c / 2) / (re_c / 2))), virtuales=vir)
        T(f"\n== {k}: delta_c={dc:.12f} c={c:.10f} B_pred={Bp:+.5f} r_e(dc)={re_c:+.6f}")
        T(f"   ajuste kappa = A D + B D^2 + C D^3 (1e-4 <= s <= 0.01): A={A:.10f} (A-c)/c={(A-c)/c:+.1e} B={B:+.5f} C={C3:+.3f}")
        T(f"   <r>kappa = {ord0:.6f} + {pend:+.5f} kappa + ... ; r_e/2 = {re_c/2:+.5f} (dif rel {(pend - re_c/2)/(re_c/2):+.1e})")
        T("   s        kappa          (kERE-k)/k  (1/a-k)/k   (cD-k)/k   kappa*a    <r>kappa   cola")
        for x in lig:
            T(f"   {x['s']:.1e}  {x['kappa']:.6e}  {(x['kappa_ERE']-x['kappa'])/x['kappa']:+.1e}  "
              f"{(x['kappa_lead']-x['kappa'])/x['kappa']:+.1e}  {(x['kappa_cD']-x['kappa'])/x['kappa']:+.1e}  "
              f"{x['kappa_a']:.6f}  {x['rk']:.6f}  {x['frac_cola']:.4f}")
        T("   virtual: s       kappa_v(dir)     (ERE-dir)/dir  (1/|a|-dir)/dir  E_virtual")
        for x in vir:
            T(f"   {x['s']:.1e}  {x['kappa_v_dir']:.6e}  {(x['kappa_v_ERE']-x['kappa_v_dir'])/x['kappa_v_dir']:+.1e}  "
              f"{(x['kappa_v_lead']-x['kappa_v_dir'])/x['kappa_v_dir']:+.1e}  {x['E_virtual']:.4e}")
    out["pasa"] = ok
    T("controles:", ok)
    C.guardar("03_ligados_virtuales", out)
    T.cerrar()


if __name__ == "__main__":
    main()
