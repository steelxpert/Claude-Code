# Defeaturing pipeline — bulk FEA geometry cleanup

Clean designer-supplied assemblies for FEA in bulk with headless
SpaceClaim 2020 R1: delete fasteners, remove fillets, fill small holes —
with per-file conservation verification and an audit manifest.

This is the production branch of the harness; the gear loop
(`README.md`) is its calibration piece. Same machinery, different
script family and verifier.

## Pipeline

```
folder of .stp/.step        recipe.json (your thresholds)
        │                          │
        ▼                          ▼
harness/defeature_batch.py  ── per file ──►  SpaceClaim /RunScript
                                             sc_scripts/defeature.py:
                                               open → measure BEFORE
                                               delete fastener components
                                               → measure STRUCTURE
                                               remove fillets ≤ r
                                               fill holes ≤ d
                                               → measure AFTER
                                               export clean.stp + PNGs
        │
        ▼
harness/verify_defeature.py  (conservation checks per file)
        │
        ▼
summary.md + summary.json    (the 5-minute review document)
```

## The recipe

`recipe.example.json` — copy per job and edit:

| Key | Meaning |
|---|---|
| `remove_fillets_below_r_mm` | fillet/round faces with radius ≤ this are removed (0 = skip) |
| `fill_holes_below_d_mm` | holes with diameter ≤ this are filled (0 = skip) |
| `delete_components_matching` | case-insensitive name fragments; matching components are deleted whole (bolts, nuts, DIN/ISO part numbers…) |
| `keep_components_matching` | overrides deletion — protect named parts |
| `volume_tolerance_pct` | allowed volume change of the structure through defeaturing (default 2 %) |
| `max_feature_failure_pct` | max share of selected features that may resist removal before the file FAILS (default 10 %) |

Thresholds are engineering judgement per job: an 8 mm hole may be
noise on a 2 t weldment and structure on a bracket. When in doubt,
run, read the manifest, adjust, rerun — runs are cheap after the first.

## Three measured states, not two

The script measures the model at three points: **before** (as
received), **structure** (after fastener deletion, before defeaturing),
and **after** (cleaned). Conservation is checked against *structure*,
not *before* — a deleted protruding bolt legitimately shrinks volume
and bbox, and is instead accounted item-by-item in the manifest.

## Verification (per file, deterministic)

| Check | Rule | Catches |
|---|---|---|
| `script_status` | script finished | crashes, bad input file |
| `selection_effective` | recipe matched something | wrong thresholds / unit mistake |
| `fastener_accounting` | (before − structure) volume = Σ manifest deletions ± 0.5 % | a body vanishing unlogged — the worst failure |
| `volume_conservation` | after vs structure within tolerance | a fill/round removal that mangled geometry |
| `bbox_conservation` | envelope unchanged ± 0.2 % | shifted or lost geometry |
| `body_count` | unchanged through defeaturing | parts split or merged by a bad heal |
| `feature_failures` | failures ≤ threshold | systematic Remove-Rounds trouble |

Failures that only *resist* (a stubborn fillet) are warnings with a
face list; the run continues and reports. Tested by defect injection:
`lost_body`, `volume_blown`, `nothing_removed`, `fill_failures`,
`script_error` — each must fail the batch (and does, in mock mode).

## Usage

Dry run anywhere (no license):

    python3 harness/defeature_batch.py --mock \
        --recipe recipe.example.json --in demo_in --out demo_out

Real run on the Windows box:

    python harness/defeature_batch.py --real --config config.json \
        --recipe job123_recipe.json --in P:\job123\step --out P:\job123\clean

Or conversationally, in `claude` in the project folder:
"Defeature every STEP in `P:\job123\step`: fillets under 5, holes
under 8, drop all DIN912/DIN933 fasteners, report to me."

Many files run in sequence per licensed launch-cycle; leave it running
over lunch or overnight.

## Review workflow (your part)

1. Open `summary.md` in the output folder: PASS/FAIL per file, ΔV %,
   deletion list with volumes, failed-feature counts.
2. Spot-check `before.png` / `after.png` for anything surprising.
3. Anything flagged: open that one part in the GUI, fix by hand or
   adjust the recipe and rerun the file.
4. `clean.stp` goes to meshing (PrePoMax, AxisVM, …).

The machine does the tedium; the judgement — thresholds and the final
scan — stays with the engineer signing the analysis.

## One-time teaching session (like the gear's)

The `VERIFY`-tagged API calls in `sc_scripts/defeature.py` must be
aligned once against a recorded macro. Record in the Script editor:
open a STEP → delete one component → Prepare ▸ Remove Rounds on a
selection → Fill on a hole → save-as STEP. Then tell Claude to repair
the tags and run the mock-to-real bring-up, same as the gear
(runbook Phase 4). If the recording shows a power-selection call for
rounds/holes, prefer it over the fallback face-walk in the template —
much faster on large assemblies.

## Known limits

- **95 %, not 100 %.** A diameter threshold cannot know a drain hole
  from a bolt hole in a load path. Keep-lists and your manifest review
  carry that judgement.
- **Remove Rounds fails sometimes** even in the GUI on tangled fillet
  chains — that is what `feature_failures` and the warning list are for.
- **Suppressed/graphics-only vendor parts** (STEP with no solid) show up
  as body-count surprises; the manifest makes them visible.
- **Midsurface extraction** is the natural next recipe on the same
  machinery — not scaffolded yet.
