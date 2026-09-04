# Desktop-app agent harness — session knowledge extract

Consolidated knowledge from the Claude Code session (Aug–Sep 2026) that
designed and built the SpaceClaim agent harness in `steelxpert/Claude-Code`,
branch `claude/code-external-tool-integration-7orw3z`. Written to be fed
into another project as context. Owner: Bán Csaba / STEELXPERT Kft.

## 1. The question and the answer

**Question:** can Claude Code "learn" a desktop app (Ansys SpaceClaim) and
use it to create/modify content in an automated loop?

**Answer:** yes — but not by driving the GUI. Split the problem into three
independent layers; conflating them is why such projects usually fail:

1. **Control layer** — how the app is mechanically driven. Prefer the
   app's scripting API in headless batch mode over GUI automation
   (deterministic, loggable, diffable). GUI/vision automation is a last
   resort only for apps with no API.
2. **Knowledge layer** — how the agent "knows" the app. Not learning by
   watching: retrievable, versioned knowledge (a Claude Code skill file)
   seeded from the app's own macro recorder and grown by the loop's
   failures.
3. **Loop layer** — generate → run → measure → verify → fix. Converges
   only if the verifier is objective (see §4).

## 2. Verified environment facts (SpaceClaim / Ansys, licensing)

- User's license: **Ansys Discovery SpaceClaim 2020 R1 perpetual**
  (v201), Windows-only. Exe:
  `C:\Program Files\ANSYS Inc\v201\scdm\SpaceClaim.exe`.
- Headless batch works on v201:
  `SpaceClaim.exe /RunScript="<abs>.py" /Headless=True /Splash=False
  /Welcome=False /ExitAfterScript=True` (flags stable v193→v251).
- Scripting is **IronPython 2.7** in-process; API assembly
  `SpaceClaim.Api.V18` for 2020 R1; recorded scripts start
  `# Python Script, API Version = V18` (never raise the header).
  API geometry units are **meters**; `Shape.Volume` returns m³.
- The Script editor **records every GUI action as V18 Python** — the
  bootstrap/ground-truth mechanism for API call signatures.
- **PyAnsys**: MIT/open-source clients but they need a licensed modern
  backend. PyAnsys Geometry requires ≥23.2.1, realistically **24 R1** —
  unusable on 2020 R1/2021 R2 (the gRPC service doesn't exist there).
  PyMAPDL works from ~2021 R1; PyDPF only with old pins.
- Economics: each headless launch = one license-seat checkout + 20–60 s
  startup → batch all of an iteration's work into ONE launch; seat count
  caps parallelism (assume 1).
- Community precedent for the pattern: Blender/FreeCAD/Fusion 360 MCP
  servers — all thin wrappers over the app's scripting API.

## 3. What was built (all pushed, mock-tested on Linux)

```
spaceclaim-harness/
  README.md                  architecture + quickstarts (gear = calibration)
  DEFEATURE.md               production pipeline guide (bulk FEA cleanup)
  config.example.json        exe path, timeout
  recipe.example.json        defeaturing thresholds/patterns per job
  mcp_server.py              optional FastMCP wrapper (env_check, build_gear,
                             run_sc_script); needed only for cross-machine use
  harness/
    runner.py                Windows subprocess wrapper; SC_JOB_DIR env-var
                             job contract (params.json in, result.json out)
    gear_math.py / verify.py analytic expectations + 6-check verifier
    mock_backend.py          Linux stand-in, 5 injectable defects
    loop.py                  one iteration CLI (--mock/--real), exit 0/1
    verify_defeature.py      7 conservation checks (see §5)
    mock_defeature.py        5 injectable defects
    defeature_batch.py       folder batch driver → summary.md/.json
  sc_scripts/
    spur_gear.py             IronPython V18 template (exact involute math;
                             ~10 VERIFY-tagged API calls)
    defeature.py             IronPython V18 template (open→delete fasteners→
                             remove fillets≤r→fill holes≤d→export+manifest)
.claude/skills/spaceclaim-scripting/SKILL.md   growing gotcha memory
.mcp.json                    registers the MCP server (errors harmlessly in cloud)
```
Deliverables produced: web runbook artifact ("SpaceClaim Gear Loop",
claude.ai/code/artifact/dd9f875a-3fd7-42d1-ac66-e240da7eed7b) + PDF;
defeature guide .md + PDF (Chromium print pipeline, fonts inlined).

## 4. Generalizable design patterns (the part worth transplanting)

- **Deterministic verifier, never LLM self-judgment.** The agent writes
  code and diagnoses failures; acceptance is decided by dumb comparison
  code. An LLM grading its own output grades generously; a formula
  doesn't. Verifier output: `{name, ok, detail}` per check, where
  `detail` is a human sentence — failures diagnose themselves for the
  next agent iteration.
- **Two independent paths to the same numbers.** Expected values from
  pure math on the request; measured values interrogated from the real
  artifact (never echoed from inputs). Verifier only compares.
- **Bracket, don't guess.** Where exact targets are hard (tooth volume),
  gate on rigorous bounds plus a softer warning band. Every tolerance
  carries a written physical justification; widening a tolerance to pass
  is forbidden (written into the skill).
- **Three measured states for modification pipelines**:
  before / structure (after intended deletions) / after. Conservation is
  checked against *structure*; deletions are accounted item-by-item
  (name + volume) and an accounting check fails if anything vanishes
  unlogged. This is the trust mechanism for destructive bulk ops.
- **Teach-by-recording.** For any scriptable app: perform the operation
  once in the GUI, let the app record it, align template code against
  the recording. Offline-written API calls carry `VERIFY` tags until a
  recording confirms them; fixes get harvested into the skill's gotcha
  list — durable, cross-session learning.
- **Mock-first + defect injection.** A full mock backend lets the entire
  loop run without the licensed app; the verifier is validated by
  injecting known defects and proving each is caught. "A verifier you
  haven't watched fail is decoration."
- **File-based job contract via env var** (SC_JOB_DIR): version-proof,
  language-neutral, debuggable; avoids fragile arg-passing mechanisms.
- **Split dumb in-app script / smart external brain.** In-app script
  (old embedded interpreter) stays parameter-driven and dumb; all
  intelligence (math, verification, iteration) lives in modern CPython
  outside. Testable without a license.
- **Audit manifest for sign-off workflows.** Every destructive action
  logged with magnitudes; summary.md is the engineer's 5-min review.
  Target 95% automation + human judgement at thresholds and review —
  the right split for work that ends in a signature.
- **GitHub as courier / time machine / shared memory** between cloud
  sessions and the local Windows session; skills in-repo mean every
  future session starts already knowing the accumulated gotchas.
  (Cloud containers are ephemeral — a mid-session restart re-clones the
  repo; only pushed work survives.)

## 5. Verifier check inventories (reference)

Gear (build): script_status, single_body, outer_diameter (bbox vs
m(z+2), −2/+0.5%), face_width (±0.5%), volume_envelope (root↔tip disk
±2%; ±10% warning band), tooth_count. Defects proven caught:
missing_tooth, half_width, split_body, blank_disk, script_error.

Defeature (modify): script_status, selection_effective,
fastener_accounting (±0.5% of before-volume), volume_conservation
(default 2% vs structure), bbox_conservation (±0.2%), body_count,
feature_failures (default ≤10% of selected). Defects proven caught:
lost_body, volume_blown, nothing_removed, fill_failures, script_error.

## 6. Status and next actions

Done: both pipelines scaffolded, mock-verified, pushed; guides + runbook
delivered. Not done (needs the Windows PC): Phase 1–3 installs, the
one-time recording session, VERIFY-tag repair for both sc_scripts, first
real runs. Not scaffolded yet: midsurface-extraction recipe; power-
selection fast path (template uses a face-walk fallback). Cosmetic:
.mcp.json makes cloud sessions log a harmless spaceclaim-server connect
error.

Kickoff prompt for the Windows bring-up session:
"Read .claude/skills/spaceclaim-scripting/SKILL.md and
spaceclaim-harness/README.md. I've saved recorded_reference.py (and
recorded_defeature.py) in sc_scripts/. Repair all VERIFY-tagged calls in
spur_gear.py and defeature.py against the recordings, then run the gear
loop (--real, m=2 z=24) and a defeature batch on the sample folder until
verification passes. Harvest fixes into the skill, commit, push."
