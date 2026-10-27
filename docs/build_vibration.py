#!/usr/bin/env python3
"""Build FLINS-CFS-005: floor vibration criteria for the design basis."""
from __future__ import annotations
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import sxnote, vib_calc as v
from floorframe import catalog

ap = argparse.ArgumentParser()
ap.add_argument("--common", required=True); ap.add_argument("--signature", required=True); ap.add_argument("--figs", required=True); ap.add_argument("--out", required=True)
ap.add_argument("--projno", default="2026.032a"); ap.add_argument("--rev", default="rev0"); ap.add_argument("--final", action="store_true")
A = ap.parse_args(); F = Path(A.figs)
PROJECT = "FlexInSheet cold-formed steel floor framing system on screw piles: product development"
DOCID = f"STEELXPERT {A.projno} — FLINS-CFS-005 {A.rev}"
TITLE = "Floor vibration criteria for the design basis"
SUBTITLE = "International practice for lightweight residential floors and a provisional criterion set for the span tables"
N = sxnote.Note(A.common, A.signature, A.projno, DOCID, PROJECT, "27 October 2026", "27.10.2026", (2026, 10, 27), A.rev,
                title=TITLE, subject=SUBTITLE, keywords="floor vibration, EN 1995-1-1 7.3.3, SCI P354, CFSEI J200-26, ATC DG1, Onysko, lightweight floor", final=A.final)
H, P, B, T, FIG = N.H, N.P, N.B, N.table, N.figure
N.cover(TITLE, SUBTITLE, [("Project:", PROJECT), ("Client:", "FlexInSheet Kft. (FLINS)\n2400 Dunaújváros, Előd utca 4."),
    ("Subject:", "Answers Q4 and risk item 3 of the feasibility note: the Hungarian National Annex gives no vibration criterion for lightweight floors; international practice is adopted"),
    ("Status:", "Desk research from published summaries and standing knowledge, with screening calculations on the development catalogue. Values flagged in section 6 are to be verified against the documents."),
    ("Engineer:", "STEELXPERT Kft.\nCsaba Bán, MSc civil engineer (T-T/01-18387)"),
    ("Related:", f"STEELXPERT {A.projno} — FLINS-CFS-001 rev0 (Q&A); FLINS-CFS-002 rev0 (test plan, T6)"), ("Document:", DOCID), ("Date:", "27 October 2026")],
    [[A.rev, "First issue for discussion", "27.10.2026", "Cs. Bán", "–"]])
N.toc()

H(1, "Why vibration decides the span of this floor", new_page=True)
P("A cold-formed steel joist floor with a wood-based deck weighs 50 to 120 kg/m². Its strength is rarely the limit of the span; its "
  "response to a person walking is. Low mass means that a footfall produces a larger acceleration than on a concrete floor of the same "
  "stiffness, and the natural frequency sits in the range where either resonance with walking harmonics (below about 8 to 10 Hz) or the "
  "transient response to each heel strike (above it) is felt. Eurocode 0 (ref. EN 1990:2002, A1.4.4) requires the check and refers to the "
  "material parts; EN 1993 has no criterion for floors of this kind, and the Hungarian National Annexes are silent. The criterion must "
  "therefore be adopted from international practice and stated in the design basis, as agreed in the comment on Q4.")
P("The screening calculation in Figure 1 shows the consequence for the catalogue. With the dry build-up, the 200 mm joist at 600 mm "
  "spacing drops below 8 Hz at about 4.8 m, well inside its strength span; with a heavier build-up, which the acoustic and fire "
  "requirements of a separating floor bring anyway, the frequency falls further because the added mass is not matched by stiffness. The "
  "vibration column of the span tables therefore governs most of the practical spans, and the criterion chosen here sets the product's "
  "economy.")
FIG(F / "F1_frequency_vs_span.png", "Fundamental frequency of simply supported catalogue joists at 600 mm against span, for two floor masses (placeholder section stiffness, 0.85 I_[gross])")

H(1, "The criteria in use", new_page=True)
P("Four families of criteria are in use for lightweight floors; most national practices combine two of them.")
H(2, "Frequency floor")
P("EN 1995-1-1:2004, 7.3.3 for residential timber floors requires special investigation below f_[1] = 8 Hz, and most National Annexes keep "
  "the 8 Hz value; a European comparison finds cut-offs between 7 and 10.5 Hz across the countries. For cold-formed steel floors, research "
  "on floors with form deck and gypsum underlayment proposed a minimum of 10 Hz, because the low mass makes the second and third walking "
  "harmonics felt even above 8 Hz. SCI practice for light steel floors is that the floor should be a high-frequency floor above 8 Hz.")
H(2, "Stiffness under a 1 kN point load")
P("The most widely used criterion for lightweight joisted floors, because it correlates best with subjective ratings: the deflection "
  "under a 1 kN concentrated load, with load sharing to the neighbouring joists. Limits in use: Onysko (Canada, in the NBC Part 9 "
  "vibration criterion and ATC Design Guide 1): 2.0 mm below 3 m span and 8 / L^[1.3] mm above; UK National Annex to EN 1995-1-1: 1.8 mm "
  "below 4 m span, decreasing with span above; Sweden 1.5 mm; Australia 2.0 mm. EN 1995-1-1, 7.3.3 expresses the same check as "
  "w / F ≤ a with a national value a, and the Hungarian National Annex value of a is to be read (section 6).")
H(2, "Unit impulse velocity")
P("The second EN 1995-1-1 check, v ≤ b^[(f1 ζ − 1)], limits the velocity response to a unit impulse for high-frequency floors, with a "
  "national parameter b and damping ζ. It is rarely governing for steel joists with a stiff deck but is part of the Eurocode route and is "
  "kept as a check.")
H(2, "Response factor or acceleration")
P("The steel-industry method (ref. SCI P354, 2009 revised edition) computes the acceleration response to walking, weights it for human "
  "perception and compares it with the ISO 10137 and BS 6472 base curves through a response factor R; P354 has a section for light steel "
  "floors and a simplified high-frequency method. The multiplying factors for residential use are the lowest in the table (of the order of "
  "2 to 4 by day and 1.4 at night, to be confirmed in P354 Table 5.3), which lightweight floors meet only with mass and damping. The North "
  "American route (ref. AISC Design Guide 11, 2nd edition 2016; ATC Design Guide 1, 1999) limits the peak acceleration, 0.5 % g for "
  "offices and residences in DG11; CFSEI Tech Note J200-26 (January 2026) applies these to cold-formed steel joist floors and separates "
  "low-frequency from high-frequency systems. The University of Waterloo work (Parnell) found the ATC method the best predictor for CFS "
  "floors, with the walking acceleration within the ISO residential limit and the 1 kN deflection within the Onysko limit for the tested "
  "floors, and recommended design damping values that are to be taken from the thesis.")

H(1, "Provisional criterion set for the span tables", new_page=True)
P("Three tiers, all three to be satisfied; the first two are computed for every span-table cell, the third only where it can govern.")
T("Provisional vibration criteria", ["Tier", "Criterion", "Value", "Source"],
  [["1", "Fundamental frequency f_[1] (simply supported, permanent mass plus 10 % of imposed)", "≥ 8 Hz required; ≥ 10 Hz target for the dry build-up", "EN 1995-1-1 7.3.3; CFS research"],
   ["2", "Deflection under 1 kN at mid-span with load sharing k_[dist]", "≤ min(1.5 mm; 8 / L^[1.3] mm)", "Onysko / NBC; UK NA; Sweden"],
   ["3", "Response factor R by the SCI P354 high-frequency method, spans > 4.5 m or bays > 20 m²", "R ≤ 8 required; the residential day value of P354 as target", "SCI P354; ISO 10137"],
   ["–", "Unit impulse velocity v", "EN 1995-1-1 (7.4) with b from the Hungarian NA, as a check", "EN 1995-1-1 7.3.3"]], [1.0, 6.5, 5.0, 4.0])
P("The values are provisional. Tier 1 at 8 Hz is the European minimum; the 10 Hz target protects the dry build-up, which has the least "
  "mass and damping. Tier 2 takes the stricter of the Swedish constant and the Onysko span function, which coincide at about 3.6 m. "
  "Tier 3 is the only one that accounts for mass and damping explicitly and is the one the floor prototype test (ref. FLINS-CFS-002, T6) "
  "calibrates: measured frequency, damping and the 1 kN deflection are compared with the computed values, and the criterion set is "
  "adjusted once before the tables are frozen.")
P("Damping. Until the T6 measurement, the design values are 3 % for a bare joist floor with deck, 4.5 % with a plasterboard ceiling and "
  "partitions, consistent with P354 Table 4.1 for fitted-out steel floors and the lower end of the Waterloo recommendations.")

H(1, "How the engine computes the tiers", new_page=True)
P("Tier 1 uses EN 1995-1-1 (7.5): f_[1] = (π / 2L²) · √((EI)_[l] / m), with (EI)_[l] the joist bending stiffness per metre width (E I_[eff] / s) "
  "and m the floor mass in kg/m². The deck's own stiffness is ignored for the frequency, which is conservative for a screwed deck.")
P("Tier 2 computes w = F L³ / (48 E I_[eff]) · k_[dist], where k_[dist] is the share of the 1 kN load carried by the loaded joist. The UK "
  "National Annex expression, k_[dist] = max(0.38 − 0.08 ln(14 (EI)_[b] / s⁴), 0.30) with (EI)_[b] the deck stiffness across the joists "
  "in kNm²/m and s the spacing in m, gives the 0.30 floor value for a 22 mm OSB deck at 400 and 600 mm; a stiffer deck does not improve it "
  "further. The screwed deck-to-joist connection, its slip and the swaged or clip-angle ends all reduce the real stiffness below the "
  "simply supported ideal; the T6 test measures the difference and sets a stiffness factor for the tables.")
rows = []
for name in ("C200-1.5", "C250-2.0", "C300-2.5"):
    sec = catalog.section(name)
    for L in (3.0, 3.6, 4.2, 4.8, 5.4):
        f60, f110 = v.f1_hz(sec, L, 600, 60), v.f1_hz(sec, L, 600, 110)
        w = v.w_1kN_mm(sec, L, v.k_dist_ukna(sec, 600)); lim = min(1.5, v.onysko_limit_mm(L))
        ok = "yes" if (f60 >= 8 and w <= lim) else "no"
        rows.append([name, f"{L:.1f}", f"{f60:.1f}", f"{f110:.1f}", f"{w:.2f}", f"{lim:.2f}", ok])
T("Screening of the catalogue joists at 600 mm spacing (placeholder stiffness 0.85 I_[gross], k_[dist] = 0.30)",
  ["Section", "L [m]", "f1, 60 kg/m² [Hz]", "f1, 110 kg/m² [Hz]", "w(1 kN) [mm]", "limit [mm]", "Tier 1 and 2, dry"], rows, [2.2, 1.4, 2.8, 2.8, 2.4, 2.0, 2.9])
P("The screening shows the pattern the tables will have: the 1 kN deflection is comfortably met by all three sections at every span, "
  "and the frequency decides. For the heavier separating-floor build-up the 200 mm joist is limited to about 4.0 m and the 250 mm joist "
  "to about 5.2 m by the 8 Hz tier, before any response-factor check. Deeper joists, closer spacing or a stiffer composite deck are the "
  "levers; added mass alone makes it worse.")

H(1, "What the test programme adds", new_page=True)
P("The T6 floor prototype of the test plan measures the natural frequency and damping by heel drop and walking, and the 1 kN deflection "
  "(ref. ISO 18324:2016 for the method; SCI P354 Appendix for the walking test). The measured values calibrate the stiffness factor and the "
  "damping of this section, and a subjective rating by the people present is recorded alongside, which is how most of the criteria above "
  "were derived in the first place. A second measurement on the first built house closes the loop.")

H(1, "Verification list and sources", new_page=True)
T("Values to be verified against the source documents", ["Item", "Where", "Status"],
  [["Hungarian NA values of a, b and ζ for 7.3.3", "MSZ EN 1995-1-1 NA (MSZT)", "not retrieved"],
   ["Residential multiplying factors and light steel floor method", "SCI P354, Table 5.3 and section on light steel floors", "search summary; standing knowledge"],
   ["k_dist expression and the 1.8 mm limit", "UK NA to BS EN 1995-1-1, NA.2.6", "standing knowledge"],
   ["Onysko limits 2.0 mm and 8/L^1.3", "ATC DG1; NBC 2010 Part 9", "search summary"],
   ["Acceleration limit 0.5 % g", "AISC DG11, 2nd ed., Table 4-1", "standing knowledge"],
   ["CFS criteria and damping values", "CFSEI J200-26 (2026); Parnell, U. Waterloo thesis", "search summaries"],
   ["10 Hz proposal for CFS floors", "ICCFSS 2018/2019 papers (Missouri S&T repository)", "search summary"]], [6.0, 7.0, 3.5])
T("Sources consulted", ["Source", "Content"],
  [["EN 1990:2002, A1.4.4", "Vibration serviceability principle"],
   ["EN 1995-1-1:2004, 7.3.3 and (7.5)", "8 Hz, point-load and impulse-velocity checks, frequency formula"],
   ["SCI P354 (2009)", "Response-factor method, light steel floors, damping table"],
   ["SCI P402 (2015)", "8 Hz and 5 mm criteria quoted in the STEELXPERT overview"],
   ["CFSEI Tech Note J200-26 (2026)", "Vibration of cold-formed steel joist-framed floors"],
   ["AISC Design Guide 11 (2016); ATC Design Guide 1 (1999)", "Acceleration criteria; lightweight residential floors"],
   ["Parnell, University of Waterloo", "Vibration serviceability of CFS floors; ATC method; damping"],
   ["Onysko et al.; NBC Part 9", "1 kN deflection criterion"],
   ["Aalborg University comparison; SBUF 09038 (Sweden)", "National criteria for lightweight floors; light steel floor vibration"],
   ["ISO 10137:2007; ISO 18324:2016", "Base curves; floor vibration test method"]], [6.5, 10.0])
N.signature()
print("saved", A.out, "pending:", N.save(A.out))
