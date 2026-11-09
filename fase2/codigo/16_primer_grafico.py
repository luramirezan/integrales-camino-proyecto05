#!/usr/bin/env python3
"""16_primer_grafico.py - Primer grafico de la Fase 2 (figura congelada de la primera exposicion).

Punto fuertemente ligado delta = 0.2 (V = -e^{-delta r}/r, hbar = m = g = 1):
  (a) E - E_radial frente a eps: transferencia (Richardson h^4, eps = 0.2/0.1/0.05 y extrapolada
      eps -> 0), mixto determinista tau = 20 y PIGS (mixto, tau = 20, eps = 0.1) con su barra de error.
  (b) <r> y (c) <r^2>: radial, transferencia (autovector, h = 0.02), puro determinista tau = 20 y
      PIGS (puro, tau = 20) con barras de error.
  (d) E_mixto(tau) - E_radial: curva determinista (transferencia, eps = 0.1) y PIGS en tau = 2, 5, 10, 20,
      mas las dos replicas de tau = 5.

No calcula nada nuevo: lee los JSON de los scripts 11, 12, 12b y 12c (ejecutados el 27-10-2026) y la
referencia radial fina del script 11 (h = 1/80, 1/160, R = 40). No usa numeros aleatorios.
Guarda la figura en fase2/figuras/16_primer_grafico.png (150 dpi) y las cifras graficadas, mas el sha256
de todas las figuras de fase2/figuras y de su script, en fase2/resultados/16_primer_grafico.json.
"""
import hashlib
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(AQUI)
RES = os.path.join(BASE, "resultados")
FIG = os.path.join(BASE, "figuras")

# Colores: paleta categorica de referencia (slots 1-3 en orden fijo) y gris neutro para la referencia.
C_TR = "#2a78d6"     # transferencia (determinista)
C_PIGS = "#eb6834"   # PIGS de produccion
C_REP = "#1baf7a"    # replicas de tau = 5
C_RAD = "#444441"    # radial (referencia)


def leer(nombre):
    with open(os.path.join(RES, nombre)) as f:
        return json.load(f)


def sha256(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 16), b""):
            h.update(bloque)
    return h.hexdigest()


j11 = leer("11_transferencia.json")
j12 = leer("12_pigs.json")
j12b = leer("12b_pigs_replica.json")
j12c = leer("12c_pigs_coulomb_tau5.json")

# ---------------- referencia radial (h = 1/80, 1/160, R = 40) ----------------
rad = j11["referencia_radial"]["0.2"]
E_rad, r_rad, r2_rad = rad["E0"], rad["r_med"], rad["r2_med"]

# ---------------- transferencia frente a eps ----------------
eps_l = [0.2, 0.1, 0.05]
tro = j11["trotter"]["0.2"]["Richardson h^4 (0.02,0.04)"]
E_tr = tro["E"]
E_tr_ext = tro["extrapolado"]
orden_tr = tro["orden"]
res02 = j11["resultados"]["0.2"]
r_tr = [res02["h=0.02,eps=%s" % e]["r_med"] for e in eps_l]
r2_tr = [res02["h=0.02,eps=%s" % e]["r2_med"] for e in eps_l]

# curva determinista con el mismo eps = 0.1 que el PIGS (Richardson h^4)
det = j12["transferencia"]["0.2"]["Richardson h^4"]
taus_det = sorted(det["tau"].keys(), key=float)
tau_det = [float(t) for t in taus_det]
Emix_det = [det["tau"][t]["E_mixto"] for t in taus_det]
r_puro20 = det["tau"]["20"]["r_puro"]
r2_puro20 = det["tau"]["20"]["r2_puro"]
Emix20 = det["tau"]["20"]["E_mixto"]

# ---------------- PIGS ----------------
p = j12["pigs"]["prod02"]
E_p, eE_p = p["EL"]["media"], p["EL"]["err"]
r_p, er_p = p["rmid"]["media"], p["rmid"]["err"]
r2_p, er2_p = p["r2mid"]["media"], p["r2mid"]["err"]
scan = j12["tau_scan"]
comb = j12c["C_tau5_combinado"]["por_corrida"]
rep1 = comb["replica1"]
rep2 = comb["replica2"]

# ---------------- figura ----------------
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": "#e4e3dc", "grid.linewidth": 0.6})
fig, ax = plt.subplots(2, 2, figsize=(11.5, 8.6))
U = 1e-5

# (a) energia
a = ax[0, 0]
a.axhline(0.0, color=C_RAD, lw=1.6, label="radial (dif. finitas, Richardson)")
a.plot(eps_l, [(e - E_rad) / U for e in E_tr], "o-", color=C_TR, lw=2, ms=8,
       label="transferencia (Richardson en h)")
a.plot([0.0], [(E_tr_ext - E_rad) / U], "s", color=C_TR, ms=9, mfc="white", mew=2,
       label=r"transferencia extrapolada $\epsilon\to0$")
a.plot([0.1], [(Emix20 - E_rad) / U], "D", color=C_TR, ms=8, mfc="white", mew=2,
       label=r"mixto determinista, $\tau=20$")
a.errorbar([0.112], [(E_p - E_rad) / U], yerr=[eE_p / U], fmt="o", color=C_PIGS, ms=8, capsize=4, lw=1.6,
           label=r"PIGS (mixto, $\tau=20$, 8 cadenas)")
a.set_xlabel(r"paso de tiempo imaginario $\epsilon$")
a.set_ylabel(r"$E-E_{\rm radial}$  [$10^{-5}$]")
a.set_title(r"(a) Energía del 1s, $\delta=0.2$", loc="left")
a.set_xlim(-0.015, 0.215)
a.legend(fontsize=8, loc="upper left", frameon=False)
a.text(0.60, 0.12, "transferencia:\n|E - E_radial| <= %.1e en los tres eps\n(invisible a esta escala)\nextrapolada eps->0: %+.1e"
       % (max(abs(e - E_rad) for e in E_tr), E_tr_ext - E_rad), transform=a.transAxes, fontsize=8, color="#444441")
a.set_ylim(-1.5, 22)

# (b) <r>
b = ax[0, 1]
b.axhline(r_rad, color=C_RAD, lw=1.6, label="radial")
b.plot(eps_l, r_tr, "o-", color=C_TR, lw=2, ms=8, label="transferencia (autovector, h=0.02)")
b.plot([0.1], [r_puro20], "D", color=C_TR, ms=8, mfc="white", mew=2, label=r"puro determinista, $\tau=20$")
b.errorbar([0.112], [r_p], yerr=[er_p], fmt="o", color=C_PIGS, ms=8, capsize=4, lw=1.6,
           label=r"PIGS (puro, $\tau=20$)")
b.set_xlabel(r"paso de tiempo imaginario $\epsilon$")
b.set_ylabel(r"$\langle r\rangle$  [unidades de $a=\hbar^2/mg$]")
b.set_title(r"(b) Radio medio $\langle r\rangle$", loc="left")
b.set_xlim(-0.015, 0.215)
b.legend(fontsize=8, loc="upper left", frameon=False)
b.set_ylim(1.545, 1.5725)

# (c) <r^2>
c = ax[1, 0]
c.axhline(r2_rad, color=C_RAD, lw=1.6, label="radial")
c.plot(eps_l, r2_tr, "o-", color=C_TR, lw=2, ms=8, label="transferencia (autovector, h=0.02)")
c.plot([0.1], [r2_puro20], "D", color=C_TR, ms=8, mfc="white", mew=2, label=r"puro determinista, $\tau=20$")
c.errorbar([0.112], [r2_p], yerr=[er2_p], fmt="o", color=C_PIGS, ms=8, capsize=4, lw=1.6,
           label=r"PIGS (puro, $\tau=20$)")
c.set_xlabel(r"paso de tiempo imaginario $\epsilon$")
c.set_ylabel(r"$\langle r^2\rangle$  [$a^2$]")
c.set_title(r"(c) Segundo momento $\langle r^2\rangle$", loc="left")
c.set_xlim(-0.015, 0.215)
c.legend(fontsize=8, loc="upper left", frameon=False)
c.set_ylim(3.195, 3.335)

# (d) proyeccion
d = ax[1, 1]
U4 = 1e-4
d.axhline(0.0, color=C_RAD, lw=1.6, label="radial")
d.plot(tau_det, [(e - E_rad) / U4 for e in Emix_det], "-", color=C_TR, lw=2,
       label=r"$E_{\rm mixto}(\tau)$ determinista ($\epsilon=0.1$)")
d.errorbar([s["tau"] for s in scan], [(s["E_pigs"] - E_rad) / U4 for s in scan],
           yerr=[s["eE"] / U4 for s in scan], fmt="o", color=C_PIGS, ms=8, capsize=4, lw=1.6,
           label="PIGS, producción (8 cadenas por punto)")
d.errorbar([5.5, 6.0], [(rep1["media"] - E_rad) / U4, (rep2["media"] - E_rad) / U4],
           yerr=[rep1["err"] / U4, rep2["err"] / U4], fmt="^", color=C_REP, ms=8, capsize=4, lw=1.6,
           label=r"PIGS, réplicas 1 y 2 de $\tau=5$ (16 cadenas c/u)")
d.set_xlabel(r"duración de la proyección $\tau$")
d.set_ylabel(r"$E_{\rm mixto}-E_{\rm radial}$  [$10^{-4}$]")
d.set_title(r"(d) Proyección desde $u_T=r\,e^{-r}$", loc="left")
d.legend(fontsize=8, loc="lower right", frameon=False)

fig.suptitle(r"Fase 2, primer gráfico: $\delta=0.2$, radial frente a transferencia y PIGS (misma acción de pares)",
             fontsize=11.5)
fig.tight_layout(rect=(0, 0, 1, 0.96))
ruta_fig = os.path.join(FIG, "16_primer_grafico.png")
fig.savefig(ruta_fig, dpi=150)
plt.close(fig)

# ---------------- cifras ----------------
print("Referencia radial (R=40, h=1/80,1/160): E0 = %.10f, <r> = %.8f, <r^2> = %.8f" % (E_rad, r_rad, r2_rad))
for e, x in zip(eps_l, E_tr):
    print("  transferencia eps=%.2f (Rich h^4): E = %.10f  E-E_rad = %+.2e" % (e, x, x - E_rad))
print("  transferencia extrapolada: E = %.10f  E-E_rad = %+.2e  (orden de Trotter %.3f)"
      % (E_tr_ext, E_tr_ext - E_rad, orden_tr))
print("  mixto determinista tau=20: E = %.10f  E-E_rad = %+.2e" % (Emix20, Emix20 - E_rad))
print("PIGS tau=20: E = %.6f +- %.6f  (%+.2f sigma del radial)" % (E_p, eE_p, (E_p - E_rad) / eE_p))
print("            <r> = %.5f +- %.5f  (%+.2f sigma del radial; %+.2f sigma del puro det.)"
      % (r_p, er_p, (r_p - r_rad) / er_p, (r_p - r_puro20) / er_p))
print("            <r^2> = %.5f +- %.5f  (%+.2f sigma del radial; %+.2f sigma del puro det.)"
      % (r2_p, er2_p, (r2_p - r2_rad) / er2_p, (r2_p - r2_puro20) / er2_p))
for s in scan:
    print("  tau=%4.1f  PIGS E = %.6f +- %.6f  det = %.7f  (%+.2f sigma)"
          % (s["tau"], s["E_pigs"], s["eE"], s["E_det"], s["sigma_E"]))
print("  replica 1 tau=5: %.6f +- %.6f (%+.2f sigma); replica 2: %.6f +- %.6f (%+.2f sigma)"
      % (rep1["media"], rep1["err"], rep1["sigma"], rep2["media"], rep2["err"], rep2["sigma"]))

# ---------------- huellas sha256 (figuras congeladas) ----------------
scripts_fig = {
    "10_radial_convergencia.png": "10_radial_controles.py",
    "11_proyeccion.png": "11_transferencia_controles.py",
    "11_trotter.png": "11_transferencia_controles.py",
    "12_pigs_delta02.png": "12_pigs_produccion.py",
    "12_pigs_tau.png": "12_pigs_produccion.py",
    "13_controles.png": "13_controles_hulthen_pozo.py",
    "14_cajas.png": "14_criterio_cajas.py",
    "15_limites.png": "15_limites.py",
    "16_primer_grafico.png": "16_primer_grafico.py",
    "18_primer_grafico.png": "18_figura_presentacion.py",
}
huellas = []
for nombre in sorted(os.listdir(FIG)):
    if not nombre.endswith(".png"):
        continue
    scr = scripts_fig.get(nombre, "(desconocido)")
    ruta_scr = os.path.join(AQUI, scr)
    huellas.append({"figura": "figuras/" + nombre, "sha256_figura": sha256(os.path.join(FIG, nombre)),
                    "script": "codigo/" + scr,
                    "sha256_script": sha256(ruta_scr) if os.path.exists(ruta_scr) else None})
print("\nHuellas sha256:")
for h in huellas:
    print("  %-34s %s\n  %-34s %s" % (h["figura"], h["sha256_figura"], h["script"], h["sha256_script"]))

salida = {
    "script": "fase2/codigo/16_primer_grafico.py",
    "fecha": "2026-10-27",
    "fuentes": ["11_transferencia.json", "12_pigs.json", "12b_pigs_replica.json", "12c_pigs_coulomb_tau5.json"],
    "radial": {"E0": E_rad, "r": r_rad, "r2": r2_rad, "nota": "R=40, h=1/80 y 1/160, Richardson"},
    "transferencia": {"eps": eps_l, "E_Rich_h4": E_tr, "E_extrapolado": E_tr_ext, "orden_trotter": orden_tr,
                      "r_h002": r_tr, "r2_h002": r2_tr, "E_mixto_tau20": Emix20,
                      "r_puro_tau20": r_puro20, "r2_puro_tau20": r2_puro20,
                      "tau": tau_det, "E_mixto": Emix_det},
    "pigs_tau20": {"E": E_p, "eE": eE_p, "r": r_p, "er": er_p, "r2": r2_p, "er2": er2_p,
                   "sigma_E_rad": (E_p - E_rad) / eE_p, "sigma_r_rad": (r_p - r_rad) / er_p,
                   "sigma_r2_rad": (r2_p - r2_rad) / er2_p},
    "pigs_tau": scan,
    "replicas_tau5": {"replica1": rep1, "replica2": rep2},
    "huellas": huellas,
}
with open(os.path.join(RES, "16_primer_grafico.json"), "w") as f:
    json.dump(salida, f, indent=1)
print("\nGuardado: figuras/16_primer_grafico.png y resultados/16_primer_grafico.json")
