"""02_dispersion.py -- E3: longitud de dispersion a(delta) y rango efectivo r_e(delta) a ambos lados del umbral.

Convencion del grupo: u ~ r - a fuera del alcance; a > 0 cuando hay ligado. Desarrollo de rango efectivo:
    k cot delta_0 = -1/a + (r_e/2) k^2 + O(k^4).
Metodo 1 (energia cero, Bethe 1949): 1/a de la solucion de E = 0 y r_e = 2 int_0^inf [psi^2 - phi^2] dr, con
  psi = 1 - r/a y phi = u/alfa normalizada a phi -> 1 - r/a.
Metodo 2 (desfasajes): k cot delta_0 en k = (0.02..0.10) delta (8 valores) y ajuste en k^2 de grado 3;
  la ordenada es -1/a y la pendiente r_e/2.
Pendiente c = -d(1/a)/d delta en delta_c por tres caminos:
  (i) integral de Hellmann-Feynman c_HF = 2 int (dV/d delta) phi^2 dr (identidad del wronskiano), en delta_c;
  (ii) diferencias centradas de 1/a con paso 1e-3 delta_c y 2e-3 delta_c, combinadas con Richardson (h^2);
  y la segunda derivada d2 = (1/2) d^2(1/a)/d delta^2 (para predecir el termino B Delta^2 de kappa).
Hulthen: a exacto (funcion digamma) a = (1/delta) [2 gamma + psi(1 + sqrt(2/delta)) + psi(1 - sqrt(2/delta))].

Criterios fijados ANTES de correr:
  S1 |1/a(metodo 1) - 1/a(metodo 2)| < 1e-9 y |r_e(1) - r_e(2)| < 1e-5 en los puntos comparados
  (Tras correr: S1 no pasa por la truncacion del polinomio en k^2 con k hasta 0.1 delta: la ordenada se
   desvia ~1e-9. Se anade S1b, mismo criterio con k = (0.005..0.05) delta y grado 4, como variante POSTERIOR.)
  S2 Hulthen: |a - a_exacto|/|a_exacto| < 1e-9 en todos los delta de la rejilla con |a| < 1e6
  S3 |c_HF - c_dif|/c < 1e-7
  S4 informativo: c de Yukawa frente a A = 0.7411 de la Fase 3 (ajuste con 4 cifras)
  S5 1/a cambia de signo en delta_c y solo ahi en la rejilla (monotona decreciente en delta)
"""
import numpy as np
from scipy.special import digamma

import comun_e3 as C
import perfiles as P

CRIT = {
    "S1": "|1/a_1 - 1/a_2| < 1e-9 y |r_e1 - r_e2| < 1e-5 (energia cero frente a desfasajes)",
    "S1b": "(posterior) igual que S1 con k = (0.005..0.05) delta y grado 4",
    "S2": "Hulthen: |a - a_exacto|/|a_exacto| < 1e-9 (|a| < 1e6)",
    "S3": "|c_HF - c_dif|/c < 1e-7",
    "S4": "informativo: c(Yukawa) frente a A = 0.7411 (Fase 3)",
    "S5": "1/a monotona decreciente en delta y con un solo cambio de signo, en delta_c",
}
REL = np.concatenate([-np.geomspace(0.1, 1e-4, 13), [0.0], np.geomspace(1e-4, 0.1, 13)])   # (delta - delta_c)/delta_c
COMP = [-0.05, -0.01, 0.0, 0.01, 0.05]     # puntos donde se comparan los dos metodos


def a_hulthen(d):
    x = np.sqrt(2.0 / d)
    return (2 * np.euler_gamma + digamma(1 + x) + digamma(1 - x)) / d


def main():
    T = C.Tee("02_dispersion")
    U = C.cargar("01_umbrales")["perfiles"]
    out = dict(script="02_dispersion.py", criterios=CRIT, perfiles={})
    ok = dict(S1=True, S2=True, S3=True, S5=True)
    for k in C.ORDEN:
        dc = U[k]["delta_A"]
        rej = []
        for s in REL:
            d = dc * (1 + s)
            z = P.cero(k, d)
            rej.append(dict(rel=float(s), delta=float(d), inv_a=z["inv_a"], r_e=z["r_e"], c_HF=z["c_HF"]))
        ia = np.array([x["inv_a"] for x in rej])
        mono = bool(np.all(np.diff(ia) < 0))
        cambios = int(np.sum(np.sign(ia[1:]) != np.sign(ia[:-1])))
        # cambio de signo entre los dos puntos alrededor de rel = 0 (en rel = 0, 1/a es ~1e-13: se excluye)
        sin0 = [x for x in rej if x["rel"] != 0.0]
        ia0 = np.array([x["inv_a"] for x in sin0])
        cambios0 = int(np.sum(np.sign(ia0[1:]) != np.sign(ia0[:-1])))
        ok["S5"] &= bool(mono and cambios0 == 1)
        # comparacion con desfasajes
        comp = []
        for s in COMP:
            d = dc * (1 + s)
            z = P.cero(k, d)
            ks = d * np.linspace(0.02, 0.10, 8)
            kc = np.array([P.kcot(k, d, kk) for kk in ks])
            co = np.polyfit(ks**2, kc, 3)
            # S1b, AGREGADO DESPUES de ver que S1 no pasa: k = (0.005..0.05) delta (10 valores), grado 4.
            ks_b = d * np.linspace(0.005, 0.05, 10)
            kc_b = np.array([P.kcot(k, d, kk) for kk in ks_b])
            cb = np.polyfit(ks_b**2, kc_b, 4)
            ok["S1b"] = ok.get("S1b", True) and bool(abs(z["inv_a"] + cb[-1]) < 1e-9 and abs(z["r_e"] - 2 * cb[-2]) < 1e-5)
            comp.append(dict(rel=s, delta=float(d), inv_a_1=z["inv_a"], r_e_1=z["r_e"], inv_a_2=float(-co[-1]),
                             inv_a_2b=float(-cb[-1]), r_e_2b=float(2 * cb[-2]),
                             r_e_2=float(2 * co[-2]), forma_P=float(co[-3]), resid=float(np.max(np.abs(np.polyval(co, ks**2) - kc)))))
            ok["S1"] &= bool(abs(z["inv_a"] + co[-1]) < 1e-9 and abs(z["r_e"] - 2 * co[-2]) < 1e-5)
            T(f"{k:8s} rel={s:+.2f} 1/a: {z['inv_a']:+.12e} vs {-co[-1]:+.12e}   r_e: {z['r_e']:.9f} vs {2*co[-2]:.9f}  P={co[-3]:+.4f} | S1b: {-cb[-1]-z['inv_a']:+.1e} {2*cb[-2]-z['r_e']:+.1e}")
        # pendiente en delta_c
        z0 = P.cero(k, dc)
        hs = [1e-3 * dc, 2e-3 * dc]
        der, der2 = [], []
        for h in hs:
            ip, im = P.inv_a(k, dc + h), P.inv_a(k, dc - h)
            der.append(-(ip - im) / (2 * h))
            der2.append((ip - 2 * P.inv_a(k, dc) + im) / h**2)
        c_dif = (4 * der[0] - der[1]) / 3
        d2 = 0.5 * (4 * der2[0] - der2[1]) / 3
        ok["S3"] &= bool(abs(z0["c_HF"] - c_dif) / z0["c_HF"] < 1e-7)
        # prediccion del termino cuadratico de kappa: kappa = c D + (d2 + r_e c^2/2) D^2,  D = delta_c - delta
        # (1/a = c D + d2 D^2 con D = dc - d: d2 = (1/2) d^2(1/a)/d delta^2)
        B_pred = d2 + 0.5 * z0["r_e"] * z0["c_HF"]**2
        rec = dict(delta_c=dc, rejilla=rej, comparacion=comp, c_HF=z0["c_HF"], c_dif=float(c_dif),
                   d2=float(d2), r_e_c=z0["r_e"], B_pred=float(B_pred), monotona=mono, cambios_signo=cambios0)
        if k == "hulthen":
            errs = []
            for x in rej:
                if x["rel"] == 0.0:
                    continue
                ae = a_hulthen(x["delta"])
                if abs(ae) < 1e6:
                    errs.append(abs(1 / x["inv_a"] - ae) / abs(ae))
            rec["err_rel_a_exacto_max"] = float(max(errs))
            ok["S2"] = bool(max(errs) < 1e-9)
            T(f"hulthen: max |a - a_exacto|/|a| = {max(errs):.2e}")
        if k == "yukawa":
            rec["dif_A_fase3"] = float(z0["c_HF"] - C.A_FASE3)
        out["perfiles"][k] = rec
        T(f"{k:8s} delta_c={dc:.12f} c_HF={z0['c_HF']:.10f} c_dif={c_dif:.10f} d2={d2:+.6f} r_e(dc)={z0['r_e']:+.9f} "
          f"B_pred={B_pred:+.6f} monotona={mono} cambios={cambios0}")
    # dato fisico: el perfil "atomo H" en delta = 2 es el potencial estatico e-H(1s) en unidades atomicas
    zH = P.cero("hatomo", 2.0)
    out["hatomo_delta2_eH_estatico"] = dict(a=zH["a"], r_e=zH["r_e"])
    T(f"atomo H estatico en delta = 2 (e-H estatico, u.a.): a = {zH['a']:+.6f}, r_e = {zH['r_e']:.6f}")
    out["pasa"] = ok
    T("controles:", ok)
    C.guardar("02_dispersion", out)
    T.cerrar()


if __name__ == "__main__":
    main()
