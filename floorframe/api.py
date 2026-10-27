"""FastAPI backend. Run: uvicorn floorframe.api:app --reload"""
from __future__ import annotations

import tempfile
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from . import catalog, io_dxf
from .engine.bom import bill_of_materials
from .engine.layout import generate_layout
from .model import Loads, Plan, PointLoad, Region
from .render import layout_svg

app = FastAPI(title="floorframe", version="0.0.1")
WEB = Path(__file__).parent / "web" / "index.html"


class LoadsIn(BaseModel):
    g: float = 1.5
    q: float = 2.0


class RegionIn(BaseModel):
    name: str = "floor"
    polygon: list[tuple[float, float]]
    loads: LoadsIn = Field(default_factory=LoadsIn)
    joist_direction: str | None = None


class PointLoadIn(BaseModel):
    x: float
    y: float
    P: float
    label: str = ""


class PlanIn(BaseModel):
    name: str = "project"
    regions: list[RegionIn]
    point_loads: list[PointLoadIn] = []
    pile_name: str | None = None
    allowed_spacings: list[int] | None = None
    pile_cost_kg_eq: float = 60.0


def _to_plan(p: PlanIn) -> Plan:
    return Plan(p.name, [Region(r.name, [tuple(pt) for pt in r.polygon], Loads(r.loads.g, r.loads.q), r.joist_direction) for r in p.regions],
                [PointLoad(**pl.model_dump()) for pl in p.point_loads], p.pile_name, p.allowed_spacings, p.pile_cost_kg_eq)


def _run(plan: Plan) -> dict:
    try:
        layout = generate_layout(plan)
    except ValueError as e:
        raise HTTPException(422, str(e))
    return {"layout": layout.to_dict(), "bom": bill_of_materials(layout, plan), "svg": layout_svg(layout, plan)}


@app.get("/", response_class=HTMLResponse)
def index():
    return WEB.read_text(encoding="utf-8")


@app.get("/api/catalog")
def get_catalog():
    return {"sections": [s.__dict__ | {"mass_kg_m": round(s.mass_kg_m, 2)} for s in catalog.sections()],
            "spacings_mm": catalog.spacings(), "load_classes": catalog.load_classes(), "piles": catalog.piles()}


@app.post("/api/layout")
def post_layout(plan: PlanIn):
    return _run(_to_plan(plan))


@app.post("/api/layout/dxf")
async def post_layout_dxf(file: UploadFile = File(...), g: float = Form(1.5), q: float = Form(2.0), layer: str | None = Form(None)):
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "in.dxf"
        p.write_bytes(await file.read())
        try:
            plan = io_dxf.read_plan(p, loads=Loads(g, q), layer=layer or None)
        except Exception as e:  # ezdxf errors, no polyline
            raise HTTPException(422, f"DXF import failed: {e}")
    return _run(plan)
