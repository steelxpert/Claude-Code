# ccxio

CalculiX **.inp reader/writer** and **.frd reader/writer** for Python — no
dependencies, formats byte-compatible with what `ccx` itself writes, so the
files open directly in **PrePoMax** and **cgx**. Includes geometric
**imperfection seeding** (CalculiX has no `*IMPERFECTION` keyword).

## The imperfection loop, end to end

```python
from ccxio import read_inp, read_frd, seed_imperfection, write_inp

model  = read_inp("member.inp")             # perfect mesh
modes  = read_frd("member_buckle.frd")      # *BUCKLE result from ccx
mode1  = modes.result("DISP", 0)            # first eigenmode
print(mode1.time)                           # its buckling factor

seeded = seed_imperfection(model, mode1, amplitude=0.64)  # peak |u| = 0.64
write_inp(seeded, "member_imperfect.inp")   # ready for the GMNIA run
```

`seed_imperfection` scales the field so its peak displacement magnitude
equals `amplitude` (pass `scale=` instead for a raw factor) and returns a
new model; combine modes by calling it repeatedly. `write_inp` reproduces
every keyword block of the source deck verbatim and regenerates only the
`*NODE` coordinate lines.

## Other uses

```python
from ccxio import read_inp, write_frd, NodalResult

model = read_inp("member.inp")
print(model.nset("FIX"))              # set names are case-insensitive
print(model.cards_named("MATERIAL"))  # every keyword block is preserved

# attach any nodal field and view it in PrePoMax/cgx
disp = NodalResult("DISP", ("D1", "D2", "D3"),
                   {nid: (0.0, 0.0, 0.0) for nid in model.nodes})
write_frd(model, "member.frd", results=[disp])
```

Command line:

```bash
ccxio convert model.inp -o model.frd     # inspect a mesh without solving
ccxio seed model.inp modes.frd --amplitude 0.64 -o seeded.inp
ccxio seed model.inp modes.frd --mode 2 --scale 1.0
```

## Install

```bash
pip install -e .          # from a checkout
pip install -e .[dev]     # with pytest
```

## What is supported (v0.2)

**.inp reader** (`read_inp`)
- nodes, elements (all common CCX types), `*NSET`/`*ELSET` incl.
  `GENERATE` and set-name references, `*NODE, NSET=` / `*ELEMENT, ELSET=`
  collection, `*INCLUDE`, comments, trailing-comma continuations (plus
  node-count based continuation for meshers that omit the comma)
- every other keyword block is kept verbatim in `model.cards`

**.inp writer** (`write_inp`)
- re-emits the deck from `model.cards` (order and data verbatim, `*NODE`
  coordinates regenerated from the model — exact float round-trip)
- models without cards are written as a minimal `*NODE`/`*ELEMENT`/sets deck

**.frd writer** (`write_frd`)
- node/element blocks in ASCII format; nodal result blocks: vectors (with
  the calculated `ALL` record like ccx writes for `DISP`), 6-component
  tensors (`STRESS` component order), scalars, >6-component datasets with
  `-2` continuation lines
- `1PSTEP`/`100CL` headers reproduce the `frdheader.c` algorithm, including
  the fixed-point time format ccx uses since 2018

**.frd reader** (`read_frd`)
- node block, element block, all nodal result datasets (column-sliced, so
  packed negative values parse correctly); calculated components (`ALL`)
  are dropped; `1PSTEP` step/increment and `100CL` time (buckling factor /
  frequency) are attached to each dataset
- ASCII only; binary `.frd` files are rejected with a clear message

**Imperfection seeding** (`seed_imperfection`) — see above.

The he20/pe15 `.inp`→`.frd` connectivity reordering from `frd.c` is applied
on write and inverted on read; a `.frd` stores only element shape, so read
element types come back as the representative type (`C3D20R` → `C3D20`).

Element types with no frd shape (springs, dashpots, masses) are skipped in
the element block, matching ccx behaviour.

**Not yet**: binary `.frd`, element-face result blocks, `.dat` history
parsing, axisymmetric expansion.

## Format fidelity and validation

All line layouts are transcribed from the CalculiX sources (`frd.c`,
`frdheader.c`, `frdselect.c`, `frdvector.c` — Guido Dhondt, GPLv2) rather
than from the cgx manual alone; the test-suite pins the exact column
positions. The reader and the full seed pipeline are additionally validated
against a live `ccx` 2.21 solve (single C3D20 brick under uniaxial
compression): mesh and connectivity round-trip identically, `DISP` is exact
and `STRESS` matches the hand calculation.

## Tests

```bash
python -m pytest
```
