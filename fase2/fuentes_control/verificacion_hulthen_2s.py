"""Comprobación simbólica del estado 2s exacto de Hulthén (cierra la comprobación
parcial de fase1/secciones/00_marco.md, 0.6.1). Unidades hbar=m=g=1,
V_H = -delta/(e^{delta r}-1). Fórmula general (Flügge, problema 67; Varshni 1990):
E_n = -(1/2)(1/n - n*delta/2)^2, umbral del estado ns en delta = 2/n^2.
"""
import sympy as sp

r, d, A, x = sp.symbols('r delta A x', positive=True)
k2 = sp.Rational(1, 2) - d                 # kappa_2 = 1/n - n delta/2 con n = 2
X = sp.exp(-d*r)
u = (1 - X)*(1 + A*X)*sp.exp(-k2*r)
V = -d*X/(1 - X)
E = -k2**2/2
res = sp.expand(sp.simplify((-sp.diff(u, r, 2)/2 + V*u - E*u)*(1 - X)*sp.exp(k2*r)))
res = sp.expand(sp.powsimp(sp.expand(res.subs(r, -sp.log(x)/d)), force=True))
coefs = sp.Poly(res, x).coeffs()
sol = sp.solve(coefs, A, dict=True)[0]
print('residuo (polinomio en x=e^{-delta r}):', res)
print('A =', sp.simplify(sol[A]))                       # (1+delta)/(delta-1)
print('residuo con ese A:', sp.simplify(res.subs(sol)))  # 0 para todo r y delta
print('A(delta=0.1) =', float(sol[A].subs(d, sp.Rational(1, 10))))  # -1.2222...
# n general: kappa_n = 1/n - n delta/2 > 0  <=>  delta < 2/n^2
n = sp.symbols('n', positive=True)
print('umbral ns:', sp.solve(sp.Eq(1/n - n*d/2, 0), d))
