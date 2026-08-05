# solidx — Design Document (v0.1)

Working name: **solidx** (trivially renameable). Status: draft for review.

## 1. Mission

A reliable, fast, implicit finite-element engine for **solid (continuum) elements only**,
aimed at structural steel detail analysis: bolted connections, base plates, bearing
details, pins, formwork/carrier details — up to and including **entire tunnel-formwork
carrier assemblies (Póka3d-class tunneling projects), where meshes can reach tens of
millions of DOFs**. Full contact nonlinearity (normal + Coulomb friction + bolt
pretension), metal plasticity, large displacements, parallel on a single workstation
(CPU first, GPU later).

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

Two solver pillars, chosen automatically by problem size (overridable):

- **Direct — MKL Pardiso** (LDLT/LLT), in-core with out-of-core option. Default for
  nonlinear contact work up to ~3–5 M DOF (factorization memory for 3D solids runs
  roughly 20–40 GB per 1 M DOF — the practical workstation wall).
- **Iterative — CG + AMG** (amgcl / hypre BoomerAMG): the *core* path for huge models,
  not an afterthought. Near-linear memory (~2–4 GB per 1 M DOF) and time scaling puts
  20–50 M DOF elastic models in workstation range. This is a load-bearing reason for
  the augmented-Lagrangian contact decision: AL/penalty keeps the system positive
  definite, so CG remains applicable where Lagrange-multiplier saddle points would not.
  Plasticity and closed contact degrade AMG convergence — mitigations: block-Jacobi
  smoothing, elastic-operator preconditioning, and falling back to direct on submodels.
- Parallel assembly: OpenMP with graph coloring (no atomics on the hot path),
  NUMA-aware first touch.
- **GPU (later phase)**: AMG on GPU (AmgX-class) for huge elastic solves; cuDSS /
  mixed-precision factorization + iterative refinement for direct; assembly stays on
  CPU initially.

### 4.8 Huge-model strategy (Póka3d-class assemblies)

- **Submodeling as a first-class workflow** (the industrial answer to "huge"):
  run the global assembly elastically (iterative solver, tens of M DOF), then drive
  detailed nonlinear contact submodels of the joints from interpolated global
  displacements (`*SUBMODEL`-style, node-based). Automatic cut-boundary detection,
  displacement interpolation with tolerance diagnostics, multiple submodels per global
  run. This decouples "huge" from "nonlinear" — each stays in its comfort zone.
- **Memory-lean by design**: 32-bit local indices where safe, per-element-block
  storage, no global dense scratch; peak-RAM report after every run.
- **I/O at scale**: binary `.frd` output, compressed `.vtu`; streaming writers
  (never hold two copies of a result field). Native compact results container
  (HDF5-based) for submodel interpolation and Python post-processing.
- **Post-processing reality**: PrePoMax's GUI degrades above ~5–10 M elements —
  document ParaView as the huge-model post-processor; PrePoMax remains the
  pre/post tool for component-scale work and submodels.
- **Meshing at scale**: Gmsh handles component meshes well; huge assemblies are
  meshed per-part and merged with tie constraints (mortar ties, §4.5) — also the
  natural pattern for formwork assemblies with bolted/pinned interfaces.
- Future option (explicitly deferred): static condensation / superelements for
  repeated identical carrier modules.

## 5. Performance targets (acceptance-test grade, not marketing)

Three size tiers, matching the workflows in §4.8:

- **T1 — nonlinear contact component** (bolted connection / joint submodel,
  ~1 M DOF, 2 steps / ~20 increments / ~60 factorizations): **< 30 min wall-clock
  on a 16-core desktop**, assembly < 10 % of runtime; direct solver.
- **T2 — nonlinear assembly** (~3–5 M DOF, AL contact): feasible on 128–256 GB via
  in-core or OOC direct; overnight-run acceptable, crash-free mandatory.
- **T3 — huge elastic global model** (20 M DOF, tunnel-formwork carrier assembly):
  CG+AMG setup + solve **< 15 min per load case on a 32-core / 256 GB workstation**;
  full submodel round-trip (global run → joint submodel with contact) in one working
  session.
- GPU phase: ≥ 2–3× end-to-end on factorization-bound runs (RTX-class card);
  T3-class solves on a 24 GB GPU up to ~5–8 M DOF, CPU beyond.
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
| P5 | Scale: CG+AMG core path, submodeling v1, binary/streaming I/O, OOC | T3 target met; global→submodel round-trip on a real carrier model | +1–2 months |
| P6 | GPU: AMG on GPU, cuDSS option, mixed precision | §5 GPU targets met | +1–2 months |
| P7 | GUI: VTK results viewer → model setup later | viewer replaces CGX for daily use | optional |

Note: submodeling v1 needs only P1+P2 (elastic global + nonlinear local) — it can be
pulled forward ahead of P3/P4 completion if a live Póka3d project needs it.

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

1. GPU commitment: CUDA-only (cuDSS/AmgX) acceptable, or vendor-neutral needed?
2. Kinematic hardening priority (cyclic checks) — P2 or later?
3. Exact `.inp` keyword coverage list for v1 (drive from a real PrePoMax export).
4. Final name and dedicated repository home.
5. **Calibration data needed**: 2–3 representative meshes from recent Póka3d carrier
   models (element counts, DOF, part/interface counts) to validate the §5 tier
   targets and size the submodeling workflow against reality.
