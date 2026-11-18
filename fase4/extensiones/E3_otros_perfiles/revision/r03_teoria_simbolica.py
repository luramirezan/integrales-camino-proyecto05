"""r03_teoria_simbolica.py -- Revision R3: comprobaciones simbolicas (sympy) de la teoria de E3.
1) Hulthen: u = (1 - e^{-d r}) e^{-k r} con k = 1 - d/2 resuelve u'' = 2(V - E)u, E = -k^2/2, para todo d
   (ligado si d < 2, polo virtual k_v = d/2 - 1 si d > 2); en d = 2, phi0 = 1 - e^{-2r} y r_e = 3/2 = 3/delta_c.
2) Caja en delta_c: -x cot x = r_e x^2/(2R) => 2R^2E/pi^2 = (1/4)(1 + r_e/R + (3/4) r_e^2/R^2 + O(R^-3)).
3) Cruce: delta* - delta_c = r_e pi^2/(8 c R1 R2) a primer orden.
4) ECSC: g(x) = x - 1 + e^{-x} cos x >= 0 (W <= delta): g(0) = 0, g' = 1 - h, h = e^{-x}(cos x + sin x), h' = -2 e^{-x} sin x.
"""
import json, os
import sympy as s
r, d, R, re, c, eps, x = s.symbols('r delta R r_e c epsilon x', positive=True)
k = 1 - d / 2
u = (1 - s.exp(-d * r)) * s.exp(-k * r)
V = -d * s.exp(-d * r) / (1 - s.exp(-d * r))
res1 = s.simplify(s.diff(u, r, 2) - 2 * (V + k**2 / 2) * u)
phi = 1 - s.exp(-2 * r)
re_h = s.integrate(2 * (1 - phi**2), (r, 0, s.oo))
# 2) x = pi/2 + a1/R + a2/R^2 ; -x cot x - re x^2/(2R) = 0 orden a orden
t = s.symbols('t')  # t = 1/R
a1, a2 = s.symbols('a1 a2')
X = s.pi / 2 + a1 * t + a2 * t**2
eq = s.series(-X * s.cos(X) / s.sin(X) - re * X**2 * t / 2, t, 0, 3).removeO()
sol = s.solve([eq.coeff(t, 1), eq.coeff(t, 2)], [a1, a2], dict=True)[0]
val = s.series((X.subs(sol))**2 / s.pi**2, t, 0, 3).removeO()
# 3) cruce: 1/a = -c eps ; -x cot x = R c eps + re x^2/(2R); q(R) = x/pi ; igualar q(R1) = q(R2) a primer orden
R1, R2 = s.symbols('R1 R2', positive=True)
def q(Rv):
    X = s.pi / 2 + s.Symbol('e1')
    e1 = s.Symbol('e1')
    lin = s.series(-X * s.cos(X) / s.sin(X), e1, 0, 2).removeO()       # = (pi/2) e1 + ...
    e1s = s.solve(s.Eq(lin, Rv * c * eps + re * (s.pi / 2)**2 / (2 * Rv)), e1)[0]
    return e1s
epsstar = s.solve(s.Eq(q(R1), q(R2)), eps)[0]   # mismo x = kR, es decir, mismo 2R^2E/pi^2
g = x - 1 + s.exp(-x) * s.cos(x)
out = dict(hulthen_residuo=str(res1), hulthen_re_umbral=str(re_h), caja_2R2E_pi2_igual_x2_sobre_pi2="ver siguiente",
           caja_x_sobre_pi_al_cuadrado=str(s.expand(val)), cruce_eps=str(s.simplify(epsstar)),
           ecsc_gprima=str(s.simplify(s.diff(g, x))), ecsc_hprima=str(s.simplify(s.diff(s.exp(-x) * (s.cos(x) + s.sin(x)), x))))
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'r03_teoria_simbolica.json'), 'w'), indent=1)
