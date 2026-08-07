# ccxio

CalculiX **.inp mesh reader** and **.frd result writer** for Python — no
dependencies, output byte-compatible with what `ccx` itself writes, so the
files open directly in **PrePoMax** and **cgx**.

## Why

Typical workflow this package serves: generate or read a CalculiX input deck
in a script, compute a nodal field (e.g. a scaled buckling mode shape as an
imperfection field), and write it as a `.frd` displacement dataset that
PrePoMax can consume via *Update Nodal Coordinates From File* — or simply
convert an `.inp` mesh to `.frd` to inspect it without running a solve.

## Install

```bash
pip install -e .          # from a checkout
pip install -e .[dev]     # with pytest
```

## Usage

```python
from ccxio import read_inp, write_frd, NodalResult

model = read_inp("member.inp")
print(len(model.nodes), len(model.elements))
print(model.nset("FIX"))              # set names are case-insensitive
print(model.cards_named("MATERIAL"))  # every keyword block is preserved

# attach a nodal vector field (e.g. an imperfection / mode shape)
disp = NodalResult(
    "DISP", ("D1", "D2", "D3"),
    {nid: (0.0, 0.0, 0.0) for nid in model.nodes},
    step=1, increment=1, time=1.0,
)
write_frd(model, "member.frd", results=[disp])
```

Command line (mesh-only conversion):

```bash
ccxio model.inp -o model.frd
# or: python -m ccxio model.inp
```

## What is supported (v0.1)

**Reader** (`read_inp`)
- nodes, elements (all common CCX types), `*NSET`/`*ELSET` incl.
  `GENERATE` and set-name references, `*NODE, NSET=` / `*ELEMENT, ELSET=`
  collection, `*INCLUDE`, comments, trailing-comma continuations (plus
  node-count based continuation for meshers that omit the comma)
- every other keyword block is kept verbatim in `model.cards`

**Writer** (`write_frd`)
- node and element blocks in ASCII short format
- nodal result blocks: vectors (with the calculated `ALL` record like ccx
  writes for `DISP`), 6-component tensors (`STRESS` component order),
  scalars, and >6-component datasets with `-2` continuation lines
- `1PSTEP` / `100CL` headers reproduce the `frdheader.c` algorithm,
  including the fixed-point time format ccx uses since 2018
- the he20/pe15 `.inp`→`.frd` connectivity reordering from `frd.c`

Element types with no frd shape (springs, dashpots, masses) are skipped in
the element block, matching ccx behaviour.

**Not yet**: `.frd` reading, binary `.frd` output, element-face result
blocks, axisymmetric expansion.

## Format fidelity

All line layouts are transcribed from the CalculiX sources (`frd.c`,
`frdheader.c`, `frdselect.c`, `frdvector.c` — Guido Dhondt, GPLv2) rather
than from the cgx manual alone; the test-suite pins the exact column
positions.

## Tests

```bash
python -m pytest
```
