import math

from shapely.geometry import LineString, Point, Polygon

from floorframe.engine.bom import bill_of_materials
from floorframe.engine.layout import generate_layout
from floorframe.model import Loads, Plan, PointLoad, Region

RECT = [(0, 0), (10000, 0), (10000, 6000), (0, 6000)]
LSHAPE = [(0, 0), (12000, 0), (12000, 6000), (7000, 6000), (7000, 9000), (0, 9000)]


def _plan(poly, **kw):
    return Plan("t", [Region("r", poly, Loads(1.5, 2.0))], **kw)


def test_rectangle_layout_is_consistent():
    lay = generate_layout(_plan(RECT))
    m = lay.meta["regions"]["r"]
    assert m["joist_direction"] == "y"           # joists span the shorter 6 m side
    assert m["bay_mm"] <= m["joist_span_limit_mm"]
    assert m["n_bays"] * m["bay_mm"] == 6000
    assert len(lay.bearers) == m["n_bays"] + 1
    joists = [j for j in lay.joists if j.kind == "joist"]
    s = m["spacing_mm"]
    n_pos = 10000 // s + 1 + (1 if 10000 - (10000 // s) * s > 50 else 0)   # grid positions plus closing edge joist
    assert len(joists) == n_pos * m["n_bays"]
    assert all(abs(j.p1[0] - j.p2[0]) < 1 for j in joists)              # joists parallel to y
    poly = Polygon(RECT).buffer(2)
    for j in lay.joists:
        assert poly.contains(Point(j.p1)) and poly.contains(Point(j.p2))
    assert all(p.N_ed > 0 for p in lay.piles)
    # every pile sits on a bearer line
    ys = {round(b.p1[1]) for b in lay.bearers}
    assert all(round(p.y) in ys for p in lay.piles)
    # pile spacing respected
    for b in lay.bearers:
        on = sorted(p.x for p in lay.piles if round(p.y) == round(b.p1[1]))
        gaps = [b2 - a for a, b2 in zip(on, on[1:])]
        assert max(gaps) <= m["pile_spacing_mm"] + 1


def test_lshape_clips_to_polygon():
    lay = generate_layout(_plan(LSHAPE))
    poly = Polygon(LSHAPE).buffer(2)
    assert sum(1 for j in lay.joists if j.kind == "joist") > 20
    for j in lay.joists:
        assert poly.contains(Point(j.p1)) and poly.contains(Point(j.p2))
    for b in lay.bearers:
        assert poly.contains(Point(b.p1)) and poly.contains(Point(b.p2))
    # the notch (x>7000, y>6000) must be empty of piles
    assert not any(p.x > 7001 and p.y > 6001 for p in lay.piles)


def test_point_load_far_from_piles_is_flagged():
    lay = generate_layout(_plan(RECT, point_loads=[PointLoad(5000, 1700, 4.0, "stove")]))
    assert any(f.level == "warn" and "stove" in f.text for f in lay.flags)


def test_forced_direction_and_pile_choice():
    lay = generate_layout(Plan("t", [Region("r", RECT, Loads(), joist_direction="x")], pile_name="SP89-2500"))
    assert lay.meta["regions"]["r"]["joist_direction"] == "x"
    assert {p.name for p in lay.piles} == {"SP89-2500"}


def test_bom_totals():
    plan = _plan(RECT)
    lay = generate_layout(plan)
    bom = bill_of_materials(lay, plan)
    assert bom["deck_m2"] == 60.0
    assert bom["steel_total_kg"] > 0
    assert sum(p["count"] for p in bom["piles"]) == len(lay.piles)
    assert math.isclose(sum(i["mass_kg"] for i in bom["steel"]), bom["steel_total_kg"], abs_tol=0.5)


USHAPE = [(0, 0), (16000, 0), (16000, 11000), (11000, 11000), (11000, 5000), (5000, 5000), (5000, 11000), (0, 11000)]


def _on_segment(pt, p1, p2, tol=1.0):
    return LineString([p1, p2]).distance(Point(pt)) <= tol


def test_ushape_every_joist_end_is_supported():
    lay = generate_layout(_plan(USHAPE))
    m = lay.meta["regions"]["r"]
    assert m["joist_direction"] == "y"
    assert m["bay_mm"] <= m["joist_span_limit_mm"]
    # a bearer runs along the re-entrant courtyard base
    assert any(abs(b.p1[1] - 5000) < 1 and min(b.p1[0], b.p2[0]) <= 5000 and max(b.p1[0], b.p2[0]) >= 11000
               for b in lay.bearers)
    # every bearer is on piles: piles at both ends, gaps within the pile spacing
    for b in lay.bearers:
        on = sorted(math.hypot(p.x - b.p1[0], p.y - b.p1[1]) for p in lay.piles if _on_segment((p.x, p.y), b.p1, b.p2))
        L = math.hypot(b.p2[0] - b.p1[0], b.p2[1] - b.p1[1])
        assert on and on[0] < 1 and abs(on[-1] - L) < 1
        assert all(c - a <= m["pile_spacing_mm"] + 1 for a, c in zip(on, on[1:]))
    # every joist end lies on a bearer (directly, or under the rim it ends at)
    joists = [j for j in lay.joists if j.kind == "joist"]
    for j in joists:
        assert abs(j.p2[1] - j.p1[1]) <= m["joist_span_limit_mm"] + 1
        for end in (j.p1, j.p2):
            assert any(_on_segment(end, b.p1, b.p2) for b in lay.bearers), end
