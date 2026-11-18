"""06_verificacion.py -- comprobaciones adicionales (diagnostico, no cambian los criterios ya fijados).

V1  Diagnostico de C7 (que no paso): diferencia A - B en valor ABSOLUTO para delta = 0.2 ... 1.18 con h = 1/40 y
    h = 1/80 en el metodo B. Si la diferencia absoluta baja ~16 veces al pasar a h = 1/80 (Richardson de orden 2
    deja error de orden 4), la causa es la discretizacion de B y no el metodo A.
V2  Conversion de unidades del deuteron: E = eps mu alpha_g^2 debe devolver -B_d.
V3  Plasma: densidad critica por la formula numerica del NRL (n = T (743/lambda_cm)^2) frente a la formula SI.
V4  Sensibilidad del deuteron a la eleccion de m_pi: rango de delta_d, g y m_pi critico entre pi0 y pi+-.
V5  Longitud de dispersion en la Fase 3 (a_s(1.19) = +2204, a_s(1.20) = -142.9) frente a la nuestra.
Salida: resultados/06_verificacion.json
"""
import numpy as np

import comun_e1 as c

log = c.Registro()
K = c.CONST
P = c.leer("02_plasma")
D = c.leer("04_deuteron")
M = c.leer("03_materia_oscura")
out = {}

# V1
v1 = []
for x in P["curva_E"]:
    d, EA, R = x["delta"], x["E_A_hartree"], x["R_caja"]
    E40 = x["E_B_hartree"]
    E80 = c.estado_1s_caja(d, R, h=1 / 80)["E0"]
    v1.append(dict(delta=d, R=R, dif_abs_h40=abs(EA - E40), dif_abs_h80=abs(EA - E80),
                   cociente=abs(EA - E40) / max(abs(EA - E80), 1e-300), dif_rel_h80=abs(EA - E80) / abs(EA)))
    log(f"V1 delta = {d:5.2f}: |E_A - E_B(h=1/40)| = {abs(EA - E40):.2e}, |E_A - E_B(h=1/80)| = {abs(EA - E80):.2e},"
        f" cociente = {abs(EA - E40) / max(abs(EA - E80), 1e-300):.1f}, rel(h=1/80) = {abs(EA - E80) / abs(EA):.1e}")
out["V1"] = v1

# V2
cen = D["escenario_A"]["promedio"]
E_MeV = cen["eps"] * D["mu"] * cen["alpha_g"] ** 2
out["V2"] = dict(E_MeV=E_MeV, B=D["B_masas"], dif=E_MeV + D["B_masas"])
log(f"V2 eps mu alpha^2 = {E_MeV:.10f} MeV ; -B = {-D['B_masas']:.10f} MeV")

# V3
lam_cm = P["lambda_c_a0"] * K["a0"] * 100
n_nrl = (K["nrl_coef_cm"] / lam_cm) ** 2          # cm^-3 por eV
out["V3"] = dict(n_nrl_por_eV=n_nrl, n_SI_por_eV=P["n_crit_por_eV_cm3"], rel=n_nrl / P["n_crit_por_eV_cm3"] - 1)
log(f"V3 n_crit/T: NRL {n_nrl:.4e}, SI {P['n_crit_por_eV_cm3']:.4e} cm^-3 eV^-1 (rel {n_nrl / P['n_crit_por_eV_cm3'] - 1:.1e})")

# V4
E = D["escenario_A"]
rng = {k: (min(E[s][k] for s in E), max(E[s][k] for s in E)) for k in ("delta_A", "alpha_g", "m_pi_crit_g_fijo",
                                                                       "r_str_modelo_fm")}
out["V4"] = rng
for k, v in rng.items():
    log(f"V4 {k}: de {v[0]:.5f} a {v[1]:.5f} (variacion relativa {(v[1] - v[0]) / v[0]:.2%})")

# V5
out["V5"] = dict(a119=M["a_s_119"], a120=M["a_s_120"], fase3=(2204, -142.9))
log(f"V5 a_s(1.19) = {M['a_s_119']:.1f} (Fase 3: +2204), a_s(1.20) = {M['a_s_120']:.2f} (Fase 3: -142.9)")
c.guardar("06_verificacion", out, log.texto())
