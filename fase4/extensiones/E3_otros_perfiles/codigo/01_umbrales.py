"""01_umbrales.py -- E3: apantallamiento critico delta_c (1s) de cada perfil con dos metodos independientes.

Metodo A (energia cero): brentq sobre 1/a(delta) = 0, con 1/a de la solucion regular a E = 0 (u ~ alfa + beta r
  fuera del alcance, 1/a = -beta/alfa; continua a traves del umbral).
  Estabilidad: rf = 60/delta frente a 80/delta, y rtol del integrador 1e-13 frente a 1e-11.
Metodo B (energias de ligado, sin usar E = 0): kappa(delta) por disparo con empalme a e^{-kappa r} en
  delta_j = delta_A (1 - s_j), s_j = 0.002..0.03 (8 puntos); polinomio cubico kappa(delta) y su raiz.
  (Los puntos se eligen con delta_A solo para situarlos; la raiz sale del ajuste.)
Control exacto: Hulthen delta_c = 2 (E = -(1/2)(1 - delta/2)^2) y Yukawa contra la referencia de las Fases 1-3.

Criterios fijados ANTES de correr (17-11-2026):
  U1 |delta_A(rf 60) - delta_A(rf 80)| < 1e-11 y |delta_A(rtol 1e-13) - delta_A(rtol 1e-11)| < 1e-10
  U2 |delta_A - delta_B| < 1e-8 en los cuatro perfiles
  U3 Hulthen |delta_A - 2| < 1e-10; Yukawa |delta_A - 1.1906124210606| < 1e-10
  U4 Hulthen kappa del disparo frente a 1 - delta/2: |dif| < 1e-11 en los 8 puntos
  (Tras correr: U2 no pasa en el ECSC con el cubico hasta s = 0.03; se anade B2, cubico con s = 1e-4..2e-3,
   como variante POSTERIOR, sin cambiar U2.)
  U5 (informativo) ECSC frente a la literatura verificada (fuentes.md): se informa la diferencia
"""
import numpy as np

import comun_e3 as C
import perfiles as P

CRIT = {
    "U1": "estabilidad de delta_A: rf 60/d vs 80/d < 1e-11; rtol 1e-13 vs 1e-11 < 1e-10",
    "U2": "|delta_A - delta_B| < 1e-8 (cuatro perfiles)",
    "U3": "Hulthen |delta_A - 2| < 1e-10; Yukawa |delta_A - 1.1906124210606| < 1e-10",
    "U4": "Hulthen: |kappa_disparo - (1 - delta/2)| < 1e-11",
    "U5": "informativo: diferencia con la literatura",
}
S = [0.002, 0.003, 0.005, 0.0075, 0.01, 0.015, 0.02, 0.03]
LIT = {   # cifras impresas que se verificaron (ver fuentes.md); 'fuente' es la clave de fuentes.md
    "yukawa": [("Roy 2019 (arXiv:1904.11166), tabla I", 1.190610), ("Gomes, Chacham y Mohallem 1994 (citado por Roy)", 1.19061227),
               ("Fases 1-3 de este proyecto", 1.1906124210606)],
    "ecsc": [("Roy 2019 (arXiv:1904.11166), tabla I", 0.7205240), ("Singh y Varshni 1983 (citado por Roy)", 0.72052408),
             ("Nasser et al. 2011 (citado por Roy)", 0.72055425), ("Lam y Varshni 1972 (citado por Roy)", 0.7115)],
    "hulthen": [("Roy 2019 (arXiv:1904.11166), tabla I", 2.0), ("exacto", 2.0)],
    "hatomo": [],
}


def main():
    T = C.Tee("01_umbrales")
    out = dict(script="01_umbrales.py", criterios=CRIT, perfiles={})
    ok = {}
    for k in C.ORDEN:
        dA = P.delta_c(k)
        # estabilidad: rf mayor y rtol menos estricto
        a, b = P.PERFILES[k]["bracket"]
        from scipy.optimize import brentq
        dA_rf80 = brentq(lambda d: P.inv_a(k, d, rf=80.0 / d), a, b, xtol=1e-14, rtol=1e-15)
        P.RTOL = 1e-11
        dA_rt11 = brentq(lambda d: P.inv_a(k, d), a, b, xtol=1e-14, rtol=1e-15)
        P.RTOL = 1e-13
        # metodo B
        ds = np.array([dA * (1 - s) for s in S])
        kap = []
        for d in ds:
            L = P.ligado(k, d, observables=False)
            kap.append(L["kappa"])
        kap = np.array(kap)
        x = ds - dA                       # centrado solo para el condicionamiento del ajuste
        co = np.polyfit(x, kap, 3)
        raices = np.roots(co)
        reales = raices[np.abs(raices.imag) < 1e-12].real
        r0 = reales[np.argmin(np.abs(reales))]
        dB = float(dA + r0)
        resid = float(np.max(np.abs(np.polyval(co, x) - kap)))
        # ajuste con cuartico, para ver la sensibilidad del metodo B al grado
        co4 = np.polyfit(x, kap, 4)
        rr4 = np.roots(co4); rr4 = rr4[np.abs(rr4.imag) < 1e-12].real
        dB4 = float(dA + rr4[np.argmin(np.abs(rr4))])
        # B2: AGREGADO DESPUES de ver que U2 no pasa en el ECSC (17-11-2026): cubico con puntos mas cerca del
        # umbral, s = 1e-4..2e-3 (5 puntos nuevos). Variante posterior: no cambia el veredicto de U2.
        S2 = [1e-4, 2e-4, 5e-4, 1e-3, 2e-3]
        ds2 = np.array([dA * (1 - s) for s in S2])
        kap2 = np.array([P.ligado(k, d, observables=False)["kappa"] for d in ds2])
        co2 = np.polyfit(ds2 - dA, kap2, 3)
        rr2 = np.roots(co2); rr2 = rr2[np.abs(rr2.imag) < 1e-12].real
        dB2 = float(dA + rr2[np.argmin(np.abs(rr2))])
        rec = dict(delta_B2_post_hoc=dB2, dif_AB2=float(dA - dB2), delta_A=float(dA), delta_A_rf80=float(dA_rf80), delta_A_rtol11=float(dA_rt11),
                   delta_B=dB, delta_B_cuartico=dB4, dif_AB=float(dA - dB), residuo_ajuste_B=resid,
                   puntos_B=dict(delta=ds.tolist(), kappa=kap.tolist()),
                   literatura=[dict(fuente=f, valor=v, dif=float(dA - v)) for f, v in LIT[k]])
        if k == "hulthen":
            rec["dif_kappa_exacto_max"] = float(np.max(np.abs(kap - (1 - ds / 2))))
        out["perfiles"][k] = rec
        T(f"{k:8s} delta_A = {dA:.13f}  (rf80 {dA_rf80 - dA:+.1e}, rtol11 {dA_rt11 - dA:+.1e})  "
          f"delta_B = {dB:.13f} (cuartico {dB4:.13f}; B2 post hoc {dB2:.13f})  A-B = {dA - dB:+.2e}  resid {resid:.1e}")
        for f, v in LIT[k]:
            T(f"           literatura {f}: {v}  (delta_A - lit = {dA - v:+.2e})")
    pf = out["perfiles"]
    ok["U1"] = all(abs(p["delta_A_rf80"] - p["delta_A"]) < 1e-11 and abs(p["delta_A_rtol11"] - p["delta_A"]) < 1e-10 for p in pf.values())
    ok["U2"] = all(abs(p["dif_AB"]) < 1e-8 for p in pf.values())
    ok["U3"] = bool(abs(pf["hulthen"]["delta_A"] - 2) < 1e-10 and abs(pf["yukawa"]["delta_A"] - C.DELTA_C_YUK_REF) < 1e-10)
    ok["U4"] = bool(pf["hulthen"]["dif_kappa_exacto_max"] < 1e-11)
    out["pasa"] = ok
    T("controles:", ok)
    C.guardar("01_umbrales", out)
    T.cerrar()


if __name__ == "__main__":
    main()
