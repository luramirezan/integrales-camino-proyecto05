"""Bloque 00: toy models del umbral de enlace y comparacion con Yukawa (l=0).
Unidades: hbar=m=g=1, delta = mu*hbar^2/(m g). Ecuacion: -u''/2 + V u = E u, u(0)=0.
(A) Hulthen V_H(r;d) = -d/(e^{d r}-1): solucion exacta, umbral d=2, <r> exacto.
(B) Comparacion rigurosa V_H(d) <= V_Y(d) <= V_H(2d)  =>  1 <= delta_c <= 2.
(C) Pozo esferico cuadrado V=-V0 (r<R): umbral V0 R^2 = pi^2/8, ley kappa R ~ (lambda-lambda_c).
(D) Comprobacion numerica (diferencias finitas + Richardson; disparo a energia cero).
Salida: resumen impreso y figura fase1/figuras/00_toy_model.png."""
import os as _os
_RAIZ = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..','..'))  # raiz del repositorio
import numpy as np
import sympy as sp
from scipy.linalg import eigh_tridiagonal
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

DC_REF = 1.19061242106   # Gebremedhin y Weatherford (2023), via cita secundaria (ver sec. 6)
OUT = _RAIZ + "/fase1/figuras/00_toy_model.png"

r, x, d, k, E = sp.symbols("r x delta kappa E", positive=True)

print("=== (A) Hulthen ===")
VH = -d/(sp.exp(d*r) - 1)
print("lim_{delta->0} V_H =", sp.limit(VH, d, 0))
print("serie de V_H en r=0:", sp.series(VH, r, 0, 2).removeO())
print("serie de V_Y en r=0:", sp.series(-sp.exp(-d*r)/r, r, 0, 2).removeO())
kap = 1 - d/2
u = (1 - sp.exp(-d*r))*sp.exp(-kap*r)
E0H = -kap**2/2
res = sp.simplify(-sp.diff(u, r, 2)/2 + VH*u - E0H*u)
print("residuo de -u''/2+V_H u-E u con u=(1-e^{-dr})e^{-(1-d/2)r}, E=-(1-d/2)^2/2:", res)
print("u(0) =", u.subs(r, 0), "; u'(0) =", sp.diff(u, r).subs(r, 0))
print("E0_H(delta) expandida:", sp.expand(E0H))
# estados excitados: u_n = (1-e^{-dr}) * P(e^{-dr}) e^{-kappa_n r}; formula conocida verificada para n=2
n = 2
k2 = sp.Rational(1, n) - n*d/2
A = sp.symbols("A")
u2 = (1 - sp.exp(-d*r))*(1 + A*sp.exp(-d*r))*sp.exp(-k2*r)
res2 = sp.expand(sp.simplify((-sp.diff(u2, r, 2)/2 + VH*u2 + k2**2/2*u2)*(sp.exp(d*r) - 1)*sp.exp(k2*r)))
# resolver A anulando el residuo en dos puntos y comprobar en un tercero
Asol = sp.solve(res2.subs({r: 1, d: sp.Rational(1, 10)}), A)
A_val = [a for a in Asol if a.is_real]
chk = [sp.N(res2.subs({A: a, d: sp.Rational(1, 10), r: 3})) for a in A_val]
print("n=2 (d=0.1): A =", [sp.N(a, 8) for a in A_val], "residuo en r=3:", chk)
print("umbrales Hulthen: 1s d=2, 2s d=2/n^2 =", 2/n**2)
# <r> exacto
kk = sp.symbols("kappa", positive=True)
uk = (1 - sp.exp(-d*r))*sp.exp(-kk*r)
N0 = sp.integrate(uk**2, (r, 0, sp.oo))
N1 = sp.integrate(r*uk**2, (r, 0, sp.oo))
rmean = sp.simplify((N1/N0).subs(kk, 1 - d/2))
print("<r>_H(delta) =", sp.factor(rmean))
print("<r>_H(0) =", sp.limit(rmean, d, 0))
eta = sp.symbols("eta", positive=True)   # eta = 2 - delta
lead = sp.limit((rmean*2*(1 - d/2)).subs(d, 2 - eta), eta, 0)
print("lim_{delta->2} 2 kappa <r>_H =", lead)
print("zero-energy en delta=2: u=1-e^{-2r}, residuo:",
      sp.simplify(-sp.diff(1 - sp.exp(-2*r), r, 2)/2 + VH.subs(d, 2)*(1 - sp.exp(-2*r))),
      "; u'(oo) =", sp.limit(sp.diff(1 - sp.exp(-2*r), r), r, sp.oo))

print("\n=== (B) Comparacion V_H(d) <= V_Y(d) <= V_H(2d) ===")
# en x = d r: r*V_H(d) = -x/(e^x-1); r*V_Y = -e^{-x}; r*V_H(2d) = -2x/(e^{2x}-1)
f1 = x/(sp.exp(x) - 1) - sp.exp(-x)          # >= 0  <=> V_H(d) <= V_Y(d)
g1 = sp.simplify(f1*(sp.exp(x) - 1)*sp.exp(x))  # = x e^x - e^x + 1
print("f1*(e^x-1)e^x =", sp.expand(g1), "; en 0:", g1.subs(x, 0), "; derivada:", sp.simplify(sp.diff(g1, x)))
f2 = sp.exp(-x) - 2*x/(sp.exp(2*x) - 1)      # >= 0  <=> V_Y(d) <= V_H(2d)
print("f2 = e^{-x}(1 - x/sinh x):", sp.simplify((f2 - sp.exp(-x)*(1 - x/sp.sinh(x))).rewrite(sp.exp)) == 0, "; sinh x - x >= 0: derivada cosh x - 1 >= 0")
xs = np.linspace(1e-6, 40, 400001)
F1 = sp.lambdify(x, f1, "numpy"); F2 = sp.lambdify(x, f2, "numpy")
with np.errstate(over="ignore", invalid="ignore"):
    m1 = np.nanmin(F1(xs)); m2 = np.nanmin(F2(xs))
print(f"min numerico en (0,40]: f1 = {m1:.2e}, f2 = {m2:.2e} (ambos >= 0)")
print("=> E_H(d) <= E_Y(d) <= E_H(2d) = -(1-d)^2/2 ; Yukawa ligado si d<1, no ligado si d>=2")

print("\n=== (C) Pozo esferico cuadrado ===")
V0, R, K = sp.symbols("V0 R K", positive=True)
lam = sp.symbols("lambda", positive=True)
# dentro u = sin(k r), k^2 = 2(V0+E); fuera e^{-kappa r}; empalme k cot(kR) = -kappa
lam_c = sp.solve(sp.Eq(sp.sqrt(2*lam), sp.pi/2), lam)[0]
print("umbral (kappa=0 => kR=pi/2): V0 R^2 =", lam_c)
# en variables adimensionales (R=1): K=kR, q=kappa R, K^2+q^2=2 lambda, q=-K cot K
s = sp.symbols("s")   # s = lambda - lambda_c
q = sp.symbols("q")
Kf = lambda q_, s_: sp.sqrt(2*(lam_c + s_) - q_**2)
F = -Kf(q, s)*sp.cot(Kf(q, s)) - q
dq_ds = sp.simplify(-sp.diff(F, s)/sp.diff(F, q)).subs({q: 0, s: 0})
print("d(kappa R)/d(lambda) en el umbral =", sp.nsimplify(sp.simplify(dq_ds)))
for sv in [1e-2, 1e-3]:
    qn = brentq(lambda qq: float(F.subs({q: qq, s: sv})), 1e-12, 0.5)
    print(f"  lambda-lambda_c={sv:g}: kappa R={qn:.6e}, cociente={qn/sv:.5f}, E R^2={-qn**2/2:.4e}")

print("\n=== (D) Comprobacion numerica ===")
def fd(V, R_, N):
    h = R_/(N + 1); rr = h*np.arange(1, N + 1)
    w, v = eigh_tridiagonal(1/h**2 + V(rr), -0.5/h**2*np.ones(N - 1), select="i", select_range=(0, 0))
    uu = v[:, 0]
    return w[0], np.sum(rr*uu**2)/np.sum(uu**2)
def fd_rich(V, R_, N):
    E1, r1 = fd(V, R_, N); E2, r2 = fd(V, R_, 2*N + 1)
    return (4*E2 - E1)/3, (4*r2 - r1)/3
VHn = lambda dd: (lambda rr: -dd/np.expm1(dd*rr))
VYn = lambda dd: (lambda rr: -np.exp(-dd*rr)/rr)
rm_f = sp.lambdify(d, rmean, "numpy")
maxdE = 0; maxdr = 0
for dd in [0.2, 0.5, 1.0, 1.5]:
    En, rn = fd_rich(VHn(dd), 80.0, 8000)
    maxdE = max(maxdE, abs(En - (-(1 - dd/2)**2/2))); maxdr = max(maxdr, abs(rn - rm_f(dd)))
print(f"Hulthen FD vs exacto (d=0.2,0.5,1,1.5): max|dE| = {maxdE:.1e}, max|d<r>| = {maxdr:.1e}")
viol = 0
rows = []
for dd in [0.1, 0.3, 0.5, 0.7, 0.9]:
    EY, rY = fd_rich(VYn(dd), 120.0, 12000)
    lo, hi = -(1 - dd/2)**2/2, -(1 - dd)**2/2
    viol += not (lo <= EY <= hi)
    rows.append((dd, lo, EY, hi))
print("sandwich E_H(d) <= E_Y(d) <= E_H(2d), violaciones:", viol, "de", len(rows))
for dd, lo, EY, hi in [rows[0], rows[2], rows[4]]:
    print(f"  d={dd}: {lo:.6f} <= {EY:.6f} <= {hi:.6f}")
# umbral Yukawa por disparo a energia cero (independiente de la caja)
def slope_end(dd, Rmax=200.0):
    f = lambda t, y: [y[1], -2*np.exp(-dd*t)/t*y[0]]
    r0 = 1e-8; y0 = [r0 - r0**2, 1 - 2*r0]
    sol = solve_ivp(f, [r0, Rmax], y0, rtol=1e-12, atol=1e-14, method="DOP853")
    return sol.y[1, -1]
dcY = brentq(slope_end, 1.1, 1.3, xtol=1e-13)
print(f"Yukawa 1s, disparo E=0: delta_c = {dcY:.10f} (ref. {DC_REF}, dif {dcY-DC_REF:.1e})")
def slope_end2(dd, Rmax=400.0):  # 2s: segundo cambio de signo de u'(R) al bajar delta
    return slope_end(dd, Rmax)
grid = np.linspace(0.2, 0.5, 31); vals = [slope_end2(g) for g in grid]
i = [j for j in range(len(grid) - 1) if np.sign(vals[j]) != np.sign(vals[j + 1])][0]
dc2 = brentq(slope_end2, grid[i], grid[i + 1], xtol=1e-10)
print(f"Yukawa 2s, disparo E=0: delta_c(2s) = {dc2:.6f}; Hulthen 2s: 0.5")
print(f"cocientes de umbrales: 1s Y/H = {dcY/2:.4f}; 2s Y/H = {dc2/0.5:.4f}")
# Yukawa: kappa/(dc-d) cerca del umbral (compara con c_H=1/2)
for dd in [1.10, 1.15]:
    EY, _ = fd_rich(VYn(dd), 400.0, 40000)
    print(f"  Yukawa d={dd}: kappa/(dc-d) = {np.sqrt(-2*EY)/(dcY-dd):.4f}   (Hulthen: 0.5 exacto)")

# figura: espacio de parametros
dg = np.linspace(0, 2.05, 300)
dY = np.linspace(0, 1.15, 24)
EYs = [fd_rich(VYn(v), 400.0, 40000)[0] if v > 0 else -0.5 for v in dY]
fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
ax[0].plot(dg, np.where(dg < 2, -(1 - dg/2)**2/2, 0), label=r"Hulthén $V_H(\delta)$ (exacto)")
ax[0].plot(dg, np.where(dg < 1, -(1 - dg)**2/2, 0), label=r"Hulthén $V_H(2\delta)$ (exacto)")
ax[0].plot(dY, EYs, "o", ms=4, label="Yukawa (DF + Richardson)")
ax[0].axvline(dcY, ls=":", c="k", lw=1); ax[0].text(dcY + 0.02, -0.45, r"$\delta_c^{Y}$", fontsize=12)
ax[0].set_xlabel(r"$\delta=\mu\hbar^2/(mg)$", fontsize=12); ax[0].set_ylabel(r"$E_0\;[mg^2/\hbar^2]$", fontsize=12)
ax[0].set_title(r"$E_H(\delta)\leq E_Y(\delta)\leq E_H(2\delta)$", fontsize=12); ax[0].legend(fontsize=10)
lg = np.linspace(0.5, 4.0, 300)
qs = []
for lv in lg:
    if lv <= float(lam_c): qs.append(0.0); continue
    qs.append(brentq(lambda qq: float(F.subs({q: qq, s: lv - float(lam_c)})), 1e-14, np.sqrt(2*lv) - 1e-9))
qs = np.array(qs)
ax[1].plot(lg, -qs**2/2, label=r"pozo cuadrado: $ER^2$")
ax[1].plot(lg, -np.clip(lg - float(lam_c), 0, None)**2/2, "--", label=r"$-(\lambda-\pi^2/8)^2/2$")
ax[1].axvline(float(lam_c), ls=":", c="k", lw=1)
ax[1].set_xlabel(r"$\lambda=V_0R^2$ (con $\hbar=m=1$)", fontsize=12); ax[1].set_ylabel(r"$E_0R^2$", fontsize=12)
ax[1].set_title("Pozo esférico: umbral $\\pi^2/8$", fontsize=12); ax[1].legend(fontsize=10)
fig.tight_layout(); fig.savefig(OUT, dpi=150)
print("figura:", OUT)
