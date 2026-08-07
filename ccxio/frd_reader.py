"""Reader for CalculiX ASCII .frd result files.

Parses the format that ccx writes for ``*NODE FILE`` output with ASCII
format flag 1 (the default): node block, element block and nodal result
datasets. Values are read by column slicing, never by whitespace splitting —
adjacent negative values in .frd data lines run together without spaces
(`` 1.00000E-03-2.00000E-03``).

Connectivity of 20-node bricks and 15-node wedges is mapped back from the
.frd node order to the .inp order (the inverse of the permutation applied
by :mod:`ccxio.frd_writer`), so a mesh round-trips unchanged.

Calculated component records (``iexist`` = 1, e.g. the ``ALL`` magnitude of
a DISP dataset) carry no stored data and are dropped from the returned
components.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Union
import os

from .model import Element, Model
from .frd_writer import NodalResult, _PERMUTATION

__all__ = ["read_frd", "FrdFile", "FrdSyntaxError"]


class FrdSyntaxError(ValueError):
    pass


# frd element type id -> (representative ccx type name, node count).
# The .frd stores only the geometric shape; the original formulation
# (C3D8 vs C3D8R, S4 vs CPS4, B31 vs T3D2 ...) is not recoverable.
_FRD_TO_CCX: Dict[int, Tuple[str, int]] = {
    1: ("C3D8", 8), 2: ("C3D6", 6), 3: ("C3D4", 4),
    4: ("C3D20", 20), 5: ("C3D15", 15), 6: ("C3D10", 10),
    7: ("S3", 3), 8: ("S6", 6), 9: ("S4", 4), 10: ("S8", 8),
    11: ("B31", 2), 12: ("B32", 3),
}

# inverse of the writer's .inp -> .frd position permutation
_INV_PERMUTATION: Dict[int, Tuple[int, ...]] = {}
for _ftype, _perm in _PERMUTATION.items():
    inv = [0] * len(_perm)
    for _k, _p in enumerate(_perm):
        inv[_p] = _k
    _INV_PERMUTATION[_ftype] = tuple(inv)


@dataclass
class FrdFile:
    """Contents of one .frd file."""

    name: str = ""
    nodes: Dict[int, Tuple[float, float, float]] = field(default_factory=dict)
    elements: Dict[int, Element] = field(default_factory=dict)
    results: List[NodalResult] = field(default_factory=list)

    def as_model(self) -> Model:
        """Mesh portion as a :class:`Model` (no sets, no cards)."""
        return Model(name=self.name, nodes=dict(self.nodes),
                     elements=dict(self.elements))

    def result(self, name: str, index: int = 0) -> NodalResult:
        """The index-th result block named ``name`` (case-insensitive)."""
        hits = [r for r in self.results if r.name.upper() == name.upper()]
        return hits[index]


def read_frd(source: Union[str, os.PathLike]) -> FrdFile:
    with open(source, "r", errors="replace") as f:
        lines = f.read().splitlines()

    frd = FrdFile()
    pstep = (1, 1, 1)  # icounter, iinc, istep from the last 1PSTEP record
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        code = line[:6]
        if code == "    1C":
            frd.name = line[6:].strip()
            i += 1
        elif code == "    2C":
            _check_ascii(line, "node block")
            i = _read_nodes(lines, i + 1, frd)
        elif code == "    3C":
            _check_ascii(line, "element block")
            i = _read_elements(lines, i + 1, frd)
        elif line.startswith("    1PSTEP"):
            pstep = (
                _int_at(line, 24, 36, default=1),
                _int_at(line, 36, 48, default=1),
                _int_at(line, 48, 60, default=1),
            )
            i += 1
        elif line.startswith("  100C"):
            i = _read_result_block(lines, i, frd, pstep)
        elif line.strip() == "9999":
            break
        else:
            i += 1  # 1U records, other 1P parameter records, blanks
    return frd


# ---------------------------------------------------------------- helpers


def _check_ascii(header: str, what: str) -> None:
    flag = header[73:74].strip() or header.rstrip()[-1:]
    if flag not in ("1", "0"):
        raise FrdSyntaxError(
            f"{what}: format flag {flag!r} not supported "
            "(binary .frd files cannot be read; rerun ccx with ASCII output)"
        )


def _int_at(line: str, a: int, b: int, default: Optional[int] = None) -> int:
    s = line[a:b].strip()
    if not s:
        if default is None:
            raise FrdSyntaxError(f"expected integer in columns {a}:{b} of {line!r}")
        return default
    return int(s)


def _read_nodes(lines: List[str], i: int, frd: FrdFile) -> int:
    # " -1" + I10 node id + 3 x E12.5
    while i < len(lines):
        line = lines[i]
        if line.startswith(" -3"):
            return i + 1
        if line.startswith(" -1"):
            nid = _int_at(line, 3, 13)
            frd.nodes[nid] = (
                float(line[13:25]), float(line[25:37]), float(line[37:49])
            )
        i += 1
    raise FrdSyntaxError("node block not terminated by -3")


def _read_elements(lines: List[str], i: int, frd: FrdFile) -> int:
    n = len(lines)
    while i < n:
        line = lines[i]
        if line.startswith(" -3"):
            return i + 1
        if not line.startswith(" -1"):
            i += 1
            continue
        eid = _int_at(line, 3, 13)
        ftype = _int_at(line, 13, 18)
        if ftype not in _FRD_TO_CCX:
            raise FrdSyntaxError(f"element {eid}: unknown frd type {ftype}")
        ccx_type, nnodes = _FRD_TO_CCX[ftype]
        i += 1
        conn: List[int] = []
        while len(conn) < nnodes:
            if i >= n or not lines[i].startswith(" -2"):
                raise FrdSyntaxError(f"element {eid}: connectivity truncated")
            row = lines[i][3:]
            for start in range(0, len(row.rstrip()), 10):
                conn.append(int(row[start:start + 10]))
            i += 1
        if len(conn) != nnodes:
            raise FrdSyntaxError(
                f"element {eid}: {len(conn)} node ids, expected {nnodes}"
            )
        inv = _INV_PERMUTATION.get(ftype)
        nodes = tuple(conn) if inv is None else tuple(conn[k] for k in inv)
        frd.elements[eid] = Element(eid, ccx_type, nodes)
    raise FrdSyntaxError("element block not terminated by -3")


def _read_result_block(lines: List[str], i: int, frd: FrdFile,
                       pstep: Tuple[int, int, int]) -> int:
    header = lines[i]
    time = float(header[12:24])
    ictype = _int_at(header, 57, 58, default=0)
    i += 1
    n = len(lines)

    # -4 record: dataset name + component count (incl. calculated ones)
    if i >= n or not lines[i].startswith(" -4"):
        raise FrdSyntaxError(f"100CL block without -4 record near line {i}")
    name = lines[i][5:13].strip()
    i += 1

    # -5 records: keep only stored components (iexist != 1)
    stored: List[str] = []
    while i < n and lines[i].startswith(" -5"):
        comp = lines[i][5:13].strip()
        iexist = _int_at(lines[i], 33, 38, default=0)
        if iexist != 1:
            stored.append(comp)
        i += 1
    if not stored:
        raise FrdSyntaxError(f"result {name}: no stored components")

    values: Dict[int, Tuple[float, ...]] = {}
    ncomp = len(stored)
    while i < n:
        line = lines[i]
        if line.startswith(" -3"):
            i += 1
            break
        if not line.startswith(" -1"):
            raise FrdSyntaxError(f"unexpected line in result {name}: {line!r}")
        nid = _int_at(line, 3, 13)
        vals = _slice_values(line, min(ncomp, 6))
        i += 1
        got = len(vals)
        while got < ncomp:
            if i >= n or not lines[i].startswith(" -2"):
                raise FrdSyntaxError(f"result {name}, node {nid}: data truncated")
            vals += _slice_values(lines[i], min(ncomp - got, 6))
            got = len(vals)
            i += 1
        values[nid] = tuple(vals)

    frd.results.append(NodalResult(
        name=name,
        components=tuple(stored),
        values=values,
        step=pstep[2],
        increment=pstep[1],
        time=time,
        ictype=ictype,
    ))
    return i


def _slice_values(line: str, count: int) -> List[float]:
    # values start at column 13 on both -1 and -2 lines, 12 chars each
    out: List[float] = []
    for k in range(count):
        chunk = line[13 + 12 * k: 25 + 12 * k]
        if not chunk.strip():
            break
        out.append(float(chunk))
    return out
