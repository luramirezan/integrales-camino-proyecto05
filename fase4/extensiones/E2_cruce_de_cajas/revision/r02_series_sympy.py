"""r02_series_sympy.py -- revision R2: rehace con sympy las series de teoria.md.
x cot x = z - (eps/2) x^2 ; y = x^2/pi^2. Puntos fijos, serie de y(z, eps), cruce (R, 2R) y (R1, R2) general,
y*, punto fijo y coeficiente k1 de <r>/R. Salida: resultados/r02_series_sympy.json"""
import json, sympy as sp
z, e, d = sp.symbols("z epsilon d")
t, x = sp.symbols("t x", positive=True)
pi = sp.pi
lam = sp.symbols("lambda")
# x = pi/2 + d(z, eps): resolver por series con escala lam (z -> lam z, eps -> lam eps)
d1, d2 = sp.symbols("d1 d2")
X = pi / 2 + lam * d1 + lam**2 * d2
expr = X * sp.cos(X) - (lam * z - lam * e / 2 * X**2) * sp.sin(X)
ser = sp.series(expr, lam, 0, 3).removeO()
s1 = sp.solve(sp.expand(ser).coeff(lam, 1), d1)[0]
s2 = sp.solve(sp.expand(ser.subs(d1, s1)).coeff(lam, 2), d2)[0]
Y = sp.expand(sp.series((X.subs({d1: s1, d2: s2}))**2 / pi**2, lam, 0, 3).removeO().subs(lam, 1))
print("y(z, eps) =", Y)
# cruce (R, 2R): z -> 2z, eps -> eps/2 ; z* = a1 eps + a2 eps^2
a1, a2 = sp.symbols("a1 a2")
zs = a1 * lam * e + a2 * (lam * e)**2
Ye = Y.subs({z: zs, e: lam * e}); Y2 = Y.subs({z: 2 * zs, e: lam * e / 2})
dif = sp.expand(sp.series(Ye - Y2, lam, 0, 3).removeO())
A1 = sp.solve(dif.coeff(lam, 1), a1)[0]
A2 = sp.solve(dif.coeff(lam, 2).subs(a1, A1), a2)[0]
print("z* =", A1, "eps +", sp.simplify(A2), "eps^2")
ystar = sp.simplify(sp.expand(sp.series(Ye.subs({a1: A1, a2: A2}), lam, 0, 3).removeO().subs(lam, 1)))
print("y* =", sp.expand(ystar))
# general R1, R2 = q R1 a primer orden: z1 = R1/a, z2 = q z1, eps2 = eps1/q
q, w = sp.symbols("q w")   # w = R1/a
Y1 = Y.subs({z: w, e: e}); Yq = Y.subs({z: q * w, e: e / q})
lin = sp.expand(sp.series(Y1.subs({w: lam * w, e: lam * e}) - Yq.subs({w: lam * w, e: lam * e}), lam, 0, 2).removeO().coeff(lam, 1))
wsol = sp.solve(lin, w)[0]
print("primer orden general: R1/a* =", sp.simplify(wsol), " -> 1/a* = (R1/a*)/R1 con eps = r_e/R1")
# rho: umbral y coeficiente
G0 = sp.simplify(1 - sp.integrate(t * sp.sin(pi / 2 * t)**2, (t, 0, 1)) / sp.integrate(sp.sin(pi / 2 * t)**2, (t, 0, 1)))
Gx = 1 - sp.integrate(t * sp.sin(x * t)**2, (t, 0, 1)) / sp.integrate(sp.sin(x * t)**2, (t, 0, 1))
dGdx = sp.simplify(sp.diff(Gx, x).subs(x, pi / 2))
dxdz = sp.Rational(-2) / pi
dGdz = sp.simplify(dGdx * dxdz)
# primer orden: rho(delta_c, R) = G0 + K eps, con K = G0 (norma) + dG/dz * dz_equiv, dz_equiv = -pi^2 eps/8
K = sp.simplify(G0 + dGdz * (-pi**2 / 8))
k1 = sp.simplify(K / (2 * dGdz))
print("G0 =", G0, "=", sp.N(G0), "; dG/dz =", dGdz, "=", sp.N(dGdz), "; K =", K, "=", sp.N(K), "; k1 =", k1, "=", sp.N(k1))
res = dict(y_serie=str(Y), z_estrella=[str(A1), str(sp.simplify(A2))], y_estrella=str(sp.expand(ystar)),
           general_R1a=str(sp.simplify(wsol)), G0=float(G0), dGdz=float(dGdz), K=float(K), k1=float(k1),
           k1_E2=float(sp.pi**2 * (4 + sp.pi**2) / (16 * (sp.pi**2 - 12))))
json.dump(res, open("resultados/r02_series_sympy.json", "w"), indent=1)
