"""V1 parte E: proyeccion determinista con el operador de Trotter espectral (FEDVR), delta=0.2, eps=0.1, R=40.
E_mixto(tau) = <uT|E_L M^n|uT>/<uT|M^n|uT>, <r>, <r^2> puros en el eslabon central; uT = r e^{-r}.
Tambien comprueba de forma independiente delta=1.0 con una base mas fina (convergencia de la parte B).
Guarda resultados/v1e_proyeccion.json."""
import json, time
import numpy as np
import v_fedvr as F
import v_trotter as T

t0 = time.time()
W = lambda r: -np.expm1(-0.2 * r) / r
out = {}
for n_el, l1 in ((12, 0.5), (14, 0.25)):
    B = F.bordes_graduados(40.0, l1=l1, extra=(20.0,))
    S = T.Espectral(F.FEDVR(B, n_el), lambda r: -1 / r)
    taus = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 15.0, 20.0, 30.0, 60.0]
    pr = S.pigs_det(W, lambda r: W(r) - 0.5, lambda r: r * np.exp(-r), 0.1, taus)
    out[f"n{n_el}_l{l1}"] = {str(k): v for k, v in pr.items()}
    print(n_el, l1)
    for k, v in pr.items():
        print("  tau", k, v)
# convergencia de delta=1.0, R=174 (parte B usa n=12, l1=0.5, l3=4)
Wd = lambda r: -np.expm1(-1.0 * r) / r
for n_el, l1, l3 in ((12, 0.5, 4.0), (12, 0.5, 2.0), (14, 0.25, 2.0)):
    B = F.bordes_graduados(174.0, l1=l1, l3=l3, extra=(87.0,))
    S = T.Espectral(F.FEDVR(B, n_el), lambda r: -1 / r)
    Es = [S.trotter(Wd, e)["E"] for e in (0.2, 0.1, 0.05)]
    out[f"d1.0_n{n_el}_l1{l1}_l3{l3}"] = Es
    print("delta=1.0", n_el, l1, l3, len(S.f.x), Es, round(time.time() - t0, 1))
json.dump(out, open("resultados/v1e_proyeccion.json", "w"), indent=1)
print("tiempo", time.time() - t0)
