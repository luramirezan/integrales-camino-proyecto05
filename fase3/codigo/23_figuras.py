"""23_figuras.py -- Proyecto 05, Fase 3: figuras con barras de error a partir de los JSON 20, 20b, 20c, 21 y 22.
No calcula nada nuevo. Salida: fase3/figuras/23_barrido_delta.png, 23_cajas.png, 23_convergencia.png."""
import json, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comun3 as c  # noqa: E402

L = lambda n: json.load(open(os.path.join(c.RES3, n)))
B, CJ, CV = L("21_barrido.json"), L("20_cajas.json"), L("22_convergencia.json")
B119 = L("20b_umbral_119.json")
F119 = L("20c_umbral_119_fino.json") if os.path.exists(os.path.join(c.RES3, "20c_umbral_119_fino.json")) else None
plt.rcParams.update({"font.size": 10})

# ------------------------------------------------------------ 1. barrido en delta
P = B["puntos"]; dc = B["delta_c_ref"]
fig, ax = plt.subplots(1, 3, figsize=(15, 4.4))
dr = np.array([p["delta"] for p in P]); Er = np.array([p["radial"]["E0"] for p in P])
rr = np.array([p["radial"]["r_med"] for p in P]); kap = np.array([p["kappa"] for p in P])
T = [p for p in P if "tr" in p]
dt = np.array([p["delta"] for p in T]); Et = np.array([p["tr"]["E_mejor"] for p in T]); eEt = np.array([p["tr"]["err"] for p in T])
rt = np.array([p["tr"]["obs"]["r_med"]["mejor"] for p in T]); ert = np.array([p["tr"]["obs"]["r_med"]["err"] for p in T])
ins = np.array([p.get("caja_insuficiente", False) for p in T])
ax[0].plot(dr, Er, "-", color="tab:blue", label="radial (caja $R\\geq25/\\kappa$)")
ax[0].errorbar(dt[~ins], Et[~ins], yerr=eEt[~ins], fmt="o", mfc="none", color="tab:orange", capsize=3,
               label="integral de camino (transferencia extrapolada)")
ax[0].errorbar(dt[ins], Et[ins], yerr=eEt[ins], fmt="s", mfc="none", color="tab:red", capsize=3,
               label="idem, caja insuficiente (R = 3200)")
ax[0].axvline(dc, color="k", ls=":", lw=0.8); ax[0].axhline(0, color="k", lw=0.5)
ax[0].set_yscale("symlog", linthresh=1e-6); ax[0].set_xlabel("$\\delta=\\mu\\hbar^2/(mg)$"); ax[0].set_ylabel("$E_0$ ($mg^2/\\hbar^2$)")
ax[0].set_title("(a) Energía del estado fundamental"); ax[0].legend(fontsize=7.5, loc="upper left")
ax[1].plot(dr, rr, "-", color="tab:blue", label="radial")
ax[1].errorbar(dt[~ins], rt[~ins], yerr=ert[~ins], fmt="o", mfc="none", color="tab:orange", capsize=3, label="transferencia")
ax[1].plot(dr, 1 / (2 * kap), "--", color="gray", lw=0.9, label="$1/(2\\kappa)$ (cola $e^{-\\kappa r}$)")
ax[1].axvline(dc, color="k", ls=":", lw=0.8); ax[1].set_yscale("log")
ax[1].set_xlabel("$\\delta$"); ax[1].set_ylabel("$\\langle r\\rangle$ ($\\hbar^2/mg$)"); ax[1].set_title("(b) Extensión radial")
ax[1].legend(fontsize=7.5)
x = dc - dr
A, Bq = B["ajuste_kappa"]["A"], B["ajuste_kappa"]["B"]
xs = np.logspace(-4, np.log10(1.1), 100)
ax[2].loglog(x, kap, "o", color="tab:blue", label="radial")
ax[2].loglog(xs, A * xs + Bq * xs**2, "-", color="tab:green", lw=0.9, label=f"$\\kappa={A:.3f}\\,\\Delta{Bq:+.3f}\\,\\Delta^2$ (ajuste $\\delta\\geq1.15$)")
ax[2].set_xlabel("$\\Delta=\\delta_c-\\delta$"); ax[2].set_ylabel("$\\kappa=\\sqrt{-2E_0}$"); ax[2].set_title("(c) Cerca del umbral: $\\kappa\\propto\\Delta$")
ax[2].legend(fontsize=7.5)
fig.suptitle("Fase 3 · barrido en el apantallamiento (g fijo)")
fig.tight_layout(); fig.savefig(os.path.join(c.FIG3, "23_barrido_delta.png"), dpi=150); plt.close(fig)

# ------------------------------------------------------------ 2. cajas
col = {"1.15": "tab:blue", "1.18": "tab:green", "1.19": "tab:purple", "1.2": "tab:red", "1.25": "tab:brown"}
fig, ax = plt.subplots(1, 3, figsize=(15, 4.6))
for k, C in CJ["celdas"].items():
    Rs = sorted(int(r[1:]) for r in C)
    Erad = [C[f"R{R}"]["radial"]["E0"] for R in Rs]
    Etr = [C[f"R{R}"]["E_mejor"] for R in Rs]; eEtr = [C[f"R{R}"]["err"] for R in Rs]
    ax[0].plot(Rs, Erad, "-", color=col[k], label=f"δ={k}")
    ax[0].errorbar(Rs, Etr, yerr=eEtr, fmt="o", mfc="none", color=col[k], capsize=2)
    for j, q in ((1, "r_sobre_R"), (2, "F12")):
        ax[j].plot(Rs, [C[f"R{R}"]["radial"][q] for R in Rs], "-", color=col[k], label=f"δ={k}")
        ax[j].errorbar(Rs, [C[f"R{R}"]["obs"][q]["mejor"] for R in Rs], yerr=[C[f"R{R}"]["obs"][q]["err"] for R in Rs],
                       fmt="o", mfc="none", color=col[k], capsize=2)
ext = F119["radial"] if F119 else B119["radial"]
Rx = sorted(int(r[1:]) for r in ext)
ax[0].plot(Rx, [ext[f"R{R}"]["E0"] for R in Rx], "--", color=col["1.19"], lw=1, label="δ=1.19 radial, R hasta 25600")
ax[1].plot(Rx, [ext[f"R{R}"]["r_sobre_R"] for R in Rx], "--", color=col["1.19"], lw=1)
ax[2].plot(Rx, [min(ext[f"R{R}"]["F12"], 1.0) for R in Rx], "--", color=col["1.19"], lw=1)
ax[0].set_yscale("symlog", linthresh=1e-7); ax[0].axhline(0, color="k", lw=0.6)
ax[0].set_ylabel("$E_0(R)$"); ax[0].set_title("(a) Energía más baja en la caja")
ax[1].axhline(0.5, color="k", ls=":", lw=0.8); ax[1].set_ylabel("$\\langle r\\rangle/R$"); ax[1].set_title("(b) Tamaño relativo a la caja")
ax[2].axhline(0.5, color="k", ls=":", lw=0.8); ax[2].set_ylabel("$F_{1/2}$"); ax[2].set_title("(c) Fracción en la mitad interior")
for a in ax:
    a.set_xscale("log"); a.set_xlabel("radio de la caja $R$")
ax[0].legend(fontsize=7, loc="center right", framealpha=0.9)
fig.suptitle("Fase 3 · criterio de cajas: radial (líneas) e integral de camino (círculos con barras)")
fig.tight_layout(); fig.savefig(os.path.join(c.FIG3, "23_cajas.png"), dpi=150); plt.close(fig)

# ------------------------------------------------------------ 3. convergencia
fig, ax = plt.subplots(1, 2, figsize=(11, 4.4))
cc = {"0.2": "tab:blue", "0.8": "tab:green", "1": "tab:orange", "1.15": "tab:red"}
for k, X in CV["casos"].items():
    es = sorted(float(e) for e in X["E_hRich"])
    absE = abs(X["E_radial"])
    y = [abs(X["E_hRich"][f"{e:g}"] - X["E_ext"]) / absE for e in es]
    ax[0].loglog(es, y, "o-", color=cc[k], label=f"δ={k} (orden {X['orden_trotter'][0]:.2f})")
    hs = (0.04, 0.02)
    ym = [abs(X["E"][f"h{h:g}_eps0.05"] - X["E_hRich"]["0.05"]) / absE for h in hs]
    ax[1].loglog(hs, ym, "s-", color=cc[k], label=f"δ={k} (orden {X['orden_malla']['0.05']:.2f})")
e_ = np.array([0.025, 0.2]); ax[0].loglog(e_, 1e-3 * (e_ / 0.2)**2, "k:", lw=0.8, label="pendiente 2")
h_ = np.array([0.02, 0.04]); ax[1].loglog(h_, 1e-6 * (h_ / 0.04)**4, "k:", lw=0.8, label="pendiente 4")
ax[0].set_xlabel("paso de tiempo imaginario $\\epsilon$"); ax[0].set_ylabel("$|E(\\epsilon)-E_{\\epsilon\\to0}|/|E_0|$")
ax[0].set_title("(a) Sesgo de Trotter (Richardson en h)"); ax[0].legend(fontsize=7.5)
ax[1].set_xlabel("malla $h$"); ax[1].set_ylabel("$|E(h)-E_{h\\to0}|/|E_0|$ ($\\epsilon=0.05$)")
ax[1].set_title("(b) Error de malla Nyström"); ax[1].legend(fontsize=7.5)
fig.suptitle("Fase 3 · convergencia temporal y espacial")
fig.tight_layout(); fig.savefig(os.path.join(c.FIG3, "23_convergencia.png"), dpi=150); plt.close(fig)
print("figuras escritas")

# ------------------------------------------------------------ 4. delta = 1.19 (autovalor cercano a cero)
fig, ax = plt.subplots(1, 3, figsize=(15, 4.3))
C = CJ["celdas"]["1.19"]; Rs = sorted(int(r[1:]) for r in C)
fin = F119["radial"]; Rf = sorted(int(r[1:]) for r in fin)
ax[0].plot(Rs, [C[f"R{R}"]["radial"]["E0"] for R in Rs], "-", color="tab:purple", label="radial, h = 1/40")
ax[0].plot(Rf, [fin[f"R{R}"]["E0"] for R in Rf], "s--", color="tab:purple", mfc="white", label="radial, h = 1/160")
ax[0].errorbar(Rs, [C[f"R{R}"]["E_mejor"] for R in Rs], yerr=[C[f"R{R}"]["err"] for R in Rs], fmt="o", color="tab:orange",
               capsize=3, label="integral de camino (extrapolada)")
TG = L("26_transferencia_grande.json")["celdas"]; Rg = sorted(int(r[1:]) for r in TG)
ax[0].errorbar(Rg, [TG[f"R{R}"]["E_mejor"] for R in Rg], yerr=[TG[f"R{R}"]["err"] for R in Rg], fmt="D", color="tab:red",
               capsize=3, label="integral de camino, LU en banda")
ax[0].set_yscale("symlog", linthresh=1e-8); ax[0].axhline(0, color="k", lw=0.7)
ax[0].set_ylabel("$E_0(R)$"); ax[0].set_title("(a) El signo cambia entre R = 1600 y 3200"); ax[0].legend(fontsize=8)
for j, (q, t) in enumerate((("r_sobre_R", "(b) $\\langle r\\rangle/R$"), ("F12", "(c) $F_{1/2}$")), 1):
    ax[j].plot(Rs, [C[f"R{R}"]["radial"][q] for R in Rs], "-", color="tab:purple")
    ax[j].plot(Rf, [min(fin[f"R{R}"][q], 1.0) for R in Rf], "s--", color="tab:purple", mfc="white")
    ax[j].errorbar(Rs, [C[f"R{R}"]["obs"][q]["mejor"] for R in Rs], yerr=[C[f"R{R}"]["obs"][q]["err"] for R in Rs], fmt="o",
                   color="tab:orange", capsize=3)
    ax[j].errorbar(Rg, [TG[f"R{R}"]["obs"][q]["mejor"] for R in Rg], yerr=[TG[f"R{R}"]["obs"][q]["err"] for R in Rg], fmt="D",
                   color="tab:red", capsize=3)
    ax[j].set_title(t)
ax[2].axhline(0.95, color="k", ls=":", lw=0.8)
for a in ax:
    a.set_xscale("log"); a.set_xlabel("radio de la caja $R$"); a.axvline(F119["a_s"], color="gray", ls=":", lw=0.8)
ax[1].text(F119["a_s"] * 1.08, 0.27, "$a_s=+2204$", fontsize=8, color="gray")
fig.suptitle("δ = 1.19 (a 6×10⁻⁴ del umbral): estado ligado débil, no artefacto de caja")
fig.tight_layout(); fig.savefig(os.path.join(c.FIG3, "23_delta119.png"), dpi=150); plt.close(fig)
print("figura 1.19")
