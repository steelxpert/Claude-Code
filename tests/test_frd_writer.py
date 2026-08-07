import io

import pytest

from ccxio import Model, Element, NodalResult, write_frd, FrdWriteError
from ccxio.frd_writer import frd_element_type


def frd_lines(model, results=(), **kw):
    buf = io.StringIO()
    write_frd(model, buf, results=results, **kw)
    return buf.getvalue().splitlines()


@pytest.fixture
def tiny_model():
    m = Model(name="tiny")
    m.nodes = {
        1: (0.0, 0.0, 0.0),
        2: (1.0, 0.0, 0.0),
        3: (0.0, 1.0, 0.0),
        4: (0.0, 0.0, 1.0),
    }
    m.elements = {5: Element(5, "C3D4", (1, 2, 3, 4))}
    return m


def test_file_frame(tiny_model):
    lines = frd_lines(tiny_model)
    assert lines[0] == "    1Ctiny"
    assert lines[-1] == " 9999"


def test_node_block_format(tiny_model):
    lines = frd_lines(tiny_model)
    header = next(l for l in lines if l.startswith("    2C"))
    # "    2C" + 18 blanks + %12d count + %38d format flag  (frd.c)
    assert header == "    2C" + " " * 18 + "%12d" % 4 + "%38d" % 1
    assert len(header) == 74

    node1 = next(l for l in lines if l.startswith(" -1"))
    assert node1 == " -1         1 0.00000E+00 0.00000E+00 0.00000E+00"
    assert len(node1) == 3 + 10 + 3 * 12


def test_element_block_format(tiny_model):
    lines = frd_lines(tiny_model)
    i = lines.index("    3C" + " " * 18 + "%12d" % 1 + "%38d" % 1)
    assert lines[i + 1] == " -1         5    3    0    1"
    assert lines[i + 2] == " -2         1         2         3         4"


def test_he20_node_permutation():
    m = Model()
    m.nodes = {i: (float(i), 0.0, 0.0) for i in range(1, 21)}
    m.elements = {1: Element(1, "C3D20R", tuple(range(1, 21)))}
    lines = frd_lines(m)
    i = next(k for k, l in enumerate(lines)
             if l.startswith(" -1") and lines[k + 1].startswith(" -2"))
    row1 = [int(x) for x in lines[i + 1][3:].split()]
    row2 = [int(x) for x in lines[i + 2][3:].split()]
    # frd.c writes inp nodes 1-10, then 11-12, 17-20, 13-16
    assert row1 == list(range(1, 11))
    assert row2 == [11, 12, 17, 18, 19, 20, 13, 14, 15, 16]


def test_pe15_node_permutation():
    m = Model()
    m.nodes = {i: (float(i), 0.0, 0.0) for i in range(1, 16)}
    m.elements = {1: Element(1, "C3D15", tuple(range(1, 16)))}
    lines = frd_lines(m)
    i = next(k for k, l in enumerate(lines)
             if l.startswith(" -1") and lines[k + 1].startswith(" -2"))
    row1 = [int(x) for x in lines[i + 1][3:].split()]
    row2 = [int(x) for x in lines[i + 2][3:].split()]
    # frd.c writes inp nodes 1-9, 13, then 14-15, 10-12
    assert row1 == [1, 2, 3, 4, 5, 6, 7, 8, 9, 13]
    assert row2 == [14, 15, 10, 11, 12]


def test_unmappable_elements_skipped(tiny_model):
    tiny_model.elements[99] = Element(99, "SPRINGA", (1, 2))
    lines = frd_lines(tiny_model)
    header = next(l for l in lines if l.startswith("    3C"))
    assert int(header.split()[1]) == 1  # only the tetra
    assert frd_element_type("SPRINGA") is None


def test_displacement_block(tiny_model):
    disp = NodalResult(
        "DISP", ("D1", "D2", "D3"),
        {n: (0.001 * n, -0.002 * n, 0.0) for n in tiny_model.nodes},
        step=1, increment=1, time=1.0,
    )
    lines = frd_lines(tiny_model, results=[disp])

    pstep = next(l for l in lines if l.startswith("    1PSTEP"))
    assert len(pstep) == 70
    assert pstep[24:36] == "%12d" % 1
    assert pstep[48:60] == "%12d" % 1

    hdr = next(l for l in lines if l.startswith("  100CL"))
    # frdheader.c: 75 chars, 100+kode at [7:12], time at [12:24],
    # node count at [24:36], kode at [58:63], ascii flag '1' at [74]
    assert len(hdr) == 75
    assert hdr[7:12] == "  101"
    assert hdr[12:24] == " 1.000000000"  # fixed point since ccx 2018 change
    assert hdr[24:36] == "%12d" % 4
    assert hdr[57] == "0"
    assert hdr[58:63] == "    1"
    assert hdr[74] == "1"

    # component records exactly as ccx writes them for DISP
    assert " -4  DISP        4    1" in lines
    assert " -5  D1          1    2    1    0" in lines
    assert " -5  D2          1    2    2    0" in lines
    assert " -5  D3          1    2    3    0" in lines
    assert " -5  ALL         1    2    0    0    1ALL" in lines

    data1 = next(l for l in lines if l.startswith(" -1") and "E-0" in l)
    assert data1 == " -1         1 1.00000E-03-2.00000E-03 0.00000E+00"


def test_stress_block_and_scalars(tiny_model):
    stress = NodalResult(
        "STRESS", ("SXX", "SYY", "SZZ", "SXY", "SYZ", "SZX"),
        {1: (1.0, 2.0, 3.0, 4.0, 5.0, 6.0)},
    )
    temp = NodalResult("NDTEMP", ("T",), {1: (20.0,)})
    lines = frd_lines(tiny_model, results=[stress, temp])

    assert " -4  STRESS      6    1" in lines
    assert " -5  SXX         1    4    1    1" in lines
    assert " -5  SZX         1    4    3    1" in lines
    assert " -4  NDTEMP      1    1" in lines
    assert " -5  T           1    1    0    0" in lines

    # second block increments the loadcase counters
    hdrs = [l for l in lines if l.startswith("  100CL")]
    assert hdrs[1][7:12] == "  102"
    assert hdrs[1][58:63] == "    2"


def test_seven_component_continuation(tiny_model):
    sdv = NodalResult(
        "SDV", tuple(f"SDV{i}" for i in range(1, 8)),
        {1: tuple(float(i) for i in range(1, 8))},
        vector_all=False,
    )
    lines = frd_lines(tiny_model, results=[sdv])
    i = lines.index(" -1         1" + "".join("%12.5E" % v for v in (1, 2, 3, 4, 5, 6)))
    assert lines[i + 1] == " -2" + " " * 10 + "%12.5E" % 7.0


def test_time_formatting(tiny_model):
    small = NodalResult("DISP", ("D1", "D2", "D3"), {1: (0.0,) * 3}, time=0.25)
    big = NodalResult("DISP", ("D1", "D2", "D3"), {1: (0.0,) * 3}, time=1234.5)
    lines = frd_lines(tiny_model, results=[small, big])
    hdrs = [l for l in lines if l.startswith("  100CL")]
    assert hdrs[0][12:24] == " 2.50000E-01"  # < 1 stays scientific
    assert hdrs[1][12:24] == " 1234.500000"  # 10 significant digits fixed


def test_component_length_mismatch_raises(tiny_model):
    bad = NodalResult("DISP", ("D1", "D2", "D3"), {1: (0.0, 0.0)})
    with pytest.raises(FrdWriteError):
        frd_lines(tiny_model, results=[bad])
