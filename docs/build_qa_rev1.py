#!/usr/bin/env python3
"""Build FLINS-CFS-001 rev1: the feasibility Q&A with the review answers of 27.10.2026 folded in."""
from __future__ import annotations
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import sxnote

ap = argparse.ArgumentParser()
ap.add_argument("--common", required=True); ap.add_argument("--signature", required=True); ap.add_argument("--out", required=True)
ap.add_argument("--projno", default="2026.032a"); ap.add_argument("--rev", default="rev1"); ap.add_argument("--final", action="store_true")
A = ap.parse_args()
PROJECT = "FlexInSheet cold-formed steel floor framing system on screw piles: product development"
DOCID = f"STEELXPERT {A.projno} — FLINS-CFS-001 {A.rev}"
TITLE = "Cold-formed steel floor framing on screw piles"
SUBTITLE = "Feasibility questions and answers for the product development"
N = sxnote.Note(A.common, A.signature, A.projno, DOCID, PROJECT, "27 October 2026", "27.10.2026", (2026, 10, 27), A.rev,
                title=TITLE, subject=SUBTITLE, keywords="cold-formed steel, floor framing, screw piles, GMNIA, Eurocode", final=A.final)
H, P, B, T = N.H, N.P, N.B, N.table

def Q(n, q, owner=None): H(3, f"Q{n}. {q}"); owner and P(f"**Decision owner: {owner}.**")
def R(text): P(f"**Review (27.10.2026):** {text}")

N.cover(TITLE, SUBTITLE, [("Project:", PROJECT), ("Client:", "FlexInSheet Kft. (FLINS)\n2400 Dunaújváros, Előd utca 4."),
    ("Subject:", "Feasibility of the product and of its design and proposal tool: questions, provisional answers, review answers and open decisions"),
    ("Engineer:", "STEELXPERT Kft.\nCsaba Bán, MSc civil engineer (T-T/01-18387)"),
    ("Inputs:", "FlexInSheet brainstorming note (October 2026); STEELXPERT overview 'Hidegen hajlított acél padlórendszerek – tervezési alapok' (October 2026); review comments on rev0 (27.10.2026)"),
    ("Follow-up notes:", "FLINS-CFS-002 test plan · CFS-003 AI assistance · CFS-004 fire and acoustics · CFS-005 vibration criteria · CFS-006 bearer concept"),
    ("Document:", DOCID), ("Date:", "27 October 2026")],
    [["rev1", "Review answers of 27.10.2026 folded in; project number assigned; follow-up notes referenced", "27.10.2026", "Cs. Bán", "–"],
     ["rev0", "First issue for discussion with the development team", "27.10.2026", "Cs. Bán", "–"]])
N.toc()

H(1, "Purpose, inputs and how to read this note", new_page=True)
P("FlexInSheet Kft. is considering a new product: a cold-formed steel (CFS) floor framing system on screw-pile foundations for residential houses, "
  "together with a design and proposal tool for its sales staff. The brainstorming note of October 2026 asked for a question-and-answer pass "
  "on the idea, a recommendation of the best options, and a first rough version of the tool. This note is the first of the three.")
P("Revision 1 folds in the review answers given on rev0: each question now carries the provisional answer, the review answer in bold, and "
  "where the review asked for more, a reference to the follow-up note that provides it. Decision owners are FlexInSheet (product), the "
  "geotechnical partner (foundation) and STEELXPERT (structural design basis).")

H(1, "Product and scope", new_page=True)
Q(1, "Which floor type is the product?")
P("The joisted floor cassette: C-section joists on a rim track with an OSB deck, as in the North American and British light steel framing "
  "practice (ref. AISI S240-15, section B2; SCI P402, section 2.1). Single-storey ground floor over screw piles first, upper floors later from "
  "the same catalogue. The bearer line on the pile heads is the detail the floor framing documents treat only generically.")
R("Agreed. The high concentrated reactions of the screw piles are not well covered in such systems; a member that distributes the inverted "
  "force flow is needed, built up from cold-formed sections (boxed or back-to-back) or hot-rolled (RHS, SHS, shallow HEA/HEB). "
  "The screening is in FLINS-CFS-006: bending never governs, web crippling at the pile head does, and two concepts go to the T3 tests.")
Q(2, "Prefabricated cassette or site-assembled framing?", "FlexInSheet")
P("Decides the joint catalogue, the lifting load case and whether the tool must panelise. The rough tool assumes site assembly.")
R("FlexInSheet has both manufacturing and site capabilities and is open to both; site assembly from linear pieces is expected first. "
  "The test plan keeps the cassette lifting test as an option (FLINS-CFS-002, section 6).")
Q(3, "What load envelope must the tables cover?")
P("MSZ EN 1991-1-1 with the Hungarian National Annex: q_[k] = 2.0 kN/m² for category A, partitions 0.8 to 1.2 kN/m², finishes 0.5 to 1.5 kN/m², "
  "point loads 2.0 kN plus user-defined. Table classes of total characteristic load 2.5, 3.5, 4.5 and 5.5 kN/m².")
R("Agreed. The realistic residential imposed load is 2.0 to 3.0 kN/m² at most, combined with line loads from partition and load-bearing walls "
  "and concentrated loads (stove, chimney). Line loads from walls are added to the table axes as a separate case.")
Q(4, "Which serviceability criteria apply?", "STEELXPERT")
P("The British set as the default (ref. SCI P402, section 2.1.2): L/350 and 15 mm total, L/450 imposed, a 1 kN point-load limit, 8 Hz with 5 mm "
  "under permanent plus 20 % imposed; a separate vibration column in the tables.")
R("Values accepted for now; international practice is relied on, based on the detailed research. That research is FLINS-CFS-005, which "
  "proposes a three-tier criterion set (8 Hz required and 10 Hz target; 1 kN deflection by the Onysko and Swedish limits; SCI P354 response "
  "factor for long spans) and shows that vibration, not strength, decides most spans.")
Q(5, "Which section family?", "FlexInSheet")
P("Lipped C 150 to 300 mm, 1.2 to 2.5 mm, S350GD+Z, at 400 or 600 mm, with service holes; the roll-former defines the real family.")
R("Agreed; see Q1 for the bearer sections.")

H(1, "Structural method", new_page=True)
Q(6, "AISI as guidance and Eurocode as verification: compatible?")
P("Yes: AISI S240-15 supplies the framing rules, GMNIA produces the resistances, EN 1993-1-3 and EN 1993-1-14 verify them with γ_[M1], and DSM "
  "(ref. AISI S100-16, Appendix 1) is the independent benchmark.")
R("Accepted.")
Q(7, "Is a parametric GMNIA load-table campaign feasible with CalculiX?")
P("Feasible and proven at member level; about 340 joist cases, 60 support cases, 80 bearer cases; a few CPU-days. The cost is the validation: "
  "a model factor γ_[FE] calibrated against physical tests per failure mode (ref. EN 1993-1-14:2025, Annex A).")
R("Sounds good. FlexInSheet always tests a new product physically, but not in a laboratory. The test plan (FLINS-CFS-002) is written for the "
  "FlexInSheet workshop, with accredited witnessing only for the approval test.")
Q(8, "Which failure modes must the tables resolve?")
P("Mid-span local and distortional buckling with the bottom flange free, vibration; web crippling at the supports with and without bearing "
  "stiffener (ref. EN 1993-1-3:2006, 6.1.7; AISI S100-16, G5); bearer bending, crippling and hold-down at the pile head.")
R("Agreed.")
Q(9, "Should the joints be parametric too?")
P("Test-based resistances for the screwed joints (ref. EN 1993-1-3:2006, section 8 and Annex A), finite element work only for the pile-head detail.")
R("Accepted, with the request for a rough test plan referenced to AISI and EN, with figures, incorporating Q7. Delivered as FLINS-CFS-002: "
  "series T0 to T6, six set-up figures, matrix and evaluation.")
Q(10, "What is needed from the geotechnical side?", "geotechnical partner")
P("Design compression, lateral and uplift resistances per pile type and length, minimum spacing, frost rule; a catalogue file. The tool "
  "never computes soil mechanics.")
R("Noted.")

H(1, "The design and proposal tool", new_page=True)
Q(11, "Who uses it and what must it output?")
P("Sales staff; a proposal pack with layout, bill of materials, price and a signed design basis; deterministic and traceable structural part.")
R("Sounds good.")
Q(12, "Is input from the authority permit drawings realistic?")
P("Partly: DXF import, vector-PDF import with confirmation, and manual tracing over the PDF as the safety net.")
R("Agreed. The question whether AI can be used here, as a harness built in consecutive sessions on real layouts like the PrePoMax harness, "
  "is answered in FLINS-CFS-003: yes, as touch point A, with the harness loop built from real projects and a scored test set.")
Q(13, "Client PC, own server and browser: a contradiction?")
P("No: Python backend with a browser front-end runs on a laptop, on FlexInSheet's server or hosted; catalogues from a central URL with a local cache.")
R("Good. The owner is STEELXPERT (content, tables, design basis, harness) and the administrator is the developer; sales staff are users "
  "(FLINS-CFS-003, section 4).")
Q(14, "Should it be AI-assisted?")
P("Yes, outside the load path: drawing interpretation, proposal text, questions, and the developer side driving the FE campaign.")
R("More was asked for, in a form for non-developers with a structural background. Delivered as FLINS-CFS-003 (5 pages).")
Q(15, "FreeCAD as the user interface?")
P("No for the sales tool; web interface with a 2D canvas. FreeCAD as a later exporter.")
R("Agreed; IFC export is wanted.")

H(1, "Risks and verdict", new_page=True)
N.N(["Hungarian acceptance of screw piles. No national rule; the DIBt route is German. **Review:** FlexInSheet has considerable experience with all aspects of screw-pile practice; the route is to be documented with them.",
     "Model factor γ_[FE]. Without physical tests the tables are not Eurocode-compliant (ref. EN 1993-1-14:2025, Annex A). **Review:** to be seen after the test plans; now FLINS-CFS-002.",
     "Vibration criteria. The Hungarian National Annex does not define them. **Review:** international practice is adopted on the basis of the research; now FLINS-CFS-005.",
     "Drawing import quality. Mitigated by the manual tracing level. **Review:** agreed.",
     "Fire and acoustic performance. Test-based, not calculable. **Review:** seen as a big problem; thorough research before any analysis work, a fire expert to be hired by FlexInSheet, and the Lindab purlin fire paper as a reference. Research delivered as FLINS-CFS-004; the Lindab paper was not found online and a copy is requested."])
P("Verdict unchanged: the product and the tool are feasible. The critical path is the physical test series, the fire concept and the "
  "geotechnical acceptance route, not the software.")
T("Open decisions and their owners after the review", ["Item", "Owner", "Needed for"],
  [["Prefabricated cassette or site-assembled framing (Q2): site assembly expected, to be confirmed", "FlexInSheet", "Joint catalogue, lifting load case"],
   ["Section family of the roll-former (Q5)", "FlexInSheet", "Analysis campaign, catalogue file"],
   ["Bearer concept: boxed CFS with stiffeners or hot-rolled (Q1)", "STEELXPERT with FlexInSheet, after T3", "Pile-line detail, tables"],
   ["Vibration criterion set (Q4): provisional set in CFS-005", "STEELXPERT", "Design basis, span tables"],
   ["Pile design values, spacing, frost rule (Q10)", "Geotechnical partner", "Pile catalogue file"],
   ["Fire concept and expert; Lindab paper", "FlexInSheet (expert), Csaba Bán (paper)", "Build-up catalogue, approval"],
   ["Hungarian acceptance route for screw piles", "FlexInSheet with the geotechnical partner", "Product approval"]], [7.0, 4.0, 5.5])
N.signature()
print("saved", A.out, "pending:", N.save(A.out))
