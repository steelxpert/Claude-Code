#!/usr/bin/env python3
"""Figures for FLINS-CFS-006: bearer candidates at the pile head, and utilisation bars. Usage: python3 docs/figures_bearer.py OUT_DIR"""
import sys
from pathlib import Path
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyArrowPatch, Circle
sys.path.insert(0, str(Path(__file__).parent)); import bearer_calc as bc

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "figs"); OUT.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8})
STEEL, HOT, LOAD, SUP, GREY = "#2a4d7a", "#7b241c", "#d35400", "#333333", "#777777"


def cshape(ax, x, y, h, b, c, t, flip=False, color=STEEL):
    s = -1 if flip else 1
    pts = [(x, y), (x + s * b, y), (x + s * b, y + c), (x + s * (b - t), y + c), (x + s * (b - t), y + t), (x + s * t, y + t),
           (x + s * t, y + h - t), (x + s * (b - t), y + h - t), (x + s * (b - t), y + h - c), (x + s * b, y + h - c), (x + s * b, y + h), (x, y + h)]
    ax.add_patch(Polygon(pts, closed=True, fc="#dfe8f3", ec=color, lw=1))


def f1():
    f, ax = plt.subplots(figsize=(15.5 / 2.54, 3.0)); ax.set_aspect("equal"); ax.axis("off")
    k = 0.012  # mm -> units
    base_y = 1.3
    # (a) back-to-back 2xC250
    x = 1.0; cshape(ax, x, base_y, 250 * k, 60 * k, 18 * k, 2.5 * k, flip=True); cshape(ax, x, base_y, 250 * k, 60 * k, 18 * k, 2.5 * k)
    ax.text(x, base_y + 250 * k + 0.25, "(a) 2×C back-to-back,\nscrewed webs", ha="center", fontsize=6.5, va="bottom")
    # (b) boxed 2xC
    x = 3.3; cshape(ax, x - 60 * k, base_y, 250 * k, 60 * k, 18 * k, 2.5 * k); cshape(ax, x + 60 * k, base_y, 250 * k, 60 * k, 18 * k, 2.5 * k, flip=True)
    ax.text(x, base_y + 250 * k + 0.25, "(b) 2×C boxed,\nlips inward", ha="center", fontsize=6.5, va="bottom")
    # (c) 2xC with bearing stiffener at the pile
    x = 5.6; cshape(ax, x, base_y, 250 * k, 60 * k, 18 * k, 2.5 * k, flip=True); cshape(ax, x, base_y, 250 * k, 60 * k, 18 * k, 2.5 * k)
    ax.add_patch(Rectangle((x - 0.55, base_y + 0.05), 0.5, 250 * k - 0.1, fc="none", ec=LOAD, lw=1.2, ls="--")); ax.add_patch(Rectangle((x + 0.05, base_y + 0.05), 0.5, 250 * k - 0.1, fc="none", ec=LOAD, lw=1.2, ls="--"))
    ax.text(x, base_y + 250 * k + 0.25, "(c) 2×C with bearing\nstiffeners at each pile", ha="center", fontsize=6.5, va="bottom")
    # (d) HEA 140
    x = 7.9; h, b, tf, tw = 133 * k, 140 * k, 8.5 * k, 5.5 * k
    ax.add_patch(Polygon([(x - b / 2, base_y), (x + b / 2, base_y), (x + b / 2, base_y + tf), (x + tw / 2, base_y + tf), (x + tw / 2, base_y + h - tf), (x + b / 2, base_y + h - tf), (x + b / 2, base_y + h),
                          (x - b / 2, base_y + h), (x - b / 2, base_y + h - tf), (x - tw / 2, base_y + h - tf), (x - tw / 2, base_y + tf), (x - b / 2, base_y + tf)], closed=True, fc="#f2dede", ec=HOT, lw=1))
    ax.text(x, base_y + 250 * k + 0.25, "(d) HEA 140, hot-dip\ngalvanised, bolted", ha="center", fontsize=6.5, va="bottom")
    # (e) RHS 150x100
    x = 10.2; ax.add_patch(Rectangle((x - 50 * k, base_y), 100 * k, 150 * k, fc="#f2dede", ec=HOT, lw=1.2)); ax.add_patch(Rectangle((x - 45 * k, base_y + 5 * k), 90 * k, 140 * k, fc="white", ec=HOT, lw=0.8))
    ax.text(x, base_y + 250 * k + 0.25, "(e) RHS 150×100×5,\ngalvanised, bolted", ha="center", fontsize=6.5, va="bottom")
    # pile head plates and reaction arrows for all
    for x in (1.0, 3.3, 5.6, 7.9, 10.2):
        ax.add_patch(Rectangle((x - 0.9, base_y - 0.12), 1.8, 0.12, fc="#aaaaaa", ec=SUP, lw=0.8))
        ax.add_patch(Rectangle((x - 0.1, base_y - 0.75), 0.2, 0.63, fc="#cccccc", ec=SUP, lw=0.8))
        ax.add_patch(FancyArrowPatch((x, base_y - 1.25), (x, base_y - 0.8), arrowstyle="-|>", mutation_scale=10, color=LOAD, lw=1.4))
    ax.text(5.6, base_y - 1.45, "pile reaction R_Ed ≈ 33 to 50 kN at 2.0 to 3.0 m pile spacing (bay 3.0 m, g = 1.5, q = 2.0 kN/m²), entering the bearer from below", ha="center", fontsize=7, color=LOAD)
    ax.set_xlim(-0.2, 11.4); ax.set_ylim(-0.4, 5.2); f.savefig(OUT / "F1_bearer_candidates.png", dpi=220, bbox_inches="tight"); plt.close(f)


def f2():
    f, ax = plt.subplots(figsize=(15.5 / 2.54, 2.8))
    names = [c["name"].replace(" back-to-back", "") for c in bc.CANDIDATES]
    import numpy as np
    xs = np.arange(len(names)); wdt = 0.26
    for i, (s_p, col) in enumerate(((2.0, "#a9cce3"), (2.5, "#5499c7"), (3.0, "#1f618d"))):
        u = [bc.check(c, s_p, 3.0)["uR"] for c in bc.CANDIDATES]
        ax.bar(xs + (i - 1) * wdt, u, wdt, color=col, label=f"pile spacing {s_p} m")
    ax.axhline(1.0, color=LOAD, lw=1, ls="--"); ax.text(len(names) - 0.6, 1.03, "limit", color=LOAD, fontsize=7)
    ax.set_xticks(xs); ax.set_xticklabels(names, fontsize=7); ax.set_ylabel("R_Ed / R_w,Rd at the pile"); ax.set_ylim(0, 1.4); ax.legend(fontsize=7); ax.grid(axis="y", alpha=0.3)
    f.tight_layout(); f.savefig(OUT / "F2_crippling_utilisation.png", dpi=220); plt.close(f)


f1(); f2(); print("figures written to", OUT)
