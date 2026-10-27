# 02 · Options and recommended choices

Each row: the options considered, the pick, and why. Picks are provisional until the
Q&A items marked [CLIENT]/[GEO] are closed.

## Structural data pipeline

| Topic | Options | Pick | Why |
|---|---|---|---|
| Framing rules | invent own · AISI S240/S230 · SCI P402 | **AISI S240 rules, SCI P402 for serviceability** | Decades of use; rules are prescriptive and easy to encode |
| Resistance source | hand calc EN 1993-1-3 only · DSM · GMNIA | **GMNIA (CalculiX) verified via EN 1993-1-14, DSM as benchmark, EN 1993-1-3 cross-check** | Existing proven method; captures deck restraint and web holes that hand methods treat crudely |
| Model factor | γ_FE = 1.0 · calibrated | **Calibrate from a physical test series per mode** | Required for non-standard cases (web holes, unbraced bottom flange) |
| Joints | all FE · all test | **Test-based for screws/clips; FE for pile-head detail** | Screwed joints are cheap to test, expensive to model reliably |
| Table format | per-section PDF tables · dense matrix | **Dense JSON matrix: section × spacing × load class → max span (strength, deflection, vibration) + support reaction** | App does lookups and interpolation, no re-analysis |
| Campaign driver | manual PrePoMax · scripted | **Scripted case matrix → `.inp` → ccx → parser → table**, PrePoMax MCP for review | Reproducible, re-runnable when a section changes |

## Application

| Topic | Options | Pick | Why |
|---|---|---|---|
| Architecture | desktop app · web app · FreeCAD plugin | **Python FastAPI backend + browser UI (same stack as the CFD apps)** | Runs on laptop, own server or hosted without change |
| Deployment | installer · Docker · hosted | **Docker image + single-file launcher; hosted later** | Covers all three client wishes |
| Geometry engine | own · shapely · CAD kernel | **shapely (2D)**; no CAD kernel | A floor layout is 2D polygon work |
| Drawing input | DXF · vector PDF · raster trace | **DXF (ezdxf) first, vector PDF (pymupdf) second, manual trace over image always available** | Permit drawings are heterogeneous |
| Layout generation | fully automatic · assisted | **Automatic first iteration, user edits (joist direction, bearer lines, pile positions)** | Sales staff need a start, engineer needs control |
| Database | local SQLite · central Postgres · JSON catalogues | **Versioned JSON catalogues fetched from a central URL with local cache; project files local** | Simple, updatable, offline-capable |
| AI | none · LLM in load path · LLM assistant | **Claude as assistant (drawing interpretation, proposal text, help), never in the structural path** | Auditability |
| Output | PDF only · DXF · IFC | **PDF proposal + DXF layout + JSON project; IFC later** | What a client and a site team need |
| Licensing of stack | mixed | **All MIT/BSD/GPL-tool-at-arm's-length (CalculiX is GPL but used as an external process)** | No licensing risk for a commercial app |

## Development roadmap (rough)

1. **Catalogue + rules (now)**: section family, build-ups, framing rules, load classes.
2. **Rough app (this repo)**: polygon in → joists/bearers/piles out, BOM, SVG/DXF.
3. **FEA campaign**: joist bending tables, support/crippling tables, bearer tables;
   DSM benchmark; validation plan for the test series.
4. **Tests**: joists + joints + pile head; derive γ_FE; freeze tables v1.
5. **App v1**: DXF/PDF import, editing, proposal PDF, pricing, central catalogue server.
6. **Approvals**: design-basis document, geotechnical acceptance route, ÉMI/NMÉ as needed.
