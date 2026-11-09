"""Fase 1 - Bloque 01: adimensionalizacion de la ecuacion radial con potencial de Yukawa.
Verificacion simbolica (sympy) y numerica (numpy/scipy). Genera figura en ../figuras/."""
import os
import sympy as sp
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AQUI = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(AQUI, "..", "figuras")

# ---------- 1. Ecuacion dimensional ----------
r, x, hbar, m, g, mu, E, l = sp.symbols("r x hbar m g mu E l", positive=True)
eps, delta = sp.symbols("epsilon delta", real=True)
u = sp.Function("u")
V = -g * sp.exp(-mu * r) / r
radial = -hbar**2 / (2 * m) * u(r).diff(r, 2) + (V + hbar**2 * l * (l + 1) / (2 * m * r**2)) * u(r) - E * u(r)

# ---------- 2. Escalas ----------
a = hbar**2 / (m * g)          # radio de Bohr generalizado
EH = m * g**2 / hbar**2        # energia de Hartree generalizada = g/a
assert sp.simplify(EH - g / a) == 0
assert sp.simplify(EH - hbar**2 / (m * a**2)) == 0
print("a   =", a, "   E_H =", EH, "  (E_H = g/a = hbar^2/(m a^2))")

# ---------- 3. Cambio de variables r = a x, E = eps*E_H, mu = delta/a ----------
w = sp.Function("w")  # w(x) = u(a x)
sub = radial.subs(u(r).diff(r, 2), w(x).diff(x, 2) / a**2).subs(u(r), w(x))
sub = sub.subs({E: eps * EH}).subs(r, a * x).subs(mu, delta / a)
adim = sp.expand(sp.simplify(sub * (-2) / EH))
objetivo = w(x).diff(x, 2) + (2 * sp.exp(-delta * x) / x - l * (l + 1) / x**2 + 2 * eps) * w(x)
dif = sp.simplify(adim - sp.expand(objetivo))
print("Ecuacion adimensional - objetivo =", dif)
assert dif == 0
print("delta = mu*a =", sp.simplify(mu * a), "  (adimensional)")

# Analisis dimensional explicito: [hbar]=M L^2 T^-1, [g]=M L^3 T^-2, [mu]=L^-1
M_, L_, T_ = sp.symbols("M L T", positive=True)
dims = {hbar: M_ * L_**2 / T_, m: M_, g: M_ * L_**3 / T_**2, mu: 1 / L_}
print("[a] =", sp.simplify(a.subs(dims)), " [E_H] =", sp.simplify(EH.subs(dims)),
      " [delta] =", sp.simplify((mu * a).subs(dims)))
assert sp.simplify((mu * a).subs(dims)) == 1

# ---------- 4. Comprobaciones: limite de Coulomb y condiciones de frontera ----------
u0 = x * sp.exp(-x)
res = sp.simplify(u0.diff(x, 2) + (2 / x - 0 + 2 * sp.Rational(-1, 2)) * u0)
print("delta=0, l=0, u=x e^{-x}, eps=-1/2  -> residuo:", res)
assert res == 0
# <r> = int x |u|^2 / int |u|^2
rmed = sp.integrate(x * u0**2, (x, 0, sp.oo)) / sp.integrate(u0**2, (x, 0, sp.oo))
print("<x> hidrogeno 1s =", rmed)
# Comportamiento cerca del origen: e^{-delta x}/x = 1/x - delta + delta^2 x/2 + ...
print("Serie de e^{-delta x}/x:", sp.series(sp.exp(-delta * x) / x, x, 0, 3))
# Indice indicial: u ~ x^s -> s(s-1) = l(l+1) -> s = l+1 o s = -l
s = sp.symbols("s")
print("Raices indiciales:", sp.solve(s * (s - 1) - l * (l + 1), s))
# Asintotico: u ~ exp(-kappa x), kappa = sqrt(-2 eps)
kap = sp.symbols("kappa", positive=True)
print("kappa^2 + 2 eps = 0  ->  eps =", sp.solve(kap**2 + 2 * eps, eps))

# Equivalencia entre el potencial reescalado y las unidades atomicas: V/E_H = -e^{-delta x}/x
print("V/E_H =", sp.simplify((V / EH).subs(r, a * x).subs(mu, delta / a)))

# ---------- 5. Verificacion numerica ----------
def ec(xx, y, d, e, ll=0):
    return [y[1], -(2 * np.exp(-d * xx) / xx - ll * (ll + 1) / xx**2 + 2 * e) * y[0]]

xs = np.linspace(1e-6, 12, 2000)
sol = solve_ivp(ec, (xs[0], xs[-1]), [xs[0], 1 - xs[0]], t_eval=xs, args=(0.0, -0.5), rtol=1e-11, atol=1e-13)
err = np.max(np.abs(sol.y[0] - xs * np.exp(-xs)))
print(f"Numerico (delta=0, eps=-1/2): max|u - x e^-x| en [0,12] = {err:.2e}")

# Ejemplo dimensional -> adimensional (prueba de consistencia numerica de escalas)
hb, mm, gg, mmu = 1.3, 0.7, 2.1, 0.45
aa = hb**2 / (mm * gg); EHn = mm * gg**2 / hb**2
print(f"Ejemplo: a={aa:.6f}, E_H={EHn:.6f}, delta=mu*a={mmu*aa:.6f}")
rr = np.array([0.3, 1.0, 2.5])
Vd = -gg * np.exp(-mmu * rr) / rr
Va = -EHn * np.exp(-(mmu * aa) * (rr / aa)) / (rr / aa)
print("  max|V_dim - E_H * V_adim| =", np.max(np.abs(Vd - Va)))

# Valores fisicos ilustrativos: hidrogeno con apantallamiento de Debye
a0 = 0.529177210903e-10  # m (CODATA 2018)
for lam in [1e-10, 5.29e-11, 4.44e-11, 1e-9]:
    print(f"  lambda_D = {lam:.3e} m  -> delta = a0/lambda = {a0/lam:.4f}")

# ---------- 6. Figura ----------
plt.rcParams.update({"font.size": 11})
fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
xg = np.linspace(0.02, 8, 800)
for d, c in zip([0, 0.5, 1.0, 1.1906, 2.0], ["k", "C0", "C1", "C3", "C2"]):
    ax[0].plot(xg, -np.exp(-d * xg) / xg, c, label=fr"$\delta={d}$")
ax[0].set_ylim(-3, 0.1); ax[0].set_xlabel(r"$x=r/a$"); ax[0].set_ylabel(r"$V/E_H=-e^{-\delta x}/x$")
ax[0].set_title("Potencial de Yukawa adimensional"); ax[0].legend(fontsize=9); ax[0].axhline(0, color="gray", lw=.5)
ax[1].plot(xs, xs * np.exp(-xs), "k", lw=3, alpha=.4, label=r"exacta $x e^{-x}$")
ax[1].plot(xs, sol.y[0], "C3--", label=r"numérica, $\delta=0,\ \varepsilon=-1/2$")
ax[1].set_xlabel(r"$x$"); ax[1].set_ylabel(r"$u(x)$"); ax[1].set_xlim(0, 10)
ax[1].set_title("Comprobación del límite de Coulomb"); ax[1].legend(fontsize=9)
fig.tight_layout()
out = os.path.join(FIG, "01_potencial_adimensional.png")
fig.savefig(out, dpi=160)
print("Figura:", os.path.abspath(out))
print("TODAS LAS VERIFICACIONES PASARON")
