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

## 7. Framing details, one level deeper (owner: one framing type at a time)

Order set by the owner: roof first. All numbers are first-pass hand estimates,
PRELIMINARY, to make the parts plausible; they are not checks (STATE D-007).

### 7.1 Roof (drafted 2026-11-10, owner has not yet commented)

Load path: standing seam -> purlins -> main frames (grids 2, 3, 4) and gable walls
(grids 1, 5) -> legs and studs -> floor frame -> soil screws. Rafter thrust is closed by
the tie rod at eaves; legs get vertical load only.

| part | concept | first-pass figure |
|---|---|---|
| rafter and leg | 2 × C150×45×1.5 back-to-back with a 6 mm gap, packer plates at about 600 mm; rafter about 3.4 m long | about 5.9 kN/m on plan per frame; M about 5 kNm with N about 17 kN; C150 pair roughly half used |
| tie rod | M16 with turnbuckle at eaves, fork end pinned to the knee gusset | about 9 kN tension (M12 would carry it) |
| knee gusset | 6 mm plate between the webs of leg and rafter, 4 × M12 in each member | bolt bearing in 2 × 1.5 mm webs about 30 kN per bolt; count set by stiffness and layout |
| apex gusset | 6 mm plate between the webs, 4 × M12 per rafter, seat for the ridge purlin | — |
| purlins | C150×45×1.5 at about 850 mm on slope (650 mm on plan), 4 per slope + eaves + ridge; single spans 3.0–3.25 m, butted over each frame on a screwed cleat angle | about 1.2 kN/m vertical per purlin |
| sag straps | one line at mid-bay, eaves purlin over the ridge to the other eaves purlin | down-slope component about 0.8 kN/m per purlin at 40°: weak-axis bending of the C is the governing point of the roof |
| roof bracing | strap X in the plane of both slopes, end bays 1–2 and 4–5 | extent decided by the transverse-stability check (9.25 m between grid 2 and gable 5) |
| skylight | roof window about 780 × 1180 mm: one purlin cut, two trimmers down the slope between the purlins above and below, cut purlin on cleats, sag strap line moved aside | — |

Loads behind the figures: roof dead about 0.65 kN/m² on plan; snow s_k 1.25 kN/m²,
mu_1 0.53 at 40°, s about 0.67 kN/m²; ULS about 1.9 kN/m² on plan; frame tributary
3.125 m.

Base decisions taken by the planner, open to the owner's correction: gap-and-gusset
frame joints; M16 tie rod with turnbuckle; single-span purlins on cleats with one sag
strap line per bay; strap bracing in the roof end bays.

To do in the viewer: close-up scenes for knee + tie-rod end, apex, purlin cleat + sag
strap, skylight trimming; the current viewer still shows the uncut purlin through the
skylight opening.

### 7.2 Ground floor frame (drafted, parked: owner gave no preference; planner's options stand until he comments)

Cross bearers 2 × C200×45×1.5 back-to-back on 3 soil screws (2 × 2.6 m; about
13.5 kN/m, about 11 kNm over the centre screw - a C150 pair does not carry it at
1.5 mm; whether FLINS can roll C200 is an open question). Joist cassettes C150 at
400 mm stacked on top of the bearers (bearing joints, 350 mm total depth), end tracks
U150, web stiffeners at joist ends, bolted saddle plate on each screw head. Centre
screw about 45 kN design compression. Governing: web crippling (a gerinclemez
beroppanása) at the bearer centre support and the joist ends. Open: stacked vs flush,
module 400 / 600, subfloor as diaphragm (board, steel sheet or straps).

### 7.3 Still to do, in this order

Wall panels and openings; loft floor; bracing and hold-downs. Then work breakdown in
hours (4 weeks) and the Hungarian offer letter. End products for FLINS are Hungarian;
working versions stay English (owner, 2026-11-10).
