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

### 7.1 Roof - FIRST DRAFT, SUPERSEDED by 7.4 (kept for the record)

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

### 7.4 Roof - FINAL concept (owner instructions, 2026-11-11; shown in concept_viewer.html)

Scope rule (owner): FLINS delivers the bare steel skeleton. Deck, covering and finishes
are by others and are NOT relied on structurally. Figures are PRELIMINARY (STATE D-007).

| item | decision |
|---|---|
| panels | 8 factory roof panels, one per bay and slope, sitting ON TOP of the frame rafters; 6 mm gap between panels at each frame |
| purlins | C150x45x1.5 along the house, span = frame spacing, at about 556 mm on the slope (last spacing at the ridge about 630 mm), ending in the panel tracks like studs |
| tracks | asymmetric U: upper flange 45, lower flange 70 lying on the rafter top; SDS to the rafter at 600 mm; about 5 kN sliding per track line, about 0.8 kN per screw against about 4.6 kN. New section for FLINS (open) |
| frame rafters and legs | 2 x C150 back-to-back, 6 mm gap, gussets between the webs and kept below the rafter top; M16 tie rod at eaves |
| blocking + bridging | one row at mid-bay per panel: solid C150 block in the first and last purlin space, 50 x 1.5 straps on both faces, ending straight on the ridge-edge member |
| skylight | rear slope, bay 3-4, opening 780 x 1600: two boxed jambs (C150 + U150 cap) parallel to the purlins, full panel length, each midway between two purlin lines (s = 0.860 and 2.525 m from the eave); head and sill = one U150 track each down the slope; three cut purlins = six cripples ending in the head/sill tracks; jamb cap stopped 50 mm short at the ends; two bridging rows on the head/sill lines; no diagonal straps in this panel |
| ridge | closed RIDGE BOX: panels extended to the ridge so the lower corners of the two ridge-edge members meet; folded cap on the top flanges; folded inner angle (45 mm legs) under the bottom flanges, stopping at each frame; ridge blocking plate (kite plate, 50 mm bent edge on all four sides for SDS) at every bridging row: 6 plates, three of them in bay 3-4. Carries the vertical resultant of the down-slope load, about 8 kN per bay, about 6.5 kNm against an estimated 9-10 kNm |
| diagonal straps | roof-panel X-straps only in the two gable-end bays (4 panels) |

Open for the calculation: wind on the long walls must reach the gables through the frames
and the ridge box (no diagonals in the middle bays); ends of the ridge-edge members at the
tracks about 4 kN, near the web crippling limit, may need a clip; eave framing still to be
detailed.

Owner's working rules for this thread: one item at a time (instruction -> comment ->
approval -> implement -> check -> next); every sketch as an assembly view and an exploded
view; few words, judge by pictures; end products Hungarian, working versions English.

Grid naming (owner, 2026-11-11): cross grids A (rear wall, door, Z=0), B (centre line, middle soil screws), C (front wall, glazed). Earlier text in this brief that says "wall B" for the glazed front means wall C.

Web perforations (owner, 2026-11-11, approved): slotted holes 38 x 100 mm at 600 mm c/c in the webs of wall studs and roof purlins (incl. ridge-edge members and skylight cripples), first slot 300 mm from the stud bottom / purlin end, none within 250 mm of a member end. Not in tracks, frame members, mullions; floor and loft joists to be decided with the floors. Open: confirm size and end distance against shear and web crippling.

Eave contact (owner, 2026-11-11, approved): long walls A and C are 150 mm thick, centred on the grid. The lowest edge of the roof panel eave-edge purlin meets the INNER top edge of the wall top track (3 mm clearance). Roof panels start 161 mm up the slope from the eaves work point (first purlin spacing about 400 mm); top of wall = eaves work point + 158 mm; wall panel height about 2760 mm above the floor frame (eaves level 2.6 m was scaled from the reference and may be tuned to a round panel height). Wall top track interrupted at each main frame. Open: eave closure over the wall top, fixings.

Eave box (owner, 2026-11-11): folded eave cap on the outside (roof panel top plane + wall outer face, one bend where the planes meet; approved) and folded inner angle on the inside (45 mm legs: eave-edge purlin bottom flange to the inner flange of the wall top track; bay by bay, stops at the frames; drawn, owner check pending). No blocking plates at the eave (owner). Open: eccentric bearing on the wall top, 75 mm off the wall centre line.

Long wall panels (owner, 2026-11-11, approved): walls A and C are shop panels, one per bay like the roof panels, 6 mm gap at grids 2, 3, 4; ONE end stud per panel end, web on the panel end, so neighbouring panels stand back-to-back like the roof tracks; these back-to-back end studs act as the frame leg (separate legs removed); top and bottom tracks run the full panel length and cover the end studs; studs at 600 with slotted webs; two rows of lateral bracing (solid slotted C-blocks in the first and last stud space + 50 x 1.5 straps on both faces) at about 0.92 and 1.84 m. Wall A: second diagonal of the X beside the door (bay 2-3) deleted by the owner. Glazed bays of wall C: separate item, not decided. Open: knee joint (rafter foot to stop at the wall inside face, gusset in the 6 mm gap between the end studs).

Door (owner, 2026-11-11, approved): boxed header = two perforated C150 studs lying along the wall, webs on the wall faces, toes facing, seated in a U150 bottom track with its open side UP; a U150 top track of the same rotation on top holds the cripple stud; jamb studs are C150 capped with a U150 track (box), web toward the opening. Wall A bracing: the X-bracing in bay 2-3 beside the door is deleted completely (owner); wall A keeps one X in bay 4-5. Open for the calculation: longitudinal bracing of wall A with one braced bay.
Door threshold (owner): the panel bottom track runs through the door opening and is cut out on site after erection.

Gable 5 (owner, 2026-11-12, approved as FIRST APPROXIMATION, published as viewer v19): two shop panels with a HORIZONTAL panel joint on the eave line (top of wall, EV + 158 mm); not a vertical split. Lower "wall panel" 5.05 x 2.76 m between the long walls (the last long-wall panels and the end roof panels, eave cap and ridge cap run to the gable's OUTER face, x = 12.575); studs at 600, two bridging rows at 0.92 / 1.84 m. Upper "apex panel": bottom track on the lower top track, raking U150 tracks with their top face in the rafter-top plane so the end roof panels bear on them, studs on the 600 module plus a ridge stud, one bridging row 0.92 m above the joint. Window 1.5 x 1.5 (z 3.0-4.5, sill 0.4 m above the floor frame) framed as the door: boxed header in rotated U150 tracks, capped box jambs full height, U150 sill track open side down, cripples above and below. X-straps from the wall A corner to the window jamb, full height of the lower panel; none in the apex panel. Terminology: "panel joint" / track-to-track connection, not "splice" (EN 1993-1-8 6.2.7 reserves splice for one member). OPEN (owner to instruct): hidden header in the apex top track (gable studs are not aligned with the roof panels), corner where the raking track meets the bottom track (3 mm of room; drawn starting 75 mm in), hold-downs, apex-panel bracing, gable 1 mirror.

Gable 5 apex panel (owner, 2026-11-12, accepted "for now", published as viewer v20): raking top build-up under the roof panel, top to bottom, perpendicular to the slope: (1) U150 cap track open side down, top face in the rafter-top plane, the end roof-panel tracks lie on it; (2) a C150 stud lying along the rake inside it, web down, lips up, nesting into a capped box = the weak-axis header (the roof-panel tracks and the gable studs are on different modules); (3) the normal raking U150 top track of the gable, the studs end in it. Stack about 95 mm perpendicular; studs end about 60 mm (vertical) below the roof plane. Both sides meet at the ridge. Studs uniformly at 600 (0.6 to 4.8 m), eight studs, NO ridge stud, no crowding anywhere. Corner: each stack member runs down the slope on its own until its lowest square-cut edge is about 3 mm above the web of the apex bottom track (cap track and header C end 0.12 m from the long wall's inner face, raking track 0.16 m); the apex bottom track runs the full 5.05 m. Bridging row 0.92 m above the joint: straps on both faces run from stack to stack and are screwed to it; one solid block at each end between the last stud and the stack (1.8 m rear, 3.6 m front). Terminology: horizontal "panel joint" / track-to-track connection, not splice. OPEN: fixing of the stack ends at the corners, hold-downs, bracing in the apex panel, gable 1 mirror.
