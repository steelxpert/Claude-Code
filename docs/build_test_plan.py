#!/usr/bin/env python3
"""Build FLINS-CFS-002: test plan for members and joints (.docx).
Usage: python3 docs/build_test_plan.py --common common.py --signature sig.png --figs FIGDIR --out OUT.docx [--projno 2026.032a] [--final]"""
from __future__ import annotations
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import sxnote

ap = argparse.ArgumentParser()
ap.add_argument("--common", required=True); ap.add_argument("--signature", required=True); ap.add_argument("--figs", required=True); ap.add_argument("--out", required=True)
ap.add_argument("--projno", default="2026.032a"); ap.add_argument("--rev", default="rev0"); ap.add_argument("--final", action="store_true")
A = ap.parse_args(); F = Path(A.figs)

PROJECT = "FlexInSheet cold-formed steel floor framing system on screw piles: product development"
DOCID = f"STEELXPERT {A.projno} — FLINS-CFS-002 {A.rev}"
TITLE = "Test plan for members and joints"
SUBTITLE = "Physical tests for the validation of the GMNIA span tables and for the test-based joint resistances"
N = sxnote.Note(A.common, A.signature, A.projno, DOCID, PROJECT, "27 October 2026", "27.10.2026", (2026, 10, 27), A.rev,
                title=TITLE, subject=SUBTITLE, keywords="cold-formed steel, test plan, GMNIA validation, EN 1993-1-14, AISI S100 K2, web crippling, joist connector", final=A.final)
H, P, B, T, FIG = N.H, N.P, N.B, N.table, N.figure

N.cover(TITLE, SUBTITLE, [("Project:", PROJECT), ("Client:", "FlexInSheet Kft. (FLINS)\n2400 Dunaújváros, Előd utca 4."),
    ("Subject:", "Rough test plan answering Q7 and Q9 of the feasibility note: which specimens, which set-ups, how many, how the results are evaluated under EN 1993-1-3 Annex A, EN 1990 Annex D, EN 1993-1-14 and AISI S100-16 Chapter K"),
    ("Engineer:", "STEELXPERT Kft.\nCsaba Bán, MSc civil engineer (T-T/01-18387)"),
    ("Related:", f"STEELXPERT {A.projno} — FLINS-CFS-001 rev0 (feasibility Q&A); development repository, package 'floorframe', module fea/campaign.py"),
    ("Document:", DOCID), ("Date:", "27 October 2026")],
    [[A.rev, "First issue for discussion: test philosophy, series T0 to T6, matrix and evaluation", "27.10.2026", "Cs. Bán", "–"]])
N.toc()

# ------------------------------------------------------------------ 1
H(1, "Purpose and scope", new_page=True)
P("This note sets out the physical tests needed to put the FlexInSheet floor system on a Eurocode footing. It answers two questions from the "
  "feasibility note (ref. FLINS-CFS-001, Q7 and Q9): what tests are needed so that the span tables produced by the GMNIA campaign can be used "
  "as design resistances, and what tests give the resistances of the three joints that the finite element work does not cover economically.")
P("The plan is a first version for discussion with FlexInSheet and the geotechnical partner. Specimen counts, spans and the section family are "
  "placeholders tied to the catalogue of the development repository and will be fixed once the roll-former profile set is known "
  "(ref. FLINS-CFS-001, Q5). Fire and acoustic testing are outside this plan; they are the subject of a separate research note.")
P("Standards are cited by edition and clause (ref. ...). Clause numbers were taken from the editions listed in section 9 and are to be checked "
  "against STEELXPERT's indexed standards library before the plan is issued to a testing body.")

# ------------------------------------------------------------------ 2
H(1, "Test philosophy", new_page=True)
P("The tests have three different jobs, and the evaluation differs for each. Figure 1 shows how the series feed each other.")
B("**Validation of the finite element model.** Member tests (T1, T2) are compared with GMNIA runs that use the measured material, thickness and "
  "initial imperfection of each specimen. The comparison fixes the model factor γ_[FE] that converts the GMNIA peak into a design resistance "
  "(ref. EN 1993-1-14:2025, section 7 and Annex A). Once validated, the model is used to produce the full span-table matrix for all sections, "
  "spacings and load classes without further testing. This is the economic reason for the GMNIA route: the tests are few, the tables are many.")
B("**Test-based resistances.** Joint and bearer tests (T3, T4, T5) give characteristic and design resistances directly from the test results "
  "(ref. EN 1993-1-3:2006, section 9 and Annex A.6; EN 1990:2002, Annex D; AISI S100-16, Chapter K2.1). The finite element model is used only "
  "for the pile-head detail, where the force flow is non-standard.")
B("**Confirmation of the system.** One or two floor prototypes (T6) confirm that the components behave together as assumed: support stiffness, "
  "load sharing, vibration and the ultimate behaviour of the assembly (ref. EN 1993-1-3:2006, Annex A.4.2 and A.4.3; AISI S100-16, K2.2).")
FIG(F / "F1_programme.png", "Test programme: what each series produces and where it is used")
P("Two principles follow from the method already in use at STEELXPERT. First, the failure mode matters more than the amplitude: every specimen is "
  "measured for initial geometric imperfection before testing, and the observed collapse mode is recorded and compared with the Stage-1 "
  "prediction from the finite-strip signature curve. A test whose mode does not match the prediction is a finding, not a data point. Second, "
  "the AISI Direct Strength Method is the independent benchmark (ref. AISI S100-16, Appendix 1): each member test result is compared with "
  "DSM as well as with GMNIA, which gives a second check on both the test and the model.")
P("FlexInSheet tests in its own workshop and not in an accredited laboratory (ref. FLINS-CFS-001, Q7 answer). This is adequate for the "
  "validation and development tests in this plan, provided the load and displacement measurement is calibrated and documented (section 7). "
  "Where a result has to support a third-party approval, the relevant series is repeated or witnessed at an accredited body; those cases are "
  "marked in the matrix.")

# ------------------------------------------------------------------ 3
H(1, "Specimens, materials and measurements common to all series", new_page=True)
H(2, "T0: material and geometry")
P("Tensile coupons are cut from the flat part of each coil and thickness used in the programme, three per coil, tested to EN ISO 6892-1:2019. "
  "The coating is removed and the core thickness measured before the test. The measured yield strength f_[y,obs] and core thickness t_[obs] "
  "are used (a) as input to the validation GMNIA runs and (b) to adjust the test results to the nominal values "
  "(ref. EN 1993-1-3:2006, A.6.2; AISI S100-16, K2.1.1). The steel is S350GD+Z to EN 10346:2015; the mill certificate is kept with the record.")
P("Every member specimen is measured before the test: web and flange out-of-flatness at five sections along the length with a straight edge and "
  "feeler gauges or a laser line, flange and lip angles, and overall bow and twist. The measured field is used to seed the validation model; "
  "where the measurement is coarse, the Schafer and Peköz distributions are used to bound it (local 0.34t and distortional 0.94t medians, "
  "1.35t and 3.44t at the 95 % level).")
H(2, "Instrumentation")
B("Load: hydraulic jack with a calibrated load cell, or dead weight (sand bags, water tanks) weighed to ±2 %. Dead weight is acceptable for "
  "the floor prototype and the long-span bending tests; the jack is preferred for crippling and joint tests because it gives displacement "
  "control past the peak.")
B("Displacement: dial gauges or LVDTs at the points shown on the figures, read at every load step; 0.01 mm resolution for joint slip, 0.1 mm "
  "for deflections. Support settlement is measured and subtracted.")
B("Lateral movement of the free bottom flange at mid-span (two transducers) in the bending tests, because this is the signature of the "
  "distortional mode that the GMNIA must reproduce.")
B("Photographs of each specimen before, at peak and after collapse, with a scale bar; a short video of the collapse where possible.")
B("Optional and cheap: a fixed camera with a speckle pattern on the web for digital image correlation of the local buckling pattern.")
H(2, "Loading protocol")
P("Load is applied in at least ten steps to the expected characteristic resistance, held for one minute at each step for the readings, then in "
  "smaller steps to the peak and beyond until the load has dropped by at least 20 % or the deformation makes the test unsafe. A preload of "
  "5 % of the expected peak removes the bedding-in. For the serviceability readings the specimen is unloaded and reloaded once "
  "(ref. EN 1993-1-3:2006, A.3.1 and A.4.2).")

# ------------------------------------------------------------------ 4 member tests
H(1, "Member tests for the GMNIA validation (Q7)", new_page=True)
H(2, "T1: joist bending")
P("A pair of joists at 600 mm spacing with the OSB deck screwed at 300 mm centres is tested in four-point bending (Figure 2). The pair with its "
  "deck is the real restraint condition of the floor: the top flange is restrained by the deck, the bottom flange is free, and the deck fasteners "
  "carry the lateral restraint force. A single joist in a restraint frame is the laboratory alternative (ref. AISI S911-17 for hat-shaped "
  "beams, the closest standard procedure; EN 1993-1-3:2006, A.3.4) but it idealises the restraint and is not needed for validation.")
P("The spans are chosen from the Stage-1 signature curve of each section so that each governing mode of the family is tested at least once: a "
  "span where distortional buckling of the compression flange and lip governs, a span where local buckling of the web governs, and the longest "
  "catalogue span where the deflection and vibration criteria govern and the strength margin is largest. For the placeholder family these are "
  "about 3.0, 4.2 and 5.4 m for the 200 mm and 250 mm sections.")
P("Bearing stiffeners and a 100 mm bearing length are used at the supports so that the test fails in bending and not in web crippling; web "
  "crippling has its own series. One configuration is repeated with the standard service web holes, because holes reduce the shear and "
  "crippling capacity and the campaign includes them (ref. AISI S100-16, G6; AISI S240-15, B2.2).")
FIG(F / "F2_joist_bending.png", "T1 joist bending: pair of joists with deck in four-point bending, bearing stiffeners at the supports")
P("Each test gives the peak moment, the moment-deflection curve including the post-peak branch, the lateral movement of the bottom flange and "
  "the collapse mode. The validation GMNIA run of the same specimen uses the measured f_[y,obs], t_[obs] and imperfection field, with the deck "
  "restraint modelled as discrete springs at the screw positions. Acceptance: peak within ±10 % and the same collapse mode; otherwise the "
  "model is corrected before the campaign runs.")
H(2, "T2: web crippling at the supports")
P("Web crippling at the supports is the governing check of most floor joists (ref. FLINS-CFS-001, Q8) and the one where the Eurocode and AISI "
  "formulae differ most (ref. EN 1993-1-3:2006, 6.1.7; AISI S100-16, G5). Two load cases occur in this floor (Figure 3): the joist end bearing on "
  "the bearer, which is the end-one-flange case (EOF), and the bearer bearing on the pile head with the joist loads coming from above, which is "
  "the interior-one-flange case (IOF) at an interior pile and EOF at an end pile. The test procedure follows AISI S909-17 and "
  "EN 1993-1-3:2006, A.5.2 (internal support test), with the bearing length of the real detail.")
P("Each joist case is tested without and with the bearing stiffener that AISI S240-15 prescribes (ref. B2.5), because the stiffener is a cost "
  "and the tables must say when it is needed. The bearer case is tested on the candidate bearer sections of series T3, so T2(b) and T3 share "
  "specimens.")
FIG(F / "F3_web_crippling.png", "T2 web crippling: (a) joist end on the bearer, EOF, unstiffened and stiffened; (b) bearer over the pile head, IOF")
P("The validation model of the crippling test is a short shell model with the measured imperfection; the model factor for this mode is "
  "derived separately from the bending mode, since EN 1993-1-14 asks for the factor per failure mode and the AISI web-crippling expression "
  "is itself empirical.")

# ------------------------------------------------------------------ 5 joints and bearers
H(1, "Bearer and joint tests (Q9)", new_page=True)
H(2, "T3: bearers under pile reactions")
P("The bearer carries the inverted force flow: distributed joist loads from above and concentrated pile reactions from below "
  "(ref. FLINS-CFS-001, Q1 answer). Three candidate families are tested in the IOF set-up of Figure 3(b): a back-to-back pair of the deepest "
  "C-section, a boxed pair, and a hot-rolled alternative (RHS or a shallow HEA). The bearer length is three pile spacings with the outer "
  "supports on soft springs that represent the adjacent piles, so that the moment and the concentrated reaction at the central pile occur "
  "together as in the floor. Results: moment-crippling interaction at the pile, the required head-plate size, and whether a web stiffener or "
  "a hot-rolled insert is needed. The hot-rolled candidate is verified by calculation to EN 1993-1-1 and is tested once for the detail only.")
H(2, "T4: joist-to-rim and joist-to-bearer joints")
P("The joist end connection is tested in vertical shear with the rim track fixed to a rigid frame and the joist stub loaded near the joint "
  "(Figure 4). The procedure follows AISI S914-15 (joist connectors attached to cold-formed steel framing) with the evaluation of "
  "EN 1993-1-3:2006, A.6. Three details are tested: the clip angle, the bent tab, and the swaged (coped) end, each with the screw pattern "
  "proposed for production. The slip at service load is recorded because it enters the floor stiffness and vibration.")
P("Screw lap-shear coupons give the per-screw bearing and tilting resistance for the thickness combinations of the family "
  "(ref. AISI S905-17; EN 1993-1-3:2006, 8.3 and A.6). If the screw supplier holds a European Technical Assessment for the screws in these "
  "thicknesses (ref. EAD 330046-01-0602), the coupon series is reduced to a confirmation of five tests per combination.")
FIG(F / "F4_joist_rim_joint.png", "T4 joist-to-rim joint shear test and screw lap-shear coupon")
H(2, "T5: bearer-to-pile-head joint")
P("The pile-head joint is the only non-standard joint of the system and the one with the least guidance in the sources. It is tested in four "
  "ways on a pile shaft stub fixed to the rig (Figure 5): compression through the head plate, uplift through the bolts, horizontal shear, and "
  "compression with the bearer placed off-centre by the installation tolerance. The tolerance is itself a test parameter: the geotechnical "
  "partner states the achievable positional and level tolerance of the piles, and the joint is tested at that eccentricity "
  "(ref. the ±1° setting accuracy of the manufacturer's guide quoted in the STEELXPERT overview, with no positional tolerance given).")
P("The test results calibrate a finite element model of the detail, which is then used to size the head plate, the slotted holes and the "
  "stiffener for the whole catalogue of bearers and pile types, rather than testing every combination.")
FIG(F / "F5_pile_head_joint.png", "T5 pile-head joint: compression, uplift, horizontal shear and eccentric compression")

# ------------------------------------------------------------------ 6 system
H(1, "Floor system prototype (T6)", new_page=True)
P("A two-bay floor of at least four joist spacings width, with rim track, bearers on pile stubs or rigid posts and the OSB deck, is built as "
  "it would be on site (Figure 6). It is tested in three stages on the same specimen. Stage 1, serviceability: 1 kN point load deflection, "
  "heel-drop and walking excitation for the natural frequency and damping, with accelerometers at mid-bay "
  "(ref. SCI P354; ISO 18324:2016 for the floor vibration test method; EN 1993-1-3:2006, A.6.5). Stage 2, strength: uniform load by sand bags "
  "or water tanks in steps to 1.0, 1.35 and 1.5 times (g + q), held, with deflections and support settlements recorded "
  "(ref. EN 1993-1-3:2006, A.4.2 acceptance and strength test; AISI S100-16, K2.2). Stage 3, prototype failure: load increased to collapse, "
  "which shows whether the system fails in the member mode predicted from T1 and T2 or at a joint (ref. EN 1993-1-3:2006, A.4.3).")
P("If the product goes to a prefabricated cassette (ref. FLINS-CFS-001, Q2), a lifting test of the cassette at the designated lifting points "
  "is added to Stage 1, because transport and lifting often exceed the in-service demand (ref. SCI P402, section 3.3.3).")
FIG(F / "F6_floor_system.png", "T6 floor prototype: serviceability, strength and prototype failure stages on one specimen")
P("The diaphragm (in-plane shear) capacity of the deck, needed for the lateral stability of the house, is not in this plan. It is a "
  "standard cantilever diaphragm test (ref. AISI S907-17; ASTM E455) and is added when the wall system is defined.")

# ------------------------------------------------------------------ 7 matrix
H(1, "Test matrix and phasing", new_page=True)
P("Table 1 lists the series with placeholder counts for the catalogue of the development repository (seven C-sections, two spacings). The "
  "minimum of three replicates per configuration follows AISI S100-16, K2.1.1; EN 1993-1-3:2006, A.6.3.3 allows a characteristic value from "
  "fewer tests with a larger reduction, which is used only for the hot-rolled bearer. Where the spread between replicates exceeds 15 % of "
  "the mean, a further three are tested (ref. AISI S100-16, K2.1.1).")
rows = [["T0", "Tensile coupons", "each coil and thickness, 3 each", "15", "1", "workshop"],
        ["T0", "Imperfection survey", "every member specimen", "all", "1", "workshop"],
        ["T1", "Joist bending, pair with deck", "2 sections × 3 spans × 3", "18", "1", "workshop"],
        ["T1h", "Joist bending with web holes", "1 section × 1 span × 3", "3", "1", "workshop"],
        ["T2a", "Web crippling, joist on bearer (EOF)", "2 sections × 2 (stiffened/not) × 3", "12", "1", "workshop"],
        ["T2b/T3", "Bearer over pile head (IOF), bearer candidates", "3 bearer types × 3", "9", "2", "workshop"],
        ["T4", "Joist-to-rim joint shear", "3 details × 3", "9", "2", "workshop"],
        ["T4s", "Screw lap-shear coupons", "3 thickness pairs × 5", "15", "2", "workshop, or supplier ETA"],
        ["T5", "Pile-head joint", "4 load cases × 3", "12", "2", "workshop with geotechnical partner"],
        ["T6", "Floor prototype, three stages", "1 or 2 specimens", "1–2", "3", "workshop; witnessed for approval"],
        ["T7", "Deck diaphragm (later)", "per AISI S907 / ASTM E455", "–", "later", "accredited laboratory"]]
T("Test matrix (placeholder counts for the development catalogue)", ["Series", "What", "Configurations × replicates", "No.", "Phase", "Where"], rows, [1.3, 4.6, 4.6, 1.0, 1.1, 3.9])
P("Phase 1 (T0, T1, T2a) is the validation of the campaign and comes first, because the span tables cannot be published without it. Phase 2 "
  "(T3, T4, T5) runs in parallel with the campaign once the bearer and joint details are drawn. Phase 3 (T6) closes the development and "
  "is the test to witness for a third-party approval. The total is about 95 specimens, of which about 60 are small coupons and joint "
  "stubs that take under an hour each; the bending and prototype tests are the schedule drivers.")

# ------------------------------------------------------------------ 8 evaluation
H(1, "Evaluation of the results", new_page=True)
H(2, "Member tests to the model factor")
P("For each T1 and T2 specimen the validation GMNIA is run with the measured properties. The ratio R_[test] / R_[GMNIA] over the series gives the "
  "mean and the coefficient of variation of the model; the model factor γ_[FE] is derived from them following EN 1993-1-14:2025, Annex A, "
  "with the statistical procedure of EN 1990:2002, Annex D.8 (resistance model with a known coefficient of variation). A result in the "
  "expected range is γ_[FE] between 1.0 and 1.15. The design resistance in the span tables is then "
  "R_[d] = R_[GMNIA,nominal] / (γ_[FE] · γ_[M1]), where the nominal GMNIA uses nominal f_[y], nominal t and the Eurocode equivalent "
  "imperfections, as already implemented in the campaign module of the repository.")
P("The same test results are compared with DSM (ref. AISI S100-16, Appendix 1) and with the hand calculation to EN 1993-1-3:2006, "
  "sections 6.1.4 and 6.1.7. The three-way comparison (test, GMNIA, code) is reported per specimen in the run log.")
H(2, "Joint and bearer tests to design resistances")
P("Test results are first adjusted to the nominal material and thickness (ref. EN 1993-1-3:2006, A.6.2). The characteristic value of a "
  "configuration is the mean minus k times the standard deviation, with k from A.6.3 for the number of tests, and the design value follows "
  "from γ_[M] of A.6.4. For a family of tests covering a range (for example the screw coupons over several thicknesses) the family "
  "procedure of A.6.3.2 is used so that one resistance expression covers the range. The AISI route (ref. S100-16, K2.1.1, resistance "
  "factor from the test statistics) is run in parallel on the same data, as the client intends to use both standards.")
H(2, "Serviceability data")
P("Joint slip at service load, bearer and support stiffness and the measured floor frequency and damping are collected into the stiffness "
  "parameters of the layout tool: the span tables carry a vibration column, and the T6 result confirms or corrects the 8 Hz criterion "
  "adopted in the design basis (ref. FLINS-CFS-001, Q4).")
H(2, "Records")
P("Each specimen gets a one-page record: identification, measured properties and imperfections, set-up photograph, load-displacement curve, "
  "peak, collapse mode and the comparison with the prediction. The records and the run logs of the validation models are kept together with "
  "the campaign results in the project folder, so that the tables are traceable to the tests that support them.")

# ------------------------------------------------------------------ 9 references
H(1, "Standards and references", new_page=True)
refs = [["EN 1990:2002", "Annex D: design assisted by testing (D.4 planning, D.7 single property, D.8 resistance models)"],
        ["EN 1993-1-3:2006", "6.1.4 bending, 6.1.7 local transverse forces, 8.3 self-tapping screws, section 9 design assisted by testing, Annex A testing procedures (A.3, A.4, A.5, A.6)"],
        ["EN 1993-1-14:2025", "Design assisted by finite element analysis: section 7 validation and verification, Annex A model factor"],
        ["EN 1993-1-1:2005", "Hot-rolled bearer alternative"],
        ["EN ISO 6892-1:2019", "Tensile testing of metallic materials"],
        ["EN 10346:2015", "Continuously hot-dip coated steel; S350GD+Z"],
        ["EAD 330046-01-0602", "Fastening screws for metal members and sheeting (basis of screw ETAs)"],
        ["AISI S100-16", "Chapter G (G5 web crippling, G6 with holes), Chapter K (K2.1 tests for determining structural performance, K2.2 confirming tests), Appendix 1 (DSM)"],
        ["AISI S240-15", "B2 floor framing, B2.5 bearing stiffeners, B1.5 connections"],
        ["AISI S905-17", "Test methods for mechanically fastened cold-formed steel connections"],
        ["AISI S907-17 / ASTM E455", "Cantilever test method for diaphragms (later phase)"],
        ["AISI S909-17", "Web crippling test method"],
        ["AISI S911-17", "Flexural testing of cold-formed steel hat-shaped beams (closest procedure for the joist bending test)"],
        ["AISI S914-15", "Test standard for joist connectors attached to cold-formed steel framing"],
        ["SCI P354; ISO 18324:2016", "Floor vibration design and test method"],
        ["SCI P402 (2015)", "Light steel framing in residential construction; 3.3.3 lifting and transport"],
        ["Schafer and Peköz (1998)", "Imperfection distributions for cold-formed steel members"]]
T("Standards and references cited", ["Reference", "Used for"], refs, [4.0, 12.5])
P("Clause numbers are to be verified against the editions held in the indexed standards library before issue; the 2024 second-generation "
  "edition of EN 1993-1-3 renumbers the clauses above and is to be adopted once the Hungarian National Annex to it is published.")
N.signature()
print("saved", A.out, "pending:", N.save(A.out))
