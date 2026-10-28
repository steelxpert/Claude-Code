"""Layout generator: joists, rim, bearers (sills) and screw piles for each region.

Rough version: a bearer/joist grid on the region's bounding box, clipped to the region
polygon. Every region edge that runs across the joists is a support line and gets a bearer
(on piles); intermediate bearers are spaced evenly between consecutive support lines so
that no joist span exceeds the table span. The choice of joist section, spacing, number of bearer lines, bearer section
and pile type is a brute-force minimum of (steel mass + piles * pile_cost_kg_eq) over
the catalogue, with every candidate checked against the span tables.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from shapely.geometry import LineString, Polygon, MultiLineString

from .. import catalog
from ..model import Bearer, Flag, Joist, Layout, Pile, Plan, Region

EDGE_EPS = 1.0  # mm: lines on the bbox boundary are nudged inward before clipping


@dataclass
class _Candidate:
    joist: catalog.Section
    spacing: int
    line_coords: list[float]
    bay_mm: float
    joist_span_limit_mm: float
    bearer: catalog.Section
    pile: dict
    pile_spacing_mm: float
    cost: float
    steel_kg: float
    n_piles: int


def _clip(line: LineString, poly: Polygon) -> list[LineString]:
    inter = line.intersection(poly)
    if inter.is_empty:
        return []
    if isinstance(inter, LineString):
        return [inter] if inter.length > 1 else []
    if isinstance(inter, MultiLineString):
        return [g for g in inter.geoms if g.length > 1]
    return []


def _line_parallel(axis: str, coord: float, bbox) -> LineString:
    """Line parallel to `axis` ("x" or "y") at `coord` on the other axis, nudged inside the bbox."""
    minx, miny, maxx, maxy = bbox
    if axis == "x":      # parallel to x at y = coord
        c = min(max(coord, miny + EDGE_EPS), maxy - EDGE_EPS)
        return LineString([(minx - 10, c), (maxx + 10, c)])
    c = min(max(coord, minx + EDGE_EPS), maxx - EDGE_EPS)
    return LineString([(c, miny - 10), (c, maxy + 10)])


def _support_coords(poly: Polygon, along: str) -> list[float]:
    """Coordinates (on the joist axis) of every polygon edge that runs across the joists."""
    i = 0 if along == "x" else 1
    ring = list(poly.exterior.coords)
    coords = sorted({round(p1[i], 3) for p1, p2 in zip(ring[:-1], ring[1:]) if abs(p1[i] - p2[i]) < 1e-6})
    return [c for k, c in enumerate(coords) if k == 0 or c - coords[k - 1] > 1]


def _bearer_lines(supports: list[float], lim: float) -> list[float]:
    """Support lines plus evenly spaced intermediate lines so that no bay exceeds `lim`."""
    out = [supports[0]]
    for a, b in zip(supports, supports[1:]):
        n = max(1, math.ceil((b - a) / lim - 1e-9))
        out += [a + (b - a) * k / n for k in range(1, n + 1)]
    return out


def _tribs(lines: list[float]) -> list[float]:
    gaps = [b - a for a, b in zip(lines, lines[1:])]
    return [((gaps[i - 1] if i > 0 else 0.0) + (gaps[i] if i < len(gaps) else 0.0)) / 2 for i in range(len(lines))]


def _bearer_intervals(w_axis: str, c: float, poly: Polygon) -> list[tuple[float, float]]:
    """Extent of the bearer line at `c` within the closed polygon, as merged intervals on the other axis.

    The line is probed just either side of `c`, so lines on the boundary (outer or re-entrant
    edges) pick up the floor on whichever side(s) it lies.
    """
    i = 0 if w_axis == "x" else 1
    minx, miny, maxx, maxy = poly.bounds
    spans = []
    for d in (-EDGE_EPS, EDGE_EPS):
        cc = c + d
        line = (LineString([(minx - 10, cc), (maxx + 10, cc)]) if w_axis == "x"
                else LineString([(cc, miny - 10), (cc, maxy + 10)]))
        for part in _clip(line, poly):
            v = [pt[i] for pt in part.coords]
            spans.append((min(v), max(v)))
    spans.sort()
    merged: list[list[float]] = []
    for lo, hi in spans:
        if merged and lo <= merged[-1][1] + 1:
            merged[-1][1] = max(merged[-1][1], hi)
        else:
            merged.append([lo, hi])
    return [(lo, hi) for lo, hi in merged]


def _pile_spacing(bearer: catalog.Section, trib_mm: float, lc: str, loads, pile: dict) -> float:
    span = catalog.bearer_span(bearer, trib_mm, lc).span_mm
    w_d = (1.35 * loads.g + 1.5 * loads.q) * trib_mm / 1000  # kN/m on the bearer line
    s_cap = pile["R_cd"] / w_d * 1000 if w_d > 0 else span
    return max(min(span, s_cap), 1.0)


def _enumerate(region: Region, supports: list[float], width_mm: float, spacings: list[int], pile_cost: float, pile_name: str | None):
    lc = catalog.load_class_for(region.loads.g, region.loads.q)
    piles = [p for p in catalog.piles() if pile_name is None or p["name"] == pile_name]
    span_mm = supports[-1] - supports[0]
    best: _Candidate | None = None
    for s in spacings:
        n_joists = math.floor(width_mm / s) + 1 + 1  # + closing edge joist
        for js in catalog.sections():
            lim = catalog.joist_span(js, s, lc).span_mm
            lines = _bearer_lines(supports, lim)
            bay = max(b - a for a, b in zip(lines, lines[1:]))
            trib_max = max(_tribs(lines))
            joist_kg = n_joists * span_mm / 1000 * js.mass_kg_m
            rim_kg = 2 * (span_mm + width_mm) / 1000 * js.mass_kg_m
            n_lines = len(lines)
            for bs in catalog.sections():
                bearer_kg = n_lines * width_mm / 1000 * 2 * bs.mass_kg_m
                for p in piles:
                    sp = _pile_spacing(bs, trib_max, lc, region.loads, p)
                    if sp < p["min_spacing_mm"]:
                        continue
                    n_piles = n_lines * (math.ceil(width_mm / sp) + 1)
                    steel = joist_kg + rim_kg + bearer_kg
                    cost = steel + n_piles * pile_cost
                    if best is None or cost < best.cost:
                        best = _Candidate(js, s, lines, bay, lim, bs, p, sp, cost, steel, n_piles)
    if best is None:
        raise ValueError(f"region {region.name}: no catalogue combination satisfies pile minimum spacing")
    return best, lc


def _layout_region(region: Region, plan: Plan, out: Layout) -> None:
    poly = Polygon(region.polygon)
    if not poly.is_valid or poly.area <= 0:
        raise ValueError(f"region {region.name}: invalid polygon")
    minx, miny, maxx, maxy = poly.bounds
    bbox = (minx, miny, maxx, maxy)
    ext_x, ext_y = maxx - minx, maxy - miny
    along = region.joist_direction or ("x" if ext_x <= ext_y else "y")  # joists span the shorter side
    width_mm = ext_y if along == "x" else ext_x
    spacings = plan.allowed_spacings or catalog.spacings()

    supports = _support_coords(poly, along)
    best, lc = _enumerate(region, supports, width_mm, spacings, plan.pile_cost_kg_eq, plan.pile_name)

    # bearer lines: perpendicular to joists, on every cross edge plus intermediate lines between them
    line_coords = best.line_coords
    n_bays = len(line_coords) - 1
    w_axis = "y" if along == "x" else "x"

    # joists
    w0 = miny if along == "x" else minx
    positions = [w0 + k * best.spacing for k in range(math.floor(width_mm / best.spacing) + 1)]
    w_end = w0 + width_mm
    if w_end - positions[-1] > 50:
        positions.append(w_end)
    for pos in positions:
        for i in range(n_bays):
            a, b = line_coords[i], line_coords[i + 1]
            # joists are parallel to `along`; boundary joists are nudged inward for clipping only
            for part in _clip(_line_parallel(along, pos, bbox), poly):
                (x1, y1), (x2, y2) = part.coords[0], part.coords[-1]
                # restrict to this bay
                lo, hi = (a, b)
                if along == "x":
                    x1, x2 = max(x1, lo), min(x2, hi)
                    if x2 - x1 < 1:
                        continue
                    out.joists.append(Joist(best.joist.name, (x1, pos), (x2, pos)))
                else:
                    y1, y2 = max(y1, lo), min(y2, hi)
                    if y2 - y1 < 1:
                        continue
                    out.joists.append(Joist(best.joist.name, (pos, y1), (pos, y2)))

    # rim track along the perimeter
    ring = list(poly.exterior.coords)
    for p1, p2 in zip(ring[:-1], ring[1:]):
        out.joists.append(Joist(best.joist.name, tuple(p1), tuple(p2), kind="rim"))

    # bearers and piles
    w_d_unit = (1.35 * region.loads.g + 1.5 * region.loads.q) / 1000  # kN per mm2 *1000 -> kN/(m*mm)
    for c, trib in zip(line_coords, _tribs(line_coords)):
        for lo, hi in _bearer_intervals(w_axis, c, poly):  # bearers run perpendicular to the joists
            if along == "x":
                x1 = x2 = c
                y1, y2 = lo, hi
            else:
                y1 = y2 = c
                x1, x2 = lo, hi
            out.bearers.append(Bearer(best.bearer.name, (x1, y1), (x2, y2), trib))
            L = math.hypot(x2 - x1, y2 - y1)
            n = math.ceil(L / best.pile_spacing_mm) + 1
            w_line = w_d_unit * trib  # kN/m
            for k in range(n):
                f = k / (n - 1) if n > 1 else 0.5
                px, py = x1 + f * (x2 - x1), y1 + f * (y2 - y1)
                trib_len = (L / (n - 1)) * (0.5 if k in (0, n - 1) else 1.0) if n > 1 else L
                out.piles.append(Pile(best.pile["name"], px, py, round(w_line * trib_len / 1000, 2)))

    util = best.bay_mm / best.joist_span_limit_mm
    out.meta["regions"][region.name] = {
        "load_class": lc, "joist_direction": along, "joist_section": best.joist.name,
        "spacing_mm": best.spacing, "n_bays": n_bays, "bay_mm": round(best.bay_mm),
        "joist_span_limit_mm": round(best.joist_span_limit_mm), "joist_utilisation": round(util, 2),
        "bearer_section": f"2x{best.bearer.name}", "pile": best.pile["name"],
        "pile_spacing_mm": round(best.pile_spacing_mm), "steel_kg": round(best.steel_kg), "piles": best.n_piles,
        "table_source": catalog.joist_span(best.joist, best.spacing, lc).source,
    }
    out.flags.append(Flag("info", f"{region.name}: {best.joist.name} @ {best.spacing} mm, {n_bays} bay(s) of up to {best.bay_mm:.0f} mm "
                                  f"(util. {util:.2f}), bearers 2x{best.bearer.name}, piles {best.pile['name']} @ {best.pile_spacing_mm:.0f} mm"))


def generate_layout(plan: Plan) -> Layout:
    out = Layout(plan.name, [], [], [], [], {"regions": {}, "version": "rough-0.0.1"})
    for region in plan.regions:
        _layout_region(region, plan, out)
    # point loads: need a pile (or a stiffened joist/bearer) nearby
    for pl in plan.point_loads:
        d = min((math.hypot(p.x - pl.x, p.y - pl.y) for p in out.piles), default=math.inf)
        if d > 300:
            out.flags.append(Flag("warn", f"point load {pl.P} kN '{pl.label}' at ({pl.x:.0f},{pl.y:.0f}) is {d:.0f} mm from the nearest pile: "
                                          "add a pile or check the joist/bearer for the concentrated load", (pl.x, pl.y)))
    for name, r in out.meta["regions"].items():
        if r["table_source"] == "PLACEHOLDER":
            out.flags.append(Flag("warn", f"{name}: span table is a PLACEHOLDER (not GMNIA/EC-verified); for internal development only"))
    return out
