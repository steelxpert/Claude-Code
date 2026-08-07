import math

import pytest

from ccxio import (
    NodalResult,
    read_inp,
    seed_imperfection,
    write_inp,
    ImperfectionError,
)

DECK = """\
*HEADING
seed test
*NODE, NSET=NALL
1, 0.0, 0.0, 0.0
2, 100.0, 0.0, 0.0
3, 200.0, 0.0, 0.0
*ELEMENT, TYPE=B31, ELSET=BEAM
1, 1, 2
2, 2, 3
*BOUNDARY
1, 1, 3
"""


@pytest.fixture
def model():
    return read_inp(DECK.splitlines())


def half_sine_mode(model):
    # unit-normalised lateral half-sine over member length 200
    return {nid: (0.0, math.sin(math.pi * x / 200.0), 0.0)
            for nid, (x, y, z) in model.nodes.items()}


def test_amplitude_scaling(model):
    seeded = seed_imperfection(model, half_sine_mode(model), amplitude=0.8)
    assert seeded.nodes[2][1] == pytest.approx(0.8)   # peak lands at L/2
    assert seeded.nodes[1] == (0.0, 0.0, 0.0)
    assert seeded.nodes[3][1] == pytest.approx(0.0, abs=1e-12)
    # original untouched
    assert model.nodes[2][1] == 0.0


def test_raw_scale_and_nodal_result_input(model):
    mode = NodalResult("DISP", ("D1", "D2", "D3"),
                       {2: (0.0, 0.5, 0.0)})
    seeded = seed_imperfection(model, mode, scale=2.0)
    assert seeded.nodes[2][1] == pytest.approx(1.0)
    assert seeded.nodes[1] == model.nodes[1]  # missing from field: unmoved


def test_mode_combination_by_repeated_calls(model):
    m1 = seed_imperfection(model, half_sine_mode(model), amplitude=0.8)
    m2 = seed_imperfection(
        m1, {nid: (0.0, 0.0, 1.0) for nid in model.nodes}, amplitude=0.2)
    assert m2.nodes[2][1] == pytest.approx(0.8)
    assert m2.nodes[2][2] == pytest.approx(0.2)


def test_argument_validation(model):
    with pytest.raises(ImperfectionError):
        seed_imperfection(model, half_sine_mode(model))
    with pytest.raises(ImperfectionError):
        seed_imperfection(model, half_sine_mode(model), amplitude=1, scale=1)
    with pytest.raises(ImperfectionError):
        seed_imperfection(model, {n: (0.0, 0.0, 0.0) for n in model.nodes},
                          amplitude=1.0)  # zero-magnitude field


def test_seeded_deck_roundtrip(model, tmp_path):
    seeded = seed_imperfection(model, half_sine_mode(model), amplitude=0.8)
    out = tmp_path / "seeded.inp"
    write_inp(seeded, str(out))
    text = out.read_text()
    # non-mesh cards survive verbatim, in order
    assert "*BOUNDARY" in text and "1, 1, 3" in text
    reread = read_inp(str(out))
    assert reread.nodes[2][1] == pytest.approx(0.8)
    assert reread.elements[2].nodes == (2, 3)
    assert reread.nset("NALL") == (1, 2, 3)
    assert reread.name == "seed test"
