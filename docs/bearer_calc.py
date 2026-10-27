"""Bearer concept screening for FLINS-CFS-006: candidates under floor line load and screw-pile reactions.

Model: continuous bearer over piles at spacing s_p, floor tributary width B (one bay), loads g, q (kN/m2).
  w_d = (1.35 g + 1.5 q) B ;  M_Ed ~ w_d s_p^2 / 10 (continuous) ;  R_Ed ~ 1.1 w_d s_p (interior pile) ;  V_Ed ~ 0.6 w_d s_p
CFS candidates: bending M_Rd = n * W_EFF * W_gross * fy / gM0  (placeholder effective factor, as in the catalogue);
  web crippling per web, EN 1993-1-3:2006 eq. (6.15), category 2 (interior support, la = ss <= 200 mm), phi = 90 deg:
  R_w,Rd = alpha t^2 sqrt(fyb E) (1 - 0.1 sqrt(r/t)) (0.5 + sqrt(0.02 la/t)) (2.4 + (phi/90)^2) / gM1, alpha = 0.115
  interaction (6.28): M_Ed/M_c,Rd + R_Ed/R_w,Rd <= 1.25
Hot-rolled candidates: M_pl,Rd = W_pl fy / gM0 ; web crippling EN 1993-1-5 section 6 is not governing for these (checked as
  F_Rd ~ fy t_w (ss + 2 (t_f + r)) per web as a lower bound).
Deflection: continuous beam, delta ~ w_k s_p^4 / (185 E I) ; limit s_p / 350.
Bearer frequency with tributary mass m B (kg/m): f_b = (pi / 2 s_p^2) sqrt(E I / (m B)) ; floor system f by Dunkerley.
"""
from __future__ import annotations
import math
from floorframe import catalog

E, FY_CFS, GM0, GM1 = 210000.0, 350.0, 1.0, 1.0
W_EFF, I_EFF = 0.70, 0.85
SS = 150.0          # bearing length on the pile head plate, mm
HOT = {  # name: (W_pl cm3, I cm4, mass kg/m, t_w mm, t_f mm, r mm, fy, depth mm)
    "HEA 120": (119.5, 606, 19.9, 5.0, 8.0, 12, 355, 114),
    "HEA 140": (173.5, 1033, 24.7, 5.5, 8.5, 12, 355, 133),
    "RHS 150x100x5": (115.0, 739, 18.6, 5.0, 5.0, 7.5, 355, 150),
    "RHS 200x100x5": (185.0, 1522, 22.3, 5.0, 5.0, 7.5, 355, 200),
}


def cfs_crippling_per_web(t, r=None, la=SS, alpha=0.115, phi=90.0):
    r = 1.5 * t if r is None else r
    la = min(la, 200.0)
    return alpha * t**2 * math.sqrt(FY_CFS * E) * (1 - 0.1 * math.sqrt(r / t)) * (0.5 + math.sqrt(0.02 * la / t)) * (2.4 + (phi / 90) ** 2) / GM1 / 1000  # kN


def candidate_cfs(name, n=2):
    sec = catalog.section(name)
    return {"name": f"{n}x{name} {'back-to-back' if n == 2 else ''}".strip(), "M_Rd": n * W_EFF * sec.W_mm3 * FY_CFS / GM0 / 1e6,
            "R_w": n * cfs_crippling_per_web(sec.t), "I": n * I_EFF * sec.I_mm4, "mass": n * sec.mass_kg_m, "depth": sec.h, "kind": "CFS"}


def candidate_hot(name):
    Wpl, I, mass, tw, tf, r, fy, h = HOT[name]
    return {"name": name, "M_Rd": Wpl * 1e3 * fy / GM0 / 1e6, "R_w": 2 * fy * tw * (SS + 2 * (tf + r)) / 1000 if "RHS" in name else fy * tw * (SS + 2 * (tf + r)) / 1000,
            "I": I * 1e4, "mass": mass, "depth": h, "kind": "hot-rolled"}


def demands(s_p, B, g=1.5, q=2.0):
    w_d = (1.35 * g + 1.5 * q) * B; w_k = (g + q) * B
    return {"w_d": w_d, "w_k": w_k, "M_Ed": w_d * s_p**2 / 10, "R_Ed": 1.1 * w_d * s_p, "V_Ed": 0.6 * w_d * s_p}


def check(c, s_p, B, g=1.5, q=2.0, m_floor=60.0):
    d = demands(s_p, B, g, q)
    uM, uR = d["M_Ed"] / c["M_Rd"], d["R_Ed"] / c["R_w"]
    inter = uM + uR if c["kind"] == "CFS" else None
    delta = d["w_k"] * (s_p * 1000) ** 4 / (185 * E * c["I"]) if True else 0  # mm, w_k in kN/m = N/mm
    f_b = math.pi / (2 * s_p**2) * math.sqrt(E * c["I"] * 1e-6 / (m_floor * B))
    return {**d, "uM": uM, "uR": uR, "inter": inter, "delta": delta, "delta_lim": s_p * 1000 / 350, "f_b": f_b}


CANDIDATES = [candidate_cfs("C250-2.0"), candidate_cfs("C250-2.5"), candidate_cfs("C300-2.5"), candidate_hot("HEA 120"), candidate_hot("HEA 140"), candidate_hot("RHS 150x100x5")]

if __name__ == "__main__":
    for s_p in (2.0, 2.5, 3.0):
        print(f"--- pile spacing {s_p} m, bay 3.0 m, g=1.5 q=2.0 ->", {k: round(v, 1) for k, v in demands(s_p, 3.0).items()})
        for c in CANDIDATES:
            r = check(c, s_p, 3.0)
            print(f"{c['name']:28s} M_Rd {c['M_Rd']:6.1f} R_w {c['R_w']:6.1f} | uM {r['uM']:.2f} uR {r['uR']:.2f} inter {r['inter'] if r['inter'] is None else round(r['inter'],2)} | d {r['delta']:.1f}/{r['delta_lim']:.1f} mm | f_b {r['f_b']:.1f} Hz | {c['mass']:.1f} kg/m h={c['depth']}")
