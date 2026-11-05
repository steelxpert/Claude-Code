"""Common set-up for the Hungarian informative translations of the FLINS-CFS notes (-HU documents).

    from hu_build import start
    N, A, F = start("FLINS-CFS-003", TITLE, SUBTITLE, KEYWORDS, cover_rows)

Command line: --figs FIGDIR --out OUT.docx [--projno 2026.032a] [--rev rev0] [--common COMMON.py] [--signature SIG.png]
The house common.py is used when given; otherwise hu_common.py. Without --signature no signature block is added.
Default is a light reading copy (title block, no cover or contents page); --formal gives the cover and contents.
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
    ap.add_argument("--figs", default="."); ap.add_argument("--out", required=True)
    ap.add_argument("--projno", default="2026.032a"); ap.add_argument("--rev", default="rev0")
    ap.add_argument("--common", default=str(HERE / "hu_common.py")); ap.add_argument("--signature", default=None)
    ap.add_argument("--final", action="store_true"); ap.add_argument("--formal", action="store_true", help="cover page and contents")
    A = ap.parse_args()
    docid = f"STEELXPERT {A.projno} — {code}-HU {A.rev}"
    N = sxnote.Note(A.common, A.signature, A.projno, docid, PROJECT, DATE_TXT, DATE_NUM, DATE_TUP, A.rev,
                    title=title, subject=subtitle, keywords=keywords, kind="Műszaki feljegyzés", final=A.final, lang="hu")
    if A.formal:
        rows = ([("Projekt:", PROJECT), ("Megbízó:", CLIENT)] + list(rows_before)
                + [("Tervező:", ENGINEER), ("Eredeti:", f"STEELXPERT {A.projno} — {code} {A.rev} (angol nyelvű), {EN_DATE}")]
                + list(rows_after) + [("Dokumentum:", docid), ("Kelt:", DATE_TXT), ("Megjegyzés:", NOTICE)])
        N.cover(title, subtitle, rows, [[A.rev, f"Tájékoztató magyar fordítás ({code} {A.rev} alapján)", DATE_NUM, "Bán Cs.", "–"]])
    else:
        _light(N, A, code, title, subtitle, rows_before)
    return N, A, Path(A.figs)


def _light(N, A, code, title, subtitle, rows):
    """Reading copy: one-line header, a short title block on page 1, no cover, no contents page, no forced page breaks."""
    from docx.shared import Cm, Pt
    C, doc = N.C, N.doc
    sec = doc.sections[0]; sec.top_margin = Cm(2.5)
    hdr = sec.header
    for t in list(hdr.tables):
        t._tbl.getparent().remove(t._tbl)
    p = hdr.paragraphs[0]
    for r in list(p.runs):
        r._r.getparent().remove(r._r)
    C.rich(p, f"STEELXPERT · FlexInSheet {A.projno} · {code}-HU · tájékoztató fordítás", size=7.5, color="7F7F7F")
    p = doc.add_paragraph(); C.rich(p, "MŰSZAKI FELJEGYZÉS · TÁJÉKOZTATÓ FORDÍTÁS", size=8.5, bold=True, color="808080")
    p.paragraph_format.space_after = Pt(2)
    p = doc.add_paragraph(); C.rich(p, title, size=18, bold=True); p.paragraph_format.space_after = Pt(2)
    p = doc.add_paragraph(); C.rich(p, subtitle, size=11.5, color="404040"); p.paragraph_format.space_after = Pt(6)
    p = doc.add_paragraph()
    C.rich(p, f"STEELXPERT Kft. · Bán Csaba · {DATE_TXT} · Eredeti: {code} {A.rev} (angol, {EN_DATE}); "
              "eltérés esetén az angol változat az irányadó.", size=8.5, color="595959")
    for k, v in rows:
        p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(2)
        C.rich(p, f"**{k}** {v}", size=8.5, color="595959")
    rule = doc.add_paragraph(); rule.paragraph_format.space_after = Pt(10)
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    pPr = rule._p.get_or_add_pPr(); bdr = OxmlElement("w:pBdr"); b = OxmlElement("w:bottom")
    for k_, v_ in (("w:val", "single"), ("w:sz", "6"), ("w:color", "A6A6A6"), ("w:space", "1")):
        b.set(qn(k_), v_)
    bdr.append(b); pPr.append(bdr)
    N.toc = lambda: None
    h = N.H

    import os
    breaks = set(filter(None, os.environ.get("HU_BREAK_BEFORE", "").split("|")))

    def heading(level, text, new_page=False):
        """No forced page breaks, except before headings that a render check found stranded at a page foot
        (HU_BREAK_BEFORE="heading|heading", set by the pagination pass)."""
        hp = h(level, text, text in breaks)
        hp.paragraph_format.keep_with_next = True
        return hp
    N.H = heading
