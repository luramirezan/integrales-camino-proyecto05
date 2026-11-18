"""r44_accion_pares.py -- revision R4: comprobaciones independientes del nucleo libre K_1 y de la accion de pares U_1
(onda p) de E4.
 (1) K_l frente a la transformada de Hankel exacta K_l(r,r') = (2/pi) int_0^inf e^{-eps k^2/2} (kr) j_l(kr) (kr') j_l(kr') dk
     (scipy.integrate.quad; no usa ive ni la formula de E4).
 (2) Semigrupo: int K_1(r,s;eps) K_1(s,r';eps) ds = K_1(r,r';2 eps).
 (3) rho_1 = <r|exp(-eps H_1)|r'> de Coulomb + centrifugo con colocacion de Chebyshev (no la red de diferencias
     finitas de E4): suma espectral con autofunciones normalizadas por Clenshaw-Curtis en la caja [0, 14];
     U_1 = -ln(rho_1/K_1) frente a la tabla de E4 (Richardson h_tab = 0.01, 0.005).
Salida: revision/r44_accion_pares.json y _salida.txt."""
import json, math, os, sys, time
import numpy as np
from scipy.special import spherical_jn, ive
from scipy.integrate import quad

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), "codigo"))
import pares_l as pl          # solo para leer la tabla cacheada de E4 y su logK_l (lo que se pone a prueba)
import espectral as s

log = open(os.path.join(AQUI, "r44_accion_pares_salida.txt"), "w")
def p(*a):
    t = " ".join(str(x) for x in a); print(t, flush=True); log.write(t + "\n"); log.flush()
out = {}
T0 = time.time()

# (1) Hankel
def K_hankel(r, rp, eps, l):
    f = lambda k: math.exp(-eps * k * k / 2) * (k * r) * spherical_jn(l, k * r) * (k * rp) * spherical_jn(l, k * rp)
    kmax = math.sqrt(2 * 40 / eps)
    return 2 / math.pi * quad(f, 0, kmax, limit=2000, epsabs=0, epsrel=1e-12)[0]
filas = []
for (r, rp, eps) in ((0.05, 0.08, 0.1), (0.3, 0.5, 0.1), (1.0, 1.2, 0.2), (2.0, 2.0, 0.05), (5.0, 5.3, 0.1), (0.5, 0.5, 0.2)):
    for l in (1, 2):
        kh = K_hankel(r, rp, eps, l)
        ke = math.exp(float(pl.logK_l(r, rp, eps, l)))
        filas.append(dict(r=r, rp=rp, eps=eps, l=l, hankel=kh, E4=ke, rel=(ke - kh) / kh))
        p(f"(1) K_{l}({r},{rp};{eps}): Hankel {kh:.15e}  E4 {ke:.15e}  rel {filas[-1]['rel']:+.1e}")
out["hankel"] = filas
# (2) semigrupo
filas = []
for (r, rp, eps) in ((0.3, 0.4, 0.05), (1.0, 1.5, 0.1), (3.0, 3.0, 0.2)):
    f = lambda x: math.exp(float(pl.logK_l(r, x, eps, 1) + pl.logK_l(x, rp, eps, 1)))
    I = quad(f, 1e-12, max(r, rp) + 40 * math.sqrt(eps), limit=500, epsabs=0, epsrel=1e-12)[0]
    k2 = math.exp(float(pl.logK_l(r, rp, 2 * eps, 1)))
    filas.append(dict(r=r, rp=rp, eps=eps, int=I, K2eps=k2, rel=(I - k2) / k2))
    p(f"(2) semigrupo K_1 ({r},{rp};{eps}): rel {filas[-1]['rel']:+.1e}")
out["semigrupo"] = filas

# (3) rho_1 espectral
def bary(tn, fvals, tq):
    N = len(tn) - 1
    w = (-1.0) ** np.arange(N + 1); w[0] *= 0.5; w[-1] *= 0.5
    d = tq[:, None] - tn[None, :]
    exact = np.isclose(d, 0, atol=1e-15)
    d[exact] = 1.0
    C = w / d
    res = (C @ fvals) / C.sum(axis=1)[:, None]
    for i, j in zip(*np.nonzero(exact)):
        res[i] = fvals[j]
    return res

def rho_espectral(eps, N, c, RB=14.0, l=1):
    m = s.Malla(RB, N, c)
    H = -0.5 * m.D2 + np.diag(0.5 * l * (l + 1) / np.where(m.r > 0, m.r, 1)**2 - 1 / np.where(m.r > 0, m.r, 1))
    Hi = H[1:N, 1:N]
    w, V = np.linalg.eig(Hi)
    ok = (np.abs(w.imag) < 1e-9) & (w.real * eps < 45)
    w, V = w[ok].real, V[:, ok].real
    Vf = np.zeros((N + 1, V.shape[1])); Vf[1:N] = V
    nrm = np.sqrt(m.w @ Vf**2)
    Vf = Vf / nrm
    o = np.argsort(w)
    return m, w[o], Vf[:, o]

def t_de_r(r, m):
    b = math.asinh(m.Rx / m.c)
    return 2 * np.arcsinh(np.asarray(r) / m.c) / b - 1

puntos = [(0.01, 0), (0.02, 0), (0.01, 1), (0.05, 0), (0.1, 0), (0.5, 0), (1.0, 0), (3.0, 0), (9.0, 0), (0.1, 1), (0.5, 1), (1.0, 1), (3.0, 1)]
out["U1"] = {}
for eps in (0.2, 0.1, 0.05):
    tb = pl.tabla_richardson_l(1, eps)      # cache de E4 (solo lectura)
    res = {}
    for N, c in ((700, 8.0), (900, 8.0)):
        m, w, Vf = rho_espectral(eps, N, c)
        vals = []
        for r, off in puntos:
            rp = r + off * math.sqrt(eps)
            k = int(round(r / tb.h)) - 1
            mm = int(round((rp - r) / tb.h))
            rp = r + mm * tb.h
            phi = bary(m.t, Vf, t_de_r(np.array([r, rp]), m))
            rho = float(np.sum(np.exp(-eps * w) * phi[0] * phi[1]))
            K = math.exp(float(pl.logK_l(r, rp, eps, 1)))
            U = -math.log(rho / K)
            vals.append(dict(r=r, rp=rp, U_esp=U, U_E4=float(tb.Ub[k, mm]), dif=U - float(tb.Ub[k, mm]),
                             err_h001=float(tb.U1[k, mm]) - U, err_h0005=float(tb.U2[k, mm]) - U))
        res[N] = dict(vals=vals, nest=len(w))
    out["U1"][str(eps)] = {str(k): v for k, v in res.items()}
    for a, b in zip(res[700]["vals"], res[900]["vals"]):
        p(f"(3) eps={eps} r={a['r']:<4} r'={a['rp']:.4f}: U_esp(N=900) = {b['U_esp']:+.10f}  E4 = {b['U_E4']:+.10f}  "
          f"dif = {b['dif']:+.1e}  (N 700->900: {b['U_esp'] - a['U_esp']:+.1e}; error de U_h=0.01 {-b['err_h001']:+.1e}, de U_h=0.005 {-b['err_h0005']:+.1e})")
out["t"] = time.time() - T0
json.dump(out, open(os.path.join(AQUI, "r44_accion_pares.json"), "w"), indent=1, default=float)
p(f"tiempo {out['t']:.0f} s")
