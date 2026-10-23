"""Genera todas las figuras de circuitos (PNG + SVG) en ../figuras/.

Uso:  python3 src/circuitos.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from simbolos import Diagram, GROUP, PILOT, INK  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "figuras")
os.makedirs(OUT, exist_ok=True)


def out(name):
    return os.path.join(OUT, name)


def pil(d, pts):
    d.line(pts, pilot=True)


# =========================================================== símbolos sueltos
def simbolos():
    d = Diagram(6.6, 2.6, -0.8, -0.3)
    d.cylinder(0.5, 0.4, "", L=3.4, marks=None)
    d.save(out("sym_cil_de"))

    d = Diagram(6.6, 2.6, -0.8, -0.3)
    d.cylinder(0.5, 0.4, "", L=3.4, single=True, marks=None)
    d.save(out("sym_cil_se"))

    specs = [
        ("sym_32_boton", "3/2", "button", "spring", 1),
        ("sym_32_rodillo", "3/2", "roller", "spring", 1),
        ("sym_32_rodillo_esc", "3/2", "roller1", "spring", 1),
        ("sym_32_pilot", "3/2", "pilot", "spring", 1),
        ("sym_52_boton", "5/2", "button", "spring", 1),
        ("sym_52_pilot_resorte", "5/2", "pilot", "spring", 1),
        ("sym_52_biestable", "5/2", "pilot", "pilot", 1),
        ("sym_42_biestable", "4/2", "pilot", "pilot", 1),
        ("sym_32_pedal", "3/2", "pedal", "spring", 1),
        ("sym_32_rodillo_accionado", "3/2", "roller", "spring", 0),
    ]
    for name, kind, l, r, pos in specs:
        d = Diagram(4.4, 2.6, -1.1, -0.95)
        d.valve(0, 0.25, kind, left=l, right=r, pos=pos)
        d.save(out(name))

    d = Diagram(2.6, 1.6, -1.3, -0.6)
    d.logic(0, 0, "or")
    d.save(out("sym_or"))
    d = Diagram(2.6, 1.6, -1.3, -0.6)
    d.logic(0, 0, "and")
    d.save(out("sym_and"))

    d = Diagram(2.0, 2.0, -1.0, -0.2)
    d.flow_ctrl(0, 0)
    d.save(out("sym_reguladora"))

    d = Diagram(4.2, 1.6, -0.5, -0.8)
    d.service_unit(0, 0)
    d.save(out("sym_unidad"))

    d = Diagram(1.4, 1.0, -0.7, -0.75)
    d.seg((0, 0.15), (0, 0))
    d.source((0, 0))
    d.save(out("sym_fuente"))

    d = Diagram(1.4, 1.0, -0.7, -0.6)
    d.seg((0, 0.3), (0, 0))
    d.exhaust((0, 0))
    d.save(out("sym_escape"))

    # tipos de línea
    d = Diagram(9.0, 5.0, -0.2, -0.3)
    rows = [("Línea de trabajo (potencia)", dict()), ("Línea de pilotaje / señal", dict(pilot=True)),
            ("Línea de grupo (cascada)", dict(color=GROUP[0], lw=2.2))]
    for k, (lab, kw) in enumerate(rows):
        y = 4.2 - k * 1.0
        d.line([(0.2, y), (3.2, y)], **kw)
        d.text((3.6, y), lab, fs=10, ha="left")
    y = 1.2
    d.line([(0.2, y), (3.2, y)])
    d.line([(1.7, y), (1.7, y + 0.5)])
    d.dot((1.7, y))
    d.text((3.6, y), "Unión (con punto)", fs=10, ha="left")
    y = 0.2
    d.line([(0.2, y), (3.2, y)])
    d.line([(1.7, y - 0.3), (1.7, y + 0.4)])
    d.text((3.6, y), "Cruce sin unión (sin punto)", fs=10, ha="left")
    d.save(out("sym_lineas"))

    # marcas de final de carrera sobre el cilindro
    d = Diagram(8.4, 3.4, -0.9, -0.6)
    d.cylinder(0.3, 0.2, "A", L=3.4)
    d.save(out("sym_marcas"))

    # accionamientos
    for k in ["button", "lever", "pedal", "roller", "roller1", "spring", "pilot"]:
        d = Diagram(2.2, 1.6, -0.3, -0.3)
        d.ax.add_patch(__import__("matplotlib").patches.Rectangle((1.2, 0), 0.7, 1.0, fill=False, ec=INK, lw=1.5))
        d.actuator(k, 1.2, 0.5, -1)
        d.save(out("act_" + k))


# ============================================================ teoría
def anatomia_valvula():
    d = Diagram(18.4, 7.2, -4.4, -2.6)
    d.valve(1.5, 1.0, "5/2", left="pilot", right="spring", pos=1)
    fs = 9
    d.text((2.0, 2.55), "a", fs=11, color=PILOT, weight="bold")
    d.text((2.45, 2.55), "b", fs=11, color=PILOT, weight="bold")
    d.text((-4.1, 1.5), "a = posición accionada (piloto 14)\nb = posición de reposo (resorte)", fs=fs,
           ha="left", color=PILOT, va="center")
    d.text((7.6, 3.6), "2, 4  →  utilización (van al cilindro)", fs=fs, ha="left")
    d.seg((3.3, 2.5), (7.4, 3.6), color="#888", lw=0.8)
    d.text((7.6, 0.4), "1  →  alimentación (presión)\n3, 5  →  escape a la atmósfera", fs=fs, ha="left")
    d.seg((3.2, 0.2), (7.4, 0.4), color="#888", lw=0.8)
    d.text((7.6, -1.6), "Resorte: retorno a la posición de reposo\n(válvula monoestable)", fs=fs, ha="left")
    d.seg((4.2, 1.4), (7.4, -1.4), color="#888", lw=0.8)
    d.text((-4.1, 3.6), "Piloto 14: con señal conecta 1 → 4", fs=fs, ha="left")
    d.seg((-0.4, 3.4), (0.9, 1.65), color="#888", lw=0.8)
    d.text((-4.1, -1.7), "Los puertos se dibujan SOLO\nen el cuadro de reposo", fs=fs, ha="left",
           color="#c0392b")
    d.seg((0.5, -1.45), (2.6, -0.1), color="#c0392b", lw=0.8)
    d.save(out("anatomia_valvula"))


def mando_directo_se():
    d = Diagram(8, 6.4, -0.5, -0.5)
    c = d.cylinder(1.5, 4.0, "A", L=3.4, single=True, marks=None)
    v = d.valve(0.5, 1.0, "3/2", left="button", label="S1")
    d.line([v["2"], c["A"]])
    d.save(out("t_mando_directo_se"))


def mando_directo_de():
    d = Diagram(9, 6.6, -0.5, -0.5)
    c = d.cylinder(1.5, 4.2, "A", L=3.4, marks=None)
    v = d.valve(1.9, 1.0, "5/2", left="button", label="S1")
    d.line([v["4"], (v["4"][0], 3.2), (c["A"][0], 3.2), c["A"]])
    d.line([v["2"], (v["2"][0], 3.2), (c["B"][0], 3.2), c["B"]])
    d.save(out("t_mando_directo_de"))


def _cyl_valve(d, cx, cy, vy, name, valve="5/2", right="pilot", left="pilot",
               flows=None, L=3.4, marks=("0", "1"), vlabel=None, route_y=None):
    """Columna estándar: cilindro + (reguladoras) + válvula de potencia.
    flows: dict {'A': 'up'|'down', 'B': ...} con reguladoras en esas líneas."""
    c = d.cylinder(cx, cy, name, L=L, marks=marks)
    vx = cx + 0.4
    v = d.valve(vx, vy, valve, left=left, right=right, label=vlabel or "V" + name,
                label_side="below")
    flows = flows or {}
    fy = cy - 0.3 - 1.6  # y inferior de reguladora
    ends = {}
    for p in ("A", "B"):
        if p in flows:
            f = d.flow_ctrl(c[p][0], fy, free=flows[p], label="R" + name + ("1" if p == "A" else "2"),
                            label_side="left" if p == "A" else "right")
            d.line([f["top"], c[p]])
            ends[p] = f["bot"]
        else:
            ends[p] = c[p]
    ry = route_y if route_y is not None else vy + 1.3 + 0.6
    d.line([v["4"], (v["4"][0], ry), (ends["A"][0], ry), ends["A"]])
    d.line([v["2"], (v["2"][0], ry), (ends["B"][0], ry), ends["B"]])
    return c, v


def mando_indirecto_memoria():
    d = Diagram(11, 9.8, -1.0, -2.4)
    c, v = _cyl_valve(d, 2.5, 5.6, 2.8, "A", marks=None)
    s1 = d.valve(-0.2, -0.4, "3/2", left="button", label="S1 (A+)", label_side="below")
    s2 = d.valve(5.8, -0.4, "3/2", left="button", label="S2 (A−)", label_side="below")
    pil(d, [s1["2"], (s1["2"][0], v["14"][1]), v["14"]])
    pil(d, [s2["2"], (s2["2"][0], v["12"][1]), v["12"]])
    d.save(out("t_mando_indirecto_memoria"))


def regulacion_velocidad():
    d = Diagram(21, 9.4, -0.6, -1.4)
    for k, (x0, free, ttl) in enumerate([(0.6, "down", "Estrangulación a la ENTRADA (meter-in)"),
                                        (11.0, "up", "Estrangulación a la SALIDA (meter-out)  ✔")]):
        c = d.cylinder(x0 + 1.2, 5.6, "A", L=3.4, marks=None)
        f1 = d.flow_ctrl(c["A"][0], 3.7, free=free)
        f2 = d.flow_ctrl(c["B"][0], 3.7, free=free)
        d.line([f1["top"], c["A"]])
        d.line([f2["top"], c["B"]])
        v = d.valve(x0 + 1.6, 0.6, "5/2", left="button")
        d.line([v["4"], (v["4"][0], 3.0), (f1["bot"][0], 3.0), f1["bot"]])
        d.line([v["2"], (v["2"][0], 3.0), (f2["bot"][0], 3.0), f2["bot"]])
        d.text((x0 + 4.0, 7.6), ttl, fs=10, weight="bold",
               color="#c0392b" if free == "down" else "#0b7a53")
    d.save(out("t_regulacion_velocidad"))


def logica(kind):
    d = Diagram(12.6, 11.4, -1.6, -2.4)
    c, v = _cyl_valve(d, 2.8, 7.2, 4.2, "A", right="spring", marks=None)
    g = d.logic(v["14"][0] - 0.3, 1.9, kind,
                label="válvula selectora (O)" if kind == "or" else "válvula de simultaneidad (Y)")
    pil(d, [g["out"], (g["out"][0], v["14"][1]), v["14"]])
    s1 = d.valve(-0.6, -0.5, "3/2", left="button", label="S1", label_side="below")
    s2 = d.valve(4.4, -0.5, "3/2", left="button", label="S2", label_side="below")
    pil(d, [s1["2"], (s1["2"][0], g["l"][1]), g["l"]])
    pil(d, [s2["2"], (s2["2"][0], g["r"][1]), g["r"]])
    d.save(out("t_logica_" + kind))


def semiautomatico():
    d = Diagram(13, 10.0, -1.0, -2.4)
    c, v = _cyl_valve(d, 2.5, 5.6, 2.8, "A", marks=(None, "1"))
    s1 = d.valve(-0.2, -0.4, "3/2", left="button", label="S1", label_side="below")
    a1 = d.valve(7.0, -0.4, "3/2", left="roller", lim="a1")
    pil(d, [s1["2"], (s1["2"][0], v["14"][1]), v["14"]])
    pil(d, [a1["2"], (a1["2"][0], v["12"][1]), v["12"]])
    d.save(out("t_semiautomatico"))


def secuencia_abab():
    """A+ B+ A- B- sin cascada (no hay señales bloqueadas)."""
    d = Diagram(21, 13.4, -1.0, -1.8)
    cA, vA = _cyl_valve(d, 2.5, 8.6, 5.8, "A")
    cB, vB = _cyl_valve(d, 12.0, 8.6, 5.8, "B")
    sy = 0.4
    b0 = d.valve(1.0, sy, "3/2", left="roller", lim="b0", pos=0)
    s = d.valve(0.0, sy + 2.0, "3/2", left="button", supply=False, label="S", label_side="top")
    b1 = d.valve(5.0, sy, "3/2", left="roller", lim="b1")
    a1 = d.valve(9.0, sy, "3/2", left="roller", lim="a1")
    a0 = d.valve(15.2, sy, "3/2", left="roller", lim="a0", pos=0)
    pil(d, [b0["2"], s["1"]])
    pil(d, [s["2"], (s["2"][0], vA["14"][1]), vA["14"]])
    pil(d, [b1["2"], (b1["2"][0], vA["12"][1]), vA["12"]])
    pil(d, [a1["2"], (a1["2"][0], vB["14"][1]), vB["14"]])
    pil(d, [a0["2"], (a0["2"][0], vB["12"][1]), vB["12"]])
    d.save(out("t_secuencia_ABAB"))


def cascada_abba():
    """A+ B+ / B- A-  con cascada de 2 grupos."""
    d = Diagram(23.5, 17.6, -0.4, -0.4)
    yL1, yL2 = 4.8, 4.0
    cA, vA = _cyl_valve(d, 5.5, 14.2, 10.8, "A")
    cB, vB = _cyl_valve(d, 13.5, 14.2, 10.8, "B")
    vg = d.valve(1.6, 1.0, "5/2", left="pilot", right="pilot", label="VG\n(selectora de grupo)",
                 label_side="below")
    sy = 6.2
    a0 = d.valve(2.2, sy, "3/2", left="roller", lim="a0", pos=0, supply=False)
    s = d.valve(1.2, sy + 2.0, "3/2", left="button", supply=False, label="S", label_side="above")
    b0 = d.valve(6.5, sy, "3/2", left="roller", lim="b0", pos=0, supply=False)
    a1 = d.valve(10.3, sy, "3/2", left="roller", lim="a1", supply=False)
    b1 = d.valve(18.0, sy, "3/2", left="roller", lim="b1", supply=False)
    g1, g2 = GROUP[0], GROUP[1]
    # líneas de grupo
    d.line([(vg["4"][0], vg["4"][1]), (vg["4"][0], yL1)], color=g1, lw=2.2)
    d.line([(vg["2"][0], vg["2"][1]), (vg["2"][0], yL2)], color=g2, lw=2.2)
    d.line([(vg["4"][0], yL1), (19.3, yL1)], color=g1, lw=2.2)
    d.line([(a0["1"][0], yL2), (16.9, yL2)], color=g2, lw=2.2)
    d.text((12.6, yL1 + 0.4), "Línea I  (A+ B+)", fs=9, ha="left", color=g1, weight="bold")
    d.text((12.6, yL2 - 0.4), "Línea II (B− A−)", fs=9, ha="left", color=g2, weight="bold")
    # alimentación de válvulas de señal desde las líneas
    for v, y, col in ((a0, yL2, g2), (b0, yL2, g2), (a1, yL1, g1), (b1, yL1, g1)):
        d.line([v["1"], (v["1"][0], y)], color=col, lw=1.6)
        d.dot((v["1"][0], y), color=col)
    d.dot((vg["2"][0], yL2), color=g2)
    d.dot((vg["4"][0], yL1), color=g1)
    # serie a0 -> S
    pil(d, [a0["2"], s["1"]])
    # señales
    pil(d, [s["2"], (s["2"][0], 9.9), (0.2, 9.9), (0.2, vg["14"][1]), vg["14"]])
    d.line([(vA["14"][0], yL1), (vA["14"][0], vA["14"][1])], pilot=True, color=g1)
    d.dot((vA["14"][0], yL1), color=g1)
    pil(d, [b0["2"], (b0["2"][0], 9.0), (vA["12"][0] + 0.5, 9.0), (vA["12"][0] + 0.5, vA["12"][1]),
            vA["12"]])
    pil(d, [a1["2"], (a1["2"][0], vB["14"][1]), vB["14"]])
    d.line([(16.9, yL2), (16.9, vB["12"][1]), vB["12"]], pilot=True, color=g2)
    d.dot((16.9, yL2), color=g2)
    pil(d, [b1["2"], (b1["2"][0], 7.9), (21.3, 7.9), (21.3, vg["12"][1]), vg["12"]])
    d.save(out("t_cascada_ABBA"))


# ============================================================ enunciados
def e1_1_puerta():
    d = Diagram(12.2, 16.4, -1.0, -2.2)
    c = d.cylinder(3.0, 12.0, "A", L=3.4)
    d.text((5.0, 13.85), "(puerta)", fs=8, color="#555")
    f = d.flow_ctrl(c["A"][0], 10.1, free="up", label="R1\ncierre lento", label_side="left")
    d.line([f["top"], c["A"]])
    v = d.valve(3.4, 7.0, "5/2", left="pilot", right="pilot", label="VA", label_side="below")
    d.line([v["4"], (v["4"][0], 9.4), (f["bot"][0], 9.4), f["bot"]])
    d.line([v["2"], (v["2"][0], 9.4), (c["B"][0], 9.4), c["B"]])
    a0 = d.valve(1.6, 4.4, "3/2", left="roller", lim="a0", pos=0, supply=False)
    a1 = d.valve(6.4, 4.4, "3/2", left="roller", lim="a1", supply=False)
    g = d.logic(5.0, 2.6, "or")
    s1 = d.valve(0.4, 0.2, "3/2", left="button", label="S1 interior", label_side="below")
    s2 = d.valve(7.2, 0.2, "3/2", left="button", label="S2 exterior", label_side="below")
    pil(d, [s1["2"], (s1["2"][0], g["l"][1]), g["l"]])
    pil(d, [s2["2"], (s2["2"][0], g["r"][1]), g["r"]])
    pil(d, [g["out"], (g["out"][0], 3.6)])
    pil(d, [(a0["1"][0], 3.6), (a1["1"][0], 3.6)])
    pil(d, [(a0["1"][0], 3.6), a0["1"]])
    pil(d, [(a1["1"][0], 3.6), a1["1"]])
    d.dot((g["out"][0], 3.6), pilot=True)
    pil(d, [a0["2"], (a0["2"][0], v["14"][1]), v["14"]])
    pil(d, [a1["2"], (a1["2"][0], v["12"][1]), v["12"]])
    d.save(out("e1_1_puerta_conmutada"))


def e1_1_puerta_botonera():
    d = Diagram(15.2, 16.4, -2.4, -2.6)
    c = d.cylinder(3.0, 12.0, "A", L=3.4, marks=None)
    d.text((5.0, 13.4), "(puerta)", fs=8, color="#555")
    f = d.flow_ctrl(c["A"][0], 10.1, free="up", label="R1\ncierre lento", label_side="left")
    d.line([f["top"], c["A"]])
    v = d.valve(3.4, 7.0, "5/2", left="pilot", right="pilot", label="VA", label_side="below")
    d.line([v["4"], (v["4"][0], 9.4), (f["bot"][0], 9.4), f["bot"]])
    d.line([v["2"], (v["2"][0], 9.4), (c["B"][0], 9.4), c["B"]])
    o1 = d.logic(2.0, 3.2, "or")
    o2 = d.logic(8.6, 3.2, "or")
    pil(d, [o1["out"], (o1["out"][0], v["14"][1]), v["14"]])
    pil(d, [o2["out"], (o2["out"][0], v["12"][1]), v["12"]])
    xs = [-1.4, 2.4, 5.6, 9.2]
    labels = ["S1 abrir\n(interior)", "S2 abrir\n(exterior)", "S3 cerrar\n(interior)", "S4 cerrar\n(exterior)"]
    targets = [o1["l"], o1["r"], o2["l"], o2["r"]]
    for x, lab, t in zip(xs, labels, targets):
        s = d.valve(x, 0.2, "3/2", left="button", label=lab, label_side="below")
        pil(d, [s["2"], (s["2"][0], t[1]), t])
    d.save(out("e1_1_puerta_botonera"))


def e1_2_cuchara():
    d = Diagram(13, 13.4, -0.4, -1.6)
    c = d.cylinder(3, 9, "A", L=4.0, marks=(None, "1"))
    d.text((5.0, 10.75), "(cuchara)", fs=8, color="#555")
    f1 = d.flow_ctrl(3.3, 7.1, label="R1", label_side="left")
    f2 = d.flow_ctrl(6.7, 7.1, label="R2")
    v = d.valve(4, 4.5, "4/2", left="pilot", right="pilot", label="VA", label_side="below")
    d.line([v["4"], (v["4"][0], 6.4), (3.3, 6.4), f1["bot"]])
    d.line([v["2"], (v["2"][0], 6.4), (6.7, 6.4), f2["bot"]])
    s = d.valve(0.8, 1.0, "3/2", left="button", label="S1", label_side="below")
    a = d.valve(8.4, 1.0, "3/2", left="roller", lim="a1")
    pil(d, [s["2"], (s["2"][0], v["14"][1]), v["14"]])
    pil(d, [a["2"], (a["2"][0], v["12"][1]), v["12"]])
    d.save(out("e1_2_cuchara"))


# ---------------------------------------------------------------- cascada
def _feed(d, v, y, col):
    """Alimenta el puerto 1 de una válvula de señal desde una línea de grupo."""
    d.line([v["1"], (v["1"][0], y)], color=col, lw=1.6)
    d.dot((v["1"][0], y), color=col)


def _direct(d, x, y_line, pilot, col):
    """Señal directa desde una línea de grupo hasta un pilotaje."""
    d.line([(x, y_line), (x, pilot[1]), pilot], pilot=True, color=col)
    d.dot((x, y_line), color=col)


def _group_lines(d, vg, specs):
    """specs: lista de (puerto_VG, y, x_ini, x_fin, color, texto, (x_txt, y_txt))."""
    for port, y, x0, x1, col, txt, tp in specs:
        d.line([vg[port], (vg[port][0], y)], color=col, lw=2.2)
        d.line([(x0, y), (x1, y)], color=col, lw=2.2)
        d.dot((vg[port][0], y), color=col)
        d.text(tp, txt, fs=9, ha="left", color=col, weight="bold")


def e2_1_estampado():
    """A+ B+ (A- B-) C+ C-  — 2 grupos: I = {C-, A+, B+}, II = {A-, B-, C+}.
    Reposo: grupo I activo (línea I = salida 2 de VG)."""
    d = Diagram(29.6, 18.3, -1.0, -1.7)
    g1, g2 = GROUP[:2]
    yI, yII = 3.2, 4.0
    L = 3.0
    cA, vA = _cyl_valve(d, 5.8, 13.8, 11.4, "A", L=L)
    cB, vB = _cyl_valve(d, 13.0, 13.8, 11.4, "B", L=L)
    cC, vC = _cyl_valve(d, 20.2, 13.8, 11.4, "C", L=L)
    vg = d.valve(1.0, 0.2, "5/2", left="pilot", right="pilot", label="VG", label_side="below")
    sy = 5.6
    c0 = d.valve(1.4, sy, "3/2", left="roller", lim="c0", pos=0, supply=False)
    s = d.valve(0.4, sy + 2.0, "3/2", left="button", supply=False, label="S", label_side="top")
    c1 = d.valve(5.2, sy, "3/2", left="roller", lim="c1", supply=False)
    a1 = d.valve(9.9, sy, "3/2", left="roller", lim="a1", supply=False)
    a0 = d.valve(17.1, sy, "3/2", left="roller", lim="a0", pos=0, supply=False)
    b0 = d.valve(17.1, sy + 2.0, "3/2", left="roller", lim="b0", pos=0, supply=False)
    b1 = d.valve(24.5, sy, "3/2", left="roller", lim="b1", supply=False)
    _group_lines(d, vg, [
        ("2", yI, 1.7, b1["1"][0], g1, "Línea I  (C− A+ B+)", (12.0, yI - 0.42)),
        ("4", yII, vg["4"][0], vC["12"][0] + 0.45 - 7.2, g2, "Línea II (A− B− C+)", (12.0, yII + 0.42)),
    ])
    # línea II llega hasta a0 y el carril de VB12
    d.line([(vB["12"][0] + 0.45, yII), (a0["1"][0], yII)], color=g2, lw=2.2)
    for v in (c0, a1, b1):
        _feed(d, v, yI, g1)
    for v in (c1, a0):
        _feed(d, v, yII, g2)
    pil(d, [c0["2"], s["1"]])
    pil(d, [a0["2"], b0["1"]])
    _direct(d, vC["12"][0] + 0.45, yI, vC["12"], g1)
    _direct(d, vA["12"][0] + 0.45, yII, vA["12"], g2)
    _direct(d, vB["12"][0] + 0.45, yII, vB["12"], g2)
    pil(d, [s["2"], (s["2"][0], vA["14"][1]), vA["14"]])
    pil(d, [a1["2"], (a1["2"][0], vB["14"][1]), vB["14"]])
    pil(d, [b0["2"], (b0["2"][0], vC["14"][1]), vC["14"]])
    pil(d, [c1["2"], (c1["2"][0], 7.55), (8.6, 7.55), (8.6, vg["12"][1]), vg["12"]])
    pil(d, [b1["2"], (b1["2"][0], 7.6), (27.9, 7.6), (27.9, -1.4), (-0.6, -1.4), (-0.6, vg["14"][1]),
            vg["14"]])
    d.save(out("e2_1_estampado_ABC"))


def e2_2_doblado():
    """A+ B+ C+ (A- B- C-) — 2 grupos. Reposo: grupo II (línea II = salida 2)."""
    d = Diagram(30.0, 19.2, -0.9, -0.9)
    g1, g2 = GROUP[:2]
    yI, yII = 4.0, 3.2
    L = 3.0
    fl = {"B": "up"}
    cA, vA = _cyl_valve(d, 5.8, 15.6, 11.4, "A", L=L, flows=fl)
    cB, vB = _cyl_valve(d, 13.4, 15.6, 11.4, "B", L=L, flows=fl)
    cC, vC = _cyl_valve(d, 21.0, 15.6, 11.4, "C", L=L, flows=fl)
    vg = d.valve(1.0, 0.2, "5/2", left="pilot", right="pilot", label="VG", label_side="below")
    sy = 5.6
    a0 = d.valve(1.2, sy, "3/2", left="roller", lim="a0", pos=0, supply=False)
    b0 = d.valve(1.2, sy + 2.0, "3/2", left="roller", lim="b0", pos=0, supply=False)
    c0 = d.valve(6.0, sy, "3/2", left="roller", lim="c0", pos=0, supply=False)
    s = d.valve(5.0, sy + 2.0, "3/2", left="button", supply=False, label="S", label_side="top")
    lane = lambda v: v["12"][0] + 0.45  # noqa: E731
    a1 = d.valve(lane(vA) + 0.8, sy, "3/2", left="roller", lim="a1", supply=False)
    b1 = d.valve(lane(vB) + 0.8, sy, "3/2", left="roller", lim="b1", supply=False)
    c1 = d.valve(lane(vC) + 0.8, sy, "3/2", left="roller", lim="c1", supply=False)
    _group_lines(d, vg, [
        ("4", yI, -0.2, c1["1"][0], g1, "Línea I  (A+ B+ C+)", (14.6, yI + 0.42)),
        ("2", yII, a0["1"][0], lane(vC), g2, "Línea II (A− B− C−)", (14.6, yII - 0.42)),
    ])
    _feed(d, a0, yII, g2)
    for v in (a1, b1, c1):
        _feed(d, v, yI, g1)
    pil(d, [a0["2"], b0["1"]])
    pil(d, [c0["2"], s["1"]])
    pil(d, [b0["2"], (b0["2"][0], 9.25), (4.3, 9.25), (4.3, 4.65), (c0["1"][0], 4.65), c0["1"]])
    pil(d, [s["2"], (s["2"][0], 9.65), (0.2, 9.65), (0.2, vg["14"][1]), vg["14"]])
    d.line([(-0.2, yI), (-0.2, vA["14"][1]), vA["14"]], pilot=True, color=g1)
    d.dot((-0.2, yI), color=g1)
    for vv in (vA, vB, vC):
        _direct(d, lane(vv), yII, vv["12"], g2)
    pil(d, [a1["2"], (a1["2"][0], vB["14"][1]), vB["14"]])
    pil(d, [b1["2"], (b1["2"][0], vC["14"][1]), vC["14"]])
    pil(d, [c1["2"], (c1["2"][0], 7.6), (c1["2"][0] + 1.9, 7.6), (c1["2"][0] + 1.9, vg["12"][1]),
            vg["12"]])
    d.save(out("e2_2_doblado"))


def e2_3_prensa():
    """(A+ B+) A- B-  — 2 grupos. A = plataforma 3, B = plataforma 4. Reposo: grupo II."""
    d = Diagram(27.4, 19.2, -2.4, -0.9)
    g1, g2 = GROUP[:2]
    yI, yII = 4.0, 3.2
    L = 3.0
    fl = {"B": "up"}
    cA, vA = _cyl_valve(d, 5.8, 15.6, 11.4, "A", L=L, flows=fl)
    cB, vB = _cyl_valve(d, 13.0, 15.6, 11.4, "B", L=L, flows=fl)
    d.text((7.3, 17.25), "(plataforma 3)", fs=8, color="#555")
    d.text((14.5, 17.25), "(plataforma 4)", fs=8, color="#555")
    vg = d.valve(1.0, 0.2, "5/2", left="pilot", right="pilot", label="VG", label_side="below")
    sy = 5.6
    p = d.valve(-0.7, sy, "3/2", left="pedal", supply=False, label="P", label_side="top")
    s = d.valve(2.9, sy, "3/2", left="button", supply=False, label="S", label_side="top")
    g = d.logic(2.4, sy + 1.85, "or")
    b0 = d.valve(2.1, sy + 3.0, "3/2", left="roller", lim="b0", pos=0, supply=False)
    a0 = d.valve(16.8, sy, "3/2", left="roller", lim="a0", pos=0, supply=False)
    a1 = d.valve(20.6, sy, "3/2", left="roller", lim="a1", supply=False)
    b1 = d.valve(20.6, sy + 2.0, "3/2", left="roller", lim="b1", supply=False)
    _group_lines(d, vg, [
        ("4", yI, vg["4"][0], a1["1"][0], g1, "Línea I  (A+ B+)", (9.5, yI + 0.42)),
        ("2", yII, p["1"][0], a0["1"][0], g2, "Línea II (A− B−)", (9.5, yII - 0.42)),
    ])
    for v in (p, s, a0):
        _feed(d, v, yII, g2)
    _feed(d, a1, yI, g1)
    pil(d, [p["2"], (p["2"][0], g["l"][1]), g["l"]])
    pil(d, [s["2"], (s["2"][0], g["r"][1]), g["r"]])
    pil(d, [g["out"], b0["1"]])
    pil(d, [b0["2"], (b0["2"][0], 10.2), (-1.9, 10.2), (-1.9, vg["14"][1]), vg["14"]])
    pil(d, [a1["2"], b1["1"]])
    pil(d, [b1["2"], (b1["2"][0], 9.9), (24.1, 9.9), (24.1, vg["12"][1]), vg["12"]])
    for vv in (vA, vB):
        _direct(d, vv["14"][0], yI, vv["14"], g1)
    _direct(d, vA["12"][0] + 0.45, yII, vA["12"], g2)
    pil(d, [a0["2"], (a0["2"][0], vB["12"][1]), vB["12"]])
    d.save(out("e2_3_prensa"))


def e2_1_selectores():
    d = Diagram(25, 7.8, -0.6, -1.9)
    for k, n in enumerate("DEF"):
        x0 = k * 8.4
        c = d.cylinder(x0 + 1.6, 3.6, n, L=3.4, marks=None)
        v = d.valve(x0 + 2.0, 0.6, "5/2", left="button", label="S" + n, label_side="below")
        d.line([v["4"], (v["4"][0], 2.5), (c["A"][0], 2.5), c["A"]])
        d.line([v["2"], (v["2"][0], 2.5), (c["B"][0], 2.5), c["B"]])
        d.text((x0 + 3.6, 5.1), "Selector %d" % (k + 1), fs=9, color="#555")
    d.save(out("e2_1_selectores_DEF"))


if __name__ == "__main__":
    simbolos()
    anatomia_valvula()
    mando_directo_se()
    mando_directo_de()
    mando_indirecto_memoria()
    regulacion_velocidad()
    logica("or")
    logica("and")
    semiautomatico()
    secuencia_abab()
    cascada_abba()
    e1_1_puerta()
    e1_1_puerta_botonera()
    e1_2_cuchara()
    e2_1_estampado()
    e2_1_selectores()
    e2_2_doblado()
    e2_3_prensa()
    print("ok")
