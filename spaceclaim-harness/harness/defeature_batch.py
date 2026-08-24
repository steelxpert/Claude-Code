"""Bulk defeaturing driver: run one cleanup recipe over a folder of
STEP files, verify conservation per file, and write an engineer-facing
summary (summary.json + summary.md).

Mock mode (any OS):
    python3 harness/defeature_batch.py --mock --recipe recipe.example.json \
        --in demo_in --out demo_out
    python3 harness/defeature_batch.py --mock --defect lost_body ...
Real mode (Windows + SpaceClaim v201):
    python  harness/defeature_batch.py --real --config config.json \
        --recipe recipe.json --in P:\\job123\\step --out P:\\job123\\clean

Exit 0 only if EVERY file passed verification. The summary.md is the
5-minute review document: what was deleted, what was filled, what
failed, and the conservation numbers per file.
"""
import argparse
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verify_defeature
import mock_defeature


def run_one(path, recipe, args):
    params = dict(recipe, input=os.path.abspath(path))
    if args.mock:
        return mock_defeature.run(params, defect=args.defect)
    import runner
    cfg = runner.load_config(args.config) if args.config else {}
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    stem = os.path.splitext(os.path.basename(path))[0]
    return runner.run(
        script_path=os.path.join(base, "sc_scripts", "defeature.py"),
        params=params,
        job_dir=os.path.join(args.out, stem),
        exe=cfg.get("spaceclaim_exe", runner.DEFAULT_EXE),
        timeout_s=cfg.get("timeout_s", 1800),
    )


def summary_md(rows):
    lines = ["# Defeaturing batch summary", "",
             "| File | Result | dV vs structure | Fasteners deleted | "
             "Fillets | Holes | Warnings |",
             "|---|---|---|---|---|---|---|"]
    for r in rows:
        res, rep = r["result"], r["verification"]
        if res.get("status") != "ok":
            lines.append("| %s | ERROR | - | - | - | - | %s |"
                         % (r["file"], (res.get("error") or "")[:80]))
            continue
        st, af = res["structure"], res["after"]
        dv = 100.0 * (af["volume_mm3"] - st["volume_mm3"]) \
            / st["volume_mm3"] if st["volume_mm3"] else 0.0
        man = res["manifest"]
        fil, hol = man["fillets"], man["holes"]
        lines.append(
            "| %s | %s | %+.2f%% | %d (%.0f mm3) | %d/%d | %d/%d | %s |"
            % (r["file"], "PASS" if rep["passed"] else "**FAIL**", dv,
               len(man["deleted_components"]),
               sum(d["volume_mm3"] for d in man["deleted_components"]),
               fil["removed"], fil["selected"],
               hol["filled"], hol["selected"],
               "; ".join(rep["warnings"]) or "-"))
    failed = [r for r in rows if not r["verification"]["passed"]]
    lines += ["", "%d file(s), %d failed verification."
              % (len(rows), len(failed)), ""]
    for r in rows:
        man = (r["result"].get("manifest") or {})
        dels = man.get("deleted_components", [])
        if dels:
            lines.append("## Deleted from %s" % r["file"])
            for d in dels:
                lines.append("- %s (%.0f mm3)" % (d["name"],
                                                  d["volume_mm3"]))
            lines.append("")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--recipe", required=True)
    ap.add_argument("--in", dest="indir", required=True)
    ap.add_argument("--out", required=True)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--mock", action="store_true")
    mode.add_argument("--real", action="store_true")
    ap.add_argument("--defect", default=None,
                    help="mock only: lost_body|volume_blown|"
                         "nothing_removed|fill_failures|script_error")
    ap.add_argument("--config", default=None)
    args = ap.parse_args(argv)

    with open(args.recipe) as fh:
        recipe = json.load(fh)
    files = sorted(glob.glob(os.path.join(args.indir, "*.st*p")))
    if not files:
        print("no .stp/.step files in %s" % args.indir)
        return 2
    os.makedirs(args.out, exist_ok=True)

    rows = []
    for path in files:
        result = run_one(path, recipe, args)
        report = verify_defeature.verify(result, recipe)
        rows.append({"file": os.path.basename(path), "result": result,
                     "verification": report})

    with open(os.path.join(args.out, "summary.json"), "w") as fh:
        json.dump(rows, fh, indent=2)
    md = summary_md(rows)
    with open(os.path.join(args.out, "summary.md"), "w") as fh:
        fh.write(md)
    print(md)
    return 0 if all(r["verification"]["passed"] for r in rows) else 1


if __name__ == "__main__":
    sys.exit(main())
