"""Catalogues: sections, steel, load classes, piles and (placeholder) load tables.

The load tables returned by `span_table()` are PLACEHOLDERS computed from gross
thin-walled section properties with flat effective-section reductions. They exist so
the layout engine can run end to end; they are to be replaced by the GMNIA-derived
`load_tables.json` produced by `floorframe.fea.campaign` once the campaign and the
EN 1993-1-14 model-factor calibration are done.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

_HERE = Path(__file__).parent


@lru_cache
def _raw(name: str) -> dict:
    return json.loads((_HERE / name).read_text(encoding="utf-8"))


@dataclass(frozen=True)
class Section:
    name: str
    h: float  # depth, mm
    b: float  # flange, mm
    c: float  # lip, mm
    t: float  # thickness, mm

    @property
    def area_mm2(self) -> float:
        return self.t * (self.h + 2 * self.b + 2 * self.c)

    @property
    def I_mm4(self) -> float:
        """Gross second moment of area about the strong axis (centreline model)."""
        t, h, b, c = self.t, self.h, self.b, self.c
        web = t * h**3 / 12
        flanges = 2 * (b * t * (h / 2) ** 2)
        lips = 2 * (t * c**3 / 12 + c * t * (h / 2 - c / 2) ** 2)
        return web + flanges + lips

    @property
    def W_mm3(self) -> float:
        return self.I_mm4 / (self.h / 2)

    @property
    def mass_kg_m(self) -> float:
        return self.area_mm2 * 1e-6 * _raw("sections.json")["steel"]["density_kg_m3"]


def steel() -> dict:
    return _raw("sections.json")["steel"]


def sections() -> list[Section]:
    return [Section(**s) for s in _raw("sections.json")["sections"]]


def section(name: str) -> Section:
    for s in sections():
        if s.name == name:
            return s
    raise KeyError(name)


def spacings() -> list[int]:
    return list(_raw("sections.json")["spacings_mm"])


def load_classes() -> dict[str, dict]:
    return {k: v for k, v in _raw("sections.json")["load_classes"].items() if not k.startswith("_")}


def load_class_for(g: float, q: float) -> str:
    """Smallest catalogue class whose g and q both envelope the demand."""
    for name, lc in sorted(load_classes().items(), key=lambda kv: kv[1]["g"] + kv[1]["q"]):
        if lc["g"] >= g - 1e-9 and lc["q"] >= q - 1e-9:
            return name
    raise ValueError(f"load g={g}, q={q} exceeds catalogue load classes")


def piles() -> list[dict]:
    return list(_raw("piles.json")["piles"])


@dataclass(frozen=True)
class SpanEntry:
    section: str
    spacing_mm: float      # tributary width (joist spacing, or bearer tributary width)
    load_class: str
    span_strength_mm: float
    span_deflection_mm: float
    source: str

    @property
    def span_mm(self) -> float:
        return min(self.span_strength_mm, self.span_deflection_mm)


def _placeholder_span(sec: Section, trib_mm: float, g: float, q: float, n_sections: int = 1) -> SpanEntry:
    """Simply supported span limited by placeholder bending resistance and deflection.

    n_sections = 2 models a back-to-back pair used as a bearer.
    """
    st = _raw("sections.json")
    eff = st["placeholder_effective_factors"]
    sls = st["serviceability"]
    fy, E = steel()["fy"], steel()["E"]
    w_uls = (1.35 * g + 1.5 * q) * trib_mm / 1000  # kN/m
    w_sls = (g + q) * trib_mm / 1000
    M_rd = n_sections * eff["W_eff"] * sec.W_mm3 * fy / steel()["gamma_M0"] / 1e6  # kNm
    EI = n_sections * eff["I_eff"] * E * sec.I_mm4 / 1e6  # kN m2  (N/mm2 * mm4 = N mm2 -> *1e-6 kN m2 ... see below)
    # units: E [N/mm2] * I [mm4] = N mm2 ; /1e6 -> N m2 ; /1e3 -> kN m2
    EI = EI / 1e3
    L_strength = math.sqrt(8 * M_rd / w_uls)  # m
    # 5 w L^4 / (384 EI) <= L/ratio  ->  L^3 <= 384 EI / (5 w ratio)
    L_ratio = (384 * EI / (5 * w_sls * sls["deflection_total_ratio"])) ** (1 / 3)
    # and <= 15 mm absolute: 5 w L^4/(384 EI) <= 0.015
    L_abs = (384 * EI * sls["deflection_total_max_mm"] / 1000 / (5 * w_sls)) ** 0.25
    return SpanEntry(sec.name, trib_mm, load_class_for(g, q), 1000 * L_strength, 1000 * min(L_ratio, L_abs), "PLACEHOLDER")


def joist_span(sec: Section, spacing_mm: float, load_class: str) -> SpanEntry:
    lc = load_classes()[load_class]
    gm = _gmnia_table()
    key = (sec.name, int(spacing_mm), load_class)
    if key in gm:
        return gm[key]
    return _placeholder_span(sec, spacing_mm, lc["g"], lc["q"])


def bearer_span(sec: Section, trib_width_mm: float, load_class: str) -> SpanEntry:
    """Back-to-back pair of `sec` carrying a tributary floor strip of width trib_width_mm."""
    lc = load_classes()[load_class]
    return _placeholder_span(sec, trib_width_mm, lc["g"], lc["q"], n_sections=2)


@lru_cache
def _gmnia_table() -> dict[tuple, SpanEntry]:
    """GMNIA-derived joist table if present (written by floorframe.fea.campaign)."""
    p = _HERE / "load_tables.json"
    if not p.exists():
        return {}
    out = {}
    for row in json.loads(p.read_text(encoding="utf-8"))["joists"]:
        e = SpanEntry(row["section"], row["spacing_mm"], row["load_class"],
                      row["span_strength_mm"], row["span_deflection_mm"], row.get("source", "GMNIA"))
        out[(e.section, int(e.spacing_mm), e.load_class)] = e
    return out
