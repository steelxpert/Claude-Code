# 01 · Q&A and feasibility pass

Input: FlexInSheet Kft. brainstorming note (2026-10) and the STEELXPERT overview
"Hidegen hajlított acél padlórendszerek – tervezési alapok" (2026-10).
Format: each question gets a provisional answer or a working assumption so the work can
continue; items marked **[CLIENT]** need FlexInSheet's decision, **[GEO]** the
geotechnical partner's, **[CSABA]** yours.

## A. Product and scope

**Q1. Which floor type is the product?**
The overview already narrows it to the joisted floor cassette (C-joists on rim track,
OSB deck) rather than composite deck or volumetric modules. Assumption: single-storey
ground floor over screw piles first; upper floors (wall-to-wall) later with the same
catalogue. The ground-floor case adds the bearer (sill) line on pile heads, which the
US/Canadian floor framing documents treat only generically.

**Q2. Prefabricated cassette or site-assembled framing?** **[CLIENT]**
This decides the joint catalogue (factory rivet/clinch vs site screws), the lifting load
case, and whether the app must split the layout into transportable panels (≈ 2.5 × 12 m).
Assumption for the rough app: site-assembled stick framing, with panelisation as an
optional post-processing step.

**Q3. What load envelope must the tables cover?**
EN 1991-1-1 with the Hungarian NA: category A floors q = 2.0 kN/m² (NA value; UK 1.5 is
not applicable), partition allowance 0.8–1.2 kN/m², finishes/self-weight 0.5–1.5 kN/m²
depending on build-up (dry 0.4, screed 1.5+). Point loads: 2.0 kN (cat. A) and
user-defined (stoves, bath, piano). Table axis therefore: total characteristic
(g + q) classes 2.5 / 3.5 / 4.5 / 5.5 kN/m², plus a point-load check.

**Q4. Serviceability criteria?** **[CSABA]**
Deflection L/350 and 15 mm (characteristic), L/450 live only, 1 kN point load limit and
the 8 Hz / 5 mm vibration criterion from SCI P402 as the default set, because the
Hungarian NA leaves it to the designer. Vibration will govern long spans; the table
must carry a separate vibration column, not only strength.

**Q5. Which section family?** **[CLIENT]**
Lipped C 150–300 mm deep, 1.2–2.5 mm, S350GD+Z, 400/600 mm spacing, with web holes for
services. FlexInSheet's roll-former defines the real family; the catalogue is a JSON
file so changing it costs nothing. Rim track and bearers: back-to-back C or box.

## B. Structural method

**Q6. AISI as guidance, Eurocode as verification: compatible?**
Yes. AISI S240 gives the framing *rules* (bearing stiffeners, blocking, web-hole
limits, diaphragm detailing, span-table format). Resistances are produced by GMNIA and
verified under EN 1993-1-3 / EN 1993-1-14 with γ_M1. DSM (AISI S100 App. 1) serves as
the independent benchmark of every GMNIA peak, exactly as in the existing virtual-testing
method. Where AISI prescribes something Eurocode does not (e.g. bearing-stiffener rules)
we adopt the AISI rule and prove it by the FE study.

**Q7. Is a parametric GMNIA load-table campaign feasible with CalculiX?**
Feasible and already proven at member level. Size of the campaign: 7 sections × 2
spacings × ~6 spans × 4 load classes ≈ 340 joist cases, plus support/web-crippling
cases (≈ 60) and bearer cases (≈ 80). At 5–20 min per S8R displacement-controlled run
that is a few CPU-days on one workstation; trivial in parallel. The expensive part is
not solving but the **validation** against a physical test series (EN 1993-1-14 model
factor γ_FE) — budget at least one test series per failure mode.

**Q8. Which failure modes must the tables resolve?**
Mid-span: local/distortional buckling in bending (top flange braced by deck, bottom
flange free), vibration. Supports: web crippling (EN 1993-1-3 6.1.7) with and without
bearing stiffener — the overview is right that this governs most often. Bearer on pile
head: combined bending + crippling + hold-down. Each is a separate table.

**Q9. Joints: parametric too?**
Yes, but with physical tests as the primary source: joist-to-rim (clip angle / swaged
end / tab), joist-to-bearer, bearer-to-pile head. GMNIA of screwed joints is possible
with the hinge/spring idealisation already in the method, but EN 1993-1-3 §8 + test
calibration is cheaper for self-drilling screws. Recommendation: test-based joint
resistances, FE only for the pile-head detail (the only non-standard joint).

**Q10. Geotechnics boundary** **[GEO]**
The app needs from the geotechnical partner only: design compression resistance per
pile type and length class, lateral/uplift resistance, minimum spacing, and frost depth
rule. These enter as a second JSON catalogue; the app never computes soil mechanics.

## C. The app

**Q11. Who uses it and what must it output?**
Sales staff with basic technical background. Output: a proposal pack (plan with joists,
bearers, piles; bill of materials; price; a "design basis" sheet signed off by the
engineer). The structural part must be **deterministic and traceable** (table lookup +
documented rules) so a proposal is reproducible and auditable — AI must never be in
the load path.

**Q12. Input from authority permit drawings: realistic?**
Partly. Hungarian permit sets are PDF; DXF is available in maybe half of the cases on
request. Vectorised PDF line extraction works for walls when the drawing is clean, fails
on hatched or raster plans. Practical path: (1) DXF import, (2) vector-PDF import with
the user confirming the outline, (3) manual tracing/drawing of the floor outline in the
browser on top of the PDF as an image. (3) is the safety net and must exist from day one.

**Q13. Run on client PC, own server, in a browser: contradictory?**
No. A Python backend (FastAPI) + browser front-end runs identically on a laptop
(single executable or Docker), on FlexInSheet's server, or hosted. Catalogues and load
tables are fetched from a central URL with a local cache, so updates do not require
reinstalling.

**Q14. AI-assisted?**
Yes, but outside the load path: drawing interpretation assistance (which polygon is the
floor, which walls are load-bearing), proposal text, Q&A for sales staff, and as the
developer-side driver of the FEA campaign (the PrePoMax/CalculiX MCP server). The
structural engine stays plain code.

**Q15. FreeCAD as GUI?**
No for the sales tool: too heavy, desktop-only, steep UI. Keep it as an optional
exporter (IFC/3D) later. Web UI with SVG/2D canvas is enough for a layout tool.

## D. Risks, in order

1. Hungarian acceptance of screw piles (no national rule; DIBt route is German) — **[GEO]**.
2. Model factor γ_FE: without physical tests the tables are not Eurocode-compliant.
3. Vibration criteria undefined in the Hungarian NA — needs an explicit design basis.
4. Drawing import quality — mitigated by manual tracing.
5. Fire and acoustic performance are test-based, not calculable; they constrain the
   build-up catalogue, not the app.

Verdict: doable. The structural pipeline is an extension of what already exists; the
app is standard web engineering. The critical path is the test campaign and the
geotechnical approval, not the software.
