# Assessment: can the AI run the C / U member checks of the pilot house itself, from EN 1993-1-3?

FLIN-008, 2026-11-12. Owner question (item 0): investigate thoroughly whether all C and U profiles
of the house can be checked "by you", on the equations, expressions and methods of the attached
Eurocode (EN 1993-1-3, read from the owner's licensed PDF; EN 1993-1-5 §4.4 and EN 1993-1-1 §6.3
where 1-3 refers to them). Assessment only; nothing in it is a design value (D-007). Evidence:
`ec3_1_3_proto.py` (prototype), `qa_run.py` + `cufsm_qa.py` (QA), `QA_REPORT.md` (output).

## 1. Verdict

**Yes for the single C and U members, with conditions; not alone for the built-up, boxed and
perforated members, and never as the signing engineer.**

- The single lipped C (C150x45x10x1.5, C200x60x15x2.0 / 2.5) and plain U (U150x45x1.5,
  U150x40x2.0) members are fully inside the scope of "design by calculation" of EN 1993-1-3
  (§5.2 Table 5.1, §5.5, §6.1, §6.2). Every check the house needs for them - effective section
  in compression and bending, distortional stiffener reduction, shear, web crippling, flexural /
  torsional-flexural / lateral-torsional buckling, N+M interaction, SLS stiffness - is a closed
  procedure that a script reproduces exactly. The prototype does this today for compression and
  major-axis bending and passed the QA (section 3).
- Where the standard gives no rule, the AI cannot invent one: back-to-back pairs (frames, posts,
  trimmers), boxed C+U and C+C build-ups (jambs, headers, girt, rims, ridge box), the perforated
  stud and purlin webs (38 x 100 slots at 600), the asymmetric track. These need owner
  assumptions first (section 4). With the assumptions written down they are computable too.
- D-006 (the AI stays outside the structural load path) is the owner's decision and is not
  changed by this memo. What the prototype shows is that the member checks can be **scripted
  and audited**: open Python, every number traceable to a clause, three independent cross-checks
  (FE section model, finite strip, a second design method), and the owner checking and signing.
  That is a different thing from "the AI decides a resistance". If the owner wants this route,
  D-006 needs a sentence that distinguishes the two.

## 2. What EN 1993-1-3 asks for, member by member (house as in viewer v33)

| member | section | action | checks (clause) | by calculation? |
|---|---|---|---|---|
| wall studs A / C, gables, cripples | C150x1.5, perforated web | N + My (wind), bridging at 0.92 / 1.84 | 5.5 Aeff, Weff; 6.1.9 or 6.2.5 (6.36); 6.2.2-6.2.4 with Lz = LT = 0.92; 6.1.7 at the track; SLS 7.1 | yes; **perforation outside 1-3** (section 4) |
| king / jack / end posts, mullions, wind posts | C+U cap, 2 x C back to back | N + My | as studs; composite action? | with an assumption (section 4) |
| purlins, ridge-edge members, skylight cripples | C150x1.5, perforated | My (+ Mz on the slope) + N (diaphragm) | 6.1.4 both axes, 6.1.7 (6.7a), 6.2.4 LTB with L = bridging spacing; 6.1.11 M + F | yes; biaxial Weff,z to add; perforation as above |
| tracks: wall top / bottom, raking, head / sill, cap tracks | U150x1.5, U150x40x2.0 | bending (raking tracks carry end roof panels), bearing of stud ends | 5.5.2 outstand flanges (Table 4.2), 6.1.4, 6.1.7.2 unstiffened flanges (6.15b-e) | yes |
| asymmetric track (purlin ends) | new section | bending + bearing | 5.5, 6.1; buckling curve by analogy 6.2.2(2) | yes, geometry needed |
| headers, girts (door, windows, gable / wall C girt) | U + 2 x C lying + U | My, deflection L/350 | 5.5 on each C (web b/t 100 in compression), 6.1.4, 6.2.4 | with an assumption on the box |
| loft joists, trimmers, header joist | C150x1.5 (holes to be decided) | My, floor vibration | 6.1.4, 6.1.7, 7.1, vibration (FLINS-CFS-005) | yes |
| floor panels: joists, rims, end tracks | C150x1.5, boxed C rims, U150 | My, bearing on bearers | as above | yes / assumption for the boxed rim |
| cross bearers | 2 x C200x60x15x2.5 b-t-b, 6 mm gap | My continuous, 2 spans, F at the T gussets | 6.1.4, 6.1.7 (web crippling at 3 screws governs), 6.1.11, 6.2.4 (gap, packers) | with an assumption on the pair |
| frame columns and rafters | 2 x C200x2.0 b-t-b, 26 mm gap + U150x40x2.0 both edges | N + My, knee / apex | 6.2.5 on the pair; the U tracks as part of the section or not | with an assumption on the pair |
| straps, tie rod, hold-downs | flats, rod | tension | 6.1.2, EN 1993-1-8 | yes (not 1-3 members) |

## 3. Prototype and QA - what was tested and what it found

Prototype (`ec3_1_3_proto.py`, about 600 lines): Annex C section constants on the rounded
midline; notional flat widths per Fig. 5.1; EN 1993-1-5 Tables 4.1 / 4.2 reductions; edge
stiffener per 5.5.3.2 with the spring stiffness (5.10b) and the χd iteration (5.16); Aeff, eN,
Ieff, Weff with the web ψ iteration (5.5.2(3)); Nc,Rd (6.2), Mc,Rd (6.4), Vb,Rd (6.8), Rw,Rd
(6.15a-e); Ncr,T / Ncr,TF (6.33-6.35), buckling curve b (Table 6.3), Mcr and χLT curve b
(6.2.4), interaction (6.36). Partial factors γM0 = γM1 = 1.0 per 2(3) (HU NA to confirm).

QA (`QA_REPORT.md`):

| test | reference | result |
|---|---|---|
| Q1 gross A, Iy, Iz, It, Iw, shear centre, 5 sections | sectionproperties (2D FE of the real rounded outline, independent library) | all within 0.5 %; shear centre exact |
| Q2 elastic local buckling | CUFSM finite strip (pycufsm) | EN plate formula (kσ = 4, 1-5 Table 4.1) is 33-40 % below the finite strip for the C's, 3 % for the U: the closed form is conservative, as expected (no flange restraint credited) |
| Q2 elastic distortional, bending | CUFSM | σcr,s of (5.15) is 36-47 % below the finite-strip distortional minimum: conservative |
| Q2 elastic distortional, compression | CUFSM | **no distinct distortional minimum exists** for these narrow-flange, short-lip sections; the signature curve runs from the local minimum straight into the global branch. The 5.5.3.2 model still produces χd = 0.60 / 0.67 / 0.75 (C150 / C200x2.0 / C200x2.5). A cFSM modal decomposition would be needed to use 5.5.3.1(8) instead; not done |
| Q3 formula layer | hand values (χ curves, ρ, kσ, χd, plate stress) | 10 / 10 pass |
| Q4 consistency | limits, monotonicity, physical floors | pass after the fixes below |
| Q5 whole-member resistance | AISI S100 Direct Strength Method with the CUFSM inputs (a different design method) | Pn / Nb,Rd = 0.99, 1.02, 1.05, 1.16 for the four stud / column cases: inside the ±20 % band |
| external benchmark | Access Steel SX023a (Aeff = 436.8 mm², χd = 0.744 per the SCIA benchmark page) | **not run**: the hosts are outside the cloud network policy; the owner's Drive holds only the flowchart SF038a. To do locally (section 5) |

Defects the QA found in the first version of the prototype, all fixed and re-run:

1. Shear centre 37 % off (Q1). The Annex C sectorial formulas give the shear centre relative to
   the pole, not to the gravity centre as first coded. Found only because an independent FE
   model was in the loop. Ncr,TF and every stud buckling number depended on it.
2. Corner areas missing from Aeff and Ieff (Q4 stocky-section test). Notional widths were
   measured to the corner midpoints (Fig. 5.1) but the corner arcs were then left out of the sum:
   Aeff of the C150 was 7.7 % low. The effective section is now assembled on the rounded midline
   with the corners fully effective (5.1(1), (5)).
3. No guard for a vanishing lip. For thick fictitious sections the lipped C came out weaker than
   the plain U; 5.2(2) (ignore the lip if c/b < 0.2) and a width guard now apply. For the FLINS
   C150x45x10 the lip is at c/b = 0.22, two hundredths above the limit where the standard says
   to ignore it; worth confirming the real lip length with FLINS.
4. Tooling: pycufsm's compiled solver is incompatible with numpy 2; a shimmed copy of its
   pure-Python solver is used for the QA only.

Reading of these for the owner: a one-pass "AI calculation" would have shipped defects 1 and 2.
A scripted calculation with independent cross-checks in the loop caught them in the same
session. The method is only as good as the QA that surrounds it.

## 4. Where the standard stops - owner assumptions needed before the script can run

1. **Perforated webs** (studs, purlins: 38 x 100 slots at 600, first slot 300 from the end, none
   within 250 of an end). EN 1993-1-3 has no rule for web holes; §9 / Annex A would send them to
   testing. AISI S100 does have calculation rules (effective width of webs with holes, web
   crippling reduction, shear at the hole). Proposal: cite AISI S100 as the supplementary
   method with its applicability limits (depth of hole / web ≤ 0.5, hole length ≤ 114 mm,
   clear distance between holes ≥ 457 mm, end distance ≥ 254 mm [MEMORY, verify in AISI S100
   before use]). The 250 mm end distance of the brief is 4 mm short of that limit; make it 260.
2. **Back-to-back pairs** (frames 2 x C200 with 26 mm gap + packing, bearers 6 mm gap, posts,
   trimmers). 1-3 is silent on the composite member; EN 1993-1-1 §6.4 covers built-up
   compression members with battens / packing (interconnection spacing ≤ 15 i_min to treat as one
   member, Table 6.9 [verify]); AISI S100 uses a modified slenderness. Owner to choose: (a)
   each C alone with half the force (lower bound), or (b) integral section with 1-1 §6.4 limits
   on the packer spacing, which then becomes a drawing requirement.
3. **Boxed build-ups** (C in U cap, two C toes facing, U + 2 C + U headers / girt). Closed only
   if the screw lines transfer the shear flow; otherwise two open sections sharing the load with
   the cap as lateral restraint. Proposal: (a) as lower bound; the cap track counted as full
   lateral restraint of the free lips (LT and distortional) only where the screw spacing is given.
4. **Restraint assumptions**: bridging rows (40 mm straps both faces + end blocks) as lateral and
   torsional restraint of studs and purlins -> Lz = LT = 0.92 m; purlin LTB length = half the bay
   (one bridging row). Orientation number: the C150 purlin unrestrained over 3.0 m has
   Mb,Rd ≈ 1.3 kNm against the brief's estimated 1.35 kNm (1.2 kN/m), restrained at mid-bay it
   is about 3 kNm. The sheathing is never counted (D-016 rule 3), so these rows are structural.
5. **Load position** at the eave (eccentric bearing of the roof panel on the inner track edge)
   and at the purlin ends (web crippling with ss = track flange = 45 mm: Rw,Rd ≈ 5.8 kN at a
   free end, 10.4 kN interior for the C150, PRELIMINARY): matches the viewer's "about 4 kN,
   near the limit" note; cleats will be needed at some purlin ends (6.1.7.1(3)).
6. **Material**: S350GD assumed (fyb = 350, fu = 420 per EN 10346 [verify]); fya per 3.2.2 not
   used (sections are not fully effective). Internal radius r = 1.5 t assumed - FLINS tooling
   value needed; it enters 5.1 and 6.1.7 (k2, k5).
7. **Edition**: the Drive PDF is EN 1993-1-3:2006 (E) without AC:2009 and A1:2009. The
   consolidated MSZ EN 1993-1-3:2007 + A1:2010 text must be the citation basis before anything
   is signed; the web-crippling and some table entries were touched by the corrigendum [verify].
8. **HU NA**: γM0, γM1, γM2 and the NA choices of 1-3 and 1-5 from the owner's standards library
   (`_na`), not from the recommended values used here.

## 5. If the owner chooses this route - what it takes

- Complete the module: Mz and biaxial Weff (purlins on the slope), U in bending about z,
  6.1.11 M + F, 7.1 SLS stiffness (Ific), 6.1.10, the built-up / boxed options of section 4 as
  switchable assumptions, the AISI hole rules, HU NA values, a member table reader for the
  AxisVM / global model forces, a results table writer for the Hungarian annex. About 20 h.
- Validation before first use: Access Steel SX023a / SX022a benchmarks run locally (the
  hosts are blocked from the cloud; the owner fetches the two PDFs into the standards library),
  one section cross-checked in Consteel or in ANSYS if a licence is at hand, the QA suite kept
  green under pytest. About 6 h. Validation is the owner's check, not the AI's.
- Running the checks for lines 5a-5h then costs about 0.3 h per member group instead of
  about 1 h by hand: the 58 h of lines 5a-5h in WORK_BREAKDOWN rev 0 become roughly 40 h, so
  the job total stays about the same (163 h) in this first use. The module is then an asset
  for the FLINS span tables and the later programme (D-007, D-012).
- Hours for item 1 (O-014) are proposed in this form only; the price is the owner's (O-010).

## 6. Recommendation (for the owner's decision, item 1)

Use AxisVM for actions and the global model as planned (line 4). For lines 5a-5h the scripted
EN 1993-1-3 route is feasible for every single C and U member and already QA'd at prototype
level; the built-up, boxed and perforated members need the assumptions of section 4 first,
and the owner remains the checker and signatory. If the owner prefers a licensed member-check
program (Consteel) for the signature, the prototype still earns its place as the independent
cross-check of that program's results, which no second commercial licence gives as cheaply.
