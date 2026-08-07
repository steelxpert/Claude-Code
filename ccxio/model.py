"""In-memory model built from a CalculiX .inp file.

The mesh entities (nodes, elements, sets) are parsed into typed containers;
every keyword block of the file, mesh ones included, is additionally kept
verbatim as a :class:`KeywordCard` so nothing in the deck is lost.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class Element:
    id: int
    type: str  # CalculiX type name, uppercase (e.g. "C3D20R", "S4", "B31")
    nodes: Tuple[int, ...]


@dataclass
class KeywordCard:
    """One keyword block exactly as it appeared in the deck.

    keyword: uppercase name without the leading '*', internal whitespace
             collapsed (e.g. "NODE", "NODE FILE", "STATIC").
    params:  uppercase parameter names mapped to their raw value, or None
             for flag parameters (e.g. {"TYPE": "C3D20R", "GENERATE": None}).
    data:    the block's data lines, stripped, comments removed.
    """

    keyword: str
    params: Dict[str, Optional[str]] = field(default_factory=dict)
    data: List[str] = field(default_factory=list)

    def get(self, name: str, default: Optional[str] = None) -> Optional[str]:
        return self.params.get(name.upper(), default)


@dataclass
class Model:
    """Mesh + sets + the full keyword stream of a CalculiX input deck.

    Set names are stored uppercase: Abaqus/CalculiX treat them
    case-insensitively, so 'Fix' and 'FIX' are the same set.
    """

    name: str = ""
    nodes: Dict[int, Tuple[float, float, float]] = field(default_factory=dict)
    elements: Dict[int, Element] = field(default_factory=dict)
    nsets: Dict[str, Tuple[int, ...]] = field(default_factory=dict)
    elsets: Dict[str, Tuple[int, ...]] = field(default_factory=dict)
    cards: List[KeywordCard] = field(default_factory=list)

    def nset(self, name: str) -> Tuple[int, ...]:
        return self.nsets[name.upper()]

    def elset(self, name: str) -> Tuple[int, ...]:
        return self.elsets[name.upper()]

    def cards_named(self, keyword: str) -> List[KeywordCard]:
        kw = " ".join(keyword.upper().split())
        return [c for c in self.cards if c.keyword == kw]
