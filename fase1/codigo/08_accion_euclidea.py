"""Bloque 08: accion euclidea discreta, analisis del peso y toy model.
Unidades: hbar=m=g=1, V(r) = -exp(-delta r)/r, delta = mu hbar^2/(m g).

Partes:
  A. Identidades simbolicas (sympy): nucleo radial con imagen, divergencia de
     r^2 exp(eps/r), estimador virial de Yukawa, energia discreta exacta del
     oscilador armonico con Trotter simetrico y con Takahashi-Imada (TI).
  B. Divergencia de la integral sobre una coordenada intermedia con el peso
     primitivo, truncada en r_min (mpmath, log-escala), para varios eps y delta.
     Comparacion con pesos regularizados (TI y suavizado V_a).
  C. Nucleo exacto de corto tiempo (radial, l=0) por descomposicion espectral de
     H discretizado: es finito en r->0; accion de pares U finita.
  D. Suavizado V_a = -exp(-delta r)/sqrt(r^2+a^2): delta_c(a), E0(a) y
     extrapolacion a->0.
  E. Toy model: oscilador armonico 1D. Matriz de transferencia: sesgo de Trotter
     ~ eps^2 (primitiva) y ~ eps^4 (TI); proyeccion en tiempo imaginario.
  F. Toy model por Monte Carlo (PIMC primitivo, Metropolis): estimadores
     termodinamico y virial frente a los valores exactos discretos.
Tiempo total: ~1 min.
"""
import os as _os
_RAIZ = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..','..'))  # raiz del repositorio
import time
import numpy as np
import sympy as sp
import mpmath as mp
from scipy.linalg import eigh, eigh_tridiagonal
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

FIG = _RAIZ + "/fase1/figuras/"
DC = 1.19061242106                      # Gebremedhin y Weatherford 2023
C1, C2, C3, C4 = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
t0 = time.time()

# ---------------------------------------------------------------- A. sympy
print("=== A. Identidades simbolicas ===")
r, rp, e, d, x = sp.symbols("r r' epsilon delta x", positive=True)
th = sp.symbols("theta", real=True)
K3 = (2*sp.pi*e)**sp.Rational(-3, 2)*sp.exp(-(r**2 + rp**2 - 2*r*rp*sp.cos(th))/(2*e))
ang = sp.integrate(K3*2*sp.pi*sp.sin(th), (th, 0, sp.pi))     # integral angular
KD = (2*sp.pi*e)**sp.Rational(-1, 2)*(sp.exp(-(r - rp)**2/(2*e)) - sp.exp(-(r + rp)**2/(2*e)))
chk = sp.simplify((r*rp*ang - KD).rewrite(sp.exp))
print("A1  r r' * integral angular de K0_3D - K_D(imagen) =", chk)
lim = sp.limit(r**2*sp.exp(e/r), r, 0, '+')
print("A2  lim_{r->0+} r^2 exp(eps/r) =", lim)
Ix = sp.integrate(x**-4*sp.exp(e*x), (x, 1, sp.oo))
print("A3  int_1^oo x^-4 exp(eps x) dx (x=1/r) =", Ix)
# imagen: K_D(rho,r)^2 ~ r^2 cerca de 0, tampoco compensa
rho = sp.symbols("rho", positive=True)
KDr = KD.subs({rp: rho})
print("A4  lim_{r->0+} K_D(rho,r)^2 / r^2 =", sp.simplify(sp.limit(KDr**2/r**2, r, 0, '+')),
      "(finito y >0: el integrando radial ~ r^2 exp(eps/r) tambien diverge)")
V = -sp.exp(-d*r)/r
vir = sp.simplify(V + r*sp.diff(V, r)/2)
print("A5  V + r V'/2 =", vir, "  (delta=0:", vir.subs(d, 0), ")")
print("A6  V cerca de 0:", sp.series(V, r, 0, 2).removeO(), " -> Yukawa ~ Coulomb en r->0")

# Oscilador: autofuncion gaussiana exp(-al x^2/2) de T = e^{-eps W/2} K0 e^{-eps W/2},
# W = Om^2 x^2/2. Primitiva: Om^2=1. TI: W = V + eps^2 V'^2/24 => Om^2 = 1+eps^2/12.
al, Om2 = sp.symbols("alpha Omega2", positive=True)
A = 1/(2*e) + e*Om2/4 + al/2
sol = sp.solve(sp.Eq(al/2, 1/(2*e) + e*Om2/4 - 1/(4*e**2*A)), al)
al_s = [s for s in sol if s.subs({e: sp.Rational(1, 10), Om2: 1}).is_positive][0]
lam = 1/sp.sqrt(2*e*A.subs(al, al_s))
E_prim = sp.simplify(-sp.log(lam.subs(Om2, 1))/e)
E_TI = sp.simplify(-sp.log(lam.subs(Om2, 1 + e**2/12))/e)
ser_TI = sp.expand(sp.series(E_TI, e, 0, 6).removeO().subs(
    {sp.log(24): 3*sp.log(2) + sp.log(3), sp.log(6): sp.log(2) + sp.log(3)}))
print("A7  E0 primitiva(eps) =", sp.series(E_prim, e, 0, 5).removeO())
print("A8  E0 TI(eps)        =", ser_TI)
fE_prim = sp.lambdify(e, E_prim, "numpy"); fE_TI = sp.lambdify(e, E_TI, "numpy")
# estimador termodinamico a beta->inf (M fijo): -d ln lambda/d eps
ET_prim = sp.simplify(-sp.diff(sp.log(lam.subs(Om2, 1)), e))
print("A9  <E_termo>(beta->inf) primitiva =", sp.series(ET_prim, e, 0, 4).removeO())
fET = sp.lambdify(e, ET_prim, "numpy")

# ---------------------------------------------------------------- B. divergencia
print(f"\n[t={time.time()-t0:.0f} s]"); print("\n=== B. Integral sobre una coordenada intermedia, peso primitivo ===")
mp.mp.dps = 30
RHO = 1.0   # vecinos r_{k-1} = r_{k+1} a distancia RHO del origen (radio de Bohr)

def g_ang(rr, eps):
    """Promedio angular de K0(a,r)K0(r,b) con a=b, |a|=RHO (en 3D)."""
    z = 2*RHO*rr/eps
    sh = mp.sinh(z)/z if z > 0 else mp.mpf(1)
    return (2*mp.pi*eps)**-3*mp.e**(-(RHO**2 + rr**2)/eps)*sh

def I_int(rmin, eps, dl, kind="prim", a=0.0, rmax=8.0):
    def W(rr):
        if kind == "prim":
            return -mp.e**(-dl*rr)/rr
        if kind == "TI":
            v = -mp.e**(-dl*rr)/rr; dv = mp.e**(-dl*rr)*(1 + dl*rr)/rr**2
            return v + eps**2*dv**2/24
        return -mp.e**(-dl*rr)/mp.sqrt(rr**2 + a**2)
    f = lambda rr: 4*mp.pi*rr**2*g_ang(rr, eps)*mp.e**(-eps*W(rr))
    pts = [rmin] + [rmin*2**k for k in range(1, 60) if rmin*2**k < rmax] + [rmax]
    return mp.quad(f, pts)

def asint(rmin, eps, dl):
    return 4*mp.pi*g_ang(0, eps)*rmin**4*mp.e**(eps*mp.e**(-dl*rmin)/rmin)/eps

rmins = np.logspace(-1.0, -3.0, 9)
divB = {}
for eps in (0.05, 0.1, 0.2):
    for dl in (0.0, DC):
        vals = [I_int(mp.mpf(rm), eps, dl) for rm in rmins]
        divB[(eps, dl)] = np.array([float(mp.log10(v)) for v in vals])
        rat = float(vals[-1]/asint(mp.mpf(rmins[-1]), eps, dl))
        print(f"eps={eps:4.2f} delta={dl:6.4f}: log10 I(r_min=0.1)={divB[(eps, dl)][0]:8.3f}  "
              f"log10 I(r_min=1e-3)={divB[(eps, dl)][-1]:9.3f}  I/asintota(1e-3)={rat:.4f}")
r0 = mp.mpf("1e-3")
print("Cociente I(delta=delta_c)/I(delta=0) en r_min=1e-3, eps=0.1:",
      float(I_int(r0, 0.1, DC)/I_int(r0, 0.1, 0.0)), " vs exp(-eps delta_c) =", np.exp(-0.1*DC))
print("Pesos regularizados (eps=0.1, delta=delta_c), log10 I al bajar r_min:")
for kind, a in (("TI", 0.0), ("soft", 0.1), ("soft", 0.02)):
    v = [float(mp.log10(I_int(mp.mpf(rm), 0.1, DC, kind, a))) for rm in (1e-1, 1e-2, 1e-3, 1e-5)]
    print(f"   {kind:4s} a={a:4.2f}: " + "  ".join(f"{y:.6f}" for y in v), " (converge)")
# radial con imagen: integrando K_D(rho,r)^2 exp(eps e^{-delta r}/r) (sin 4 pi r^2)
def I_rad(rmin, eps, dl, rmax=8.0):
    KDn = lambda rr: (2*mp.pi*eps)**-0.5*(mp.e**(-(RHO - rr)**2/(2*eps)) - mp.e**(-(RHO + rr)**2/(2*eps)))
    f = lambda rr: KDn(rr)**2*mp.e**(eps*mp.e**(-dl*rr)/rr)
    pts = [rmin] + [rmin*2**k for k in range(1, 60) if rmin*2**k < rmax] + [rmax]
    return mp.quad(f, pts)
print("Radial con imagen (eps=0.1, delta=delta_c): log10 I(r_min) para r_min=1e-1,1e-2,3e-3,1e-3,5e-4 =",
      "  ".join(f"{float(mp.log10(I_rad(mp.mpf(rm), 0.1, DC))):.2f}" for rm in (1e-1, 1e-2, 3e-3, 1e-3, 5e-4)))
print("3D, mismo caso: log10 I(r_min) para r_min=1e-1,1e-2,3e-3,1e-3,5e-4 =",
      "  ".join(f"{float(mp.log10(I_int(mp.mpf(rm), 0.1, DC))):.2f}" for rm in (1e-1, 1e-2, 3e-3, 1e-3, 5e-4)))

# ---------------------------------------------------------------- C. nucleo exacto
print(f"\n[t={time.time()-t0:.0f} s]"); print("\n=== C. Nucleo exacto de corto tiempo (l=0) ===")
def kernel_exact(eps, dl, h, R=4.0):
    N = int(round(R/h)) - 1; rr = h*np.arange(1, N + 1)
    dg = 1/h**2 - np.exp(-dl*rr)/rr; of = -0.5/h**2*np.ones(N - 1)
    w, v = eigh_tridiagonal(dg, of)
    diag = (v**2*np.exp(-eps*w)).sum(axis=1)/h     # rho(r,r;eps) para u
    return rr, diag
EPSC = 0.1
KDd = lambda rr, eps: (2*np.pi*eps)**-0.5*(1 - np.exp(-2*rr**2/eps))
Cres = {}
for dl in (0.0, DC):
    ra, da = kernel_exact(EPSC, dl, 0.005); rb, db = kernel_exact(EPSC, dl, 0.0025)
    for rq in (0.02, 0.1, 0.5, 1.5):
        ia = np.argmin(abs(ra - rq)); ib = np.argmin(abs(rb - rq))
        Ua = -np.log(da[ia]/KDd(ra[ia], EPSC)); Ub = -np.log(db[ib]/KDd(rb[ib], EPSC))
        print(f"delta={dl:6.4f} r={rq:4.2f}: U_par(h=.005)={Ua:8.4f} U_par(h=.0025)={Ub:8.4f} "
              f"eps V(r)={-EPSC*np.exp(-dl*rq)/rq:9.4f}")
    Cres[dl] = (rb, db)
rb, db = Cres[0.0]
print("rho_exact(r,r)/r^2 en r=0.01,0.02 (delta=0):",
      [f"{db[np.argmin(abs(rb - q))]/q**2:.3f}" for q in (0.01, 0.02)], " -> finito (~r^2)")

# ---------------------------------------------------------------- D. suavizado
print(f"\n[t={time.time()-t0:.0f} s]"); print("\n=== D. Suavizado V_a = -exp(-delta r)/sqrt(r^2+a^2) ===")
def slope_inf(dl, a, R=400.0):
    f = lambda rr, y: [y[1], -2*np.exp(-dl*rr)/np.sqrt(rr**2 + a**2)*y[0]]
    s = solve_ivp(f, (1e-8, R), [1e-8, 1.0], method="DOP853", rtol=1e-12, atol=1e-14)
    return s.y[1, -1]
def dc_a(a):
    return brentq(lambda dl: slope_inf(dl, a), 0.9, 1.25, xtol=1e-12)
def E0_a(a, dl=0.0, R=30.0):
    """Disparo: u(0)=0, u'(0)=1; E0 es la energia que anula u(R) (sin nodos)."""
    def uR(E):
        f = lambda rr, y: [y[1], 2*(-np.exp(-dl*rr)/np.sqrt(rr**2 + a**2) - E)*y[0]]
        return solve_ivp(f, (1e-8, R), [1e-8, 1.0], method="DOP853", rtol=1e-12, atol=1e-30).y[0, -1]
    return brentq(uR, -0.6, -0.3, xtol=1e-13)
avals = np.array([0.4, 0.2, 0.1, 0.05, 0.025, 0.0125, 0.00625, 0.003125])
dca = np.array([dc_a(a) for a in avals]); E0a = np.array([E0_a(a) for a in avals])
dc0 = dc_a(0.0); E00 = E0_a(0.0)
print(f"control a=0: E0 = {E00:.10f} (exacto -0.5)")
for a, q, E in zip(avals, dca, E0a):
    print(f"a={a:7.4f}: delta_c(a)={q:.8f} (dif {q - dc0:+.2e})  E0(a,delta=0)={E:.8f} (dif {E + 0.5:+.2e})")
print(f"a=0 (Coulomb-Yukawa puro, mismo integrador): delta_c={dc0:.10f}")
# ajuste f(a) = f0 + c1 a^2 ln a + c2 a^2 con los 4 valores mas pequenos
Xf = np.c_[np.ones(4), avals[-4:]**2*np.log(avals[-4:]), avals[-4:]**2]
cE = np.linalg.lstsq(Xf, E0a[-4:], rcond=None)[0]
cD = np.linalg.lstsq(Xf, dca[-4:], rcond=None)[0]
print(f"Extrapolacion a->0 (f0 + c1 a^2 ln a + c2 a^2): E0 -> {cE[0]:.8f} (c1={cE[1]:.3f}), "
      f"delta_c -> {cD[0]:.8f} (dif con lit. {cD[0] - DC:+.1e})")
pE = np.polyfit(np.log(avals[-3:]), np.log(E0a[-3:] + 0.5), 1)[0]
print(f"Pendiente log-log de E0(a)+1/2 (3 menores a): {pE:.3f}  (a^2 ln(1/a) da ~2 con correccion log)")
print("Prediccion perturbativa de primer orden (Coulomb): (E0(a)+1/2)/(2 a^2 ln(1/a)) =",
      "  ".join(f"{(E+0.5)/(2*a**2*np.log(1/a)):.3f}" for a, E in zip(avals[-4:], E0a[-4:])))
print(f"Sin extrapolar, a={avals[-1]} da delta_c={dca[-1]:.6f}: error {dca[-1] - DC:+.1e}")

# ---------------------------------------------------------------- E. toy model
print(f"\n[t={time.time()-t0:.0f} s]"); print("\n=== E. Toy model: oscilador armonico 1D, matriz de transferencia ===")
def transfer(eps, W, dx=None, L=9.0):
    dx = dx or min(0.02, np.sqrt(eps)/12)
    xs = np.arange(-L, L + dx/2, dx)
    K = np.exp(-(xs[:, None] - xs[None, :])**2/(2*eps))/np.sqrt(2*np.pi*eps)*dx
    w = np.exp(-eps*W(xs, eps)/2)
    return xs, w[:, None]*K*w[None, :]
Wp = lambda xx, eps: xx**2/2
Wti = lambda xx, eps: xx**2/2 + eps**2*xx**2/24       # V + eps^2 V'^2/24, V'=x
epsl = np.array([1.0, 0.7, 0.5, 0.35, 0.25, 0.18, 0.125])
Ep, Et = [], []
for eps in epsl:
    for W, store in ((Wp, Ep), (Wti, Et)):
        xs, T = transfer(eps, W)
        lmax = eigh(T, eigvals_only=True, subset_by_index=[len(xs) - 1, len(xs) - 1])[0]
        store.append(-np.log(lmax)/eps)
Ep, Et = np.array(Ep), np.array(Et)
for eps, a1, a2 in zip(epsl, Ep, Et):
    print(f"eps={eps:5.3f}: E_prim={a1:.10f} (analit {fE_prim(eps):.10f})  E_TI={a2:.10f} "
          f"(analit {fE_TI(eps):.10f})")
sp_ = np.polyfit(np.log(epsl[-4:]), np.log(np.abs(Ep[-4:] - 0.5)), 1)[0]
st_ = np.polyfit(np.log(epsl[-4:]), np.log(np.abs(Et[-4:] - 0.5)), 1)[0]
print(f"Coeficientes: (E_prim-1/2)/eps^2 en eps=0.125: {(Ep[-1]-0.5)/0.125**2:.5f} (analit -1/48={-1/48:.5f}); "
      f"(E_TI-1/2)/eps^4: {(Et[-1]-0.5)/0.125**4:.6f} (analit -1/1440={-1/1440:.6f})")
print(f"Pendiente log-log sesgo primitiva = {sp_:.3f} (esperado 2);  TI = {st_:.3f} (esperado 4)")
# proyeccion: trial exp(-|x|)
eps = 0.1
xs, T = transfer(eps, Wp)
psi = np.exp(-np.abs(xs)); G = [psi @ psi]; v = psi.copy()
nst = 80
for n in range(nst):
    v = T @ v; G.append(psi @ v)
G = np.array(G); tau = eps*np.arange(nst)
Eeff = -np.log(G[1:]/G[:-1])/eps
for tq in (0.5, 1.0, 2.0, 4.0, 7.9):
    k = int(round(tq/eps)); print(f"proyeccion eps=0.1 tau={tau[k]:4.1f}: E_eff={Eeff[k]:.10f}  "
                                    f"E_eff-E0(eps)={Eeff[k] - fE_prim(eps):+.2e}")
gap = np.polyfit(tau[40:75], np.log(np.abs(Eeff[40:75] - fE_prim(eps))), 1)[0]
wd = np.sort(np.linalg.eigvalsh(T))[::-1][:3]
print(f"tasa de convergencia de E_eff (tau 4-7.5): {-gap:.4f};  brecha discreta E2-E0 = "
      f"{-np.log(wd[2]/wd[0])/eps:.4f} (continuo 2; el trial par no tiene componente en E1)")
# Z(beta): dos derivadas distintas (revision adversarial, ronda 2).
#  (i) a eps fijo variando M: -(lnZ(M+1)-lnZ(M-1))/(2 eps). Da la energia del autovalor a beta finito;
#      NO es el estimador termodinamico de 8.2.7.
#  (ii) estimador termodinamico de 8.2.7, a M fijo variando eps. Con lambda_n = exp(-(n+1/2) theta),
#      cosh(theta) = 1 + eps^2/2: Z_M = 1/(2 sinh(M theta/2)) y -dlnZ/dbeta|_M = (1/2) theta'(eps) coth(M theta/2).
wT = np.linalg.eigvalsh(T); wT = wT[wT > 1e-300]
lnZ = lambda M: np.log(np.sum(wT**M))
th = lambda e: np.arccosh(1 + e**2/2)
dth = lambda e: e/np.sqrt((1 + e**2/2)**2 - 1)          # theta'(eps)
print(f"comprobacion de lambda_n: -ln(lambda0)/eps numerico={-np.log(np.max(wT))/eps:.8f}  "
      f"theta/(2 eps)={th(eps)/(2*eps):.8f}")
for beta in (1.0, 3.0, 6.0, 10.0):
    M = int(round(beta/eps)); Eb = -(lnZ(M + 1) - lnZ(M - 1))/(2*eps)
    lnZM = lambda e, M=M: -np.log(2*np.sinh(M*th(e)/2))
    dd = 1e-5
    Eth_num = -(lnZM(eps + dd) - lnZM(eps - dd))/(2*dd)/M
    Eth = 0.5*dth(eps)/np.tanh(M*th(eps)/2)
    print(f"beta={beta:4.1f}: (i) eps fijo, variando M: {Eb:.6f} | (ii) termodinamico a M fijo: {Eth:.6f} "
          f"(dif. finita en eps {Eth_num:.6f}) | continuo (1/2)coth(beta/2)={0.5/np.tanh(beta/2):.6f}")
print(f"beta->inf: (ii) -> theta'(eps)/2 = {0.5*dth(eps):.6f}; 1/2 - eps^2/16 = {0.5 - eps**2/16:.6f}")

# ---------------------------------------------------------------- F. PIMC
print(f"\n[t={time.time()-t0:.0f} s]"); print("\n=== F. PIMC primitivo (Metropolis, oscilador, beta=10, M=40, eps=0.25) ===")
rng = np.random.default_rng(20261012)
M, eps = 40, 0.25; beta = M*eps
xp = np.zeros(M); step = 0.9; nsw, nth = 200000, 5000
eT, eV, acc = [], [], 0
even = np.arange(0, M, 2); odd = np.arange(1, M, 2)
def S_loc(xk, xl, xr):
    return ((xk - xl)**2 + (xr - xk)**2)/(2*eps) + eps*xk**2/2
for sw in range(nsw):
    for idx in (even, odd):
        xl = xp[(idx - 1) % M]; xr = xp[(idx + 1) % M]; xo = xp[idx]
        xn = xo + step*rng.uniform(-1, 1, idx.size)
        dS = S_loc(xn, xl, xr) - S_loc(xo, xl, xr)
        ok = rng.random(idx.size) < np.exp(-dS); xp[idx] = np.where(ok, xn, xo); acc += ok.sum()
    sh = 0.5*rng.uniform(-1, 1)                # movimiento rigido del camino (Metropolis)
    dS = eps*np.sum((xp + sh)**2 - xp**2)/2
    if rng.random() < np.exp(-dS): xp += sh
    if sw >= nth:
        dif = np.roll(xp, -1) - xp
        eT.append(1/(2*eps) - np.mean(dif**2)/(2*eps**2) + np.mean(xp**2)/2)
        eV.append(np.mean(xp**2))
def blocking(a, nb=50):
    a = np.array(a); b = a[:len(a)//nb*nb].reshape(nb, -1).mean(1)
    return a.mean(), b.std(ddof=1)/np.sqrt(nb)
mT, sT = blocking(eT); mV, sV = blocking(eV)
# exactos discretos (matriz de transferencia, mismo eps y M)
xs, T = transfer(eps, Wp); wv, vv = eigh(T)
TM = (vv*wv**M) @ vv.T; Zd = np.trace(TM); x2 = np.sum(xs**2*np.diag(TM))/Zd
print(f"aceptacion={acc/(nsw*M):.2f}")
print(f"E_termo = {mT:.4f} +- {sT:.4f}   exacto discreto -dln lambda/deps = {fET(eps):.4f}")
print(f"E_virial= {mV:.4f} +- {sV:.4f}   exacto discreto <x^2>_M = {x2:.4f}   continuo 0.5")
print(f"E0(eps) por autovalor = {fE_prim(eps):.4f}")

# ---------------------------------------------------------------- G. remedio recomendado
print(f"\n[t={time.time()-t0:.0f} s]"); print("\n=== G. Prueba de concepto: nucleo exacto de Coulomb + resto W=(1-e^{-delta r})/r ===")
rs_ = sp.symbols("r", positive=True)
Wsym = (1 - sp.exp(-d*rs_))/rs_
print("G1  W(r->0) =", sp.limit(Wsym, rs_, 0, '+'), "; W'(r->0) =", sp.limit(sp.diff(Wsym, rs_), rs_, 0, '+'),
      " (acotado y suave: 0 <= W <= delta)")
def coulomb_plus_W(dl, R, h, epss):
    N = int(round(R/h)) - 1; rr = h*np.arange(1, N + 1)
    off = -0.5/h**2*np.ones(N - 1)
    wC, vC = eigh_tridiagonal(1/h**2 - 1/rr, off)                  # Coulomb puro (no depende de delta)
    Eex = eigh_tridiagonal(1/h**2 - np.exp(-dl*rr)/rr, off, select="i", select_range=(0, 0))[0][0]
    Wr = (1 - np.exp(-dl*rr))/rr; out = []
    for ee in epss:
        rhoC = (vC*np.exp(-ee*(wC - wC[0]))) @ vC.T               # nucleo exacto (desplazado)
        g = np.exp(-ee*Wr/2); Tm = g[:, None]*rhoC*g[None, :]
        lm = eigh(Tm, eigvals_only=True, subset_by_index=[N - 1, N - 1])[0]
        out.append(wC[0] - np.log(lm)/ee)
    return Eex, np.array(out)
epsG = np.array([0.8, 0.4, 0.2, 0.1, 0.05])
Gres = {}
for dl, R, h in ((0.5, 30.0, 0.02), (1.0, 70.0, 0.035)):
    Eex, Eg = coulomb_plus_W(dl, R, h, epsG); Gres[dl] = (Eex, Eg)
    sl = np.polyfit(np.log(epsG[-3:]), np.log(np.abs(Eg[-3:] - Eex)), 1)[0]
    print(f"delta={dl}: E0 misma malla (exacto discreto)={Eex:.8f}; " +
          "  ".join(f"eps={ee}: {E:.8f}" for ee, E in zip(epsG, Eg)) + f"; pendiente sesgo={sl:.2f}")
# escala de tiempo de proyeccion cerca del umbral (FD, misma receta que el bloque 05)
for dl in (0.5, 1.0, 1.1):
    R = 370.0 if dl == 1.1 else 120.0; N = int(R/0.025)
    hh = R/(N + 1); rr = hh*np.arange(1, N + 1)
    E0d = eigh_tridiagonal(1/hh**2 - np.exp(-dl*rr)/rr, -0.5/hh**2*np.ones(N - 1),
                           select="i", select_range=(0, 0))[0][0]
    print(f"delta={dl}: E0={E0d:.6f}  1/|E0|={1/abs(E0d):8.1f}  M=tau/eps con tau=5/|E0|, eps=0.1: {5/abs(E0d)/0.1:8.0f}")

# ---------------------------------------------------------------- figuras
plt.rcParams.update({"axes.spines.top": False, "axes.spines.right": False, "font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
cols = {0.05: C1, 0.1: C2, 0.2: C3}
for (eps_, dl), y in divB.items():
    ax[0].plot(1/rmins, y, "o-" if dl == 0 else "s--", ms=4, lw=2 if dl == 0 else 1.2, color=cols[eps_],
               label=fr"$\epsilon={eps_}$, $\delta={'0' if dl == 0 else r'\delta_c'}$")
ax[0].set_xscale("log"); ax[0].set_xlabel(r"$1/r_{\min}$  [$mg/\hbar^2$]")
ax[0].set_ylabel(r"$\log_{10} I(r_{\min})$")
ax[0].set_title("(a) Peso primitivo: la integral sobre $\\mathbf{r}_k$ diverge\n(curvas $\\delta=0$ y $\\delta=\\delta_c$ casi superpuestas)", fontsize=9)
ax[0].legend(fontsize=7, frameon=False)
for dl, c in ((0.0, C1), (DC, C2)):
    rr, dd = Cres[dl]; m = rr <= 2.0
    U = -np.log(dd[m]/KDd(rr[m], EPSC))
    ax[1].plot(rr[m], U, color=c, lw=2, label=fr"$U$ exacta (pares), $\delta={'0' if dl == 0 else r'\delta_c'}$")
    ax[1].plot(rr[m], -EPSC*np.exp(-dl*rr[m])/rr[m], color=c, lw=1.2, ls="--",
               label=fr"primitiva $\epsilon V$, $\delta={'0' if dl == 0 else r'\delta_c'}$")
ax[1].set_ylim(-1.2, 0.05); ax[1].set_xlabel(r"$r$  [$\hbar^2/mg$]")
ax[1].set_ylabel(r"acción por paso en la diagonal ($\epsilon=0.1$)")
ax[1].set_title("(b) La acción de pares es finita en $r\\to0$", fontsize=9)
ax[1].legend(fontsize=7, frameon=False)
fig.tight_layout(); fig.savefig(FIG + "08_divergencia_peso.png", dpi=160); plt.close(fig)

fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
ee = np.logspace(-1, 0, 50)
ax[0].loglog(epsl, np.abs(Ep - 0.5), "o", ms=6, color=C1, label="primitiva (matriz de transferencia)")
ax[0].loglog(ee, np.abs(fE_prim(ee) - 0.5), "-", lw=1.2, color=C1, alpha=.6, label="primitiva (analítica)")
ax[0].loglog(epsl, np.abs(Et - 0.5), "s", ms=6, color=C2, label="Takahashi-Imada (matriz)")
ax[0].loglog(ee, np.abs(fE_TI(ee) - 0.5), "-", lw=1.2, color=C2, alpha=.6, label="Takahashi-Imada (analítica)")
ax[0].loglog(ee, ee**2/48, ":", color="gray", lw=1, label=r"$\epsilon^2/48$")
ax[0].loglog(ee, ee**4/1440, "-.", color="gray", lw=1, label=r"$\epsilon^4/1440$")
ax[0].set_xlabel(r"$\epsilon$"); ax[0].set_ylabel(r"$|E_0(\epsilon)-E_0|$")
ax[0].set_title("(a) Sesgo de Trotter, oscilador 1D", fontsize=9); ax[0].legend(fontsize=7, frameon=False)
ax[1].semilogy(tau[:60], np.abs(Eeff[:60] - fE_prim(0.1)), "-", lw=2, color=C3,
               label=r"$|E_{\rm eff}(\tau)-E_0(\epsilon)|$, $\epsilon=0.1$")
ax[1].semilogy(tau[:60], 0.4*np.exp(-2*tau[:60]), ":", color="gray", label=r"$\propto e^{-2\tau}$")
ax[1].set_xlabel(r"$\tau$"); ax[1].set_title("(b) Proyección en tiempo imaginario", fontsize=9)
ax[1].legend(fontsize=7, frameon=False)
fig.tight_layout(); fig.savefig(FIG + "08_toy_trotter.png", dpi=160); plt.close(fig)

fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
ag = np.logspace(np.log10(0.0025), np.log10(0.03), 40)   # region del ajuste
ax[0].plot(avals, dca, "o", ms=6, color=C1, label=r"$\delta_c(a_s)$ (disparo a $E=0$)")
ax[0].plot(ag, cD[0] + cD[1]*ag**2*np.log(ag) + cD[2]*ag**2, "-", lw=1.2, color=C1, alpha=.6,
           label=r"ajuste $f_0+c_1a_s^2\ln a_s+c_2a_s^2$ (4 menores $a_s$)")
ax[0].axhline(DC, ls="--", color="gray", lw=1, label=r"$\delta_c$ (lit.)")
ax[0].set_xscale("log"); ax[0].set_xlabel(r"$a_s$  [$\hbar^2/mg$]"); ax[0].set_ylabel(r"$\delta_c(a_s)$")
ax[0].set_title("(a) Umbral con potencial suavizado", fontsize=9); ax[0].legend(fontsize=7, frameon=False)
ax[1].loglog(avals, E0a + 0.5, "s", ms=6, color=C2, label=r"$E_0(a_s)+1/2$, $\delta=0$")
ax[1].loglog(ag, cE[1]*ag**2*np.log(ag) + cE[2]*ag**2 + (cE[0] + 0.5), "-", lw=1.2, color=C2, alpha=.6,
             label=r"ajuste (4 menores $a_s$)")
ax[1].set_xlabel(r"$a_s$  [$\hbar^2/mg$]"); ax[1].set_ylabel(r"sesgo en energía  [$mg^2/\hbar^2$]")
ax[1].set_title("(b) Sesgo del suavizado (límite de Coulomb)", fontsize=9)
ax[1].legend(fontsize=7, frameon=False)
fig.tight_layout(); fig.savefig(FIG + "08_suavizado.png", dpi=160); plt.close(fig)

fig, ax = plt.subplots(figsize=(5.6, 4.2))
for (dl, c) in ((0.5, C1), (1.0, C2)):
    Eex, Eg = Gres[dl]
    ax.loglog(epsG, np.abs(Eg - Eex), "o-", ms=6, lw=2, color=c, label=fr"$\delta={dl}$")
ax.loglog(epsG, 0.5*np.abs(Gres[0.5][1][-1] - Gres[0.5][0])*(epsG/epsG[-1])**2/0.5, ":", color="gray",
          label=r"$\propto\epsilon^2$")
ax.set_xlabel(r"$\epsilon$"); ax.set_ylabel(r"$|E_0(\epsilon)-E_0|$  [$mg^2/\hbar^2$]")
ax.set_title("Coulomb exacto + resto $W$ acotado: sesgo $O(\\epsilon^2)$", fontsize=9)
ax.legend(fontsize=7, frameon=False)
fig.tight_layout(); fig.savefig(FIG + "08_pares_coulomb.png", dpi=160); plt.close(fig)
print(f"\nFiguras: 08_pares_coulomb.png, 08_divergencia_peso.png, 08_toy_trotter.png, 08_suavizado.png. Tiempo {time.time() - t0:.0f} s")
