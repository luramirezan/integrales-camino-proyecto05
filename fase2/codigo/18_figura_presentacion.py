"""18_figura_presentacion.py -- Primer grafico de la Fase 2 (presentacion de la semana 7).

Comparacion radial frente a tiempo imaginario en delta = 0.2 (punto fuertemente ligado):
  (a) E0: radial, transferencia (eps = 0.1 y extrapolada eps -> 0) y PIGS (tau = 20, 8 cadenas).
  (b) <r>: radial, transferencia (eps = 0.1, tau -> inf y estimador puro en tau = 20) y PIGS.
  (c) E_mixto(tau) desde u_T = r e^{-r} (no exacta): curva de la transferencia y PIGS con
      las dos replicas de tau = 5.

No calcula nada nuevo: solo LEE los JSON de los scripts 10, 11, 12, 12b y 12c (despues de V3)
y dibuja. No usa numeros aleatorios (semilla fijada por estilo). Guarda la figura en
fase2/figuras/18_primer_grafico.png y las cifras dibujadas en fase2/resultados/18_figura_presentacion.json.
Unidades hbar = m = g = 1, V = -e^{-delta r}/r.
"""
import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

np.random.seed(20262000)
BASE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
RES = os.path.join(BASE, "resultados")
FIG = os.path.join(BASE, "figuras")


def leer(nombre):
    with open(os.path.join(RES, nombre)) as f:
        return json.load(f)


j11 = leer("11_transferencia.json")
j12 = leer("12_pigs.json")
j12b = leer("12b_pigs_replica.json")
j12c = leer("12c_pigs_coulomb_tau5.json")

# Referencia radial fina (h = 1/80 y 1/160, R = 40), la de la seccion 11
rad = j11["referencia_radial"]["0.2"]
E_rad, r_rad = rad["E0"], rad["r_med"]

# Transferencia: eps = 0.1, h = 0.02 (tabla Richardson); y extrapolada eps -> 0 con Richardson en h
tr01 = j11["resultados"]["0.2"]["h=0.02,eps=0.1"]
E_tr01, r_tr01 = tr01["E_tablaRich"], tr01["r_med"]
E_tr_ext = j11["trotter"]["0.2"]["Richardson h^4 (0.02,0.04)"]["extrapolado"]

# Curva determinista E_mixto(tau) y <r> puro(tau), mismo eps = 0.1, Richardson en h (script 12)
det = j12["transferencia"]["0.2"]["Richardson h^4"]
taus = sorted(float(t) for t in det["tau"])
Emix_det = [det["tau"][k]["E_mixto"] for k in sorted(det["tau"], key=float)]
r_det20 = det["tau"]["20"]["r_puro"]

# PIGS produccion tau = 20 (8 cadenas)
p = j12["pigs"]["prod02"]
E_p, eE_p = p["EL"]["media"], p["EL"]["err"]
r_p, er_p = p["rmid"]["media"], p["rmid"]["err"]

# Barrido en tau (produccion) y replicas de tau = 5
scan = j12["tau_scan"]
rep = j12c["C_tau5_combinado"]["por_corrida"]
las40 = j12c["C_tau5_combinado"]["las_40"]

fig, ax = plt.subplots(1, 3, figsize=(15, 4.6))

# (a) energia, en unidades de 1e-5 respecto al radial
U = 1e5
nombres = ["radial", "transferencia\n$\\epsilon=0.1$", "transferencia\n$\\epsilon\\to0$", "PIGS $\\tau=20$\n(8 cadenas)"]
vals = [0.0, (E_tr01 - E_rad) * U, (E_tr_ext - E_rad) * U, (E_p - E_rad) * U]
errs = [0.0, 0.0, 0.0, eE_p * U]
cols = ["#1B2A41", "#2E86AB", "#2E86AB", "#C0392B"]
for i, (v, e, c) in enumerate(zip(vals, errs, cols)):
    ax[0].errorbar(i, v, yerr=e if e > 0 else None, fmt="o", color=c, ms=8, capsize=5, lw=1.8)
ax[0].axhline(0, color="#1B2A41", ls=":", lw=1)
ax[0].set_xticks(range(4))
ax[0].set_xticklabels(nombres, fontsize=9.5)
ax[0].set_ylabel("$(E - E_{\\rm radial})\\times10^{5}$")
ax[0].set_title("(a) Energía del 1s en $\\delta=0.2$")
ax[0].set_xlim(-0.5, 3.5)
ax[0].annotate(f"{(E_p - E_rad) / eE_p:+.2f}$\\sigma$", (3, (E_p - E_rad) * U), xytext=(-48, 0),
               textcoords="offset points", color="#C0392B", fontsize=10, va="center")

# (b) radio medio
nombres_b = ["radial", "transferencia\n$\\tau\\to\\infty$", "transferencia\npuro $\\tau=20$", "PIGS $\\tau=20$\n(8 cadenas)"]
vals_b = [r_rad, r_tr01, r_det20, r_p]
errs_b = [0.0, 0.0, 0.0, er_p]
for i, (v, e, c) in enumerate(zip(vals_b, errs_b, cols)):
    ax[1].errorbar(i, v, yerr=e if e > 0 else None, fmt="o", color=c, ms=8, capsize=5, lw=1.8)
ax[1].axhline(r_rad, color="#1B2A41", ls=":", lw=1)
ax[1].set_xticks(range(4))
ax[1].set_xticklabels(nombres_b, fontsize=9.5)
ax[1].set_ylabel("$\\langle r\\rangle$ (unidades de $a=\\hbar^2/mg$)")
ax[1].set_title("(b) Radio medio en $\\delta=0.2$")
ax[1].set_xlim(-0.5, 3.5)
ax[1].annotate(f"{(r_p - r_rad) / er_p:+.2f}$\\sigma$", (3, r_p), xytext=(-48, 0),
               textcoords="offset points", color="#C0392B", fontsize=10, va="center")

# (c) E_mixto(tau) desde u_T = r e^{-r}
U4 = 1e4
ax[2].plot(taus, (np.array(Emix_det) - E_rad) * U4, "-", color="#2E86AB", lw=2,
           label="transferencia (sin muestreo)")
ax[2].axhline(0, color="#1B2A41", ls=":", lw=1, label="radial $E_0$")
first = True
for s in scan:
    ax[2].errorbar(s["tau"], (s["E_pigs"] - E_rad) * U4, yerr=s["eE"] * U4, fmt="o", color="#C0392B",
                   ms=7, capsize=4, lw=1.6, label="PIGS producción (8 cadenas)" if first else None)
    first = False
for k, (nom, dx) in enumerate([("replica1", 0.45), ("replica2", 0.9)]):
    ax[2].errorbar(5 + dx, (rep[nom]["media"] - E_rad) * U4, yerr=rep[nom]["err"] * U4, fmt="s",
                   mfc="white", color="#C0392B", ms=6, capsize=4, lw=1.4,
                   label="PIGS réplicas $\\tau=5$ (16 + 16 cadenas)" if k == 0 else None)
ax[2].set_xlabel("duración de proyección $\\tau = M\\epsilon$ ($\\epsilon=0.1$)")
ax[2].set_ylabel("$(E_{\\rm mixto}(\\tau) - E_{\\rm radial})\\times10^{4}$")
ax[2].set_title("(c) Proyección desde $u_T = r\\,e^{-r}$ (no exacta)")
ax[2].legend(fontsize=8.5, loc="lower right")
ax[2].set_xlim(0, 31)

for a in ax:
    a.grid(alpha=0.25)
fig.tight_layout()
os.makedirs(FIG, exist_ok=True)
salida = os.path.join(FIG, "18_primer_grafico.png")
fig.savefig(salida, dpi=150)

datos = {
    "script": "18_figura_presentacion.py",
    "nota": "solo lee JSON de 11, 12, 12b, 12c; no calcula nada nuevo",
    "E_radial": E_rad, "r_radial": r_rad,
    "E_transferencia_eps0.1_h0.02": E_tr01, "dif_E_tr01": E_tr01 - E_rad,
    "E_transferencia_extrapolada": E_tr_ext, "dif_E_tr_ext": E_tr_ext - E_rad,
    "r_transferencia_eps0.1": r_tr01, "r_transferencia_puro_tau20": r_det20,
    "PIGS_tau20": {"E": E_p, "eE": eE_p, "sigma_vs_radial": (E_p - E_rad) / eE_p,
                   "r": r_p, "er": er_p, "sigma_r_vs_radial": (r_p - r_rad) / er_p},
    "Emixto_det": dict(zip([str(t) for t in taus], Emix_det)),
    "tau5": {"produccion": rep["produccion"], "replica1": rep["replica1"], "replica2": rep["replica2"],
             "las_40": las40},
    "j12b_las_16_E": j12b["replica"]["las_16"]["E"]["media"],
}
with open(os.path.join(RES, "18_figura_presentacion.json"), "w") as f:
    json.dump(datos, f, indent=1)

print("Figura:", salida)
print(f"E_radial = {E_rad:.12f}   <r>_radial = {r_rad:.10f}")
print(f"transferencia eps=0.1, h=0.02: E = {E_tr01:.12f} (dif {E_tr01 - E_rad:+.3e}); <r> = {r_tr01:.8f}")
print(f"transferencia extrapolada eps->0: E = {E_tr_ext:.12f} (dif {E_tr_ext - E_rad:+.3e})")
print(f"PIGS tau=20: E = {E_p:.6f} +- {eE_p:.6f} ({(E_p - E_rad) / eE_p:+.2f} sigma frente al radial fino)")
print(f"PIGS tau=20: <r> = {r_p:.5f} +- {er_p:.5f} ({(r_p - r_rad) / er_p:+.2f} sigma)")
for nom in ["produccion", "replica1", "replica2"]:
    print(f"tau=5 {nom}: {rep[nom]['media']:.6f} +- {rep[nom]['err']:.6f} ({rep[nom]['sigma']:+.2f} sigma frente a la transferencia)")
print(f"tau=5 las 40 cadenas: {las40['sigma_ponderada']:+.2f} sigma (ponderada)")
