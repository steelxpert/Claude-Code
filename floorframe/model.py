"""Data model of a floor-framing project (rough version)."""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any

Point = tuple[float, float]


@dataclass
class Loads:
    g: float = 1.5   # permanent incl. finishes, kN/m2 (joist self-weight is small, included)
    q: float = 2.0   # imposed, kN/m2 (EN 1991-1-1 cat. A, HU NA)


@dataclass
class PointLoad:
    x: float
    y: float
    P: float  # kN, characteristic
    label: str = ""


@dataclass
class Region:
    name: str
    polygon: list[Point]          # mm, closed implicitly
    loads: Loads = field(default_factory=Loads)
    joist_direction: str | None = None  # "x" | "y" | None = auto


@dataclass
class Plan:
    name: str
    regions: list[Region]
    point_loads: list[PointLoad] = field(default_factory=list)
    pile_name: str | None = None        # from piles.json; None = cheapest adequate
    allowed_spacings: list[int] | None = None
    pile_cost_kg_eq: float = 60.0       # cost of one installed pile expressed in kg of steel equivalent


@dataclass
class Joist:
    section: str
    p1: Point
    p2: Point
    kind: str = "joist"   # joist | rim


@dataclass
class Bearer:
    section: str          # back-to-back pair of this C
    p1: Point
    p2: Point
    trib_width_mm: float


@dataclass
class Pile:
    name: str
    x: float
    y: float
    N_ed: float           # kN, design reaction


@dataclass
class Flag:
    level: str            # info | warn | error
    text: str
    at: Point | None = None


@dataclass
class Layout:
    plan_name: str
    joists: list[Joist]
    bearers: list[Bearer]
    piles: list[Pile]
    flags: list[Flag]
    meta: dict[str, Any]

    def to_dict(self) -> dict:
        return asdict(self)
