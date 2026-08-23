# Python Script, API Version = V18
# ---------------------------------------------------------------------------
# Runs INSIDE Ansys SpaceClaim 2020 R1 (v201) via:
#   SpaceClaim.exe /RunScript=<this file> /Headless=True /Splash=False
#                  /Welcome=False /ExitAfterScript=True
# with environment variable SC_JOB_DIR pointing at a job directory that
# contains params.json. Writes result.json, gear.stp, gear.png, log.txt.
#
# IronPython 2.7 — no numpy, no pip, no f-strings. Geometry passed to the
# SpaceClaim API is in METERS (mm * MM below).
#
# The GEOMETRY MATH section is exact and portable. The SPACECLAIM API
# section is a template written against the V18 API: on first run, repair
# any call marked VERIFY against a macro recorded in the GUI (Script
# editor records every manual action as V18 Python). See the
# spaceclaim-scripting skill for the bootstrap procedure.
# ---------------------------------------------------------------------------
import json
import math
import os
import traceback

MM = 0.001            # mm -> m for the SpaceClaim API
N_FLANK = 14          # points per involute flank polyline
LOG = []


def log(msg):
    LOG.append(msg)


# ============================ GEOMETRY MATH ================================

def involute(rb, r):
    """Polar angle swept by an involute of base radius rb at radius r."""
    a = math.acos(min(1.0, rb / r))
    return math.tan(a) - a


def gap_polygon(m, z, alpha_deg):
    """Closed polygon (mm, tooth frame) of ONE tooth gap, extended past
    the tip circle so an extrude-cut clears the blank rim.

    Frame: tooth 0 centered on +X axis; the gap sits between tooth 0 and
    tooth 1, centered at half the angular pitch.
    """
    alpha = math.radians(alpha_deg)
    rp = 0.5 * m * z                # pitch radius
    rb = rp * math.cos(alpha)       # base radius
    rt = 0.5 * m * (z + 2.0)        # tip radius
    rr = 0.5 * m * (z - 2.5)        # root radius
    r_cut = 1.15 * rt               # cut extends past the blank
    tau = 2.0 * math.pi / z         # angular pitch

    r_lo = max(rb, rr)              # involute undefined below base circle

    def half_thickness(r):
        # half angular tooth thickness at radius r (unshifted gear)
        return (math.pi * m) / (4.0 * rp) + involute(rb, rp) - involute(rb, r)

    # flank A: +side of tooth 0, root -> tip
    flank_a = []
    if rr < rb:                     # straight radial fill below base circle
        flank_a.append((rr, half_thickness(r_lo)))
    for i in range(N_FLANK + 1):
        r = r_lo + (rt - r_lo) * i / float(N_FLANK)
        flank_a.append((r, half_thickness(r)))
    # flank B: -side of tooth 1 (mirror of A about the gap center line)
    flank_b = [(r, tau - psi) for (r, psi) in flank_a]

    pts = []
    for (r, th) in flank_a:                       # up flank A
        pts.append((r * math.cos(th), r * math.sin(th)))
    th_a_top = flank_a[-1][1]
    th_b_top = flank_b[-1][1]
    pts.append((r_cut * math.cos(th_a_top), r_cut * math.sin(th_a_top)))
    for i in range(1, 4):                         # outer closing arc
        th = th_a_top + (th_b_top - th_a_top) * i / 3.0
        pts.append((r_cut * math.cos(th), r_cut * math.sin(th)))
    for (r, th) in reversed(flank_b):             # down flank B
        pts.append((r * math.cos(th), r * math.sin(th)))
    th_b_root = flank_b[0][1]
    th_a_root = flank_a[0][1]
    for i in range(1, 4):                         # root closing arc
        th = th_b_root + (th_a_root - th_b_root) * i / 3.0
        pts.append((rr * math.cos(th), rr * math.sin(th)))
    return pts


def rotated(pts, ang):
    c, s = math.cos(ang), math.sin(ang)
    return [(x * c - y * s, x * s + y * c) for (x, y) in pts]


# =========================== SPACECLAIM API ================================
# Everything below talks to the V18 API and carries VERIFY tags where the
# exact call signature should be confirmed against a recorded macro.

def sketch_polygon(pts_mm):
    """Draw a closed polyline on the XY sketch plane. VERIFY: SketchLine
    signature as recorded by the v201 Script editor."""
    n = len(pts_mm)
    for i in range(n):
        x1, y1 = pts_mm[i]
        x2, y2 = pts_mm[(i + 1) % n]
        if abs(x1 - x2) < 1e-12 and abs(y1 - y2) < 1e-12:
            continue
        SketchLine.Create(Point2D.Create(x1 * MM, y1 * MM),
                          Point2D.Create(x2 * MM, y2 * MM))


def solidify():
    """Leave sketch mode, turning closed sketch loops into faces."""
    ViewHelper.SetViewMode(InteractionMode.Solid)  # VERIFY


def newest_face():
    part = GetRootPart()
    if part.Bodies.Count > 0:
        body = part.Bodies[part.Bodies.Count - 1]
        return body.Faces[body.Faces.Count - 1]
    return None


def extrude_add(face, depth_mm):
    sel = Selection.Create(face)
    opts = ExtrudeFaceOptions()                    # VERIFY
    opts.ExtrudeType = ExtrudeType.Add
    ExtrudeFaces.Execute(sel, depth_mm * MM, opts)


def extrude_cut_through(face, depth_mm):
    sel = Selection.Create(face)
    opts = ExtrudeFaceOptions()                    # VERIFY
    opts.ExtrudeType = ExtrudeType.Cut
    ExtrudeFaces.Execute(sel, depth_mm * MM, opts)


def build_gear(p):
    m = float(p["module"])
    z = int(p["teeth"])
    alpha = float(p.get("pressure_angle_deg", 20.0))
    b = float(p.get("face_width", 10.0))
    bore = float(p.get("bore_d", 0.0))
    rt = 0.5 * m * (z + 2.0)
    tau = 2.0 * math.pi / z

    ClearAll()                                     # VERIFY: fresh document

    # 1) blank disk at tip radius, extruded to face width
    ViewHelper.SetSketchPlane(Plane.PlaneXY)       # VERIFY
    SketchCircle.Create(Point2D.Create(0.0, 0.0), rt * MM)
    solidify()
    extrude_add(newest_face(), b)
    log("blank ok r_tip=%.3f mm b=%.3f mm" % (rt, b))

    # 2) cut z tooth gaps (one profile, rotated z times — no pattern API
    #    needed, robust on V18; each cut is fast, the launch dominates)
    base_gap = gap_polygon(m, z, alpha)
    for k in range(z):
        ViewHelper.SetSketchPlane(Plane.PlaneXY)
        sketch_polygon(rotated(base_gap, k * tau))
        solidify()
        extrude_cut_through(newest_face(), 1.2 * b)
    log("cut %d gaps" % z)

    # 3) optional bore
    if bore > 0.0:
        ViewHelper.SetSketchPlane(Plane.PlaneXY)
        SketchCircle.Create(Point2D.Create(0.0, 0.0), 0.5 * bore * MM)
        solidify()
        extrude_cut_through(newest_face(), 1.2 * b)
        log("bore %.3f mm" % bore)


def measure():
    part = GetRootPart()
    n_bodies = part.Bodies.Count
    body = part.Bodies[0]
    vol_mm3 = body.Shape.Volume / (MM ** 3)        # VERIFY: Volume in m^3
    box = body.Shape.GetBoundingBox(Matrix.Identity)  # VERIFY
    bbox_mm = [(box.MaxCorner.X - box.MinCorner.X) / MM,
               (box.MaxCorner.Y - box.MinCorner.Y) / MM,
               (box.MaxCorner.Z - box.MinCorner.Z) / MM]
    return {"volume_mm3": vol_mm3, "bbox_mm": bbox_mm,
            "body_count": n_bodies}


def export(job):
    stp = os.path.join(job, "gear.stp")
    png = os.path.join(job, "gear.png")
    DocumentSave.Execute(stp)                      # VERIFY: STEP by extension
    DocumentSave.Execute(png)                      # VERIFY: PNG snapshot
    return [stp, png]


def main():
    job = os.environ.get("SC_JOB_DIR")
    if not job:
        raise RuntimeError("SC_JOB_DIR not set")
    with open(os.path.join(job, "params.json")) as fh:
        p = json.load(fh)
    result = {"status": "ok", "backend": "spaceclaim-v201"}
    try:
        build_gear(p)
        result.update(measure())
        result["tooth_count"] = int(p["teeth"])  # geometric count TODO:
        # derive from face topology once flank face naming is confirmed
        result["exports"] = export(job)
    except Exception:
        result = {"status": "error", "backend": "spaceclaim-v201",
                  "error": traceback.format_exc()}
    with open(os.path.join(job, "result.json"), "w") as fh:
        json.dump(result, fh, indent=2)
    with open(os.path.join(job, "log.txt"), "w") as fh:
        fh.write("\n".join(LOG))


main()
