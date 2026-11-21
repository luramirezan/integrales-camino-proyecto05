# Material para auditoría (parte 2 de 3)

Responde solo "Recibido".

## controles.md

# Controles de la extensión E1 (generado por `codigo/07_documentos.py` desde los JSON)

Los criterios se escribieron en la cabecera de cada script **antes** de correrlo (17-11-2026) y no se cambiaron
después. Pasan 9 de 12.

| # | control | criterio fijado antes | valor | ¿pasa? | script |
|---|---|---|---|---|---|
| C1 | delta_c(1s) con dos metodos frente a la referencia | \|A-ref\| < 1e-9 y \|B-ref\| < 1e-9 | A-ref = 4.0e-15; B-ref = -1.3e-10 | pasa | `01_umbral_y_controles.py` |
| C2 | Coulomb exacto (delta = 0), metodos A y B | A: \|E0+1/2\|<1e-9, \|<r>-3/2\|<1e-7, \|<r2>-3\|<1e-6; B: \|E0+1/2\|<1e-6 | A: 1.7e-16, -5.8e-15, -1.6e-14; B: 6.1e-09 | pasa | `01_umbral_y_controles.py` |
| C3 | Hulthen exacto (delta = 1), metodo A | \|E0-E_ex\| < 1e-10, \|<r>-<r>_ex\| < 1e-8 | -1.6e-15; -6.7e-15 | pasa | `01_umbral_y_controles.py` |
| C4 | delta_c(2s) y delta_c(3s), A frente a B | \|A-B\| < 1e-8 | 2s: 8.4e-11; 3s: 6.5e-11 | pasa | `01_umbral_y_controles.py` |
| C5 | Formula de Debye en SI frente al coeficiente del NRL Plasma Formulary | \|coef/743 - 1\| < 1e-3 | 743.394 cm (rel 5.3e-04) | pasa | `02_plasma.py` |
| C6 | Longitud critica frente a Rogers, Graboske y Harwood 1970 (D0 = 0.83991 a0) | \|1/delta_c - 0.83991\| < 5e-6 (ultima cifra publicada) | 0.8399039 | **no pasa** | `02_plasma.py` |
| C7 | Energia del 1s en 8 valores de delta: disparo (A) frente a caja (B) | max \|E_A - E_B\|/\|E_A\| < 1e-6 | 1.4e-04 | **no pasa** | `02_plasma.py` |
| C8 | Primera resonancia s de Tulin, Yu y Zurek (b = 1.68) frente a 2/delta_c | \|2/delta_c - 1.68\| <= 0.005 | 2/delta_c = 1.67981 | pasa | `03_materia_oscura.py` |
| C9 | Antirresonancia s (a_s = 0) frente a Tulin, Yu y Zurek (b = 4.52); A frente a B | \|b - 4.52\| <= 0.005 y \|delta_A - delta_B\| < 1e-6 | b = 4.4657; dif A-B = 1.6e-09 | **no pasa** | `03_materia_oscura.py` |
| C10 | Energia de enlace: m_p + m_n - m_d frente al dato E_B(d) de CODATA 2022 | \|dif\| < 1e-6 MeV | -0.03 eV | pasa | `04_deuteron.py` |
| C11 | Reproduccion del prototipo con sus mismas entradas | \|delta - 0.8304596701595315\| < 1e-9 | 1.9e-13 | pasa | `04_deuteron.py` |
| C12 | Deuteron central: disparo (A) frente a caja (B); caja R frente a 2R | delta: <1e-7 rel; <r>, <r2>: <1e-5 rel; E(R) vs E(2R): <1e-9 rel | 2.5e-08; 1.5e-08, 8.1e-08; 1.5e-11 | pasa | `04_deuteron.py` |

## Controles que no pasan y su causa medida

- **C6** (Rogers, Graboske y Harwood 1970). Nuestro $1/\delta_c$ = 0.8399039 redondea a 0.83990, y el resumen
  del artículo de 1970 da 0.83991. La diferencia, 6.1e-06, es mayor que media unidad de la
  última cifra publicada, que fue el criterio fijado. Nuestro valor coincide con las Fases 1 a 3 y con dos métodos
  independientes a 10^-10 (C1), así que atribuimos la diferencia a la precisión de 1970 (integración numérica de la
  época); la revisión adversarial lo confirmó con un tercer método (fase de Prüfer, `revision/`). La tabla 1 de
  Janev et al. (2016) da 0.839907, que también redondea a 0.83991 y queda 3 ppm por encima del nuestro. No cambia
  ninguna conclusión física: es una diferencia de 7 partes por millón en la longitud crítica.
- **C7** (energía del 1s, disparo frente a caja). El criterio relativo de 10^-6 se fijó antes de correr y falla
  cerca del umbral: la diferencia **absoluta** entre los dos métodos es casi constante, entre
  4.3e-09 y 6.7e-09 hartree, y al dividir
  por una energía que tiende a cero crece hasta 1.4e-04 en $\delta = 1.18$.
  La verificación V1 muestra la causa: con $h = 1/80$ en el método de caja la diferencia absoluta baja en un factor
  15.6 a 16.2 (el 16 esperado para el
  error de orden 4 que deja Richardson), así que el error es de discretización del método B con $h=1/40$, no del
  disparo. Con $h = 1/80$ la diferencia relativa máxima es 8.9e-06, todavía
  por encima de 10^-6 en $\delta = 1.18$; no damos el control por aprobado.
- **C9** (antirresonancia de Tulin, Yu y Zurek). Encontramos $a_s = 0$ en $\delta = 0.44785728$,
  es decir, $b = \alpha m_\chi/m_\phi = 4.4657$, con dos métodos que coinciden a
  2e-09. El artículo menciona una
  antirresonancia en $b = 4.52$ (1.2% más arriba). La causa es de
  definición, no un error nuestro ni de la fuente: 4.52 es la etiqueta de una de las curvas ilustrativas de su
  figura 3 (sección eficaz frente a velocidad con $\alpha_X = 0.01$), elegida para mostrar la supresión, y el
  artículo no dice que sea el cero de $a_s$ a velocidad nula. La revisión midió dos cosas que lo explican: la
  fórmula de Hulthén del mismo artículo (Sec. VI, $b = \kappa r^2$ con $r = 1.6909$) pone la
  antirresonancia en $b = 4.575$ con $\kappa = 1.6$, y el cero de la fase s del Yukawa
  se mueve con la velocidad: con $kL = v/\alpha = 0.05$ y 0.06 sale en $b = 4.502$ y
  4.518 (`revision/r03_antirresonancia_y_extras.py`). El control, tal como lo fijamos, no
  pasa; el criterio estaba mal planteado porque comparaba un cero exacto con un valor ilustrativo.


## codigo/comun_e1.py

```python
"""comun_e1.py -- utilidades de la extension E1 (contexto fisico del umbral), proyecto 05.

Problema adimensional (Fases 1-3): -u''/2 - e^{-delta r}/r u = eps u, u(0)=0, hbar = m = g = 1.
Unidad de longitud L = hbar^2/(m g); unidad de energia m g^2/hbar^2; delta = mu_s L, con mu_s la
inversa de la longitud de apantallamiento. 'm' es la masa del termino cinetico (masa reducida).

Dos metodos independientes para el estado 1s:
  Metodo A (este archivo): disparo con solve_ivp (DOP853) hacia afuera desde r0 y hacia adentro desde
     R_lejos con la solucion que decae, empalme del cociente u'/u en r_m; observables <r>, <r^2> por
     integracion de u^2 junto con la EDO. No usa caja.
  Metodo B: diferencias finitas en caja de Dirichlet con Richardson (fase2/codigo/radial.py a traves de
     fase3/codigo/comun3.py:radial_ref). Se importa, no se copia.
Umbral delta_c:
  Metodo A: pendiente de la solucion de energia cero (radial.umbral, solve_ivp).
  Metodo B: Numerov propio a energia cero en malla uniforme, con Richardson en h (independiente de solve_ivp).

Constantes fisicas: cada una con su fuente (ver fuentes.md). Nada se escribe a mano en el texto: todo pasa
por los JSON de resultados/.
"""
import json
import os
import sys
import time

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(AQUI)                       # .../E1_contexto_fisico
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(BASE)))   # /mnt/project-files
RES = os.path.join(BASE, "resultados")
FIG = os.path.join(BASE, "figuras")
for p in (os.path.join(RAIZ, "fase2", "codigo"), os.path.join(RAIZ, "fase3", "codigo")):
    if p not in sys.path:
        sys.path.insert(0, p)
import radial            # noqa: E402  (Fase 2, sin modificar)
import comun3            # noqa: E402  (Fase 3, sin modificar)

DELTA_C_REF = comun3.DELTA_C_REF   # 1.1906124210606 (Fases 1-3)

# ----------------------------------------------------------------------------- constantes (con fuente)
# CODATA 2022 (Mohr et al., Rev. Mod. Phys. 97, 025002 (2025)), tal como las lista la tabla de constantes
# del PDG 2025 (rpp2025-rev-phys-constants.pdf) y el archivo allascii.txt de NIST. Verificadas el 17-11-2026.
CONST = dict(
    m_p=938.27208943,          # MeV, u = 0.00000029
    m_n=939.56542194,          # MeV, u = 0.00000048
    m_d=1875.61294500,         # MeV, u = 0.00000058
    m_e=0.51099895069,         # MeV
    hbar_c=197.3269804,        # MeV fm (exacta)
    a0=5.29177210544e-11,      # m (radio de Bohr, con m_e)
    e=1.602176634e-19,         # C (exacta)
    eps0=8.8541878188e-12,     # F/m
    kB_eV=8.617333262e-5,      # eV/K (exacta)
    E_h_eV=2 * 13.605693122990,  # eV, energia de Hartree = 2 Ry
    E_B_d_codata_keV=2224.56640,  # keV, dato de entrada de CODATA 2022 (Sec. II.2), u = 0.00038
    r_d_fm=2.12778,            # fm, radio cuadratico medio de carga del deuteron (CODATA 2022), u = 0.00027
    r_d_u_fm=0.00027,
    r_p_fm=0.84075,            # fm, radio de carga del proton (CODATA 2022), u = 0.00064
    r_p_u_fm=0.00064,
    # PDG 2025 (rpp2025-tab-mesons-light.pdf)
    m_pi_pm=139.57039,         # MeV, u = 0.00018
    m_pi_0=134.9768,           # MeV, u = 0.0005
    # r_n^2: PDG 2024 (rpp2024-tab-baryons-N.pdf, espejo de KEK) y pdgLive: -0.1155(17) fm^2. [Revision R1-01: antes
    # se usaba -0.1161(22), el promedio antiguo del PDG que cita Filin et al. (2020) solo para comparar.]
    rn2_fm2=-0.1155, rn2_u_fm2=0.0017,
    rn2_filin_pdg_antiguo=-0.1161,
    # r_d^2 - r_p^2 = 3.82070(31) fm^2 por el desplazamiento isotopico H-D 1S-2S (Filin et al., Ec. 1, que cita a
    # Pachucki, Patkos y Yerokhin 2018). Solo se usa para la incertidumbre: r_d y r_p de CODATA estan casi totalmente
    # correlacionados y sumar sus incertidumbres como independientes la sobreestima. [Revision R1-04]
    rd2_rp2_iso_u_fm2=0.00031,
    r_str_filin_fm=1.9731, r_str_filin_up=0.0013, r_str_filin_dn=0.0018,   # Ec. (9) de Filin et al.
    # NPLQCD, PRD 87, 034506 (2013), arXiv:1206.5219, Sec. III (p. 8) y Tabla VII (p. 11)
    lat_m_pi=805.9, lat_m_pi_u=(0.6, 0.4, 8.9),
    lat_M_B=1634.0, lat_M_B_u=(0.0, 0.0, 18.0),
    lat_B_d=19.5, lat_B_d_u=(3.6, 3.1, 0.2),
    # Berengut et al., PRD 87 (2013), arXiv:1301.1738, Ec. (4.1) y Tabla I
    K_deut_q=-0.86, K_deut_q_up=0.45, K_deut_q_dn=0.50, K_pi_q=0.494,
    K_N_q=0.048,               # Berengut et al., Ec. (2.4): K_N^q = 0.048(+0.002/-0.006) [Revision R1-05]
    # NRL Plasma Formulary (Huba, ed. 2004), p. 29: lambda_D = 7.43e2 (T/n)^{1/2} cm, T en eV, n en cm^-3
    nrl_coef_cm=7.43e2,
    # Rogers, Graboske y Harwood, PRA 1, 1577 (1970), resumen: D0(1s) = 0.83991 a0/Z
    rgh_D0=0.83991,
    # Tulin, Yu y Zurek, PRD 87, 115007 (2013), arXiv:1302.3898, Sec. IV B: primera resonancia s en b = 1.68,
    # antirresonancia s en b = 4.52, con b = alpha m_X/m_phi y masa reducida m_X/2
    tyz_b_res=1.68, tyz_b_antires=4.52, tyz_kappa_hulthen=1.6,
    # Tulin, Yu y Zurek, Sec. VI: antirresonancia de Hulthen en b = kappa r^2, r raiz de 2 gamma + psi(1+r) + psi(1-r) = 0
    # (r ~ 1.69). Nota de la revision (R1-03): 1.68 y 4.52 son las etiquetas de curvas ilustrativas de su Fig. 3,
    # no umbrales ni ceros calculados con precision.
)


def guardar(nombre, datos, salida_txt=None):
    os.makedirs(RES, exist_ok=True)
    with open(os.path.join(RES, nombre + ".json"), "w") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False, default=float)
    if salida_txt is not None:
        with open(os.path.join(RES, nombre + "_salida.txt"), "w") as f:
            f.write(salida_txt)


def leer(nombre):
    with open(os.path.join(RES, nombre + ".json")) as f:
        return json.load(f)


class Registro:
    """Imprime y acumula la salida para guardarla en <nombre>_salida.txt."""
    def __init__(self):
        self.lineas = []

    def __call__(self, *a):
        s = " ".join(str(x) for x in a)
        print(s, flush=True)
        self.lineas.append(s)

    def texto(self):
        return "\n".join(self.lineas) + "\n"


# ----------------------------------------------------------------------------- metodo A: disparo sin caja
def _V(delta, perfil="yukawa"):
    if perfil == "yukawa":
        return lambda r: -np.exp(-delta * r) / r
    if perfil == "hulthen":          # control exacto: E = -(1/2)(1 - delta/2)^2
        return lambda r: -delta / np.expm1(min(delta * r, 700.0))
    raise ValueError(perfil)


def _afuera(E, V, r0, rm):
    """Solucion regular desde r0 hasta rm. y = [u, u', int u^2, int r u^2, int r^2 u^2]."""
    def f(r, y):
        u = y[0]
        return [y[1], 2.0 * (V(r) - E) * u, u * u, r * u * u, r * r * u * u]
    # u ~ r (1 - r) cerca de 0 para V ~ -1/r (u'' = -2u/r + ...)
    y0 = [r0 * (1 - r0), 1 - 2 * r0, 0.0, 0.0, 0.0]
    s = solve_ivp(f, [r0, rm], y0, method="DOP853", rtol=1e-12, atol=1e-30)
    return s.y[:, -1]


def _adentro(E, V, rm, Rl):
    """Solucion que decae, desde Rl hasta rm (integracion estable hacia adentro)."""
    k = np.sqrt(-2.0 * E)

    def f(r, y):
        u = y[0]
        return [y[1], 2.0 * (V(r) - E) * u, u * u, r * u * u, r * r * u * u]
    y0 = [1.0, -k, 0.0, 0.0, 0.0]
    s = solve_ivp(f, [Rl, rm], y0, method="DOP853", rtol=1e-12, atol=1e-30)
    return s.y[:, -1]       # las integrales salen negativas (se integra de Rl a rm < Rl)


def _rm_Rl(E):
    k = np.sqrt(-2.0 * E)
    rm = min(max(2.0, 1.0 / k), 40.0)        # empalme en la zona interna
    Rl = rm + 40.0 / k                        # e^{-40} relativo: la cola restante es despreciable
    return rm, Rl


def desajuste(E, delta, perfil="yukawa", r0=1e-8):
    V = _V(delta, perfil)
    rm, Rl = _rm_Rl(E)
    a = _afuera(E, V, r0, rm)
    b = _adentro(E, V, rm, Rl)
    # diferencia de derivadas logaritmicas, acotada (wronskiano normalizado)
    return (a[1] * b[0] - b[1] * a[0]) / np.hypot(a[0], a[1]) / np.hypot(b[0], b[1])


def estado_1s_disparo(delta, perfil="yukawa", Emin=None, xtol=1e-15):
    """Energia y observables del estado fundamental l=0 sin caja (metodo A)."""
    t = time.perf_counter()
    if Emin is None:
        Emin = -0.52          # por debajo del fundamental de Coulomb (-1/2), cota inferior para todo delta >= 0
    # el fundamental es el unico cero si delta > delta_c(2s) = 0.31; para delta menores se busca el mas bajo
    Es = -np.logspace(np.log10(-Emin), -6, 36)
    vals = [desajuste(E, delta, perfil) for E in Es]
    E0 = None
    for i in range(len(Es) - 1):
        if np.sign(vals[i]) != np.sign(vals[i + 1]) and abs(vals[i]) < 1 and abs(vals[i + 1]) < 1:
            E0 = brentq(desajuste, Es[i], Es[i + 1], args=(delta, perfil), xtol=xtol, rtol=1e-15)
            break
    if E0 is None:
        return dict(E0=float("nan"), ligado=False)
    V = _V(delta, perfil)
    rm, Rl = _rm_Rl(E0)
    a = _afuera(E0, V, 1e-8, rm)
    b = _adentro(E0, V, rm, Rl)
    c = a[0] / b[0]                        # escala la cola para que u sea continua en rm
    N = a[2] - c * c * b[2]
    R1 = a[3] - c * c * b[3]
    R2 = a[4] - c * c * b[4]
    return dict(E0=float(E0), ligado=True, r_med=float(R1 / N), r2_med=float(R2 / N),
                kappa=float(np.sqrt(-2 * E0)), rm=float(rm), Rl=float(Rl), t=time.perf_counter() - t)


# ----------------------------------------------------------------------------- metodo B: caja (Fases 2-3)
def caja_para(E_aprox, Rmin=60.0, factor=30.0):
    R = radial.caja_recomendada(E_aprox, Rmin=Rmin, factor=factor)
    return float(np.ceil(R / 10.0) * 10.0)


def estado_1s_caja(delta, R, h=1 / 40):
    c = comun3.radial_ref(delta, R, h=h)
    c["R"] = float(R)
    c["h"] = float(h)
    return c


# ----------------------------------------------------------------------------- umbral delta_c(ns)
def umbral_A(a=1.1, b=1.3, R=200.0):
    """radial.umbral: u'(R)=0 para la solucion de energia cero (solve_ivp, Fase 2)."""
    return radial.umbral(radial.V_yukawa, a, b, R=R)


def _numerov_pendiente(delta, h, R=60.0, con_u=False):
    """Numerov a E=0: u'' = 2 V u. Devuelve la pendiente en r_{N-2} (diferencia centrada de 4.o orden);
    con_u=True devuelve (r_{N-2}, u_{N-2}, u'_{N-2})."""
    N = int(round(R / h))
    r = h * np.arange(N + 1)
    k2 = np.zeros(N + 1)                  # u'' = -k2 u, k2 = -2V = 2 e^{-delta r}/r
    k2[1:] = 2.0 * np.exp(-delta * r[1:]) / r[1:]
    u = np.zeros(N + 1)
    # u(0)=0; u(h) de la serie u = r - r^2 + ((1 + delta)/3) r^3 (de u'' = -2 e^{-delta r} u/r)
    u[1] = h - h * h + (1.0 + delta) / 3.0 * h ** 3
    # k2[0]*u[0] es el limite r->0 de (2/r) u = 2; se incluye como termino fuente f0 = -2
    f = -k2 * u
    f[0] = -2.0
    c = h * h / 12.0
    for n in range(1, N):
        # (1 + c k2_{n+1}) u_{n+1} = 2 u_n - u_{n-1} + c (f_{n-1} + 10 f_n)  con f = u''
        u[n + 1] = (2 * u[n] - u[n - 1] + c * (f[n - 1] + 10 * f[n])) / (1 + c * k2[n + 1])
        f[n + 1] = -k2[n + 1] * u[n + 1]
    up = (u[N - 4] - 8 * u[N - 3] + 8 * u[N - 1] - u[N]) / (12 * h)   # derivada centrada en r_{N-2}
    if con_u:
        return r[N - 2], u[N - 2], up
    return up


def umbral_B(hs=(1 / 200, 1 / 400), a=1.15, b=1.25, R=60.0, ns=None):
    """Numerov propio; brentq en delta para cada h y Richardson con orden aparente medido."""
    out = []
    for h in hs:
        out.append(brentq(lambda d: _numerov_pendiente(d, h, R), a, b, xtol=1e-14))
    return out


def long_dispersion_A(delta, R=200.0):
    """a_s = R - u(R)/u'(R) de la solucion de energia cero (solve_ivp). Signo: a_s > 0 si hay ligado cerca."""
    V = radial.V_yukawa(delta)
    f = lambda r, y: [y[1], 2.0 * float(V(np.array([r]))[0]) * y[0]]
    s = solve_ivp(f, [1e-8, R], [1e-8, 1.0], method="DOP853", rtol=1e-13, atol=1e-16)
    u, up = s.y[0, -1], s.y[1, -1]
    return float(R - u / up)


def long_dispersion_B(delta, h=1 / 400, R=200.0):
    r, u, up = _numerov_pendiente(delta, h, R, con_u=True)
    return float(r - u / up)

```

## codigo/02_plasma.py

```python
"""02_plasma.py -- hidrogeno en un plasma de Debye (modelo de Yukawa estatico).

Correspondencia: V(r) = -(e^2/4 pi eps0) e^{-r/lambda_D}/r. Con m = masa del termino cinetico y g = e^2/4 pi eps0,
L = hbar^2/(m g). Si m = m_e (nucleo infinito, como Rogers et al. 1970), L = a0 y delta = a0/lambda_D.
Con la masa reducida m_e m_p/(m_e+m_p), L = a0 (1 + m_e/m_p).

Longitud de Debye (NRL Plasma Formulary, Huba 2004, p. 29), solo electrones:
    lambda_De = (eps0 k T_e/(n_e e^2))^{1/2}  [SI]  = (kT/4 pi n e^2)^{1/2} [gaussiano] = 7.43e2 (T_eV/n_cm3)^{1/2} cm.
Variante con electrones y protones a la misma T (suma de inversas al cuadrado): lambda = lambda_De/sqrt(2).
La curva de "desaparicion del 1s" es lambda_D = L/delta_c:
    n_e(T) = eps0 k T delta_c^2/(e^2 L^2)    (solo electrones)
Indicadores de validez del modelo estatico de Debye-Huckel, evaluados SOBRE la curva:
    N_D = (4 pi/3) n_e lambda_D^3 (particulas en la esfera de Debye; DH requiere N_D >> 1),
    Gamma_e = e^2/(4 pi eps0 a_ws k T), a_ws = (3/(4 pi n_e))^{1/3} (acoplamiento; DH requiere Gamma << 1),
    Theta = k T/E_F, E_F = hbar^2 (3 pi^2 n_e)^{2/3}/(2 m_e) (degeneracion; DH clasico requiere Theta >> 1).
Ademas: energia del 1s, E(lambda_D), con los metodos A y B, en eV (unidad m g^2/hbar^2 = 1 Hartree).
Salida: resultados/02_plasma.json, figuras/02_plasma_diagrama.png, figuras/02_plasma_energia.png
"""
import time

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import comun_e1 as c

log = c.Registro()
t0 = time.perf_counter()
K = c.CONST
U1 = c.leer("01_umbral")
dc = U1["delta_c_1s"]["A"]

a0 = K["a0"]
me_mp = K["m_e"] / K["m_p"]
L_inf = a0
L_red = a0 * (1 + me_mp)
lam_c = L_inf / dc
lam_c_red = L_red / dc
log(f"delta_c = {dc:.13f}")
log(f"lambda_D critica (nucleo infinito)   = {lam_c / a0:.7f} a0 = {lam_c * 1e12:.4f} pm")
log(f"lambda_D critica (masa reducida)     = {lam_c_red / a0:.7f} a0")
log(f"Rogers, Graboske y Harwood 1970: D0(1s) = {K['rgh_D0']} a0/Z ; nuestro 1/delta_c = {1 / dc:.6f}")

# --- comprobacion de la formula NRL con constantes SI
e, eps0 = K["e"], K["eps0"]
kT1 = 1.0 * e                      # 1 eV en J
lam_1 = np.sqrt(eps0 * kT1 / (1e6 * e * e))   # n = 1 cm^-3 = 1e6 m^-3, en m
coef_cm = lam_1 * 100.0
log(f"coeficiente de Debye recalculado = {coef_cm:.4f} cm  (NRL: {K['nrl_coef_cm']})")

hbar = K["hbar_c"] * 1e6 * e * 1e-15 / 299792458.0      # J s, a partir de hbar c en MeV fm
me_kg = K["m_e"] * 1e6 * e / 299792458.0 ** 2


def n_crit(T_eV, especies="e"):
    """densidad electronica (m^-3) en la que lambda_D = lam_c, a temperatura T_eV."""
    fac = 1.0 if especies == "e" else 0.5
    return fac * eps0 * T_eV * e * dc ** 2 / (e * e * a0 ** 2)


def indicadores(n, T_eV, lam):
    ND = 4 * np.pi / 3 * n * lam ** 3
    aws = (3 / (4 * np.pi * n)) ** (1 / 3)
    Gam = e * e / (4 * np.pi * eps0 * aws * T_eV * e)
    EF = hbar ** 2 * (3 * np.pi ** 2 * n) ** (2 / 3) / (2 * me_kg) / e     # eV
    return ND, Gam, T_eV / EF, aws


Ts = np.logspace(-1, 4, 51)        # 0.1 eV a 10 keV
tab = []
for T in Ts:
    n = n_crit(T)
    ND, G, Th, aws = indicadores(n, T, lam_c)
    tab.append(dict(T_eV=float(T), n_e_m3=float(n), n_e_cm3=float(n * 1e-6), N_D=float(ND), Gamma=float(G),
                    Theta=float(Th), a_ws_sobre_lambdaD=float(aws / lam_c),
                    n_e_cm3_con_iones=float(n_crit(T, "ei") * 1e-6)))
puntos = {}
for T in (1.0, 13.6, 100.0, 1000.0):
    n = n_crit(T)
    ND, G, Th, aws = indicadores(n, T, lam_c)
    puntos[f"{T:g}"] = dict(T_eV=T, n_e_cm3=float(n * 1e-6), n_e_cm3_con_iones=float(n_crit(T, "ei") * 1e-6),
                            N_D=float(ND), Gamma=float(G), Theta=float(Th), a_ws_sobre_lambdaD=float(aws / lam_c))
    log(f"T = {T:7g} eV: n_e = {n * 1e-6:.3e} cm^-3 (con iones {n_crit(T, 'ei') * 1e-6:.3e}),"
        f" N_D = {ND:.3e}, Gamma = {G:.3f}, T/E_F = {Th:.3f}, a_ws/lambda_D = {aws / lam_c:.3f}")
# N_D sobre la curva es proporcional a T: temperatura en la que N_D = 1 y en la que N_D = 10
T_ND1 = float(1.0 / puntos["1"]["N_D"])
log(f"Sobre la curva N_D = {puntos['1']['N_D']:.4e} * (T/eV); N_D = 1 en T = {T_ND1:.1f} eV,"
    f" N_D = 10 en T = {10 * T_ND1:.0f} eV")

# --- energia del 1s frente a lambda_D (dos metodos), en eV
Eh = K["E_h_eV"]
deltas = [0.2, 0.4, 0.6, 0.8, 1.0, 1.1, 1.15, 1.18]
curva = []
for d in deltas:
    A = c.estado_1s_disparo(d)
    R = c.caja_para(A["E0"], Rmin=60.0, factor=30.0)
    B = c.estado_1s_caja(d, R)
    curva.append(dict(delta=d, lambda_D_a0=1 / d, E_A_hartree=A["E0"], E_B_hartree=B["E0"], R_caja=R,
                      dif_rel=abs(A["E0"] - B["E0"]) / abs(A["E0"]), E_A_eV=A["E0"] * Eh,
                      r_med_A=A["r_med"], r_med_B=B["r_med"]))
    log(f"delta = {d:5.2f} (lambda_D = {1 / d:6.3f} a0): E_A = {A['E0']:.10f} Ha, E_B = {B['E0']:.10f} Ha"
        f" (R = {R:g}), |dif|/|E| = {abs(A['E0'] - B['E0']) / abs(A['E0']):.1e}, E = {A['E0'] * Eh:.5f} eV")

out = dict(delta_c=dc, lambda_c_a0=lam_c / a0, lambda_c_red_a0=lam_c_red / a0, lambda_c_pm=lam_c * 1e12,
           rgh_D0=K["rgh_D0"], coef_NRL_recalculado_cm=coef_cm, coef_NRL=K["nrl_coef_cm"],
           n_crit_por_eV_cm3=float(n_crit(1.0) * 1e-6), T_ND1_eV=T_ND1, puntos=puntos, tabla=tab, curva_E=curva)

# --- figura 1: diagrama (n_e, T)
fig, ax = plt.subplots(figsize=(7.2, 5.4))
nn = np.logspace(18, 28, 300)          # cm^-3
TT = np.logspace(-1, 4, 300)           # eV
Ng, Tg = np.meshgrid(nn, TT)
lam = np.sqrt(eps0 * Tg * e / (Ng * 1e6 * e * e))
delta_g = a0 / lam
cs = ax.contour(Ng, Tg, delta_g, levels=[0.25, 0.5], colors="0.55", linewidths=0.8, linestyles=":")
ax.clabel(cs, fmt={0.25: "δ = 0.25", 0.5: "δ = 0.5"}, fontsize=8)
ax.fill_betweenx(TT, n_crit(TT) * 1e-6, 1e30, color="#d9534f", alpha=0.12)
ax.plot(n_crit(TT) * 1e-6, TT, color="#b52b27", lw=2.2,
        label=r"$\lambda_D = a_0/\delta_c = %.4f\,a_0$ (solo electrones)" % (lam_c / a0))
ax.plot(n_crit(TT, "ei") * 1e-6, TT, color="#b52b27", lw=1.2, ls="--",
        label=r"misma condición con electrones y protones ($\lambda_D/\sqrt{2}$)")
# lineas de validez
Gam1_T = e * e / (4 * np.pi * eps0 * (3 / (4 * np.pi * nn * 1e6)) ** (1 / 3)) / e     # Gamma = 1
EF_n = hbar ** 2 * (3 * np.pi ** 2 * nn * 1e6) ** (2 / 3) / (2 * me_kg) / e
ax.plot(nn, Gam1_T, color="#1f5aa6", lw=1.3, label=r"$\Gamma_e = 1$ (acoplamiento)")
ax.plot(nn, EF_n, color="#2e8b57", lw=1.3, label=r"$k_BT = E_F$ (degeneración)")
ND1_T = (1.0 / (4 * np.pi / 3 * (nn * 1e6) * (eps0 / (nn * 1e6 * e * e)) ** 1.5 * e ** 1.5)) ** (2 / 3)
ax.plot(nn, ND1_T, color="#8a5a00", lw=1.3, ls="-.", label=r"$N_D = 1$ (esfera de Debye)")
ax.axhline(13.6057, color="0.3", lw=0.8, ls=":")
ax.text(2e18, 15.5, "13.6 eV", fontsize=8, color="0.3")
ax.text(3e18, 0.2, "1s ligado en el modelo estático\n(λ_D > a0/δ_c)", fontsize=9)
ax.text(4e25, 0.2, "sin 1s en el\nmodelo estático", fontsize=9, color="#b52b27")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(1e18, 1e28); ax.set_ylim(0.1, 1e4)
ax.set_xlabel(r"densidad electrónica $n_e$ (cm$^{-3}$)")
ax.set_ylabel(r"temperatura $k_BT$ (eV)")
ax.set_title("Hidrógeno en un plasma de Debye: dónde desaparece el 1s (Yukawa estático)", fontsize=10)
ax.legend(fontsize=7.5, loc="upper left")
ax.grid(alpha=0.25, which="both", lw=0.4)
fig.tight_layout()
fig.savefig(c.os.path.join(c.FIG, "02_plasma_diagrama.png"), dpi=150)
plt.close(fig)

# --- figura 2: E_1s frente a lambda_D
fig, ax = plt.subplots(figsize=(6.2, 4.2))
dd = np.array([x["delta"] for x in curva])
ax.plot(1 / dd, [x["E_A_eV"] for x in curva], "o-", color="#1f5aa6", label="disparo sin caja (A)")
ax.plot(1 / dd, [x["E_B_hartree"] * Eh for x in curva], "x", ms=9, color="#d9534f", label="caja + Richardson (B)")
ax.axvline(lam_c / a0, color="0.3", ls="--", lw=1)
ax.text(lam_c / a0 * 1.03, -10, r"$a_0/\delta_c$", fontsize=9)
ax.axhline(0, color="0.5", lw=0.6)
ax.set_xscale("log")
ax.set_xlabel(r"longitud de Debye $\lambda_D/a_0$")
ax.set_ylabel(r"energía del 1s (eV)")
ax.set_title("Energía del 1s en el modelo estático (masa $m_e$, núcleo infinito)", fontsize=10)
ax.legend(fontsize=8)
ax.grid(alpha=0.3, lw=0.4)
fig.tight_layout()
fig.savefig(c.os.path.join(c.FIG, "02_plasma_energia.png"), dpi=150)
plt.close(fig)

# --- controles (criterios fijados antes de correr)
ctl = [dict(id="C5", control="Formula de Debye en SI frente al coeficiente del NRL Plasma Formulary",
            criterio="|coef/743 - 1| < 1e-3", valor=f"{coef_cm:.3f} cm (rel {coef_cm / 743 - 1:.1e})",
            pasa=bool(abs(coef_cm / 743 - 1) < 1e-3)),
       dict(id="C6", control="Longitud critica frente a Rogers, Graboske y Harwood 1970 (D0 = 0.83991 a0)",
            criterio="|1/delta_c - 0.83991| < 5e-6 (ultima cifra publicada)",
            valor=f"{1 / dc:.7f}", pasa=bool(abs(1 / dc - K["rgh_D0"]) < 5e-6)),
       dict(id="C7", control="Energia del 1s en 8 valores de delta: disparo (A) frente a caja (B)",
            criterio="max |E_A - E_B|/|E_A| < 1e-6",
            valor=f"{max(x['dif_rel'] for x in curva):.1e}",
            pasa=bool(max(x["dif_rel"] for x in curva) < 1e-6))]
out["controles"] = ctl
for k in ctl:
    log(k["id"], k["control"], "|", k["valor"], "|", "pasa" if k["pasa"] else "NO PASA")
out["t_s"] = time.perf_counter() - t0
log(f"tiempo {out['t_s']:.1f} s")
c.guardar("02_plasma", out, log.texto())

```

## codigo/03_materia_oscura.py

```python
"""03_materia_oscura.py -- materia oscura que interactua por un mediador ligero (potencial de Yukawa).

V(r) = -alpha e^{-m_phi r}/r entre dos particulas de masa m_chi: masa reducida m = m_chi/2, g = alpha hbar c,
mu_s = m_phi c/hbar. Entonces delta = m_phi/(m alpha) = 2 m_phi/(alpha m_chi), y hay estado ns ligado si
delta < delta_c(ns), es decir, si b = alpha m_chi/m_phi > 2/delta_c(ns).
Se compara con:
  * Tulin, Yu y Zurek (2013), Sec. IV B: primera resonancia s en b = 1.68 y antirresonancia s en b = 4.52
    (b = alpha m_X/m_phi, masa reducida m_X/2; barrido numerico de la ecuacion de Schrodinger).
  * Aproximacion de Hulthen: resonancias en b = kappa n^2 con kappa = 1.6 (Tulin et al., Ec. 24) y
    kappa = pi^2/6 (Feng, Kaplinghat y Yu 2010, Ec. 7).
  * Petraki, Postma y de Vries (2017): solo da la condicion aproximada xi = mu alpha/m_phi >~ n^2 en el texto
    principal (Sec. 2.2); en nuestras variables xi = b/2.
La antirresonancia (fase s nula a v -> 0) es el cero de la longitud de dispersion entre los umbrales 1s y 2s;
se calcula con dos metodos (solve_ivp y Numerov propio).
Criterios FIJADOS ANTES DE CORRER:
  C8  |2/delta_c - 1.68| <= 0.005 (redondeo de la cifra publicada)
  C9  |b_antirresonancia - 4.52| <= 0.005 y |a_s=0 por A - por B| < 1e-6 en delta
Salida: resultados/03_materia_oscura.json
"""
import time

import numpy as np
from scipy.optimize import brentq

import comun_e1 as c

log = c.Registro()
t0 = time.perf_counter()
K = c.CONST
U1 = c.leer("01_umbral")
dcs = {"1s": U1["delta_c_1s"]["A"], "2s": U1["delta_c_2s"]["A"], "3s": U1["delta_c_3s"]["A"]}
b_n = {k: 2.0 / v for k, v in dcs.items()}
xi_n = {k: 1.0 / v for k, v in dcs.items()}
for k in dcs:
    log(f"{k}: delta_c = {dcs[k]:.10f}  ->  alpha m_chi/m_phi > {b_n[k]:.6f}   (xi = mu alpha/m_phi > {xi_n[k]:.6f})")

hul = {"kappa_1.6": [K["tyz_kappa_hulthen"] * n ** 2 for n in (1, 2, 3)],
       "kappa_pi2/6": [np.pi ** 2 / 6 * n ** 2 for n in (1, 2, 3)]}
for k, v in hul.items():
    log(f"Hulthen {k}: b_n = " + ", ".join(f"{x:.4f}" for x in v))
err_hul = {k: [v[i] / b_n[s] - 1 for i, s in enumerate(("1s", "2s", "3s"))] for k, v in hul.items()}
for k, v in err_hul.items():
    log(f"   error relativo frente al Yukawa: " + ", ".join(f"{x:+.3%}" for x in v))

# --- antirresonancia: a_s(delta) = 0 con delta_c(2s) < delta < delta_c(1s)
aA = lambda d: c.long_dispersion_A(d, R=200.0)
aB = lambda d: c.long_dispersion_B(d, h=1 / 400, R=200.0)
# a_s pasa de -inf (justo arriba de delta_c(2s)... ) a +inf al acercarse a delta_c(1s) por debajo; buscar cambio de signo
ds = np.linspace(0.33, 1.15, 42)
va = [aA(d) for d in ds]
raices = []
for i in range(len(ds) - 1):
    if np.sign(va[i]) != np.sign(va[i + 1]) and abs(va[i]) < 50 and abs(va[i + 1]) < 50:
        raices.append((ds[i], ds[i + 1]))
log("intervalos con cambio de signo de a_s (|a_s|<50):", raices)
d0A = brentq(aA, *raices[0], xtol=1e-13)
d0B = brentq(aB, *raices[0], xtol=1e-13)
b_anti = 2.0 / d0A
log(f"a_s = 0 en delta = {d0A:.10f} (A), {d0B:.10f} (B)  ->  b = {b_anti:.5f} (Tulin et al.: {K['tyz_b_antires']})")
# [Revision R1-03] antirresonancia de Hulthen (Tulin, Yu y Zurek, Sec. VI): b = kappa r^2 con
# 2 gamma + psi(1 + r) + psi(1 - r) = 0, primera raiz r ~ 1.69
from scipy.special import digamma
r_hul = brentq(lambda r: 2 * np.euler_gamma + digamma(1 + r) + digamma(1 - r), 1.2, 1.99, xtol=1e-14)
b_anti_hul = {"kappa_1.6": K["tyz_kappa_hulthen"] * r_hul ** 2, "kappa_pi2/6": np.pi ** 2 / 6 * r_hul ** 2}
log(f"antirresonancia de Hulthen: r = {r_hul:.5f}, b = {b_anti_hul['kappa_1.6']:.4f} (kappa 1.6),"
    f" {b_anti_hul['kappa_pi2/6']:.4f} (pi^2/6)")
# longitud de dispersion a ambos lados del umbral (como en la Fase 3: a_s(1.19) = +2204, a_s(1.20) = -142.9)
a119 = aA(1.19)
a120 = aA(1.20)
log(f"control de signo: a_s(1.19) = {a119:.1f}, a_s(1.20) = {a120:.2f}")

# --- ejemplos numericos (solo ilustrativos): masa minima de m_chi para que exista el 1s
ejemplos = []
for alpha in (0.01, 0.1):
    for mphi_MeV in (1.0, 10.0, 100.0):
        mchi_min_GeV = b_n["1s"] * mphi_MeV / alpha / 1000.0
        ejemplos.append(dict(alpha=alpha, m_phi_MeV=mphi_MeV, m_chi_min_GeV=mchi_min_GeV))
        log(f"alpha = {alpha:5g}, m_phi = {mphi_MeV:6g} MeV  ->  hay 1s si m_chi > {mchi_min_GeV:.4g} GeV")

ctl = [dict(id="C8", control="Primera resonancia s de Tulin, Yu y Zurek (b = 1.68) frente a 2/delta_c",
            criterio="|2/delta_c - 1.68| <= 0.005", valor=f"2/delta_c = {b_n['1s']:.5f}",
            pasa=bool(abs(b_n["1s"] - K["tyz_b_res"]) <= 0.005)),
       dict(id="C9", control="Antirresonancia s (a_s = 0) frente a Tulin, Yu y Zurek (b = 4.52); A frente a B",
            criterio="|b - 4.52| <= 0.005 y |delta_A - delta_B| < 1e-6",
            valor=f"b = {b_anti:.4f}; dif A-B = {d0A - d0B:.1e}",
            pasa=bool(abs(b_anti - K["tyz_b_antires"]) <= 0.005 and abs(d0A - d0B) < 1e-6))]
for k in ctl:
    log(k["id"], k["control"], "|", k["valor"], "|", "pasa" if k["pasa"] else "NO PASA")
out = dict(delta_c=dcs, b_umbral=b_n, xi_umbral=xi_n, hulthen=hul, error_rel_hulthen=err_hul,
           antirresonancia=dict(delta_A=d0A, delta_B=d0B, b=b_anti, b_tyz=K["tyz_b_antires"],
                                r_hulthen=r_hul, b_hulthen=b_anti_hul),
           a_s_119=a119, a_s_120=a120, ejemplos=ejemplos, controles=ctl, t_s=time.perf_counter() - t0)
log(f"tiempo {out['t_s']:.1f} s")
c.guardar("03_materia_oscura", out, log.texto())

```

## codigo/04_deuteron.py

```python
"""04_deuteron.py -- deuteron de juguete: un solo Yukawa en onda s con el alcance del pion.

V(r) = -g e^{-m_pi r}/r, masa reducida mu = m_p m_n/(m_p + m_n). Con g = alpha_g hbar c:
    delta = m_pi/(mu alpha_g),   E = eps mu alpha_g^2  =>  eps/delta^2 = E mu/m_pi^2 (masas en MeV).
Se busca delta_d tal que eps(delta_d)/delta_d^2 = -B mu/m_pi^2 (B = energia de enlace) y luego
    alpha_g = m_pi/(mu delta_d), L = hbar c delta_d/m_pi (fm), <r> y <r^2> de la coordenada relativa en fm,
    radio de "estructura" del modelo r_str = (1/2) <r^2>^{1/2} (cada nucleon puntual a r/2 del centro de masa).
Comparacion experimental: r_str^2 = r_d^2 - r_p^2 - r_n^2 - 3/(4 m_p^2)  (Filin et al. 2020, Ec. 2), con r_d y r_p de
CODATA 2022 y r_n^2 del PDG citado por Filin et al.; y el valor teorico de Filin et al. (Ec. 9).
Escenarios (se declara SIEMPRE que se mantiene fijo):
  A. g y mu fijos (los fisicos); solo cambia m_pi. m_pi critico = m_pi delta_c/delta_d.
     Sensibilidad local d ln B/d ln m_pi a g fijo, frente a K_deut^q/K_pi^q de Berengut et al. 2013.
  B. g reajustado al punto de QCD en red de NPLQCD (m_pi = 805.9 MeV, M_B = 1634 MeV, B_d = 19.5 MeV):
     se obtiene delta_L y alpha_g(L), y se mide cuanto tendria que cambiar g para reproducirlo.
Tres elecciones de m_pi: pi0, pi+- y promedio de isospin (2 m_pi+- + m_pi0)/3; la central es el promedio.
Criterios FIJADOS ANTES DE CORRER:
  C10 |B(masas CODATA) - E_B(d) CODATA| < 1e-6 MeV
  C11 Reproduce el prototipo con sus mismas entradas: |delta_d - 0.8304596701595315| < 1e-9
  C12 delta_d: |A - B|/delta_d < 1e-7; <r>, <r^2>: |A - B|/A < 1e-5; caja R y 2R: |dE/E| < 1e-9
Salida: resultados/04_deuteron.json
"""
import time

import numpy as np
from scipy.optimize import brentq

import comun_e1 as c

log = c.Registro()
t0 = time.perf_counter()
K = c.CONST
U1 = c.leer("01_umbral")
dc = U1["delta_c_1s"]["A"]
hc = K["hbar_c"]

B_masas = K["m_p"] + K["m_n"] - K["m_d"]
B_codata = K["E_B_d_codata_keV"] / 1000.0
mu = K["m_p"] * K["m_n"] / (K["m_p"] + K["m_n"])
mpis = {"pi0": K["m_pi_0"], "pi+-": K["m_pi_pm"], "promedio": (2 * K["m_pi_pm"] + K["m_pi_0"]) / 3}
log(f"B (m_p + m_n - m_d, CODATA 2022) = {B_masas:.8f} MeV ; E_B(d) de entrada CODATA = {B_codata:.8f} MeV")
log(f"mu = {mu:.8f} MeV ; m_pi: " + ", ".join(f"{k} = {v:.6f}" for k, v in mpis.items()))


def eps_A(d):
    return c.estado_1s_disparo(d)["E0"]


def eps_B(d, R=200.0, h=1 / 40):
    return c.estado_1s_caja(d, R, h)["E0"]


def ajustar(target, metodo="A", a=0.3, b=1.18):
    f = (lambda d: eps_A(d) / d ** 2 - target) if metodo == "A" else (lambda d: eps_B(d) / d ** 2 - target)
    return brentq(f, a, b, xtol=1e-13)


def describir(B, mu_, mpi, metodo_obs=True):
    target = -B * mu_ / mpi ** 2
    dA = ajustar(target, "A")
    dB = ajustar(target, "B")
    A = c.estado_1s_disparo(dA)
    R = c.caja_para(A["E0"], Rmin=100.0, factor=40.0)
    Bx = c.estado_1s_caja(dA, R)
    B2 = c.estado_1s_caja(dA, 2 * R)
    alpha = mpi / (mu_ * dA)
    L = hc * dA / mpi
    r_med_fm = A["r_med"] * L
    r_rms_fm = np.sqrt(A["r2_med"]) * L
    return dict(target=target, delta_A=dA, delta_B=dB, dif_rel_delta=abs(dA - dB) / dA, eps=A["E0"],
                alpha_g=alpha, L_fm=L, kappa_inv_fm=L / A["kappa"],
                r_med=A["r_med"], r2_med=A["r2_med"], r_med_B=Bx["r_med"], r2_med_B=Bx["r2_med"], R_caja=R,
                dif_rel_rmed=abs(A["r_med"] - Bx["r_med"]) / A["r_med"],
                dif_rel_r2=abs(A["r2_med"] - Bx["r2_med"]) / A["r2_med"],
                dif_rel_E_R_2R=abs(Bx["E0"] - B2["E0"]) / abs(Bx["E0"]),
                r_med_fm=r_med_fm, r_rms_rel_fm=r_rms_fm, r_str_modelo_fm=r_rms_fm / 2,
                delta_sobre_delta_c=dA / dc, m_pi_crit_g_fijo=mpi * dc / dA)


out = dict(B_masas=B_masas, B_codata=B_codata, mu=mu, m_pi=mpis, delta_c=dc)
esc = {}
for k, mpi in mpis.items():
    d = describir(B_masas, mu, mpi)
    esc[k] = d
    log(f"[{k:8s}] delta_d = {d['delta_A']:.10f} (A) {d['delta_B']:.10f} (B), delta_d/delta_c = {d['delta_sobre_delta_c']:.4f},"
        f" g/hbar c = {d['alpha_g']:.6f}, <r> = {d['r_med_fm']:.4f} fm, <r^2>^1/2 = {d['r_rms_rel_fm']:.4f} fm,"
        f" r_str = {d['r_str_modelo_fm']:.4f} fm, 1/kappa = {d['kappa_inv_fm']:.4f} fm,"
        f" m_pi crit (g fijo) = {d['m_pi_crit_g_fijo']:.3f} MeV")
out["escenario_A"] = esc
central = esc["promedio"]

# --- radio experimental de estructura (puntual) a partir de CODATA y PDG
DF = 3.0 / 4.0 * (hc / K["m_p"]) ** 2
rstr2 = K["r_d_fm"] ** 2 - K["r_p_fm"] ** 2 - K["rn2_fm2"] - DF
rstr = np.sqrt(rstr2)
# incertidumbre: r_d^2 - r_p^2 por el desplazamiento isotopico (correlacion casi total de r_d y r_p) y r_n^2 del PDG
u_rstr = np.sqrt(K["rd2_rp2_iso_u_fm2"] ** 2 + K["rn2_u_fm2"] ** 2) / (2 * rstr)
u_rstr_indep = np.sqrt((K["r_d_fm"] * K["r_d_u_fm"]) ** 2 + (K["r_p_fm"] * K["r_p_u_fm"]) ** 2
                       + (K["rn2_u_fm2"] / 2) ** 2) / rstr     # version anterior (sin correlacion), solo informativa
rstr_rn2_antiguo = np.sqrt(K["r_d_fm"] ** 2 - K["r_p_fm"] ** 2 - K["rn2_filin_pdg_antiguo"] - DF)
out["radio_exp"] = dict(r_d=K["r_d_fm"], r_p=K["r_p_fm"], rn2=K["rn2_fm2"], darwin_foldy_fm2=DF,
                        r_str=rstr, u_r_str=u_rstr, u_r_str_indep=u_rstr_indep, r_str_rn2_antiguo=rstr_rn2_antiguo,
                        r_str_filin=K["r_str_filin_fm"],
                        modelo_sobre_exp=central["r_str_modelo_fm"] / rstr,
                        alcance_cero_r_str=central["kappa_inv_fm"] / np.sqrt(8))
log(f"r_str experimental = sqrt(r_d^2 - r_p^2 - r_n^2 - 3/4m_p^2) = {rstr:.4f} +- {u_rstr:.4f} fm"
    f" (Darwin-Foldy {DF:.5f} fm^2); Filin et al. (teoria) {K['r_str_filin_fm']} fm")
log(f"modelo / experimento = {central['r_str_modelo_fm'] / rstr:.4f};"
    f" limite de alcance cero 1/(sqrt(8) kappa) = {central['kappa_inv_fm'] / np.sqrt(8):.4f} fm")

# --- sensibilidad local a g fijo: B = mu alpha^2 |eps(delta)|, delta ~ m_pi
h = 1e-3
dd = central["delta_A"]
ep = abs(eps_A(dd * (1 + h)))
em = abs(eps_A(dd * (1 - h)))
dlnB = (np.log(ep) - np.log(em)) / (np.log(1 + h) - np.log(1 - h))
epB = abs(eps_B(dd * (1 + h)))
emB = abs(eps_B(dd * (1 - h)))
dlnB_B = (np.log(epB) - np.log(emB)) / (np.log(1 + h) - np.log(1 - h))
K_ber = K["K_deut_q"] / K["K_pi_q"]
K_ber_rango = ((K["K_deut_q"] - K["K_deut_q_dn"]) / K["K_pi_q"], (K["K_deut_q"] + K["K_deut_q_up"]) / K["K_pi_q"])
# [Revision R1-05] K_deut de Berengut incluye la variacion de la masa del nucleon. En el modelo a g fijo,
# B = mu alpha^2 |eps(m_pi/(mu alpha))|, asi que d ln B/d ln mu = 1 - d ln B/d ln m_pi, y
# K_deut(modelo) = (d ln B/d ln m_pi) K_pi + (d ln B/d ln mu) K_N.
dlnB_dlnmu = 1.0 - dlnB
K_deut_modelo = dlnB * K["K_pi_q"] + dlnB_dlnmu * K["K_N_q"]
out["sensibilidad"] = dict(dlnB_dlnmpi_A=dlnB, dlnB_dlnmpi_B=dlnB_B, berengut=K_ber, berengut_rango=K_ber_rango,
                           dlnB_dlnmu=dlnB_dlnmu, K_deut_modelo_con_mN=K_deut_modelo,
                           K_deut_modelo_sin_mN=dlnB * K["K_pi_q"],
                           cociente_con_mN=K_deut_modelo / K["K_deut_q"], cociente_sin_mN=dlnB * K["K_pi_q"] / K["K_deut_q"])
log(f"K_deut del modelo a g fijo: {K_deut_modelo:.3f} con m_N variable (K_N = {K['K_N_q']}),"
    f" {dlnB * K['K_pi_q']:.3f} sin ella; Berengut {K['K_deut_q']}")
log(f"d ln B/d ln m_pi (g y mu fijos) = {dlnB:.4f} (A), {dlnB_B:.4f} (B);"
    f" Berengut et al. K_deut/K_pi = {K_ber:.3f} (rango {K_ber_rango[0]:.2f} a {K_ber_rango[1]:.2f})")

# --- escenario B: punto de NPLQCD
mpiL, MBL, BL = K["lat_m_pi"], K["lat_M_B"], K["lat_B_d"]
muL = MBL / 2
uBL = float(np.sqrt(sum(x ** 2 for x in K["lat_B_d_u"])))
lat = {}
for et, Bv in (("central", BL), ("B-1sigma", BL - uBL), ("B+1sigma", BL + uBL)):
    t = -Bv * muL / mpiL ** 2
    dL = ajustar(t, "A", a=0.2, b=1.18)
    dLB = ajustar(t, "B", a=0.2, b=1.18)
    lat[et] = dict(B=Bv, delta_A=dL, delta_B=dLB, alpha_g=mpiL / (muL * dL))
    log(f"NPLQCD [{et}] B = {Bv:.2f} MeV: delta_L = {dL:.6f} (A) {dLB:.6f} (B), g/hbar c = {mpiL / (muL * dL):.4f}")
delta_gfijo = mpiL / (muL * central["alpha_g"])
lat["delta_con_g_fisico"] = delta_gfijo
lat["cociente_g"] = lat["central"]["alpha_g"] / central["alpha_g"]
lat["u_B"] = uBL
lat["mu_L"] = muL
log(f"con g fisico ({central['alpha_g']:.4f}) en el punto de red: delta = {delta_gfijo:.4f} = {delta_gfijo / dc:.3f} delta_c"
    f" (no ligado); para ligarlo con 19.5 MeV, g debe multiplicarse por {lat['cociente_g']:.3f}")
out["escenario_B_red"] = lat

# --- control con las entradas del prototipo
proto = -2.22457 * (938.918 / 2) / 138.04 ** 2
d_proto = ajustar(proto, "A")
out["prototipo"] = dict(delta=d_proto, delta_impreso=0.8304596701595315)
log(f"prototipo (sus entradas): delta_d = {d_proto:.13f}; impreso por el prototipo 0.8304596701595315")

ctl = [dict(id="C10", control="Energia de enlace: m_p + m_n - m_d frente al dato E_B(d) de CODATA 2022",
            criterio="|dif| < 1e-6 MeV", valor=f"{(B_masas - B_codata) * 1e6:.2f} eV",
            pasa=bool(abs(B_masas - B_codata) < 1e-6)),
       dict(id="C11", control="Reproduccion del prototipo con sus mismas entradas",
            criterio="|delta - 0.8304596701595315| < 1e-9", valor=f"{d_proto - 0.8304596701595315:.1e}",
            pasa=bool(abs(d_proto - 0.8304596701595315) < 1e-9)),
       dict(id="C12", control="Deuteron central: disparo (A) frente a caja (B); caja R frente a 2R",
            criterio="delta: <1e-7 rel; <r>, <r2>: <1e-5 rel; E(R) vs E(2R): <1e-9 rel",
            valor=f"{central['dif_rel_delta']:.1e}; {central['dif_rel_rmed']:.1e}, {central['dif_rel_r2']:.1e};"
                  f" {central['dif_rel_E_R_2R']:.1e}",
            pasa=bool(central["dif_rel_delta"] < 1e-7 and central["dif_rel_rmed"] < 1e-5
                      and central["dif_rel_r2"] < 1e-5 and central["dif_rel_E_R_2R"] < 1e-9))]
for k in ctl:
    log(k["id"], k["control"], "|", k["valor"], "|", "pasa" if k["pasa"] else "NO PASA")
out["controles"] = ctl
out["t_s"] = time.perf_counter() - t0
log(f"tiempo {out['t_s']:.1f} s")
c.guardar("04_deuteron", out, log.texto())

```
