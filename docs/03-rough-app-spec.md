# 03 · Rough app: what is in this repository

Package `floorframe` — a first, runnable iteration of the layout engine with a minimal
web UI. Everything structural in it is a **placeholder** until the GMNIA tables exist;
the placeholder tables are computed from gross section properties with a flat
effective-section reduction and are labelled `source: "PLACEHOLDER"` in the data.

## Flow

```
DXF / PDF trace / rectangle  ──►  Plan (regions, loads, pile capacity)
                                     │
                                     ▼
                      engine.layout.generate_layout()
      ┌──────────────┬───────────────┼───────────────┬──────────────┐
      ▼              ▼               ▼               ▼              ▼
  joist direction  section &      bearer lines    pile spacing     BOM
  (shorter span)   spacing from   so that span    from bearer      & mass
                   load table     ≤ table span    table and P_d
                                     │
                                     ▼
                      Layout ──► SVG (web) · DXF (ezdxf) · JSON
```

## Modules

- `floorframe/catalog/sections.json` — lipped-C family (depth, flange, lip, t, fy).
- `floorframe/catalog/__init__.py` — section properties (thin-walled), placeholder
  load tables, loaders for the future GMNIA-derived `load_tables.json`.
- `floorframe/model.py` — dataclasses: `Region`, `Loads`, `Plan`, `Joist`, `Bearer`,
  `Pile`, `Layout`.
- `floorframe/engine/layout.py` — the layout generator (joists, rim, bearers, piles).
- `floorframe/engine/bom.py` — bill of materials and mass.
- `floorframe/io_dxf.py` — DXF import (closed polylines on a layer) and export.
- `floorframe/render.py` — SVG rendering.
- `floorframe/fea/campaign.py` — parametric case matrix for the GMNIA campaign and
  the result → load-table conversion (R_d = R_GMNIA / (γ_FE·γ_M1)). Building and
  solving the `.inp` is delegated to the existing CalculiX/PrePoMax tooling.
- `floorframe/api.py` — FastAPI app: `POST /api/layout`, `POST /api/layout/dxf`,
  `GET /` serves `floorframe/web/index.html`.
- `tests/` — pytest coverage of the engine and API.

## Run

```
pip install -e .
uvicorn floorframe.api:app --reload      # open http://127.0.0.1:8000
python -m floorframe.cli examples/sample_house.dxf --out out/
pytest
```

## Known limits of this iteration

- Rectangular bounding-box joist/bearer grid clipped to the region polygon; L-shaped
  floors work but are not optimised per wing.
- Simple spans only (no continuity over bearers), no openings (stairs), no point-load
  redistribution — point loads only trigger a pile/stiffener flag.
- Pile capacity is a single design value; the geotechnical catalogue is a stub.
- No pricing, no proposal PDF, no PDF import yet.
