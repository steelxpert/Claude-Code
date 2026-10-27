#!/usr/bin/env python3
"""Build FLINS-CFS-003: how the AI assistance fits the tool and the workflow (plan for non-developers)."""
from __future__ import annotations
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import sxnote

ap = argparse.ArgumentParser()
ap.add_argument("--common", required=True); ap.add_argument("--signature", required=True); ap.add_argument("--figs", required=True); ap.add_argument("--out", required=True)
ap.add_argument("--projno", default="2026.032a"); ap.add_argument("--rev", default="rev0"); ap.add_argument("--final", action="store_true")
A = ap.parse_args(); F = Path(A.figs)

PROJECT = "FlexInSheet cold-formed steel floor framing system on screw piles: product development"
DOCID = f"STEELXPERT {A.projno} — FLINS-CFS-003 {A.rev}"
TITLE = "How the AI assistance fits the tool"
SUBTITLE = "A short plan for the development team: what the AI does, what it never does, and how it learns from real projects"
N = sxnote.Note(A.common, A.signature, A.projno, DOCID, PROJECT, "27 October 2026", "27.10.2026", (2026, 10, 27), A.rev,
                title=TITLE, subject=SUBTITLE, keywords="AI assistance, harness, drawing interpretation, proposal tool, auditability", final=A.final)
H, P, B, T, FIG = N.H, N.P, N.B, N.table, N.figure

N.cover(TITLE, SUBTITLE, [("Project:", PROJECT), ("Client:", "FlexInSheet Kft. (FLINS)\n2400 Dunaújváros, Előd utca 4."),
    ("Readers:", "Development team with a structural engineering background: STEELXPERT, the geotechnical partner, FlexInSheet. No programming knowledge assumed."),
    ("Subject:", "Answers the questions raised on Q12, Q13 and Q14 of the feasibility note"),
    ("Engineer:", "STEELXPERT Kft.\nCsaba Bán, MSc civil engineer (T-T/01-18387)"),
    ("Related:", f"STEELXPERT {A.projno} — FLINS-CFS-001 rev0 (feasibility Q&A); FLINS-CFS-002 rev0 (test plan)"),
    ("Document:", DOCID), ("Date:", "27 October 2026")],
    [[A.rev, "First issue for discussion", "27.10.2026", "Cs. Bán", "–"]])

# ---------------------------------------------------------------- 1
H(1, "The one rule", new_page=True)
P("The tool has two kinds of parts. The structural engine is plain, deterministic code: it reads the engineer-signed span tables, the joint "
  "and pile catalogues and the framing rules, and from a confirmed floor outline it produces the same layout, bill of materials and price every "
  "time. The AI assistance sits beside this engine. It prepares inputs for the user to confirm and explains outputs; it never selects a section, "
  "counts a pile or changes a table. Figure 1 shows the arrangement.")
P("The rule has a practical reason beyond safety. A proposal that goes out under a company name must be reproducible: two sales people with the "
  "same drawing must get the same answer, and the engineer must be able to trace every number to a table and a rule. An AI answer is not "
  "reproducible in that sense, so it is kept where a wrong answer costs a correction, not a structure.")
FIG(F / "F1_ai_touchpoints.png", "The AI touch points (A to D) beside the deterministic load path")

# ---------------------------------------------------------------- 2
H(1, "What the AI does: the four touch points", new_page=True)
H(2, "A. Reading the permit drawing")
P("The user uploads the permit plan (PDF or DXF). The AI proposes the floor outline, marks which walls it takes as load-bearing, and lists "
  "the point loads it can recognise (stove, chimney, bath). The proposal appears on screen over the drawing. The user corrects and confirms "
  "it, and only the confirmed geometry goes to the engine. On a clean DXF the AI will mostly be right; on a scanned PDF it will mostly be a "
  "head start for manual tracing. Both are useful.")
H(2, "B. Explaining the result and drafting the proposal")
P("The engine returns a layout and numbers. The AI turns them into the proposal text in the client's language, explains in plain words why "
  "the piles are where they are, and lists the assumptions the engineer must sign. It writes from the engine's output and the design basis "
  "only; it is not allowed to invent a number that is not in them.")
H(2, "C. Answering questions")
P("Sales staff ask: 'can we have 4 m between piles here', 'what if the client wants a tiled floor'. The AI answers from the design basis and "
  "the tables, or re-runs the engine with the changed input and shows the difference. Where the question needs the engineer, it says so and "
  "drafts the question for him.")
H(2, "D. The developer side")
P("The same AI, in its developer form (Claude Code), writes and tests the software, drives the finite element campaign through the PrePoMax "
  "and CalculiX connection, and builds the reports. This is where most of the AI effort of the project goes, and it is invisible to the sales "
  "user. The validated tables it helps produce are reviewed and signed by the engineer before they enter the tool.")
T("What the AI may and may not do", ["Allowed", "Not allowed"],
  [["Propose the floor outline and loads for confirmation", "Change a confirmed outline on its own"],
   ["Explain a result; draft proposal text from the engine output", "Invent a resistance, span, pile count or price"],
   ["Re-run the engine with a changed input and compare", "Edit the span tables or catalogues"],
   ["Draft a question for the engineer", "Sign off a design basis"],
   ["Write and test code; drive the FE campaign (developer side)", "Publish a table without the engineer's review"]], [8.2, 8.3])

# ---------------------------------------------------------------- 3
H(1, "How it learns: the harness", new_page=True)
P("The question from Q12 was whether the AI could be trained on real projects, in the way the PrePoMax harness is being built from recorded "
  "tutorials. It can, and the mechanism is simpler than it sounds. The AI model itself is not trained or modified. What is built is a "
  "harness: a set of written instructions, worked examples, checklists and automatic checks that the AI reads at the start of every "
  "session and that we own as ordinary files. The PrePoMax harness is exactly this, built from what the tutorials show.")
P("For the floor tool the harness is built from real projects, one at a time (Figure 2). Each project is a session in which the AI reads the "
  "drawing, the engineer corrects what it got wrong, and the correction is written into the instructions or added as a worked example. The "
  "same project, with its drawing and the confirmed correct result, is then stored as a test case. Every later change to the harness is "
  "scored against all stored test cases, so the tool can only get better on the plans it has already seen, and the score on new plans is "
  "measured and reported. After twenty or thirty real plans the harness covers the common Hungarian drawing conventions; after a hundred it "
  "is a trained assistant in every practical sense, and still nothing in it is a black box.")
FIG(F / "F2_harness_loop.png", "The harness loop: each real project becomes a rule, an example and a test case")
P("Three things make this work in practice. The corrections must be made by someone who knows what a load-bearing wall is, so the first "
  "projects are done with the engineer in the loop. The test set must be kept, which means a folder of drawings with their confirmed results "
  "and the permission to use them for this purpose. And the score must be looked at: a harness that is not measured drifts.")

# ---------------------------------------------------------------- 4
H(1, "Roles, data and cost", new_page=True)
H(2, "Roles")
P("The answer to the question on Q13 is yes. The owner of the tool and of its content is STEELXPERT (the signed tables, the design basis, the "
  "harness). The administrator who installs, updates and backs it up is the developer. Sales staff are users. The geotechnical partner "
  "supplies and reviews the pile catalogue. FlexInSheet decides the product content (sections, details, prices).")
H(2, "Where the data goes")
P("Client drawings are personal and commercial data. The tool runs on FlexInSheet's own server or on the sales laptop; drawings stay there. "
  "Only the parts the AI needs for a given step are sent to the AI service, under a commercial agreement that excludes the use of the data "
  "for training the provider's models. Nothing in the structural engine ever leaves the server. If FlexInSheet prefers, the AI touch points "
  "A to C can be switched off and the tool still works with manual tracing.")
H(2, "What it costs")
B("A commercial AI subscription for the sales users and the developer; in the order of a few hundred euros a month at the start.")
B("Developer time for the harness: the first ten projects take the longest, after that about an hour per project to fold in the corrections.")
B("Engineer time: the review of the first twenty readings, and the signed design basis that the AI answers from.")
B("A folder of real permit drawings with permission to use them as test cases.")
H(2, "First three months")
N.N(["Rough tool as it exists now: outline typed or DXF, engine, layout, bill of materials (done).",
     "Touch point A on DXF and clean PDF, with ten real drawings as the first test set.",
     "Touch point B: proposal text template approved by FlexInSheet, filled from the engine output.",
     "Harness and test set in place; score reported monthly; touch point C added once the design basis is signed."])
N.signature()
print("saved", A.out, "pending:", N.save(A.out))
