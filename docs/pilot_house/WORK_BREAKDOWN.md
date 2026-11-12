# FLINS pilot house - engineering work breakdown (rev 0, 2026-11-12, FLIN-007)

Status: owner-reviewed draft (FLIN-007). Hours only; the fixed price and the end date are the
owner's (O-010). Scope = the house as built in viewer v33 (`concept_viewer.html`, D-017..D-031).
Every figure in the job stays PRELIMINARY (D-007).

| # | Deliverable | h |
|---|---|---|
| 1 | Design basis: site envelope Hungary, materials, profile set, assumptions; project set-up | 6 |
| 2 | 3D framing model (SpaceClaim .scdoc + STEP), house as in viewer v33, one worked detail per joint type | 26 |
| 3 | Actions to EN 1990 / EN 1991 + HU NA: self-weight, imposed (floor, loft, roof), snow (incl. drift at skylight), wind on walls / roof incl. internal pressure; combinations | 8 |
| 4 | Global 3D beam model: build, loads, equilibrium and solver-mass check | 16 |
| 5a | Roof member checks (EN 1993-1-3): panels, purlins, asymmetric track, skylight trimmers, ridge box | 8 |
| 5b | Long walls: studs (axial + wind), wall C glazed bays (king / jack posts, mullions) | 8 |
| 5c | Gables 1 and 5: studs, wind girt, posts / jambs, apex panel | 8 |
| 5d | Loft: joists, grid-2 header, partition posts | 4 |
| 5e | Ground floor: floor panels, joists, rims, 2 x C200 bearers | 8 |
| 5f | Main frames: 2 x C200x2.0 columns / rafters, tie rod, knee and apex | 10 |
| 5g | Bracing and global stability: roof and wall X-straps, hold-down forces, transverse / longitudinal load path, plan torsion | 9 |
| 5h | SLS: deflections, floor vibration | 3 |
| 6 | Connection checks (EN 1993-1-8 / EN 1993-1-3), one per type: frame gussets + packing, column base T on screw, tie-rod ends, hold-downs, girt / post ends, panel to bearer (INCLUDED, owner FLIN-007) | 16 |
| 7 | Soil-screw reaction table for the geotechnics lead (Szecsey Márton) | 3 |
| 8 | Model export STEP + general-arrangement PDF views (format agreed, owner FLIN-007) | 6 |
| 9 | Hungarian report + calculation annex + tervezői nyilatkozat (flins-sdr) | 18 |
| 10 | Coordination: 2 review meetings with FLINS, one revision round | 6 |
| | **Total** | **163 h (about 4 weeks)** |

## Assumptions
- Profiles FLINS rolls today: C / U150x1.5; C200x2.0 (main frames) and C200x2.5 (floor bearers)
  as the agreed exceptions.
- Section resistances by calculation (EN 1993-1-3), not by test: PRELIMINARY until the FLINS
  T-series exists (D-007).
- Site: Hungarian envelope below about 400 m, not one address.
- Covering: light metal standing seam, carries nothing structurally; deck and finishes by others.

## Exclusions
Architecture, building physics, fire and acoustic design; geotechnical design and test loading of
the soil screws (FLINS / Szecsey Márton, O-007); tests; shop drawings and cutting lists; permit
documents; deck and finishes.

## Open
- Member-check software for lines 5a-5h (Consteel or ANSYS; AxisVM for actions + global model):
  owner answers in FLIN-008 after an assessment (O-014). May shift the hours of lines 4-5.
