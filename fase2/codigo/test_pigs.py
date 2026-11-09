"""test_pigs.py -- pruebas rapidas de pigs.py (Fase 2). Ejecutar: python test_pigs.py"""
import os
import sys
import time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pares  # noqa: E402
import pigs   # noqa: E402

TAB = pares.tabla_richardson(0.1)
res = []


def prueba(nombre, cond, info):
    res.append(cond)
    print(f"[{'OK' if cond else 'FALLA'}] {nombre}: {info}")


# 1. interpolacion bilineal propia = la de TablaPares; bicubica reproduce la tabla en los nodos
rng = np.random.default_rng(1)
a = 0.01 + 9.9 * rng.random(3000); b = np.abs(a + 0.4 * rng.standard_normal(3000)) + 0.01
Ub, Uc = pigs.interpolador(TAB, "bilineal"), pigs.interpolador(TAB, "bicubica")
d1 = np.nanmax(np.abs(Ub(a, b) - TAB.valor(a, b, "bilineal")))
prueba("bilineal propia = TablaPares bilineal", d1 < 1e-12, f"max dif {d1:.1e}")
k = rng.integers(0, TAB.nt - 30, 500); m = rng.integers(0, 20, 500)
d2 = np.nanmax(np.abs(Uc(TAB.r[k], TAB.r[k + m]) - TAB.Ub[k, m]))
prueba("bicubica en nodos = tabla", d2 < 1e-10, f"max dif {d2:.1e}")
prueba("fuera de banda -> NaN", np.isnan(Uc(np.array([1.0]), np.array([1.0 + TAB.banda + 0.1])))[0], "ok")

# 2. Coulomb con u_T exacta: E_L = -1/2 en todos los barridos
t = time.perf_counter()
o = pigs.cadena(0.0, 2.0, 0.1, 300, 7, Uc, ntherm=50)
prueba("Coulomb E_L = -0.5 exacto", np.all(o["EL"] == -0.5), f"var {o['EL'].var():.1e}, M={o['M']}, {time.perf_counter()-t:.1f} s")
prueba("aceptaciones razonables", 0.3 < o["acept_puentes"] < 0.99 and 0.3 < o["acept_escala"] < 0.99,
       f"puentes {o['acept_puentes']:.2f}, extremos {o['acept_extremos']:.2f}, escala {o['acept_escala']:.2f}")
# V3 (H12 de V2): antes esta prueba se llamaba "caminos positivos y reproducibles" y solo miraba la reproducibilidad
prueba("reproducible (misma semilla -> misma serie)",
       np.allclose(pigs.cadena(0.0, 2.0, 0.1, 300, 7, Uc, ntherm=50)["rmid"], o["rmid"]), "misma semilla -> misma serie")
prueba("caminos positivos", bool((o["r_final"] > 0).all() and (o["rmid"] > 0).all()),
       f"min r_final {o['r_final'].min():.3f}, min r_mid {o['rmid'].min():.3f}")
# V3 (H8 de V2): tau/eps no multiplo de L -> error explicito (antes M se truncaba en silencio)
try:
    pigs.cadena(0.2, 2.5, 0.2, 10, 1, Uc, ntherm=5)
    prueba("tau/eps no multiplo de L -> ValueError", False, "no lanzo error")
except ValueError as ex:
    prueba("tau/eps no multiplo de L -> ValueError", True, str(ex))
prueba("tau_ef guardado", abs(o["tau_ef"] - 2.0) < 1e-12, f"tau_ef = {o['tau_ef']}")

# V3 (H12 de V2): prueba de la DISTRIBUCION muestreada. delta = 0.2, tau = 1, eps = 0.1 (M = 10): el histograma de
# r_{M/2} debe seguir [T^{M/2} u_T]^2 de la transferencia (misma accion, h = 0.02). Error por intervalo por bloques.
from scipy import stats  # noqa: E402
import transferencia as trf  # noqa: E402
t = time.perf_counter()
oh = pigs.cadena(0.2, 1.0, 0.1, 40000, 20262100, Uc, ntherm=500)
Tm, rg = trf.matriz_T(40.0, 0.02, 0.1, W=trf.W_yukawa(0.2), tabla=TAB)
x = rg * np.exp(-rg)
for _ in range(oh["M"] // 2):
    x = Tm @ x
rr = np.concatenate(([0.0], rg))
bins = np.linspace(0.0, 6.0, 25)


def chi2_hist(dens):
    cdf = np.concatenate(([0.0], np.cumsum(0.5 * (dens[1:] + dens[:-1]) * np.diff(rr))))
    P = np.diff(np.interp(bins, rr, cdf / cdf[-1]))
    Hb = np.array([np.histogram(blk, bins)[0] / len(blk) for blk in np.array_split(oh["rmid"], 20)])
    m_, se = Hb.mean(0), Hb.std(0, ddof=1) / np.sqrt(len(Hb))
    ok = se > 0
    c2 = float((((m_ - P)[ok] / se[ok])**2).sum())
    return c2, int(ok.sum()), float(stats.chi2.sf(c2, int(ok.sum())))


c2, dof, pv = chi2_hist(np.concatenate(([0.0], x**2)))
prueba("histograma de r_{M/2} = [T^{M/2} u_T]^2", pv > 1e-3, f"chi2 = {c2:.1f} con {dof} intervalos, p = {pv:.3f}, "
       f"{time.perf_counter()-t:.1f} s")
# potencia: la misma densidad con la escala de r alterada un 5 % (cambio de <r> de ~0.08, unos 5 errores) debe rechazarse
xs = np.interp(rr / 1.05, rr, np.concatenate(([0.0], x**2))) / 1.05
c2m, dofm, pvm = chi2_hist(xs)
prueba("la prueba de histograma tiene potencia (rechaza la escala r*1.05)", pvm < 1e-4,
       f"chi2 = {c2m:.1f} con {dofm}, p = {pvm:.1e}")

# 3. estadistica: AR(1) con phi = 0.8 -> tau_int = (1+phi)/(2(1-phi)) = 4.5
x = np.zeros(400000); e = rng.standard_normal(400000)
for i in range(1, len(x)):
    x[i] = 0.8 * x[i - 1] + e[i]
ti, Wn = pigs.tau_int_sokal(x)
prueba("tau_int Sokal en AR(1)", abs(ti - 4.5) < 0.3, f"{ti:.2f} (exacto 4.5), ventana {Wn}")
m_, eb = pigs.bloques(x, 20)
eteo = np.sqrt(2 * 4.5 * x.var() / len(x))
prueba("error por bloques en AR(1)", 0.5 < eb / eteo < 1.6, f"{eb:.4f} frente a {eteo:.4f}")
c = pigs.combinar([rng.standard_normal(20000) for _ in range(8)])
prueba("combinar: iid", abs(c["err"] / (1 / np.sqrt(160000)) - 1) < 0.5, f"err {c['err']:.2e} (teorico {1/np.sqrt(160000):.2e})")

print(f"\n{sum(res)}/{len(res)} pruebas pasan")
assert all(res)
