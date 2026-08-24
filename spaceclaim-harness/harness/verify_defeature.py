"""Conservation verification for a defeaturing run.

Defeaturing has no analytic target; "correct" means NOTHING IMPORTANT
CHANGED. Three measured states anchor the checks:
    before    - the model as received
    structure - after component (fastener) deletion, before defeaturing
    after     - the cleaned model
The reference for conservation is `structure`, NOT `before`: removing a
bolt that protrudes legitimately shrinks the bbox and volume, and that
removal is accounted for explicitly in the manifest instead.
"""


def _check(checks, name, ok, detail):
    checks.append({"name": name, "ok": bool(ok), "detail": detail})
    return ok


def _rel(a, b):
    return abs(a - b) / b if b else 0.0


def verify(result, recipe):
    checks = []
    warnings = []

    if not _check(checks, "script_status", result.get("status") == "ok",
                  "status=%r error=%r" % (result.get("status"),
                                          result.get("error"))):
        return {"passed": False, "warnings": warnings, "checks": checks}

    before = result["before"]
    structure = result["structure"]
    after = result["after"]
    man = result["manifest"]
    fil = man.get("fillets", {})
    hol = man.get("holes", {})
    deleted = man.get("deleted_components", [])

    # 1) The recipe must have gripped SOMETHING; matching nothing at all
    #    usually means wrong thresholds or a unit mistake.
    touched = (fil.get("selected", 0) + hol.get("selected", 0)
               + len(deleted))
    _check(checks, "selection_effective", touched > 0,
           "fillets selected=%d, holes selected=%d, components deleted=%d"
           % (fil.get("selected", 0), hol.get("selected", 0), len(deleted)))

    # 2) Fastener accounting: volume lost between `before` and `structure`
    #    must equal the manifest's deleted volumes. A mismatch means a
    #    body vanished that nobody logged - the worst failure mode.
    v_deleted = sum(d.get("volume_mm3", 0.0) for d in deleted)
    v_gap = before["volume_mm3"] - structure["volume_mm3"]
    _check(checks, "fastener_accounting",
           abs(v_gap - v_deleted) <= 0.005 * before["volume_mm3"],
           "volume drop %.0f mm3 vs manifest-deleted %.0f mm3"
           % (v_gap, v_deleted))

    # 3) Volume conservation of the structure through defeaturing.
    tol = float(recipe.get("volume_tolerance_pct", 2.0)) / 100.0
    _check(checks, "volume_conservation",
           _rel(after["volume_mm3"], structure["volume_mm3"]) <= tol,
           "after=%.0f vs structure=%.0f mm3 (%.2f%%, tol %.1f%%)"
           % (after["volume_mm3"], structure["volume_mm3"],
              100 * _rel(after["volume_mm3"], structure["volume_mm3"]),
              100 * tol))

    # 4) Bounding box: defeaturing must not move the envelope.
    bb_ok = all(abs(a - s) <= 0.002 * max(s, 1.0)
                for a, s in zip(after["bbox_mm"], structure["bbox_mm"]))
    _check(checks, "bbox_conservation", bb_ok,
           "after=%s vs structure=%s mm" % (after["bbox_mm"],
                                            structure["bbox_mm"]))

    # 5) Defeaturing never changes the body count.
    _check(checks, "body_count",
           after["body_count"] == structure["body_count"],
           "after=%d vs structure=%d" % (after["body_count"],
                                         structure["body_count"]))

    # 6) Per-feature failures: some fillets/holes resisting removal is
    #    normal and reported; too many means the approach is wrong.
    n_sel = fil.get("selected", 0) + hol.get("selected", 0)
    n_fail = fil.get("failed", 0) + hol.get("failed", 0)
    max_fail = float(recipe.get("max_feature_failure_pct", 10.0)) / 100.0
    _check(checks, "feature_failures",
           n_sel == 0 or n_fail <= max_fail * n_sel,
           "%d of %d selected features failed" % (n_fail, n_sel))
    if 0 < n_fail:
        warnings.append("%d feature(s) resisted removal - listed in the "
                        "manifest; review them in the GUI" % n_fail)

    return {"passed": all(c["ok"] for c in checks),
            "warnings": warnings, "checks": checks}
