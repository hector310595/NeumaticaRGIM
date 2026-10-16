"""Mini-librería para dibujar esquemas neumáticos con símbolos ISO 1219 simplificados.

Convenciones (las mismas que se piden a los alumnos en FluidSim):
  * Esquema "por niveles": cilindros arriba, válvulas de potencia al medio,
    elementos de señal (pulsadores, rodillos, lógica) abajo.
  * Todo se dibuja en posición inicial (reposo, cilindros retraídos).
  * Líneas de trabajo continuas; líneas de pilotaje (señal) discontinuas.
  * Cada puerto 1 lleva su símbolo de fuente de aire (como en FluidSim),
    en lugar de dibujar toda la red de alimentación.

Unidad de dibujo: 1 u = lado de un cuadro de válvula.
"""
import matplotlib

matplotlib.use("Agg")
matplotlib.rcParams["svg.hashsalt"] = "rgim-neumatica"
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Arc, Circle, Polygon, Rectangle  # noqa: E402

INK = "#1a1a1a"
PILOT = "#1f4e9c"      # color de líneas de señal / pilotaje
ACCENT = "#c0392b"     # resaltados (p.ej. señal bloqueada)
GROUP = ["#0b7a53", "#b5651d", "#6a3d9a"]  # colores de líneas de grupo (cascada)
LW = 1.5
SCALE = 0.42  # pulgadas por unidad
PORT_FS = 7
LABEL_FS = 10.5


class Diagram:
    def __init__(self, w, h, x0=0.0, y0=0.0):
        self.fig = plt.figure(figsize=(w * SCALE, h * SCALE))
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set_xlim(x0, x0 + w)
        self.ax.set_ylim(y0, y0 + h)
        self.ax.set_aspect("equal")
        self.ax.axis("off")

    # ---------------------------------------------------------------- básicos
    def line(self, pts, pilot=False, color=None, lw=LW, z=1):
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        c = color or (PILOT if pilot else INK)
        self.ax.plot(xs, ys, color=c, lw=lw if not pilot else lw * 0.9,
                     linestyle=(0, (4, 2.5)) if pilot else "-",
                     solid_capstyle="butt", zorder=z)

    def dot(self, p, color=None, pilot=False):
        c = color or (PILOT if pilot else INK)
        self.ax.add_patch(Circle(p, 0.07, color=c, zorder=5))

    def text(self, p, s, fs=LABEL_FS, ha="center", va="center", color=INK,
             weight="normal", style="normal", **kw):
        self.ax.text(p[0], p[1], s, fontsize=fs, ha=ha, va=va, color=color,
                     fontweight=weight, fontstyle=style, zorder=6, **kw)

    def seg(self, a, b, color=INK, lw=LW, z=3):
        self.ax.plot([a[0], b[0]], [a[1], b[1]], color=color, lw=lw,
                     solid_capstyle="butt", zorder=z)

    def arrow(self, a, b, color=INK, lw=1.2, head=0.16):
        """Flecha interna de válvula de a hacia b."""
        import math
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        base = (b[0] - ux * head, b[1] - uy * head)
        self.seg(a, base, color=color, lw=lw)
        px, py = -uy * head * 0.45, ux * head * 0.45
        self.ax.add_patch(Polygon([b, (base[0] + px, base[1] + py),
                                   (base[0] - px, base[1] - py)],
                                  closed=True, color=color, zorder=4))

    def block(self, p, inward):
        """Puerto bloqueado (símbolo T). inward = +1 si el puerto está abajo."""
        x, y = p
        y2 = y + inward * 0.2
        self.seg((x, y), (x, y2), lw=1.2)
        self.seg((x - 0.1, y2), (x + 0.1, y2), lw=1.2)

    def exhaust(self, p):
        """Escape a la atmósfera (triángulo abierto bajo el puerto)."""
        x, y = p
        self.ax.add_patch(Polygon([(x, y), (x - 0.13, y - 0.2), (x + 0.13, y - 0.2)],
                                  closed=True, fill=False, ec=INK, lw=1.1, zorder=4))

    def source(self, p):
        """Fuente de aire comprimido (círculo con triángulo) colgando del puerto p."""
        x, y = p
        c = (x, y - 0.17)
        self.ax.add_patch(Circle(c, 0.17, fill=False, ec=INK, lw=1.1, zorder=4))
        self.ax.add_patch(Polygon([(x, c[1] + 0.1), (x - 0.08, c[1] - 0.06),
                                   (x + 0.08, c[1] - 0.06)],
                                  closed=True, color=INK, zorder=4))

    # ---------------------------------------------------------- actuadores
    def actuator(self, kind, xs, ym, d, label=None):
        """Dibuja el accionamiento en el lado xs (borde), d=-1 izquierda, +1 derecha.
        Devuelve el punto de conexión (solo útil para pilotaje)."""
        if kind is None:
            return None
        if kind == "spring":
            pts = [(xs, ym)]
            n = 6
            for i in range(1, n + 1):
                pts.append((xs + d * 0.1 * i, ym + (0.18 if i % 2 else -0.18)))
            pts.append((xs + d * 0.7, ym))
            self.ax.plot([p[0] for p in pts], [p[1] for p in pts], color=INK, lw=1.1, zorder=3)
            return None
        if kind == "button":
            self.seg((xs, ym), (xs + d * 0.25, ym), lw=1.2)
            self.seg((xs + d * 0.25, ym - 0.22), (xs + d * 0.25, ym + 0.22), lw=1.2)
            cx = xs + d * 0.25
            th1, th2 = (90, 270) if d < 0 else (-90, 90)
            self.ax.add_patch(Arc((cx, ym), 0.3, 0.44, theta1=th1, theta2=th2,
                                  ec=INK, lw=1.2, zorder=3))
            return None
        if kind == "pedal":
            self.seg((xs, ym), (xs + d * 0.2, ym), lw=1.2)
            self.seg((xs + d * 0.2, ym - 0.2), (xs + d * 0.55, ym + 0.2), lw=1.4)
            return None
        if kind == "lever":
            self.seg((xs, ym), (xs + d * 0.2, ym), lw=1.2)
            self.seg((xs + d * 0.2, ym), (xs + d * 0.5, ym + 0.35), lw=1.2)
            self.ax.add_patch(Circle((xs + d * 0.5, ym + 0.35), 0.05, color=INK, zorder=4))
            return None
        if kind in ("roller", "roller1"):
            self.seg((xs, ym), (xs + d * 0.2, ym), lw=1.2)
            self.seg((xs + d * 0.2, ym - 0.15), (xs + d * 0.2, ym + 0.15), lw=1.2)
            if kind == "roller":
                self.seg((xs + d * 0.2, ym), (xs + d * 0.42, ym), lw=1.2)
                c = (xs + d * 0.54, ym)
            else:  # rodillo escamoteable (actúa en un solo sentido)
                self.seg((xs + d * 0.2, ym), (xs + d * 0.36, ym), lw=1.2)
                self.seg((xs + d * 0.36, ym), (xs + d * 0.46, ym + 0.14), lw=1.2)
                c = (xs + d * 0.54, ym + 0.24)
                self.arrow((xs + d * 0.38, ym - 0.22), (xs + d * 0.7, ym - 0.22), lw=0.9, head=0.1)
            self.ax.add_patch(Circle(c, 0.12, fill=False, ec=INK, lw=1.2, zorder=4))
            if label:
                self.text((c[0] + d * 0.05, c[1] + 0.38), label, fs=LABEL_FS, weight="bold",
                          color=PILOT)
            return None
        if kind == "pilot":
            tip = (xs, ym)
            b = xs + d * 0.28
            self.ax.add_patch(Polygon([tip, (b, ym + 0.13), (b, ym - 0.13)], closed=True,
                                      fill=False, ec=INK, lw=1.1, zorder=4))
            self.seg((b, ym), (xs + d * 0.45, ym), lw=1.1)
            return (xs + d * 0.45, ym)
        raise ValueError(kind)

    # -------------------------------------------------------------- válvulas
    VALVES = {
        # ports: nombre -> (lado, x relativo dentro del cuadro)
        "3/2": {
            "ports": {"2": ("top", 0.3), "1": ("bot", 0.3), "3": ("bot", 0.7)},
            # contenido de cada cuadro: 0 = accionado (izquierda), 1 = reposo (derecha)
            "boxes": [
                [("arrow", (0.3, 0), (0.3, 1)), ("block", "3")],
                [("arrow", (0.3, 1), (0.7, 0)), ("block", "1")],
            ],
            "pilots": ("12", "10"),
        },
        "5/2": {
            "ports": {"4": ("top", 0.25), "2": ("top", 0.75), "5": ("bot", 0.2),
                      "1": ("bot", 0.5), "3": ("bot", 0.8)},
            "boxes": [
                [("arrow", (0.5, 0), (0.25, 1)), ("arrow", (0.75, 1), (0.8, 0)), ("block", "5")],
                [("arrow", (0.5, 0), (0.75, 1)), ("arrow", (0.25, 1), (0.2, 0)), ("block", "3")],
            ],
            "pilots": ("14", "12"),
        },
        "4/2": {
            "ports": {"4": ("top", 0.3), "2": ("top", 0.7), "1": ("bot", 0.3),
                      "3": ("bot", 0.7)},
            "boxes": [
                [("arrow", (0.3, 0), (0.3, 1)), ("arrow", (0.7, 1), (0.7, 0))],
                [("arrow", (0.3, 0), (0.7, 1)), ("arrow", (0.3, 1), (0.7, 0))],
            ],
            "pilots": ("14", "12"),
        },
    }

    def valve(self, x, y, kind, left=None, right="spring", pos=1, label=None,
              supply=True, exhausts=True, label_side="right", lim=None):
        """Válvula de 2 posiciones con esquina inferior izquierda en (x, y).
        pos: cuadro al que se conectan los puertos (1 = reposo/derecha, 0 = izquierda).
        Devuelve dict de puntos de conexión (extremos de los puertos y pilotajes)."""
        spec = self.VALVES[kind]
        s = 1.0
        for i in range(2):
            self.ax.add_patch(Rectangle((x + i * s, y), s, s, fill=False, ec=INK, lw=LW, zorder=3))
            for item in spec["boxes"][i]:
                if item[0] == "arrow":
                    a = (x + i * s + item[1][0], y + item[1][1])
                    b = (x + i * s + item[2][0], y + item[2][1])
                    self.arrow(a, b)
                else:
                    side, rx = spec["ports"][item[1]]
                    py = y if side == "bot" else y + s
                    self.block((x + i * s + rx, py), 1 if side == "bot" else -1)
        ports = {}
        for name, (side, rx) in spec["ports"].items():
            px = x + pos * s + rx
            if side == "top":
                self.seg((px, y + s), (px, y + s + 0.3))
                ports[name] = (px, y + s + 0.3)
                self.text((px + 0.13, y + s + 0.17), name, fs=PORT_FS, ha="left")
            else:
                ln = 0.62 if name == "1" else 0.3
                self.seg((px, y), (px, y - ln))
                ports[name] = (px, y - ln)
                self.text((px + 0.1, y - 0.15), name, fs=PORT_FS, ha="left")
                if name == "1" and supply:
                    self.source((px, y - ln))
                if name in ("3", "5") and exhausts:
                    self.exhaust((px, y - 0.3))
        lp = self.actuator(left, x, y + 0.5, -1, label=lim)
        rp = self.actuator(right, x + 2 * s, y + 0.5, +1, label=lim)
        if lp:
            ports[spec["pilots"][0]] = lp
            self.text((lp[0] + 0.05, lp[1] + 0.2), spec["pilots"][0], fs=PORT_FS, ha="right")
        if rp:
            ports[spec["pilots"][1]] = rp
            self.text((rp[0] - 0.05, rp[1] + 0.2), spec["pilots"][1], fs=PORT_FS, ha="left")
        if label:
            if label_side == "right":
                off = 2 * s + (0.85 if right else 0.2)
                self.text((x + off, y + 0.5), label, fs=LABEL_FS, ha="left", weight="bold")
            elif label_side == "below":
                self.text((x + s, y - 1.05), label, fs=LABEL_FS, weight="bold", va="top")
            elif label_side == "top":
                self.text((x + 0.5, y + 1.12), label, fs=LABEL_FS, weight="bold", va="bottom")
            elif label_side == "above":
                self.text((x - 0.15, y + 1.25), label, fs=LABEL_FS, weight="bold", ha="right")
            else:
                off = 0.85 if left else 0.2
                self.text((x - off, y + 0.5), label, fs=LABEL_FS, ha="right", weight="bold")
        ports["_box"] = (x, y)
        return ports

    # ------------------------------------------------------------- cilindros
    def cylinder(self, x, y, name, L=4.0, H=1.0, single=False, marks=("0", "1"),
                 mark_names=None):
        """Cilindro horizontal (retraído). Puertos abajo: 'A' (cámara posterior) y
        'B' (lado vástago). Marcas de final de carrera sobre el vástago."""
        self.ax.add_patch(Rectangle((x, y), L, H, fill=False, ec=INK, lw=LW, zorder=3))
        xp = x + 0.45
        self.ax.add_patch(Rectangle((xp - 0.07, y), 0.14, H, color=INK, zorder=3))
        tip = x + L + 0.6
        self.ax.add_patch(Rectangle((xp, y + H / 2 - 0.1), tip - xp, 0.2, fill=False,
                                    ec=INK, lw=1.2, zorder=3))
        ports = {"A": (x + 0.3, y - 0.3)}
        self.seg((x + 0.3, y), (x + 0.3, y - 0.3))
        if single:
            pts = [(xp + 0.1, y + 0.5 * H)]
            n = 10
            span = (x + L - 0.05) - (xp + 0.1)
            for i in range(1, n):
                pts.append((xp + 0.1 + span * i / n, y + H * (0.82 if i % 2 else 0.18)))
            pts.append((x + L - 0.05, y + 0.5 * H))
            self.ax.plot([p[0] for p in pts], [p[1] for p in pts], color=INK, lw=0.9, zorder=2)
            # orificio de venteo
            self.seg((x + L - 0.3, y), (x + L - 0.3, y - 0.12), lw=1.0)
        else:
            ports["B"] = (x + L - 0.3, y - 0.3)
            self.seg((x + L - 0.3, y), (x + L - 0.3, y - 0.3))
        self.text((x - 0.35, y + H / 2), name, fs=13, weight="bold", ha="right")
        stroke = L - 0.9
        ports["tip0"] = (tip, y + H / 2)
        ports["tip1"] = (tip + stroke, y + H / 2)
        if marks:
            lo = name.lower()
            names = mark_names or [(lo + m) if m else None for m in marks]
            for k, xm in enumerate((tip, tip + stroke)):
                if names[k] is None:
                    continue
                self.seg((xm, y + H / 2 + 0.2), (xm, y + H + 0.45), color=PILOT, lw=1.2)
                self.text((xm, y + H + 0.7), names[k], fs=LABEL_FS, weight="bold", color=PILOT)
            self.seg((tip, y + H + 0.3), (tip + stroke, y + H + 0.3), color="#9aa7bd", lw=0.8)
        return ports

    # --------------------------------------------------- reguladores y lógica
    def flow_ctrl(self, x, y, free="up", label=None, label_side="right"):
        """Válvula reguladora de caudal unidireccional (estrangulación + antirretorno),
        vertical. Puertos 'bot' (x, y) y 'top' (x, y+1.6)."""
        yb, yt = y + 0.3, y + 1.3
        self.seg((x, y), (x, yb))
        self.seg((x, yt), (x, y + 1.6))
        xl, xr = x - 0.28, x + 0.28
        self.seg((xl, yb), (xr, yb))
        self.seg((xl, yt), (xr, yt))
        ym = (yb + yt) / 2
        # rama estrangulación
        self.seg((xl, yb), (xl, ym - 0.22))
        self.seg((xl, ym + 0.22), (xl, yt))
        self.ax.add_patch(Arc((xl - 0.14, ym), 0.24, 0.44, theta1=-60, theta2=60, ec=INK, lw=1.1, zorder=3))
        self.ax.add_patch(Arc((xl + 0.14, ym), 0.24, 0.44, theta1=120, theta2=240, ec=INK, lw=1.1, zorder=3))
        self.arrow((xl - 0.25, ym - 0.3), (xl + 0.25, ym + 0.3), lw=0.9, head=0.11)
        # rama antirretorno
        sgn = 1 if free == "up" else -1
        apex = (xr, ym - sgn * 0.18)
        self.seg((xr, yb if sgn > 0 else yt), apex)
        self.seg(apex, (xr - 0.13, ym + sgn * 0.02))
        self.seg(apex, (xr + 0.13, ym + sgn * 0.02))
        ball = (xr, ym + sgn * 0.0)
        self.ax.add_patch(Circle(ball, 0.09, fill=False, ec=INK, lw=1.1, zorder=4))
        self.seg((xr, ym + sgn * 0.09), (xr, yt if sgn > 0 else yb))
        # recuadro de componente
        self.ax.add_patch(Rectangle((x - 0.6, y + 0.15), 1.2, 1.3, fill=False, ec="#777",
                                    lw=0.8, ls=(0, (3, 2)), zorder=2))
        if label:
            if label_side == "right":
                self.text((x + 0.7, y + 0.8), label, fs=PORT_FS + 1, ha="left")
            else:
                self.text((x - 0.7, y + 0.8), label, fs=PORT_FS + 1, ha="right")
        return {"bot": (x, y), "top": (x, y + 1.6)}

    def logic(self, x, y, kind="or", label=None):
        """Válvula selectora (OR) o de simultaneidad (AND), centrada en (x, y).
        Entradas izquierda/derecha, salida arriba."""
        w, h = 1.0, 0.44
        self.ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, fill=False, ec=INK, lw=LW, zorder=3))
        if kind == "or":
            self.ax.add_patch(Circle((x, y), 0.11, color=INK, zorder=4))
            for s in (-1, 1):
                xs = x + s * 0.28
                self.seg((xs, y - 0.13), (xs + s * 0.12, y), lw=1.0)
                self.seg((xs, y + 0.13), (xs + s * 0.12, y), lw=1.0)
        else:
            for s in (-1, 1):
                self.ax.add_patch(Rectangle((x + s * 0.3 - 0.06, y - 0.12), 0.12, 0.24,
                                            fill=False, ec=INK, lw=1.0, zorder=4))
            self.seg((x - 0.24, y), (x + 0.24, y), lw=1.0)
        self.seg((x - w / 2, y), (x - w / 2 - 0.25, y))
        self.seg((x + w / 2, y), (x + w / 2 + 0.25, y))
        self.seg((x, y + h / 2), (x, y + h / 2 + 0.3))
        self.text((x - 0.62, y - 0.17), "1", fs=PORT_FS)
        self.text((x + 0.62, y - 0.17), "1", fs=PORT_FS)
        self.text((x + 0.12, y + h / 2 + 0.15), "2", fs=PORT_FS, ha="left")
        if label:
            self.text((x, y - 0.48), label, fs=PORT_FS + 1)
        return {"l": (x - w / 2 - 0.25, y), "r": (x + w / 2 + 0.25, y),
                "out": (x, y + h / 2 + 0.3)}

    def service_unit(self, x, y):
        """Fuente + unidad de mantenimiento (símbolo simplificado). Salida a la derecha."""
        self.ax.add_patch(Circle((x, y), 0.3, fill=False, ec=INK, lw=LW, zorder=3))
        self.ax.add_patch(Polygon([(x + 0.18, y), (x - 0.1, y + 0.15), (x - 0.1, y - 0.15)],
                                  closed=True, color=INK, zorder=4))
        self.seg((x + 0.3, y), (x + 0.8, y))
        bx = x + 0.8
        self.ax.add_patch(Rectangle((bx, y - 0.55), 1.4, 1.1, fill=False, ec=INK, lw=LW,
                                    ls=(0, (4, 2)), zorder=3))
        cx = bx + 0.7
        self.ax.add_patch(Polygon([(cx - 0.3, y), (cx, y + 0.3), (cx + 0.3, y), (cx, y - 0.3)],
                                  closed=True, fill=False, ec=INK, lw=1.2, zorder=4))
        self.seg((cx - 0.18, y), (cx + 0.18, y), lw=0.9)
        self.seg((cx - 0.3, y), (bx, y))
        self.seg((cx + 0.3, y), (bx + 1.4, y))
        self.seg((bx + 1.4, y), (bx + 1.8, y))
        return {"out": (bx + 1.8, y)}

    def save(self, path_noext):
        self.fig.savefig(path_noext + ".png", dpi=220, transparent=False, facecolor="white")
        self.fig.savefig(path_noext + ".svg", facecolor="white", metadata={"Date": None})
        plt.close(self.fig)
