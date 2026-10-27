"""Vibration screening numbers for the catalogue joists (used by the FLINS-CFS-005 note and its figure).

Simply supported single span, joist spacing s, floor mass m (kg/m2), effective EI = I_EFF * E * I_gross (placeholder reduction).
f1 = (pi / (2 L^2)) * sqrt(EI_per_m / m)              EN 1995-1-1 (7.5) with EI per metre width = E I / s
w_1kN = F L^3 / (48 EI_joist) * k_dist                  k_dist: share of a 1 kN point load carried by the loaded joist (deck load sharing)
"""
from __future__ import annotations
import math
from floorframe import catalog

I_EFF = 0.85
E = catalog.steel()["E"]  # MPa


def f1_hz(sec, L_m, s_mm, m_kg_m2):
    EI_m = E * I_EFF * sec.I_mm4 / (s_mm / 1000) * 1e-6  # N m2 per m width  (MPa*mm4 = N mm2 -> *1e-6 = N m2)
    return math.pi / (2 * L_m**2) * math.sqrt(EI_m / m_kg_m2)


def w_1kN_mm(sec, L_m, k_dist):
    EI = E * I_EFF * sec.I_mm4  # N mm2
    L = L_m * 1000
    return 1000 * L**3 / (48 * EI) * k_dist


def k_dist_ukna(sec, s_mm, EI_b_Nmm2_per_mm=None):
    """Load-sharing factor of the UK NA to EN 1995-1-1 (NA.2.6): k_dist = max(0.38 - 0.08 ln(14 (EI)_b / s^4), 0.30),
    (EI)_b in N mm2/mm (deck stiffness per mm width), s in mm. Placeholder deck: 22 mm OSB/3, E ~ 3500 MPa."""
    if EI_b_Nmm2_per_mm is None:
        EI_b_Nmm2_per_mm = 3500 * 22**3 / 12
    EI_b_kNm2_per_m = EI_b_Nmm2_per_mm * 1e-6  # kN m2 / m
    s_m = s_mm / 1000
    return max(0.38 - 0.08 * math.log(14 * EI_b_kNm2_per_m / s_m**4), 0.30)


def onysko_limit_mm(L_m):
    return 2.0 if L_m < 3.0 else 8.0 / L_m**1.3


if __name__ == "__main__":
    for name in ("C200-1.5", "C250-2.0", "C300-2.5"):
        sec = catalog.section(name)
        for L in (3.0, 3.6, 4.2, 4.8, 5.4):
            print(name, L, round(f1_hz(sec, L, 600, 60), 1), round(f1_hz(sec, L, 600, 110), 1), round(w_1kN_mm(sec, L, k_dist_ukna(sec, 600)), 2), round(onysko_limit_mm(L), 2))
