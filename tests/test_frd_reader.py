import io

import pytest

from ccxio import (
    Element,
    Model,
    NodalResult,
    read_frd,
    write_frd,
    FrdSyntaxError,
)


def roundtrip(model, results=()):
    buf = io.StringIO()
    write_frd(model, buf, results=results)
    text = buf.getvalue()
    import tempfile, os
    fd, path = tempfile.mkstemp(suffix=".frd")
    try:
        with os.fdopen(fd, "w") as f:
            f.write(text)
        return read_frd(path)
    finally:
        os.unlink(path)


@pytest.fixture
def model():
    m = Model(name="rt")
    m.nodes = {
        1: (0.0, 0.0, 0.0),
        2: (1.5, 0.0, 0.0),
        3: (0.0, -2.25e-3, 0.0),
        7: (0.0, 0.0, 1.0e8),
    }
    m.elements = {4: Element(4, "C3D4", (1, 2, 3, 7))}
    return m


def test_mesh_roundtrip(model):
    frd = roundtrip(model)
    assert frd.name == "rt"
    assert set(frd.nodes) == set(model.nodes)
    for nid, xyz in model.nodes.items():
        assert frd.nodes[nid] == pytest.approx(xyz, rel=1e-5)
    assert frd.elements[4].nodes == (1, 2, 3, 7)
    assert frd.elements[4].type == "C3D4"


def test_he20_connectivity_roundtrips():
    m = Model()
    m.nodes = {i: (float(i), 0.0, 0.0) for i in range(1, 21)}
    conn = tuple(range(1, 21))
    m.elements = {1: Element(1, "C3D20R", conn)}
    frd = roundtrip(m)
    # the frd stores a permuted order; reading must undo it exactly
    assert frd.elements[1].nodes == conn
    assert frd.elements[1].type == "C3D20"  # shape only, R not recoverable


def test_pe15_connectivity_roundtrips():
    m = Model()
    m.nodes = {i: (float(i), 0.0, 0.0) for i in range(1, 16)}
    conn = tuple(range(1, 16))
    m.elements = {1: Element(1, "C3D15", conn)}
    frd = roundtrip(m)
    assert frd.elements[1].nodes == conn


def test_displacement_roundtrip_with_packed_negatives(model):
    # adjacent negative values run together with no separating space
    disp = NodalResult(
        "DISP", ("D1", "D2", "D3"),
        {n: (1e-3 * n, -2e-3 * n, -3e-3 * n) for n in model.nodes},
        step=2, increment=5, time=3.75,
    )
    frd = roundtrip(model, [disp])
    r = frd.result("DISP")
    assert r.components == ("D1", "D2", "D3")  # calculated ALL dropped
    assert r.step == 2 and r.increment == 5
    assert r.time == pytest.approx(3.75)
    assert r.values[3] == pytest.approx((3e-3, -6e-3, -9e-3), rel=1e-5)


def test_tensor_and_multiblock_roundtrip(model):
    stress = NodalResult(
        "STRESS", ("SXX", "SYY", "SZZ", "SXY", "SYZ", "SZX"),
        {1: (1.0, -2.0, 3.0, -4.0, 5.0, -6.0)},
    )
    sdv = NodalResult(
        "SDV", tuple(f"SDV{i}" for i in range(1, 8)),
        {1: tuple(float(i) for i in range(1, 8))},
        vector_all=False,
    )
    frd = roundtrip(model, [stress, sdv])
    assert [r.name for r in frd.results] == ["STRESS", "SDV"]
    assert frd.result("STRESS").values[1] == \
        pytest.approx((1.0, -2.0, 3.0, -4.0, 5.0, -6.0))
    # 7 components exercise the -2 continuation-line path
    assert frd.result("SDV").values[1] == pytest.approx(tuple(range(1, 8)))


def test_buckle_style_multiple_modes(model):
    modes = [
        NodalResult("DISP", ("D1", "D2", "D3"),
                    {n: (float(k), 0.0, 0.0) for n in model.nodes},
                    increment=k + 1, time=float(10 * k))
        for k in (1, 2, 3)
    ]
    frd = roundtrip(model, modes)
    disp = [r for r in frd.results if r.name == "DISP"]
    assert len(disp) == 3
    assert frd.result("DISP", 1).time == pytest.approx(20.0)
    assert frd.result("DISP", 2).values[1][0] == pytest.approx(3.0)


def test_as_model(model):
    m2 = roundtrip(model).as_model()
    assert isinstance(m2, Model)
    assert set(m2.elements) == {4}


def test_binary_rejected(tmp_path):
    p = tmp_path / "b.frd"
    p.write_text("    1Cx\n    2C" + " " * 18 + "%12d%38d\n" % (0, 2))
    with pytest.raises(FrdSyntaxError):
        read_frd(str(p))
