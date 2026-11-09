"""Verificacion independiente (V1): solucionador radial por DISPARO con solve_ivp (DOP853).
No usa nada de fase1/codigo ni de fase2/codigo. Unidades hbar=m=1.
Ecuacion: u'' = 2 (V(r) - E) u, u(0)=0.  Arranque en r0 con la serie u = r - Z r^2 (Z = -lim r V).
Se integran a la vez I0=int u^2, I1=int r u^2, I2=int r^2 u^2 (y la mitad de la caja por evento).
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

RTOL = 1e-12
ATOL = 1e-14

def yukawa(delta):
    if delta == 0:
        return lambda r: -1.0 / r
    return lambda r: -np.exp(-delta * r) / r

def hulthen(delta):
    return lambda r: -delta * np.exp(-delta * r) / (-np.expm1(-delta * r))

def _rhs(V, E):
    def f(r, y):
        u, up = y[0], y[1]
        u2 = u * u
        return [up, 2.0 * (V(r) - E) * u, u2, r * u2, r * r * u2]
    return f

def _arranque(Z, r0):
    return [r0 - Z * r0**2, 1.0 - 2.0 * Z * r0, 0.0, 0.0, 0.0]

def integra(V, E, a, b, y0, saltos=(), max_step=np.inf):
    """Integra de a a b (a<b o a>b), partiendo en los saltos del potencial."""
    pts = [a] + [s for s in sorted(saltos, reverse=(b < a)) if min(a, b) < s < max(a, b)] + [b]
    y = np.array(y0, float)
    for p, q in zip(pts[:-1], pts[1:]):
        # para que V se evalue del lado correcto del salto, se integra en el abierto
        sol = solve_ivp(_rhs(V, E), (p, q), y, method="DOP853", rtol=RTOL, atol=ATOL, max_step=max_step)
        y = sol.y[:, -1]
    return y

def caja(V, E, R, Z=1.0, r0=1e-7, saltos=()):
    """u(R) y las integrales para disparo de 0 a R."""
    return integra(V, E, r0, R, _arranque(Z, r0), saltos)

def autovalor_caja(V, R, Ebajo, Ealto, Z=1.0, saltos=(), xtol=1e-15):
    f = lambda E: caja(V, E, R, Z, saltos=saltos)[0]
    E = brentq(f, Ebajo, Ealto, xtol=xtol, rtol=1e-15, maxiter=200)
    return E

def observables_caja(V, E, R, Z=1.0, saltos=()):
    yh = caja(V, E, R / 2.0, Z, saltos=saltos)
    y = integra(V, E, R / 2.0, R, yh, saltos)
    I0, I1, I2 = y[2], y[3], y[4]
    return dict(E0=E, r=I1 / I0, r2=I2 / I0, rrms=np.sqrt(I2 / I0), F12=yh[2] / I0, r_sobre_R=I1 / I0 / R, uR=y[0])

def primeros_ceros(V, R, Emin, Emax, n, Z=1.0, saltos=(), npts=400):
    """Primeros n autovalores de caja buscando cambios de signo de u(R;E) en una rejilla de E."""
    Es = np.linspace(Emin, Emax, npts)
    vals = np.array([caja(V, E, R, Z, saltos=saltos)[0] for E in Es])
    raices = []
    for i in range(len(Es) - 1):
        if vals[i] == 0 or vals[i] * vals[i + 1] < 0:
            raices.append(autovalor_caja(V, R, Es[i], Es[i + 1], Z, saltos))
            if len(raices) == n:
                break
    return raices

# ---------- energia cero: umbral y longitud de dispersion ----------
def cero(V, rmax, Z=1.0, r0=1e-7):
    y = integra(V, 0.0, r0, rmax, _arranque(Z, r0))
    u, up = y[0], y[1]
    return u, up, rmax - u / up   # a_s = r - u/u' (u -> r - a_s)

def umbral(fV, d1, d2, rmax_fun, Z=1.0):
    return brentq(lambda d: cero(fV(d), rmax_fun(d), Z)[1], d1, d2, xtol=1e-15, rtol=1e-15)

# ---------- estado ligado en espacio libre: disparo hacia afuera y hacia adentro ----------
def _empalme(V, E, rm, rmax, Z, saltos, r0=1e-7):
    yo = integra(V, E, r0, rm, _arranque(Z, r0), saltos)
    k = np.sqrt(-2.0 * E)
    yi = integra(V, E, rmax, rm, [np.exp(-k * (rmax - rm)) * 1e-0, -k * np.exp(-k * (rmax - rm)), 0, 0, 0], saltos)
    return yo, yi

def ligado(V, Ebajo, Ealto, rm, rmax=None, Z=1.0, saltos=()):
    """Raiz en E de la diferencia de derivadas logaritmicas en rm. rmax por defecto: kappa*rmax = 45."""
    def g(E):
        rM = rmax if rmax is not None else rm + 45.0 / np.sqrt(-2 * E)
        yo, yi = _empalme(V, E, rm, rM, Z, saltos)
        return yo[1] / yo[0] - yi[1] / yi[0]
    E = brentq(g, Ebajo, Ealto, xtol=1e-16, rtol=1e-15, maxiter=200)
    rM = rmax if rmax is not None else rm + 45.0 / np.sqrt(-2 * E)
    yo, yi = _empalme(V, E, rm, rM, Z, saltos)
    s = yo[0] / yi[0]
    I = [yo[2 + j] - s * s * yi[2 + j] for j in range(3)]   # tramo de adentro se integro hacia atras
    return dict(E0=E, r=I[1] / I[0], r2=I[2] / I[0], rrms=np.sqrt(I[2] / I[0]), up0=1.0 / np.sqrt(I[0]))
