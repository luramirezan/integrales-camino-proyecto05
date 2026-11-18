"""r03_antirresonancia_y_extras.py -- revisor: (1) antirresonancia de Hulthen segun Tulin, Yu y Zurek (2013), Sec. VI:
b = kappa r^2 con 2 gamma + psi(1+r) + psi(1-r) = 0; (2) a_s del Yukawa en b = 4.52; (3) cero de la fase s del
Yukawa a momento finito k (kL = v/alpha = 2a en variables de TYZ) para ver si la velocidad finita mueve el cero;
(4) sensibilidad del deuteron de juguete incluyendo la variacion de la masa del nucleon (K_N^q de Berengut et al.);
(5) radio experimental con r_n^2 del PDG 2024 y con la diferencia isotopica r_d^2 - r_p^2 = 3.82070(31) fm^2."""
import json, os
import numpy as np
from scipy.special import digamma
from scipy.optimize import brentq
from scipy.integrate import solve_ivp
import scipy.constants as sc
AQUI = os.path.dirname(os.path.abspath(__file__))
R1 = json.load(open(os.path.join(AQUI, "r01_recalculo.json")))
out = {}
g = np.euler_gamma
f = lambda r: 2 * g + digamma(1 + r) + digamma(1 - r)
r1 = brentq(f, 1.2, 1.99)
out["hulthen_r1"] = r1
out["b_anti_hulthen_1.6"] = 1.6 * r1 ** 2
out["b_anti_hulthen_pi2/6"] = np.pi ** 2 / 6 * r1 ** 2
print(f"Hulthen: r1 = {r1:.5f}; b_anti = {1.6 * r1**2:.4f} (kappa 1.6), {np.pi**2/6 * r1**2:.4f} (pi^2/6);"
      f" Yukawa exacto (r01) = {R1['mo']['b_anti']:.4f}")


def fase_k(delta, k, R=120.0):
    """fase s a momento k (unidades 1/L), Pruefer: tan(phi) = k u/u', phi' = k + (U/k) sin^2(phi), U = -2V."""
    def fun(r, y):
        p = y[0]
        s = np.sin(p)
        U = 2 * np.exp(-delta * r) / r if r > 0 else 0.0   # -2V
        return [k + (U / k) * s * s]
    s = solve_ivp(fun, [0, R], [0.0], method="Radau", rtol=1e-12, atol=1e-14)
    return s.y[0, -1] - k * R        # delta_0 mod pi


for kk in (1e-3, 0.02, 0.05, 0.06, 0.1):
    d0 = brentq(lambda d: np.sin(fase_k(d, kk)), 0.40, 0.50, xtol=1e-12)
    out[f"b_cero_fase_k{kk:g}"] = 2 / d0
    print(f"cero de la fase s del Yukawa con kL = {kk:g} (a = v/2alpha = {kk/2:g}): b = {2 / d0:.4f}")
# a_s en b = 4.52
d452 = 2 / 4.52
s = solve_ivp(lambda r, y: [np.cos(y[0]) ** 2 + (2 * np.exp(-d452 * r) / r) * np.sin(y[0]) ** 2 if r > 0 else 1.0],
              [0, 200], [0.0], method="Radau", rtol=1e-13, atol=1e-15)
a452 = 200 - np.tan(s.y[0, -1])
out["a_s_b4.52_L"] = a452
print(f"a_s(b = 4.52) = {a452:.4f} L = {a452 * d452:.4f} / m_phi  (la caida de sigma ~ 4 pi a^2 es fuerte pero no nula)")
# sensibilidad con masa del nucleon variable (K_N^q = 0.048, Berengut Ec. 2.4) a g fijo
D = R1["deuteron"]
s_pi = D["escenarios"]["promedio"]["sens"]       # dlnB/dln m_pi a g y mu fijos
dlnB_dlnmu = 1 - s_pi                              # B = mu alpha^2 |eps(m_pi/(mu alpha))|
Kpi, KN, Kd = 0.494, 0.048, -0.86
Kd_mod = s_pi * Kpi + dlnB_dlnmu * KN
out.update(sens_mu=dlnB_dlnmu, K_deut_modelo_gfijo=Kd_mod, cociente_con_mN=Kd_mod / Kd,
           cociente_sin_mN=s_pi * Kpi / Kd)
print(f"modelo a g fijo: dlnB/dln mu = {dlnB_dlnmu:.4f}; K_deut(modelo) = {Kd_mod:.3f} con m_N variable"
      f" (frente a {s_pi * Kpi:.3f} sin ella); Berengut -0.86: cociente {Kd_mod / Kd:.2f} (sin m_N: {s_pi * Kpi / Kd:.2f})")
# radio experimental
hc = sc.hbar * sc.c / (sc.e * 1e6) * 1e15
mp = sc.physical_constants["proton mass energy equivalent in MeV"][0]
DF = 0.75 * (hc / mp) ** 2
rd, rp = 2.12778, 0.84075
for nombre, rn2, urn2 in (("PDG antiguo (Filin)", -0.1161, 0.0022), ("PDG 2024", -0.1155, 0.0017)):
    rs = np.sqrt(rd ** 2 - rp ** 2 - rn2 - DF)
    u_ind = np.sqrt((2 * rd * 0.00027) ** 2 + (2 * rp * 0.00064) ** 2 + urn2 ** 2) / (2 * rs)
    u_iso = np.sqrt(0.00031 ** 2 + urn2 ** 2) / (2 * rs)
    rs_iso = np.sqrt(3.82070 - rn2 - DF)
    out[f"rstr_{nombre}"] = dict(rstr=rs, u_indep=u_ind, u_iso=u_iso, rstr_iso=rs_iso)
    print(f"r_str ({nombre}): {rs:.5f} fm, u indep = {u_ind:.5f}, u con dif. isotopica = {u_iso:.5f};"
          f" con r_d^2-r_p^2 = 3.82070: {rs_iso:.5f} fm")
json.dump(out, open(os.path.join(AQUI, "r03_extras.json"), "w"), indent=2, default=float)
