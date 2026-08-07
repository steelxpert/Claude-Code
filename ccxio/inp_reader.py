"""Reader for CalculiX / Abaqus-style .inp input decks.

Parses the mesh (nodes, elements, node/element sets) into a
:class:`ccxio.model.Model` and keeps every keyword block verbatim in
``model.cards`` so downstream code can inspect materials, steps, BCs, etc.

Format rules honoured here:
  * ``**`` comment lines are dropped anywhere in the deck.
  * Keywords and parameters are case-insensitive; keyword names may contain
    spaces ("NODE FILE" is a different keyword than "NODE").
  * A line ending in a comma continues on the next line (both keyword and
    data lines).  Element connectivity is additionally completed by node
    count for known element types, so decks whose continuation lines lack
    the trailing comma still parse.
  * ``*INCLUDE, INPUT=file`` is inlined, relative to the including file.
  * ``*NSET``/``*ELSET`` support ``GENERATE`` and references to previously
    or later defined sets; references are resolved after the whole deck is
    read.  Repeated definitions of the same set append, as in CalculiX.
"""

from __future__ import annotations

import os
from typing import Dict, Iterable, List, Optional, Tuple, Union

from .model import Element, KeywordCard, Model

__all__ = ["read_inp", "InpSyntaxError"]


class InpSyntaxError(ValueError):
    pass


# Node counts for common CalculiX element types, used to keep consuming
# connectivity lines when a mesher omitted the trailing continuation comma.
# Prefix-matched, longest prefix first (C3D20RI, S8R5, CPE4R... all resolve).
_ELEM_NNODES: Dict[str, int] = {
    "C3D20": 20, "C3D15": 15, "C3D10": 10, "C3D8": 8, "C3D6": 6, "C3D4": 4,
    "F3D8": 8, "F3D6": 6, "F3D4": 4,
    "CPS8": 8, "CPE8": 8, "CAX8": 8, "M3D8": 8, "S8": 8,
    "CPS6": 6, "CPE6": 6, "CAX6": 6, "M3D6": 6, "S6": 6,
    "CPS4": 4, "CPE4": 4, "CAX4": 4, "M3D4": 4, "S4": 4,
    "CPS3": 3, "CPE3": 3, "CAX3": 3, "M3D3": 3, "S3": 3,
    "B31": 2, "B21": 2, "T3D2": 2, "T2D2": 2,
    "B32": 3, "T3D3": 3,
    "SPRINGA": 2, "SPRING2": 2, "SPRING1": 1,
    "DASHPOTA": 2, "MASS": 1, "DCOUP3D": 1, "GAPUNI": 2,
}
_ELEM_PREFIXES = sorted(_ELEM_NNODES, key=len, reverse=True)


def nnodes_for_type(elem_type: str) -> Optional[int]:
    """Node count for a CalculiX element type name, or None if unknown."""
    t = elem_type.upper()
    for p in _ELEM_PREFIXES:
        if t.startswith(p):
            return _ELEM_NNODES[p]
    return None


def read_inp(source: Union[str, os.PathLike, Iterable[str]]) -> Model:
    """Read a CalculiX .inp deck.

    ``source`` is a file path, or any iterable of lines (then *INCLUDE
    paths resolve against the current working directory).
    """
    if isinstance(source, (str, os.PathLike)) and "\n" not in str(source):
        base = os.path.dirname(os.path.abspath(source))
        with open(source, "r", errors="replace") as f:
            raw = f.readlines()
    else:
        base = os.getcwd()
        if isinstance(source, str):
            raw = source.splitlines()
        else:
            raw = list(source)

    lines = _expand_includes(raw, base)
    model = Model()
    # Set entries may reference other sets by name; collect raw entries
    # first and resolve names once the whole deck is known.
    raw_nsets: Dict[str, List[Union[int, str]]] = {}
    raw_elsets: Dict[str, List[Union[int, str]]] = {}

    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        if not line.startswith("*"):
            # Stray data line outside any block (or deck starts with data):
            # CalculiX would reject this; be strict so errors surface early.
            raise InpSyntaxError(f"data line outside keyword block: {line!r}")

        header, i = _read_logical_line(lines, i)
        keyword, params = _parse_keyword(header)
        card = KeywordCard(keyword, params)
        model.cards.append(card)

        if keyword == "ELEMENT":
            i = _read_element_block(lines, i, card, params, model, raw_elsets)
        else:
            # Generic data collection for every other keyword.
            while i < n and not lines[i].startswith("*"):
                data, i = _read_logical_line(lines, i)
                card.data.append(data)
            if keyword == "HEADING":
                if card.data and not model.name:
                    model.name = card.data[0]
            elif keyword == "NODE":
                _parse_nodes(card, params, model, raw_nsets)
            elif keyword == "NSET":
                _parse_set(card, params, "NSET", raw_nsets)
            elif keyword == "ELSET":
                _parse_set(card, params, "ELSET", raw_elsets)

    # *ELEMENT, ELSET=... contributions were appended as ints already.
    model.nsets = _resolve_sets(raw_nsets, "node")
    model.elsets = _resolve_sets(raw_elsets, "element")
    return model


# ---------------------------------------------------------------- helpers


def _clean(line: str) -> Optional[str]:
    """Strip comments/whitespace; None for lines to drop."""
    s = line.rstrip("\n\r").strip()
    if not s or s.startswith("**"):
        return None
    return s


def _expand_includes(raw: List[str], base: str) -> List[str]:
    out: List[str] = []
    for line in raw:
        s = _clean(line)
        if s is None:
            continue
        if s.upper().replace(" ", "").startswith("*INCLUDE"):
            _, params = _parse_keyword(s)
            path = params.get("INPUT")
            if not path:
                raise InpSyntaxError(f"*INCLUDE without INPUT= : {s!r}")
            if not os.path.isabs(path):
                path = os.path.join(base, path)
            with open(path, "r", errors="replace") as f:
                out.extend(_expand_includes(f.readlines(), os.path.dirname(path)))
        else:
            out.append(s)
    return out


def _read_logical_line(lines: List[str], i: int) -> Tuple[str, int]:
    """Join trailing-comma continuations starting at lines[i]."""
    parts = [lines[i]]
    i += 1
    while parts[-1].endswith(",") and i < len(lines) and not lines[i].startswith("*"):
        parts.append(lines[i])
        i += 1
    return "".join(parts), i


def _parse_keyword(header: str) -> Tuple[str, Dict[str, Optional[str]]]:
    body = header.lstrip("*")
    fields = [f.strip() for f in body.split(",")]
    keyword = " ".join(fields[0].upper().split())
    params: Dict[str, Optional[str]] = {}
    for f in fields[1:]:
        if not f:
            continue
        if "=" in f:
            k, v = f.split("=", 1)
            params[" ".join(k.upper().split())] = v.strip()
        else:
            params[" ".join(f.upper().split())] = None
    return keyword, params


def _parse_nodes(
    card: KeywordCard,
    params: Dict[str, Optional[str]],
    model: Model,
    raw_nsets: Dict[str, List[Union[int, str]]],
) -> None:
    nset = params.get("NSET")
    collected: List[int] = []
    for data in card.data:
        toks = [t for t in (x.strip() for x in data.split(",")) if t]
        if not toks:
            continue
        try:
            nid = int(toks[0])
            coords = [float(t) for t in toks[1:4]]
        except ValueError as e:
            raise InpSyntaxError(f"bad node line: {data!r}") from e
        coords += [0.0] * (3 - len(coords))
        model.nodes[nid] = (coords[0], coords[1], coords[2])
        collected.append(nid)
    if nset:
        raw_nsets.setdefault(nset.upper(), []).extend(collected)


def _read_element_block(
    lines: List[str],
    i: int,
    card: KeywordCard,
    params: Dict[str, Optional[str]],
    model: Model,
    raw_elsets: Dict[str, List[Union[int, str]]],
) -> int:
    etype = (params.get("TYPE") or "").upper()
    if not etype:
        raise InpSyntaxError("*ELEMENT without TYPE=")
    elset = params.get("ELSET")
    expect = nnodes_for_type(etype)
    ids: List[int] = []

    n = len(lines)
    while i < n and not lines[i].startswith("*"):
        data, i = _read_logical_line(lines, i)
        toks = [t for t in (x.strip() for x in data.split(",")) if t]
        # A known type may span extra lines even without trailing commas.
        while expect is not None and len(toks) < 1 + expect and i < n \
                and not lines[i].startswith("*"):
            more, i = _read_logical_line(lines, i)
            toks += [t for t in (x.strip() for x in more.split(",")) if t]
        card.data.append(data)
        try:
            eid = int(toks[0])
            conn = tuple(int(t) for t in toks[1:])
        except ValueError as e:
            raise InpSyntaxError(f"bad element line: {data!r}") from e
        if expect is not None and len(conn) != expect:
            raise InpSyntaxError(
                f"element {eid} ({etype}) has {len(conn)} nodes, expected {expect}"
            )
        model.elements[eid] = Element(eid, etype, conn)
        ids.append(eid)

    if elset:
        # Merged with any *ELSET blocks of the same name at resolve time.
        raw_elsets.setdefault(elset.upper(), []).extend(ids)
    return i


def _parse_set(
    card: KeywordCard,
    params: Dict[str, Optional[str]],
    name_param: str,
    store: Dict[str, List[Union[int, str]]],
) -> None:
    name = params.get(name_param)
    if not name:
        raise InpSyntaxError(f"*{name_param} without {name_param}= parameter")
    entries = store.setdefault(name.upper(), [])
    generate = "GENERATE" in params
    for data in card.data:
        toks = [t for t in (x.strip() for x in data.split(",")) if t]
        if not toks:
            continue
        if generate:
            if len(toks) < 2:
                raise InpSyntaxError(f"GENERATE line needs first,last[,inc]: {data!r}")
            first, last = int(toks[0]), int(toks[1])
            inc = int(toks[2]) if len(toks) > 2 else 1
            entries.extend(range(first, last + 1, inc))
        else:
            for t in toks:
                try:
                    entries.append(int(t))
                except ValueError:
                    entries.append(t.upper())  # reference to another set


def _resolve_sets(
    raw: Dict[str, List[Union[int, str]]], kind: str
) -> Dict[str, Tuple[int, ...]]:
    resolved: Dict[str, Tuple[int, ...]] = {}
    resolving: set = set()

    def resolve(name: str) -> Tuple[int, ...]:
        if name in resolved:
            return resolved[name]
        if name in resolving:
            raise InpSyntaxError(f"circular {kind} set reference: {name}")
        resolving.add(name)
        out: List[int] = []
        for e in raw[name]:
            if isinstance(e, int):
                out.append(e)
            elif e in raw:
                out.extend(resolve(e))
            else:
                raise InpSyntaxError(f"unknown {kind} set referenced: {e} (in {name})")
        resolving.discard(name)
        resolved[name] = tuple(out)
        return resolved[name]

    for name in raw:
        resolve(name)
    return resolved
