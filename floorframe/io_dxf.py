"""DXF import/export with ezdxf. Units: mm (DXF $INSUNITS is read and converted when set)."""
from __future__ import annotations

from pathlib import Path

import ezdxf
from ezdxf import units as ezunits

from .model import Bearer, Joist, Layout, Loads, Pile, Plan, Region

FLOOR_LAYERS = ("FLOOR", "PADLO", "FODEM", "SLAB", "0")


def _scale(doc) -> float:
    u = doc.header.get("$INSUNITS", 0)
    return {ezunits.MM: 1.0, ezunits.CM: 10.0, ezunits.M: 1000.0, ezunits.IN: 25.4}.get(u, 1.0)


def read_plan(path: str | Path, name: str | None = None, loads: Loads | None = None, layer: str | None = None) -> Plan:
    """Closed LWPOLYLINEs on the floor layer (first matching of FLOOR_LAYERS, or `layer`) become regions."""
    doc = ezdxf.readfile(str(path))
    k = _scale(doc)
    msp = doc.modelspace()
    layers = [layer] if layer else list(FLOOR_LAYERS)
    regions: list[Region] = []
    for ly in layers:
        for i, e in enumerate(msp.query(f'LWPOLYLINE[layer=="{ly}"]')):
            if not e.closed:
                continue
            pts = [(float(x) * k, float(y) * k) for x, y, *_ in e.get_points()]
            regions.append(Region(f"{ly}-{i + 1}", pts, loads or Loads()))
        if regions:
            break
    if not regions:
        raise ValueError(f"no closed polyline found on layers {layers}")
    return Plan(name or Path(path).stem, regions)


def write_layout(layout: Layout, path: str | Path, plan: Plan | None = None) -> None:
    doc = ezdxf.new("R2010")
    doc.header["$INSUNITS"] = ezunits.MM
    for ly, color in (("FLOOR", 8), ("JOISTS", 5), ("RIM", 4), ("BEARERS", 1), ("PILES", 3), ("TEXT", 7)):
        doc.layers.add(ly, color=color)
    msp = doc.modelspace()
    if plan:
        for r in plan.regions:
            msp.add_lwpolyline(r.polygon, close=True, dxfattribs={"layer": "FLOOR"})
    for j in layout.joists:
        msp.add_line(j.p1, j.p2, dxfattribs={"layer": "RIM" if j.kind == "rim" else "JOISTS"})
    for b in layout.bearers:
        msp.add_line(b.p1, b.p2, dxfattribs={"layer": "BEARERS", "lineweight": 50})
    for p in layout.piles:
        msp.add_circle((p.x, p.y), 125, dxfattribs={"layer": "PILES"})
        msp.add_text(f"{p.N_ed:.1f} kN", height=60, dxfattribs={"layer": "TEXT"}).set_placement((p.x + 150, p.y + 150))
    for name, r in layout.meta.get("regions", {}).items():
        msp.add_text(f"{name}: {r['joist_section']} @ {r['spacing_mm']} | 2x{r['bearer_section']} | {r['pile']}",
                     height=120, dxfattribs={"layer": "TEXT"}).set_placement((0, -300 - 200 * len(msp.query("TEXT"))))
    doc.saveas(str(path))


def write_sample_house(path: str | Path) -> None:
    """L-shaped single-storey house footprint, mm, on layer FLOOR."""
    doc = ezdxf.new("R2010")
    doc.header["$INSUNITS"] = ezunits.MM
    doc.layers.add("FLOOR")
    doc.modelspace().add_lwpolyline([(0, 0), (12000, 0), (12000, 6000), (7000, 6000), (7000, 9000), (0, 9000)],
                                    close=True, dxfattribs={"layer": "FLOOR"})
    doc.saveas(str(path))
