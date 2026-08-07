import subprocess
import sys


DECK = """\
*HEADING
cli smoke
*NODE, NSET=NALL
1, 0., 0., 0.
2, 1., 0., 0.
3, 0., 1., 0.
*ELEMENT, TYPE=S3, ELSET=SHELL
1, 1, 2, 3
"""


def test_inp_to_frd(tmp_path):
    inp = tmp_path / "m.inp"
    inp.write_text(DECK)
    # no subcommand: back-compat shorthand for "convert"
    out = subprocess.run(
        [sys.executable, "-m", "ccxio", str(inp)],
        capture_output=True, text=True, check=True,
    )
    frd = tmp_path / "m.frd"
    assert frd.exists()
    assert "3 nodes, 1 elements" in out.stdout
    text = frd.read_text()
    assert text.startswith("    1Ccli smoke\n")
    assert text.rstrip("\n").endswith(" 9999")


def test_seed_command(tmp_path):
    import io
    from ccxio import read_inp, write_frd, NodalResult, read_inp as _

    inp = tmp_path / "m.inp"
    inp.write_text(DECK)
    model = read_inp(str(inp))
    mode = NodalResult("DISP", ("D1", "D2", "D3"),
                       {1: (0.0, 0.0, 0.0), 2: (0.0, 0.0, 1.0),
                        3: (0.0, 0.0, 0.5)},
                       time=42.5)  # buckling factor
    frd = tmp_path / "modes.frd"
    write_frd(model, str(frd), results=[mode])

    out = subprocess.run(
        [sys.executable, "-m", "ccxio", "seed", str(inp), str(frd),
         "--amplitude", "0.25"],
        capture_output=True, text=True, check=True,
    )
    seeded_path = tmp_path / "m_imperfect.inp"
    assert seeded_path.exists()
    assert "42.5" in out.stdout  # reports the mode's factor

    seeded = read_inp(str(seeded_path))
    assert abs(seeded.nodes[2][2] - 0.25) < 1e-9
    assert abs(seeded.nodes[3][2] - 0.125) < 1e-9
    assert seeded.nodes[1] == (0.0, 0.0, 0.0)
