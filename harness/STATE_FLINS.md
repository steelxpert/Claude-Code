# STATE — FLINS / FlexInSheet CFS floor system (project "flins", prefix FLIN)

Purpose: session handoff. A new session reads `harness/README.md` (how the home works),
this file (where we are) and the newest `gotchas.md` section, then the kickoff it was
given. Method comes from the skills named in the README skill map, never from here.

Last updated: 2026-11-11 (FLIN-003, cloud). Register and queue in §6–§7.

**Direction change (kick-off, Tuesday 2026-11-10, D-012…D-014):** the floor-system
development programme (catalogue, GMNIA campaign, T-series, app) is ON HOLD; the owner
proposed a fixed-price pilot house design instead (O-010). Read §3 and §7 before anything else.

## 1. Project

- Client: FlexInSheet Kft. (FLINS), 2400 Dunaújváros, Előd utca 4. Contact Szabó András
  (ügyvezető); the conglomerate owner Ajkay Tibor holds all HU material issued so far.
- STEELXPERT project number **2026.032a** ("a" = ajánlat, proposal stage). When the job is
  won the Drive folder is renamed `2026.032` (owner action O-001).
- Subject: cold-formed steel (hidegen alakított) floor framing on screw piles for
  residential houses; a design/proposal tool for the sales staff; a GMNIA + test
  programme that produces the span tables.
- Owner's roles: structural concept; CFS analysis, research and optimisation (GMNIA,
  EN 1993-1-3, EN 1993-1-14); app development now and later. Geotechnics: Szecsey Márton.
  Code help: Máté (roles to be decided, O-002).

## 2. Where things are

See `harness/README.md`. Deliverables issued to date (all under Drive `2026.032a`):
FLINS-CFS-001 rev1 feasibility Q&A (EN + HU), 002 rev0 test programme, 003 rev0 role of
AI, 004 rev0 fire and acoustics, 005 rev0 floor vibration, 006 rev0 bearer concept study;
detail figures D01–D09 (`docs/figures/details`); client deck "FlexInSheet
ügyféltalálkozó" (17 slides, artifact AJLrG5BTfyRMYuw5RyQYs8). Sources: `docs/build_*.py`
and `docs/*_hu.py`; the rough app is `floorframe/` (12 tests).

## 3. Decisions (D-nnn, owner-ratified)

| id | decision | session |
|---|---|---|
| D-001 | Home layout: repo = truth (code, note sources, harness), Drive 2026.032a = issued deliverables only, Claude Project = read-only copies for chats, Drive ledger = session rows | FLIN-002 |
| D-002 | Thin harness: project-specific state only; every generic CCX/PPM, GMNIA, Eurocode, DOCX or HU-glossary finding is harvested into the owning skill (README skill map), nothing generic duplicated here | FLIN-002 |
| D-003 | The code stays in steelxpert/Claude-Code for now; no repo split or rename before the roles with Máté are set (O-002, O-003) | FLIN-002 |
| D-004 | Harness text lives in `harness/` at the repo root; the ledger folder `flins/` on Drive holds only INFO.md and KICKOFF_NEXT_FLIN.txt | FLIN-002 |
| D-005 | Skill map includes ec3-1-8-connection-workbook, hu-technical-doc-workflow, flins-sdr, engineering-docx-house-rules, engineering-docx-build besides the CCX/PPM and GMNIA skills | FLIN-002 |
| D-006 | The AI stays outside the structural load path (FLINS-CFS-003): drawing interpretation, proposal text, help; never a resistance | FLIN-001 |
| D-007 | Every span-table number is a PLACEHOLDER until the GMNIA tables and the T-series tests exist; the app and the deck label them so | FLIN-001 |
| D-008 | Hungarian client material follows the EN-HU Eurocode glossary (hidegen alakított, dobozszelvény, a gerinclemez beroppanása, határállapot, torzulásos horpadás) and the light reading-copy format (title block, no cover, no contents page; `--formal` keeps the cover) | FLIN-001 |
| D-009 | Architecture picks as in `docs/02-options-and-decisions.md` (AISI S240 framing rules, GMNIA via EN 1993-1-14 with DSM benchmark, dense JSON span matrix, FastAPI + browser UI, shapely, DXF first) — provisional until the [CLIENT]/[GEO] items close | FLIN-001 |
| D-011 | Smart token-usage rule: Fable for planning, troubleshooting, gotchas and verdicts; delegated tiers for implementation and chores; the kickoff names the tier (README) | FLIN-002 |
| D-012 | Kick-off outcome (2026-11-10): the product idea (CFS / LGS frame system on screw piles) is agreed to be good, but FLINS will not fund the structural + software development programme until they know (a) what superstructure is built on the foundation frame and (b) the market (residential, commercial, defence). Catalogue freeze, GMNIA campaign, T0–T6 tests and app development are ON HOLD; nothing issued so far is withdrawn | FLIN-003 |
| D-013 | Owner's proposal at the meeting: STEELXPERT designs one complete small pilot (test) house on screw piles — a modern barn-house style weekend cottage — with floor (foundation) frame, load-bearing external and non-load-bearing internal walls, partial upper floor (ceiling) frame, roof, wall bracing, window framing, skylight; deliverable = 3D model + EC-compliant calculation for a set price and end date, as the basis of FLINS in-house discussion. Status: PROPOSED, FLINS acceptance pending (O-010) | FLIN-003 |
| D-014 | FLIN-003 scope steps 2–5 (catalogue v0, GMNIA case matrix, recipes, CONTRIBUTING) NOT run: their input (rolled profile set, deck decision D1) was not decided and D-012 parks them. `floorframe/` stays as is (12 tests) | FLIN-003 |
| D-015 | Pilot house concept, owner Q&A (2026-11-10): reference geometry 12.5 x 5.2 m grid, gable about 40 deg; CFS frames on grids 2, 3, 4 with a steel tie rod at eaves; loft over bay 1-2; skylight on the rear slope; ground floor on cross bearers and 15 soil screws; profiles C150x45x1.5 / U150x45, nothing thicker than 1.5 mm; screws / rivets, bolts only at primary joints; envelope loads for Hungary; framing-level model in SpaceClaim, about 4 weeks. Record: `docs/pilot_house/BRIEF.md` | FLIN-003 |
| D-016 | Owner's working rules for the pilot house: one item at a time (instruct -> comment -> approve -> implement -> check); few words, judge by pictures; every sketch as assembly + exploded view; draft before publishing; FLINS delivers the bare steel skeleton, deck and finishes by others and never relied on structurally; end products Hungarian, working versions English | FLIN-003 |
| D-017 | Framing decided so far (owner-approved, shown in `docs/pilot_house/concept_viewer.html`, recorded in BRIEF 7.4 onward): roof = 8 shop panels on the frame rafters, purlins ending in asymmetric tracks, blocking + strap bridging, framed skylight 780 x 1600 with boxed jambs, closed ridge box with blocking plates, diagonal straps in the gable-end bays only; cross grids A / B / C on the soil screw lines (front wall = wall C); slotted web perforations 38 x 100 at 600; eave: roof panel's lowest edge on the inner top edge of the wall track, folded cap outside and angle inside; long walls = shop panels per bay, single end studs back-to-back with the neighbour (they are the frame leg), two bridging rows; door with boxed header and capped jambs, bottom track cut out on site | FLIN-003 |
| D-018 | Gable 5 (first approximation, viewer v19): two shop panels with a horizontal panel joint on the eave line (wall panel 5.05 x 2.76 m + apex panel); long-wall end panels, end roof panels, eave and ridge caps run to the gable outer face; raking tracks in the rafter-top plane carry the end roof panels; window framed as the door plus a sill track; X-straps corner to window jamb. Open: hidden header in the apex top track, corner detail, hold-downs, apex bracing (BRIEF 7.4, last paragraph) | FLIN-004 |
| D-010 | Tuesday 2026-11-11 kick-off: live at FLINS, Dunaújváros; decisions first (the six items of deck slide 17), then workstreams; no new client material is prepared for it; the agenda is the owner's internal chair notes (`harness/meetings/2026-11-11_kickoff_Dunaujvaros.md`) | FLIN-002 |

## 4. Open owner items (O-nnn)

| id | item | status |
|---|---|---|
| O-001 | Rename Drive folder `2026.032a` → `2026.032` once the job is won; update the project number in `docs/*.py` (`--projno`) and the deck footers in the same session | waits for the award |
| O-002 | Roles with Máté: owner writes a rough plan of how the app should look, behave and work, then holds his own kick-off with Máté; all structural concept stays with the owner; who starts coding is decided there | open |
| O-003 | Repo split (`steelxpert/floorframe`) or rename — only after O-002 | open |
| O-004 | Create the Claude Project "FlexInSheet" with read-only copies of `docs/` and this STATE | open, low effort |
| O-005 | The six client decisions of deck slide 17 (profile set Q5, geotechnical partner and pile catalogue, feedback on CFS-001…006, target market, hosting, AI assistance) | not decided item by item at the kick-off [owner to confirm]; parked by D-012. Profile set, target market and superstructure type come back through the pilot house (O-010) |
| O-006 | Test laboratory partner for T0–T6 and the certification body for T6 | parked (D-012) |
| O-007 | Geotechnics lead Szecsey Márton: screw-pile catalogue, acceptance route (MSZ EN 1997-1), test loading | carried: the pilot house needs pile design resistances for one real site/soil assumption |
| O-009 | Upload the patched 3w-cp skill (`harness/skills-proposed/3w-cp.zip`): Where = venue on machine, smart token rule; until then the harness README copy is the stop-gap | owner, tonight |
| O-010 | Pilot house (D-013): FLINS acceptance; fixed price and end date; brief (footprint, storeys, roof pitch, site / snow / wind zone, cladding and build-ups, profile set FLINS can roll today, preferred joints); 3D model format FLINS can open; one written proposal letter (structural-proposal-letter skill) | owner + FLINS, open |
| O-011 | Project number / Drive folder: does the pilot house stay under 2026.032a or get its own number; O-001 rename stays blocked until an order exists | owner |
| O-012 | The meeting note file is named 2026-11-11 but the kick-off Tuesday was 2026-11-10; file not renamed (no restructuring without say-so) | owner |
| O-013 | Pilot house, still to instruct (owner): glazed bays of wall C; knee joint (rafter foot vs the end-stud leg); gable 5 hidden header + corner detail, gable 1; remaining wall bracing (wall A has one braced bay); loft; ground floor; partitions. For the calculation: wind on the long walls with roof diagonals only in the end bays; ridge-edge member ends about 4 kN; eccentric bearing at the eave; asymmetric track is a new section for FLINS | open |
| O-008 | FLiBess EN-HU glossary (`research/glossary_EN-HU_Eurocode.md`) and its use rules: copy into this repo or keep the Drive copy as the single source | open |

## 5. Standing rules (non-negotiables)

- No repository or Drive restructuring without owner say-so.
- The AI stays outside the structural load path (D-006).
- PLACEHOLDER span tables until GMNIA + T-series exist (D-007); every number in a client
  document has a source (clause, test, recipe).
- Hungarian material: glossary terms verbatim, `⚠ not in glossary` where a term is missing,
  light reading-copy format (D-008).
- Analysis runs are recipes (`harness/recipes/README.md`); `[MEASURED]` only after a
  clean re-run.
- Smart token-usage rule (`harness/README.md`): Fable plans, troubleshoots, writes gotchas
  and verdicts; Opus / Sonnet / Haiku sub-agents or separate sessions do the rest.
- Session close per `harness/README.md` §Session shape and the `3w-cp` skill.

## 6. Session register

| id | date | venue / model | what |
|---|---|---|---|
| FLIN-001 | 2026-11-08 | cloud, model n/r | client meeting material: HU notes FLINS-CFS-001…005 (-HU), deck (17 slides), detail figures D01–D09, glossary alignment, light reading-copy format; branch `claude/trusting-mayer-47ebp9` to 8676f47 |
| FLIN-002 | 2026-11-08 | cloud, Fable 5.1 high | home and harness decided by owner Q&A (D-001…D-005, D-010, D-011); `harness/` created; flins/FLIN registered in the ledger (rows FLIN-001, FLIN-002); Tuesday chair notes drafted; smart token rule and venue rule encoded; 3w-cp skill patch built (`harness/skills-proposed/3w-cp.zip`, owner uploads) |
| FLIN-003 | 2026-11-10..11 | cloud (model in the ledger row) | context verified (1382e5e, 12 passed, ledger FLIN-003); kick-off outcome logged: D-012 programme on hold, D-013 pilot house proposed, D-014 catalogue / case matrix not run; then, at the owner's lead, the pilot house concept: brief by Q&A (D-015), interactive 3D viewer with detail scenes and member picking, roof / ridge / eave / long wall panels / door decided item by item (D-016, D-017); branch at 5ccf1cc; kickoff FLIN-004 rewritten |

## 7. Queue

1. **FLIN-004** — pilot house framing, continued one item at a time (O-013): glazed bays of
   wall C, knee joint, gable walls, loft, ground floor; then the work breakdown in hours and
   the Hungarian fixed-price offer with the viewer as attachment (O-010). Kickoff:
   `harness/kickoffs/KICKOFF_FLIN-004.txt`.
2. Parked by D-012, resume only on a FLINS decision on superstructure + market: catalogue
   freeze v0, GMNIA campaign case matrix, test programme, app (`KICKOFF_FLIN-003.txt` keeps
   that scope text).
3. If FLINS declines the pilot house: one ledger row `paused (programme on hold)`.
