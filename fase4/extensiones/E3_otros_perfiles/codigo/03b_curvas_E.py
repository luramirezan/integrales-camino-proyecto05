"""03b_curvas_E.py -- E3: curvas E0(delta) y <r>(delta) del 1s en todo el intervalo 0.1 delta_c .. 0.999 delta_c
(disparo con empalme a la cola, sin caja), para la figura de energias reescaladas. Sin criterios: solo datos.
Control: Hulthen frente a -(1/2)(1 - delta/2)^2 (se informa el maximo de la diferencia)."""
import numpy as np

import comun_e3 as C
import perfiles as P


def main():
    T = C.Tee("03b_curvas_E")
    D2 = C.cargar("02_dispersion")["perfiles"]
    out = dict(script="03b_curvas_E.py", perfiles={})
    xs = np.concatenate([np.linspace(0.1, 0.9, 17), [0.95, 0.97, 0.98, 0.99, 0.995, 0.999]])
    for k in C.ORDEN:
        dc = D2[k]["delta_c"]
        filas = []
        for x in xs:
            L = P.ligado(k, dc * x)
            filas.append(dict(x=float(x), delta=float(dc * x), E0=L["E0"], kappa=L["kappa"], r_med=L["r_med"],
                              nodos=L["nodos"], n_ligados_s=len(L["raices"])))
        out["perfiles"][k] = dict(delta_c=dc, curva=filas)
        T(f"{k:8s} " + " ".join(f"{f['x']:.3f}:{f['E0']:+.4e}({f['n_ligados_s']})" for f in filas[::4]))
        if k == "hulthen":
            dmax = max(abs(f["E0"] + 0.5 * (1 - f["delta"] / 2)**2) for f in filas)
            out["hulthen_dif_max_exacta"] = float(dmax)
            T(f"hulthen: max |E0 - exacta| = {dmax:.2e}")
    C.guardar("03b_curvas_E", out)
    T.cerrar()


if __name__ == "__main__":
    main()
