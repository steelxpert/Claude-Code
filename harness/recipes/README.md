# recipes/ — reproducible analysis runs

One file per run that produced a number used anywhere (note, table, deck). Convention
borrowed from the PMX harness.

Header (first lines of every recipe):

```
# R<nn>_<task>.py — <one line: what it computes>
# Session: FLIN-nnn   Date: YYYY-MM-DD   Status: [DOC] | [MEASURED] | [INFERENCE]
# Inputs: <files, catalogue version>   Outputs: <files>
# Acceptance stated before the run: <value and where it is read>
```

Rules: explicit inputs (no hidden state), one statement per line, results written to a
file next to the recipe, `[MEASURED]` only after a clean re-run in a fresh folder. The
span-table generator (`floorframe/fea/campaign.py`) is the only route that may write
`floorframe/catalog/load_tables.json`; until the GMNIA campaign and the T-series tests
exist every table stays `source: "PLACEHOLDER"`.
