"""Objective verification of a SpaceClaim gear build against analytic truth.

Input: the result.json written by the in-app script (or mock backend):
    {status, volume_mm3, bbox_mm: [dx, dy, dz], body_count, tooth_count?}
Output: {"passed": bool, "warnings": [...], "checks": [{name, ok, detail}]}
"""


def _check(checks, name, ok, detail):
    checks.append({"name": name, "ok": bool(ok), "detail": detail})
    return ok


def verify(result, exp):
    checks = []
    warnings = []

    if not _check(checks, "script_status", result.get("status") == "ok",
                  "status=%r error=%r" % (result.get("status"),
                                          result.get("error"))):
        return {"passed": False, "warnings": warnings, "checks": checks}

    _check(checks, "single_body", result.get("body_count") == 1,
           "body_count=%r (expected 1; >1 means an open/failed profile)"
           % result.get("body_count"))

    bbox = result.get("bbox_mm") or [0, 0, 0]
    od = max(bbox[0], bbox[1])
    da = exp["tip_d"]
    # Polyline-approximated involutes may shave the tips slightly: allow
    # -2% under, +0.5% over the analytic tip diameter.
    _check(checks, "outer_diameter",
           0.98 * da <= od <= 1.005 * da,
           "bbox OD=%.3f mm vs tip_d=%.3f mm" % (od, da))

    b = exp["face_width"]
    _check(checks, "face_width",
           abs(bbox[2] - b) <= 0.005 * b + 1e-6,
           "bbox dz=%.3f mm vs face_width=%.3f mm" % (bbox[2], b))

    vol = float(result.get("volume_mm3") or 0.0)
    v_min, v_max = exp["volume_min_mm3"], exp["volume_max_mm3"]
    _check(checks, "volume_envelope",
           0.98 * v_min <= vol <= 1.02 * v_max,
           "volume=%.1f mm3 vs envelope [%.1f, %.1f]" % (vol, v_min, v_max))
    v_est = exp["volume_est_mm3"]
    if vol and abs(vol - v_est) > 0.10 * v_est:
        warnings.append("volume %.1f deviates >10%% from estimate %.1f "
                        "(model builds, but tooth form is suspect)"
                        % (vol, v_est))

    if result.get("tooth_count") is not None:
        _check(checks, "tooth_count",
               int(result["tooth_count"]) == exp["teeth"],
               "counted %r, expected %d" % (result["tooth_count"],
                                            exp["teeth"]))

    if exp["undercut_risk"]:
        warnings.append("z=%d < 17: undercut not modelled; flank is "
                        "approximated below the base circle" % exp["teeth"])

    return {"passed": all(c["ok"] for c in checks),
            "warnings": warnings, "checks": checks}
