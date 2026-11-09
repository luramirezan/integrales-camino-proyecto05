"""Bloque 04: cotas superiores del umbral de enlace (Bargmann, Calogero, Schwinger/Birman-Schwinger)
para Yukawa adimensional: u'' = [ -2 e^{-delta x}/x + l(l+1)/x^2 - 2E ] u  (U(x) = 2 e^{-delta x}/x)."""
import os as _os
_RAIZ = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..','..'))  # raiz del repositorio
import sympy as sp, numpy as np
from scipy.integrate import solve_ivp, quad, dblquad
from scipy.optimize import brentq
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

x, y, d = sp.symbols('x y delta', positive=True)
U = 2*sp.exp(-d*x)/x
# Bargmann l=0: n < int x|U| dx
B = sp.simplify(sp.integrate(x*U, (x, 0, sp.oo)))
print("Bargmann  int x|U| =", B, "-> delta_max =", sp.solve(sp.Eq(B, 1), d))
# Calogero: n < (2/pi) int sqrt|U|
C = sp.simplify(2/sp.pi*sp.integrate(sp.sqrt(U), (x, 0, sp.oo)))
dC = sp.solve(sp.Eq(C, 1), d); print("Calogero  =", C, "-> delta_max =", dC, [sp.N(v) for v in dC])
# Birman-Schwinger Hilbert-Schmidt: 1 <= Tr K^2 = int int |U(x)||U(y)| min(x,y)^2
inner = sp.integrate(x*sp.exp(-d*x), (x, 0, y))
T2 = sp.simplify(8*sp.integrate(sp.exp(-d*y)/y*inner, (y, 0, sp.oo)))
dS = sp.solve(sp.Eq(T2, 1), d); print("Tr K^2 =", T2, "-> delta_max =", dS, [sp.N(v) for v in dS])
# Tr K^p numerico con discretizacion del nucleo simetrico K(x,y)=sqrt(U(x)) min(x,y) sqrt(U(y))
def K_eigs(delta, N=1500, L=60.0):
    t, w = np.polynomial.legendre.leggauss(N)
    # mapeo x = L*(s/(1-s))^? -> usar x = s/(1-s)*c
    s = 0.5*(t+1); c = 1.0/delta; xs = c*s/(1-s); ws = 0.5*w*c/(1-s)**2
    Ux = 2*np.exp(-delta*xs)/xs
    M = np.sqrt(ws*Ux)[:, None]*np.minimum.outer(xs, xs)*np.sqrt(ws*Ux)[None, :]
    return np.linalg.eigvalsh(M)[::-1]
def trp(delta, p): return np.sum(K_eigs(delta)**p)
for p in (1, 2, 3, 4):
    dp = brentq(lambda dd: trp(dd, p)-1, 0.5, 3)
    print(f"Tr K^{p}=1 -> delta_max = {dp:.6f}")
# umbral exacto: lambda_max(K)=1
dc_K = brentq(lambda dd: K_eigs(dd)[0]-1, 1.0, 1.5); print("lambda_max(K)=1 (N=1500 nodos Gauss-Legendre) -> delta_c =", dc_K)
print("cruce de la curva de Calogero con n0=1: 16/pi =", 16/np.pi, "; valor en delta=1:", 4/np.sqrt(np.pi))
# comprobacion por disparo a E=0: u(x) a x grande sin nodo
def nodes(delta):
    sol = solve_ivp(lambda r, z: [z[1], -2*np.exp(-delta*r)/r*z[0]], [1e-8, 200/1], [1e-8, 1.0], rtol=1e-11, atol=1e-14)
    return sol.y[1, -1]  # u'(inf) cambia de signo en el umbral
dc = brentq(nodes, 1.0, 1.5, xtol=1e-12); print("disparo E=0 -> delta_c =", dc)
print("verif. numerica Bargmann delta=0.7:", quad(lambda r: 2*np.exp(-0.7*r), 0, np.inf)[0], 2/0.7)

dd = np.linspace(0.5, 5.6, 300)
plt.figure(figsize=(7, 4.3))
plt.plot(dd, 2/dd, label=r"Bargmann $2/\delta$")
plt.plot(dd, 4/np.sqrt(np.pi*dd), label=r"Calogero $4/\sqrt{\pi\delta}$")  # (2/pi) int sqrt(U), U=2e^{-dx}/x
plt.plot(dd, 8*(np.log(2)-0.5)/dd**2, label=r"Schwinger (Tr$K^2$) $8(\ln2-\frac{1}{2})/\delta^2$")
plt.axhline(1, color='k', lw=.8); plt.axvline(16/np.pi, color='C1', ls=':', lw=.8)
plt.axvline(2, color='C0', ls=':', lw=.8); plt.axvline(2*np.sqrt(2*np.log(2)-1), color='C2', ls=':', lw=.8); plt.axvline(dc, color='gray', ls='--', label=rf"$\delta_c={dc:.4f}$")
plt.ylim(0, 3); plt.xlabel(r"$\delta=\mu a$"); plt.ylabel("cota de $n_0$")
plt.legend(); plt.title("Cotas superiores al numero de estados s ligados (Yukawa)"); plt.tight_layout()
plt.savefig(_RAIZ + "/fase1/figuras/04_cotas_superiores.png", dpi=150)
