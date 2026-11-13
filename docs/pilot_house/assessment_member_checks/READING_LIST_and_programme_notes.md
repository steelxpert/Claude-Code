# Reading list and programme notes - automated CFS house design (FLIN-008, owner replies 6)

Working document, English. Status of every reference: LEAD from a web search on 2026-11-13, not
read; bibliographic fields marked *verify on landing* were completed from memory or from catalogue
snippets. The owner fetches the PDFs into the standards library / papers folder, the next session
inventories them, verifies each against its own title page, then proposes the methodology plan.

## 0  What the owner asked (replies to the six-step programme)

- (a) envelope loads: agreed; later also CFD pressure point clouds mapped onto the envelope.
- (b) skeleton and load paths: think harder, look for ways to make it more straightforward.
- (c) member checks: ranked list of papers and best practice; owner fetches; AI reads; plan.
- (d) optimisation: agreed.
- (e) 3D model: check Inventor / SolidWorks export; are the formats public?
- (f) drawings / BOM: agreed, shop drawings separate.

## 1  (b) Skeleton and load paths - how to make it straightforward

What the search found: no published general "load-path generator" for light-frame houses. The
practice is (i) commercial assembly-level tools that design one wall / floor / roof assembly at a
time with the loads from above handed down (SteelSmart System: load-bearing wall module, multi-
storey load accumulation, lateral load generator per ASCE 7; ProtaStructure and LoadTakedown
automate tributary areas), and (ii) rule-based BIM prototypes for light-frame wood (FrameX,
boarding automation) where the rules are formalised trade know-how and the load paths are
*scripted beforehand*, not inferred. The caveat the literature repeats: geometry-only tributary
rules go wrong where the real stiffness decides the path (two-way action, diaphragms).

Proposal (the straight version), built on what already exists in the viewer:

1. **Member classes, not members.** Every member in the viewer has a role (stud, end stud, king,
   jack, purlin, ridge-edge, trimmer, joist, rim, bearer, column, rafter, girt C, track, strap).
   The load-path rules are written once per class, by the owner, as a short table: what it
   supports (tributary rule), what supports it (bearing rule), its span and restraint
   conditions (bridging rows, tracks), the actions it receives (G, Q, S, W by zone), the checks
   that apply. About 20 rows for this house.
2. **A support graph, not a FE model.** From the viewer geometry the script derives the directed
   graph "member A bears on member B at point P" (stud -> track -> rim/joist -> bearer -> screw;
   purlin -> rafter / raking track -> gable stud -> girt / track). Loads are pushed down the
   graph as reactions. This is the load take-down every hand calculation does, made explicit.
3. **Equilibrium closure as the QA.** At every level the sum of reactions equals the applied
   load on that level, and at the bottom the 15 screw reactions close against the total G + Q +
   S + W of the house (vertical and horizontal, per load case). A silent path error breaks the
   closure. This is the check the owner runs, one number per load case.
4. **Statics per member from span tables, not solvers.** Simply supported, two-span, cantilever
   and propped cases cover every member of this house; the tied-rafter frame is a closed-form
   case; strap fields are hand statics. The only member that may need a solver is the frame with
   semi-rigid knees (brief §4.1); a 2D plane-frame routine with its own QA covers that.
5. **Lateral system by hand rules too**: wind on a wall -> half to the roof diaphragm / girt,
   half to the floor; roof diaphragm -> end-bay roof diagonals -> braced wall bays; braced bay ->
   hold-down and shear in the straps; plan torsion from the eccentric bracing of wall C as an
   explicit check (brief §4.2).
6. **Envelope loads per member (a)** come from the same graph: each envelope member owns a set
   of envelope facets (panel grammar), each facet has its zone, cpe, cpi, snow shape
   coefficient; the member load is the area-weighted sum. The CFD extension is the same
   operation with a pressure field sampled on the facets instead of code zones; the code zones
   stay as the envelope and the CFD as a refinement with its own validation (D-006 unchanged).

Where this can fail and the owner must decide: members with two possible paths (a jack under a
girt and the stud beside it), stiffness-dependent sharing (boxed header and its cap track),
diaphragm action that the sheathing would give but which this house never counts (D-016 rule 3).
The rule table makes each of these an explicit choice, logged.

## 2  (c) Ranked reading list

Priority: 1 = read before the methodology plan; 2 = read before the module is extended; 3 =
background. "Use" says what is to be extracted.

### A. Built-up members (frames 2 x C200, bearers, posts, trimmers; boxed headers, jambs, rims)

1. [1] Roy K., Mohammadjani C., Lim J.B.P. (2019). Experimental and numerical investigation into
   the behaviour of face-to-face built-up cold-formed steel channel sections under compression.
   *Thin-Walled Structures* 134, 291-309. **Use:** the only result that compares EN 1993-1-3
   directly (conservative ~15 % overall, unconservative ~8 % for local-buckling failures);
   screw spacing effect; basis for the boxed-section assumption of memo §4.3.
2. [1] Ting T.C.H., Roy K., Lau H.H., Lim J.B.P. (2018). Effect of screw spacing on behavior of
   axially loaded back-to-back cold-formed steel built-up channel sections. *Advances in
   Structural Engineering* 21(3), 474-487. **Use:** modified-slenderness approach (AISI / AS-NZS)
   verified for back-to-back channels, 30 tests; unconservative ~10 % for stub columns; the rule
   for the 2 x C200 frames and posts.
3. [1] Fratamico D.C., Torabian S., Zhao X., Rasmussen K.J.R., Schafer B.W. (2018). Experiments on
   the global buckling and collapse of built-up cold-formed steel columns. *Journal of
   Constructional Steel Research* 144, 65-80 *(verify on landing)*. **Use:** composite action vs
   fastener layout, end fastener groups; what "integral member" requires on the drawing.
4. [1] A critical review of cold-formed built-up members: developments, challenges and future
   directions. *Journal of Building Engineering* (2023) *(authors verify on landing)*. **Use:**
   map of configurations (face-to-face, back-to-back gapped / non-gapped, closed), code
   discrepancies; the entry point before reading the rest.
5. [2] Lau H.H., Ting T.C.H. (2012 / 2013). Built-up box sections from two lipped channels joined at
   the flanges, stub and slender columns, screw spacing *(exact titles verify on landing)*.
   **Use:** EWM predicted better than DSM for boxes; capacity above the sum of the two channels;
   no North American rule for the configuration.
6. [2] Web crippling design of cold-formed steel built-up I-sections. *Engineering Structures*
   (2022) *(authors verify)*. **Use:** bearer and frame-base bearing on the T gussets.
7. [2] Design recommendation of cold-formed steel built-up sections under concentric and eccentric
   compression. *Journal of Constructional Steel Research* (2023) *(authors verify)*. **Use:**
   eccentric compression of the boxed posts under the girt.
8. [3] Test and design of cold-formed steel closed built-up beams (double sigma / triple lipped
   channel). *Thin-Walled Structures* (2023). **Use:** closed built-up beams in bending: the
   U + 2C + U headers and girt; AISI S100 gives no explicit rule.

### B. Perforated webs (studs, purlins: 38 x 100 slots at 600)

9. [1] Moen C.D., Schafer B.W. (2011). Direct Strength Method for design of cold-formed steel
   columns with holes. *Journal of Structural Engineering* ASCE 137(5), 559-570. **Use:** the
   method behind the AISI hole rules; net-section yielding; elastic buckling with holes.
10. [1] Moen C.D., Schafer B.W. (2009). Elastic buckling of thin plates with holes in compression
    or bending. *Thin-Walled Structures* 47(12), 1597-1607. **Use:** closed-form local buckling
    with holes, the piece that can be added to the prototype directly.
11. [2] Moen C.D. (2008). Direct strength design of cold-formed steel members with perforations.
    PhD thesis, Johns Hopkins University (AISI research report). **Use:** full derivation,
    beams with holes, limits (hole depth up to about 2/3 web depth validated).
12. [2] Stability of perforated cold-formed steel beam-columns (SSRC 2016 proceedings) and the
    Nottingham study proposing a strength reduction factor for perforated high-strength
    C-sections *(both verify)*. **Use:** where DSM with holes is scattered; the margin to keep.

### C. Stud ends, tracks, bridging (the house-specific checks)

13. [1] Fox S.R., Schuster R.M. (2000). Strength of wind load bearing wall stud-to-track
    connections. *15th International Specialty Conference on Cold-Formed Steel Structures*,
    St. Louis. And: Lewis, Fox, Schuster (2008). Strength of cold-formed steel jamb stud-to-track
    connections, AISI RP08-1 (University of Waterloo thesis). **Use:** stud web crippling at the
    track and track flange punch-through, gap between stud end and track web, missing screws;
    this is exactly the "about 4 kN near the limit" question of the purlin and stud ends.
14. [1] Green P.S., Sputo T., Urala V. (2006). Strength and stiffness of conventional bridging
    systems for cold-formed cee studs. *Journal of Structural Engineering* 132(4), 550-557.
    **Use:** what a bridging row must provide to count as the Lz = lT = 0.92 m restraint assumed
    in the stud sheet; brace force 1-2 % of N, stiffness twice the ideal.
15. [2] Blum H.B., Zeinoddini V., Schafer B.W. (2013). Bracing for flexural buckling in cold-formed
    steel framed walls. *SSRC Annual Stability Conference*. And Sputo T., Beery K. (2008)
    accumulation of brace forces over several studs *(verify)*. **Use:** strap + blocking rows
    as in the viewer: strength and stiffness check of the row and its anchorage.

### D. Code evolution: what the second-generation Eurocode changes

16. [1] EN 1993-1-3:2024 (second generation), with prA1:2026 draft amendment (adds DSM
    references in notes and bibliography; corrections). Owner to obtain the MSZ / BSI text.
    **Use:** the citation basis of the whole module from 2028 on; harmonised wording with
    1-1 / 1-5 / 1-8; what moved in the clauses used by the prototype (5.5, 6.1, 6.2, 8.2.5).
17. [1] Ungermann D. et al. (2022). A new Eurocode-compliant design approach for cold-formed steel
    sections. *ce/papers* (Eurosteel 2022), TU Dortmund. **Use:** DSM in a Eurocode frame; the
    bridge between the prototype's EWM and the CUFSM results already in the QA.
18. [2] JRC (2025). The second-generation Eurocodes - key changes and benefits through design
    examples, online workshop 3-5 June 2025; section "Evolution of EN 1993-1-3". **Use:**
    change list from the drafters (fetch attempted from the cloud, see section 4).
19. [2] An assessment of the Eurocode 3 simplified formulas for distortional buckling of
    cold-formed steel lipped channels. *Applied Sciences* 14(11), 4924 (2024) *(authors verify)*.
    **Use:** quantifies what the QA saw: σcr,s of (5.15) against finite strip; whether to use
    5.5.3.1(8) numerical σcr,s for the FLINS lip.
20. [2] EN 1993-1-14 (design assisted by FE analysis; already in the owner's Drive) and the 2024
    data paper "Dataset of a numerical model of a cold-formed C-shaped section in compression
    according to EN 1993-1-14" *(verify)*. **Use:** the route for the members the rules do not
    cover, if ever needed.

### E. Benchmarks and design manuals (to have on the shelf)

21. [1] Access Steel SX022a (lipped channel in bending) and SX023a (lipped channel in
    compression) worked examples; SF038a flowchart is already on Drive. **Use:** the external
    benchmark the QA could not run from the cloud (SCIA reproduces SX023a: Aeff = 436.8 mm²,
    χd = 0.744).
22. [1] Dubina D., Ungureanu V., Landolfo R. (2012). *Design of Cold-formed Steel Structures*.
    ECCS / Ernst & Sohn. **Use:** worked examples for every check type; the house style of a
    calculation annex.
23. [2] AISI S100-16 (2020) with Supplement 2 and AISI S240-20 (North American standard for CFS
    structural framing). **Use:** the hole rules, web crippling with holes, bridging and
    stud-to-track provisions that EN 1993-1-3 does not have (memo §4.1, §4.4).
24. [3] SCI P402 *Light steel framing in residential construction* and the ECCS TC7 design
    manuals *(titles verify)*. **Use:** practice conventions for panelised houses, detailing
    that keeps members inside the calculation rules.

## 3  (e) Inventor and SolidWorks export

- The native formats (.ipt / .iam, .sldprt / .sldasm) are proprietary binary containers. No
  public specification exists; third-party readers (CAD Exchanger, Altair, CoreTechnologie)
  reverse-engineer them under licence and lag the current versions. Writing them without the
  vendor's own application is not a realistic route.
- Writing them *with* the vendor's application is possible only through its API (Inventor API /
  iLogic, SolidWorks API) on a Windows machine with a licence: a script drives the installed
  program. If FLINS or the owner holds a licence, a small importer script can rebuild the frame
  from our member list; that is their side of the fence, not ours.
- The route that needs nothing: STEP AP214 / AP242 from an open kernel (CadQuery / OCP, i.e.
  OpenCASCADE). Both Inventor and SolidWorks import STEP natively, and AP242 carries assembly
  structure and part names, so every member arrives as its own body with its mark. STEP already
  is the agreed deliverable (D-032). For BIM use IFC via IfcOpenShell is the second open route.
- Recommendation: STEP AP242 with one body per member, named by mark, plus a CSV BOM keyed to
  the same marks. No native export.

## 4  Addendum

The research continuation of 2026-11-13 (EN 1993-1-3:2024 change leads, Access Steel SX022a/SX023a target numbers from the SCIA benchmark pages, vendor verification examples, stud-to-track and bridging papers, open-source tools) is in `READING_LIST_addendum_research_2026-11-13.md`. Two leads that change the plan: the 2024 edition renumbers the clauses the prototype cites (materials 5, members 8; inferred, verify) and contains no DSM equations (prA1:2026 adds only a reference); SX022a has unequal flanges, so the prototype needs the b1 != b2 extension before that benchmark runs.

## 5  Still wanted / blocked from the cloud

- JRC 2025 workshop PDF (item 18): host eurocodes.jrc.ec.europa.eu is outside the cloud network policy; owner fetches locally (the ResearchGate entry lists the same proceedings).
- Access Steel SX022a / SX023a (item 21): hosts blocked from the cloud; owner fetches locally.
- Items 3, 4, 5, 6, 7, 12, 15, 19, 24: author / title fields to verify on landing.
