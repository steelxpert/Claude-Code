"""Common set-up for the Hungarian informative translations of the FLINS-CFS notes (-HU documents).

    from hu_build import start
    N, A, F = start("FLINS-CFS-003", TITLE, SUBTITLE, KEYWORDS, cover_rows)

Command line: --figs FIGDIR --out OUT.docx [--projno 2026.032a] [--rev rev0] [--common COMMON.py] [--signature SIG.png]
The house common.py is used when given; otherwise hu_common.py. Without --signature no signature block is added.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import sxnote

HERE = Path(__file__).parent
PROJECT = "FlexInSheet hidegen alakított acél födémrendszer csavarcölöp-alapozással: termékfejlesztés"
CLIENT = "FlexInSheet Kft. (FLINS)\n2400 Dunaújváros, Előd utca 4."
ENGINEER = "STEELXPERT Kft.\nBán Csaba okl. építőmérnök (T-T/01-18387)"
DATE_TXT, DATE_NUM, DATE_TUP = "2026. november 4.", "2026.11.04.", (2026, 11, 4)
EN_DATE = "2026. október 27."
NOTICE = ("Tájékoztató fordítás, aláírás nélkül. Az angol nyelvű eredeti tartalmát változatlanul adja vissza; "
          "eltérés esetén az angol változat az irányadó.")


def start(code, title, subtitle, keywords, rows_before, rows_after=()):
    ap = argparse.ArgumentParser()
    ap.add_argument("--figs", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--projno", default="2026.032a"); ap.add_argument("--rev", default="rev0")
    ap.add_argument("--common", default=str(HERE / "hu_common.py")); ap.add_argument("--signature", default=None)
    ap.add_argument("--final", action="store_true")
    A = ap.parse_args()
    docid = f"STEELXPERT {A.projno} — {code}-HU {A.rev}"
    N = sxnote.Note(A.common, A.signature, A.projno, docid, PROJECT, DATE_TXT, DATE_NUM, DATE_TUP, A.rev,
                    title=title, subject=subtitle, keywords=keywords, kind="Műszaki feljegyzés", final=A.final, lang="hu")
    rows = ([("Projekt:", PROJECT), ("Megbízó:", CLIENT)] + list(rows_before)
            + [("Tervező:", ENGINEER), ("Eredeti:", f"STEELXPERT {A.projno} — {code} {A.rev} (angol nyelvű), {EN_DATE}")]
            + list(rows_after) + [("Dokumentum:", docid), ("Kelt:", DATE_TXT), ("Megjegyzés:", NOTICE)])
    N.cover(title, subtitle, rows, [[A.rev, f"Tájékoztató magyar fordítás ({code} {A.rev} alapján)", DATE_NUM, "Bán Cs.", "–"]])
    return N, A, Path(A.figs)
