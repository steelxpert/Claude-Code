"""Linux/CI stand-in for SpaceClaim: fabricates a plausible result.json.

Lets the whole loop (params -> build -> measure -> verify) run without a
Windows box or a license. `defect` injects known failure modes so the
verifier itself can be tested.
"""
import math


def run(params, defect=None):
    m = float(params["module"])
    z = int(params["teeth"])
    b = float(params.get("face_width", 10.0))
    bore = float(params.get("bore_d", 0.0))
    da = m * (z + 2.0)
    df = m * (z - 2.5)
    area = (math.pi / 4.0) * (df ** 2 + 0.5 * (da ** 2 - df ** 2)
                              - bore ** 2)
    result = {
        "status": "ok",
        "backend": "mock",
        "volume_mm3": area * b * 1.002,   # deterministic ~0.2% CAD noise
        "bbox_mm": [da * 0.999, da * 0.999, b],
        "body_count": 1,
        "tooth_count": z,
        "exports": [],
    }
    if defect == "missing_tooth":
        result["tooth_count"] = z - 1
        result["volume_mm3"] *= 1.01
    elif defect == "half_width":
        result["bbox_mm"][2] = b / 2.0
        result["volume_mm3"] /= 2.0
    elif defect == "split_body":
        result["body_count"] = 2
    elif defect == "blank_disk":
        result["volume_mm3"] = math.pi / 4.0 * da ** 2 * b
        result["tooth_count"] = 0
    elif defect == "script_error":
        result = {"status": "error", "backend": "mock",
                  "error": "Traceback: NameError: SketchCircle"}
    return result
