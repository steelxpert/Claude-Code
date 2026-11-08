---
name: "3w-cp"
description: "The owner's standard end-of-session wrap-up and handoff ritual, project-agnostic (solidx, CFD, any repo or engineering project). Invoke whenever the owner writes '3w+cp', '3w', '4w', 'cp', 'wrap up', 'wrap it up', 'handoff', or asks where do we stand / what's next at the end of a work session — even mid-conversation after a merge, a report, or a milestone. Produces the four W's (What was done, What's next, Where — cloud vs local, Which — model recommendation), appends the session's row to the cross-project ledger SESSIONS.csv on Google Drive with the machine name, rewrites the thread's KICKOFF_NEXT file, and then the cp: a ready-to-paste kickoff prompt for the top next task. Do not wait to be asked twice — any session that ends with pushed work should get this wrap-up when the owner signals they are closing out."
---

# 3w+cp — session wrap-up and handoff

The owner (Csaba, STEELXPERT) runs many engagements in parallel — solidx,
CFD work, client SDRs — across both cloud containers and the local
workstation. Sessions end; context does not carry itself. This ritual is
how a session hands its state to the next one, in a form the owner can
read in one minute and act on by pasting one prompt into the right kind
of session on the right model. Keep it dense, factual, and
decision-ready — the same register as an owner task report, but one
screen long. ("3w" is the historical shorthand; the ritual now carries
four W's, owner-extended 2026-08-15.)

> Provenance: reconstructed and owner-ratified in the solidx contact-C3
> session (2026-08-15), where the cloud container had no memory store —
> which is exactly why it lives in a skill: skills sync to every session
> and project, memories do not. Same-day owner corrections already
> applied: "Where" must carry a cloud/local recommendation; "Which"
> (model) added as the fourth W; cp means the copy-paste kickoff prompt,
> not commit-and-push. If the owner corrects anything else, update this
> file rather than working around it.

## The four W's

Deliver all four sections, in this order, each a short titled block.

**1. What (was done).** The session's outcomes as facts with their
evidence: what merged/shipped/was measured, with the key numbers,
PR/commit references, and any findings that change how the owner should
think about the project (a discovered bug, a corrected baseline, a
rejected design). Failures and skipped scope stated plainly. Close this
block with the persistence check — verify, don't assume: working tree
clean, everything committed and pushed to the right branch, PR/CI state
named explicitly (green / running / red), deliverables in their
conventional homes, and anything that could NOT be persisted (unmounted
memory store, local-only files) listed with where its content went
instead. Fix any gap before reporting; the block states what IS true.

**Literature check** (owner workflow, added 2026-09-22 after the
Perplexity-batch lesson): if the session landed, newly identified, or
invalidated any papers, update the project's papers-wanted ledger before
wrapping (2d-cfd: `docs/rev/papers-wanted.md`; other projects: their
equivalent shelf; house format: full bibliographic references at first
mention, unverified fields marked "verify on landing", never guessed).
Then list the STILL-WANTED papers precisely in this block — full
citations, one per line — so the owner can fetch them between sessions
and drop the PDFs into the project's papers folder
(2d-cfd: `source/papers-wanted/...`). Only leads that changed status
belong here (new-wanted, landed, rejected), not every paper mentioned.

**2. What's next.** The concrete follow-on tasks, ranked. For each: one
line of scope, why it is next (dependency, risk, owner decision
pending), and rough size (hours / a session / multiple sessions).
Decisions that are the owner's to make are flagged as such, not folded
into work items.

**3. Where.** Where the next work should happen: always one explicit line per
task (or one for a uniform batch) in the form `Where: <venue> on <machine>`,
followed by one sentence of reasoning. Venue is one of (owner rule 2026-11-08,
FLIN-002):

- **Claude Code cloud** — repo work, Drive via connector, no PC files;
  machine = `cloud`.
- **Claude Code local** — repo work that needs PC files or tools;
  machine = hostname.
- **Cowork desktop + device bridge** — PC folders, PrePoMax / AIM / SpaceClaim,
  Drive folders staged through the bridge; machine = hostname.
- **Claude Project chat** — reading and client-facing drafting only; a kickoff
  is never run inside a Project (owner rule ORG-003b).

The cp block repeats the same `Where:` line verbatim, so the owner opens the
right product on the right PC before pasting. The criteria below decide
between the first three venues:

- **Cloud** when the task is code + tests + CI + PR + docs on a repo the
  cloud environment can reach, the compute fits a container (test suites
  up to ~10–15 min, modest RAM), or several independent tasks could run
  as parallel cloud sessions while the owner does something else.
- **Local (workstation)** when the task needs: long or heavy compute
  (hours-long solves, large meshes, many-GB RAM, MKL/Pardiso performance
  numbers — container timings are not representative and must never be
  recorded as benchmarks); GUI/licensed tools (SpaceClaim/Discovery,
  PrePoMax, AxisVM, ANSYS, ParaView inspection); files that live only on
  the workstation or client drives; or the session must read/update the
  memory store (mounted locally only — cloud sessions fall back to repo
  docs).
- When mixed, split the task and say which half goes where.

**4. Which (model).** Recommend the model tier for each next task (or
the batch), with one sentence of reasoning. The current ladder — update
as Anthropic's lineup moves, and check the session's own model id rather
than guessing names:

- **Fable/Mythos 5 (top tier)** — formulation and design work, anything
  that edits a frozen measured record or calibrated gates, debugging
  where the failure mode is unknown, multi-constraint judgment calls
  (the cost premium is small against a wrong entry in a record that
  signed work later relies on).
- **Opus 5** — the same class of work when top-tier is unavailable or
  the task is large but well-understood; also long grinding sessions
  where fast mode helps.
- **Sonnet 5** — well-scoped mechanical implementation against existing
  patterns, reruns, report/figure regeneration, refactors with full test
  coverage as the safety net.
- **Haiku** — trivial scripted chores only.

Smart token rule (owner, 2026-11-08): the top tier plans, troubleshoots,
writes gotchas and verdicts; implementation, reruns, regeneration and chores
go to Opus / Sonnet / Haiku sub-agents or separate sessions whose kickoff names
the tier. Also note the reasoning-effort setting when it matters: default/medium
for mechanical work; high only where the task genuinely needs deep
deliberation. Borderline calls: say so, name both options and the
tiebreaker, and let the price/urgency tradeoff be the owner's.

## Ledger row (owner rule ORG-001, 2026-11-07; moved to Drive by ORG-004 the same day) — before the cp

The owner keeps one cross-project ledger in a Google Drive folder that
is available offline on every PC: `G:\Saját meghajtó\ledger\SESSIONS.csv`
(columns: `date, project, session_id, machine, folder, model, status,
next_kickoff`) and its summary `STATE_INDEX.md` beside it. The old
location `C:\!PROJECTS\CLAUDE.AI\` holds only frozen `.moved-to-GD-2026-11-07`
copies and a `LEDGER_MOVED.txt` pointer — never append there. Every
wrap-up appends ONE row and refreshes that project's line in the index.
Rules:

- **Machine name is mandatory.** Measure it, never recall it: from a
  linked device session `get_device_info` → `deviceName`; from a shell on
  the PC `hostname`. Known names: `desktop-lrm6oei` = hp_WS (this is the
  AIM / SpaceClaim / cowork PC), `desktop-p1e5ab3` = WS_28core (PrePoMax,
  solidx clone), `desktop-thrbt1a` = WS_dell (home). A pure cloud session
  with no device link writes `cloud` and names the repo in `folder`.
- **Model** = the session's own model id (check it, do not guess);
  sub-agents appended with `+`.
- **Project slugs** in use: `ansys` (PDB / SCX / BJT), `ppm` (PPM), `pmx`
  (PMX / PMXP / CRD), `ny909` (GIR / TRS / FRM / CAR), `flibess` (FLIB),
  `solidx` (SOLX), `org` (ORG). A new project gets a new short slug, a
  line in STATE_INDEX.md and a folder `<slug>\` in the ledger folder
  holding `INFO.md` (what it is, where its STATE files live, its
  prefixes).
- **Session ids (owner rule 2026-11-07):** `PREFIX-nnn` — 3 or 4
  meaningful letters, a dash, three digits. No two-letter prefixes, no
  letters inside the counter (`PMX-P31` → `PMXP-032`), no suffix letters
  (`020b` is not allowed: a re-run or continuation takes the next number
  and says "continuation of 020" in its status). The prefix table with
  the next id of every thread is in STATE_INDEX.md ("Session-id
  prefixes"); look it up, never invent a prefix that is not there — a
  new thread registers its letters in that table before its first row.
- **KICKOFF_NEXT file.** The cp block is also written to
  `<ledger>\<slug>\KICKOFF_NEXT_<PREFIX>.txt` (overwrite; one file per
  thread, constant name) in the same stage → commit pass as the ledger
  row, so the owner always finds exactly one current kickoff per thread
  and never has to search chats or STATE files for it. If a thread has
  nothing queued, the file says so in one line.
- **HARVEST (project threads).** For a client job or any thread that will
  end when its deliverable ships (ny909, future jobs), the "What" block
  ends with `HARVEST:` lines — each reusable finding and the harness or
  skill it belongs to (AIM API behaviour → ansys PDB gotchas; methods →
  a method skill; report rules → engineering-docx-house-rules / the
  client style skill). Repeat them in the receiving harness's
  KICKOFF_NEXT file as a to-do. When the job is delivered, the thread's
  last row gets status `archived` after a check that every HARVEST line
  has landed.
- **status** is one of `closed`, `in-progress (…)`, `paused (…)`,
  `merged`, `stopped (…)`; **next_kickoff** is the next session id plus
  a few words, the same thing the cp block starts with. Inferred values
  carry `[INFERENCE]`; unrecorded values are `n/r`, never invented.
- **How to write it (Drive folders are bridge-only).** The device shell
  (`device_bash`) cannot mount Google Drive folders, even offline ones,
  so never try `echo >>` or `sed -i` on the ledger. Instead: (1) if
  `G:\Saját meghajtó\ledger` is not in `connectedFolders`, request it once
  with `device_request_folder_access`; (2) `device_stage_files` both
  files; (3) append the row and edit the index in the cloud container
  with a short python read-modify-write — UTF-8, **every line CRLF**, no
  header repeated, no reorder; (4) `device_commit_files` both files back
  to the same Drive paths; (5) verify by `device_list_dir` sizes (and by
  re-staging and counting lines when anything looked odd). Exit check,
  always printed: line count before/after (+1), header count 1, CRLF
  count = LF count. If the folder cannot be reached (cloud-only session,
  Drive not running), write the finished row as the last line of the
  "What" block, marked **LEDGER ROW NOT WRITTEN — owner to append**, so it
  is never silently lost.
- One session writes the ledger at a time; Drive does not merge
  concurrent edits (it keeps two files). If a second copy such as
  `SESSIONS (1).csv` ever appears, stop and tell the owner.
- The row is written AFTER the persistence check (so `status` is true)
  and BEFORE the cp (so `next_kickoff` and the cp agree).

## cp: the copy-paste kickoff prompt

End with a fenced code block the owner can paste verbatim into a fresh
session to start the TOP next task (additional tasks get one only on
request). It must stand alone — the new session has no memory of this
one. Model it on what works:

- **Task line**: imperative one-liner naming the deliverable and the
  project phase. If the task was gated on an owner decision, state that
  pasting this prompt IS the owner say-so.
- **Verify context first**: pull latest main; verify (not assume) the
  state this session left behind — the merged PR by number, via gh.
  If the precondition fails, stop and ask.
- **Read-first list**: the exact files/records that carry the context
  (theory-guide chapters, reports, test headers, memories where
  mounted — with the cloud fallback named).
- **Scope bullets**: what to build/change, at the level of decisions
  already made — don't re-litigate settled design in the new session.
- **Non-negotiables**: the project's standing invariants that a fresh
  session could unknowingly violate (bit-identical baselines, frozen
  records, tolerance-calibration rules, SPD/solver constraints — carry
  them forward verbatim from the project's conventions).
- **Papers shelf check**: when the wrap-up listed wanted papers, the cp
  carries that list and instructs the new session to inventory the
  papers folder FIRST, verify every newly landed PDF against its own
  title page before trusting it (AI-search and secondhand citations are
  leads, never references), update the papers-wanted ledger
  (landed / still wanted / rejected), and commit the ledger change with
  provenance before the main work starts.
- **Exit gates**: measurable pass criteria, plus the repo workflow
  (branch, full suite before push, PR + CI green, no merge without
  owner say-so, task report, and close with this ritual: 3w+cp — which
  includes appending the session's row to `SESSIONS.csv` with the
  measured machine name).
- **Machine line**: name the PC the session must run on (hostname), or
  `cloud`, so the ledger row of the next session is unambiguous.
- **Where + Which lines**: repeat the `Where: <venue> on <machine>` line and
  the model recommendation from the W's verbatim so the prompt is
  self-contained.