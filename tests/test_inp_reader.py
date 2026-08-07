import os
import textwrap

import pytest

from ccxio import read_inp, InpSyntaxError

DECK = """\
*HEADING
Test beam model
** a comment line
*NODE, NSET=NALL
1, 0.0, 0.0, 0.0
2, 1.0, 0.0
3, 2.0
4, 3.0, 1.0, 2.0
*ELEMENT, TYPE=C3D20R, ELSET=SOLIDS
** twenty nodes over continuation lines, trailing commas
1, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2,
3, 4, 1, 2, 3, 4, 1, 2, 3, 4
*ELEMENT, TYPE=B31, ELSET=BEAMS
10, 1, 2
11, 2, 3
*NSET, NSET=FIX
1, 2
*NSET, NSET=Generated, GENERATE
1, 4, 1
*NSET, NSET=Combined
FIX, 4
*ELSET, ELSET=EVERYTHING
SOLIDS, BEAMS
*BOUNDARY
1, 1, 3
*STEP
*STATIC
*END STEP
"""


@pytest.fixture
def model():
    return read_inp(DECK.splitlines())


def test_heading_and_nodes(model):
    assert model.name == "Test beam model"
    assert len(model.nodes) == 4
    # missing coordinates default to zero
    assert model.nodes[2] == (1.0, 0.0, 0.0)
    assert model.nodes[3] == (2.0, 0.0, 0.0)
    assert model.nodes[4] == (3.0, 1.0, 2.0)


def test_elements_with_continuation(model):
    el = model.elements[1]
    assert el.type == "C3D20R"
    assert len(el.nodes) == 20
    assert el.nodes[:4] == (1, 2, 3, 4)
    assert model.elements[10].nodes == (1, 2)


def test_sets(model):
    assert model.nset("NALL") == (1, 2, 3, 4)   # from *NODE, NSET=
    assert model.nset("fix") == (1, 2)          # case-insensitive lookup
    assert model.nset("GENERATED") == (1, 2, 3, 4)
    assert model.nset("COMBINED") == (1, 2, 4)  # set reference + literal
    assert model.elset("SOLIDS") == (1,)
    assert model.elset("EVERYTHING") == (1, 10, 11)


def test_cards_preserved(model):
    assert model.cards_named("BOUNDARY")[0].data == ["1, 1, 3"]
    assert [c.keyword for c in model.cards_named("STATIC")] == ["STATIC"]
    elem_cards = model.cards_named("ELEMENT")
    assert elem_cards[0].get("type") == "C3D20R"


def test_continuation_without_trailing_comma():
    # some meshers split connectivity without the trailing comma; a known
    # node count keeps the parser consuming lines
    deck = [
        "*NODE",
        "1, 0, 0, 0",
        "*ELEMENT, TYPE=C3D20",
        "7, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1",
        "1, 1, 1, 1, 1, 1, 1, 1, 1, 1",
    ]
    m = read_inp(deck)
    assert len(m.elements[7].nodes) == 20


def test_include(tmp_path):
    inc = tmp_path / "mesh.inp"
    inc.write_text("*NODE\n1, 1.0, 2.0, 3.0\n")
    main = tmp_path / "main.inp"
    main.write_text(f"*INCLUDE, INPUT=mesh.inp\n*NSET, NSET=A\n1,\n")
    m = read_inp(str(main))
    assert m.nodes[1] == (1.0, 2.0, 3.0)
    assert m.nset("A") == (1,)


def test_wrong_node_count_raises():
    deck = ["*NODE", "1, 0, 0, 0", "*ELEMENT, TYPE=C3D4", "1, 1, 1, 1"]
    with pytest.raises(InpSyntaxError):
        read_inp(deck)


def test_unknown_set_reference_raises():
    deck = ["*NSET, NSET=A", "NOSUCHSET,"]
    with pytest.raises(InpSyntaxError):
        read_inp(deck)
