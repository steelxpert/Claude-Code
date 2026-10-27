"""Parametric GMNIA campaign: case matrix out, load tables in.

Scope of this module is the bookkeeping around the virtual tests, not the solver:
- `case_matrix()` enumerates joist cases (section x spacing x load class x span) and
  writes a JSON that the CalculiX/PrePoMax tooling (cfs-gmnia-virtual-testing +
  calculix-prepomax-ops skills) consumes one case at a time: build the S8R shell model,
  seed the Stage-1 imperfection (leading mode 100 %, accompanying 70 %, both signs),
  run displacement-controlled GMNIA, report the peak line load.
- `results_to_tables()` turns the peak line loads into the design table used by the
  layout engine: R_d = R_GMNIA / (gamma_FE * gamma_M1) per EN 1993-1-14, then the
  largest tabulated span whose design demand w_Ed is within R_d, with the deflection
  limit from the elastic branch of the same run.
"""
from __future__ import annotations

import json
from pathlib import Path

from .. import catalog

SPANS_MM = [2400, 3000, 3600, 4200, 4800, 5400, 6000, 6600, 7200]
DECK_SCREW_PITCH_MM = 300   # top-flange lateral restraint spacing (AISI S240 B2.7 / SCI P402)
GAMMA_FE_DEFAULT = 1.1       # until calibrated from the physical test series (EN 1993-1-14 Annex A)


def case_id(section: str, spacing: int, load_class: str, span: int) -> str:
    return f"J_{section}_s{spacing}_{load_class}_L{span}"


def case_matrix(spans: list[int] | None = None) -> list[dict]:
    cases = []
    for sec in catalog.sections():
        for s in catalog.spacings():
            for lc, loads in catalog.load_classes().items():
                for L in spans or SPANS_MM:
                    w_ed = (1.35 * loads["g"] + 1.5 * loads["q"]) * s / 1000
                    cases.append({
                        "id": case_id(sec.name, s, lc, L),
                        "section": sec.name, "h": sec.h, "b": sec.b, "c": sec.c, "t": sec.t,
                        "steel": catalog.steel(),
                        "span_mm": L, "spacing_mm": s, "load_class": lc,
                        "w_Ed_kN_m": round(w_ed, 3),
                        "w_sls_kN_m": round((loads["g"] + loads["q"]) * s / 1000, 3),
                        "model": {
                            "element": "S8R", "support": "simply supported, web bearing stiffener at supports",
                            "top_flange_restraint_mm": DECK_SCREW_PITCH_MM, "bottom_flange": "free",
                            "loading": "uniform line load on top flange via deck, displacement control at midspan",
                            "imperfection": {"leading": "from Stage-1 CUFSM/DSM triage", "accompanying_factor": 0.7,
                                             "amplitude": "EN 1993-1-5 Annex C equivalent (no separate residual stress field)",
                                             "signs": "both"},
                            "stage1": "cfs_triage.py on the section: Mcrl, Mcrd, Mcre(Lb = restraint spacing)",
                        },
                        "outputs": ["w_peak_kN_m", "collapse_mode", "deflection_at_w_sls_mm", "support_reaction_kN"],
                    })
    return cases


def write_case_matrix(path: str | Path, spans: list[int] | None = None) -> int:
    cases = case_matrix(spans)
    Path(path).write_text(json.dumps({"campaign": "joist-bending-v0", "gamma_FE": GAMMA_FE_DEFAULT,
                                      "gamma_M1": catalog.steel()["gamma_M1"], "cases": cases}, indent=1), encoding="utf-8")
    return len(cases)


def results_to_tables(results: list[dict], gamma_FE: float = GAMMA_FE_DEFAULT) -> dict:
    """results: [{id, section, spacing_mm, load_class, span_mm, w_peak_kN_m, deflection_at_w_sls_mm}, ...]

    Returns {"joists": [{section, spacing_mm, load_class, span_strength_mm, span_deflection_mm, source}, ...]}.
    Span limits are the largest tabulated span passing each check (no interpolation beyond the grid).
    """
    gM1 = catalog.steel()["gamma_M1"]
    sls = catalog._raw("sections.json")["serviceability"]
    groups: dict[tuple, list[dict]] = {}
    for r in results:
        groups.setdefault((r["section"], int(r["spacing_mm"]), r["load_class"]), []).append(r)
    rows = []
    for (sec, s, lc), rs in groups.items():
        loads = catalog.load_classes()[lc]
        w_ed = (1.35 * loads["g"] + 1.5 * loads["q"]) * s / 1000
        ok_strength = [r["span_mm"] for r in rs if r["w_peak_kN_m"] / (gamma_FE * gM1) >= w_ed]
        ok_defl = [r["span_mm"] for r in rs
                   if r["deflection_at_w_sls_mm"] <= min(r["span_mm"] / sls["deflection_total_ratio"], sls["deflection_total_max_mm"])]
        rows.append({"section": sec, "spacing_mm": s, "load_class": lc,
                     "span_strength_mm": max(ok_strength, default=0), "span_deflection_mm": max(ok_defl, default=0),
                     "source": f"GMNIA gamma_FE={gamma_FE}"})
    return {"joists": rows}
