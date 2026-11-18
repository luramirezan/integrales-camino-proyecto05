"""r01_recalculo_independiente.py -- revision adversarial de E1: recalculo desde cero de las cifras centrales.

Escrito por el revisor (no reutiliza codigo de E1 ni de las Fases 2-3). Metodos distintos a los de E1:
  * Umbrales y longitud de dispersion: ecuacion de fase de Pruefer a energia cero,
        u = rho sin(phi), u' = rho cos(phi),  phi' = cos^2 phi + 2 e^{-delta r} sin^2(phi)/r,  phi(0) = 0,
    integrada con Radau (implicito) desde r = 0 exacto. Umbral n-esimo: phi(R) = (n - 1/2) pi; longitud de
    dispersion a = R - tan(phi(R)) (convencion u ~ r - a, a > 0 con ligado, como en el proyecto).
  * Estado 1s: colocacion espectral de Chebyshev con el mapeo algebraico r = Lm (1+x)/(1-x) (Dirichlet en r=0 e
    infinito), autovalores densos; observables con cuadratura de Clenshaw-Curtis. Sensibilidad por
    Hellmann-Feynman: d eps/d delta = <e^{-delta r}>, sin diferencias finitas.
  * Constantes: scipy.constants (CODATA 2022 en scipy 1.18) y, para lo que scipy no trae, PDG 2025 escrito aqui.
Salida: revision/r01_recalculo.json y r01_recalculo_salida.txt
"""
import json
import os
import time

import numpy as np
import scipy.constants as sc
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

AQUI = os.path.dirname(os.path.abspath(__file__))
lineas = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    lineas.append(s)


t0 = time.perf_counter()


# --------------------------------------------------------------------------- Pruefer a energia cero
def fase_cero(delta, R=200.0):
    def f(r, y):
        p = y[0]
        s = np.sin(p)
        pot = 2.0 * np.exp(-delta * r) * (s * s / r if r > 0 else 0.0)
        return [np.cos(p) ** 2 + pot]
    s = solve_ivp(f, [0.0, R], [0.0], method="Radau", rtol=1e-13, atol=1e-15)
    return s.y[0, -1], R


def umbral(n, a, b, R=200.0):
    return brentq(lambda d: fase_cero(d, R)[0] - (n - 0.5) * np.pi, a, b, xtol=1e-15, rtol=1e-15)


def a_disp(delta, R=200.0):
    p, R = fase_cero(delta, R)
    return R - np.tan(p)


# --------------------------------------------------------------------------- Chebyshev con mapeo algebraico
def cheb(N):
    x = np.cos(np.pi * np.arange(N + 1) / N)
    c = np.hstack([2, np.ones(N - 1), 2]) * (-1) ** np.arange(N + 1)
    X = np.tile(x, (N + 1, 1)).T
    dX = X - X.T
    D = np.outer(c, 1 / c) / (dX + np.eye(N + 1))
    D -= np.diag(D.sum(axis=1))
    return D, x


def clenshaw_curtis(N):
    theta = np.pi * np.arange(N + 1) / N
    w = np.zeros(N + 1)
    v = np.ones(N - 1)
    th = theta[1:-1]
    if N % 2 == 0:
        w[0] = w[N] = 1.0 / (N ** 2 - 1)
        for k in range(1, N // 2):
            v -= 2 * np.cos(2 * k * th) / (4 * k * k - 1)
        v -= np.cos(N * th) / (N ** 2 - 1)
    else:
        w[0] = w[N] = 1.0 / N ** 2
        for k in range(1, (N - 1) // 2 + 1):
            v -= 2 * np.cos(2 * k * th) / (4 * k * k - 1)
    w[1:-1] = 2 * v / N
    return w


_cache = {}


def estado(delta, Lm, N=260, pot="yukawa"):
    key = N
    if key not in _cache:
        _cache[key] = (cheb(N), clenshaw_curtis(N))
    (D, x), w = _cache[key]
    xi = x[1:-1]
    r = Lm * (1 + xi) / (1 - xi)
    rp = 2 * Lm / (1 - xi) ** 2
    rpp = 4 * Lm / (1 - xi) ** 3
    D1 = D[1:-1, 1:-1]
    D2 = (D @ D)[1:-1, 1:-1]
    d2 = np.diag(1 / rp ** 2) @ D2 - np.diag(rpp / rp ** 3) @ D1
    if pot == "yukawa":
        V = -np.exp(-delta * r) / r
    else:   # Hulthen: -delta e^{-delta r}/(1 - e^{-delta r})
        V = -delta / np.expm1(np.minimum(delta * r, 700))
    H = -0.5 * d2 + np.diag(V)
    ev, vec = np.linalg.eig(H)
    ev = ev.real
    i = np.argmin(ev)
    u = vec[:, i].real
    ww = w[1:-1] * rp
    nrm = np.sum(ww * u * u)
    m1 = np.sum(ww * r * u * u) / nrm
    m2 = np.sum(ww * r * r * u * u) / nrm
    hf = np.sum(ww * np.exp(-delta * r) * u * u) / nrm      # <e^{-delta r}> = d eps/d delta
    return dict(E=ev[i], r=m1, r2=m2, dEdd=hf)


def estado_conv(delta, Lm, pot="yukawa"):
    """dos N para estimar error espectral."""
    a = estado(delta, Lm, 220, pot)
    b = estado(delta, Lm, 300, pot)
    b["errE"] = abs(a["E"] - b["E"])
    b["err_r2"] = abs(a["r2"] - b["r2"])
    return b


res = {}
# --------------------------------------------------------------------------- 1. umbrales
dc1 = umbral(1, 1.15, 1.25)
dc1_R100 = brentq(lambda d: fase_cero(d, 100.0)[0] - 0.5 * np.pi, 1.15, 1.25, xtol=1e-15)
dc2 = umbral(2, 0.28, 0.35, R=400.0)
dc3 = umbral(3, 0.12, 0.16, R=600.0)
res["delta_c"] = {"1s": dc1, "1s_R100": dc1_R100, "2s": dc2, "3s": dc3}
log(f"[umbral Pruefer] dc(1s) = {dc1:.13f} (R=100: {dc1_R100:.13f}); dc(2s) = {dc2:.11f}; dc(3s) = {dc3:.11f}")

# controles exactos del Chebyshev
cou = estado_conv(0.0, 1.0)
hul = estado_conv(1.0, 2.0, pot="hulthen")
log(f"[Cheb] Coulomb E+1/2 = {cou['E'] + 0.5:.1e}, <r>-1.5 = {cou['r'] - 1.5:.1e}, <r2>-3 = {cou['r2'] - 3:.1e}")
log(f"[Cheb] Hulthen d=1: E+1/8 = {hul['E'] + 0.125:.1e}, <r>-11/6 = {hul['r'] - 11 / 6:.1e}")
res["exactos"] = dict(coulomb=cou, hulthen=hul)

# --------------------------------------------------------------------------- 2. plasma
a0 = sc.physical_constants["Bohr radius"][0]
Eh = sc.physical_constants["Hartree energy in eV"][0]
me, mp = sc.m_e, sc.m_p
lam_c = a0 / dc1
lam_c_red = a0 * (1 + me / mp) / dc1
coefNRL = np.sqrt(sc.epsilon_0 * sc.e / (1e6 * sc.e ** 2)) * 100     # cm, T = 1 eV, n = 1 cm^-3
n1 = sc.epsilon_0 * 1.0 * sc.e / (sc.e ** 2 * lam_c ** 2) * 1e-6       # cm^-3 a 1 eV
log(f"[plasma] lambda_c = {lam_c / a0:.7f} a0 = {lam_c * 1e12:.4f} pm; masa reducida {lam_c_red / a0:.7f} a0;"
    f" coef. Debye = {coefNRL:.4f} cm; n_e/T = {n1:.4e} cm^-3/eV")


def indic(T):
    n = n1 * T * 1e6
    ND = 4 * np.pi / 3 * n * lam_c ** 3
    aws = (3 / (4 * np.pi * n)) ** (1 / 3)
    G = sc.e ** 2 / (4 * np.pi * sc.epsilon_0 * aws) / (T * sc.e)
    EF = sc.hbar ** 2 * (3 * np.pi ** 2 * n) ** (2 / 3) / (2 * me) / sc.e
    # longitud de Debye total (e + p a la misma T): misma lambda requiere n/2; tambien con electrones
    # degenerados (Thomas-Fermi generalizado) la longitud real es mayor: lambda^-2 = e^2 n/(eps0 kT_eff)
    return dict(n=n * 1e-6, ND=ND, Gamma=G, Theta=T / EF, aws_lam=aws / lam_c, EF=EF)


pl = {f"{T:g}": indic(T) for T in (1.0, 13.6, 100.0, 1000.0)}
for k, v in pl.items():
    log(f"   T = {k} eV: n = {v['n']:.4e}, N_D = {v['ND']:.4e}, Gamma = {v['Gamma']:.3f}, T/E_F = {v['Theta']:.3f},"
        f" a_ws/lambda = {v['aws_lam']:.3f}")
T_ND1 = 1 / pl["1"]["ND"]
log(f"   N_D = 1 en T = {T_ND1:.2f} eV")
# energias del 1s en la curva de 02_plasma
curva = {}
for d in (0.2, 0.4, 0.6, 0.8, 1.0, 1.1, 1.15, 1.18):
    E0 = estado_conv(d, 1.0)["E"]
    kap = np.sqrt(-2 * E0)
    s = estado_conv(d, 0.5 / kap)
    curva[f"{d:g}"] = dict(E=s["E"], errE=s["errE"], E_eV=s["E"] * Eh)
    log(f"   [Cheb] delta = {d:4.2f}: E = {s['E']:.12f} Ha (err espectral {s['errE']:.1e}), {s['E'] * Eh:.5f} eV")
res["plasma"] = dict(lam_c_a0=lam_c / a0, lam_c_pm=lam_c * 1e12, lam_c_red_a0=lam_c_red / a0, coef_cm=coefNRL,
                     n_por_eV=n1, puntos=pl, T_ND1=T_ND1, curva=curva)

# --------------------------------------------------------------------------- 3. materia oscura
b = {k: 2 / v for k, v in (("1s", dc1), ("2s", dc2), ("3s", dc3))}
d_anti = brentq(a_disp, 0.40, 0.50, xtol=1e-14)
log(f"[MO] b_c = {b['1s']:.6f}, {b['2s']:.4f}, {b['3s']:.4f}; xi_c = {1 / dc1:.6f};"
    f" Hulthen 1.6: {1.6 / b['1s'] - 1:+.3%}, pi2/6: {np.pi ** 2 / 6 / b['1s'] - 1:+.3%}")
log(f"[MO] a_s = 0 en delta = {d_anti:.10f} -> b = {2 / d_anti:.5f}; a_s(1.19) = {a_disp(1.19):.1f},"
    f" a_s(1.20) = {a_disp(1.20):.2f}; ejemplo m_chi(alpha=0.01, m_phi=10 MeV) = {b['1s'] * 10 / 0.01 / 1000:.4f} GeV")
res["mo"] = dict(b=b, xi=1 / dc1, d_anti=d_anti, b_anti=2 / d_anti, a119=a_disp(1.19), a120=a_disp(1.20))

# --------------------------------------------------------------------------- 4. deuteron
MeV = sc.physical_constants["electron volt-joule relationship"][0] * 1e6
m_p = sc.physical_constants["proton mass energy equivalent in MeV"][0]
m_n = sc.physical_constants["neutron mass energy equivalent in MeV"][0]
m_d = sc.physical_constants["deuteron mass energy equivalent in MeV"][0]
hc = sc.hbar * sc.c / MeV * 1e15
Bd = m_p + m_n - m_d
mu = m_p * m_n / (m_p + m_n)
mpi = {"pi0": 134.9768, "pi+-": 139.57039}
mpi["promedio"] = (2 * mpi["pi+-"] + mpi["pi0"]) / 3
log(f"[d] m_p = {m_p}, m_n = {m_n}, m_d = {m_d}, hbar c = {hc:.7f}; B = {Bd:.8f} MeV, mu = {mu:.8f}")


def eps_de(d):
    E0 = estado(d, 1.0, 220)["E"]
    return estado(d, 0.5 / np.sqrt(-2 * E0), 260)


def ajusta(target, a=0.3, b=1.15):
    return brentq(lambda d: eps_de(d)["E"] / d ** 2 - target, a, b, xtol=1e-13)


deu = {}
for k, m in mpi.items():
    t = -Bd * mu / m ** 2
    d = ajusta(t)
    s = eps_de(d)
    al = m / (mu * d)
    L = hc * d / m
    kap = np.sqrt(-2 * s["E"])
    sens = d * s["dEdd"] / s["E"]          # d ln|eps|/d ln delta = d ln B/d ln m_pi a g y mu fijos
    deu[k] = dict(delta=d, ratio=d / dc1, alpha=al, r_fm=s["r"] * L, rrms_fm=np.sqrt(s["r2"]) * L,
                  rstr_fm=np.sqrt(s["r2"]) * L / 2, kinv_fm=L / kap, mpic=m * dc1 / d, sens=sens,
                  B_chiral=mu * al ** 2 / 2)
    log(f"[d {k:8s}] delta_d = {d:.10f} ({d / dc1:.4f} dc), g/hc = {al:.6f}, <r> = {s['r'] * L:.4f},"
        f" rms = {np.sqrt(s['r2']) * L:.4f}, r_str = {np.sqrt(s['r2']) * L / 2:.4f}, 1/kappa = {L / kap:.4f} fm,"
        f" m_pi^c = {m * dc1 / d:.3f} MeV, dlnB/dlnm_pi (HF) = {sens:.5f}, B(m_pi->0) = {mu * al ** 2 / 2:.2f} MeV")
# rango efectivo del modelo en el polo (rho(-B,-B)): rho = 2 int (w^2 - u^2) dr, u ~ w = e^{-kappa r} asintotico
c = deu["promedio"]
# radio experimental
rd = sc.physical_constants["deuteron rms charge radius"]
rp = sc.physical_constants["proton rms charge radius"]
rn2, urn2 = -0.1161, 0.0022
DF = 0.75 * (hc / m_p) ** 2
rstr = np.sqrt(rd[0] ** 2 * 1e30 - rp[0] ** 2 * 1e30 - rn2 - DF)
u_ind = np.sqrt((rd[0] * rd[2] * 1e30) ** 2 + (rp[0] * rp[2] * 1e30) ** 2 + (urn2 / 2) ** 2) / rstr
u_sin_rp_rd = (urn2 / 2) / rstr   # si r_d^2 - r_p^2 se toma con su correlacion casi total (isotopico)
log(f"[d] r_str exp = {rstr:.5f} fm, u (independientes) = {u_ind:.5f}, u solo por r_n^2 = {u_sin_rp_rd:.5f};"
    f" Darwin-Foldy = {DF:.5f} fm^2; modelo/exp = {c['rstr_fm'] / rstr:.4f}; alcance cero = {c['kinv_fm'] / np.sqrt(8):.4f}")
# NPLQCD
mL, MB, BL, uBL = 805.9, 1634.0, 19.5, float(np.sqrt(3.6 ** 2 + 3.1 ** 2 + 0.2 ** 2))
muL = MB / 2
lat = {}
for et, Bv in (("central", BL), ("menos", BL - uBL), ("mas", BL + uBL)):
    d = ajusta(-Bv * muL / mL ** 2, 0.2, 1.15)
    lat[et] = dict(delta=d, alpha=mL / (muL * d))
d_gf = mL / (muL * c["alpha"])
d_gf_mufis = mL / (mu * c["alpha"])     # si ademas se mantuviera la masa reducida fisica
lat.update(delta_g_fisico=d_gf, delta_g_y_mu_fisicos=d_gf_mufis, cociente=lat["central"]["alpha"] / c["alpha"],
           uB=uBL)
log(f"[NPLQCD] delta_L = {lat['central']['delta']:.6f} ({lat['mas']['delta']:.4f} a {lat['menos']['delta']:.4f}),"
    f" g/hc = {lat['central']['alpha']:.4f}, cociente = {lat['cociente']:.4f}; delta con g fisico = {d_gf:.4f}"
    f" ({d_gf / dc1:.3f} dc); con g y mu fisicos = {d_gf_mufis:.4f}")
# Berengut
Kd, Kd_up, Kd_dn, Kpi, Kpi_up, Kpi_dn = -0.86, 0.45, 0.50, 0.494, 0.009, 0.013
ber = dict(cent=Kd / Kpi, rango_solo_Kd=((Kd - Kd_dn) / Kpi, (Kd + Kd_up) / Kpi),
           rango_ambos=((Kd - Kd_dn) / (Kpi - Kpi_dn), (Kd + Kd_up) / (Kpi + Kpi_up)))
log(f"[Berengut] K_d/K_pi = {ber['cent']:.4f}; rango por K_d: {ber['rango_solo_Kd'][0]:.3f} a {ber['rango_solo_Kd'][1]:.3f};"
    f" con K_pi tambien: {ber['rango_ambos'][0]:.3f} a {ber['rango_ambos'][1]:.3f};"
    f" cociente modelo/Berengut = {c['sens'] / ber['cent']:.3f}")
res["deuteron"] = dict(Bd=Bd, mu=mu, mpi=mpi, escenarios=deu, rstr=rstr, u_rstr_indep=u_ind, u_rstr_rn2=u_sin_rp_rd,
                       DF=DF, nplqcd=lat, berengut=ber, aumento_mpi=dc1 / c["delta"] - 1)
log(f"[d] aumento relativo de m_pi hasta desligar: {dc1 / c['delta'] - 1:.4%}")
res["t_s"] = time.perf_counter() - t0
log(f"tiempo {res['t_s']:.1f} s")
with open(os.path.join(AQUI, "r01_recalculo.json"), "w") as f:
    json.dump(res, f, indent=2, default=float)
with open(os.path.join(AQUI, "r01_recalculo_salida.txt"), "w") as f:
    f.write("\n".join(lineas) + "\n")
