"""06_fuentes: comprueba los numeros que aportan las referencias.
Unidades atomicas adimensionales: u'' = [l(l+1)/r^2 - 2 e^{-delta r}/r - 2E] u."""
import sympy as sp, numpy as np
from scipy.linalg import eigh_tridiagonal
r, d = sp.symbols('r delta', positive=True)
# Bargmann (l=0): n_0 < int_0^inf r |2V| dr con 2m/hbar^2 = 2 en u.a.
I = sp.integrate(r*2*sp.exp(-d*r)/r, (r, 0, sp.oo))
print("Integral de Bargmann =", I, "-> sin ligados si", sp.solve(sp.Eq(I, 1), d), "<= delta")
def E0(delta, N=6000, R=None):
    R = R or max(60.0, 40/max(1e-3, 1.2-delta+0.05))
    h = R/(N+1); x = h*np.arange(1, N+1)
    diag = 1/h**2 - np.exp(-delta*x)/x; off = -0.5/h**2*np.ones(N-1)
    return eigh_tridiagonal(diag, off, select='i', select_range=(0, 0))[0][0]
print("E0(delta=0) =", E0(0.0), "(esperado -0.5)")
# Ejemplo del SESGO DE CAJA (no es una determinacion de delta_c): umbral aparente de una
# sola caja de Dirichlet, es decir, el delta para el que E0 = 0 en [0, R] con u(R) = 0.
# Version corregida (21-10-2026): la version anterior biseccionaba el signo de E0 con
# diferencias finitas h = 0.02 y mezclaba un error de malla de ~ -2e-4 con el sesgo de caja.
# Ahora se integra u'' = -2 e^{-delta r}/r u a energia cero (serie de Frobenius cerca de 0 y
# DOP853 con rtol = 1e-13) y se busca u(R) = 0 con brentq: el resultado no depende de h.
# La determinacion independiente de R es el metodo C de la seccion 5 (u'(R) = 0 a E = 0).
from math import factorial
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
DC_REF = 1.19061242106   # Gebremedhin y Weatherford 2023 (via arXiv:2510.10420, tabla II)
def u_cero(delta, R, r0=0.05, M=40):
    """u(R) y u'(R) a E = 0 con u ~ r cerca del origen."""
    a = np.zeros(M); a[1] = 1.0
    ek = [(-delta)**k/factorial(k) for k in range(M)]
    for n in range(M-2):   # u'' = -2 e^{-delta r} u / r  ->  recurrencia de la serie
        a[n+2] = -2*sum(ek[k]*a[n-k+1] for k in range(n+1))/((n+2)*(n+1))
    n = np.arange(M)
    y0 = [np.sum(a*r0**n), np.sum(n[1:]*a[1:]*r0**(n[1:]-1))]
    f = lambda x, y: [y[1], -2*np.exp(-delta*x)/x*y[0]]
    return solve_ivp(f, (r0, R), y0, method='DOP853', rtol=1e-13, atol=1e-30).y[:, -1]
def umbral_caja(R):
    return brentq(lambda dl: u_cero(dl, R)[0], 1.10, 1.1905, xtol=1e-13)
for R in (100, 200, 400, 800):
    dcR = umbral_caja(R)
    print(f"R={R:4d}: umbral aparente de caja = {dcR:.6f}  sesgo = {dcR-DC_REF:+.3e}"
          f"  R*(dc - dc(R)) = {R*(DC_REF-dcR):.3f}")
print("referencia de alta precision (Gebremedhin y Weatherford 2023):", DC_REF)
