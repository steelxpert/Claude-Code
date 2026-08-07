"""Writer for CalculiX .frd result files (ASCII), cgx/PrePoMax compatible.

Every line format here is transcribed from the CalculiX sources
(frd.c, frdheader.c, frdselect.c, frdvector.c, Guido Dhondt, GPLv2), so the
output is byte-compatible with what ccx itself writes:

  * model header  ``    1C`` + ``    1U`` records
  * node block    ``    2C`` header, `` -1`` lines ``%10d %12.5E x3``, `` -3``
  * element block ``    3C`` header, `` -1`` definition + `` -2`` connectivity
    (max 10 node ids per line), `` -3``
  * result blocks ``    1PSTEP`` + ``  100CL`` headers, `` -4``/`` -5``
    component records, `` -1``/`` -2`` nodal data lines, `` -3``
  * `` 9999`` terminator

Node ordering quirk: 20-node bricks and 15-node wedges are stored in .frd
with the top-face mid-edge nodes *after* the vertical mid-edge nodes,
i.e. the .inp groups 13-16 / 17-20 (he20) and 10-12 / 13-15 (pe15) swap.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, TextIO, Tuple, Union

from .model import Model

__all__ = ["NodalResult", "write_frd", "FrdWriteError", "frd_element_type"]


class FrdWriteError(ValueError):
    pass


# frd element type id -> node count (cgx manual, "Element Types")
_FRD_NNODES = {1: 8, 2: 6, 3: 4, 4: 20, 5: 15, 6: 10,
               7: 3, 8: 6, 9: 4, 10: 8, 11: 2, 12: 3}

# CalculiX element name prefix -> frd type id.  Longest prefix wins, so
# C3D20R / C3D20RI resolve through "C3D20", S8R through "S8", etc.
_CCX_TO_FRD = {
    "C3D20": 4, "C3D15": 5, "C3D10": 6, "C3D8": 1, "C3D6": 2, "C3D4": 3,
    "F3D8": 1, "F3D6": 2, "F3D4": 3,
    "CPS8": 10, "CPE8": 10, "CAX8": 10, "M3D8": 10, "S8": 10,
    "CPS6": 8, "CPE6": 8, "CAX6": 8, "M3D6": 8, "S6": 8,
    "CPS4": 9, "CPE4": 9, "CAX4": 9, "M3D4": 9, "S4": 9,
    "CPS3": 7, "CPE3": 7, "CAX3": 7, "M3D3": 7, "S3": 7,
    "B32": 12, "T3D3": 12,
    "B31": 11, "B21": 11, "T3D2": 11, "T2D2": 11,
}
_CCX_PREFIXES = sorted(_CCX_TO_FRD, key=len, reverse=True)

# .inp -> .frd connectivity permutation (0-based positions), from frd.c:
# he20 writes nodes 1-12, then 17-20, then 13-16; pe15 writes 1-9, then
# 13-15, then 10-12.  All other types pass through unchanged.
_PERMUTATION = {
    4: tuple(range(12)) + (16, 17, 18, 19) + (12, 13, 14, 15),
    5: tuple(range(9)) + (12, 13, 14) + (9, 10, 11),
}


def frd_element_type(ccx_type: str) -> Optional[int]:
    """frd type id for a CalculiX element name, or None if not mappable."""
    t = ccx_type.upper()
    for p in _CCX_PREFIXES:
        if t.startswith(p):
            return _CCX_TO_FRD[p]
    return None


@dataclass
class NodalResult:
    """One nodal result block (one ``100CL`` dataset).

    name:       dataset name as shown in cgx/PrePoMax (e.g. "DISP", "STRESS").
    components: component names (e.g. ("D1","D2","D3") or the 6 stress comps).
    values:     node id -> tuple of component values (len == len(components)).
    step, increment: written to the 1PSTEP record.
    time:       step time / frequency / buckling factor for the 100CL record.
    ictype:     analysis type of the 100CL record: 0 static, 1 time step,
                2 frequency, 3 load step, 4 user named (ccx uses 4 for
                buckling); default 0.
    vector_all: for 3-component vectors, append the calculated "ALL"
                component record exactly like ccx does for DISP (default on;
                ignored for non-3-component results).
    """

    name: str
    components: Tuple[str, ...]
    values: Dict[int, Tuple[float, ...]]
    step: int = 1
    increment: int = 1
    time: float = 1.0
    ictype: int = 0
    vector_all: bool = True


def write_frd(
    model: Model,
    target: Union[str, TextIO],
    results: Sequence[NodalResult] = (),
    model_name: Optional[str] = None,
) -> None:
    """Write ``model`` (and optional nodal results) as an ASCII .frd file.

    Elements whose type has no frd shape (springs, dashpots, masses) are
    skipped, matching ccx, which never shows them in the frd either.
    """
    if hasattr(target, "write"):
        _write(model, target, results, model_name)  # type: ignore[arg-type]
    else:
        with open(target, "w", newline="\n") as f:
            _write(model, f, results, model_name)


# ---------------------------------------------------------------- internals


def _write(model: Model, f: TextIO, results: Sequence[NodalResult],
           model_name: Optional[str]) -> None:
    name = model_name if model_name is not None else (model.name or "Model")
    f.write(f"    1C{name[:66]}\n")
    f.write("    1UUSER\n")
    f.write("    1UPGM               ccxio\n")

    # ---- node block: "    2C" + 18 blanks + %12d count + %38d format(1=asc)
    f.write("    2C" + " " * 18 + "%12d%38d\n" % (len(model.nodes), 1))
    for nid, (x, y, z) in model.nodes.items():
        f.write(" -1%10d%12.5E%12.5E%12.5E\n" % (nid, x, y, z))
    f.write(" -3\n")

    # ---- element block
    writable = []
    for el in model.elements.values():
        ftype = frd_element_type(el.type)
        if ftype is None:
            continue
        if len(el.nodes) != _FRD_NNODES[ftype]:
            raise FrdWriteError(
                f"element {el.id} ({el.type}) has {len(el.nodes)} nodes, "
                f"frd type {ftype} needs {_FRD_NNODES[ftype]}"
            )
        writable.append((el, ftype))

    f.write("    3C" + " " * 18 + "%12d%38d\n" % (len(writable), 1))
    for el, ftype in writable:
        # " -1" elem-id, type, group (0), material (1); then " -2" lines
        # with at most 10 node ids of 10 chars each.
        f.write(" -1%10d%5d%5d%5d\n" % (el.id, ftype, 0, 1))
        perm = _PERMUTATION.get(ftype)
        conn = el.nodes if perm is None else tuple(el.nodes[p] for p in perm)
        for start in range(0, len(conn), 10):
            chunk = conn[start:start + 10]
            f.write(" -2" + "".join("%10d" % n for n in chunk) + "\n")
    f.write(" -3\n")

    # ---- nodal result blocks
    icounter = 0  # loadcase counter over the whole file (1PSTEP record)
    kode = 0      # increment counter over the whole file (100CL record)
    for res in results:
        icounter += 1
        kode += 1
        _write_result_block(f, res, icounter, kode)

    f.write(" 9999\n")


def _write_result_block(f: TextIO, res: NodalResult,
                        icounter: int, kode: int) -> None:
    ncomp = len(res.components)
    for vals in res.values.values():
        if len(vals) != ncomp:
            raise FrdWriteError(
                f"{res.name}: value tuple of length {len(vals)}, "
                f"expected {ncomp}"
            )

    f.write(_pstep_line(icounter, res.increment, res.step))
    f.write(_100cl_line(len(res.values), res.time, kode, res.ictype))

    is_vector = ncomp == 3 and res.vector_all
    is_tensor = ncomp == 6
    # entity records: " -4" name + ncomps + irtype(1 = nodal data)
    f.write(" -4  %-8s%5d%5d\n" % (res.name[:8], ncomp + (1 if is_vector else 0), 1))
    if is_vector:
        for j, comp in enumerate(res.components, start=1):
            f.write(" -5  %-8s%5d%5d%5d%5d\n" % (comp[:8], 1, 2, j, 0))
        f.write(" -5  %-8s%5d%5d%5d%5d%5d%s\n" % ("ALL", 1, 2, 0, 0, 1, "ALL"))
    elif is_tensor:
        # symmetric tensor component index pairs, ccx order XX YY ZZ XY YZ ZX
        pairs = ((1, 1), (2, 2), (3, 3), (1, 2), (2, 3), (3, 1))
        for comp, (i1, i2) in zip(res.components, pairs):
            f.write(" -5  %-8s%5d%5d%5d%5d\n" % (comp[:8], 1, 4, i1, i2))
    else:
        for comp in res.components:
            f.write(" -5  %-8s%5d%5d%5d%5d\n" % (comp[:8], 1, 1, 0, 0))

    # data: " -1" node + up to 6 values per line, continuation " -2" + 10 blanks
    for nid, vals in res.values.items():
        f.write(" -1%10d" % nid)
        f.write("".join("%12.5E" % v for v in vals[:6]))
        f.write("\n")
        for start in range(6, ncomp, 6):
            f.write(" -2" + " " * 10)
            f.write("".join("%12.5E" % v for v in vals[start:start + 6]))
            f.write("\n")
    f.write(" -3\n")


def _pstep_line(icounter: int, iinc: int, istep: int) -> str:
    # frdheader.c: "    1PSTEP" padded to 70, ints at columns 24, 36, 48
    text = list("    1PSTEP".ljust(70))
    text[24:36] = "%12d" % icounter
    text[36:48] = "%12d" % iinc
    text[48:60] = "%12d" % istep
    return "".join(text) + "\n"


def _100cl_line(numnod: int, time: float, kode: int, ictype: int) -> str:
    # frdheader.c 100CL template, 75 chars, format flag '1' (ascii) at col 74
    text = list("  100CL       .00000E+00                                 0    1".ljust(75))
    text[7:12] = "%5d" % (100 + kode)
    text[12:24] = _fmt_time(time)
    text[24:36] = "%12d" % numnod
    text[57] = "%1d" % ictype
    text[58:63] = "%5d" % kode
    text[74] = "1"
    return "".join(text) + "\n"


def _fmt_time(t: float) -> str:
    # frdheader.c since 2018: fixed point with 10 significant digits for
    # 1 <= t < 1e10, scientific otherwise.
    if t <= 0.0:
        return "%12.5E" % t
    lg = math.log10(t)
    if 0 <= lg < 10:
        ncomma = 10 - int(math.floor(lg + 1.0))
        return "%12.*f" % (ncomma, t)
    return "%12.5E" % t
