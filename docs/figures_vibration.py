#!/usr/bin/env python3
"""Figure for FLINS-CFS-005: fundamental frequency versus span for the catalogue joists. Usage: python3 docs/figures_vibration.py OUT_DIR"""
import sys
from pathlib import Path
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
sys.path.insert(0, str(Path(__file__).parent)); import vib_calc as v
from floorframe import catalog

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "figs"); OUT.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8})
L = np.linspace(2.4, 6.0, 60)
f, axs = plt.subplots(1, 2, figsize=(15.5 / 2.54, 2.9), sharey=True)
cols = {"C150-1.5": "#7f8c8d", "C200-1.5": "#2a6ebb", "C250-2.0": "#c0392b", "C300-2.5": "#1e8449"}
for ax, m, title in ((axs[0], 60, "dry build-up, m = 60 kg/m²"), (axs[1], 110, "with gypsum-fibre or dry screed, m = 110 kg/m²")):
    for name, c in cols.items():
        sec = catalog.section(name); ax.plot(L, [v.f1_hz(sec, x, 600, m) for x in L], color=c, lw=1.5, label=f"{name} @ 600 mm")
    ax.axhline(8, color="#d35400", lw=1, ls="--"); ax.text(5.95, 8.3, "8 Hz (EN 1995-1-1 7.3.3)", ha="right", fontsize=6.5, color="#d35400")
    ax.axhline(10, color="#d35400", lw=0.8, ls=":"); ax.text(5.95, 10.3, "10 Hz target (CFS research)", ha="right", fontsize=6.5, color="#d35400")
    ax.set_ylim(0, 30); ax.set_xlim(2.4, 6.0); ax.set_xlabel("span L [m]"); ax.set_title(title, fontsize=8); ax.grid(alpha=0.3)
axs[0].set_ylabel("f1 [Hz]"); axs[0].legend(fontsize=6.5, loc="upper right")
f.tight_layout(); f.savefig(OUT / "F1_frequency_vs_span.png", dpi=220); print("figure written to", OUT)
