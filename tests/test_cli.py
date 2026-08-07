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
