"""CLI: convert a CalculiX .inp mesh to a viewable .frd file.

    python -m ccxio model.inp [-o model.frd] [--name TITLE]

Writes the mesh (nodes + elements) as an .frd that cgx and PrePoMax open
directly; useful for inspecting generated meshes without running a solve.
"""

from __future__ import annotations

import argparse
import os
import sys

from . import __version__, read_inp, write_frd, frd_element_type


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        prog="ccxio",
        description="Convert a CalculiX .inp mesh to a cgx/PrePoMax .frd file.",
    )
    ap.add_argument("inp", help="input .inp file")
    ap.add_argument("-o", "--output", help="output .frd path "
                    "(default: input name with .frd extension)")
    ap.add_argument("--name", help="model name written to the frd header")
    ap.add_argument("--version", action="version", version=f"ccxio {__version__}")
    args = ap.parse_args(argv)

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


if __name__ == "__main__":
    sys.exit(main())
