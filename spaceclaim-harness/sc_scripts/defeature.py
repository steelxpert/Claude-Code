# Python Script, API Version = V18
# ---------------------------------------------------------------------------
# FEA defeaturing script - runs INSIDE Ansys SpaceClaim 2020 R1 via
# /RunScript (see runner.py). Contract: reads %SC_JOB_DIR%/params.json
# (a cleanup recipe + "input" path), writes result.json, clean.stp,
# before.png, after.png.
#
# Pipeline:  open -> measure BEFORE -> delete fastener components
#         -> measure STRUCTURE -> remove fillets -> fill holes
#         -> measure AFTER -> export + manifest
#
# The three measured states let the verifier prove conservation:
# fastener removal is accounted per component; defeaturing must then
# keep volume/bbox/body-count of the remaining structure.
#
# IronPython 2.7, geometry in METERS (MM = 0.001). API calls marked
# VERIFY must be aligned once against a recorded macro (record: open a
# file, delete a component, Prepare > Remove Rounds, Fill on selected
# faces, save-as) - procedure in the spaceclaim-scripting skill.
# ---------------------------------------------------------------------------
import json
import math
import os
import traceback

MM = 0.001
LOG = []


def log(msg):
    LOG.append(msg)


def name_matches(name, patterns):
    low = name.lower()
    for p in patterns:
        if p.lower() in low:
            return True
    return False


# ------------------------- measurement helpers -----------------------------

def all_bodies():
    """Every design body in the whole assembly tree."""
    bodies = []

    def walk(part):
        for b in part.Bodies:
            bodies.append(b)
        for comp in part.Components:
            walk(comp.Content)               # VERIFY: child part accessor
    walk(GetRootPart())
    return bodies


def body_volume_mm3(body):
    return body.Shape.Volume / (MM ** 3)     # VERIFY: Volume in m^3


def measure():
    bodies = all_bodies()
    vol = 0.0
    lo = [1e30, 1e30, 1e30]
    hi = [-1e30, -1e30, -1e30]
    for b in bodies:
        vol += body_volume_mm3(b)
        box = b.Shape.GetBoundingBox(Matrix.Identity)   # VERIFY
        mn = (box.MinCorner.X, box.MinCorner.Y, box.MinCorner.Z)
        mx = (box.MaxCorner.X, box.MaxCorner.Y, box.MaxCorner.Z)
        for i in range(3):
            lo[i] = min(lo[i], mn[i])
            hi[i] = max(hi[i], mx[i])
    bbox = [(hi[i] - lo[i]) / MM for i in range(3)] if bodies else [0, 0, 0]
    return {"volume_mm3": vol, "bbox_mm": bbox, "body_count": len(bodies)}


# --------------------------- cleanup operations ----------------------------

def delete_fastener_components(patterns, keep_patterns):
    """Delete components whose name matches the recipe; log each with its
    volume so the verifier can account for every removed gram."""
    deleted = []

    def walk(part):
        # snapshot the list - we mutate while iterating
        comps = [c for c in part.Components]
        for comp in comps:
            name = comp.Content.Master.DisplayName    # VERIFY: name accessor
            if name_matches(name, keep_patterns):
                continue
            if name_matches(name, patterns):
                vol = 0.0
                for b in comp.Content.Bodies:
                    vol += body_volume_mm3(b)
                Delete.Execute(Selection.Create(comp))  # VERIFY
                deleted.append({"name": name, "volume_mm3": vol})
                log("deleted %s (%.0f mm3)" % (name, vol))
            else:
                walk(comp.Content)
    walk(GetRootPart())
    return deleted


def select_round_faces(max_r_mm):
    """Faces that are fillets/rounds with radius <= max_r_mm.

    VERIFY: prefer the recorded power-selection call if the macro shows
    one. Fallback below walks faces and picks cylinder/torus geometry by
    radius - functional but slower on huge assemblies."""
    faces = []
    for body in all_bodies():
        for f in body.Faces:
            geo = f.Shape.Geometry                     # VERIFY
            r = None
            if isinstance(geo, Cylinder):              # VERIFY type names
                r = geo.Radius
            elif isinstance(geo, Torus):
                r = geo.MinorRadius
            if r is not None and r <= max_r_mm * MM:
                faces.append(f)
    return faces


def select_small_hole_faces(max_d_mm):
    """Cylindrical faces of holes with diameter <= max_d_mm.
    VERIFY against a recorded 'select holes' power selection; fallback
    picks small cylinders (a hole wall is a cylinder seen from inside)."""
    faces = []
    for body in all_bodies():
        for f in body.Faces:
            geo = f.Shape.Geometry                     # VERIFY
            if isinstance(geo, Cylinder) and \
                    2.0 * geo.Radius <= max_d_mm * MM:
                faces.append(f)
    return faces


def remove_faces_by_fill(faces, label):
    """Apply Fill to each candidate face; Fill deletes the feature and
    heals the surrounding geometry. Per-face try/except: a feature that
    resists removal is REPORTED, never allowed to kill the run."""
    removed, failed = 0, 0
    for f in faces:
        try:
            sel = Selection.Create(f)
            Fill.Execute(sel)                          # VERIFY
            removed += 1
        except Exception:
            failed += 1
    log("%s: %d removed, %d failed of %d" % (label, removed, failed,
                                             len(faces)))
    return removed, failed


# --------------------------------- main ------------------------------------

def main():
    job = os.environ.get("SC_JOB_DIR")
    if not job:
        raise RuntimeError("SC_JOB_DIR not set")
    with open(os.path.join(job, "params.json")) as fh:
        p = json.load(fh)
    result = {"status": "ok", "backend": "spaceclaim-v201",
              "input": p["input"]}
    try:
        DocumentOpen.Execute(p["input"])               # VERIFY
        result["before"] = measure()
        DocumentSave.Execute(os.path.join(job, "before.png"))  # VERIFY

        deleted = delete_fastener_components(
            p.get("delete_components_matching", []),
            p.get("keep_components_matching", []))
        result["structure"] = measure()

        fil_removed = fil_failed = hol_removed = hol_failed = 0
        n_fil = n_hol = 0
        r_max = float(p.get("remove_fillets_below_r_mm", 0.0))
        if r_max > 0.0:
            faces = select_round_faces(r_max)
            n_fil = len(faces)
            fil_removed, fil_failed = remove_faces_by_fill(faces, "fillets")
        d_max = float(p.get("fill_holes_below_d_mm", 0.0))
        if d_max > 0.0:
            faces = select_small_hole_faces(d_max)
            n_hol = len(faces)
            hol_removed, hol_failed = remove_faces_by_fill(faces, "holes")

        result["after"] = measure()
        result["manifest"] = {
            "deleted_components": deleted,
            "fillets": {"selected": n_fil, "removed": fil_removed,
                        "failed": fil_failed},
            "holes": {"selected": n_hol, "filled": hol_removed,
                      "failed": hol_failed},
        }
        stp = os.path.join(job, "clean.stp")
        DocumentSave.Execute(stp)                      # VERIFY
        DocumentSave.Execute(os.path.join(job, "after.png"))
        result["exports"] = [stp]
    except Exception:
        result = {"status": "error", "backend": "spaceclaim-v201",
                  "input": p.get("input"),
                  "error": traceback.format_exc()}
    with open(os.path.join(job, "result.json"), "w") as fh:
        json.dump(result, fh, indent=2)
    with open(os.path.join(job, "log.txt"), "w") as fh:
        fh.write("\n".join(LOG))


main()
