"""Seed geometric imperfections by perturbing nodal coordinates.

CalculiX has no ``*IMPERFECTION`` keyword, so imperfect geometry is made by
adding a scaled displacement field (typically a ``*BUCKLE`` eigenmode read
from the .frd) to the perfect mesh:

    from ccxio import read_inp, read_frd, seed_imperfection, write_inp

    model = read_inp("member.inp")
    modes = read_frd("member_buckle.frd")
    mode1 = modes.result("DISP", 0)          # first eigenmode
    seeded = seed_imperfection(model, mode1, amplitude=0.64)  # mm
    write_inp(seeded, "member_imperfect.inp")

For mode combinations call :func:`seed_imperfection` repeatedly, once per
mode, each with its own amplitude.
"""

from __future__ import annotations

import math
from typing import Dict, Mapping, Optional, Sequence, Tuple, Union

from .frd_writer import NodalResult
from .model import Model

__all__ = ["seed_imperfection", "ImperfectionError"]

FieldLike = Union[NodalResult, Mapping[int, Sequence[float]]]


class ImperfectionError(ValueError):
    pass


def seed_imperfection(
    model: Model,
    mode: FieldLike,
    amplitude: Optional[float] = None,
    scale: Optional[float] = None,
) -> Model:
    """Return a copy of ``model`` with nodes displaced by a scaled field.

    mode:      a :class:`NodalResult` with at least 3 components (the first
               three are taken as dx, dy, dz — ccx DISP order), or a plain
               mapping ``{node id: (dx, dy, dz)}``.
    amplitude: scale the field so its peak displacement *magnitude* equals
               this value (the usual way: eigenmodes come normalised to a
               unit peak, the amplitude is the physical imperfection, e.g.
               a fraction of the plate width or member length).
    scale:     multiply the field by this raw factor instead.

    Exactly one of ``amplitude`` / ``scale`` must be given.  Nodes missing
    from the field stay put; field entries for unknown nodes are ignored.
    The returned model shares cards/sets/elements with the input (they are
    unaffected by moving nodes); only the node table is new.
    """
    if (amplitude is None) == (scale is None):
        raise ImperfectionError("give exactly one of amplitude= or scale=")

    disp = _as_displacements(mode)

    if amplitude is not None:
        peak = max(
            (math.sqrt(dx * dx + dy * dy + dz * dz)
             for nid, (dx, dy, dz) in disp.items() if nid in model.nodes),
            default=0.0,
        )
        if peak == 0.0:
            raise ImperfectionError(
                "field has zero peak magnitude on this mesh; cannot scale "
                "to an amplitude"
            )
        factor = amplitude / peak
    else:
        factor = scale  # type: ignore[assignment]

    nodes: Dict[int, Tuple[float, float, float]] = {}
    for nid, (x, y, z) in model.nodes.items():
        d = disp.get(nid)
        if d is None:
            nodes[nid] = (x, y, z)
        else:
            nodes[nid] = (x + factor * d[0], y + factor * d[1], z + factor * d[2])

    return Model(
        name=model.name,
        nodes=nodes,
        elements=model.elements,
        nsets=model.nsets,
        elsets=model.elsets,
        cards=model.cards,
    )


def _as_displacements(mode: FieldLike) -> Mapping[int, Sequence[float]]:
    if isinstance(mode, NodalResult):
        if len(mode.components) < 3:
            raise ImperfectionError(
                f"result {mode.name!r} has {len(mode.components)} components; "
                "a displacement field needs 3"
            )
        return mode.values
    for nid, d in mode.items():
        if len(d) < 3:
            raise ImperfectionError(f"node {nid}: need (dx, dy, dz), got {d!r}")
        break
    return mode
