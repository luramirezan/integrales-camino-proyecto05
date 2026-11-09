"""Bloque 03: cota inferior variacional del umbral de enlace (Yukawa).
Unidades: hbar=m=g=1 (radios de Bohr a=hbar^2/(m g), energia m g^2/hbar^2).
H = -1/2 Lap - exp(-delta r)/r ; estado l=0.
"""
import os as _os
_RAIZ = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..','..'))  # raiz del repositorio
import numpy as np, sympy as sp
from scipy.optimize import minimize, minimize_scalar, brentq
from scipy.linalg import eigh
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

r, b, d, c = sp.symbols('r b delta c', positive=True)
print("=== 1. Prueba hidrogenoide psi = exp(-r/b) ===")
psi = sp.exp(-r/b)
N = sp.integrate(psi**2*r**2, (r, 0, sp.oo))
T = sp.integrate(sp.Rational(1,2)*sp.diff(psi, r)**2*r**2, (r, 0, sp.oo))/N
V = -sp.integrate(psi**2*sp.exp(-d*r)/r*r**2, (r, 0, sp.oo))/N
E = sp.simplify(T+V)
print("N =", N, " <T> =", sp.simplify(T), " <V> =", sp.simplify(V))
print("E(b,delta) =", E)
# comprobacion: E = 1/(2b^2) - 4/(b(2+delta b)^2)
assert sp.simplify(E - (1/(2*b**2) - 4/(b*(2+d*b)**2))) == 0
# delta=0 -> hidrogeno
E0 = E.subs(d, 0); bmin = sp.solve(sp.diff(E0, b), b); print("delta=0: b*=", bmin, "E=", E0.subs(b, bmin[0]))
# condicion E<0  <=>  P(b)= delta^2 b^2 + (4 delta - 8) b + 4 < 0
P = sp.expand((2+d*b)**2 - 8*b); disc = sp.factor(sp.discriminant(P, b))
print("P(b) =", P, " discriminante =", disc)
print("raices de P en delta<1:", sp.solve(P, b))
# Comprobacion con beta=1/b (notacion del guion)
beta = sp.symbols('beta', positive=True)
print("E(beta) =", sp.simplify(E.subs(b, 1/beta)))
# en delta=1: raiz doble b=4, E(4,1)=0
print("P(b) en delta=1:", sp.factor(P.subs(d,1)), "-> raiz doble b=2")
print("E(b=2,delta=1) =", E.subs({b:2, d:1}), " dE/db(2,1) =", sp.diff(E, b).subs({b:2, d:1}))
# umbral analitico: E<0 <=> delta < g1(x)=8x/(x+2)^2, x=delta*b
x = sp.symbols('x', positive=True); g1 = 8*x/(x+2)**2
xs = sp.solve(sp.diff(g1, x), x); print("max g1 en x=", xs, " delta_c^(1) =", g1.subs(x, xs[0]))

def Emin1(delta):
    f = lambda lb: float(E.subs({b: sp.exp(lb), d: delta}).evalf()) if False else \
        (0.5*np.exp(-2*lb) - 4/(np.exp(lb)*(2+delta*np.exp(lb))**2))
    # busqueda acotada alrededor de b*=2/delta (b* esta en [1,2] para 0<=delta<=1); evita que el
    # minimizador escape a b->inf, donde E->0+ (artefacto senalado en la revision)
    hi = np.log(4.0/delta) if delta > 0 else np.log(12.0)
    g = np.linspace(np.log(0.5), hi, 3001); k = np.argmin(f(g))
    res = minimize_scalar(f, bounds=(g[max(k-1,0)], g[min(k+1,len(g)-1)]), method='bounded')
    return res.fun, np.exp(res.x)
for dd in [0, 0.5, 0.9, 0.99, 1.0, 1.01]:
    em, bs = Emin1(dd)
    nota = "  (minimo en el borde de la ventana: para delta>1 el infimo es 0+ con b->inf)" if dd > 1 else ""
    print(f"  delta={dd}: Emin={em:.6e}  b*={bs:.4f}{nota}")
# integral numerica de comprobacion
from scipy.integrate import quad
bb, dd = 1.7, 0.6
num = (quad(lambda x: 0.5*np.exp(-2*x/bb)/bb**2*x**2, 0, np.inf)[0]
       - quad(lambda x: np.exp(-2*x/bb)*np.exp(-dd*x)*x, 0, np.inf)[0]) / quad(lambda x: np.exp(-2*x/bb)*x**2, 0, np.inf)[0]
print("chequeo numerico E(1.7,0.6):", num, float(E.subs({b:bb, d:dd})))

print("=== 2. Prueba mejorada psi = (1+c r) exp(-r/b) ===")
psi2 = (1+c*r)*sp.exp(-r/b)
N2 = sp.simplify(sp.integrate(psi2**2*r**2, (r, 0, sp.oo)))
T2 = sp.simplify(sp.integrate(sp.Rational(1,2)*sp.diff(psi2, r)**2*r**2, (r, 0, sp.oo)))
V2 = sp.simplify(-sp.integrate(psi2**2*sp.exp(-d*r)*r, (r, 0, sp.oo)))
print("N2 =", N2); print("T2 =", T2); print("V2 =", V2)
assert sp.simplify(((T2+V2)/N2).subs(c, 0) - E) == 0
E2f = sp.lambdify((b, c, d), (T2+V2)/N2, 'numpy')
def Emin2(delta):
    # parametros: lb=ln b, t=c*b (adimensional); t>-1/2 aprox. asegura N>0 (3t^2+3t+1>0 siempre)
    f = lambda p: E2f(np.exp(p[0]), p[1]/np.exp(p[0]), delta)
    LB, TT = np.meshgrid(np.linspace(-3, 8, 221), np.linspace(-0.9, 6, 139))
    with np.errstate(all='ignore'): Z = E2f(np.exp(LB), TT/np.exp(LB), delta)
    k = np.nanargmin(Z); p0 = (LB.flat[k], TT.flat[k])
    res = minimize(f, p0, method='Nelder-Mead', options=dict(xatol=1e-10, fatol=1e-16, maxiter=4000))
    return res.fun, np.exp(res.x[0]), res.x[1]
# umbral analitico-reducido: E<0 <=> delta < g2(x,t)
t = sp.symbols('t', real=True)
g2 = sp.simplify(8*x*(6*t**2+4*t*(x+2)+(x+2)**2)/((t**2+t+1)*(x+2)**4))
num_check = sp.simplify(((T2+V2)).subs({c: t/b}).subs(b, x/d))
print("g2(x,t) =", g2)
g2f = sp.lambdify((x, t), -g2, 'numpy')
best = min((minimize(lambda p: g2f(np.exp(p[0]), p[1]), (lx, tt), method='Nelder-Mead',
            options=dict(xatol=1e-12, fatol=1e-15)) for lx in [0, 1, 2, 3] for tt in [0, 0.5, 1, 2]), key=lambda r_: r_.fun)
dc2 = -best.fun
print(f"umbral con (1+cr)e^{{-r/b}}: delta_c >= {dc2:.6f} en x=delta*b={np.exp(best.x[0]):.5f}, t=c*b={best.x[1]:.5f}")
print("  chequeo: Emin2(dc2-1e-3)=", Emin2(dc2-1e-3)[0], " Emin2(dc2+1e-3)=", Emin2(dc2+1e-3)[0])

# comparacion cuantitativa E2min vs E1min y c* (malla de delta con estado ligado en la familia 1)
dmesh = np.linspace(0, 0.99, 34); dif = []; tst = []
for v in dmesh:
    e2v, b2v, t2v = Emin2(v); dif.append(abs(e2v - Emin1(v)[0])); tst.append(abs(t2v))
print(f"max|E2min-E1min| en delta in [0,0.99] (34 puntos) = {max(dif):.2e};  max|t*|=|c* b*| = {max(tst):.2e}")
# dE/dc en c=0 coincide con la condicion dE/db=0 de la prueba de 1 parametro
dEc = sp.factor(sp.diff((T2+V2)/N2, c).subs(c, 0)); print("dE/dc|_{c=0} =", dEc)
stat = sp.expand((2+d*b)**3 - 4*b*(2+3*d*b)); print("condicion dE1/db=0 <=>", stat, "= 0")
print("dE1/db =", sp.factor(sp.diff(E, b)))
# serie de E_min^(1) para delta pequeno
eps = sp.symbols('epsilon'); bser = 1 + sum(sp.Symbol(f'k{i}')*eps**i for i in (1,2,3))
ser = sp.series(sp.diff(E, b).subs({b: bser, d: eps}), eps, 0, 4).removeO()
sol = sp.solve([ser.coeff(eps, i) for i in (1,2,3)], [sp.Symbol(f'k{i}') for i in (1,2,3)], dict=True)[0]
print("b*(delta) =", bser.subs(sol), " E_min^(1)(delta) =", sp.series(E.subs({b: bser.subs(sol), d: eps}), eps, 0, 4))

print("=== 3. Base de N exponenciales (Ritz lineal) u=sum c_i r e^{-a_i r} ===")
def ritz(delta, a):
    A = a[:, None]; B = a[None, :]; s = A + B
    S = 2/s**3
    Tm = 0.5*(1/s - (A+B)/s**2 + 2*A*B/s**3)
    Vm = -1/(s+delta)**2
    if not np.all(np.isfinite(a)) or a.min() <= 0: return 1e3
    # ortogonalizacion canonica (descarta direcciones casi linealmente dependientes)
    w, U = np.linalg.eigh(S); keep = w > 1e-13*w.max()
    X = U[:, keep]/np.sqrt(w[keep])
    return np.linalg.eigvalsh(X.T@(Tm+Vm)@X)[0]
# verificacion simbolica de los elementos de matriz
a1, a2, s_ = sp.symbols('a1 a2 s', positive=True)
u1, u2 = r*sp.exp(-a1*r), r*sp.exp(-a2*r)
assert sp.simplify(sp.integrate(u1*u2, (r,0,sp.oo)) - 2/(a1+a2)**3) == 0
assert sp.simplify(sp.integrate(sp.Rational(1,2)*sp.diff(u1,r)*sp.diff(u2,r), (r,0,sp.oo))
       - sp.Rational(1,2)*(1/(a1+a2) - (a1+a2)/(a1+a2)**2 + 2*a1*a2/(a1+a2)**3)) == 0
assert sp.simplify(-sp.integrate(u1*u2*sp.exp(-d*r)/r, (r,0,sp.oo)) + 1/(a1+a2+d)**2) == 0
print("elementos de matriz verificados con sympy")
def Eritz(delta, Nb):
    f = lambda p: ritz(delta, np.exp(np.clip(p[0], -12, 3)) * np.exp(np.clip(p[1], 0.15, 2.5))**np.arange(Nb))
    best = min((minimize(f, (l0, l1), method='Nelder-Mead', options=dict(xatol=1e-9, fatol=1e-15))
                for l0 in [-6, -4, -2] for l1 in [0.5, 1.0, 1.5]), key=lambda r_: r_.fun)
    return best.fun
print("Ritz N=10 delta=0:", Eritz(0, 10))
res3 = {}
for Nb in [2, 4, 8, 12, 16]:
    res3[Nb] = brentq(lambda v: Eritz(v, Nb), 1.0, 1.25, xtol=1e-7)
    print(f"  N={Nb}: delta_c >= {res3[Nb]:.6f}")

# Figura
ds = np.linspace(0, 1.3, 131)
e1 = [min(Emin1(v)[0], 0) for v in ds]
e2 = [min(Emin2(v)[0], 0) for v in ds]
eN = [min(Eritz(v, 12), 0) for v in ds]
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.plot(ds, e1, label=r'$e^{-r/b}$ (1 parámetro)')
ax.plot(ds, e2, '--', label=r'$(1+cr)e^{-r/b}$ (2 parámetros)')
ax.plot(ds, eN, ':', lw=2, label='12 exponenciales (Ritz)')
ax.axhline(0, color='gray', lw=0.6)
for xv, lab in [(1, r'$\delta=1$'), (dc2, None), (1.1906, r'lit. $1.1906$')]:
    ax.axvline(xv, color='gray', ls=':', lw=0.7)
ax.text(1.0, -0.45, r'$\delta=1$', rotation=90, ha='right'); ax.text(1.1906, -0.45, r'$\delta_c^{lit}=1.1906$', rotation=90, ha='right')
ax.set_xlabel(r'$\delta=\mu a$'); ax.set_ylabel(r'$E_{\min}$ [$mg^2/\hbar^2$]')
ax.set_title('Cota variacional de la energía del estado base (ℓ=0)'); ax.legend(); ax.grid(alpha=.3)
fig.tight_layout(); fig.savefig(_RAIZ + '/fase1/figuras/03_Emin_vs_delta.png', dpi=160)
print("tabla:")
for xv in [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.1]:
    e1v = Emin1(xv)[0] if xv <= 1 else 0.0   # delta>1: infimo 0+ con b->inf (sin ligado en la familia)
    print(f"  {xv}: {e1v:.6f} {Emin2(xv)[0]:.6f} {Eritz(xv,12):.6f}")
