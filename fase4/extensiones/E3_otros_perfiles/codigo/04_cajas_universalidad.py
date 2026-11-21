"""04_cajas_universalidad.py -- E3: lo que ve una caja esferica dura en el umbral, para cada perfil.

Caja de Dirichlet u(R) = 0, E0(R) por disparo (sin malla). Fuera del alcance u = sin(k(R - r)), asi que
    k cot delta_0(k) = -k cot(kR)     (exacto si R >> 1/delta),
y con el desarrollo de rango efectivo k cot delta_0 = -1/a + r_e k^2/2 + P k^4, con x = kR:
    -x cot x = -R/a + r_e x^2/(2R) + P x^4/R^3.                                       (*)
Consecuencias que se comprueban:
  (1) Punto fijo: en delta_c (1/a = 0), x -> pi/2 y 2R^2E0/pi^2 -> 1/4; a primer orden
      2R^2E0/pi^2 = (1/4)(1 + r_e/R): el lado por el que se llega lo fija el signo de r_e.
  (2) Cruce de cajas R1, R2 (R1^2 E0(R1) = R2^2 E0(R2)): de (*) a primer orden 1/a* = -r_e pi^2/(8 R1 R2), es decir
      delta* - delta_c = r_e pi^2/(8 c R1 R2): con r_e > 0 el cruce llega desde arriba (Yukawa) y con r_e < 0 desde
      abajo (ECSC). Se compara el cruce medido con (*) completo (a, r_e, P del mismo delta) y con el primer orden.
  (3) <r>/R en delta_c -> 1/2 - 2/pi^2 (estado cos(pi r/2R) en el limite).
  (4) Polo virtual visto por la caja: en delta = delta_c (1 + s), s = 0.01 y 0.03, los E0(R) > 0 de R = 50..1600 dan
      k cot delta_0 = -k cot(kR); ajuste en k^2 (grado 2) -> a_caja, r_e,caja -> kappa_v; frente a 02/03.
Control de malla: radial.resolver_rich (diferencias finitas, Fase 2) frente al disparo en R = 200, delta = delta_c.

Criterios fijados ANTES de correr:
  K1 |2R^2E0/pi^2 - prediccion (*)| / (1/4) < 1e-3 para R >= 200, y signo(2R^2E0/pi^2 - 1/4) = signo(r_e) para todo R
  K2 signo(delta* - delta_c) = signo(r_e) en todos los pares (R, 2R); |cruce - prediccion (*)| < 0.1 |cruce - delta_c|
     para R1 >= 200
  K3 |<r>/R - (1/2 - 2/pi^2)| < 0.02 en R = 1600 (la correccion es O(r_e/R))
  K4 |kappa_v(caja) - kappa_v(directo)| / kappa_v < 1e-3 (s = 0.01 y 0.03)
  K5 |E0(radial) - E0(disparo)| < 2 err_radial + 1e-10 (err_radial = |E_h - E_h/2|), R = 200
"""
import sys

import numpy as np
from scipy.optimize import brentq

import comun_e3 as C
import perfiles as P

sys.path.insert(0, C.F2)
import radial  # noqa: E402

CRIT = {
    "K1": "|2R^2E0/pi^2 - pred(*)|/(1/4) < 1e-3 (R >= 200) y signo(valor - 1/4) = signo(r_e) (todo R)",
    "K2": "signo(delta* - delta_c) = signo(r_e) (todos los pares); |cruce - pred(*)| < 0.1|cruce - delta_c| (R1 >= 200)",
    "K3": "|<r>/R - (1/2 - 2/pi^2)| < 0.02 en R = 1600",
    "K4": "|kappa_v(caja) - kappa_v(directo)|/kappa_v < 1e-3",
    "K5": "|E0 radial - E0 disparo| < 2 err_radial + 1e-10 (R = 200)",
}
RS = [50, 100, 200, 400, 800, 1600]


def menos_xcotx(y):
    """-x cot x como funcion de y = x^2 (y < 0: x = i q, -x cot x = -q coth q)."""
    if y > 0:
        x = np.sqrt(y)
        return -x / np.tan(x)
    if y < 0:
        q = np.sqrt(-y)
        return -q / np.tanh(q)
    return -1.0


def E_pred(R, ia, re, Pf):
    """E0 de (*): raiz y en (-(R/a)^2*4 - 10, (pi)^2) del estado sin nodos."""
    f = lambda y: menos_xcotx(y) - (-R * ia + re * y / (2 * R) + Pf * y * y / R**3)
    hi = np.pi**2 * (1 - 1e-9)
    lo = -max(10.0, 4 * (R * ia)**2 + 10)
    return brentq(f, lo, hi, xtol=1e-15, rtol=1e-14) / (2 * R * R)


def ere(k, d):
    z = P.cero(k, d)
    ks = d * np.linspace(0.005, 0.05, 10)
    co = np.polyfit(ks**2, [P.kcot(k, d, x) for x in ks], 4)
    return z["inv_a"], z["r_e"], float(co[-3])


def caja_obs(k, d, R):
    E = P.caja(k, d, R)
    p = P.PERFILES[k]
    s = P._integrar(p["V"](d), p["W0"](d), E, R, extra=lambda r, y: [y[0]**2, r * y[0]**2, 0.0 * r])
    return E, float(s.y[3, -1] / s.y[2, -1] / R)


def main():
    T = C.Tee("04_cajas_universalidad")
    D2 = C.cargar("02_dispersion")["perfiles"]
    D3 = C.cargar("03_ligados_virtuales")["perfiles"]
    out = dict(script="04_cajas_universalidad.py", criterios=CRIT, perfiles={}, r_sobre_R_universal=0.5 - 2 / np.pi**2)
    ok = {k: True for k in CRIT}
    for k in C.ORDEN:
        dc, c = D2[k]["delta_c"], D2[k]["c_HF"]
        ia0, re0, P0 = ere(k, dc)
        T(f"\n== {k}: delta_c={dc:.12f} r_e={re0:+.6f} P={P0:+.4f} c={c:.6f}")
        fijo = []
        for R in RS:
            E, rR = caja_obs(k, dc, R)
            v = 2 * R * R * E / np.pi**2
            vp = 2 * R * R * E_pred(R, ia0, re0, P0) / np.pi**2
            v1 = 0.25 * (1 + re0 / R)
            fijo.append(dict(R=R, E0=E, valor=float(v), pred=float(vp), pred_1orden=float(v1), r_sobre_R=rR,
                             R_por_desv=float((v - 0.25) * R)))
            if R >= 200:
                ok["K1"] &= bool(abs(v - vp) / 0.25 < 1e-3)
            ok["K1"] &= bool(np.sign(v - 0.25) == np.sign(re0))
            T(f"   R={R:5d}  2R^2E/pi^2={v:.8f}  pred(*)={vp:.8f}  1/4(1+r_e/R)={v1:.8f}  R(v-1/4)={(v-0.25)*R:+.5f} "
              f"(r_e/4={re0/4:+.5f})  <r>/R={rR:.6f}")
        ok["K3"] &= bool(abs(fijo[-1]["r_sobre_R"] - (0.5 - 2 / np.pi**2)) < 0.02)
        # cruces
        cruces = []
        for R1 in RS[:-1]:
            R2 = 2 * R1
            g = lambda d: P.caja(k, d, R1) * R1**2 - P.caja(k, d, R2) * R2**2
            span = 0.02 * dc
            ds_ = np.linspace(dc - span, dc + span, 9)
            gv = [g(d) for d in ds_]
            dstar = None
            for i in range(8):
                if np.sign(gv[i]) != np.sign(gv[i + 1]):
                    dstar = brentq(g, ds_[i], ds_[i + 1], xtol=1e-14, rtol=1e-14)
                    break

            def gp(d):
                ia, re, Pf = ere(k, d)
                return E_pred(R1, ia, re, Pf) * R1**2 - E_pred(R2, ia, re, Pf) * R2**2
            dpred = brentq(gp, dc - span, dc + span, xtol=1e-13, rtol=1e-14)
            d1 = dc + re0 * np.pi**2 / (8 * c * R1 * R2)
            vstar = 2 * R2**2 * P.caja(k, dstar, R2) / np.pi**2
            cruces.append(dict(R1=R1, R2=R2, delta_star=float(dstar), dif=float(dstar - dc), pred=float(dpred),
                               pred_1orden=float(d1), valor_en_cruce=float(vstar)))
            ok["K2"] &= bool(np.sign(dstar - dc) == np.sign(re0))
            if R1 >= 200:
                ok["K2"] &= bool(abs(dstar - dpred) < 0.1 * abs(dstar - dc))
            T(f"   cruce {R1}/{R2}: delta*={dstar:.10f} (delta*-dc={dstar-dc:+.3e})  pred(*)={dpred-dc:+.3e}  "
              f"1er orden={d1-dc:+.3e}  2R^2E/pi^2 en el cruce={vstar:.6f}")
        # polo virtual desde la caja
        vir = []
        for s in (0.01, 0.03):
            d = dc * (1 + s)
            Es = np.array([P.caja(k, d, R) for R in RS])
            kk = np.sqrt(2 * Es)
            kc = -kk / np.tan(kk * np.array(RS))
            co = np.polyfit(kk**2, kc, 2)
            ia_b, re_b = -co[-1], 2 * co[-2]
            kv_b = (-1 + np.sqrt(1 - 2 * re_b * ia_b)) / re_b
            ref = [x for x in D3[k]["virtuales"] if abs(x["s"] - s) / s < 1e-6]
            if ref:
                kv_dir = ref[0]["kappa_v_dir"]
            else:   # s = 0.01, 0.03 no estan en la rejilla de 03: se calcula aqui con la misma rutina
                import importlib
                m3 = importlib.import_module("03_ligados_virtuales")
                kv_dir = m3.virtual(k, d, -ia_b)[0]
            z = P.cero(k, d)
            vir.append(dict(s=s, delta=float(d), E0_cajas=Es.tolist(), inv_a_caja=float(ia_b), r_e_caja=float(re_b),
                            inv_a=z["inv_a"], r_e=z["r_e"], kappa_v_caja=float(kv_b), kappa_v_dir=float(kv_dir),
                            E_virtual_caja=float(-0.5 * kv_b**2), dif_rel=float((kv_b - kv_dir) / kv_dir)))
            ok["K4"] &= bool(abs(kv_b - kv_dir) / kv_dir < 1e-3)
            T(f"   virtual s={s}: caja 1/a={ia_b:+.8f} (E=0: {z['inv_a']:+.8f}) r_e={re_b:+.5f} (E=0: {z['r_e']:+.5f})  "
              f"kappa_v caja={kv_b:.8e} directo={kv_dir:.8e} dif rel={(kv_b-kv_dir)/kv_dir:+.1e}")
        # control de malla con el radial de la Fase 2
        V = P.PERFILES[k]["V"](dc)
        rr = radial.resolver_rich(V, 200.0, h=1 / 40, nev=1)
        Esh = [x["E0"] for x in fijo if x["R"] == 200][0]
        err = abs(rr["E0_h"] - rr["E0_h2"])
        ok["K5"] &= bool(abs(rr["E0"] - Esh) < 2 * err + 1e-10)
        T(f"   radial FD R=200: E0={rr['E0']:.12e}  disparo={Esh:.12e}  dif={rr['E0']-Esh:+.1e}  err_radial={err:.1e}")
        out["perfiles"][k] = dict(delta_c=dc, r_e=re0, P=P0, c=c, punto_fijo=fijo, cruces=cruces, virtual_caja=vir,
                                  radial_R200=dict(E0=rr["E0"], err=err, disparo=Esh))
    out["pasa"] = ok
    T("controles:", ok)
    C.guardar("04_cajas_universalidad", out)
    T.cerrar()


if __name__ == "__main__":
    main()
