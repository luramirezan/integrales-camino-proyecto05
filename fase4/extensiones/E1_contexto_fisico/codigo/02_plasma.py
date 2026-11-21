"""02_plasma.py -- hidrogeno en un plasma de Debye (modelo de Yukawa estatico).

Correspondencia: V(r) = -(e^2/4 pi eps0) e^{-r/lambda_D}/r. Con m = masa del termino cinetico y g = e^2/4 pi eps0,
L = hbar^2/(m g). Si m = m_e (nucleo infinito, como Rogers et al. 1970), L = a0 y delta = a0/lambda_D.
Con la masa reducida m_e m_p/(m_e+m_p), L = a0 (1 + m_e/m_p).

Longitud de Debye (NRL Plasma Formulary, Huba 2004, p. 29), solo electrones:
    lambda_De = (eps0 k T_e/(n_e e^2))^{1/2}  [SI]  = (kT/4 pi n e^2)^{1/2} [gaussiano] = 7.43e2 (T_eV/n_cm3)^{1/2} cm.
Variante con electrones y protones a la misma T (suma de inversas al cuadrado): lambda = lambda_De/sqrt(2).
La curva de "desaparicion del 1s" es lambda_D = L/delta_c:
    n_e(T) = eps0 k T delta_c^2/(e^2 L^2)    (solo electrones)
Indicadores de validez del modelo estatico de Debye-Huckel, evaluados SOBRE la curva:
    N_D = (4 pi/3) n_e lambda_D^3 (particulas en la esfera de Debye; DH requiere N_D >> 1),
    Gamma_e = e^2/(4 pi eps0 a_ws k T), a_ws = (3/(4 pi n_e))^{1/3} (acoplamiento; DH requiere Gamma << 1),
    Theta = k T/E_F, E_F = hbar^2 (3 pi^2 n_e)^{2/3}/(2 m_e) (degeneracion; DH clasico requiere Theta >> 1).
Ademas: energia del 1s, E(lambda_D), con los metodos A y B, en eV (unidad m g^2/hbar^2 = 1 Hartree).
Salida: resultados/02_plasma.json, figuras/02_plasma_diagrama.png, figuras/02_plasma_energia.png
"""
import time

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import comun_e1 as c

log = c.Registro()
t0 = time.perf_counter()
K = c.CONST
U1 = c.leer("01_umbral")
dc = U1["delta_c_1s"]["A"]

a0 = K["a0"]
me_mp = K["m_e"] / K["m_p"]
L_inf = a0
L_red = a0 * (1 + me_mp)
lam_c = L_inf / dc
lam_c_red = L_red / dc
log(f"delta_c = {dc:.13f}")
log(f"lambda_D critica (nucleo infinito)   = {lam_c / a0:.7f} a0 = {lam_c * 1e12:.4f} pm")
log(f"lambda_D critica (masa reducida)     = {lam_c_red / a0:.7f} a0")
log(f"Rogers, Graboske y Harwood 1970: D0(1s) = {K['rgh_D0']} a0/Z ; nuestro 1/delta_c = {1 / dc:.6f}")

# --- comprobacion de la formula NRL con constantes SI
e, eps0 = K["e"], K["eps0"]
kT1 = 1.0 * e                      # 1 eV en J
lam_1 = np.sqrt(eps0 * kT1 / (1e6 * e * e))   # n = 1 cm^-3 = 1e6 m^-3, en m
coef_cm = lam_1 * 100.0
log(f"coeficiente de Debye recalculado = {coef_cm:.4f} cm  (NRL: {K['nrl_coef_cm']})")

hbar = K["hbar_c"] * 1e6 * e * 1e-15 / 299792458.0      # J s, a partir de hbar c en MeV fm
me_kg = K["m_e"] * 1e6 * e / 299792458.0 ** 2


def n_crit(T_eV, especies="e"):
    """densidad electronica (m^-3) en la que lambda_D = lam_c, a temperatura T_eV."""
    fac = 1.0 if especies == "e" else 0.5
    return fac * eps0 * T_eV * e * dc ** 2 / (e * e * a0 ** 2)


def indicadores(n, T_eV, lam):
    ND = 4 * np.pi / 3 * n * lam ** 3
    aws = (3 / (4 * np.pi * n)) ** (1 / 3)
    Gam = e * e / (4 * np.pi * eps0 * aws * T_eV * e)
    EF = hbar ** 2 * (3 * np.pi ** 2 * n) ** (2 / 3) / (2 * me_kg) / e     # eV
    return ND, Gam, T_eV / EF, aws


Ts = np.logspace(-1, 4, 51)        # 0.1 eV a 10 keV
tab = []
for T in Ts:
    n = n_crit(T)
    ND, G, Th, aws = indicadores(n, T, lam_c)
    tab.append(dict(T_eV=float(T), n_e_m3=float(n), n_e_cm3=float(n * 1e-6), N_D=float(ND), Gamma=float(G),
                    Theta=float(Th), a_ws_sobre_lambdaD=float(aws / lam_c),
                    n_e_cm3_con_iones=float(n_crit(T, "ei") * 1e-6)))
puntos = {}
for T in (1.0, 13.6, 100.0, 1000.0):
    n = n_crit(T)
    ND, G, Th, aws = indicadores(n, T, lam_c)
    puntos[f"{T:g}"] = dict(T_eV=T, n_e_cm3=float(n * 1e-6), n_e_cm3_con_iones=float(n_crit(T, "ei") * 1e-6),
                            N_D=float(ND), Gamma=float(G), Theta=float(Th), a_ws_sobre_lambdaD=float(aws / lam_c))
    log(f"T = {T:7g} eV: n_e = {n * 1e-6:.3e} cm^-3 (con iones {n_crit(T, 'ei') * 1e-6:.3e}),"
        f" N_D = {ND:.3e}, Gamma = {G:.3f}, T/E_F = {Th:.3f}, a_ws/lambda_D = {aws / lam_c:.3f}")
# N_D sobre la curva es proporcional a T: temperatura en la que N_D = 1 y en la que N_D = 10
T_ND1 = float(1.0 / puntos["1"]["N_D"])
log(f"Sobre la curva N_D = {puntos['1']['N_D']:.4e} * (T/eV); N_D = 1 en T = {T_ND1:.1f} eV,"
    f" N_D = 10 en T = {10 * T_ND1:.0f} eV")

# --- energia del 1s frente a lambda_D (dos metodos), en eV
Eh = K["E_h_eV"]
deltas = [0.2, 0.4, 0.6, 0.8, 1.0, 1.1, 1.15, 1.18]
curva = []
for d in deltas:
    A = c.estado_1s_disparo(d)
    R = c.caja_para(A["E0"], Rmin=60.0, factor=30.0)
    B = c.estado_1s_caja(d, R)
    curva.append(dict(delta=d, lambda_D_a0=1 / d, E_A_hartree=A["E0"], E_B_hartree=B["E0"], R_caja=R,
                      dif_rel=abs(A["E0"] - B["E0"]) / abs(A["E0"]), E_A_eV=A["E0"] * Eh,
                      r_med_A=A["r_med"], r_med_B=B["r_med"]))
    log(f"delta = {d:5.2f} (lambda_D = {1 / d:6.3f} a0): E_A = {A['E0']:.10f} Ha, E_B = {B['E0']:.10f} Ha"
        f" (R = {R:g}), |dif|/|E| = {abs(A['E0'] - B['E0']) / abs(A['E0']):.1e}, E = {A['E0'] * Eh:.5f} eV")

out = dict(delta_c=dc, lambda_c_a0=lam_c / a0, lambda_c_red_a0=lam_c_red / a0, lambda_c_pm=lam_c * 1e12,
           rgh_D0=K["rgh_D0"], coef_NRL_recalculado_cm=coef_cm, coef_NRL=K["nrl_coef_cm"],
           n_crit_por_eV_cm3=float(n_crit(1.0) * 1e-6), T_ND1_eV=T_ND1, puntos=puntos, tabla=tab, curva_E=curva)

# --- figura 1: diagrama (n_e, T)
fig, ax = plt.subplots(figsize=(7.2, 5.4))
nn = np.logspace(18, 28, 300)          # cm^-3
TT = np.logspace(-1, 4, 300)           # eV
Ng, Tg = np.meshgrid(nn, TT)
lam = np.sqrt(eps0 * Tg * e / (Ng * 1e6 * e * e))
delta_g = a0 / lam
cs = ax.contour(Ng, Tg, delta_g, levels=[0.25, 0.5], colors="0.55", linewidths=0.8, linestyles=":")
ax.clabel(cs, fmt={0.25: "δ = 0.25", 0.5: "δ = 0.5"}, fontsize=8)
ax.fill_betweenx(TT, n_crit(TT) * 1e-6, 1e30, color="#d9534f", alpha=0.12)
ax.plot(n_crit(TT) * 1e-6, TT, color="#b52b27", lw=2.2,
        label=r"$\lambda_D = a_0/\delta_c = %.4f\,a_0$ (solo electrones)" % (lam_c / a0))
ax.plot(n_crit(TT, "ei") * 1e-6, TT, color="#b52b27", lw=1.2, ls="--",
        label=r"misma condición con electrones y protones ($\lambda_D/\sqrt{2}$)")
# lineas de validez
Gam1_T = e * e / (4 * np.pi * eps0 * (3 / (4 * np.pi * nn * 1e6)) ** (1 / 3)) / e     # Gamma = 1
EF_n = hbar ** 2 * (3 * np.pi ** 2 * nn * 1e6) ** (2 / 3) / (2 * me_kg) / e
ax.plot(nn, Gam1_T, color="#1f5aa6", lw=1.3, label=r"$\Gamma_e = 1$ (acoplamiento)")
ax.plot(nn, EF_n, color="#2e8b57", lw=1.3, label=r"$k_BT = E_F$ (degeneración)")
ND1_T = (1.0 / (4 * np.pi / 3 * (nn * 1e6) * (eps0 / (nn * 1e6 * e * e)) ** 1.5 * e ** 1.5)) ** (2 / 3)
ax.plot(nn, ND1_T, color="#8a5a00", lw=1.3, ls="-.", label=r"$N_D = 1$ (esfera de Debye)")
ax.axhline(13.6057, color="0.3", lw=0.8, ls=":")
ax.text(2e18, 15.5, "13.6 eV", fontsize=8, color="0.3")
ax.text(3e18, 0.2, "1s ligado en el modelo estático\n(λ_D > a0/δ_c)", fontsize=9)
ax.text(4e25, 0.2, "sin 1s en el\nmodelo estático", fontsize=9, color="#b52b27")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(1e18, 1e28); ax.set_ylim(0.1, 1e4)
ax.set_xlabel(r"densidad electrónica $n_e$ (cm$^{-3}$)")
ax.set_ylabel(r"temperatura $k_BT$ (eV)")
ax.set_title("Hidrógeno en un plasma de Debye: dónde desaparece el 1s (Yukawa estático)", fontsize=10)
ax.legend(fontsize=7.5, loc="upper left")
ax.grid(alpha=0.25, which="both", lw=0.4)
fig.tight_layout()
fig.savefig(c.os.path.join(c.FIG, "02_plasma_diagrama.png"), dpi=150)
plt.close(fig)

# --- figura 2: E_1s frente a lambda_D
fig, ax = plt.subplots(figsize=(6.2, 4.2))
dd = np.array([x["delta"] for x in curva])
ax.plot(1 / dd, [x["E_A_eV"] for x in curva], "o-", color="#1f5aa6", label="disparo sin caja (A)")
ax.plot(1 / dd, [x["E_B_hartree"] * Eh for x in curva], "x", ms=9, color="#d9534f", label="caja + Richardson (B)")
ax.axvline(lam_c / a0, color="0.3", ls="--", lw=1)
ax.text(lam_c / a0 * 1.03, -10, r"$a_0/\delta_c$", fontsize=9)
ax.axhline(0, color="0.5", lw=0.6)
ax.set_xscale("log")
ax.set_xlabel(r"longitud de Debye $\lambda_D/a_0$")
ax.set_ylabel(r"energía del 1s (eV)")
ax.set_title("Energía del 1s en el modelo estático (masa $m_e$, núcleo infinito)", fontsize=10)
ax.legend(fontsize=8)
ax.grid(alpha=0.3, lw=0.4)
fig.tight_layout()
fig.savefig(c.os.path.join(c.FIG, "02_plasma_energia.png"), dpi=150)
plt.close(fig)

# --- controles (criterios fijados antes de correr)
ctl = [dict(id="C5", control="Formula de Debye en SI frente al coeficiente del NRL Plasma Formulary",
            criterio="|coef/743 - 1| < 1e-3", valor=f"{coef_cm:.3f} cm (rel {coef_cm / 743 - 1:.1e})",
            pasa=bool(abs(coef_cm / 743 - 1) < 1e-3)),
       dict(id="C6", control="Longitud critica frente a Rogers, Graboske y Harwood 1970 (D0 = 0.83991 a0)",
            criterio="|1/delta_c - 0.83991| < 5e-6 (ultima cifra publicada)",
            valor=f"{1 / dc:.7f}", pasa=bool(abs(1 / dc - K["rgh_D0"]) < 5e-6)),
       dict(id="C7", control="Energia del 1s en 8 valores de delta: disparo (A) frente a caja (B)",
            criterio="max |E_A - E_B|/|E_A| < 1e-6",
            valor=f"{max(x['dif_rel'] for x in curva):.1e}",
            pasa=bool(max(x["dif_rel"] for x in curva) < 1e-6))]
out["controles"] = ctl
for k in ctl:
    log(k["id"], k["control"], "|", k["valor"], "|", "pasa" if k["pasa"] else "NO PASA")
out["t_s"] = time.perf_counter() - t0
log(f"tiempo {out['t_s']:.1f} s")
c.guardar("02_plasma", out, log.texto())
