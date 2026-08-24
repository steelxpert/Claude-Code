"""Mock backend for the defeature pipeline: fabricates a plausible
before/structure/after triplet plus manifest, so the batch driver and
verifier run on any OS. `defect` injects known failure modes."""


def run(params, defect=None):
    v_before = 2.4e6                      # mm3, a mid-size weldment
    fastener_vols = [1200.0, 1150.0, 300.0, 310.0]   # 2 bolts, 2 nuts
    deleted = [
        {"name": "DIN912_M8x30", "volume_mm3": fastener_vols[0]},
        {"name": "DIN912_M8x30_2", "volume_mm3": fastener_vols[1]},
        {"name": "nut_M8", "volume_mm3": fastener_vols[2]},
        {"name": "nut_M8_2", "volume_mm3": fastener_vols[3]},
    ]
    v_structure = v_before - sum(fastener_vols)
    v_after = v_structure * 1.004         # fills/sharp corners add ~0.4%
    bbox = [640.0, 420.0, 180.0]
    result = {
        "status": "ok", "backend": "mock",
        "input": params.get("input", "mock_assembly.stp"),
        "before": {"volume_mm3": v_before, "bbox_mm": [660.0, 420.0, 180.0],
                   "body_count": 11, "component_count": 11},
        "structure": {"volume_mm3": v_structure, "bbox_mm": list(bbox),
                      "body_count": 7},
        "after": {"volume_mm3": v_after, "bbox_mm": list(bbox),
                  "body_count": 7},
        "manifest": {
            "deleted_components": deleted,
            "fillets": {"selected": 38, "removed": 36, "failed": 2},
            "holes": {"selected": 12, "filled": 12, "failed": 0},
        },
        "exports": [],
    }
    if defect == "lost_body":             # a structural part vanished
        result["structure"]["volume_mm3"] -= 85000.0
        result["structure"]["body_count"] -= 1
        result["after"]["volume_mm3"] -= 85000.0
        result["after"]["body_count"] -= 1
    elif defect == "volume_blown":        # a fill went badly wrong
        result["after"]["volume_mm3"] = v_structure * 1.08
    elif defect == "nothing_removed":     # thresholds matched nothing
        result["structure"] = dict(result["before"], body_count=11)
        result["after"] = dict(result["before"], body_count=11)
        result["manifest"] = {"deleted_components": [],
                              "fillets": {"selected": 0, "removed": 0,
                                          "failed": 0},
                              "holes": {"selected": 0, "filled": 0,
                                        "failed": 0}}
    elif defect == "fill_failures":       # removal keeps failing
        result["manifest"]["fillets"] = {"selected": 38, "removed": 22,
                                         "failed": 16}
    elif defect == "script_error":
        result = {"status": "error", "backend": "mock",
                  "error": "Traceback: fill failed on face 1042"}
    return result
