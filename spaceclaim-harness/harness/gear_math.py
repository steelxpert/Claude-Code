"""Analytic expectations for an unshifted ISO metric spur gear.

Pure math, no SpaceClaim dependency. This is the ground truth the
verifier holds the CAD model against:
    pitch d  = m*z          tip da = m*(z+2)
    root df  = m*(z-2.5)    base db = d*cos(alpha)
"""
import math


def expectations(module, teeth, pressure_angle_deg=20.0, face_width=10.0,
                 bore_d=0.0):
    m = float(module)
    z = int(teeth)
    b = float(face_width)
    alpha = math.radians(float(pressure_angle_deg))
    d = m * z
    da = m * (z + 2.0)
    df = m * (z - 2.5)
    db = d * math.cos(alpha)
    if bore_d >= df:
        raise ValueError("bore %.3f >= root diameter %.3f" % (bore_d, df))

    area_root = math.pi / 4.0 * df ** 2
    area_tip = math.pi / 4.0 * da ** 2
    area_bore = math.pi / 4.0 * float(bore_d) ** 2
    # Teeth fill roughly half of the root->tip annulus, so the expected
    # volume sits mid-band; the hard gate is the [root, tip] envelope.
    v_min = (area_root - area_bore) * b
    v_max = (area_tip - area_bore) * b
    v_est = (area_root + 0.5 * (area_tip - area_root) - area_bore) * b

    return {
        "module": m, "teeth": z, "face_width": b,
        "pressure_angle_deg": float(pressure_angle_deg),
        "bore_d": float(bore_d),
        "pitch_d": d, "tip_d": da, "root_d": df, "base_d": db,
        "volume_min_mm3": v_min, "volume_max_mm3": v_max,
        "volume_est_mm3": v_est,
        "undercut_risk": z < 17,
    }
