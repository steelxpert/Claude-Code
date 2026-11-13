# Reading list addendum - research sub-agent report, 2026-11-13 (FLIN-008)

Status: LEADS from search-engine snippets; nearly every primary host (JRC, SCIA help, Dlubal, Wiley,
iTeh, CFSEI, AISC cloud, core.ac.uk, consteelsoftware, newsteelconstruction, pdfcoffee / scribd
mirrors) is blocked from the cloud session. Only GitHub pages were fetched. Confidence: H = two
independent snippets or a fetched page; M = one snippet; L = inferred. Nothing below is read or
verified; the owner fetches, the next session verifies against the title pages.

## 1  EN 1993-1-3:2024 versus 2006 - what the snippets say

- Foreword "main changes" (CEN 2024-03; BS EN 1993-1-3:2006 withdrawn 2028-03-30): harmonisation of
  wording with EN 1993-1-1 / 1-5 / 1-8; nominal fu values (Table 5.1) aligned with 1-1 / product
  standards; sinusoidal sheeting (7.6.5); trapezoidal sheeting in axial compression (8.1.3);
  overlaps in sheeting; the stainless-fastener corrosion provisions deleted. **Inference (L):
  materials are now clause 5 and member resistance clause 8 - the 2006 numbering 3 / 5 / 6 used by
  the prototype shifts to 5 / 7 / 8 and must be re-mapped on landing.** Sources: iTeh catalogue
  page of EN 1993-1-3:2024; NBS publication index. Confidence H (list), L (renumbering).
- **No DSM equations, no new built-up-member rules, no hole rules found in the 2024 text.** A 2021
  Thin-Walled Structures paper on intermediate stiffeners in stainless CFS states that the
  effective width method "is the only design procedure used in the Eurocodes and no new approaches
  have been introduced in its current revision prEN 1993-1-3:2021". The built-up list and the
  "connections as close to the flanges as practicable" rule appear retained. The only DSM item is
  the amendment **EN 1993-1-3:2024/prA1:2026** (enquiry 2026-03 to 2026-05): a reference to a DSM
  publication in two notes and the bibliography, plus revised figures for openings in sheeting.
  Confidence H for "no DSM equations"; distortional, web crippling and buckling curves: nothing
  found either way, treat as unchanged until read.
- JRC (2020), *Overview of the evolution of EN 1993*, issue 1, 15.10.2020: about 90 technical
  amendments by SC3.WG3; Annex D improved and moved to a new Annex C; new materials in clause 5;
  bending + compression provisions of 8.2.5 changed; Annex E (purlins) removed *(verify)*; guidance
  on blind rivets and self-tapping screws added. Confidence M.
- Knobloch M., Bours A.-L. (2025), JRC online workshop 3-5 June 2025, section "Evolution of
  EN 1993-1-3" (host blocked; also on ResearchGate as the workshop proceedings). Confidence M.
- New Steel Construction (SCI / BCSA), "What's changing in the updated FprEN 1993" *(author, date
  verify)*: steel grade list expanded; sinusoidal sheeting; trapezoidal sheeting in compression;
  liner trays; "minor specifications and explanations added for the buckling design of sections in
  combined compression and bending". Confidence M.
- Ungermann D., Lemański P., Brune B. (2022). A new Eurocode-compliant design approach for
  cold-formed steel sections. *ce/papers* 5(4), 125-134, DOI 10.1002/cepa.1737 (open access;
  mirror d-nb.info/1268055441/34). Completes reading-list item 17. Confidence H.
- A **BS EN 1993-1-3:2024 TC (tracked changes)** edition exists (en-standard.eu): the cheapest
  clause-by-clause diff for the owner. Confidence H.

## 2  Access Steel SX022a / SX023a numbers (benchmark targets for `ec3_1_3_proto.py`)

- **SX022a (lipped channel in bending)**: inputs from an OCR copy: h = 200, b1 = 74 (compression
  flange), b2 = 66, c = 8.20 mm *(OCR; may be 20.2 - verify)*, r = 3, t = 2 (core about 1.96),
  fyb = 350, E = 210 000. Results per SCIA Benchmark 38: Aeff = 689.2 mm², Ieff,y about 4.14e6 mm⁴,
  Weff,com about 40 460 mm³, Weff,ten about 43 260 mm³, χd = 0.753; stiffener As = 103.3 mm²,
  Is = 3663 mm⁴, hw = 198 mm, be1 = 61.73 mm. SCIA notes the reference ignores a 1.47° principal
  axis rotation. Confidence M (inputs), H (results). Note: unequal flanges - the prototype needs the
  b1 ≠ b2 extension (kf = As2/As1) before this can be run.
- **SX023a (lipped channel in compression)**, Ungureanu / Ruff, checked Dubina. SCIA Benchmark 39:
  Aeff = 436.8 mm², χd,n = 0.744 (final iteration), be1 = 31.3 mm, be2,n = 32 mm, first-iteration
  σcr,s about 309 N/mm²; SCIA flags kf 0.97 used for both stiffeners where the lower one should be
  1.031. pdfcoffee mirror: Aeff = 436.7 mm², web ρ about 0.414. **Input dimensions not visible in
  any snippet** (verify on landing). Confidence H for Aeff / χd.
- **SX024a (wall stud in compression and bending)**, SCIA Benchmark 40: Weff,z,com = 1274 mm³,
  Weff,z,ten = 2585 mm³; Aeff values in the snippets inconsistent (118 vs 322 mm²) - verify.
  SCIA Benchmarks 38-41 are the Access Steel EN 1993-1-3 set. Confidence M.

## 3  Vendor verification examples (candidate benchmarks)

- SCIA Engineer Benchmarks 38-41 (EN 1993-1-3): reference and SCIA values side by side. H.
- Dlubal VE 9959 (RSECTION / SHAPE-THIN): C-section with edge stiffeners to DIN EN 1993-1-3:2010-12,
  ECCS TC7 "Example H": h = 102, b = 120, t = 2, r = 10, lip 26 mm, S355; Aeff compression 4.67 cm²
  (ECCS) vs 4.71 cm² (RSECTION), 0.86 %; eN,y 8.24 vs 5.13 mm; stated reason: distortional buckling
  handled only by the reduced stiffener thickness. H.
- Dlubal KB 001629 (C-section, Stahlbau-Kalender 2009 example, Aeff,stiffener 4.62 cm²) and
  KB 001628 (local transverse forces, clause 6.1.7, eq. 6.15a). M.
- ConSteel: Verification Manual 2020 (no CFS example visible); knowledge base "Secret formulas of
  EN 1993-1-3" parts 1-3 (Z-section stiffener spring stiffness, worked numbers). M.
- IDEA StatiCa: workflow articles only. CFSteel 4.1 Verification examples Vol. II (2018, cfsteel.ru):
  content not visible. ArcelorMittal Orange Book (effective properties to EN 1993-1-3:2006+AC, Z and
  Sigma visible). Bentley STAAD.Pro verification "AISI 2016 CS compressive strength" (lipped channel
  column, numbers in the help page). M.

## 4  Stud-to-track, bridging, load take-down (new items)

- Mishra S., McNally C., Wrzesien A.M., McCrum D.P. (2024). Experimental axial-compressive behaviour
  of bare cold-formed-steel studs with semirigid-track and ideal-hinged boundary conditions. *JCSR*
  216, 108600. 42 lipped channels, t 1.2-3 mm, h 75-125 mm; track end: strength x1.22, stiffness
  x0.7 vs hinged; recommends K = 0.65. H.
- Mishra S., McCrum D.P. (2024). Prediction of axial-compressive behaviour of bare CFS studs through
  a new stud-to-track contact modelling approach. *Engineering Structures* 318, 118757. "Hard contact
  significantly overestimated the axial stiffness by a factor of 3." H.
- Joorabchian A., Li Z., Peterman K.D. (2021, co-authors verify). Fixed-height CFS wall assemblies
  bearing on concrete slabs. *Thin-Walled Structures* 166, 107940 *(journal verify)*; follow-up
  Kapoor et al., SSRC 2023. M.
- LaBoube R.A., Bolte W. (2004). Behavior of curtain wall stud to track connections. *Thin-Walled
  Structures* 42(1) *(pages verify)*; track punch-through Pn = 0.6 t tw b Fu. M.
- Wang W., Roy K., Rezaeian H., Lim J.B.P. (2025). Axial load capacity of CFS studs featuring swaged
  sections. *Structures* *(volume verify)*; a 1.8 mm stud-to-track gap caused connection failure. M.
- Blum H.B., Zeinoddini V.M., Schafer B.W. (2015, authors verify). Flexural bracing requirements in
  axially loaded CFS-framed walls. *Practice Periodical on Structural Design and Construction* 20(4),
  DOI 10.1061/(ASCE)SC.1943-5576.0000242; 1.33x ideal stiffness proposed instead of 2x. M.
- Moen C.D. (2018). Bracing design for torsional buckling of CFS wall stud columns. *24th Int.
  Specialty Conf. on CFS Structures*, St. Louis (scholarsmine.mst.edu/isccss/24iccfss/session4/2). H.
- Schafer B.W. et al. (2020). Walls with discrete bridging plus sheathing, SSRC 2020 / CFSRC 2020:
  "methods do not exist for walls that rely on both." M.
- Selvaraj S., Madhavan M. (2019). Sheathing braced design of CFS members subjected to torsional
  buckling. *Structures* *(volume verify)*. M.
- CFSEI Tech Note, Design of CFS bridging and bridging anchorage (Steel Network reprint): 2 % brace
  force rule per AISI S211. M.
- Load take-down automation: no paper found; tools only (Tribby3D, openBrIM "Load Take Down",
  Tekla Structural Designer, SkyCiv); one journal item "Intelligent design concept of rural light
  steel frame structure based on BIM and genetic algorithm", *Int. J. Steel Structures* (2023,
  authors verify). Supports the conclusion that the owner's rule-table approach has no published
  precedent. M.

## 5  Open-source tools (fetched from GitHub where stated)

- pyCUFSM (ClearCalcs/pyCUFSM, fetched): LGPL-3.0, active, unconstrained + constrained FSM, template
  sections, Cython kernels, pytest; holes "planned"; no DSM helper. (Our gotcha 30: numpy-2 break.) H.
- CUFSM 5 (thinwalled/cufsm-git, fetched): MIT, MATLAB, v5.66 (29 Nov 2025 per JHU page). H.
- jmurgass99/coldformed (fetched): MIT, Python, single author, 0 stars; EN 1993-1-5 §4.4 effective
  width, EN 1993-1-3 §5.5.3 distortional for C / Z, AISI DSM, web crippling, perforations; tests +
  CI; no benchmark validation shown. H on facts, L on reliability - a possible second implementation
  to diff against, never a reference.
- vectorverse11/model_spm (fetched): no licence; EN 1993-1-5 §4.4 with hole removal and EN 1993-1-3
  §6.2.3 stub buckling for perforated rack uprights. H.
- steltic-cfs (PyPI 1.0.2, MIT, AISI S100 / S240 / S400 web app, openseespy). M.
  StructuresKit.jl (Julia, AISI S100-16). runtosolve AISIS100 (.NET). AISI only. M.
- sectionproperties: FE gross properties only (used in our QA Q1). H.
- Bronkhorst S.-J. (2017). An open-source implementation to predict buckling behaviour of
  cold-formed sections. MScEng thesis, Stellenbosch (supervisor G.C. van Rooyen); FSM + DSM. Code
  location verify. M.
- steelcalculator.pages.dev: "PRELIMINARY - NOT FOR CONSTRUCTION", formulas garbled; not a benchmark.
  OpenAEC open-fem2d-studio issue #4: EN 1993-1-3 effective-section engine proposed, not built. H.

## 6  Hosts to fetch locally

eurocodes.jrc.ec.europa.eu, help.scia.net (Benchmarks 38-41), dlubal.com (VE 9959, KB 001628/9),
onlinelibrary.wiley.com or d-nb.info (Ungermann 2022), cfsei.org (RP08-1), cloud.aisc.org (SSRC
papers), scholar.sun.ac.za (Bronkhorst), cfsteel.ru, consteelsoftware.com, newsteelconstruction.com,
pdfcoffee / idoc / vsip mirrors of SX022a-SX024a.
