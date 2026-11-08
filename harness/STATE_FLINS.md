# STATE — FLINS / FlexInSheet CFS floor system (project "flins", prefix FLIN)

Purpose: session handoff. A new session reads `harness/README.md` (how the home works),
this file (where we are) and the newest `gotchas.md` section, then the kickoff it was
given. Method comes from the skills named in the README skill map, never from here.

Last updated: 2026-11-08 (FLIN-002, cloud, Fable 5.1). Register and queue in §6–§7.

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
| D-010 | Tuesday 2026-11-11 kick-off: live at FLINS, Dunaújváros; decisions first (the six items of deck slide 17), then workstreams; no new client material is prepared for it; the agenda is the owner's internal chair notes (`harness/meetings/2026-11-11_kickoff_Dunaujvaros.md`) | FLIN-002 |

## 4. Open owner items (O-nnn)

| id | item | status |
|---|---|---|
| O-001 | Rename Drive folder `2026.032a` → `2026.032` once the job is won; update the project number in `docs/*.py` (`--projno`) and the deck footers in the same session | waits for the award |
| O-002 | Roles with Máté: owner writes a rough plan of how the app should look, behave and work, then holds his own kick-off with Máté; all structural concept stays with the owner; who starts coding is decided there | open |
| O-003 | Repo split (`steelxpert/floorframe`) or rename — only after O-002 | open |
| O-004 | Create the Claude Project "FlexInSheet" with read-only copies of `docs/` and this STATE | open, low effort |
| O-005 | The six client decisions of deck slide 17 (profile set Q5, geotechnical partner and pile catalogue, feedback on CFS-001…006, target market, hosting, AI assistance) | Tuesday 2026-11-11 |
| O-006 | Test laboratory partner for T0–T6 and the certification body for T6 | open |
| O-007 | Geotechnics lead Szecsey Márton: screw-pile catalogue, acceptance route (MSZ EN 1997-1), test loading | open |
| O-009 | Upload the patched 3w-cp skill (`harness/skills-proposed/3w-cp.zip`): Where = venue on machine, smart token rule; until then the harness README copy is the stop-gap | owner, tonight |
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

## 7. Queue

1. **FLIN-003** — after Tuesday 2026-11-11: write the decision log into §3/§4 (O-005
   closed or carried), fold client feedback into the notes if any, then start the
   catalogue freeze: section family from the rolled profile set, framing rules, load
   classes (`floorframe/catalog`), and the GMNIA campaign case matrix
   (`floorframe/fea/campaign.py`, T0–T2a validation cases first). Kickoff:
   `harness/kickoffs/KICKOFF_FLIN-003.txt`.
2. If the job is not awarded: one row `paused (no award)` and the thread sleeps.
