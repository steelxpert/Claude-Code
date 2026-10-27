# floorframe

Cold-formed steel floor framing on screw piles for residential houses: development
notes and a rough first version of the design/proposal tool (FlexInSheet Kft. project).

- `docs/01-qa-feasibility.md` — Q&A pass on the brainstorming note, with open items.
- `docs/02-options-and-decisions.md` — options considered and recommended choices.
- `docs/03-rough-app-spec.md` — what the code in this repo does and its limits.
- `floorframe/` — Python package: catalogues, layout engine, DXF/SVG I/O, FEA campaign
  bookkeeping, FastAPI backend and browser UI.
- `examples/sample_house.dxf` — L-shaped demo footprint; `examples/sample_house_layout.svg`
  is the generated layout.

```
pip install -e .[dev]
pytest
uvicorn floorframe.api:app --reload          # http://127.0.0.1:8000
python -m floorframe.cli examples/sample_house.dxf --out out/
```

All span tables in this version are placeholders; see the docs for the GMNIA/Eurocode
pipeline that replaces them.
