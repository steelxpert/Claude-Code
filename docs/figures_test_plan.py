#!/usr/bin/env python3
"""Schematic figures for the test plan (FLINS-CFS-002). Usage: python3 docs/figures_test_plan.py OUT_DIR"""
from __future__ import annotations
import sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyArrowPatch, Circle, FancyBboxPatch

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "figs"); OUT.mkdir(parents=True, exist_ok=True)
W_IN = 15.5 / 2.54
STEEL, BEARER, DECK, LOAD, SUP, GREY, GREEN = "#2a4d7a", "#b03a2e", "#c8a86a", "#d35400", "#333333", "#777777", "#1e8449"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8})


def fig(h_in=2.6):
    f, ax = plt.subplots(figsize=(W_IN, h_in)); ax.set_aspect("equal"); ax.axis("off"); return f, ax


def pin(ax, x, y, s=0.18, roller=False):
    ax.add_patch(Polygon([(x, y), (x - s, y - s * 1.6), (x + s, y - s * 1.6)], closed=True, fc="white", ec=SUP, lw=1.2))
    if roller:
        for dx in (-s * 0.6, 0, s * 0.6): ax.add_patch(Circle((x + dx, y - s * 1.9), s * 0.25, fc="white", ec=SUP, lw=1))
        ax.plot([x - s * 1.3, x + s * 1.3], [y - s * 2.2, y - s * 2.2], color=SUP, lw=1.2)
    else:
        ax.plot([x - s * 1.3, x + s * 1.3], [y - s * 1.6, y - s * 1.6], color=SUP, lw=1.2)
    for i in range(5):
        xx = x - s * 1.1 + i * s * 0.55; yy = y - (s * 2.2 if roller else s * 1.6); ax.plot([xx, xx - s * 0.3], [yy, yy - s * 0.3], color=SUP, lw=0.8)


def arrow(ax, x, y0, y1, color=LOAD, lw=1.6, label=None, dx=0.08):
    ax.add_patch(FancyArrowPatch((x, y0), (x, y1), arrowstyle="-|>", mutation_scale=12, color=color, lw=lw))
    if label: ax.text(x + dx, (y0 + y1) / 2, label, color=color, va="center", fontsize=8)


def dim(ax, x0, x1, y, text, color=GREY):
    ax.add_patch(FancyArrowPatch((x0, y), (x1, y), arrowstyle="<|-|>", mutation_scale=8, color=color, lw=0.8))
    for x in (x0, x1): ax.plot([x, x], [y - 0.08, y + 0.08], color=color, lw=0.8)
    ax.text((x0 + x1) / 2, y + 0.06, text, ha="center", va="bottom", fontsize=7.5, color=color)


def beam(ax, x0, x1, y, h=0.22, color=STEEL, label=None):
    ax.add_patch(Rectangle((x0, y), x1 - x0, h, fc="white", ec=color, lw=1.5))
    if label: ax.text((x0 + x1) / 2, y + h / 2, label, ha="center", va="center", fontsize=7.5, color=color)


def gauge(ax, x, y, label="δ"):
    ax.plot([x, x], [y, y - 0.25], color=GREEN, lw=1); ax.add_patch(Circle((x, y - 0.33), 0.08, fc="white", ec=GREEN, lw=1))
    ax.text(x + 0.12, y - 0.33, label, color=GREEN, fontsize=7.5, va="center")


def csection(ax, x, y, h=0.5, b=0.17, t=0.035, color=STEEL, flip=False):
    s = -1 if flip else 1
    pts = [(x, y), (x + s * b, y), (x + s * b, y + 0.08), (x + s * (b - t), y + 0.08), (x + s * (b - t), y + t), (x + s * t, y + t),
           (x + s * t, y + h - t), (x + s * (b - t), y + h - t), (x + s * (b - t), y + h - 0.08), (x + s * b, y + h - 0.08), (x + s * b, y + h), (x, y + h)]
    ax.add_patch(Polygon(pts, closed=True, fc="#dfe8f3", ec=color, lw=1))


# ------------------------------------------------------------------ F1 programme flow
def f1():
    f, ax = fig(3.0)
    bw, bh = 2.25, 1.0
    boxes = [(0.1, 1.6, "T0\nmaterial and geometry", "#eeeeee"), (2.6, 1.6, "T1 joist bending\nT2 web crippling", "#dfe8f3"),
             (5.1, 1.6, "GMNIA validation,\nmodel factor γFE", "#fde9d9"), (7.6, 1.6, "span tables\n(FE extrapolation)", "#e2f0d9"),
             (0.1, 0.2, "T6\nfloor prototype", "#eeeeee"), (2.6, 0.2, "T3 bearers, T4 joints,\nT5 pile-head joint", "#dfe8f3"),
             (5.1, 0.2, "test-based resistances\n(EN 1990 D, AISI K2)", "#fde9d9"), (7.6, 0.2, "joint and bearer\ncatalogue", "#e2f0d9")]
    for x, y, t, c in boxes:
        ax.add_patch(FancyBboxPatch((x, y), bw, bh, boxstyle="round,pad=0.02,rounding_size=0.08", fc=c, ec=GREY, lw=1)); ax.text(x + bw / 2, y + bh / 2, t, ha="center", va="center", fontsize=6.6)
    for y in (2.1, 0.7):
        for x in (2.35, 4.85, 7.35): ax.add_patch(FancyArrowPatch((x, y), (x + 0.25, y), arrowstyle="-|>", mutation_scale=9, color=GREY, lw=1))
    ax.add_patch(FancyArrowPatch((1.2, 1.6), (1.2, 1.2), arrowstyle="-|>", mutation_scale=9, color=GREY, lw=1)); ax.text(1.3, 1.4, "confirms", fontsize=6.5, color=GREY, va="center")
    ax.plot([3.7, 3.7], [1.6, 1.2], color=GREY, lw=0.8, ls=":"); ax.text(3.8, 1.4, "same coupons", fontsize=6.5, color=GREY, va="center")
    ax.set_xlim(0, 10.0); ax.set_ylim(0.1, 2.7); f.savefig(OUT / "F1_programme.png", dpi=220, bbox_inches="tight"); plt.close(f)


# ------------------------------------------------------------------ F2 joist bending (four-point, pair with deck)
def f2():
    f, ax = fig(3.4)
    L = 6.0; x0 = 0.8; y = 1.2
    beam(ax, x0, x0 + L, y, 0.25, STEEL, "pair of C-joists at 600 mm, OSB deck screwed at 300 mm")
    ax.add_patch(Rectangle((x0, y + 0.25), L, 0.07, fc=DECK, ec="none"))
    for xx in (x0 + L / 3, x0 + 2 * L / 3):
        beam(ax, xx - 0.08, xx + 0.08, y + 0.32, 0.1, SUP); ax.plot([xx, xx], [y + 0.42, y + 0.75], color=SUP, lw=1.2)
    ax.add_patch(Rectangle((x0 + L / 3 - 0.08, y + 0.75), L / 3 + 0.16, 0.08, fc="white", ec=SUP, lw=1.2)); ax.text(x0 + L / 2 - 0.25, y + 0.95, "spreader beam", ha="right", fontsize=7.5, color=SUP)
    arrow(ax, x0 + L / 2, y + 1.5, y + 0.85); ax.text(x0 + L / 2 + 0.15, y + 1.3, "F: jack with load cell,\nor dead weight", color=LOAD, fontsize=7.5, va="center")
    pin(ax, x0, y); pin(ax, x0 + L, y, roller=True)
    for xx in (x0 + 0.25, x0 + L - 0.25): ax.add_patch(Rectangle((xx - 0.03, y), 0.06, 0.25, fc=LOAD, ec="none"))
    ax.text(x0 + 0.25, y + 0.45, "bearing stiffener,\n100 mm bearing", ha="left", fontsize=7, color=LOAD, va="bottom")
    for xx, lab in ((x0 + L / 3, "δ1"), (x0 + L / 2, "δ2"), (x0 + 2 * L / 3, "δ3")): gauge(ax, xx, y - 0.02, lab)
    ax.text(x0 + L / 2, y - 0.6, "δ2 at mid-span; two lateral transducers on the free bottom flange at mid-span (distortional mode)", ha="center", fontsize=7, color=GREEN)
    dim(ax, x0, x0 + L / 3, y - 0.95, "L/3"); dim(ax, x0 + L / 3, x0 + 2 * L / 3, y - 0.95, "L/3, constant moment"); dim(ax, x0 + 2 * L / 3, x0 + L, y - 0.95, "L/3")
    ax.text(x0 + L / 2, y - 1.3, "span L = 3.0, 4.2 and 5.4 m, chosen from the Stage-1 signature curve", ha="center", fontsize=7.5, color=GREY)
    csection(ax, 7.45, y - 0.05, 0.55, 0.18); csection(ax, 7.95, y - 0.05, 0.55, 0.18, flip=True); ax.text(7.7, y + 0.62, "section pair", ha="center", fontsize=7, color=STEEL)
    ax.set_xlim(0, 8.4); ax.set_ylim(-0.3, 3.0); f.savefig(OUT / "F2_joist_bending.png", dpi=220, bbox_inches="tight"); plt.close(f)


# ------------------------------------------------------------------ F3 web crippling at supports
def f3():
    f, ax = fig(3.1)
    y = 1.0
    # (a)
    x0 = 0.3
    ax.text(x0 + 1.8, 2.75, "(a) joist end on the bearer: EOF,\nwith and without bearing stiffener", ha="center", fontsize=7.5, va="top")
    beam(ax, x0 + 0.3, x0 + 3.5, y, 0.5, STEEL, "C-joist, cut length 3h")
    ax.add_patch(Rectangle((x0 + 0.3, y + 0.5), 3.2, 0.06, fc=DECK, ec="none"))
    beam(ax, x0, x0 + 0.9, y - 0.3, 0.3, BEARER, "bearer")
    ax.add_patch(Rectangle((x0 + 0.55, y), 0.05, 0.5, fc=LOAD, ec="none")); ax.text(x0 + 0.45, y + 0.62, "stiffener\n(variant)", fontsize=7, color=LOAD, ha="center", va="bottom")
    pin(ax, x0 + 0.45, y - 0.3); pin(ax, x0 + 3.3, y, roller=True)
    arrow(ax, x0 + 2.0, y + 1.3, y + 0.58); ax.text(x0 + 2.1, y + 1.05, "F on the top flange\nvia the deck", color=LOAD, fontsize=7.5, va="center")
    gauge(ax, x0 + 1.1, y - 0.02, "web crushing δ")
    ax.text(x0 + 0.45, y - 0.95, "bearing N = 100 mm", ha="center", fontsize=7, color=BEARER)
    # (b)
    x0 = 4.7
    ax.text(x0 + 1.8, 2.75, "(b) bearer over the pile head: IOF,\npile reaction from below", ha="center", fontsize=7.5, va="top")
    beam(ax, x0, x0 + 3.6, y, 0.4, BEARER, "bearer: 2×C, box, RHS or HEA")
    ax.add_patch(Rectangle((x0, y + 0.4), 3.6, 0.06, fc=DECK, ec="none"))
    for xx in (x0 + 0.5, x0 + 1.3, x0 + 2.3, x0 + 3.1): arrow(ax, xx, y + 1.05, y + 0.48, lw=1.2)
    ax.text(x0 + 1.8, y + 1.15, "joist reactions through a spreader", ha="center", fontsize=7.5, color=LOAD)
    ax.add_patch(Rectangle((x0 + 1.55, y - 0.15), 0.5, 0.15, fc="#aaaaaa", ec=SUP, lw=1))
    pin(ax, x0 + 1.8, y - 0.15); ax.text(x0 + 1.8, y - 0.95, "pile head plate,\nrigid support", ha="center", fontsize=7, color=SUP, va="top")
    pin(ax, x0 + 0.15, y, roller=True); pin(ax, x0 + 3.45, y, roller=True)
    ax.text(x0 + 0.15, y - 0.95, "soft\nspring", ha="center", fontsize=6.5, color=GREY, va="top"); ax.text(x0 + 3.45, y - 0.95, "soft\nspring", ha="center", fontsize=6.5, color=GREY, va="top")
    gauge(ax, x0 + 2.6, y - 0.02, "δ")
    ax.set_xlim(0, 8.6); ax.set_ylim(-0.1, 2.8); f.savefig(OUT / "F3_web_crippling.png", dpi=220, bbox_inches="tight"); plt.close(f)


# ------------------------------------------------------------------ F4 joist-to-rim joint shear test
def f4():
    f, ax = fig(2.9)
    x0, y = 1.0, 0.4
    ax.add_patch(Rectangle((x0, y), 0.35, 1.9, fc="#f3d6d2", ec=BEARER, lw=1.5)); ax.text(x0 + 0.17, y + 2.0, "rim track,\nbolted to the rig", ha="center", fontsize=7, color=BEARER, va="bottom")
    beam(ax, x0 + 0.35, x0 + 2.6, y + 0.6, 0.6, STEEL, "joist stub, 3h long")
    ax.add_patch(Rectangle((x0 + 0.35, y + 0.6), 0.12, 0.6, fc=LOAD, ec="none")); ax.text(x0 + 0.5, y + 1.28, "clip angle, tab or\nswaged end, with\nproduction screws", fontsize=7, color=LOAD, va="bottom")
    arrow(ax, x0 + 2.45, y + 2.1, y + 1.25); ax.text(x0 + 2.45, y + 2.2, "V (vertical shear)", color=LOAD, fontsize=7.5, va="bottom", ha="center")
    ax.plot([x0 + 2.45, x0 + 2.45], [y + 0.6, y - 0.1], color=GREY, lw=0.8, ls=":"); ax.text(x0 + 2.5, y - 0.05, "free end guided\nlaterally only", fontsize=6.5, color=GREY, va="top")
    gauge(ax, x0 + 0.6, y + 0.58, "slip δ")
    ax.plot([x0 - 0.3, x0], [y + 1.9, y + 1.9], color=SUP, lw=1.2); ax.plot([x0 - 0.3, x0], [y + 0.4, y + 0.4], color=SUP, lw=1.2)
    ax.text(x0 - 0.35, y + 1.15, "rigid\nreaction\nframe", ha="right", fontsize=7, color=SUP, va="center")
    x1 = 5.6
    ax.text(x1 + 1.5, y + 2.3, "screw lap-shear coupon (AISI S905; EN 1993-1-3 Annex A):\nt1/t2 combinations of the family, 5 replicates each", ha="center", fontsize=7, va="bottom")
    ax.add_patch(Rectangle((x1, y + 1.3), 1.8, 0.14, fc="#dfe8f3", ec=STEEL, lw=1)); ax.add_patch(Rectangle((x1 + 1.2, y + 1.44), 1.8, 0.14, fc="#dfe8f3", ec=STEEL, lw=1))
    for xx in (x1 + 1.5, x1 + 1.8): ax.add_patch(Circle((xx, y + 1.44), 0.06, fc=LOAD, ec="none"))
    ax.add_patch(FancyArrowPatch((x1, y + 1.37), (x1 - 0.6, y + 1.37), arrowstyle="-|>", mutation_scale=10, color=LOAD)); ax.add_patch(FancyArrowPatch((x1 + 3.0, y + 1.51), (x1 + 3.6, y + 1.51), arrowstyle="-|>", mutation_scale=10, color=LOAD))
    ax.text(x1 + 1.5, y + 0.9, "gives the per-screw bearing and tilting resistance\nused in the joint evaluation", ha="center", fontsize=7, color=GREY, va="top")
    ax.set_xlim(0, 9.6); ax.set_ylim(-0.6, 3.1); f.savefig(OUT / "F4_joist_rim_joint.png", dpi=220, bbox_inches="tight"); plt.close(f)


# ------------------------------------------------------------------ F5 pile-head joint: compression, uplift, shear, eccentricity
def f5():
    f, ax = fig(2.6)
    cases = [("(a) compression N", (0, -1)), ("(b) uplift T", (0, 1)), ("(c) shear H", (1, 0)), ("(d) eccentric N\n(tolerance e)", (0, -1))]
    for k, (title, d) in enumerate(cases):
        x0 = 0.3 + k * 2.3; y = 0.9
        beam(ax, x0, x0 + 1.7, y, 0.35, BEARER, "bearer")
        ax.add_patch(Rectangle((x0 + 0.55, y - 0.12), 0.6, 0.12, fc="#aaaaaa", ec=SUP, lw=1))
        ax.add_patch(Rectangle((x0 + 0.78, y - 0.75), 0.14, 0.63, fc="#cccccc", ec=SUP, lw=1))
        for xx in (x0 + 0.65, x0 + 1.05): ax.add_patch(Circle((xx, y - 0.06), 0.035, fc=LOAD, ec="none"))
        ax.plot([x0 + 0.6, x0 + 1.1], [y - 0.75, y - 0.75], color=SUP, lw=1.5); ax.text(x0 + 0.85, y - 0.9, "pile stub fixed to the rig", ha="center", fontsize=6.5, color=SUP)
        xl = x0 + 0.85 + (0.5 if k == 3 else 0)
        if d == (0, -1): arrow(ax, xl, y + 1.0, y + 0.4, lw=1.6)
        elif d == (0, 1): arrow(ax, xl, y + 0.4, y + 1.0, lw=1.6)
        else: ax.add_patch(FancyArrowPatch((x0 + 2.0, y + 0.17), (x0 + 1.55, y + 0.17), arrowstyle="-|>", mutation_scale=12, color=LOAD, lw=1.6))
        if k == 3: dim(ax, x0 + 0.85, xl, y + 0.5, "e")
        ax.text(x0 + 0.85, 2.5, title, ha="center", fontsize=7.5, va="top")
        gauge(ax, x0 + 1.5, y - 0.02, "δ")
    ax.set_xlim(0, 9.4); ax.set_ylim(-0.2, 2.55); f.savefig(OUT / "F5_pile_head_joint.png", dpi=220, bbox_inches="tight"); plt.close(f)


# ------------------------------------------------------------------ F6 floor system prototype
def f6():
    f, ax = fig(3.2)
    x0, y = 0.5, 1.4; L = 3.0
    for i in range(3): beam(ax, x0 + i * L - 0.1, x0 + i * L + 0.1, y - 0.3, 0.3, BEARER)
    beam(ax, x0 - 0.1, x0 + 2 * L + 0.1, y, 0.25, STEEL, "two bays of joists, rim track, OSB deck (ceiling optional)")
    ax.add_patch(Rectangle((x0 - 0.1, y + 0.25), 2 * L + 0.2, 0.07, fc=DECK, ec="none"))
    for i in range(3):
        ax.add_patch(Rectangle((x0 + i * L - 0.07, y - 0.9), 0.14, 0.6, fc="#cccccc", ec=SUP, lw=1)); ax.text(x0 + i * L, y - 1.0, "pile stub or rigid post", ha="center", fontsize=6.5, color=SUP, va="top")
    for xx in [x0 + 0.4 + k * 0.6 for k in range(9)]: ax.add_patch(Rectangle((xx - 0.2, y + 0.32), 0.4, 0.18, fc="#e8d8b0", ec=GREY, lw=0.6))
    ax.text(x0 + L, y + 0.62, "uniform load by sand bags or water tanks, in steps to 1.0, 1.35 and 1.5 × (g + q), then to failure", ha="center", fontsize=7, va="bottom")
    arrow(ax, x0 + L / 2, y + 1.6, y + 0.55); ax.text(x0 + L / 2 + 0.15, y + 1.3, "1 kN point load and heel drop:\nfrequency, damping, δ", color=LOAD, fontsize=7.5, va="center")
    gauge(ax, x0 + L / 2, y - 0.02, "δ"); gauge(ax, x0 + 1.5 * L, y - 0.02, "δ")
    ax.text(x0 + L, y - 1.45, "accelerometers at mid-bay; transducers on the bearers at the pile heads for support settlement", ha="center", fontsize=7, color=GREEN, va="top")
    dim(ax, x0, x0 + L, y + 1.95, "bay 3.0 m"); dim(ax, x0 + L, x0 + 2 * L, y + 1.95, "bay 3.0 m"); ax.text(x0 + 2 * L + 0.4, y + 0.1, "width at least\n4 joist spacings\n(2.4 m at 600 mm)", fontsize=7, color=STEEL, va="center")
    ax.set_xlim(0, 8.8); ax.set_ylim(-0.4, 3.5); f.savefig(OUT / "F6_floor_system.png", dpi=220, bbox_inches="tight"); plt.close(f)


for fn in (f1, f2, f3, f4, f5, f6): fn()
print("figures written to", OUT)
