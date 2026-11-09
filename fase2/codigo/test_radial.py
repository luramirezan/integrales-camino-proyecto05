"""test_radial.py -- pruebas automaticas (assert) del modulo radial.py.

Uso:  python3 test_radial.py      (no necesita pytest; tambien corre con pytest si esta instalado)
Cada prueba imprime lo que compara. Si algun assert falla, el script termina con codigo 1
y dice cual. Es determinista (no hay azar).
"""
import sys, os, time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import radial as rd

H = 1 / 40          # malla gruesa; la fina es H/2 (Richardson)


def _chk(nombre, valor, ref, tol):
    d = abs(valor - ref)
    print(f"  {nombre:<34s} = {valor:+.10f}   ref {ref:+.10f}   |dif| = {d:.1e}  (tol {tol:.0e})")
    assert d < tol, f"{nombre}: {valor} vs {ref} (|dif| = {d:.2e} >= {tol:.0e})"


# ----------------------------------------------------------------------------- 1. Coulomb
def test_coulomb():
    print("[1] Coulomb delta=0, R=60")
    o = rd.resolver_rich(rd.V_coulomb(), 60.0, H)
    _chk("E0", o["E0"], -0.5, 1e-8)
    _chk("E1", o["E1"], -0.125, 1e-8)
    _chk("<r>", o["r_med"], 1.5, 1e-7)
    _chk("<r^2>", o["r2_med"], 3.0, 1e-7)
    nrm = o["rgrid"][1] - o["rgrid"][0]
    _chk("norma int u^2 dr (malla fina)", nrm * np.sum(o["u"]**2), 1.0, 1e-12)
    # orden aparente de la discretizacion pese a la singularidad -1/r
    _, p = rd.orden_aparente(rd.V_coulomb(), 60.0, [1 / 20, 1 / 40, 1 / 80, 1 / 160], exacto=-0.5)
    print(f"  orden aparente E0 (h=1/20..1/160): {', '.join(f'{x:.4f}' for x in p)}")
    assert all(abs(x - 2) < 0.01 for x in p)
    # Yukawa en delta=0 coincide con Coulomb
    o2 = rd.resolver_rich(rd.V_yukawa(0.0), 60.0, H)
    _chk("E0 Yukawa(delta=0) - Coulomb", o2["E0"] - o["E0"], 0.0, 1e-14)


# ----------------------------------------------------------------------------- 2. tabla 5.1 de la Fase 1
TABLA_51 = [  # delta, R, N, E0, <r>, |E_h - E_h/2|   (fase1/secciones/05_referencia_numerica.md)
    (0.0, 60, 2400, -0.499999994, 1.50000, 5.9e-5),
    (0.2, 60, 2400, -0.326808505, 1.54972, 5.7e-5),
    (0.4, 60, 2400, -0.198376077, 1.69137, 5.1e-5),
    (0.6, 60, 2400, -0.106135901, 1.96686, 4.3e-5),
    (0.8, 84, 3344, -0.044704298, 2.54916, 3.2e-5),
    (1.0, 174, 6972, -0.010285784, 4.36670, 1.8e-5),
    (1.1, 370, 14795, -0.002287239, 8.27764, 8.8e-6),
]


def caja_51(d):
    """Receta de 05_referencia_numerica.py: E0 previo con R=60, N=8000; R=min(max(60,25/kappa),6000), N=int(40R)."""
    E0 = rd.resolver_rich(rd.V_yukawa(d), 60.0, N=8000, nev=1)["E0"]
    R = min(max(60.0, 25 / np.sqrt(-2 * E0)), 6000.0)
    return R, int(R * 40)


def test_tabla_51():
    print("[2] Tabla 5.1 de la Fase 1 (misma receta de caja y de malla)")
    for d, R0, N0, E0, rm, dE in TABLA_51:
        R, N = caja_51(d)
        o = rd.resolver_rich(rd.V_yukawa(d), R, N=N, nev=1)
        print(f"  delta={d:.1f} R={R:.0f} N={N}: E0={o['E0']:.9f} (tabla {E0:.9f}) <r>={o['r_med']:.5f} "
              f"(tabla {rm:.5f}) |E_h-E_h/2|={o['dE']:.1e} (tabla {dE:.1e})")
        assert round(R) == R0 and N == N0
        assert abs(o["E0"] - E0) <= 5.01e-10, (d, o["E0"], E0)
        assert abs(o["r_med"] - rm) <= 5.01e-6, (d, o["r_med"], rm)
        assert abs(o["dE"] - dE) <= 0.051 * 10**np.floor(np.log10(dE)) + 1e-12, (d, o["dE"], dE)


# ----------------------------------------------------------------------------- 3. delta = 0.2
def test_delta_02():
    print("[3] Punto fuertemente ligado delta=0.2, R=60 (seccion 9.2 de la Fase 1)")
    o = rd.resolver_rich(rd.V_yukawa(0.2), 60.0, H)
    _chk("E0", o["E0"], -0.32680851, 5e-9)
    # V3 (H4 de V1): frente al valor exacto (-0.3268085113692, disparo y FEDVR de V1; Richardson h=1/320 da
    # -0.3268085113851) el error con h=1/40,1/80 es 6.2e-9 > 5e-9. Con h=1/80,1/160 baja a 3.9e-10:
    o80 = rd.resolver_rich(rd.V_yukawa(0.2), 60.0, 1 / 80)
    _chk("E0 (h=1/80,1/160) frente al exacto", o80["E0"], -0.3268085113692, 1e-9)
    _chk("E1 (R=60, como en 9.2)", o["E1"], -0.012108, 5e-7)
    _chk("<r>", o["r_med"], 1.5497, 5e-5)
    _chk("<r^2>^1/2", o["r_rms"], 1.7961, 5e-5)
    _chk("brecha E1-E0", o["E1"] - o["E0"], 0.3147, 5e-5)


# ----------------------------------------------------------------------------- 4. delta_c
def test_delta_c():
    print("[4] Umbral de Yukawa por la condicion de energia cero")
    for R in (200.0, 400.0):
        dc = rd.umbral(rd.V_yukawa, 1.1, 1.3, R=R)
        _chk(f"delta_c (R={R:.0f})", dc, rd.DELTA_C_REF, 1e-8)
    dc2 = rd.umbral(rd.V_yukawa, 0.30, 0.32, R=400.0)
    _chk("delta_c(2s) (R=400; Fase 1: 0.310209)", dc2, 0.310209, 5e-7)


# ----------------------------------------------------------------------------- 5. Hulthen
def test_hulthen():
    print("[5] Hulthen V=-delta/(e^{delta r}-1): E_n=-(1/2)(1/n-n delta/2)^2, <r> analitico (sympy)")
    for d in (0.2, 1.0, 1.5):
        ex = rd.hulthen_exacto(d)
        assert ex["residuo_simbolico"] == "0"
        R = rd.caja_recomendada(ex["E"])
        o = rd.resolver_rich(rd.V_hulthen(d), R, H)
        print(f"  delta={d} (R={R:.0f}); <r> exacto = {ex['r_med_formula']}")
        _chk(f"E0 delta={d}", o["E0"], ex["E"], 1e-8)
        # tolerancia relativa 2e-7: el residuo de Richardson es O(h^4) (en delta=1.5 vale 4e-8 relativo en <r>
        # y 1.7e-7 en <r^2> con h=1/40); se comprueba abajo que baja >8 veces al pasar a h=1/80.
        _chk(f"<r> delta={d}", o["r_med"], ex["r_med"], 2e-7 * ex["r_med"])
        _chk(f"<r^2> delta={d}", o["r2_med"], ex["r2_med"], 2e-7 * ex["r2_med"])
        o80 = rd.resolver_rich(rd.V_hulthen(d), R, H / 2)
        q = [abs(o[k] - ex[k]) / abs(o80[k] - ex[k]) for k in ("r_med", "r2_med")]
        print(f"    error(h=1/40)/error(h=1/80) tras Richardson: <r> {q[0]:.1f}, <r^2> {q[1]:.1f} (O(h^4) -> 16)")
        assert min(q) > 8, q
    ex2 = rd.hulthen_exacto(0.2, n=2)
    R = rd.caja_recomendada(ex2["E"])
    o = rd.resolver_rich(rd.V_hulthen(0.2), R, H)
    _chk(f"E1 (2s) delta=0.2 (R={R:.0f})", o["E1"], ex2["E"], 1e-8)
    _chk("umbral 1s (exacto 2)", rd.umbral(rd.V_hulthen, 1.8, 2.2, R=200.0), 2.0, 1e-8)
    _chk("umbral 2s (exacto 0.5)", rd.umbral(rd.V_hulthen, 0.4, 0.7, R=200.0), 0.5, 1e-8)


# ----------------------------------------------------------------------------- 6. pozo cuadrado
def test_pozo():
    print("[6] Pozo esferico cuadrado a=1: k cot(ka) = -kappa (brentq); umbral V0 a^2 = pi^2/8")
    _chk("umbral V0 (energia cero, R=50)",
         rd.umbral(lambda v: rd.V_pozo(v), 1.0, 1.5, R=50.0, quiebres=(1.0,)), np.pi**2 / 8, 1e-8)
    for V0 in (2.0, 1.3):
        ex = rd.pozo_exacto(V0)
        R = rd.caja_recomendada(ex["E"], entera=True)   # r=a=1 es nodo de todas las mallas
        hs = [1 / 20, 1 / 40, 1 / 80, 1 / 160, 1 / 320]
        _, pe = rd.orden_aparente(rd.V_pozo(V0, borde="estricta"), R, hs, exacto=ex["E"])
        _, pm = rd.orden_aparente(rd.V_pozo(V0, borde="media"), R, hs, exacto=ex["E"])
        print(f"  V0={V0} (R={R:.0f}) E exacta={ex['E']:.12f}")
        print(f"    orden aparente, V(a)=0      : {', '.join(f'{x:.3f}' for x in pe)}")
        print(f"    orden aparente, V(a)=-V0/2  : {', '.join(f'{x:.3f}' for x in pm)}")
        # la discontinuidad con V(a)=0 deja orden 1 (asintotico); con valor medio en el nodo vuelve a 2
        assert abs(pe[-1] - 1) < 0.1, pe
        assert abs(pm[-1] - 2) < 0.05, pm
        om = rd.resolver_rich(rd.V_pozo(V0, borde="media"), R, H, p=2)
        _chk(f"E0 V0={V0} (borde medio, Rich p=2)", om["E0"], ex["E"], 1e-8 if V0 == 2.0 else 2e-8)
        _chk(f"<r> V0={V0} (borde medio, Rich p=2)", om["r_med"], ex["r_med"], 1e-5 if V0 == 2.0 else 1e-4)
        oe = rd.resolver_rich(rd.V_pozo(V0, borde="estricta"), R, H, p=1)
        print(f"    V(a)=0 con Richardson p=1: |E-E_ex| = {abs(oe['E0'] - ex['E']):.1e}; con p=2: "
              f"{abs(rd.resolver_rich(rd.V_pozo(V0, borde='estricta'), R, H, p=2)['E0'] - ex['E']):.1e}")


# ----------------------------------------------------------------------------- 7. tabla 9.6
TABLA_96 = {  # delta: [(R, E0 Rich, <r>/R, F_1/2)]  (fase1/secciones/09_plan_computo.md, h=1/80 para <r>/R y F)
    1.15: [(50, -3.31e-4, .239, .895), (100, -4.51e-4, .164, .962), (200, -4.56e-4, .087, .998),
           (400, -4.56e-4, .044, 1.000), (800, -4.56e-4, .022, 1.000)],
    1.18: [(50, 3.38e-4, .293, .832), (100, 3.21e-5, .268, .859), (200, -2.41e-5, .225, .904),
           (400, -3.08e-5, .153, .967), (800, -3.10e-5, .081, .998)],
    1.20: [(50, 6.44e-4, .324, .790), (100, 1.87e-4, .331, .776), (200, 5.80e-5, .352, .746),
           (400, 1.84e-5, .386, .695), (800, 5.67e-6, .426, .633)],
}


# Fe de erratas encontrada al correr esta prueba: en (delta=1.18, R=400) la tabla 9.6 dice -3.08e-5, pero el
# propio codigo de la Fase 1 (09_prueba_costos.py, funcion radial, h=1/40 y 1/80) da -3.0746e-5, que redondea a
# -3.07e-5. Es un error de redondeo del documento, no del codigo. La prueba usa el valor corregido y lo avisa.
ERRATAS_96 = {(1.18, 400): -3.07e-5}


def test_tabla_96():
    print("[7] Tabla 9.6 de la Fase 1 (cajas cerca del umbral)")
    for d, filas in TABLA_96.items():
        for R, E0, rR, F in filas:
            if (d, R) in ERRATAS_96:
                print(f"  AVISO errata 9.6: delta={d} R={R}: la tabla dice {E0:+.2e}; se compara con "
                      f"{ERRATAS_96[(d, R)]:+.2e}")
                E0 = ERRATAS_96[(d, R)]
            o = rd.resolver_rich(rd.V_yukawa(d), float(R), H, nev=1)
            print(f"  delta={d} R={R}: E0={o['E0']:+.3e} (tabla {E0:+.2e})  <r>/R(h=1/80)={o['r_sobre_R_h2']:.3f} "
                  f"(tabla {rR:.3f})  F(h=1/80)={o['F12_h2']:.3f} (tabla {F:.3f})")
            # la tabla da 3 cifras significativas: media unidad de la tercera cifra
            assert abs(o["E0"] - E0) <= 0.501e-2 * 10**np.floor(np.log10(abs(E0))), (d, R, o["E0"], E0)
            assert abs(o["r_sobre_R_h2"] - rR) <= 5.01e-4, (d, R, o["r_sobre_R_h2"], rR)
            assert abs(o["F12_h2"] - F) <= 1.01e-3, (d, R, o["F12_h2"], F)


PRUEBAS = [test_coulomb, test_tabla_51, test_delta_02, test_delta_c, test_hulthen, test_pozo, test_tabla_96]

if __name__ == "__main__":
    fallos = []
    t0 = time.perf_counter()
    for f in PRUEBAS:
        t = time.perf_counter()
        try:
            f()
            print(f"  -> PASA ({time.perf_counter() - t:.1f} s)\n")
        except AssertionError as e:
            fallos.append((f.__name__, str(e)))
            print(f"  -> FALLA: {e}\n")
    print(f"Resumen: {len(PRUEBAS) - len(fallos)}/{len(PRUEBAS)} pruebas pasan "
          f"({time.perf_counter() - t0:.1f} s en total)")
    for n, e in fallos:
        print(f"  FALLA {n}: {e}")
    sys.exit(1 if fallos else 0)
