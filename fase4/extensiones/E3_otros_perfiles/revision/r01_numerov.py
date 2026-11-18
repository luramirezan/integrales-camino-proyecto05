"""r01_numerov.py -- Revision independiente de E3 (revisor R3, 17-11-2026).

Metodo distinto del de E3 (que usa solve_ivp DOP853 adaptativo y arranque de Frobenius en r0 = 1e-6):
aqui todo se hace con Numerov de paso fijo h desde r = 0 (u regular es analitica en r para V = -1/r + W(r)
con W analitica, asi que Numerov conserva su orden 4), vectorizado sobre un lote de parametros, y con
extrapolacion de Richardson h -> h/2 (h^4). Las integrales (r_e de Bethe, c) se hacen con Simpson sobre la malla.
No importa nada de E3: los potenciales se reescriben aqui.

Calcula: delta_c (1/a = 0), 1/a y r_e en 2-3 puntos por perfil, c = 2 int dV/dd phi0^2, d2 y B del Yukawa
(B = d2 + r_e c^2/2), y en el ECSC r_e(delta_c); kappa de ligados cerca del umbral (ajuste A, B); energias de caja
en delta_c (punto fijo) y dos cruces por perfil; polo virtual del Hulthen. Escribe revision/r01_numerov.json.
"""
import json
import os
import sys
import time

import numpy as np
from scipy.optimize import brentq
from numba import njit

AQUI = os.path.dirname(os.path.abspath(__file__))


# --------------------------------------------------------------------------------------------- potenciales
def V(perfil, d, r):
    r = np.asarray(r, float)
    with np.errstate(divide="ignore", invalid="ignore"):
        if perfil == "yukawa":
            v = -np.exp(-d * r) / r
        elif perfil == "ecsc":
            v = -np.exp(-d * r) * np.cos(d * r) / r
        elif perfil == "hulthen":
            v = -d / np.expm1(d * r)
        elif perfil == "hatomo":
            v = -(1 / r + d / 2) * np.exp(-d * r)
    return v


def dVdd(perfil, d, r, h=1e-5):
    # derivada respecto de delta por diferencia centrada de 4 puntos (E3 la usa analitica: otro camino)
    return (-V(perfil, d + 2 * h, r) + 8 * V(perfil, d + h, r) - 8 * V(perfil, d - h, r) + V(perfil, d - 2 * h, r)) / (12 * h)


@njit(cache=True)
def _nucleo(f, u, h):
    # u[0] = 0, u[1] dado; (f u)(0) = -2
    q = h * h / 12
    N = u.shape[0] - 1
    y_prev = 2 * q
    y_cur = (1 - q * f[0]) * u[1]
    for n in range(1, N):
        y_next = 2 * y_cur - y_prev + h * h * f[n - 1] * u[n]
        u[n + 1] = y_next / (1 - q * f[n])
        y_prev = y_cur
        y_cur = y_next


def numerov(perfil, d, E, h, rf):
    """u'' = f u, f = 2(V - E). Devuelve r, u (u'(0) = 1, u(0) = 0). E puede ser un array (lote)."""
    E = np.atleast_1d(np.asarray(E, float))
    N = int(round(rf / h))
    r = h * np.arange(N + 1)
    Vr = V(perfil, d, r[1:])
    u = np.zeros((N + 1, E.size))
    # (f u)(0) = lim 2 V r * u'(0) = -2  (V ~ -1/r)
    fu0 = -2.0
    # u(h) por la serie u = r - r^2 + c3 r^3 + c4 r^4 con c3 = (2 + 2 (W0 - E))/6; c4 se toma 0 (error h^4 local, de orden
    # menor que el global h^4 de Numerov; la extrapolacion h -> h/2 lo comprueba)
    W0 = {"yukawa": d, "ecsc": d, "hulthen": d / 2, "hatomo": d / 2}[perfil]
    c3 = (2 + 2 * (W0 - E)) / 6
    # c4 de la serie: u'' = 2(V - E) u con V = -1/r + W0 + W1 r, W1 = W'(0)
    W1 = {"yukawa": -d * d / 2, "ecsc": -d * d / 3 * 0, "hulthen": -d * d / 12, "hatomo": 0.0}[perfil]
    if perfil == "ecsc":
        W1 = 0.0          # W = d(1 - x^2/3 + ...): sin termino lineal
    # 12 c4 r^2 = 2[-c3 r^2 + (W0 - E) (-r^2) + W1 r^2]  =>  c4 = (-2 c3 - 2 (W0 - E) + 2 W1)/12
    c4 = (-2 * c3 - 2 * (W0 - E) + 2 * W1) / 12
    u[1] = h - h**2 + c3 * h**3 + c4 * h**4
    f = 2 * (Vr[:, None] - E[None, :])      # f en r_1..r_N
    for j in range(E.size):
        _nucleo(np.ascontiguousarray(f[:, j]), u[:, j], h)
    return r, u


def simpson(y, h):
    n = len(y) - 1
    if n % 2:
        # ultimo intervalo por trapecio corregido (no deberia ocurrir: N par)
        raise ValueError("N impar")
    return h / 3 * (y[0] + y[-1] + 4 * y[1:-1:2].sum(0) + 2 * y[2:-1:2].sum(0))


RF = 60.0


def cero(perfil, d, h):
    rf = RF / d
    N = 2 * int(round(rf / h / 2))
    rf = N * h
    r, u = numerov(perfil, d, 0.0, h, rf)
    u = u[:, 0]
    beta = (u[-1] - u[-2]) / h          # fuera del alcance u es lineal
    alfa = u[-1] - beta * r[-1]
    ia = -beta / alfa
    phi = u / alfa
    psi = 1 - r * ia
    re = 2 * simpson(psi**2 - phi**2, h)
    c = 2 * simpson(np.where(r > 0, dVdd(perfil, d, np.maximum(r, 1e-300)), 0.0) * phi**2, h)
    # en r = 0 dV/dd es finita (Yukawa 1, ECSC 1, Hulthen -1/2 + ...); se corrige el punto r = 0 aparte
    dv0 = {"yukawa": 1.0, "ecsc": 1.0, "hulthen": 0.5, "hatomo": 0.5}[perfil]
    # phi(0) = 0, asi que el punto r = 0 no aporta: no hace falta dv0
    return dict(inv_a=ia, r_e=re, c=c, phimax=float(phi.max()), r_phimax=float(r[np.argmax(phi)]))


def rich(fun, *a, h=0.004):
    x1, x2 = fun(*a, h=h), fun(*a, h=h / 2)
    return {k: (16 * x2[k] - x1[k]) / 15 for k in x1}, {k: abs(x2[k] - x1[k]) for k in x1}


def inv_a(perfil, d, h=0.004):
    return rich(lambda p, dd, h: {"ia": cero(p, dd, h)["inv_a"]}, perfil, d, h=h)[0]["ia"]


def g_ligado(perfil, d, kap, h):
    """Discrepancia de empalme con e^{-kappa r}: componente creciente B de u = A e^{-k r} + B e^{k r} en r_f."""
    rf = RF / d
    N = int(round(rf / h)); rf = N * h
    r, u = numerov(perfil, d, -0.5 * np.atleast_1d(kap)**2, h, rf)
    k = np.atleast_1d(kap)
    r1, r2 = r[-2], r[-1]
    u1, u2 = u[-2], u[-1]
    # resolver A, B con dos puntos: B = (u2 e^{-k r1} - u1 e^{-k r2}) / (e^{k r2} e^{-k r1} - e^{k r1} e^{-k r2})
    Bc = (u2 * np.exp(-k * r1) - u1 * np.exp(-k * r2)) / (np.exp(k * (r2 - r1)) - np.exp(-k * (r2 - r1)))
    A = u2 * np.exp(k * r2) - Bc * np.exp(2 * k * r2)
    return Bc * np.exp(k * r2) / np.hypot(u2, u1)


def kappa(perfil, d, guess, h):
    f = lambda k: float(g_ligado(perfil, d, k, h)[0])
    lo, hi = guess * 0.7, guess * 1.3
    return brentq(f, lo, hi, xtol=1e-15, rtol=1e-14)


def g_virtual(perfil, d, kap, h):
    rf = RF / d
    N = int(round(rf / h)); rf = N * h
    r, u = numerov(perfil, d, -0.5 * kap**2, h, rf)
    r1, r2 = r[-2], r[-1]; u1, u2 = u[-2, 0], u[-1, 0]
    # componente decreciente A de u = A e^{-k r} + B e^{k r}
    A = (u1 * np.exp(kap * r2) - u2 * np.exp(kap * r1)) / (np.exp(kap * (r2 - r1)) - np.exp(-kap * (r2 - r1)))
    return A / np.hypot(u1, u2)


def caja_E(perfil, d, R, h, Eg):
    N = int(round(R / h))
    hh = R / N
    f = lambda E: float(numerov(perfil, d, E, hh, R)[1][-1, 0])
    lo, hi = Eg * 0.8 if Eg > 0 else Eg * 1.2, Eg * 1.2 if Eg > 0 else Eg * 0.8
    return brentq(f, lo, hi, xtol=1e-17, rtol=1e-14)


def caja(perfil, d, R, Eg, h=0.02):
    e1, e2 = caja_E(perfil, d, R, h, Eg), caja_E(perfil, d, R, h / 2, Eg)
    return (16 * e2 - e1) / 15, abs(e2 - e1)


def main():
    t0 = time.perf_counter()
    out = {}
    E3 = json.load(open(os.path.join(AQUI, "..", "resultados", "02_dispersion.json")))["perfiles"]
    E3c = json.load(open(os.path.join(AQUI, "..", "resultados", "04_cajas_universalidad.json")))["perfiles"]
    brk = {"yukawa": (1.15, 1.25), "ecsc": (0.70, 0.74), "hulthen": (1.95, 2.05), "hatomo": (1.75, 1.9)}
    for p in ("yukawa", "ecsc", "hulthen", "hatomo"):
        res = {}
        dc = brentq(lambda d: inv_a(p, d), *brk[p], xtol=1e-14)
        # estabilidad con h mayor
        dc2 = brentq(lambda d: inv_a(p, d, h=0.008), *brk[p], xtol=1e-14)
        res["delta_c"] = dc; res["delta_c_h008"] = dc2; res["delta_c_E3"] = E3[p]["delta_c"]
        z, ez = rich(cero, p, dc)
        res.update(c=z["c"], r_e_c=z["r_e"], err_c=ez["c"], err_re=ez["r_e"], phimax=z["phimax"],
                   c_E3=E3[p]["c_HF"], r_e_E3=E3[p]["r_e_c"])
        # d2 por diferencias de 1/a (paso 2e-3 dc) y B
        hs = 2e-3 * dc
        ip, im = inv_a(p, dc + hs), inv_a(p, dc - hs)
        d2 = 0.5 * (ip + im - 2 * inv_a(p, dc)) / hs**2
        res["d2"] = d2; res["B_pred"] = d2 + 0.5 * z["r_e"] * z["c"]**2; res["B_pred_E3"] = E3[p]["B_pred"]
        # puntos a(delta), r_e(delta)
        pts = []
        for cmp in E3[p]["comparacion"]:
            if cmp["rel"] == 0.0:
                continue
            if abs(cmp["rel"]) != 0.05 and abs(cmp["rel"]) != 0.01:
                continue
            zz, _ = rich(cero, p, cmp["delta"])
            pts.append(dict(delta=cmp["delta"], inv_a=zz["inv_a"], inv_a_E3=cmp["inv_a_1"], r_e=zz["r_e"], r_e_E3=cmp["r_e_1"]))
        res["puntos"] = pts
        # kappa ligado: s = 1e-4, 1e-3, 3e-3, 1e-2 y ajuste A D + B D^2 + C D^3
        ss = [1e-4, 3e-4, 1e-3, 3e-3, 1e-2]
        Ds, ks = [], []
        for s in ss:
            d = dc * (1 - s)
            g = z["c"] * dc * s
            k1 = kappa(p, d, g, 0.004); k2 = kappa(p, d, g, 0.002)
            Ds.append(dc * s); ks.append((16 * k2 - k1) / 15)
        Ds, ks = np.array(Ds), np.array(ks)
        A, B, C3 = np.linalg.lstsq(np.vstack([Ds, Ds**2, Ds**3]).T, ks, rcond=None)[0]
        res["ajuste_kappa"] = dict(A=A, B=B, C3=C3, D=Ds.tolist(), kappa=ks.tolist())
        # caja en delta_c: R = 200 y 800 ; cruces 100/200 y 200/400
        fij = []
        for R in (200, 800):
            Eg = np.pi**2 / (8 * R**2) * (1 + z["r_e"] / R)
            E, eE = caja(p, dc, R, Eg)
            E3v = [x for x in E3c[p]["punto_fijo"] if x["R"] == R][0]
            fij.append(dict(R=R, E0=E, err=eE, E0_E3=E3v["E0"], valor=2 * R * R * E / np.pi**2))
        res["punto_fijo"] = fij
        cr = []
        for R1 in (100, 200):
            R2 = 2 * R1
            pred = dc + z["r_e"] * np.pi**2 / (8 * z["c"] * R1 * R2)

            def gg(d):
                Eg1 = np.pi**2 / (8 * R1**2) * (1 + z["r_e"] / R1)
                Eg2 = np.pi**2 / (8 * R2**2) * (1 + z["r_e"] / R2)
                return caja(p, d, R1, Eg1, h=0.02)[0] * R1**2 - caja(p, d, R2, Eg2, h=0.02)[0] * R2**2
            span = 3 * abs(pred - dc)
            ds_ = brentq(gg, dc - span, dc + span, xtol=1e-13)
            E3x = [x for x in E3c[p]["cruces"] if x["R1"] == R1][0]
            cr.append(dict(R1=R1, R2=R2, delta_star=ds_, dif=ds_ - dc, pred_1orden=pred - dc, delta_star_E3=E3x["delta_star"]))
        res["cruces"] = cr
        out[p] = res
        print(p, json.dumps(res, default=float)[:3000], flush=True)
    # Hulthen: polo virtual en delta = 2.04 y 2.2 frente a delta/2 - 1; e-H estatico a(delta = 2)
    hv = []
    for d in (2.04, 2.2):
        kv = brentq(lambda k: g_virtual("hulthen", d, k, 0.002), (d / 2 - 1) * 0.8, (d / 2 - 1) * 1.2, xtol=1e-15)
        hv.append(dict(delta=d, kappa_v=kv, exacto=d / 2 - 1))
    out["hulthen_virtual"] = hv
    zH, _ = rich(cero, "hatomo", 2.0)
    out["eH_estatico"] = dict(a=1 / zH["inv_a"], r_e=zH["r_e"])
    out["tiempo_s"] = time.perf_counter() - t0
    print(json.dumps({k: out[k] for k in ("hulthen_virtual", "eH_estatico", "tiempo_s")}, default=float))
    json.dump(out, open(os.path.join(AQUI, "r01_numerov.json"), "w"), indent=1, default=float)


if __name__ == "__main__":
    main()
