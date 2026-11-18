"""e2comun.py -- utilidades comunes de la extension E2 (criterio de cruce de cajas), proyecto 05, Fase 4.

Unidades hbar = m = g = 1, V = -e^{-delta r}/r, onda s, esfera de pared dura de radio R.
Observable de escala: y(delta, R) = 2 R^2 E0(R) / pi^2 (punto fijo 1/4 en el umbral) y rho = <r>/R
(punto fijo 1/2 - 2/pi^2). Ver teoria.md.

Importa los modulos de la Fase 2 y la Fase 3 SIN copiarlos ni modificarlos (regla 1 del CONTEXTO_COMUN):
  comun3.resolver_tr / comun3.celda (integral de camino como matriz de transferencia, receta de la Fase 3),
  comun3.radial_ref (radial de diferencias finitas con Richardson), comun3.long_dispersion.
Aqui solo se anaden: el disparo sin malla (referencia "exacta" de E0 y <r> en la caja), la longitud de
dispersion y el rango efectivo a energia cero, y las funciones de escala de alcance cero F(z), G(z), z = R/a.
"""
import json
import os
import sys
import time

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(AQUI)                                   # .../E2_cruce_de_cajas
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(BASE)))  # .../project-files
RES = os.path.join(BASE, "resultados")
FIG = os.path.join(BASE, "figuras")
sys.path.insert(0, os.path.join(RAIZ, "fase3", "codigo"))
sys.path.insert(0, os.path.join(RAIZ, "fase2", "codigo"))
import comun3  # noqa: E402  (añade fase2/codigo a sys.path e importa pares, radial, transferencia)
import radial  # noqa: E402

DELTA_C_REF = comun3.DELTA_C_REF            # 1.1906124210606
Y_FIJO = 0.25                               # 2 R^2 E0 / pi^2 en el umbral (alcance cero)
RHO_FIJO = 0.5 - 2.0 / np.pi**2            # <r>/R en el umbral (alcance cero) = 0.29736...

# Rejilla fijada antes de correr (criterios_previos.md): 15 valores, mas densos cerca de 1.1906
DELTAS_INICIAL = (1.185, 1.187, 1.189, 1.190, 1.1903, 1.1905, 1.1906, 1.1907, 1.1908, 1.1909, 1.1910, 1.1912,
                  1.192, 1.194, 1.196)
# Nodos anadidos despues del primer analisis (control K7 de interpolacion no pasaba con la rejilla inicial en
# tres pares del disparo; ver verificacion.md). No cambia ningun umbral: solo densifica la rejilla.
DELTAS_EXTRA = (1.19061, 1.19062, 1.19063, 1.19065, 1.1911, 1.1914, 1.1916, 1.195)
DELTAS = tuple(sorted(DELTAS_INICIAL + DELTAS_EXTRA))
RS = (50, 100, 200, 400, 800, 1600, 3200)


def y_de(E, R):
    return 2.0 * R * R * E / np.pi**2


def guardar(nombre, obj):
    fn = os.path.join(RES, nombre + ".json")
    with open(fn, "w") as f:
        json.dump(obj, f, indent=1, default=float)
    return fn


def cargar(nombre):
    with open(os.path.join(RES, nombre + ".json")) as f:
        return json.load(f)


class Tee:
    """Duplica la salida impresa en resultados/<nombre>_salida.txt (regla 3)."""

    def __init__(self, nombre):
        self.f = open(os.path.join(RES, nombre + "_salida.txt"), "w")
        self.o = sys.stdout

    def write(self, s):
        self.o.write(s); self.f.write(s); self.f.flush()

    def flush(self):
        self.o.flush(); self.f.flush()


# --------------------------------------------------------------------------- disparo sin malla
R0 = 1e-7


def _rhs(delta, E, signo=-1.0):
    """u'' = 2 (V - E) u con V = signo * e^{-delta r}/r; tambien acumula int u^2 y int r u^2."""
    def f(r, s):
        u, up = s[0], s[1]
        return [up, 2.0 * (signo * np.exp(-delta * r) / r - E) * u, u * u, r * u * u]
    return f


def _ci(signo=-1.0):
    # Frobenius en r0: u = r + a2 r^2 con 2 a2 = 2*signo  ->  a2 = signo (para V = signo/r cerca de 0)
    return [R0 * (1 + signo * R0), 1 + 2 * signo * R0, 0.0, 0.0]


def disparo_u(delta, E, R, signo=-1.0, rtol=1e-12):
    s = solve_ivp(_rhs(delta, E, signo), [R0, R], _ci(signo), method="DOP853", rtol=rtol, atol=1e-30)
    return s.y[:, -1]


def disparo_E0(delta, R, E_guess, signo=-1.0, rtol=1e-12, ancho=None):
    """Estado base en la caja por disparo: raiz de u(R; E) = 0 en el intervalo que contiene E_guess.
    El intervalo se ensancha hasta encontrar el cambio de signo; se comprueba que no haya nodos
    (estado base) contando cambios de signo de u en una malla densa de la solucion final."""
    g = lambda E: disparo_u(delta, E, R, signo, rtol)[0]
    w = ancho if ancho is not None else max(abs(E_guess) * 1e-3, 1e-12)
    lo, hi = E_guess - w, E_guess + w
    glo, ghi = g(lo), g(hi)
    k = 0
    while glo * ghi > 0 and k < 60:
        w *= 2.0
        lo, hi = E_guess - w, E_guess + w
        glo, ghi = g(lo), g(hi)
        k += 1
    if glo * ghi > 0:
        raise RuntimeError("sin cambio de signo")
    E = brentq(g, lo, hi, xtol=1e-22, rtol=1e-15, maxiter=200)
    s = solve_ivp(_rhs(delta, E, signo), [R0, R], _ci(signo), method="DOP853", rtol=rtol, atol=1e-30,
                  dense_output=True)
    rr = np.linspace(R0, R, 20001)
    uu = s.sol(rr)[0]
    nodos = int(np.sum(np.sign(uu[1:-200]) != np.sign(uu[:-201])))
    n0, n1 = s.y[2, -1], s.y[3, -1]
    return dict(E0=float(E), r_med=float(n1 / n0), r_sobre_R=float(n1 / n0 / R), nodos=nodos,
                uR=float(s.y[0, -1]))


# --------------------------------------------------------------------------- energia cero
def energia_cero(delta, Rf=200.0, signo=-1.0, rtol=1e-13):
    """Solucion regular a E = 0 hasta Rf. Fuera del alcance u = A (r - a), a = r - u/u'.
    Devuelve a (convencion del CONTEXTO_COMUN: a > 0 si hay ligado) y el rango efectivo
    r_e = 2 int_0^inf [(1 - r/a)^2 - (u/A)^2] dr (formula de Bethe a energia cero)."""
    def f(r, s):
        u, up = s[0], s[1]
        return [up, 2.0 * signo * np.exp(-delta * r) / r * u]
    s = solve_ivp(f, [R0, Rf], [R0 * (1 + signo * R0), 1 + 2 * signo * R0], method="DOP853", rtol=rtol,
                  atol=1e-30, dense_output=True)
    uR, upR = s.y[0, -1], s.y[1, -1]
    a = Rf - uR / upR
    A = upR
    # integral de [(1 - r/a)^2 - (u/(-A a))^2]: con u -> A (r - a) = -A a (1 - r/a)
    rr = np.linspace(R0, Rf, 400001)
    uu = s.sol(rr)[0] / (-A * a)
    integ = (1.0 - rr / a)**2 - uu**2
    re = 2.0 * np.trapezoid(integ, rr)
    return dict(a=float(a), r_e=float(re), A=float(A))


def rango_efectivo_umbral(delta, Rf=200.0, rtol=1e-13):
    """En el umbral (1/a = 0) la solucion a E = 0 tiende a una constante C: r_e = 2 int (1 - (u/C)^2) dr."""
    def f(r, s):
        return [s[1], -2.0 * np.exp(-delta * r) / r * s[0]]
    s = solve_ivp(f, [R0, Rf], [R0 * (1 - R0), 1 - 2 * R0], method="DOP853", rtol=rtol, atol=1e-30,
                  dense_output=True)
    rr = np.linspace(R0, Rf, 400001)
    uu = s.sol(rr)[0]
    C = uu[-1]
    return float(2.0 * np.trapezoid(1.0 - (uu / C)**2, rr)), float(s.y[1, -1] / C)


# --------------------------------------------------------------------------- funciones de escala (alcance cero)
def x_de_z(z):
    """Solucion de la condicion de cuantizacion de alcance cero en la esfera dura, x cot x = z, z = R/a.
    Rama del estado base: x en (0, pi) para z < 1 (E > 0); x = 0 en z = 1; para z > 1, x = i q con
    q coth q = z (E < 0). Devuelve x^2 (real, negativo si ligado), de modo que y = x^2/pi^2."""
    z = float(z)
    if abs(z - 1.0) < 1e-14:
        return 0.0
    if z < 1.0:
        f = lambda x: x * np.cos(x) - z * np.sin(x)
        x = brentq(f, 1e-12, np.pi - 1e-15, xtol=1e-15)
        return x * x
    f = lambda q: q * np.cosh(q) - z * np.sinh(q)
    hi = max(2.0 * z, 1.0)
    q = brentq(f, 1e-12, hi, xtol=1e-15)
    return -q * q


def F_escala(z):
    """y = 2 R^2 E / pi^2 = x^2/pi^2 en el limite de alcance cero."""
    return x_de_z(z) / np.pi**2


def G_escala(z):
    """<r>/R en el limite de alcance cero: u = sin(x (1 - r/R)) (o sinh para el ligado), rho = 1 - <t>."""
    x2 = x_de_z(z)
    if abs(x2) < 1e-300:
        return 0.25                  # z = 1: u = t = 1 - r/R, <t> = 3/4, <r>/R = 1/4
    t = np.linspace(0.0, 1.0, 200001)
    if x2 > 0:
        u = np.sin(np.sqrt(x2) * t)
    else:
        u = np.sinh(np.sqrt(-x2) * t)
    w = u * u
    return float(1.0 - np.trapezoid(t * w, t) / np.trapezoid(w, t))


def G_umbral_cerrado():
    return RHO_FIJO


def ahora():
    return time.strftime("%Y-%m-%d %H:%M:%S")
