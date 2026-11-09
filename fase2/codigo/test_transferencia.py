"""test_transferencia.py -- pruebas con assert de pares.py y transferencia.py (Fase 2, proyecto 05).

Ejecutar:  python test_transferencia.py   (tarda unos segundos si las tablas ya estan en la cache).
Determinista: no hay semillas.
"""
import numpy as np
import pares
import transferencia as tr


def test_tabla():
    t = pares.tabla_richardson(0.1)
    F = t.completa()
    assert np.allclose(F, F.T, equal_nan=True), "U_C no simetrica"
    assert t.info["n_no_positivos"] == (0, 0), "rho no positivo dentro de la banda"
    k, m = np.meshgrid(np.arange(t.nt), np.arange(t.nb + 1), indexing="ij")
    assert np.isfinite(t.Ub[k + m < t.nt]).all(), "NaN dentro de la banda"
    # finita cerca del origen (peso normalizable) y valor de la Fase 1 (U(0.02,0.02;0.1) = -0.7689)
    assert abs(t.Ub[1, 0] - (-0.7689)) < 5e-4, t.Ub[1, 0]
    # error de tabulacion entre h_tab = 0.01 y 0.005 pequeno (Fase 1: 5.3e-5 en |r-r'| <= 1)
    nb1 = int(round(1.0 / t.h))
    assert np.nanmax(np.abs(t.U1[:, :nb1 + 1] - t.U2[:, :nb1 + 1])) < 1e-4
    # lejos del origen se acerca a la aproximacion de extremos
    k9 = int(round(9.0 / t.h)) - 1
    assert abs(t.Ub[k9, 0] - pares.U_extremos(9.0, 9.0, 0.1)) < 1e-5
    # interpolacion: reproduce los nodos
    a = t.r[[0, 5, 100, 900]]
    for met in ("bilineal", "bicubica"):
        assert np.allclose(t.valor(a, a, met), t.Ub[[0, 5, 100, 900], 0], atol=1e-10)
    # fuera de la banda: NaN; fuera de la tabla: extremos
    assert np.isnan(t.valor(1.0, 1.0 + 1.1 * t.banda)).all()
    assert abs(t.valor(12.0, 12.1)[0] - pares.U_extremos(12.0, 12.1, 0.1)) < 1e-15


def test_coulomb():
    t = pares.tabla_richardson(0.1)
    o = tr.resolver(40.0, 0.02, 0.1, W=tr.W_yukawa(0.0), tabla=t)
    assert abs(o["E0"] + 0.5) < 1e-6, o["E0"]
    assert abs(o["r_med"] - 1.5) < 1e-4, o["r_med"]
    assert abs(o["r2_med"] - 3.0) < 1e-3, o["r2_med"]
    assert o["min_T"] > 0, "elemento no positivo en la banda"
    T, r = tr.matriz_T(40.0, 0.02, 0.1, tabla=t)
    assert abs(T - T.T).max() == 0.0, "T no simetrica"
    assert np.isfinite(T.data).all()


def test_yukawa_02():
    t = pares.tabla_richardson(0.1)
    o = tr.resolver(40.0, 0.02, 0.1, W=tr.W_yukawa(0.2), tabla=t)
    assert abs(o["E0"] - (-0.32680851)) < 1e-6, o["E0"]
    assert abs(o["r_med"] - 1.5497) < 1e-3, o["r_med"]


def test_sin_UC_oscilador():
    # oscilador 3D, l = 0: E0 = 3/2, <r> = 2/sqrt(pi); opcion sin U_C, ley eps^2
    V = lambda r: 0.5 * r**2
    E = [tr.resolver(8.0, 0.02, e, V=V)["E0"] for e in (0.2, 0.1, 0.05)]
    p = np.log2((E[0] - E[1]) / (E[1] - E[2]))
    assert 1.8 < p < 2.2, p
    Eext = E[2] + (E[2] - E[1]) / 3
    assert abs(Eext - 1.5) < 1e-5, Eext


def test_mixto():
    t = pares.tabla_richardson(0.1)
    T, r = tr.matriz_T(40.0, 0.02, 0.1, W=tr.W_yukawa(0.0), tabla=t)
    uT = r * np.exp(-r)
    Em, lim = tr.proyeccion_mixta(T, r, uT, -0.5 * uT, 0.1, [1.0, 5.0])
    assert all(abs(x + 0.5) < 1e-12 for x in Em) and abs(lim + 0.5) < 1e-12   # u_T exacta en Coulomb


def test_extremos_wk():
    # V3 (H2 de V2): la aproximacion fuera de la tabla con Wigner-Kirkwood reproduce la tabla en r = 9 a < 2e-8
    # (sin el termino eps^2 V''/12 el error es -eps^2/(6 r^3) = -2.29e-6 con eps = 0.1)
    t = pares.tabla_richardson(0.1)
    k = int(round(9.0 / t.h)) - 1
    for m in (0, 10, 30):
        a, b = t.r[k], t.r[k + m]
        d_wk = abs(t.Ub[k, m] - pares.U_extremos(a, b, 0.1, wk=True))
        d_ex = abs(t.Ub[k, m] - pares.U_extremos(a, b, 0.1, wk=False))
        assert d_wk < 2e-8 and d_wk < d_ex / 10 and (m > 0 or d_ex > 1e-6), (m, d_wk, d_ex)


def test_aviso_pared():
    # V3 (H3 de V2): la pared en R no tiene imagen; con R = 5 (delta = 0.2) resolver debe avisar
    import warnings
    t = pares.tabla_richardson(0.1)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        o = tr.resolver(5.0, 0.02, 0.1, W=tr.W_yukawa(0.2), tabla=t)
        assert any(issubclass(x.category, RuntimeWarning) for x in w), "no aviso con R = 5"
        assert o["sesgo_pared_est"] < -1e-4, o["sesgo_pared_est"]
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        o = tr.resolver(40.0, 0.02, 0.1, W=tr.W_yukawa(0.2), tabla=t)
        assert not w and abs(o["sesgo_pared_est"]) < 1e-12, o["sesgo_pared_est"]


if __name__ == "__main__":
    for f in (test_tabla, test_coulomb, test_yukawa_02, test_sin_UC_oscilador, test_mixto, test_extremos_wk,
              test_aviso_pared):
        f()
        print("pasa:", f.__name__)
    print("todas las pruebas pasan")
