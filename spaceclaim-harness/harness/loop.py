"""One iteration of the generate -> build -> measure -> verify loop.

Mock mode (any OS):
    python3 harness/loop.py --mock --module 2 --teeth 24 --face-width 12
    python3 harness/loop.py --mock --defect missing_tooth ...
Real mode (Windows box with SpaceClaim 2020 R1):
    python  harness/loop.py --real --config config.json --module 2 --teeth 24

Exit code 0 = verified, 1 = failed. The JSON report on stdout is what
the outer agent (Claude) reads to decide the next fix.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gear_math
import verify as verify_mod
import mock_backend


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--module", type=float, default=2.0)
    ap.add_argument("--teeth", type=int, default=24)
    ap.add_argument("--pressure-angle", type=float, default=20.0)
    ap.add_argument("--face-width", type=float, default=12.0)
    ap.add_argument("--bore", type=float, default=0.0)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--mock", action="store_true")
    mode.add_argument("--real", action="store_true")
    ap.add_argument("--defect", default=None,
                    help="mock only: missing_tooth|half_width|split_body|"
                         "blank_disk|script_error")
    ap.add_argument("--config", default=None,
                    help="real only: path to config.json")
    ap.add_argument("--job-dir", default=None)
    args = ap.parse_args(argv)

    params = {
        "module": args.module,
        "teeth": args.teeth,
        "pressure_angle_deg": args.pressure_angle,
        "face_width": args.face_width,
        "bore_d": args.bore,
    }
    exp = gear_math.expectations(args.module, args.teeth,
                                 args.pressure_angle, args.face_width,
                                 args.bore)

    if args.mock:
        result = mock_backend.run(params, defect=args.defect)
    else:
        import runner
        cfg = runner.load_config(args.config) if args.config else {}
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        job_dir = args.job_dir or os.path.join(base, "jobs",
                                               "gear_m%g_z%d" % (args.module,
                                                                 args.teeth))
        result = runner.run(
            script_path=os.path.join(base, "sc_scripts", "spur_gear.py"),
            params=params,
            job_dir=job_dir,
            exe=cfg.get("spaceclaim_exe", runner.DEFAULT_EXE),
            timeout_s=cfg.get("timeout_s", 600),
        )

    report = verify_mod.verify(result, exp)
    out = {"params": params, "expected": exp, "measured": result,
           "verification": report}
    json.dump(out, sys.stdout, indent=2)
    print()
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
