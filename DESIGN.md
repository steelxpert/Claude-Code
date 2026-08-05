# solidx — Design Document (v0.1)

Working name: **solidx** (trivially renameable). Status: draft for review.

## 1. Mission

A reliable, fast, implicit finite-element engine for **solid (continuum) elements only**,
aimed at structural steel detail analysis: bolted connections, base plates, bearing
details, pins, formwork/carrier details. Full contact nonlinearity (normal + Coulomb
friction + bolt pretension), metal plasticity, large displacements, parallel on a single
workstation (CPU first, GPU later).

It complements — not replaces — the existing toolchain:

| Domain | Tool |
|---|---|
| Shells | CalculiX ccx + PrePoMax |
| Beams / global models | AxisVM |
| **Solids + contact** | **solidx (this project)** |

Target: exceed ccx *in this niche* on contact robustness, solver speed, pretension
ergonomics, and scriptability. Not a general-purpose FEA clone.

## 2. Non-goals

- Shell, beam, membrane, truss elements — permanently out of scope.
- Explicit dynamics, crash, metal forming, large-sliding self-contact.
- Coupled thermal, multiphysics.
- Distributed-memory MPI clusters. Design point is a 16–64-core workstation,
  optionally one CUDA GPU.
- A full interactive pre-processor (see §3: PrePoMax fills this role).

## 3. Key product decisions

1. **Input = a strict subset of the Abaqus/ccx `.inp` dialect.**
   PrePoMax works as the pre-processor from day one; users keep their workflow.
   Unsupported keywords fail loudly with a clear message — never silently ignored
   (a known ccx footgun). A native Python API is the second, first-class input path.
2. **Output = `.frd` (PrePoMax/CGX post-processing) + `.vtu` (ParaView) + tabular
   `.dat`-style results + direct Python access.**
3. **Own GUI is a late, optional phase.** First a results viewer (VTK-based), much
   later interactive model setup. GUI work never blocks solver phases.
4. **Clean-room implementation.** Algorithms from the open literature (Simo & Hughes;
   Wriggers; Laursen; Belytschko/Liu/Moran; Crisfield). No code copied from ccx
   (GPL) or other codebases. License: MIT (internal use anyway; keeps options open).

## 4. Numerical scope

### 4.1 Elements
- **C3D10** (quadratic tet) — the workhorse for general geometry.
- **C3D8I** (linear hex, incompatible modes) and **C3D8 + B-bar** — for swept/regular regions.
- **C3D4** (linear tet) — filler/tie regions only, documented as stiff.
- **C3D20R** — quadratic hex, reduced integration.
- **C3D6** wedge — mesh transition filler.
- Near-incompressibility at large plastic strain: B-bar / F-bar treatment on hex;
  document C3D10 limits (acceptable for connection-scale plastic strains).

### 4.2 Materials
- Linear elasticity.
- **J2 (von Mises) plasticity**, multilinear isotropic hardening, optional linear
  kinematic hardening; rate-independent; radial-return mapping with consistent
  algorithmic tangent. Validated against closed-form uniaxial/thick-cylinder solutions.
- Finite-strain treatment: total-Lagrangian, Green–Lagrange strain for NLGEOM;
  moderate-strain validity documented (ample for steel details; necking-grade strain
  accuracy is not a target). Neo-Hookean available for verification problems.

### 4.3 Geometric nonlinearity
- NLGEOM on/off per step; follower pressure loads; large rotation of parts in contact.

### 4.4 Contact (the core asset — phased)
- **C1 — small-sliding node-to-surface**: penalty normal + penalty-regularized Coulomb
  friction. Gets the pipeline working end to end.
- **C2 — augmented Lagrangian normal contact** (Uzawa loop): near-zero penetration
  without ill-conditioning, keeps the stiffness matrix positive definite (no saddle
  point → simpler, faster linear solves). Tangential Coulomb friction via
  return mapping in the tangent plane; stick/slip consistent tangent.
- **C3 — finite-sliding surface-to-surface** with segment-based (mortar-style)
  integration; contact smoothing.
- **C4 — ergonomics & robustness**: automatic contact-pair detection by proximity,
  automatic contact stabilization (viscous damping ramped out before completion — the
  cure for unconstrained-part rigid-body motion in bolted assemblies), interference
  fit / `ADJUST`, clearance control.
- **Bolt pretension**: true pre-tension section (cut surface + controlled relative
  displacement via constraint equations), force- or length-controlled, lockable across
  steps. First-class feature, not an afterthought.

### 4.5 Constraints
- Linear MPC / `*EQUATION`; rigid bodies with reference points; tie constraints
  (mortar-based, mesh-independent); kinematic and **distributing coupling** (load
  application onto solid faces).

### 4.6 Nonlinear solution
- Full Newton with line search; adaptive incrementation (cutback on divergence or
  contact chatter, growth on fast convergence — Abaqus-style heuristics);
  displacement-, force-, and mixed-control steps; multiple sequential steps
  (preload → service load).
- Quasi-Newton option for cheap re-solves. Arc-length deferred (rarely needed for
  contact-dominated connection problems; revisit if demanded).

### 4.7 Linear algebra & parallelism
- Default: **MKL Pardiso** sparse direct (LDLT/LLT), in-core with out-of-core option.
- Parallel assembly: OpenMP with graph coloring (no atomics on the hot path),
  NUMA-aware first touch.
- Optional iterative path for huge, elastic-dominated models: CG + AMG (amgcl).
- **GPU (later phase)**: NVIDIA cuDSS direct solver and/or mixed-precision
  factorization + iterative refinement; assembly stays on CPU initially.

## 5. Performance targets (acceptance-test grade, not marketing)

- 1 M-DOF bolted connection, 2 steps / ~20 increments / ~60 factorizations:
  **< 30 min wall-clock on a 16-core desktop**, assembly < 10 % of runtime.
- 5 M DOF feasible in-core on 128 GB or via OOC.
- GPU phase: ≥ 2–3× end-to-end on factorization-bound runs (RTX-class card).
- Determinism: same input + same thread count → bit-identical results.

## 6. Software architecture

- **Core: C++20**, no application framework. Eigen (dense local math), MKL
  (BLAS + Pardiso), OpenMP. Rust was considered; C/C++-native ecosystem
  (MKL, Gmsh, VTK, pybind11, reference codes) wins on integration cost.
- **Python package** via pybind11: model building, running, results as NumPy arrays;
  Gmsh Python API for scripted meshing.
- Strict module layering: `io/` (inp, frd, vtu) · `mesh/` · `model/` (materials,
  contact defs, steps) · `assembly/` (elements, constraints, contact kernels) ·
  `solve/` (Newton, linear solvers) · `post/`.
- Testing: Catch2 unit tests (return mapping, element kernels vs. finite differences)
  + pytest golden-benchmark suite; both gate CI. **No feature merges without a
  reference-solution test.**

## 7. Validation plan (the real product)

Tiered, CI-gated, cross-checked against analytical solutions first, ccx/Abaqus
references second:

1. Patch tests — all elements, all formulations.
2. Cook's membrane, curved-beam solid, cantilever convergence studies.
3. Thick-walled cylinder, elastic and elastic–plastic (closed form).
4. Uniaxial/multiaxial return-mapping unit tests vs. closed form.
5. Large-rotation solid bending vs. reference NLGEOM solutions.
6. **Hertz contact** (sphere–plane, cylinder–plane) vs. analytical.
7. NAFEMS contact benchmarks.
8. Friction: shear-loaded block stick/slip transition; ring compression trends.
9. Pretensioned bolted flange: preload accuracy, prying, slip onset — vs. ccx and
   published results.
10. A growing "nasty zoo": initial gaps + rigid-body motion, near-degenerate contact
    pairs, chatter provocations — every field-discovered failure becomes a test.

## 8. Phases & exit criteria

| Phase | Content | Exit criterion | Effort (steady sessions) |
|---|---|---|---|
| P0 | Repo skeleton, CI, mesh/model core, `.inp` reader v0 | patch test passes | days |
| P1 | Linear static: C3D10/C3D8I, Pardiso, parallel assembly, `.frd`/`.vtu` out | PrePoMax round-trip works; benchmarks 1–3 (elastic) pass | 2–4 weeks |
| P2 | NLGEOM + J2 plasticity + adaptive Newton | benchmarks 3–5 pass | +4–6 weeks |
| P3 | Contact C1→C2 + pretension + stabilization | Hertz, friction, bolted-flange benchmarks pass; first real connection cross-checked vs. ccx | **the long pole: +2–4 months** |
| P4 | Contact C3–C4 (finite sliding, auto-pairs) | field problems run without hand-tuning | +1–2 months |
| P5 | Performance: OOC, tuning, GPU (cuDSS) | §5 targets met | +1–2 months |
| P6 | GUI: VTK results viewer → model setup later | viewer replaces CGX for daily use | optional |

Honest calendar: **~6 months of steady sessions to "trusted alongside ccx with
cross-checks"; ~12 months to standalone confidence** for signed work. The limiting
resource is validation discipline, not code production.

## 9. Risks

- **Contact robustness long tail** — the known project-killer. Mitigation: AL
  formulation, automatic stabilization, and the benchmark zoo growing with every
  field failure.
- Volumetric locking with plasticity on tets — mitigation: hex-region guidance,
  B-bar/F-bar, documented limits.
- `.inp` dialect drift vs. PrePoMax expectations — mitigation: strict subset,
  loud errors, round-trip test in CI.
- Single-driver project — mitigation: this document, tests as specification,
  boring code style.

## 10. Open questions

1. GPU commitment: CUDA-only (cuDSS) acceptable, or vendor-neutral needed?
2. Kinematic hardening priority (cyclic checks) — P2 or later?
3. Exact `.inp` keyword coverage list for v1 (drive from a real PrePoMax export).
4. Final name and dedicated repository home.
