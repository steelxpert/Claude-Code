# FLINS pilot house — design brief (rev 0, 2026-11-10)

Status: owner Q&A closed in session FLIN-003. FLINS has not ordered yet; they wait for the
offer (STATE O-010). Every member size below is a CONCEPT assumption, not a verified
resistance (STATE D-007).

## 1. Object

Single-storey barn-house weekend cottage with a sleeping loft, CFS framing on soil screws
(csavarcölöp). Purpose: one house that shows every framing detail type, as the basis of
FLINS in-house discussion. No architect at this stage: only architecture that changes the
framing is fixed here.

Reference for size and layout: a Danish barn-house design supplied by the owner as
screenshots (plan, four elevations, one interior photo). Used for geometry only; our model
is redrawn, their sheets are not reused.

## 2. Geometry

| item | value | source |
|---|---|---|
| grid, length | 1–5: 3250 + 3000 + 3000 + 3250 = 12 500 mm | reference plan |
| grid, width | A–B: 5200 mm | reference plan |
| outside size | 12 740 × 5440 mm | reference plan |
| roof | symmetric gable, about 40°, no overhang | scaled from the elevation |
| eaves / ridge above floor | about 2.6 m / about 4.8 m | scaled; to be fixed in the model |
| wall A (rear) | closed, one door in bay 1–2 | reference |
| wall B (front) | glazed from grid 2 to about 11.0 m, mullions at about 1.55 m | reference |
| gable 1 | closed, one window about 1 × 1 m | reference |
| gable 5 | one window about 1.5 × 1.5 m, off-centre | reference |
| loft (added) | over bay 1–2, 3.25 × 5.2 m, sleeping loft, ladder | owner |
| skylight (added) | one, rear slope over the living room, between frames | owner |

## 3. Structural concept (owner decisions)

| topic | decision |
|---|---|
| main frames | grids 2, 3, 4: CFS built-up back-to-back C rafters and legs, hot-rolled steel tie rod at eaves level |
| roof between frames | purlins frame to frame (3.0–3.25 m), metal standing seam on top |
| loft floor | joists lengthwise, gable 1 to a built-up header on grid 2 (span 3.25 m); header on hidden jambs in the kitchen partition |
| ground floor | cross bearers on grids 1–5, each on 3 soil screws (A, centre, B) = 15 screws; joists lengthwise, span 3.0–3.25 m |
| walls | factory panels (studs + tracks); external walls load-bearing, internal partitions not |
| bracing | flat-strap X-bracing with hold-downs; cladding carries nothing |
| profiles | what FLINS rolls today: C150×45×1.5 (lip 10) studs / purlins / joists, U150×45 tracks; deeper sections allowed where needed; nothing thicker than 1.5 mm for now |
| fasteners | self-drilling screws and rivets / clinching in the panels; bolts only at primary joints (frame knee, apex, tie-rod ends, hold-downs, soil-screw heads) |
| site | envelope for Hungary (HU National Annex snow and wind, below about 400 m) |
| covering | metal standing seam on roof and walls (light; wind uplift matters) |

## 4. Points the design must resolve (planner's notes)

1. Transverse stability. A tied rafter pair on two pin-ended legs has no sway stiffness of
   its own. Wind across the house must go through roof-plane strap bracing to gable 1,
   gable 5 and the grid-2 wall, or the knees must be semi-rigid. Roof bracing is the base
   assumption; knee stiffness is the check.
2. Wall B has bracing length only in bay 1–2 and the 1.5 m return at grid 5; the roof
   diaphragm must carry the rest to wall A. Torsion of the plan to be checked.
3. Cross bearers: two spans of 2.6 m with about 3.1 m of floor each side. A single or
   paired C150×1.5 is probably short at the centre support; expect a deeper pair here
   (first place where "deeper section" is used).
4. 1.5 mm limit: bolt bearing and web crippling at the frame joints and bearer supports
   govern before bending does. Gussets, doublers or bearing stiffeners per the
   cfs-load-introduction method.
5. Uplift: light roof, light house. Hold-downs and soil-screw tension resistance may
   govern the screw size (geotechnics, O-007).
6. Loft header on hidden jambs: point loads into the ground-floor bearer at grid 2.

## 5. Deliverables of the job (for the offer)

- 3D model at framing level in ANSYS SpaceClaim (native .scdoc + STEP): every member at
  its real size and position, one worked detail per joint type.
- Calculation: one global 3D beam model for forces and deflections, member checks to
  EN 1993-1-3, joint checks to EN 1993-1-8, actions to EN 1990 / EN 1991 with the HU NA;
  soil-screw reactions tabulated for the geotechnics lead.
- Duration: about 4 weeks.
- Not included: architecture, building physics, fire and acoustic design, geotechnical
  design of the screws, shop drawings and cutting lists, tests, permit documents.

## 6. Attachment for the offer

`concept_viewer.html` — interactive 3D framing concept (schematic sizes, marked CONCEPT).
