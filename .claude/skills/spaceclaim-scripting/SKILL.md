---
name: spaceclaim-scripting
description: Driving Ansys SpaceClaim 2020 R1 (v201, API V18) headless via /RunScript with IronPython for automated geometry creation (gear harness). Use whenever writing or repairing a SpaceClaim IronPython script, running the spaceclaim-harness loop, interpreting a failed result.json, or bootstrapping the V18 API calls from a recorded macro. Triggers - SpaceClaim, scdm, /RunScript, IronPython, API V18, spur gear harness, SC_JOB_DIR.
---

# SpaceClaim 2020 R1 headless scripting

## Fixed environment facts (v201)

- Exe: `C:\Program Files\ANSYS Inc\v201\scdm\SpaceClaim.exe`. API is
  **V18** (`SpaceClaim.Api.V18`); recorded scripts start with
  `# Python Script, API Version = V18` — keep that header, never raise it.
- Headless invocation:
  `SpaceClaim.exe /RunScript="<abs path>.py" /Headless=True /Splash=False /Welcome=False /ExitAfterScript=True`
- In-app language is **IronPython 2.7**: no numpy/scipy/pip, no
  f-strings. Use `%` formatting and plain math. `print("x")` works.
- **API geometry units are METERS.** All mm values must be multiplied by
  0.001 before `Point2D.Create` etc.; `Shape.Volume` returns m³.
- Job contract (this repo): runner sets env var `SC_JOB_DIR`; the script
  reads `params.json` there and writes `result.json`, `gear.stp`,
  `gear.png`, `log.txt`. Pass data via this env var, **not**
  `/ScriptArgs` (version-fragile).
- Every launch = one license checkout + 20–60 s startup. Batch all of an
  iteration's work (build + measure + export) into ONE script run. Seat
  count caps parallelism — assume 1.

## Bootstrapping / repairing API calls ("learning the app")

The offline-written API section of a script WILL have wrong call
signatures. Repair procedure, once per operation type:

1. On the Windows box, open SpaceClaim → the **Script editor** (Design
   tab → Script). It records every manual GUI action as V18 Python.
2. Perform the operation once by hand (sketch a circle, extrude, cut,
   save as STEP/PNG).
3. Compare the recorded lines with the template's `VERIFY`-tagged calls;
   replace mismatches with the recorded form verbatim.
4. Re-run headless; when green, remove the VERIFY tag and add a "Learned
   gotchas" entry below if the fix was non-obvious.

The API class library reference is the local .chm:
`...\v201\scdm\SpaceClaim.Api.V18\Help\SpaceClaim.Api.V18.chm`.

## Known gotchas (seed list — append what the loop teaches)

- `ClearAll()` starts a fresh document in scripts; without it, reruns
  accumulate bodies and `body_count` checks fail.
- Sketch→solid transition: closed sketch loops only become faces after
  `ViewHelper.SetViewMode(InteractionMode.Solid)`. An unclosed polyline
  (duplicate/coincident endpoints) yields surfaces → `split_body`-style
  failures.
- Extrude-cut must be deeper than the part (use 1.2×face width) or a
  skin remains.
- Involute flanks are polylines (N≈14 per flank): expect the measured
  tip diameter up to ~2% under analytic `m(z+2)`; the verifier already
  allows this.
- z < 17 teeth: undercut is not modelled; below the base circle the
  flank is a radial straight — fine for harness validation, not for
  manufacturing.
- Exports: `DocumentSave.Execute(path)` picks format by extension
  (.stp, .png). If the recorded macro shows an options argument, copy it.

## Verification is analytic, not visual

`harness/verify.py` gates on: single body, bbox OD vs `m(z+2)`, bbox
height vs face width, volume inside the root/tip envelope, tooth count.
A PNG is only a sanity glance. When a check fails, fix the geometry
math or the API call — never widen a tolerance to pass.

## Defeature family (bulk FEA cleanup)

`sc_scripts/defeature.py` + `harness/defeature_batch.py` +
`harness/verify_defeature.py`; full guide in
`spaceclaim-harness/DEFEATURE.md`. Key facts:

- Three measured states: before / structure (post component-deletion) /
  after. Conservation checks reference **structure**, never before.
- Every deleted component is logged with its volume;
  `fastener_accounting` fails if volume disappears unlogged.
- `Fill.Execute` on a feature's faces removes-and-heals; wrap per-face
  in try/except and count failures - never let one stubborn fillet kill
  a batch.
- Recording session for this family: open STEP, delete a component,
  Prepare > Remove Rounds, Fill, save-as. If the macro records a
  power-selection (rounds by radius / holes by size), use it instead of
  the fallback face-geometry walk - much faster on assemblies.
- Batch = many files per session; use timeout_s ~1800 for assemblies.
