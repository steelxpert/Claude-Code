#!/usr/bin/env python3
"""Build the English STEELXPERT technical note 'Feasibility Q&A' (.docx) with the house page furniture.

Usage: python3 docs/build_qa_docx.py --common PATH/common.py --signature PATH/sig.png --out PATH/out.docx [--projno 2026.xx]
`common.py` is the shared STEELXPERT python-docx helper (kept outside the repo); the signature PNG must have a pure white background.
"""
from __future__ import annotations

import argparse, importlib.util, sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--common", required=True); ap.add_argument("--signature", required=True); ap.add_argument("--out", required=True)
ap.add_argument("--projno", default="{{2026.xx}}"); ap.add_argument("--rev", default="rev0"); ap.add_argument("--final", action="store_true")
A = ap.parse_args()

spec = importlib.util.spec_from_file_location("common", A.common); C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
C.LANG = "en-GB"
C.HIGHLIGHT[0] = not A.final
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

DATE_TXT, DATE_NUM, DATE_TUP = "27 October 2026", "27.10.2026", (2026, 10, 27)
PROJECT = "FlexInSheet cold-formed steel floor framing system on screw piles: product development"
DOCID = f"STEELXPERT {A.projno} — FLINS-CFS-001 {A.rev}"
TITLE = "Cold-formed steel floor framing on screw piles"
SUBTITLE = "Feasibility questions and answers for the product development"

doc = Document(); C.DOCREF[0] = doc
C.set_lang(doc); C.base_styles(doc); C.page_setup(doc.sections[0])
C.core_props(doc, TITLE, SUBTITLE, "cold-formed steel, floor framing, screw piles, GMNIA, Eurocode", DATE_TUP)
doc.core_properties.category = "Technical note"

# ---------------------------------------------------------------- page furniture (English labels, house geometry)
def header_block(hdr):
    p = hdr.paragraphs[0]; C.rich(p, "Technical note", size=11, bold=True, color="404040"); p.paragraph_format.space_after = Pt(3)
    t = hdr.add_table(rows=3, cols=4, width=Cm(C.CONTENT_W)); C.set_widths(t, [2.4, 10.1, 2.0, 2.0])
    vals = [("Project:", PROJECT, "Page:", None), ("Project No.:", A.projno, "Revision:", A.rev), ("Document:", DOCID, "", "")]
    for i, row in enumerate(vals):
        for j, v in enumerate(row):
            cl = t.cell(i, j)
            if v is None:
                pp = cl.paragraphs[0]; pp.paragraph_format.space_after = Pt(0); pp.paragraph_format.line_spacing = 1.0
                pp.style = C.small_style(name="Header small"); C.field(pp, "PAGE", C.HDR_SIZE)
            else:
                C.cell_text(cl, v, size=C.HDR_SIZE)
            C.borders(cl, bottom=6 if i == 2 else None)
    C.cell_margins(t, top=45, bottom=15, left=60, right=60)
    for cl in t.rows[2].cells:
        tcPr = cl._tc.get_or_add_tcPr(); m = OxmlElement("w:tcMar"); b = OxmlElement("w:bottom"); b.set(qn("w:w"), "90"); b.set(qn("w:type"), "dxa"); m.append(b); tcPr.append(m)

def footer_block(ftr):
    p = ftr.paragraphs[0]; p.style = C.small_style(name="Footer small", color="404040"); p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.tab_stops.add_tab_stop(Cm(C.CONTENT_W), WD_TAB_ALIGNMENT.RIGHT)
    C.rich(p, f"STEELXPERT Kft. · Csaba Bán, MSc civil engineer (T-T/01-18387) · {DATE_NUM} · {A.rev}\tPage: ")
    C.field(p, "PAGE", C.HDR_SIZE); C.rich(p, " / "); C.field(p, "NUMPAGES", C.HDR_SIZE)

def signature(doc):
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(18); p.paragraph_format.keep_with_next = True
    C.rich(p, f"Budapest, {DATE_TXT}", size=10)
    p = doc.add_paragraph(); p.paragraph_format.keep_with_next = True; p.paragraph_format.space_after = Pt(0); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(A.signature, width=Cm(4.0))
    lines = ["- - - - - - - - - - - - - - - - - - - - - - -", "**STEELXPERT Kft.**", "Csaba Bán", "MSc civil engineer", "lead structural designer", "T-T/01-18387"]
    for i, ln in enumerate(lines):
        p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(0); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if i < len(lines) - 1: p.paragraph_format.keep_with_next = True
        C.rich(p, ln, size=10)

sec = doc.sections[0]; header_block(sec.header); footer_block(sec.footer)

# ---------------------------------------------------------------- content helpers
def H(level, text, new_page=False):
    h = doc.add_heading(text, level=level)
    if new_page: h.paragraph_format.page_break_before = True
    return h

def P(text, **kw):
    p = doc.add_paragraph(); C.rich(p, text, **kw); return p

def B(text):
    p = doc.add_paragraph(style="List Bullet"); C.rich(p, text); return p

def Q(n, question, decides=None):
    H(3, f"Q{n}. {question}")
    if decides:
        P(f"**Decision owner: {decides}.**")

def table(caption_no, caption, header, rows, widths):
    cap = doc.add_paragraph(style="Caption"); C.rich(cap, f"Table {caption_no}: {caption}"); cap.paragraph_format.keep_with_next = True
    t = doc.add_table(rows=1 + len(rows), cols=len(header)); t.style = doc.styles["Table Grid"]; C.set_widths(t, widths)
    C.cell_margins(t, top=45, bottom=30, left=60, right=60)
    for j, h in enumerate(header): C.cell_text(t.cell(0, j), h, size=10, bold=True); C.shade(t.cell(0, j), "E6E6E6")
    C.cant_split(t.rows[0], header=True)
    for i, r in enumerate(rows, 1):
        for j, v in enumerate(r): C.cell_text(t.cell(i, j), v, size=10)
        C.cant_split(t.rows[i])
    C.keep_table_start(t); doc.add_paragraph().paragraph_format.space_after = Pt(0)
    return t

# ---------------------------------------------------------------- cover
p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(60); C.rich(p, "TECHNICAL NOTE", size=10, bold=True, color="808080")
p = doc.add_paragraph(); C.rich(p, TITLE, size=20, bold=True); p.paragraph_format.space_after = Pt(4)
p = doc.add_paragraph(); C.rich(p, SUBTITLE, size=13); p.paragraph_format.space_after = Pt(24)
C.info_table(doc, [("Project:", PROJECT), ("Client:", "FlexInSheet Kft. (FLINS)\n2400 Dunaújváros, Előd utca 4."),
                   ("Subject:", "Feasibility of the product and of its design and proposal tool: questions, provisional answers and open decisions"),
                   ("Engineer:", "STEELXPERT Kft.\nCsaba Bán, MSc civil engineer (T-T/01-18387)"),
                   ("Inputs:", "FlexInSheet brainstorming note (October 2026); STEELXPERT overview 'Hidegen hajlított acél padlórendszerek – tervezési alapok' (October 2026)"),
                   ("Document:", DOCID), ("Date:", DATE_TXT)])
doc.add_paragraph().paragraph_format.space_after = Pt(12)
table("A", "Revision history", ["Rev.", "Description", "Date", "Prepared", "Checked"],
      [[A.rev, "First issue for discussion with the development team", DATE_NUM, "Cs. Bán", "–"]], [1.3, 8.2, 2.4, 2.3, 2.3])

# ---------------------------------------------------------------- table of contents
H(1, "Contents", new_page=True)
p = doc.add_paragraph()
r = p.add_run(); fc = OxmlElement("w:fldChar"); fc.set(qn("w:fldCharType"), "begin"); r._r.append(fc)
r = p.add_run(); it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = ' TOC \\o "1-3" \\h \\z \\u '; r._r.append(it)
r = p.add_run(); fc = OxmlElement("w:fldChar"); fc.set(qn("w:fldCharType"), "separate"); r._r.append(fc)
p.add_run("Table of contents: right-click and update the field (F9) in Word.").italic = True
r = p.add_run(); fc = OxmlElement("w:fldChar"); fc.set(qn("w:fldCharType"), "end"); r._r.append(fc)

# ---------------------------------------------------------------- 1 purpose
H(1, "Purpose, inputs and how to read this note", new_page=True)
P("FlexInSheet Kft. is considering a new product: a cold-formed steel (CFS) floor framing system on screw-pile foundations for residential houses, "
  "together with a design and proposal tool for its sales staff. The brainstorming note of October 2026 asked for three things in order: "
  "a question-and-answer pass on the idea, a recommendation of the best technical and software options, and a first rough version of the tool.")
P("This note is the first of the three. It lists the questions that decide whether the product and the tool are feasible, gives a provisional answer "
  "or a working assumption for each, and names who has to take the decision where the answer is not the engineer's to give. The options "
  "and the rough tool are delivered separately in the development repository (documents 02 and 03 and the 'floorframe' package).")
P("Decision owners are marked at the start of the relevant answers: FlexInSheet (product decisions), the geotechnical partner (foundation decisions) "
  "and STEELXPERT (structural design basis). Everything else is a working assumption that stands until it is contradicted.")
P("Standards are cited by edition and clause (ref. ...). Load values quoted for Hungary are those of the MSZ EN National Annexes and are to be "
  "confirmed in the design basis document before any table is published.")

# ---------------------------------------------------------------- 2 product
H(1, "Product and scope", new_page=True)
Q(1, "Which floor type is the product?")
P("The STEELXPERT overview already narrows the choice to the joisted floor cassette: C-section joists on a rim track with an OSB deck, as used in the "
  "North American and British light steel framing practice (ref. AISI S240-15, section B2; SCI P402, section 2.1). Composite deck and volumetric "
  "modules are not pursued. The working assumption is a single-storey ground floor over screw piles first, with upper floors (wall-to-wall) added "
  "later from the same catalogue. The ground-floor case adds the bearer (sill) line on the pile heads, which the American and Canadian floor "
  "framing documents treat only generically, so this detail is developed in the project.")
Q(2, "Prefabricated cassette or site-assembled framing?", "FlexInSheet")
P("This decision fixes the joint catalogue (factory rivets or clinching versus site screws), adds the lifting and transport load case "
  "(ref. SCI P402, section 3.3.3) and decides whether the tool must split a layout into transportable panels of approximately 2.5 m by 12 m. "
  "Until it is taken, the rough tool assumes site-assembled stick framing, with panelisation kept as an optional post-processing step.")
Q(3, "What load envelope must the tables cover?")
P("Loads follow MSZ EN 1991-1-1 with the Hungarian National Annex. For category A floors the imposed load is q_[k] = 2.0 kN/m² (the British value of "
  "1.5 kN/m² quoted in the SCI sources does not apply). A partition allowance of 0.8 to 1.2 kN/m² and finishes of 0.5 to 1.5 kN/m² are added "
  "according to the build-up (dry floor about 0.4 kN/m², screed 1.5 kN/m² and above). Point loads are the 2.0 kN category A value plus user-defined "
  "loads (stoves, baths, pianos). The table axis is therefore the total characteristic load (g + q) in classes of 2.5, 3.5, 4.5 and 5.5 kN/m², "
  "with a separate point-load check.")
Q(4, "Which serviceability criteria apply?", "STEELXPERT")
P("The Hungarian National Annex leaves the deflection and vibration limits of lightweight floors to the designer. The default set proposed is the "
  "British one (ref. SCI P402, section 2.1.2): total deflection L/350 and 15 mm under characteristic loads, L/450 under imposed load alone, a "
  "deflection limit under a 1 kN point load, and a natural frequency of at least 8 Hz with 5 mm deflection under permanent load plus 20 % of the "
  "imposed load. Vibration governs long spans, so the span table carries a separate vibration column and not only a strength column. "
  "The CFSEI Tech Note J200-26 criteria (frequency, acceleration and deflection) are to be reviewed as an alternative.")
Q(5, "Which section family?", "FlexInSheet")
P("Lipped C-sections 150 to 300 mm deep in 1.2 to 2.5 mm S350GD+Z, at 400 or 600 mm spacing, with web holes for services, are assumed. The real family "
  "is defined by FlexInSheet's roll-former. The catalogue is a data file in the tool, so changing the family costs nothing in software; it does "
  "cost a re-run of the analysis campaign. Rim track and bearers are back-to-back C or box sections from the same family.")

# ---------------------------------------------------------------- 3 structural method
H(1, "Structural method", new_page=True)
Q(6, "AISI as guidance and Eurocode as verification: are the two compatible?")
P("Yes. AISI S240-15 supplies the framing rules: bearing stiffeners, blocking, web-hole limits, diaphragm detailing and the span-table format "
  "(ref. sections B2.2 to B2.7, B1.5). Resistances are produced by geometrically and materially nonlinear analysis with imperfections (GMNIA) and "
  "verified under EN 1993-1-3 and EN 1993-1-14 with the Eurocode partial factor γ_[M1]. The Direct Strength Method (ref. AISI S100-16, Appendix 1) "
  "serves as the independent benchmark of every GMNIA peak, as in the virtual-testing method already in use at STEELXPERT. Where AISI prescribes a "
  "rule that Eurocode does not (for example the bearing-stiffener rules), the AISI rule is adopted and proved by the finite element study.")
Q(7, "Is a parametric GMNIA load-table campaign feasible with CalculiX?")
P("It is feasible and the method is proven at member level. The size of the campaign is about 340 joist cases (7 sections, 2 spacings, 6 spans, "
  "4 load classes), about 60 support and web-crippling cases and about 80 bearer cases. At 5 to 20 minutes per displacement-controlled S8R shell "
  "run this is a few CPU-days on one workstation and is trivially parallel. The expensive part is not the solving but the validation: EN 1993-1-14 "
  "requires a model factor γ_[FE] calibrated against physical tests for cases without a validated Eurocode resistance model (ref. EN 1993-1-14:2025, "
  "Annex A; EN 1990, Annex D). At least one test series per governing failure mode is to be budgeted.")
Q(8, "Which failure modes must the tables resolve?")
P("At mid-span: local and distortional buckling in bending with the top flange restrained by the deck and the bottom flange free, and the vibration "
  "criterion. At the supports: web crippling with and without a bearing stiffener (ref. EN 1993-1-3, 6.1.7; AISI S100-16, E3.3). The STEELXPERT "
  "overview is correct that the support condition governs most often. At the pile head: combined bending, crippling and hold-down of the bearer. "
  "Each is a separate table.")
Q(9, "Should the joints be parametric too?")
P("Yes, but with physical tests as the primary source. The joist-to-rim connection (clip angle, swaged end or tab), the joist-to-bearer connection "
  "and the bearer-to-pile-head connection are the three joints. GMNIA of screwed joints is possible with the hinge and spring idealisation already in "
  "the method, but for self-drilling screws EN 1993-1-3, section 8 with test calibration is cheaper and more reliable. The recommendation is "
  "test-based joint resistances, with finite element work reserved for the pile-head detail, which is the only non-standard joint.")
Q(10, "What is needed from the geotechnical side?", "geotechnical partner")
P("The tool needs only four things from the geotechnical partner: the design compression resistance per pile type and length class, the lateral and "
  "uplift resistances, the minimum pile spacing, and the frost-depth rule. These enter as a second catalogue file. The tool never computes soil "
  "mechanics. The Hungarian acceptance route for screw piles (the DIBt route described in the overview is German) is a separate question and is "
  "listed under the risks.")

# ---------------------------------------------------------------- 4 application
H(1, "The design and proposal tool", new_page=True)
Q(11, "Who uses it and what must it output?")
P("Sales staff with a basic technical background. The output is a proposal pack: a plan with joists, bearers and piles, a bill of materials, a price "
  "and a design-basis sheet signed off by the engineer. The structural part must be deterministic and traceable (table look-up plus documented "
  "rules) so that a proposal is reproducible and auditable. Artificial intelligence must never be in the load path.")
Q(12, "Is input from the authority permit drawings realistic?")
P("Partly. Hungarian permit sets are PDF; DXF is available in perhaps half of the cases on request. Vectorised PDF line extraction works for walls "
  "when the drawing is clean and fails on hatched or raster plans. The practical path has three levels: DXF import; vector-PDF import with the "
  "user confirming the outline; and manual tracing of the floor outline in the browser over the PDF shown as an image. The third level is the "
  "safety net and must exist from the first version.")
Q(13, "Client PC, own server and browser: a contradiction?")
P("No. A Python backend (FastAPI) with a browser front-end runs identically on a laptop (single executable or Docker), on FlexInSheet's server or "
  "hosted. Catalogues and load tables are fetched from a central URL with a local cache, so an update does not require a reinstallation. This is "
  "the same stack as the CFD applications under development.")
Q(14, "Should it be AI-assisted?")
P("Yes, outside the load path: interpretation of drawings (which polygon is the floor, which walls are load-bearing), proposal text, question "
  "answering for sales staff, and on the developer side as the driver of the finite element campaign through the PrePoMax and CalculiX MCP server. "
  "The structural engine stays plain code.")
Q(15, "FreeCAD as the user interface?")
P("No for the sales tool: too heavy, desktop only, and a steep interface for non-engineers. FreeCAD remains an option as an exporter (IFC, 3D) "
  "later. A web interface with a 2D SVG canvas is sufficient for a layout tool.")

# ---------------------------------------------------------------- 5 risks
H(1, "Risks and verdict", new_page=True)
P("The risks, in order of weight:")
risks = ["Hungarian acceptance of screw piles. There is no national rule; the DIBt route is German. Decision owner: geotechnical partner.",
         "Model factor γ_[FE]. Without physical tests the tables are not Eurocode-compliant (ref. EN 1993-1-14:2025, Annex A).",
         "Vibration criteria. The Hungarian National Annex does not define them; an explicit design basis is required.",
         "Drawing import quality. Mitigated by the manual tracing level of the import.",
         "Fire and acoustic performance. Both are test-based and not calculable; they constrain the build-up catalogue, not the tool."]
for i, r in enumerate(risks, 1):
    p = doc.add_paragraph(); p.paragraph_format.left_indent = Cm(0.8); p.paragraph_format.first_line_indent = Cm(-0.8); C.rich(p, f"{i}.\t{r}")
    p.paragraph_format.tab_stops.add_tab_stop(Cm(0.8))
P("Verdict: the product and the tool are feasible. The structural pipeline is an extension of the virtual-testing method already in use; the tool is "
  "standard web engineering. The critical path is the physical test series and the geotechnical acceptance route, not the software.")
table("1", "Open decisions and their owners", ["Item", "Owner", "Needed for"],
      [["Prefabricated cassette or site-assembled framing (Q2)", "FlexInSheet", "Joint catalogue, lifting load case, panelisation"],
       ["Section family of the roll-former (Q5)", "FlexInSheet", "Analysis campaign, catalogue file"],
       ["Serviceability and vibration criteria (Q4)", "STEELXPERT", "Design basis, span tables"],
       ["Pile design values, spacing, frost rule (Q10)", "Geotechnical partner", "Pile catalogue file"],
       ["Hungarian acceptance route for screw piles", "Geotechnical partner", "Product approval"]], [7.0, 3.5, 6.0])
signature(doc)

Path(A.out).parent.mkdir(parents=True, exist_ok=True); doc.save(A.out)

# English locale on every layer: the python-docx default template leaves en-US tags behind
import zipfile, shutil, tempfile
tmp = A.out + ".tmp"
with zipfile.ZipFile(A.out) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename.endswith(".xml"):
            data = data.replace(b'w:val="en-US"', b'w:val="en-GB"').replace(b'w:eastAsia="en-US"', b'w:eastAsia="en-GB"')
        zout.writestr(item, data)
shutil.move(tmp, A.out)
print("saved", A.out, "pending:", sorted(set(C.PENDING)))
