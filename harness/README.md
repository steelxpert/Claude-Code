# FLINS harness — FlexInSheet CFS floor system (project "flins", prefix FLIN)

The knowledge harness of the FlexInSheet cold-formed steel (CFS) floor project:
*where we are*, the decisions, the gotchas and the kickoffs. It is deliberately thin.
Reusable method lives in skills, not here (see "Skill map"). Owner-approved layout,
FLIN-002, 2026-11-08.

## Home: one source of truth per artefact type

```
                 FlexInSheet CFS floor · project "flins" · prefix FLIN
 ┌─────────────────────────────────────────────────────────────────────────┐
 │  GitHub steelxpert/cfs-house (SOURCE OF TRUTH: main; branch per session)    │
 │   floorframe/  tests/  examples/      code, pytest = release gate       │
 │   docs/        01..03 + build_*.py    note SOURCES (EN+HU), figures     │
 │   harness/     STATE_FLINS.md         where we are, decisions, queue    │
 │                gotchas.md             dated, append-only, [MEASURED]    │
 │                recipes/               reproducible analysis scripts     │
 │                kickoffs/KICKOFF_FLIN-nnn.txt   one per session          │
 │                meetings/              agendas, decision logs            │
 └──────────┬──────────────────────────────┬───────────────────────────────┘
            │ issue (PDF/DOCX/deck export)  │ copy, read-only
            ▼                              ▼
 ┌─────────────────────────┐   ┌──────────────────────────────┐
 │ Drive 2026.032a         │   │ Claude Project "FlexInSheet" │
 │  scope/ basis/ plan/    │   │  knowledge = copies of docs/ │
 │  presentation/ corresp/ │   │  + STATE; chats only, never  │
 │  ISSUED deliverables    │   │  edited there (not yet made) │
 └─────────────────────────┘   └──────────────────────────────┘
            ▲
 ┌──────────┴──────────────────────────────────────────────────┐
 │ Drive ledger/  SESSIONS.csv + STATE_INDEX.md                │
 │   flins/INFO.md  flins/KICKOFF_NEXT_FLIN.txt  (ledger only) │
 └─────────────────────────────────────────────────────────────┘
        HARVEST ──► skills (see Skill map below)
```

| Artefact type | Lives in | Rule |
|---|---|---|
| Code, tests, examples | `floorframe/`, `tests/`, `examples/` | pytest green before push; owner merges |
| Note sources (EN + HU), figures | `docs/` | the DOCX/PDF is generated, never hand-edited |
| Project state, decisions, queue | `harness/STATE_FLINS.md` | updated at every session end |
| Gotchas | `harness/gotchas.md` | append-only, dated `— YYYY-MM-DD (FLIN-nnn)` |
| Analysis recipes | `harness/recipes/` | one file per reproducible run, header per `recipes/README.md` |
| Kickoffs | `harness/kickoffs/` | one per session, written by the closing session |
| Meeting material (internal) | `harness/meetings/` | chair notes and decision logs, not sent to the client |
| Issued client deliverables | Drive `2026.032a/` (`scope`, `basis`, `plan`, `presentation`, `corresp`) | only files that went to the client; rename to `2026.032` when the job is won (owner, FLIN-002) |
| Chat knowledge | Claude Project "FlexInSheet" | read-only copies of `docs/` and STATE; kickoffs are never run inside a Project |
| Session rows, next kickoff | Drive `ledger/` (`SESSIONS.csv`, `STATE_INDEX.md`, `flins/`) | one row per 3w+cp; `KICKOFF_NEXT_FLIN.txt` mirrors the newest kickoff here |

## Harness vs skills (thin harness, harvest to skills)

FLINS keeps only what is specific to this project. Every generic finding leaves as a
`HARVEST:` line in the session wrap-up and lands in the owning skill:

| Finding type | Owning skill |
|---|---|
| CalculiX / PrePoMax mechanics (keywords, import, convergence, results) | `calculix-prepomax-ops` (and `prepomax-harness` / `pmx-field-manual` when the PMX harness proves it) |
| GMNIA method: DSM/CUFSM triage, imperfections, built-up connectors, EN 1993-1-14 spine | `cfs-gmnia-virtual-testing` |
| Load introduction into thin CFS webs, web crippling, stiffeners | `cfs-load-introduction` |
| Bolted / pinned connection checks, EN 1993-1-8 workbook | `ec3-1-8-connection-workbook` |
| Hungarian document workflow, data module, parse-by-content, render check | `hu-technical-doc-workflow` |
| Hungarian report style, EN-HU Eurocode glossary (hidegen alakított, dobozszelvény, a gerinclemez beroppanása), signature block | `steelxpert-hu-report`, glossary `research/glossary_EN-HU_Eurocode.md` (FLiBess folder) |
| DOCX layout and delivery rules for every client | `engineering-docx-house-rules` |
| DOCX build / splice / verification mechanics | `engineering-docx-build` |
| FLINS client constants (address, contacts, folder convention, AxisVM habits) | `flins-sdr` |
| Session wrap-up, ledger row, kickoff format | `3w-cp` |

What stays here: the catalogue and framing decisions, the test programme status, the
client decisions, the span-table placeholder status, the app roadmap, the kickoffs.

## Smart token-usage rule (owner rule, FLIN-002, 2026-11-08)

Spend the top-tier model only where judgement is irreplaceable, and say in the kickoff
which tier does what:

| Work | Tier | How |
|---|---|---|
| Planning a session or a workstream, choosing an approach, re-scoping | **Fable 5.1** (high effort only when the call is genuinely hard) | the main session |
| Troubleshooting an unexplained failure, deciding what a result means (verdict), writing or classifying a gotcha, anything that edits a frozen record or a gate | **Fable 5.1** | the main session; a one-line comment on *why* it needed Fable goes into the gotcha or STATE entry when the reason is not obvious |
| Mechanical implementation against an existing pattern, reruns, figure and note regeneration, refactors with tests as the net | **Opus 5.5** (large or long) or **Sonnet 5.5** (well-scoped) | a sub-agent of the Fable session, or a separate session whose kickoff names the tier |
| Scripted chores: file moves, format conversions, batch renames, index rebuilds | **Haiku** | sub-agent |

Amendment (owner, FLIN-004, D-019): for the pilot house framing thread the planning tier is
Opus 5.5 from FLIN-005 on, Sonnet 5.5 sub-agents for the viewer edits; Fable only when the
owner explicitly asks for a new session on it.

Rules: the planning session plans, delegates with a complete brief, and judges the result;
it does not grind. A delegated session's kickoff carries the tier in its "Which" line;
its ledger row records the model actually served (sub-agents appended with `+`). When a
delegated task hits an unexplained failure it stops and hands back, it does not debug
on its own.

## Venue rule: every kickoff says where the session runs (owner rule, FLIN-002)

The 3w-cp "Where" W names cloud or local. From FLIN-003 on, every FLIN kickoff and every
FLIN wrap-up carries the fuller form `Where: <venue> on <machine>`, venue being one of:

| Venue | Reaches | Use for |
|---|---|---|
| **Claude Code cloud** | the repo, Drive via connector, no PC files | code, docs, harness, ledger from the cloud |
| **Claude Code local** (hostname named) | the repo plus PC files and tools | the same when PC-only files are needed |
| **Cowork desktop + device bridge** (hostname named) | PC folders, PrePoMax / AIM / SpaceClaim, Drive folders staged | solves, GUI tools, client folders |
| **Claude Project chat** | the Project's knowledge copies | reading and client-facing drafting only; never a kickoff (ORG-003b) |

This copy is a stop-gap for FLINS. The same wording is proposed for the 3w-cp skill in
`harness/kickoffs/3w-cp_WHERE_patch.md`; once the skill is updated, the skill wins and
this section becomes a pointer.

## Session shape (FLIN-nnn)

1. Verify context: branch and commit named in the kickoff, `python -m pytest` green.
2. Read first: this file, `STATE_FLINS.md`, the newest `gotchas.md` section, the files the kickoff names, the skills it lists.
3. Work; every number that enters a client document has a source.
4. Close: STATE updated (register, decisions, open items, queue), gotchas section appended, next kickoff written, commit and push to the session branch, 3w+cp with the ledger row (machine measured) and `KICKOFF_NEXT_FLIN.txt` on Drive.
