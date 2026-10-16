"""Diagramas espacio-fase (desplazamiento-fase) con señales de mando y estado de
los finales de carrera. Genera PNG + SVG en ../figuras/.

Uso:  python3 src/diagramas.py
"""
import os

import matplotlib

matplotlib.use("Agg")
matplotlib.rcParams["svg.hashsalt"] = "rgim-neumatica"
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "figuras")
NAVY = "#042254"
GREEN = "#0b7a53"
ORANGE = "#b5651d"
RED = "#c0392b"
GREY = "#9aa7bd"
BAR = "#1f4e9c"


def phase(name, cyls, steps, signals=None, groups=None, sensors=None, conflicts=None,
          title=None):
    """cyls: 'AB'...; steps: lista de listas de movimientos ('A+', 'B-')
    signals: texto de la señal que dispara cada paso
    groups: lista de (paso_ini, paso_fin_excl, etiqueta)
    sensors: lista de sensores a dibujar ('a0', 'a1', ...)
    conflicts: lista de (sensor, paso) donde la señal queda bloqueada."""
    n = len(steps)
    pos = {c: [0] for c in cyls}
    for st in steps:
        for c in cyls:
            lv = pos[c][-1]
            for m in st:
                if m[0] == c:
                    lv = 1 if m[1] == "+" else 0
            pos[c].append(lv)
    sensors = sensors or []
    rows = len(cyls)
    rh, gap = 1.0, 0.7
    sens_h = 0.42
    top_extra = 1.5 + (0.7 if groups else 0)
    H = rows * (rh + gap) + len(sensors) * sens_h + top_extra + (0.6 if sensors else 0)
    W = n + (3.8 if conflicts else 2.6)
    fig = plt.figure(figsize=(W * 0.95, H * 0.62))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(-1.9, n + (1.9 if conflicts else 0.7))
    ax.set_ylim(-len(sensors) * sens_h - (0.6 if sensors else 0.4), rows * (rh + gap) + top_extra - 0.4)
    ax.axis("off")
    ytop = rows * (rh + gap) - gap
    # cuadrícula de fases
    for k in range(n + 1):
        ax.plot([k, k], [-(len(sensors) * sens_h) - 0.1, ytop + 0.2], color=GREY, lw=0.7, zorder=0)
        ax.text(k, ytop + 0.4, str(k + 1 if k < n else 1), ha="center", va="bottom", fontsize=9,
                color="#555")
    ax.text(-1.85, ytop + 0.4, "fase", fontsize=9, color="#555", va="bottom")
    # filas de cilindros
    for r, c in enumerate(cyls):
        y0 = (rows - 1 - r) * (rh + gap)
        ax.plot([0, n], [y0, y0], color=GREY, lw=0.6)
        ax.plot([0, n], [y0 + rh, y0 + rh], color=GREY, lw=0.6, ls=":")
        ax.text(-1.15, y0 + rh / 2, c, fontsize=15, weight="bold", ha="center", va="center", color=NAVY)
        ax.text(-0.25, y0, "0", fontsize=8, ha="center", va="center", color="#555")
        ax.text(-0.25, y0 + rh, "1", fontsize=8, ha="center", va="center", color="#555")
        xs = list(range(n + 1))
        ys = [y0 + rh * p for p in pos[c]]
        ax.plot(xs, ys, color=NAVY, lw=2.6, solid_joinstyle="round", zorder=3)
    # señales
    if signals:
        for k, s in enumerate(signals):
            ax.annotate(s, xy=(k + 0.04, ytop + 0.05), xytext=(k + 0.12, ytop + 0.95), fontsize=9,
                        color=BAR, weight="bold", ha="left",
                        arrowprops=dict(arrowstyle="-|>", color=BAR, lw=0.9))
    # grupos (cascada)
    if groups:
        cols = {"I": GREEN, "II": ORANGE, "III": "#6a3d9a"}
        for a, b, lab in groups:
            col = cols.get(lab, GREEN)
            ax.add_patch(Rectangle((a, ytop + 1.55), b - a, 0.45, color=col, alpha=0.18, lw=0))
            ax.text((a + b) / 2, ytop + 1.775, "Grupo " + lab, ha="center", va="center", fontsize=9,
                    color=col, weight="bold")
    # sensores
    for i, s in enumerate(sensors):
        y = -0.55 - i * sens_h
        c, lvl = s[0].upper(), int(s[1])
        ax.text(-1.15, y, s, fontsize=9, ha="center", va="center", color=BAR, weight="bold")
        p = pos[c]
        for k in range(n + 1):
            if p[k] == lvl:
                # activo en el punto k; se mantiene si no se mueve en el paso k
                x1 = k + 1 if (k < n and p[k + 1] == lvl) else k + 0.12
                x0 = k - 0.12 if (k == 0 or p[k - 1] != lvl) else k
                ax.add_patch(Rectangle((x0, y - 0.11), x1 - x0, 0.22, color=BAR, alpha=0.8, lw=0))
    if conflicts:
        for s, k in conflicts:
            i = sensors.index(s)
            y = -0.55 - i * sens_h
            ax.add_patch(Rectangle((k - 0.3, y - 0.2), 0.6, 0.4, fill=False, ec=RED, lw=2.0, zorder=5))
            ax.text(n + 0.2, y, "← bloqueada en fase %d" % (k + 1), fontsize=8, color=RED, va="center",
                    weight="bold")
    if title:
        ax.text(n / 2, rows * (rh + gap) + top_extra - 0.75, title, ha="center", fontsize=11,
                weight="bold", color=NAVY)
    fig.savefig(os.path.join(OUT, name + ".png"), dpi=220, facecolor="white")
    fig.savefig(os.path.join(OUT, name + ".svg"), facecolor="white", metadata={"Date": None})
    plt.close(fig)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    phase("fase_ABAB", "AB", [["A+"], ["B+"], ["A-"], ["B-"]],
          signals=["S·b0", "a1", "b1", "a0"], sensors=["a0", "a1", "b0", "b1"],
          title="A+ B+ A− B−")
    phase("fase_ABBA_bloqueo", "AB", [["A+"], ["B+"], ["B-"], ["A-"]],
          signals=["S·a0", "a1", "b1", "b0"], sensors=["a0", "a1", "b0", "b1"],
          conflicts=[("b0", 0), ("a1", 2)], title="A+ B+ B− A−  (sin cascada)")
    phase("fase_ABBA_cascada", "AB", [["A+"], ["B+"], ["B-"], ["A-"]],
          signals=["S·a0 →I", "a1", "b1 →II", "b0"],
          groups=[(0, 2, "I"), (2, 4, "II")], title="A+ B+ | B− A−  (cascada, 2 grupos)")
    phase("fase_e1_2", "A", [["A+"], ["A-"]], signals=["S1", "a1"], sensors=["a1"],
          title="A+ A−")
    phase("fase_e2_1", "ABC", [["A+"], ["B+"], ["A-", "B-"], ["C+"], ["C-"]],
          signals=["S·c0", "a1", "b1 →II", "a0·b0", "c1 →I"],
          groups=[(0, 2, "I"), (2, 4, "II"), (4, 5, "I")],
          title="A+ B+ (A− B−) C+ C−")
    phase("fase_e2_2", "ABC", [["A+"], ["B+"], ["C+"], ["A-", "B-", "C-"]],
          signals=["S·a0·b0·c0 →I", "a1", "b1", "c1 →II"],
          groups=[(0, 3, "I"), (3, 4, "II")], title="A+ B+ C+ (A− B− C−)")
    phase("fase_e2_3", "AB", [["A+", "B+"], ["A-"], ["B-"]],
          signals=["(P+S)·b0 →I", "a1·b1 →II", "a0"],
          groups=[(0, 1, "I"), (1, 3, "II")], title="(A+ B+) A− B−")
    print("ok")
