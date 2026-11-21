"""05_mapa.py -- figura "mapa": delta en funcion del parametro fisico en los tres sistemas, con la banda delta_c.

Lee 01_umbral.json, 02_plasma.json, 03_materia_oscura.json y 04_deuteron.json; no recalcula autovalores.
Panel 1: plasma, delta = a0/lambda_D = a0 (n_e e^2/(eps0 k T))^{1/2} frente a n_e, para T = 1, 10, 100 eV.
Panel 2: materia oscura, delta = 2 m_phi/(alpha m_chi) frente a m_chi, para m_phi = 10 MeV y alpha = 0.01, 0.1;
         se marcan los umbrales de Hulthen (b = 1.6 y b = pi^2/6) como referencia de la aproximacion.
Panel 3: deuteron de juguete, delta = m_pi/(mu alpha_g) frente a m_pi con g fijo (escenario A), el punto fisico y el
         punto de NPLQCD con g fisico (no ligado) y con g reajustado (barra de error por la de B_d).
Salida: figuras/05_mapa_delta.png, resultados/05_mapa.json
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import comun_e1 as c

log = c.Registro()
K = c.CONST
U1, P, D, N = (c.leer(x) for x in ("01_umbral", "02_plasma", "03_materia_oscura", "04_deuteron"))
dc = U1["delta_c_1s"]["A"]
dc2 = U1["delta_c_2s"]["A"]

fig, axs = plt.subplots(1, 3, figsize=(13.0, 4.6), sharey=True)
ymax = 3.0
for ax in axs:
    ax.axhspan(dc, ymax, color="#d9534f", alpha=0.10)
    ax.axhline(dc, color="#b52b27", lw=1.8)
    ax.axhline(dc2, color="0.45", lw=0.9, ls=":")
    ax.set_ylim(0, ymax)
    ax.grid(alpha=0.25, lw=0.4, which="both")
axs[0].text(1.3e21, dc2 + 0.05, r"$\delta_c(2s) = %.4f$" % dc2, fontsize=8, color="0.35")

# panel 1: plasma
e, eps0, a0 = K["e"], K["eps0"], K["a0"]
n = np.logspace(21, 26, 200)        # cm^-3
for T, col in ((1.0, "#1f5aa6"), (10.0, "#2e8b57"), (100.0, "#8a5a00")):
    d = a0 * np.sqrt(n * 1e6 * e * e / (eps0 * T * e))
    axs[0].plot(n, d, color=col, lw=1.6, label=f"$k_BT$ = {T:g} eV")
axs[0].set_xscale("log")
axs[0].set_xlabel(r"$n_e$ (cm$^{-3}$)")
axs[0].set_ylabel(r"$\delta = \mu\hbar^2/(m g)$")
axs[0].set_title(r"Plasma: $\delta = a_0/\lambda_D$ (solo electrones)", fontsize=10)
axs[0].legend(fontsize=8, loc="center left")

# panel 2: materia oscura
mchi = np.logspace(-1, 2.5, 200)    # GeV
mphi = 10.0e-3                      # GeV
for alpha, col in ((0.01, "#1f5aa6"), (0.1, "#2e8b57")):
    axs[1].plot(mchi, 2 * mphi / (alpha * mchi), color=col, lw=1.6, label=rf"$\alpha$ = {alpha:g}, $m_\phi$ = 10 MeV")
axs[1].axhline(2 / K["tyz_kappa_hulthen"], color="0.2", lw=0.8, ls="--")
axs[1].axhline(2 / (np.pi ** 2 / 6), color="0.2", lw=0.8, ls="-.")
axs[1].text(0.12, 2 / K["tyz_kappa_hulthen"] + 0.04, "Hulthén, κ = 1.6", fontsize=7.5)
axs[1].text(0.12, 2 / (np.pi ** 2 / 6) - 0.13, "Hulthén, κ = π²/6", fontsize=7.5)
axs[1].set_xscale("log")
axs[1].set_xlabel(r"$m_\chi$ (GeV)")
axs[1].set_title(r"Materia oscura: $\delta = 2m_\phi/(\alpha m_\chi)$", fontsize=10)
axs[1].legend(fontsize=8, loc="upper right")

# panel 3: deuteron
A = N["escenario_A"]["promedio"]
mu, alpha_f = N["mu"], A["alpha_g"]
mpi = np.linspace(30, 900, 300)
axs[2].plot(mpi, mpi / (mu * alpha_f), color="#1f5aa6", lw=1.6, label=r"$g$ y $\mu$ fijos (físicos)")
mp_f = N["m_pi"]["promedio"]
axs[2].plot([mp_f], [A["delta_A"]], "o", color="k", ms=6, label="punto físico (ajustado a $B_d$)")
L = N["escenario_B_red"]
axs[2].plot([K["lat_m_pi"]], [L["delta_con_g_fisico"]], "s", mfc="none", mec="#b52b27", ms=7,
            label="NPLQCD con $g$ físico (no ligado)")
yerr = [[L["central"]["delta_A"] - L["B+1sigma"]["delta_A"]], [L["B-1sigma"]["delta_A"] - L["central"]["delta_A"]]]
axs[2].errorbar([K["lat_m_pi"]], [L["central"]["delta_A"]], yerr=yerr, fmt="D", color="#b52b27", ms=6, capsize=3,
                label=r"NPLQCD con $g$ reajustado ($\times$%.2f)" % L["cociente_g"])
axs[2].axvline(A["m_pi_crit_g_fijo"], color="0.4", lw=0.8, ls="--")
axs[2].text(A["m_pi_crit_g_fijo"] + 12, 0.10, r"$m_\pi^{c}$ = %.0f MeV" % A["m_pi_crit_g_fijo"], fontsize=8)
axs[2].text(470, dc + 0.05, r"$\delta_c(1s) = %.7f$" % dc, fontsize=8, color="#b52b27")
axs[2].set_xlabel(r"$m_\pi$ (MeV)")
axs[2].set_title(r"Deuterón de juguete: $\delta = m_\pi/(\mu\,g/\hbar c)$", fontsize=10)
axs[2].legend(fontsize=7.2, loc="upper left")
fig.suptitle("El mismo umbral en tres sistemas: hay estado 1s solo por debajo de la línea roja", fontsize=11)
fig.tight_layout()
fig.savefig(c.os.path.join(c.FIG, "05_mapa_delta.png"), dpi=150)
plt.close(fig)
out = dict(delta_c=dc, delta_c_2s=dc2, m_phi_GeV=mphi, figura="figuras/05_mapa_delta.png")
log("figura escrita: figuras/05_mapa_delta.png")
c.guardar("05_mapa", out, log.texto())
