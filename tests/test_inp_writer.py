import io

import pytest

from ccxio import Element, Model, read_inp, write_inp

DECK = """\
*HEADING
writer roundtrip
*NODE, NSET=NALL
1, 0.0, 0.0, 0.0
2, 1.25e-3, -7.5, 0.125
*ELEMENT, TYPE=C3D20, ELSET=SOLID
1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2
1, 2, 1, 2, 1, 2, 1, 2, 1, 2
*MATERIAL, NAME=STEEL
*ELASTIC
210000., 0.3
*STEP
*STATIC
*END STEP
"""


def test_full_roundtrip():
    m1 = read_inp(DECK.splitlines())
    buf = io.StringIO()
    write_inp(m1, buf)
    m2 = read_inp(buf.getvalue().splitlines())

    assert m2.name == m1.name
    assert m2.nodes == m1.nodes  # repr() coordinates are exact
    assert m2.elements[1].nodes == m1.elements[1].nodes
    assert m2.nset("NALL") == m1.nset("NALL")
    assert [c.keyword for c in m2.cards] == [c.keyword for c in m1.cards]
    assert m2.cards_named("ELASTIC")[0].data == ["210000., 0.3"]
    assert m2.cards_named("MATERIAL")[0].get("NAME") == "STEEL"


def test_cardless_model_written_as_minimal_deck():
    m = Model(name="bare")
    m.nodes = {1: (0.0, 0.0, 0.0), 2: (1.0, 0.0, 0.0), 3: (0.0, 1.0, 0.0)}
    m.elements = {9: Element(9, "S3", (1, 2, 3))}
    m.nsets = {"EDGE": (1, 2)}
    buf = io.StringIO()
    write_inp(m, buf)
    m2 = read_inp(buf.getvalue().splitlines())
    assert m2.name == "bare"
    assert m2.nodes == m.nodes
    assert m2.elements[9].type == "S3"
    assert m2.nset("EDGE") == (1, 2)
