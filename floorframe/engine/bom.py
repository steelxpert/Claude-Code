"""Bill of materials from a Layout."""
from __future__ import annotations

import math
from collections import defaultdict

from shapely.geometry import Polygon

from .. import catalog
from ..model import Layout, Plan


def _len(p1, p2) -> float:
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def bill_of_materials(layout: Layout, plan: Plan | None = None) -> dict:
    rows = defaultdict(lambda: {"count": 0, "length_m": 0.0, "mass_kg": 0.0})
    for j in layout.joists:
        k = ("rim track" if j.kind == "rim" else "joist", j.section)
        L = _len(j.p1, j.p2) / 1000
        rows[k]["count"] += 1
        rows[k]["length_m"] += L
        rows[k]["mass_kg"] += L * catalog.section(j.section).mass_kg_m
    for b in layout.bearers:
        k = ("bearer (2x)", b.section)
        L = _len(b.p1, b.p2) / 1000
        rows[k]["count"] += 1
        rows[k]["length_m"] += L
        rows[k]["mass_kg"] += 2 * L * catalog.section(b.section).mass_kg_m
    piles = defaultdict(int)
    for p in layout.piles:
        piles[p.name] += 1
    deck_m2 = sum(Polygon(r.polygon).area for r in plan.regions) / 1e6 if plan else None
    items = [{"item": k[0], "section": k[1], "count": v["count"], "length_m": round(v["length_m"], 1), "mass_kg": round(v["mass_kg"], 1)}
             for k, v in sorted(rows.items())]
    return {
        "steel": items,
        "steel_total_kg": round(sum(v["mass_kg"] for v in rows.values()), 1),
        "piles": [{"pile": k, "count": v, "N_ed_max_kN": max(p.N_ed for p in layout.piles if p.name == k)} for k, v in sorted(piles.items())],
        "deck_m2": round(deck_m2, 1) if deck_m2 is not None else None,
    }
