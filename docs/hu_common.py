"""Page furniture helpers for STEELXPERT notes when the house `common.py` is not at hand.

Implements the subset of the `common.py` interface that `sxnote.Note` uses (rich-text markup, header/footer
fields, info and data tables, page set-up, language tags, document properties), following the house rules:
A4, top margin 3.5 cm, bottom 2.2 cm, left 2.5 cm, right 2.0 cm, header/footer distance 1.0 cm, cells aligned
to the top with a small inner margin, repeated table header rows, rows that do not split.

Markup in `rich()`: **bold**, ~italic~, x_[sub], x^[sup], {{pending}} (highlighted while HIGHLIGHT[0] is set).
"""
from __future__ import annotations

import datetime as dt
import re

from docx.enum.section import WD_ORIENT
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_COLOR_INDEX
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

LANG = "en-GB"
HIGHLIGHT = [False]
DOCREF = [None]
PENDING: list[str] = []
FONT = "Calibri"
BODY_SIZE = 10.5
HDR_SIZE = 7.5
PAGE_W, MARGINS = 21.0, dict(top=3.5, bottom=2.2, left=2.5, right=2.0)
CONTENT_W = PAGE_W - MARGINS["left"] - MARGINS["right"]
AUTHOR = "Bán Csaba (STEELXPERT Kft.)"


# ---------------------------------------------------------------- document level
def set_lang(doc):
    """Language tag on docDefaults and the theme font language (styles are re-tagged in Note.save)."""
    rpr = doc.styles.element.find(qn("w:docDefaults")).find(qn("w:rPrDefault")).find(qn("w:rPr"))
    lang = rpr.find(qn("w:lang"))
    if lang is None:
        lang = OxmlElement("w:lang"); rpr.append(lang)
    for a in ("w:val", "w:eastAsia", "w:bidi"):
        lang.set(qn(a), LANG)
    settings = doc.settings.element
    tfl = settings.find(qn("w:themeFontLang"))
    if tfl is None:
        tfl = OxmlElement("w:themeFontLang"); settings.append(tfl)
    tfl.set(qn("w:val"), LANG)


def _font(style, size=None, bold=None, italic=None, color=None):
    style.font.name = FONT
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts"); rpr.append(rfonts)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(a), FONT)
    if size: style.font.size = Pt(size)
    if bold is not None: style.font.bold = bold
    if italic is not None: style.font.italic = italic
    style.font.color.rgb = RGBColor.from_string(color or "000000")


def base_styles(doc):
    st = doc.styles
    _font(st["Normal"], BODY_SIZE)
    pf = st["Normal"].paragraph_format
    pf.space_after = Pt(6); pf.line_spacing = 1.1
    for lvl, size, before in ((1, 15, 0), (2, 12, 10), (3, 11, 8)):
        s = st[f"Heading {lvl}"]
        _font(s, size, bold=True, italic=False)
        s.paragraph_format.space_before = Pt(before); s.paragraph_format.space_after = Pt(6)
        s.paragraph_format.keep_with_next = True
    cap = st["Caption"]
    _font(cap, 9, bold=False, italic=True, color="333333")
    cap.paragraph_format.space_before = Pt(3); cap.paragraph_format.space_after = Pt(9)
    _font(st["List Bullet"], BODY_SIZE)
    st["List Bullet"].paragraph_format.space_after = Pt(3)


def page_setup(section):
    section.orientation = WD_ORIENT.PORTRAIT
    section.page_width, section.page_height = Cm(21.0), Cm(29.7)
    section.top_margin, section.bottom_margin = Cm(MARGINS["top"]), Cm(MARGINS["bottom"])
    section.left_margin, section.right_margin = Cm(MARGINS["left"]), Cm(MARGINS["right"])
    section.header_distance = section.footer_distance = Cm(1.0)


def core_props(doc, title, subject, keywords, date_tup):
    cp = doc.core_properties
    t = dt.datetime(*date_tup, 9, 0, 0)
    cp.author = cp.last_modified_by = AUTHOR
    cp.title, cp.subject, cp.keywords = title, subject, keywords
    cp.comments = ""
    cp.created = cp.modified = t
    cp.last_printed = t
    cp.revision = 1


# ---------------------------------------------------------------- text
TOKEN = re.compile(r"(\*\*.+?\*\*|~[^~]+~|_\[[^\]]+\]|\^\[[^\]]+\]|\{\{.+?\}\})")


def rich(p, text, size=None, bold=False, italic=False, color=None):
    """Add `text` to paragraph p, honouring the markup described in the module docstring."""
    for part in TOKEN.split(text):
        if not part:
            continue
        kw = dict(b=bold, i=italic, sub=False, sup=False, hl=False)
        if part.startswith("**"):
            part, kw["b"] = part[2:-2], True
        elif part.startswith("~") and part.endswith("~") and len(part) > 2:
            part, kw["i"] = part[1:-1], True
        elif part.startswith("_["):
            part, kw["sub"] = part[2:-1], True
        elif part.startswith("^["):
            part, kw["sup"] = part[2:-1], True
        elif part.startswith("{{"):
            part = part[2:-2]; PENDING.append(part); kw["hl"] = HIGHLIGHT[0]
        r = p.add_run(part)
        r.bold, r.italic = kw["b"] or None, kw["i"] or None
        r.font.subscript, r.font.superscript = kw["sub"] or None, kw["sup"] or None
        if size: r.font.size = Pt(size)
        if color: r.font.color.rgb = RGBColor.from_string(color)
        if kw["hl"]: r.font.highlight_color = WD_COLOR_INDEX.YELLOW
    return p


def small_style(name="Header small", color=None):
    """Paragraph style that carries the small size, so PAGE/NUMPAGES fields keep it when Word updates them."""
    doc = DOCREF[0]
    try:
        return doc.styles[name]
    except KeyError:
        s = doc.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
        s.base_style = doc.styles["Normal"]
        _font(s, HDR_SIZE, color=color)
        s.paragraph_format.space_after = Pt(0); s.paragraph_format.line_spacing = 1.0
        return s


def field(p, code, size=None):
    def fc(kind):
        r = p.add_run(); e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), kind); r._r.append(e); return r
    fc("begin")
    r = p.add_run(); it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = f" {code} "; r._r.append(it)
    fc("separate"); r = p.add_run("1")
    if size: r.font.size = Pt(size)
    fc("end")


# ---------------------------------------------------------------- tables
def set_widths(table, widths_cm):
    table.autofit = False
    tbl = table._tbl
    grid = tbl.tblGrid
    for gc, w in zip(grid.findall(qn("w:gridCol")), widths_cm):
        gc.set(qn("w:w"), str(int(w * 567)))
    for row in table.rows:
        for cell, w in zip(row.cells, widths_cm):
            cell.width = Cm(w)


def cell_text(cell, text, size=None, bold=False):
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP
    lines = str(text).split("\n")
    p = cell.paragraphs[0]
    for k, ln in enumerate(lines):
        if k:
            p = cell.add_paragraph()
        p.paragraph_format.space_after = Pt(0); p.paragraph_format.line_spacing = 1.0
        rich(p, ln, size=size, bold=bold)


def borders(cell, bottom=None, top=None):
    tcPr = cell._tc.get_or_add_tcPr()
    b = tcPr.find(qn("w:tcBorders"))
    if b is None:
        b = OxmlElement("w:tcBorders"); tcPr.append(b)
    for side, sz in (("top", top), ("bottom", bottom)):
        if sz:
            e = OxmlElement(f"w:{side}"); e.set(qn("w:val"), "single"); e.set(qn("w:sz"), str(sz)); e.set(qn("w:color"), "808080"); b.append(e)


def cell_margins(table, top=45, bottom=30, left=60, right=60):
    tblPr = table._tbl.tblPr
    m = OxmlElement("w:tblCellMar")
    for side, v in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        e = OxmlElement(f"w:{side}"); e.set(qn("w:w"), str(v)); e.set(qn("w:type"), "dxa"); m.append(e)
    tblPr.append(m)


def shade(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    s = OxmlElement("w:shd"); s.set(qn("w:val"), "clear"); s.set(qn("w:color"), "auto"); s.set(qn("w:fill"), hex_color); tcPr.append(s)


def cant_split(row, header=False):
    trPr = row._tr.get_or_add_trPr()
    e = OxmlElement("w:cantSplit"); trPr.append(e)
    if header:
        h = OxmlElement("w:tblHeader"); trPr.append(h)


def keep_table_start(table, rows=3):
    """Keep caption, header and the first two data rows on one page (caption is keep_with_next already)."""
    for row in table.rows[:rows]:
        for cell in row.cells:
            for p in cell.paragraphs:
                p.paragraph_format.keep_with_next = True


def info_table(doc, rows):
    t = doc.add_table(rows=len(rows), cols=2)
    t.style = doc.styles["Table Grid"]
    set_widths(t, [3.2, CONTENT_W - 3.2])
    cell_margins(t, top=50, bottom=40, left=60, right=60)
    for i, (k, v) in enumerate(rows):
        cell_text(t.cell(i, 0), k, size=9.5, bold=True); shade(t.cell(i, 0), "F2F2F2")
        cell_text(t.cell(i, 1), v, size=9.5)
        cant_split(t.rows[i])
    return t
