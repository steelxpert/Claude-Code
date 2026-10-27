"""CLI: python -m floorframe.cli plan.dxf --out out/  (or --sample to generate the example DXF)"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import io_dxf
from .engine.bom import bill_of_materials
from .engine.layout import generate_layout
from .model import Loads
from .render import layout_svg


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("dxf", nargs="?")
    ap.add_argument("--out", default="out")
    ap.add_argument("--g", type=float, default=1.5)
    ap.add_argument("--q", type=float, default=2.0)
    ap.add_argument("--sample", help="write a sample house DXF to this path and exit")
    a = ap.parse_args(argv)
    if a.sample:
        io_dxf.write_sample_house(a.sample)
        print("wrote", a.sample)
        return 0
    if not a.dxf:
        ap.error("dxf path required")
    plan = io_dxf.read_plan(a.dxf, loads=Loads(a.g, a.q))
    layout = generate_layout(plan)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "layout.json").write_text(json.dumps(layout.to_dict(), indent=1), encoding="utf-8")
    (out / "bom.json").write_text(json.dumps(bill_of_materials(layout, plan), indent=1), encoding="utf-8")
    (out / "layout.svg").write_text(layout_svg(layout, plan), encoding="utf-8")
    io_dxf.write_layout(layout, out / "layout.dxf", plan)
    for f in layout.flags:
        print(f"[{f.level}] {f.text}")
    print("wrote", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
