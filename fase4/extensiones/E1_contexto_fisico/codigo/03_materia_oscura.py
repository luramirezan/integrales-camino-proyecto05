"""03_materia_oscura.py -- materia oscura que interactua por un mediador ligero (potencial de Yukawa).

V(r) = -alpha e^{-m_phi r}/r entre dos particulas de masa m_chi: masa reducida m = m_chi/2, g = alpha hbar c,
mu_s = m_phi c/hbar. Entonces delta = m_phi/(m alpha) = 2 m_phi/(alpha m_chi), y hay estado ns ligado si
delta < delta_c(ns), es decir, si b = alpha m_chi/m_phi > 2/delta_c(ns).
Se compara con:
  * Tulin, Yu y Zurek (2013), Sec. IV B: primera resonancia s en b = 1.68 y antirresonancia s en b = 4.52
    (b = alpha m_X/m_phi, masa reducida m_X/2; barrido numerico de la ecuacion de Schrodinger).
  * Aproximacion de Hulthen: resonancias en b = kappa n^2 con kappa = 1.6 (Tulin et al., Ec. 24) y
    kappa = pi^2/6 (Feng, Kaplinghat y Yu 2010, Ec. 7).
  * Petraki, Postma y de Vries (2017): solo da la condicion aproximada xi = mu alpha/m_phi >~ n^2 en el texto
    principal (Sec. 2.2); en nuestras variables xi = b/2.
La antirresonancia (fase s nula a v -> 0) es el cero de la longitud de dispersion entre los umbrales 1s y 2s;
se calcula con dos metodos (solve_ivp y Numerov propio).
Criterios FIJADOS ANTES DE CORRER:
  C8  |2/delta_c - 1.68| <= 0.005 (redondeo de la cifra publicada)
  C9  |b_antirresonancia - 4.52| <= 0.005 y |a_s=0 por A - por B| < 1e-6 en delta
Salida: resultados/03_materia_oscura.json
"""
import time

import numpy as np
from scipy.optimize import brentq

import comun_e1 as c

log = c.Registro()
t0 = time.perf_counter()
K = c.CONST
U1 = c.leer("01_umbral")
dcs = {"1s": U1["delta_c_1s"]["A"], "2s": U1["delta_c_2s"]["A"], "3s": U1["delta_c_3s"]["A"]}
b_n = {k: 2.0 / v for k, v in dcs.items()}
xi_n = {k: 1.0 / v for k, v in dcs.items()}
for k in dcs:
    log(f"{k}: delta_c = {dcs[k]:.10f}  ->  alpha m_chi/m_phi > {b_n[k]:.6f}   (xi = mu alpha/m_phi > {xi_n[k]:.6f})")

hul = {"kappa_1.6": [K["tyz_kappa_hulthen"] * n ** 2 for n in (1, 2, 3)],
       "kappa_pi2/6": [np.pi ** 2 / 6 * n ** 2 for n in (1, 2, 3)]}
for k, v in hul.items():
    log(f"Hulthen {k}: b_n = " + ", ".join(f"{x:.4f}" for x in v))
err_hul = {k: [v[i] / b_n[s] - 1 for i, s in enumerate(("1s", "2s", "3s"))] for k, v in hul.items()}
for k, v in err_hul.items():
    log(f"   error relativo frente al Yukawa: " + ", ".join(f"{x:+.3%}" for x in v))

# --- antirresonancia: a_s(delta) = 0 con delta_c(2s) < delta < delta_c(1s)
aA = lambda d: c.long_dispersion_A(d, R=200.0)
aB = lambda d: c.long_dispersion_B(d, h=1 / 400, R=200.0)
# a_s pasa de -inf (justo arriba de delta_c(2s)... ) a +inf al acercarse a delta_c(1s) por debajo; buscar cambio de signo
ds = np.linspace(0.33, 1.15, 42)
va = [aA(d) for d in ds]
raices = []
for i in range(len(ds) - 1):
    if np.sign(va[i]) != np.sign(va[i + 1]) and abs(va[i]) < 50 and abs(va[i + 1]) < 50:
        raices.append((ds[i], ds[i + 1]))
log("intervalos con cambio de signo de a_s (|a_s|<50):", raices)
d0A = brentq(aA, *raices[0], xtol=1e-13)
d0B = brentq(aB, *raices[0], xtol=1e-13)
b_anti = 2.0 / d0A
log(f"a_s = 0 en delta = {d0A:.10f} (A), {d0B:.10f} (B)  ->  b = {b_anti:.5f} (Tulin et al.: {K['tyz_b_antires']})")
# [Revision R1-03] antirresonancia de Hulthen (Tulin, Yu y Zurek, Sec. VI): b = kappa r^2 con
# 2 gamma + psi(1 + r) + psi(1 - r) = 0, primera raiz r ~ 1.69
from scipy.special import digamma
r_hul = brentq(lambda r: 2 * np.euler_gamma + digamma(1 + r) + digamma(1 - r), 1.2, 1.99, xtol=1e-14)
b_anti_hul = {"kappa_1.6": K["tyz_kappa_hulthen"] * r_hul ** 2, "kappa_pi2/6": np.pi ** 2 / 6 * r_hul ** 2}
log(f"antirresonancia de Hulthen: r = {r_hul:.5f}, b = {b_anti_hul['kappa_1.6']:.4f} (kappa 1.6),"
    f" {b_anti_hul['kappa_pi2/6']:.4f} (pi^2/6)")
# longitud de dispersion a ambos lados del umbral (como en la Fase 3: a_s(1.19) = +2204, a_s(1.20) = -142.9)
a119 = aA(1.19)
a120 = aA(1.20)
log(f"control de signo: a_s(1.19) = {a119:.1f}, a_s(1.20) = {a120:.2f}")

# --- ejemplos numericos (solo ilustrativos): masa minima de m_chi para que exista el 1s
ejemplos = []
for alpha in (0.01, 0.1):
    for mphi_MeV in (1.0, 10.0, 100.0):
        mchi_min_GeV = b_n["1s"] * mphi_MeV / alpha / 1000.0
        ejemplos.append(dict(alpha=alpha, m_phi_MeV=mphi_MeV, m_chi_min_GeV=mchi_min_GeV))
        log(f"alpha = {alpha:5g}, m_phi = {mphi_MeV:6g} MeV  ->  hay 1s si m_chi > {mchi_min_GeV:.4g} GeV")

ctl = [dict(id="C8", control="Primera resonancia s de Tulin, Yu y Zurek (b = 1.68) frente a 2/delta_c",
            criterio="|2/delta_c - 1.68| <= 0.005", valor=f"2/delta_c = {b_n['1s']:.5f}",
            pasa=bool(abs(b_n["1s"] - K["tyz_b_res"]) <= 0.005)),
       dict(id="C9", control="Antirresonancia s (a_s = 0) frente a Tulin, Yu y Zurek (b = 4.52); A frente a B",
            criterio="|b - 4.52| <= 0.005 y |delta_A - delta_B| < 1e-6",
            valor=f"b = {b_anti:.4f}; dif A-B = {d0A - d0B:.1e}",
            pasa=bool(abs(b_anti - K["tyz_b_antires"]) <= 0.005 and abs(d0A - d0B) < 1e-6))]
for k in ctl:
    log(k["id"], k["control"], "|", k["valor"], "|", "pasa" if k["pasa"] else "NO PASA")
out = dict(delta_c=dcs, b_umbral=b_n, xi_umbral=xi_n, hulthen=hul, error_rel_hulthen=err_hul,
           antirresonancia=dict(delta_A=d0A, delta_B=d0B, b=b_anti, b_tyz=K["tyz_b_antires"],
                                r_hulthen=r_hul, b_hulthen=b_anti_hul),
           a_s_119=a119, a_s_120=a120, ejemplos=ejemplos, controles=ctl, t_s=time.perf_counter() - t0)
log(f"tiempo {out['t_s']:.1f} s")
c.guardar("03_materia_oscura", out, log.texto())
