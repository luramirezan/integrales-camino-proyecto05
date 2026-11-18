"""r5_ansatz.py -- Revision: sensibilidad del criterio de varianza del ansatz 1 + A/(r+b) (delta = 1.3, c = 1.25) al
radio final Rf. qeff = 2q - Ab/(r(r+b)^2(r+b+A)); varianza finita si la solucion regular no tiene nodos y alpha > 0.
Integracion propia (solve_ivp Radau en variable log) independiente de fk_comun. Tambien el cruce por cero en r > Rf."""
import json, os
import numpy as np
from scipy.integrate import solve_ivp
d = 1.3; a = -11.5799210238
out = {}
for c in [1.25, 2.0]:
    A = -c * a; b = (-A + np.sqrt(A*A + 4*A)) / 2
    qe = lambda r: 2*np.exp(-d*r)/r - A*b/(r*(r+b)**2*(r+b+A))
    for Rf in [46.15, 200.0, 2000.0, 20000.0]:
        r0 = 1e-8
        k0 = 2*(2 - b*A/(b*b*(b+A)))  # coeficiente de 1/r en 2 qeff... u = r - (k0/2) r^2
        s = solve_ivp(lambda r, y: [y[1], -2*qe(r)*y[0]], [r0, Rf], [r0 - k0/2*r0**2, 1 - k0*r0], method="DOP853",
                      rtol=1e-11, atol=1e-14, dense_output=True)
        rr = np.geomspace(r0, Rf, 200000); u = s.sol(rr)[0]
        nodos = int(np.sum(np.sign(u[1:]) != np.sign(u[:-1])))
        alpha = s.y[1, -1]
        out[f"c{c}_Rf{Rf:g}"] = dict(alpha=float(alpha), nodos=nodos, u_Rf=float(s.y[0, -1]))
        print(f"c={c} Rf={Rf}: alpha = {alpha:+.4e}, nodos = {nodos}, u(Rf) = {s.y[0,-1]:+.4e}")
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "r5_ansatz.json"), "w"), indent=1)
