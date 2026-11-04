"""Language switch for the note figures.

    import figlang; OUT = figlang.setup(TABLE)      # TABLE: English label -> Hungarian label

Command line of a figure script: OUT_DIR [--lang en|hu]. With --lang hu every text matplotlib draws (labels,
titles, legends, tick labels) passes through the table; decimal points in numbers become decimal commas and
the minus sign is typographic. Labels without a translation are reported at exit, so none slips through.
"""
from __future__ import annotations

import atexit
import re
import sys
from pathlib import Path

import matplotlib
import matplotlib.text as mtext

LANG = "en"
MISSING: set[str] = set()
_NUM = re.compile(r"(?<![\w.])(\d+)\.(\d+)(?![\w.])")
_KEEP = re.compile(r"^[\sδΔγζλμσαβ0-9.,:;/()×+−\-=≤≥%°'\"LhteNFVTHabcd]*$")   # symbols, numbers, single letters


def translate(s: str, table: dict[str, str]) -> str:
    if not isinstance(s, str) or not s:
        return s
    if s in table:
        out = table[s]
    else:
        out = s
        for pat, rep in table.get("__regex__", []):
            new = re.sub(pat, rep, out)
            if new != out:
                out = new
                break
        else:
            if not _KEEP.match(s) and re.search(r"[A-Za-z]{3,}", s) and not re.fullmatch(r"[A-Z0-9\-.]+", s.strip()):
                MISSING.add(s)
    out = _NUM.sub(r"\1,\2", out)
    return out.replace("-", "−") if re.fullmatch(r"-\d+([.,]\d+)?", out) else out


def setup(table: dict) -> Path:
    """Parse OUT_DIR and --lang from the command line; install the translation hook for --lang hu."""
    global LANG
    args = [a for a in sys.argv[1:]]
    if "--lang" in args:
        i = args.index("--lang"); LANG = args[i + 1]; del args[i:i + 2]
    out = Path(args[0] if args else "figs"); out.mkdir(parents=True, exist_ok=True)
    if LANG == "hu":
        matplotlib.rcParams["axes.unicode_minus"] = True
        orig = mtext.Text.set_text

        def set_text(self, s):
            orig(self, translate(s, table) if isinstance(s, str) else s)

        mtext.Text.set_text = set_text
        atexit.register(_report)
    return out


def _report():
    if MISSING:
        print("figlang: untranslated labels:", *sorted(MISSING), sep="\n  ")
