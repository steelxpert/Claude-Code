"""Writer for CalculiX .inp decks from a :class:`ccxio.model.Model`.

Reproduces the deck from ``model.cards``: every keyword block is emitted in
original order with its data lines verbatim, except ``*NODE`` blocks, whose
coordinate lines are regenerated from ``model.nodes`` — this is what makes
the writer useful after :func:`ccxio.seed_imperfection` has moved nodes.

Comments of the source deck are not preserved (the reader drops them), and
continuation lines were joined at read time; neither affects how ccx or
PrePoMax read the deck.

For a model built in memory without cards (e.g. from
:meth:`ccxio.frd_reader.FrdFile.as_model`), the mesh is written as plain
``*NODE`` / ``*ELEMENT`` blocks grouped by type, plus any sets.
"""

from __future__ import annotations

from typing import TextIO, Union

from .model import KeywordCard, Model

__all__ = ["write_inp"]


def write_inp(model: Model, target: Union[str, TextIO]) -> None:
    if hasattr(target, "write"):
        _write(model, target)  # type: ignore[arg-type]
    else:
        with open(target, "w", newline="\n") as f:
            _write(model, f)


def _write(model: Model, f: TextIO) -> None:
    if model.cards:
        for card in model.cards:
            f.write(_header_line(card))
            if card.keyword == "NODE":
                for line in card.data:
                    nid = int(line.split(",", 1)[0])
                    f.write(_node_line(nid, model.nodes[nid]))
            else:
                for line in card.data:
                    f.write(line + "\n")
        return

    # cards-free model: emit a minimal, complete mesh deck
    if model.name:
        f.write("*HEADING\n%s\n" % model.name)
    f.write("*NODE\n")
    for nid, xyz in model.nodes.items():
        f.write(_node_line(nid, xyz))
    by_type: dict = {}
    for el in model.elements.values():
        by_type.setdefault(el.type, []).append(el)
    for etype, els in by_type.items():
        f.write("*ELEMENT, TYPE=%s\n" % etype)
        for el in els:
            f.write("%d, %s\n" % (el.id, ", ".join(str(n) for n in el.nodes)))
    for name, ids in model.nsets.items():
        f.write("*NSET, NSET=%s\n" % name)
        _write_id_lines(f, ids)
    for name, ids in model.elsets.items():
        f.write("*ELSET, ELSET=%s\n" % name)
        _write_id_lines(f, ids)


def _header_line(card: KeywordCard) -> str:
    parts = ["*" + card.keyword]
    for k, v in card.params.items():
        parts.append(k if v is None else f"{k}={v}")
    return ", ".join(parts) + "\n"


def _node_line(nid: int, xyz) -> str:
    # repr() gives the shortest exact float representation; ccx reads it fine
    return "%d, %r, %r, %r\n" % (nid, xyz[0], xyz[1], xyz[2])


def _write_id_lines(f: TextIO, ids, per_line: int = 16) -> None:
    for start in range(0, len(ids), per_line):
        chunk = ids[start:start + per_line]
        f.write(", ".join(str(i) for i in chunk) + "\n")
