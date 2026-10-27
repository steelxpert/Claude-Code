#!/usr/bin/env python3
"""Build FLINS-CFS-004: fire and acoustic performance, research note."""
from __future__ import annotations
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import sxnote

ap = argparse.ArgumentParser()
ap.add_argument("--common", required=True); ap.add_argument("--signature", required=True); ap.add_argument("--out", required=True)
ap.add_argument("--projno", default="2026.032a"); ap.add_argument("--rev", default="rev0"); ap.add_argument("--final", action="store_true")
A = ap.parse_args()
PROJECT = "FlexInSheet cold-formed steel floor framing system on screw piles: product development"
DOCID = f"STEELXPERT {A.projno} — FLINS-CFS-004 {A.rev}"
TITLE = "Fire and acoustic performance of the floor system"
SUBTITLE = "Research note: Hungarian requirements, what governs a cold-formed steel joist floor, routes to compliance, and what remains to be verified"
N = sxnote.Note(A.common, A.signature, A.projno, DOCID, PROJECT, "27 October 2026", "27.10.2026", (2026, 10, 27), A.rev,
                title=TITLE, subject=SUBTITLE, keywords="fire resistance, OTSZ, EN 13501-2, EN 1365-2, acoustics, MSZ 15601-1, light steel framing", final=A.final)
H, P, B, T = N.H, N.P, N.B, N.table
N.cover(TITLE, SUBTITLE, [("Project:", PROJECT), ("Client:", "FlexInSheet Kft. (FLINS)\n2400 Dunaújváros, Előd utca 4."),
    ("Subject:", "Answers risk item 5 of the feasibility note: fire and acoustic performance are test-based and must be settled before the analysis work"),
    ("Status:", "Desk research from published summaries and standing knowledge. Source documents could not be downloaded from the development environment; every value carries a verification flag (section 7)."),
    ("Engineer:", "STEELXPERT Kft.\nCsaba Bán, MSc civil engineer (T-T/01-18387)"),
    ("Related:", f"STEELXPERT {A.projno} — FLINS-CFS-001 rev0 (Q&A); FLINS-CFS-002 rev0 (test plan)"), ("Document:", DOCID), ("Date:", "27 October 2026")],
    [[A.rev, "First issue for discussion", "27.10.2026", "Cs. Bán", "–"]])
N.toc()

H(1, "Purpose and conclusion first", new_page=True)
P("Fire resistance and sound insulation of a light steel floor cannot be calculated into existence; both are properties of a tested build-up. "
  "This note collects what the Hungarian rules require, what the research says governs the behaviour, which routes lead to a compliant "
  "product, and what is still to be verified from the source documents. It answers the comment on risk item 5 of the feasibility note.")
P("Conclusion. For a single-family house the fire requirement on the floor is low and is met by a standard plasterboard ceiling; for a "
  "multi-unit house the separating floor needs a tested 60-minute build-up and the acoustic build-up of MSZ 15601-1, and the two "
  "requirements are met by the same elements: two layers of board on resilient bars, mineral wool in the cavity, mass on the deck. The "
  "product therefore needs two build-ups, not a family of them. The recommended route is to adopt a gypsum-board manufacturer's classified "
  "light steel floor system for the 30-minute case and to commission one EN 1365-2 test at ÉMI for the 60-minute separating floor, "
  "with a fire expert engaged by FlexInSheet from the start, as proposed in the comment. The Lindab purlin paper mentioned in the comment "
  "was not found online; a copy is requested (section 4.3).")

H(1, "Hungarian fire requirements", new_page=True)
P("The fire code is the Országos Tűzvédelmi Szabályzat, decree 54/2014. (XII. 5.) BM as amended, most recently by 8/2022. (IV. 14.) BM. "
  "The fire resistance required of load-bearing elements is set by the building's risk class (NAK, AK, KK, MK) and its number of storeys, "
  "in table 1 of Annex 2 (ref. OTSZ 2. melléklet, 1. táblázat); roof floors have their own table. Fire resistance is classified to "
  "MSZ EN 13501-2 from tests to MSZ EN 1363-1 and, for floors, MSZ EN 1365-2; the R, E and I criteria and the minutes (15, 30, 45, 60, 90) "
  "are the familiar European ones. Ratings of adjacent or stacked elements cannot be added.")
P("The exact table values for a residential floor were not retrievable from the search results and must be read from the consolidated text "
  "(njt.hu or Jogtár). From standing knowledge of the table, and to be confirmed: a detached house of one or two storeys falls in NAK and "
  "its floors are in the R 15 to REI 30 range; a multi-unit house with several dwellings on top of each other is AK or KK and its "
  "dwelling-separating floors are REI 30 to REI 60. The cellar relaxation of 16. § (3) does not apply to residential buildings.")
P("Two points are specific to this product. First, the ground floor over the screw piles is a floor over an open or skirted crawl space, "
  "not a floor over a cellar; the code does not set a separate case for it, so it is treated as the lowest floor of the building, with "
  "the underside exposed to whatever the crawl space contains. A ventilated crawl space with no stored material is a low fire load, but "
  "an enclosed skirt with services and insulation is a cavity and should be detailed as one (no combustible lining, cavity barriers at "
  "the perimeter). Second, the steel bearer and the pile head are part of the load path and must carry the same rating as the floor; a "
  "bare steel bearer in an open crawl space is unprotected steel.")

H(1, "What governs the fire resistance of a cold-formed steel joist floor", new_page=True)
P("Thin cold-formed sections heat quickly and lose strength early. EN 1993-1-2 limits class 4 sections to a critical temperature of 350 °C, "
  "a limit the research consistently finds conservative: fire tests and shell-element models of Z-purlins at the Czech Technical University "
  "(Schwarz, Slatinka, Jandera, ASFE 2015), sigma beams and columns at Coimbra, and a Polish two-span purlin study put the critical "
  "temperature at 400 to 450 °C, with catenary action giving further reserve after local buckling (Aalto, Lu and Mäkeläinen). Even so, "
  "an unprotected joist reaches 350 °C within a few minutes of a standard fire, so an unprotected cold-formed floor cannot be relied on "
  "for R 15 and every rating comes from the ceiling lining.")
P("The lining and its fixings govern. Gypsum board delays the temperature rise in the cavity; the rating ends when the board cracks and "
  "falls, which depends on the board type, the number of layers, the screw pattern and the staggering of joints. The rules of thumb in the "
  "British guidance (ref. SCI P402, section 2.2.2) are: 30 minutes with an 18 mm tongue-and-groove deck and one 12.5 mm fire-rated board "
  "below; 60 minutes with a second board layer with staggered joints. Industry sources extend this to 120 minutes with three thicker boards. "
  "These are guides for pre-design, not classifications.")
P("Two findings from the Queensland (Mahendran, Kesawan) full-scale floor tests change the detailing. Cavity insulation placed against the "
  "hot flange does not help and can shorten the rating, because it traps heat in the joist; insulation outside the lining, or composite "
  "board-and-insulation panels, perform better. And web holes and the joist depth matter less than the lining: the four tests with "
  "hollow-flange joists failed by joist buckling only after the lining had failed. Steel-sheet-laminated plasterboard systems reached 120 "
  "to 140 minutes in recent tests. For this product the lesson is to put the money into the board and its fixing, not into the steel.")
P("Fire from above is the other case for an upper floor: the deck (OSB, chipboard) is combustible and the E and I criteria are met by the "
  "deck plus a non-combustible layer (gypsum-fibre board or dry screed) where required. For the ground floor over the crawl space this case "
  "does not arise.")

H(1, "Routes to a compliant fire rating", new_page=True)
H(2, "Adopt a classified system")
P("Gypsum board manufacturers hold classification reports for light steel floor and ceiling systems: Knauf, Rigips (Saint-Gobain) and Siniat "
  "in Europe, Promat for mezzanine floors on steel joists. Most published reports are for timber joists or for suspended ceilings under a "
  "floor; the ones for load-bearing cold-formed steel joists are fewer and tied to a joist depth range and a fixing pattern. The first task "
  "is to collect the Hungarian subsidiaries' current classification reports for floors with C-joists of 150 mm and deeper, and to check "
  "whether the field of application (EN 15725 extended application) covers the FlexInSheet section, spacing and deck. Where it does, the "
  "30-minute and possibly the 60-minute floor need no new test.")
H(2, "Test the separating floor")
P("Where no report covers the build-up, one furnace test to MSZ EN 1365-2 of a loaded floor specimen at ÉMI gives the classification. One "
  "test covers one build-up and a defined range of joist depths and spans by the direct field of application; the specimen is a full floor "
  "of about 4 by 3 m under the design load. The cost is of the order of a car, the lead time months; it is to be planned early and done "
  "once, on the final build-up.")
H(2, "The Lindab paper and the fire expert")
P("The Lindab paper on fire resistance of cold-formed purlins mentioned in the comment was not found online. The search returned a 2011 "
  "BME fire-resistance report on Lindab Coverline high-profile sheeting and the ÉMI certificate A-313-2006 for Lindab Construline Z and C "
  "sections; neither is the purlin paper. A copy is requested; if it reports unprotected purlin tests against the 350 °C limit, it supports "
  "the bearer design in an open crawl space. Engaging a fire expert, as the comment proposes, is agreed: the expert writes the fire concept "
  "of the product (risk classes covered, required ratings, build-ups, cavity rules, pile-head protection) and represents it to ÉMI.")

H(1, "Acoustics", new_page=True)
P("The Hungarian requirements for sound insulation inside buildings are in MSZ 15601-1 (2007 edition). For a floor between two dwellings "
  "the manufacturers' technical sheets consistently quote R'_[w] + C ≥ 51 dB airborne and L'_[n,w] ≤ 55 dB impact; these are to be confirmed "
  "from the standard, including whether the C or C_[tr] term applies. Inside one dwelling, and for a detached house, there is no mandatory "
  "value; the floor is a comfort question. The ground floor over the crawl space has no acoustic requirement at all.")
P("British data for light steel joist floors show what the build-up has to be. The SCI acoustic guidance gives, for a C-joist floor with "
  "the ceiling on resilient bars (two layers of 15 mm sound-resistant plasterboard or two of 10 mm gypsum-fibre board, 100 mm mineral "
  "wool in the cavity, a deck with a floating layer on top), expected D_[nT,w] + C_[tr] of 47 to 58 dB airborne and L'_[nT,w] of 39 to 60 dB "
  "impact, the spread depending on the floating layer and the mass. The UK new-build requirement is 45 dB and 62 dB. These are expected "
  "values from the SCI technical sheets (P320 to P322), not measurements of a FlexInSheet floor. Overall depth is 250 to 380 mm.")
P("The acoustic lesson is the same as the fire one: mass and decoupling. A light steel floor meets the separating-floor values only with a "
  "heavy top layer (gypsum-fibre board, dry screed or a thin wet screed on a resilient layer) and a decoupled ceiling. Both are the same "
  "elements that give the 60-minute fire rating, so the separating-floor build-up is one product. Flanking through the light steel walls "
  "is the usual reason site measurements miss the laboratory values; the wall junction detail must be designed with the floor.")

H(1, "Other building-physics items for the ground floor on piles", new_page=True)
B("**Thermal.** A floor over open air is 'alsó zárófödém árkád felett' in the energy decree 7/2006. (V. 24.) TNM, with U ≤ 0.17 W/m²K; "
  "over a closed, unheated crawl space the fűtetlen pince value U ≤ 0.26 W/m²K applies. To be confirmed in the current text. The bearer and "
  "pile head are thermal bridges through the insulation line and need a thermal break at the head plate.")
B("**Moisture.** An open, ventilated crawl space dries the cavity but brings cold air under an insulated floor: the steel on the cold side "
  "must stay outside the vapour-tight layer, and summer condensation on cold steel is the risk a closed skirt brings. The American "
  "practice for pile foundations prefers an unvented, insulated perimeter with a ground vapour barrier; the Hungarian climate needs its own "
  "assessment by the building-physics designer.")
B("**Durability.** EN 1993-1-3 Annex B ties the coating to the exposure: Z275 is the standard for dry interiors; a joist cassette whose "
  "underside is open to a ventilated crawl space is a damp, unheated exposure and may need Z350 or an additional organic coat; the bearer "
  "and pile head in an open crawl space are external and are to be hot-dip galvanised to EN ISO 1461. The pile shaft is the geotechnical "
  "partner's item.")

H(1, "Verification list and sources", new_page=True)
T("Values to be verified against the source documents before the design basis is issued", ["Item", "Where", "Status"],
  [["Floor fire resistance by risk class and storeys", "OTSZ 2. melléklet, 1. táblázat (consolidated text)", "not retrieved"],
   ["Separating-floor acoustic values 51 dB / 55 dB", "MSZ 15601-1:2007", "quoted from manufacturers' sheets"],
   ["30 and 60 minute rules of thumb", "SCI P402, 2.2.2", "from the STEELXPERT overview"],
   ["LSF floor acoustic ranges", "SCI P320, P321, P322", "search summary"],
   ["Class 4 critical temperature research", "ASFE 2015 (CTU), Coimbra theses, Aalto papers", "search summaries"],
   ["Queensland LSF floor fire tests", "Kesawan and Mahendran, ASCE JSE 2015; SSRC 2014", "search summary"],
   ["U-values for floors over air and over crawl space", "7/2006. (V. 24.) TNM, current annex", "standing knowledge"],
   ["Coating class for the exposure", "EN 1993-1-3:2006, Annex B", "standing knowledge"],
   ["Lindab purlin fire paper", "copy from Csaba Bán", "not found online"]], [6.0, 7.0, 3.5])
T("Sources consulted", ["Source", "Content"],
  [["54/2014. (XII. 5.) BM, 8/2022. (IV. 14.) BM", "OTSZ: risk classes, Annex 2 fire-resistance tables"],
   ["MSZ EN 13501-2; MSZ EN 1363-1; MSZ EN 1365-2", "Classification and test standards for floors"],
   ["EN 1993-1-2:2005", "Class 4 critical temperature 350 °C"],
   ["Schwarz, Slatinka, Jandera, ASFE 2015", "Z-purlin fire behaviour, 350 °C limit conservative"],
   ["Kesawan, Mahendran, ASCE J. Struct. Eng. 2015; SSRC 2014", "Full-scale LSF floor fire tests, lining and insulation effects"],
   ["SCI P402 (2015); SCI P320–P322", "Fire rules of thumb; acoustic expected values for LSF floors"],
   ["MSZ 15601-1:2007", "Sound insulation requirements inside buildings"],
   ["Efectis report for Knauf (2010); Promat PXS-REI60; Siniat floor data", "Examples of classified ceiling and floor systems"],
   ["ÉMI publications (Geier, Parlagi Gáspárné)", "Hungarian practice for timber and light-frame structures in fire"]], [6.5, 10.0])
N.signature()
print("saved", A.out, "pending:", N.save(A.out))
