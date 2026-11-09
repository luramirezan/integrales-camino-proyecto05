# -*- coding: utf-8 -*-
"""Fase 1, bloque 02: limite de Coulomb (delta -> 0) del potencial de Yukawa.
Unidades: hbar = m = g = 1 (distancias en a = hbar^2/(m g), energias en m g^2/hbar^2).
Ecuacion radial (l=0): -u''/2 - e^{-delta r}/r u = E u.
1) sympy: hidrogeno (E_1s, normalizacion, <r>, <r^2>) y serie perturbativa de E0(delta).
2) numerico: diferencias finitas (Richardson) con scipy.sparse.linalg.eigsh.
"""
import os as _os
_RAIZ = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..','..'))  # raiz del repositorio
import numpy as np, sympy as sp, scipy.sparse as sps
from scipy.sparse.linalg import eigsh
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

r, d, l = sp.symbols('r delta lambda', positive=True)
# --- Hidrogeno -------------------------------------------------------------
u1 = 2*r*sp.exp(-r)                     # u = r R, R_1s = 2 e^{-r}
assert sp.integrate(u1**2, (r, 0, sp.oo)) == 1
E1 = sp.simplify((-sp.diff(u1, r, 2)/2 - u1/r)/u1); assert E1 == sp.Rational(-1, 2)
n = sp.symbols('n', positive=True, integer=True)
for k in (1, 2, 3):   # E_n = -1/(2n^2): verificacion con u_n0 genérico n=1..3 (Laguerre)
    un = r*sp.exp(-r/k)*sp.assoc_laguerre(k-1, 1, 2*r/k)
    assert sp.simplify((-sp.diff(un, r, 2)/2 - un/r)/un + sp.Rational(1, 2*k**2)) == 0
mom = {j: sp.integrate(r**j*u1**2, (r, 0, sp.oo)) for j in (1, 2, 3)}
print("<r>, <r^2>, <r^3> =", mom)          # 3/2, 3, 15/2
# --- Serie perturbativa ------------------------------------------------------
Vexp = sp.series(-sp.exp(-d*r)/r, d, 0, 5).removeO()
print("V(r) expandido:", sp.expand(Vexp))
E1o = sp.integrate(sp.expand(Vexp + 1/r)*u1**2, (r, 0, sp.oo))
print("<V - V_C> (todos los ordenes hasta d^4 en primer orden PT):", sp.expand(E1o))
# Segundo orden de PT por Dalgarno-Lewis para W = -r/2 (coef. de d^2): (H0-E0)F u1 = -(W-<W>) u1
F = sp.Function('F'); a0, a1, a2 = sp.symbols('a0 a1 a2')
Ftry = a0 + a1*r + a2*r**2              # a0 queda libre: F=const da (H0-E1)(a0 u1)=0
W = -r/2; Wm = sp.integrate(W*u1**2, (r, 0, sp.oo))
lhs = -sp.diff(Ftry*u1, r, 2)/2 - Ftry*u1/r + sp.Rational(1, 2)*Ftry*u1
eqs = sp.Poly(sp.expand(sp.simplify((lhs + (W - Wm)*u1)/sp.exp(-r))), r).coeffs()
sol = sp.solve(eqs, [a1, a2], dict=True)[0]; Fgen = Ftry.subs(sol)
print("Dalgarno-Lewis, solucion general F =", Fgen, "(a0 libre)")
a0s = sp.solve(sp.integrate(Fgen*u1**2, (r, 0, sp.oo)), a0)[0]   # ortogonalizar: <F>=0
Fs = Fgen.subs(a0, a0s)
E2gen = sp.simplify(sp.integrate((W - Wm)*Fgen*u1**2, (r, 0, sp.oo)))
print("E2 con a0 libre =", E2gen, "(no depende de a0)")
E2W = sp.integrate((W - Wm)*Fs*u1**2, (r, 0, sp.oo))
print("Dalgarno-Lewis F =", Fs, " E2 para W =", E2W)
c = [sp.Rational(-1, 2), 1, -sp.Rational(3, 4), sp.Rational(1, 2), sp.Rational(-5, 16) + E2W]
print("Coeficientes E0 = sum c_k d^k:", c)   # c4 = -5/16 - 3/8 = -11/16

# --- Numerico --------------------------------------------------------------
def E0_fd(delta, h, R=60.0):
    N = int(R/h); x = h*np.arange(1, N+1)
    main = 1/h**2 - np.exp(-delta*x)/x; off = -0.5/h**2*np.ones(N-1)
    H = sps.diags([off, main, off], [-1, 0, 1], format='csc')
    return eigsh(H, k=1, sigma=-0.6, which='LM', return_eigenvectors=False)[0]
def E0(delta):
    e1, e2 = E0_fd(delta, 0.004), E0_fd(delta, 0.002)
    return (4*e2 - e1)/3            # Richardson O(h^4)
cf = [float(x) for x in c]
deltas = np.array([0, 0.005, 0.01, 0.02, 0.05, 0.1, 0.15, 0.2, 0.3])
rows = []
for dl in deltas:
    en = E0(dl); s1 = cf[0]+cf[1]*dl; s2 = s1+cf[2]*dl**2; s3 = s2+cf[3]*dl**3; s4 = s3+cf[4]*dl**4
    rows.append((dl, en, s1, s2, s3, s4))
print("\n| delta | E0 numerico | orden 1 | orden 2 | orden 3 | orden 4 | |num-ord2| |")
for t in rows:
    print("| %.3f | %.8f | %.6f | %.8f | %.8f | %.8f | %.2e |" % (*t, abs(t[1]-t[3])))
t = rows[-1]   # delta = 0.3: error absoluto y relativo de las series de orden 2 y 4
print("delta=0.3: |num-ord2| = %.3e (relativo %.2f %%), |num-ord4| = %.3e (relativo %.2f %%)"
      % (abs(t[1]-t[3]), 100*abs(t[1]-t[3])/abs(t[1]), abs(t[1]-t[5]), 100*abs(t[1]-t[5])/abs(t[1])))
# ajuste polinomico para estimar coeficientes numericamente
dd = np.linspace(0.002, 0.05, 12); ee = np.array([E0(x) for x in dd])
print("Ajuste polinomico grado 4 (c0..c4):", np.polyfit(dd, ee, 4)[::-1])

fig, ax = plt.subplots(1, 2, figsize=(10, 4))
dg = np.linspace(0, 0.3, 31); eg = np.array([E0(x) for x in dg])
ax[0].plot(dg, eg, 'k.', label='numérico (dif. finitas)')
for k, (lab, col) in enumerate([('orden 1', 'C0'), ('orden 2', 'C1'), ('orden 3', 'C2')]):
    ax[0].plot(dg, np.polyval(cf[:k+2][::-1], dg), col, label=lab)
ax[0].set_xlabel(r'$\delta$'); ax[0].set_ylabel(r'$E_0$ [$mg^2/\hbar^2$]'); ax[0].legend(); ax[0].set_title('Límite de Coulomb')
for k, col in zip(range(1, 5), ['C0', 'C1', 'C2', 'C3']):
    ax[1].loglog(dg[1:], np.abs(eg[1:]-np.polyval(cf[:k+1][::-1], dg[1:])), col+'o-', ms=3, label=f'orden {k}')
ax[1].set_xlabel(r'$\delta$'); ax[1].set_ylabel('|error|'); ax[1].legend(); ax[1].set_title('Error de la serie truncada')
plt.tight_layout(); plt.savefig(_RAIZ + '/fase1/figuras/02_limite_coulomb.png', dpi=150)
