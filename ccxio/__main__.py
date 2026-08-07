"""ccxio command line.

    ccxio convert model.inp [-o model.frd] [--name TITLE]
        Write the .inp mesh as a viewable .frd (no solve needed).

    ccxio seed model.inp modes.frd --amplitude 0.64 [--mode 1] [-o seeded.inp]
        Add a scaled .frd displacement dataset (e.g. a *BUCKLE eigenmode)
        to the mesh and write the perturbed deck.

``ccxio model.inp`` (no subcommand) is shorthand for ``convert``.
"""

from __future__ import annotations

import argparse
import os
import sys

from . import (
    __version__,
    frd_element_type,
    read_frd,
    read_inp,
    seed_imperfection,
    write_frd,
    write_inp,
)


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] not in ("convert", "seed", "-h", "--help", "--version"):
        argv.insert(0, "convert")  # backward-compatible: ccxio model.inp

    ap = argparse.ArgumentParser(
        prog="ccxio",
        description="CalculiX .inp/.frd tools.",
    )
    ap.add_argument("--version", action="version", version=f"ccxio {__version__}")
    sub = ap.add_subparsers(dest="cmd", required=True)

    ap_c = sub.add_parser("convert", help="convert an .inp mesh to .frd")
    ap_c.add_argument("inp", help="input .inp file")
    ap_c.add_argument("-o", "--output", help="output .frd path "
                      "(default: input name with .frd extension)")
    ap_c.add_argument("--name", help="model name written to the frd header")

    ap_s = sub.add_parser(
        "seed", help="seed a geometric imperfection from an .frd mode shape"
    )
    ap_s.add_argument("inp", help="perfect-geometry .inp deck")
    ap_s.add_argument("frd", help=".frd with displacement datasets "
                      "(e.g. a *BUCKLE result)")
    group = ap_s.add_mutually_exclusive_group(required=True)
    group.add_argument("--amplitude", type=float,
                       help="scale mode to this peak displacement magnitude")
    group.add_argument("--scale", type=float, help="raw multiplication factor")
    ap_s.add_argument("--mode", type=int, default=1,
                      help="which displacement dataset to use, 1-based in "
                      "file order (default 1 = first mode)")
    ap_s.add_argument("--dataset", default="DISP",
                      help="dataset name to look for (default DISP)")
    ap_s.add_argument("-o", "--output", help="output .inp path "
                      "(default: input name + '_imperfect.inp')")

    args = ap.parse_args(argv)
    return _convert(args) if args.cmd == "convert" else _seed(args)


def _convert(args) -> int:
    model = read_inp(args.inp)
    out = args.output or os.path.splitext(args.inp)[0] + ".frd"

    skipped = sorted({el.type for el in model.elements.values()
                      if frd_element_type(el.type) is None})
    write_frd(model, out, model_name=args.name)

    n_written = sum(1 for el in model.elements.values()
                    if frd_element_type(el.type) is not None)
    print(f"{out}: {len(model.nodes)} nodes, {n_written} elements")
    if skipped:
        print(f"warning: skipped element types without an frd shape: "
              f"{', '.join(skipped)}", file=sys.stderr)
    return 0


def _seed(args) -> int:
    model = read_inp(args.inp)
    frd = read_frd(args.frd)

    hits = [r for r in frd.results
            if r.name.upper() == args.dataset.upper()
            and len(r.components) >= 3]
    if not hits:
        print(f"error: no {args.dataset} dataset with >=3 components in "
              f"{args.frd}", file=sys.stderr)
        return 1
    if not 1 <= args.mode <= len(hits):
        print(f"error: --mode {args.mode} out of range, {args.frd} has "
              f"{len(hits)} {args.dataset} dataset(s)", file=sys.stderr)
        return 1
    mode = hits[args.mode - 1]

    seeded = seed_imperfection(
        model, mode, amplitude=args.amplitude, scale=args.scale
    )
    out = args.output or os.path.splitext(args.inp)[0] + "_imperfect.inp"
    write_inp(seeded, out)

    how = (f"amplitude {args.amplitude}" if args.amplitude is not None
           else f"scale {args.scale}")
    print(f"{out}: seeded {args.dataset} dataset {args.mode} "
          f"(time/factor {mode.time:g}) at {how}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
