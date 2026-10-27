#!/usr/bin/env python3
"""Build FLINS-CFS-006: bearer concept study (built-up CFS versus hot-rolled sections under pile reactions)."""
from __future__ import annotations
import argparse, math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import sxnote, bearer_calc as bc

ap = argparse.ArgumentParser()
ap.add_argument("--common", required=True); ap.add_argument("--signature", required=True); ap.add_argument("--figs", required=True); ap.add_argument("--out", required=True)
ap.add_argument("--projno", default="2026.032a"); ap.add_argument("--rev", default="rev0"); ap.add_argument("--final", action="store_true")
A = ap.parse_args(); F = Path(A.figs)
PROJECT = "FlexInSheet cold-formed steel floor framing system on screw piles: product development"
DOCID = f"STEELXPERT {A.projno} — FLINS-CFS-006 {A.rev}"
TITLE = "Bearer concept study"
SUBTITLE = "Built-up cold-formed sections against hot-rolled sections for the bearer that carries the screw-pile reactions"
N = sxnote.Note(A.common, A.signature, A.projno, DOCID, PROJECT, "27 October 2026", "27.10.2026", (2026, 10, 27), A.rev,
                title=TITLE, subject=SUBTITLE, keywords="bearer, screw pile, web crippling, EN 1993-1-3 6.1.7, HEA, RHS, back-to-back", final=A.final)
H, P, B, T, FIG = N.H, N.P, N.B, N.table, N.figure
N.cover(TITLE, SUBTITLE, [("Project:", PROJECT), ("Client:", "FlexInSheet Kft. (FLINS)\n2400 Dunaújváros, Előd utca 4."),
    ("Subject:", "Answers the comment on Q1 of the feasibility note: the concentrated pile reactions need a member that distributes the inverted force flow; built-up CFS, RHS, SHS and shallow I-sections are compared"),
    ("Status:", "Screening calculation with placeholder section data; the decision is taken after the T3 bearer tests of the test plan"),
    ("Engineer:", "STEELXPERT Kft.\nCsaba Bán, MSc civil engineer (T-T/01-18387)"),
    ("Related:", f"STEELXPERT {A.projno} — FLINS-CFS-001 rev0 (Q&A); FLINS-CFS-002 rev0 (test plan, T2b/T3/T5); FLINS-CFS-005 rev0 (vibration)"), ("Document:", DOCID), ("Date:", "27 October 2026")],
    [[A.rev, "First issue for discussion", "27.10.2026", "Cs. Bán", "–"]])
N.toc()

H(1, "The problem", new_page=True)
P("In a wall-supported floor the joist reactions are spread along a sill. On screw piles they are collected into a bearer and delivered to "
  "the piles at 2 to 3 m centres: the force flow is inverted, a distributed load from above against concentrated reactions from below. "
  "The comment on Q1 of the feasibility note states the consequence: light steel framing systems do not cover this case well, and the "
  "bearer may need hot-rolled steel. This note screens the candidates against the same demand and says which detail the tests should "
  "decide between.")
P("Demand. One bay of floor of B = 3.0 m tributary width with g = 1.5 and q = 2.0 kN/m² gives a design line load of about 15 kN/m on the "
  "bearer. For a continuous bearer the design moment is taken as w_[d] s_[p]² / 10 and the interior pile reaction as 1.1 w_[d] s_[p]; at "
  "pile spacings of 2.0, 2.5 and 3.0 m that is 6 to 14 kNm and 33 to 50 kN. The pile reaction is the figure that matters.")
FIG(F / "F1_bearer_candidates.png", "Bearer candidates on the pile head plate: (a) to (c) cold-formed, (d) and (e) hot-rolled")

H(1, "Candidates and checks", new_page=True)
P("Five candidates are screened (Figure 1). Bending uses the placeholder effective section of the development catalogue for the "
  "cold-formed sections and the plastic resistance for the hot-rolled ones. Web crippling at the pile head uses EN 1993-1-3:2006, "
  "equation (6.15) for a single unstiffened web in category 2 (interior support, bearing length 150 mm, 90° load, inner radius 1.5 t), "
  "doubled for the pair; the boxed pair is taken as two single webs, which is slightly conservative. The interaction of bending and "
  "crippling follows equation (6.28), M_[Ed] / M_[c,Rd] + R_[Ed] / R_[w,Rd] ≤ 1.25. For the hot-rolled sections the patch-load resistance "
  "of EN 1993-1-5, section 6 is far above the demand and is reported only as a lower bound. Deflection is checked at s_[p] / 350 under "
  "the characteristic load.")
rows = []
for s_p in (2.0, 2.5, 3.0):
    d = bc.demands(s_p, 3.0)
    for c in bc.CANDIDATES:
        r = bc.check(c, s_p, 3.0)
        rows.append([f"{s_p:.1f}", c["name"].replace(" back-to-back", ""), f"{c['M_Rd']:.0f}", f"{r['uM']:.2f}", f"{c['R_w']:.0f}", f"{r['uR']:.2f}",
                     "–" if r["inter"] is None else f"{r['inter']:.2f}", f"{r['delta']:.1f}", f"{c['mass']:.1f}"])
T("Screening at bay 3.0 m, g = 1.5, q = 2.0 kN/m² (M_Ed 6.0 / 9.4 / 13.6 kNm, R_Ed 33 / 42 / 50 kN at 2.0 / 2.5 / 3.0 m)",
  ["s_p [m]", "Candidate", "M_Rd [kNm]", "M_Ed/M_Rd", "R_w,Rd [kN]", "R_Ed/R_w,Rd", "(6.28)", "δ [mm]", "kg/m"], rows, [1.2, 3.4, 1.9, 1.8, 1.9, 2.0, 1.3, 1.4, 1.3], size=8)
FIG(F / "F2_crippling_utilisation.png", "Web-crippling utilisation at the pile head for the candidates and three pile spacings")

H(1, "What the screening says", new_page=True)
B("**Bending never governs.** The deepest cold-formed pair is at 47 % in bending at 3.0 m spacing and the hot-rolled sections at "
  "10 to 33 %. Deflection is below 4 mm against 8.6 mm allowed for all candidates.")
B("**Crippling at the pile governs the cold-formed bearers.** The 2.0 mm pair is over its limit at 2.5 m and well over at 3.0 m; the 2.5 mm "
  "pair passes crippling alone but fails the interaction at 3.0 m and sits at the limit at 2.5 m. This is the inverted force flow of the "
  "comment, in numbers: the web of a cold-formed section is the wrong element to receive a 50 kN reaction through a 150 mm plate.")
B("**A bearing stiffener at each pile changes the picture.** With a stiffener (a short stud section or a plate angle screwed inside each "
  "web, AISI S240-15, B2.5) the reaction goes into the stiffener and the cold-formed pair becomes adequate at 3.0 m; the cost is one "
  "fitted part per pile, and the stiffener resistance comes from test T2b.")
B("**The hot-rolled sections carry the reaction without thought** and at 19 to 25 kg/m against 13 to 18 kg/m for the cold-formed pairs; "
  "the mass difference is small because the cold-formed pair must be deep and doubled. HEA 120 and RHS 150×100 fit inside the floor "
  "depth; HEA 140 is the stiffest of the shallow options. Hot-rolled bearers need hot-dip galvanising after fabrication, bolted end "
  "plates, and a bolted or clamped joist-to-bearer connection instead of screws.")
B("**Torsion and tolerance.** An open back-to-back pair has little torsional stiffness; a bearer placed 50 mm off the pile axis by the "
  "installation tolerance (ref. FLINS-CFS-002, T5) twists it and loads one web. The boxed pair, the RHS and, to a lesser degree, the HEA "
  "take the eccentricity in the section. This favours the closed shapes for the pile line.")
B("**Bearer stiffness enters the floor frequency.** The joist frequency of the span tables assumes rigid supports. A shallow bearer on "
  "3.0 m piles has a frequency of its own of 15 to 29 Hz with the tributary floor mass; combined with an 8 Hz joist floor by Dunkerley's "
  "rule the system drops to 7.0 Hz on HEA 120 and to 7.7 Hz on the deep cold-formed pair. The bearer must therefore be stiff as well as "
  "strong, which counts against the shallowest hot-rolled sections and in favour of the 250 to 300 mm deep cold-formed pair or HEA 140.")

H(1, "Recommendation for the test plan", new_page=True)
P("Two concepts go into the T3 tests, not five. Concept 1 is the all-cold-formed line: a boxed pair of the deepest catalogue section in "
  "2.5 mm with a bearing stiffener at every pile and a slotted head plate for tolerance. Concept 2 is the hybrid line: a hot-dip "
  "galvanised HEA 140 (or RHS 150×100×5 where depth is limited) bolted to the pile head, with the cold-formed joists on clip angles. "
  "The expected result is that concept 1 is cheaper in material and fits the roll-former business, and concept 2 is cheaper in labour "
  "and more tolerant on site; the T3 and T5 tests give the crippling and eccentricity data that decide between them, and the pile "
  "spacing the geotechnical partner can offer decides whether the question matters at all (at 2.0 m spacing concept 1 passes without "
  "stiffeners).")
P("Whichever concept is chosen, three details are fixed now: the pile head plate is at least 150 mm long in the bearer direction with "
  "slotted holes of ± 25 mm each way; the bearer is continuous over at least two piles with any splice placed at a quarter point; and "
  "the bearer line carries the uplift and the horizontal shear of the house to the piles, which the T5 tests cover.")
T("Comparison of the two concepts", ["Aspect", "Concept 1: boxed 2×C + stiffeners", "Concept 2: HEA 140 / RHS bolted"],
  [["Crippling at 3.0 m piles", "stiffener required and tested", "margin > 5"],
   ["Mass per metre", "about 16 to 18 kg/m + stiffeners", "19 to 25 kg/m"],
   ["Torsion from eccentricity", "closed box: good", "RHS good; HEA adequate"],
   ["Floor frequency penalty", "small (deep section)", "small for HEA 140; noticeable for HEA 120"],
   ["Corrosion in the crawl space", "Z275/Z350 strip, cut edges", "hot-dip galvanised after fabrication"],
   ["Connections", "screws, factory-made", "bolts and clip angles"],
   ["Fits FlexInSheet production", "yes", "bought-in sections"],
   ["Tests needed", "T2b, T3, T5", "T5 only"]], [4.5, 6.0, 6.0])
N.signature()
print("saved", A.out, "pending:", N.save(A.out))
