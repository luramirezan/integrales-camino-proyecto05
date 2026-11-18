"""40b_umbral_fd.py -- E4: umbral delta_c con un segundo metodo independiente del integrador DOP853.

El ajuste de E(delta) del script 40 (parte C) depende del modelo de extrapolacion. Aqui se usa la condicion de energia
cero de las mismas diferencias finitas del solucionador radial: la recurrencia
    u_{j+1} = 2 u_j - u_{j-1} + 2 h^2 [V(r_j) + l(l+1)/(2 r_j^2)] u_j,   u_0 = 0,  u_1 = h^{l+1},
es exactamente la fila j de (H_FD - 0) u = 0, de modo que su umbral es el de la matriz de radial.py en caja infinita.
Lejos del potencial (r_ext = 42/delta) u = A r^{-l} + B r^{l+1}; delta_c(h) es la raiz de B (dos nodos de la malla).
Pasos h = 1/40, 1/80, 1/160, 1/320; Richardson doble (orden 2 y luego 4).
Criterio fijado ANTES de correr (17-11-2026): |delta_c(FD, Richardson) - delta_c(disparo)| < 1e-9 y orden aparente
entre 1.8 y 2.2.
Salida: resultados/40b_umbral_fd.json y _salida.txt.
"""
import math
import time

from scipy.optimize import brentq

import comun4 as c

c.Tee("40b_umbral_fd")
C40 = c.leer_json("40_controles_radial_l")["C_umbrales"]


def B_fd(l, delta, h, rext):
    N = int(round(rext / h))
    cl = 0.5 * l * (l + 1)
    um, u = 0.0, h**(l + 1)
    h2 = 2 * h * h
    for j in range(1, N):
        r = j * h
        up = 2 * u - um + h2 * (-math.exp(-delta * r) / r + cl / (r * r)) * u
        um, u = u, up
    r1, r0 = N * h, (N - 1) * h
    # u = A r^{-l} + B r^{l+1} en los dos ultimos nodos
    det = r0**(-l) * r1**(l + 1) - r1**(-l) * r0**(l + 1)
    A = (um * r1**(l + 1) - u * r0**(l + 1)) / det
    B = (u * r0**(-l) - um * r1**(-l)) / det
    x = B * r1**(2 * l + 1)
    return x / math.hypot(A, x)


out = dict(criterio=1e-9, estados={})
for nom, e in c.ESTADOS.items():
    t = time.time()
    l = e["l"]
    dref = C40[nom]["delta_c"]
    rext = 42.0 / e["br"][0]
    hs = [1 / 40, 1 / 80, 1 / 160, 1 / 320]
    ds = [brentq(lambda d: B_fd(l, d, h, rext), e["br"][0], e["br"][1], xtol=1e-15, rtol=8.9e-16) for h in hs]
    p = [math.log2((ds[i] - ds[i + 1]) / (ds[i + 1] - ds[i + 2])) for i in range(len(ds) - 2)]
    r2 = [(4 * ds[i + 1] - ds[i]) / 3 for i in range(len(ds) - 1)]
    r4 = [(16 * r2[i + 1] - r2[i]) / 15 for i in range(len(r2) - 1)]
    best = r4[-1]
    fila = dict(l=l, h=hs, delta_c_h=ds, orden=p, rich2=r2, rich4=r4, delta_c_fd=best, delta_c_disparo=dref,
                dif=best - dref, err_rich=abs(r4[-1] - r4[-2]))
    fila["pasa"] = bool(abs(fila["dif"]) < 1e-9 and 1.8 < p[-1] < 2.2)
    out["estados"][nom] = fila
    print(f"{nom} (l={l}): delta_c(h) = " + ", ".join(f"{x:.12f}" for x in ds))
    print(f"   orden aparente {', '.join(f'{x:.3f}' for x in p)};  Richardson doble {best:.13f} (+- {fila['err_rich']:.1e}); "
          f"disparo {dref:.13f};  dif = {fila['dif']:+.1e}  pasa = {fila['pasa']}  ({time.time() - t:.0f} s)", flush=True)
c.guardar_json("40b_umbral_fd", out)

# ----------------------------------------------------------------------------------------------------------------
# Diagnostico de los dos casos de la parte D del script 40 que no pasan (l = 0 cerca del umbral, h = 1/40):
# se repiten con h = 1/160 (Richardson con 1/320). Criterio fijado ANTES de correr: con h = 1/160 el error relativo
# frente al disparo baja por debajo de 1e-4 y el error absoluto escala como h^4 (cociente 1/40 frente a 1/160 > 50).
D40 = c.leer_json("40_controles_radial_l")["D_fd_vs_disparo"]
diag = []
for f in D40:
    if f["pasa"]:
        continue
    e = c.ESTADOS[f["estado"]]
    t = time.time()
    r = c.fd_rich(c.V_yukawa_np(f["delta"]), e["l"], f["R"], h=1 / 160, nev=e["nr"] + 1)
    E = r["E0" if e["nr"] == 0 else "E1"]
    z = dict(estado=f["estado"], delta=f["delta"], R=f["R"], E_disparo=f["E_disparo"], E_fd_h40=f["E_fd"], E_fd_h160=E,
             err_abs_h40=f["E_fd"] - f["E_disparo"], err_abs_h160=E - f["E_disparo"])
    z["rel_h160"] = z["err_abs_h160"] / abs(f["E_disparo"])
    z["cociente"] = abs(z["err_abs_h40"] / z["err_abs_h160"]) if z["err_abs_h160"] != 0 else float("inf")
    z["pasa"] = bool(abs(z["rel_h160"]) < 1e-4 and z["cociente"] > 50)
    diag.append(z)
    print(f"diagnostico {f['estado']} delta = {f['delta']:.8f} R = {f['R']:.0f}: error abs h=1/40 {z['err_abs_h40']:+.2e}, "
          f"h=1/160 {z['err_abs_h160']:+.2e} (rel {z['rel_h160']:+.1e}), cociente {z['cociente']:.0f}  pasa = {z['pasa']}  "
          f"({time.time() - t:.0f} s)", flush=True)
out["diagnostico_D40"] = diag
c.guardar_json("40b_umbral_fd", out)
