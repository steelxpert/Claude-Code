#!/usr/bin/env python3
"""Figure for FLINS-CFS-003: where the AI sits in the workflow. Usage: python3 docs/figures_ai_plan.py OUT_DIR"""
import sys
from pathlib import Path
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "figs"); OUT.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8})
GREY, AI, ENG, HUM = "#777777", "#fde9d9", "#dfe8f3", "#e2f0d9"


def box(ax, x, y, w, h, text, fc, fs=7.0):
    """Rounded box with text shrunk until it fits inside 92 % of the box width and height."""
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08", fc=fc, ec=GREY, lw=1))
    t = ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs)
    r = ax.figure.canvas.get_renderer()
    (bx0, by0), (bx1, by1) = ax.transData.transform([(x, y), (x + w, y + h)])
    while fs > 4.5:
        bb = t.get_window_extent(r)
        if bb.width <= 0.92 * (bx1 - bx0) and bb.height <= 0.92 * (by1 - by0): break
        fs -= 0.2; t.set_fontsize(fs)
    TEXTS.append(t)


def equalize():
    """All box labels of the current figure at the smallest fitted size."""
    if TEXTS:
        fs = min(t.get_fontsize() for t in TEXTS)
        for t in TEXTS: t.set_fontsize(fs)
    TEXTS.clear()


TEXTS = []
def arr(ax, x0, y0, x1, y1, text=None):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=9, color=GREY, lw=1))
    if text: ax.text((x0 + x1) / 2, (y0 + y1) / 2 + 0.08, text, ha="center", fontsize=6.3, color=GREY)


def f1():
    f, ax = plt.subplots(figsize=(15.5 / 2.54, 3.6)); ax.set_aspect("equal"); ax.axis("off")
    W, G = 2.4, 0.5
    xs = [0.1 + i * (W + G) for i in range(5)]
    ax.set_xlim(0, xs[4] + W + 0.1); ax.set_ylim(0, 4.55); f.canvas.draw()
    mids = ["permit drawings\n(PDF, DXF)", "floor outline, walls\nand loads, confirmed\nby the user", "layout engine:\ntables and rules,\nplain code", "layout, bill of\nmaterials, price", "proposal pack with\nsigned design basis"]
    for x, t, c in zip(xs, mids, (HUM, HUM, ENG, ENG, HUM)): box(ax, x, 1.6, W, 1.0, t, c)
    for x in xs[:-1]: arr(ax, x + W, 2.1, x + W + G, 2.1)
    box(ax, xs[0], 3.2, W, 0.85, "A  reads the drawing,\nproposes the outline", AI)
    box(ax, xs[3], 3.2, W, 0.85, "B  explains the result,\ndrafts the proposal text", AI)
    box(ax, xs[4], 3.2, W, 0.85, "C  answers questions\nfrom the design basis", AI)
    arr(ax, xs[0] + W / 2 + 0.6, 3.2, xs[1] + 0.4, 2.6, "proposal only"); arr(ax, xs[3] + W / 2, 2.6, xs[3] + W / 2, 3.2); arr(ax, xs[4] + W / 2, 2.6, xs[4] + W / 2, 3.2)
    box(ax, xs[2], 0.1, W, 0.9, "span tables, joint and\npile catalogues\n(engineer-signed)", ENG); arr(ax, xs[2] + W / 2, 1.0, xs[2] + W / 2, 1.6)
    box(ax, xs[1], 0.1, W, 0.9, "D  developer side:\nFE campaign, code,\nreports", AI); arr(ax, xs[1] + W, 0.55, xs[2], 0.55)
    ax.text(xs[2] + W / 2, 4.35, "AI touch points (orange) sit beside the load path (blue), never in it", ha="center", fontsize=7.5)
    equalize(); f.savefig(OUT / "F1_ai_touchpoints.png", dpi=220, bbox_inches="tight"); plt.close(f)


def f2():
    f, ax = plt.subplots(figsize=(15.5 / 2.54, 2.4)); ax.set_aspect("equal"); ax.axis("off")
    W, G = 2.5, 0.35
    ax.set_xlim(0, 0.2 + 5 * W + 4 * G); ax.set_ylim(-0.8, 1.8); f.canvas.draw()
    steps = ["real project\nsession", "engineer corrects\nthe AI's reading", "correction written into\nthe harness\n(rules, examples)", "added to the test set\n(drawing + confirmed\nresult)", "every change scored\nagainst all\npast projects"]
    for i, t in enumerate(steps):
        x = 0.1 + i * (W + G); box(ax, x, 0.5, W, 1.15, t, AI if i in (0, 2) else HUM)
        if i < 4: arr(ax, x + W, 1.07, x + W + G, 1.07)
    x_last = 0.1 + 4 * (W + G) + W / 2; x_first = 0.1 + W / 2
    ax.add_patch(FancyArrowPatch((x_last, 0.5), (x_first, 0.5), connectionstyle="arc3,rad=-0.25", arrowstyle="-|>", mutation_scale=9, color=GREY, lw=1, ls="--"))
    ax.text((x_last + x_first) / 2, -0.55, "next project", ha="center", fontsize=6.5, color=GREY)
    equalize(); f.savefig(OUT / "F2_harness_loop.png", dpi=220, bbox_inches="tight"); plt.close(f)


f1(); f2(); print("figures written to", OUT)
