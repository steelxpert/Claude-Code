"""QA runner for ec3_1_3_proto.py (FLIN-008 assessment). Writes QA_REPORT.md next to it.
Independent references used:
  (a) sectionproperties  - 2D FE area model of the rounded section (A, I, It, Iw, shear centre)
  (b) pycufsm (CUFSM)    - finite strip elastic buckling (local / distortional minima), CUTWP props
  (c) hand values        - EN 1993-1-1 buckling-curve spot values, closed-form plate stresses
  (d) AISI S100 DSM      - different design method, same elastic inputs (plausibility band only)
"""
import math, os, sys, warnings
import numpy as np
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(__file__))
import ec3_1_3_proto as ec

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = []


def w(s=""):
    OUT.append(s)
    print(s)


def pct(a, b):
    return 100 * (a / b - 1)


SECS = [ec.Channel("C150x45x10x1.5", 150, 45, 10, 1.5, 2.25),
        ec.Channel("C200x60x15x2.0", 200, 60, 15, 2.0, 3.0),
        ec.Channel("C200x60x15x2.5", 200, 60, 15, 2.5, 3.75),
        ec.Channel("U150x45x1.5", 150, 45, 0, 1.5, 2.25),
        ec.Channel("U150x40x2.0", 150, 40, 0, 2.0, 3.0)]

# ----------------------------------------------------------------------------- Q1 section constants
w("# QA report - EN 1993-1-3 prototype (FLIN-008)\n")
w("All sections S350GD (fyb = 350 MPa), E = 210 000 MPa, nu = 0.3, internal radius r = 1.5 t (ASSUMED, FLINS tooling unknown).\n")
w("## Q1  Gross section constants: three independent routes\n")
w("Route 1 = Annex C line model on the rounded midline (prototype). Route 2 = sharp-corner model with the 5.1(4) delta reduction. "
  "Route 3 = sectionproperties 2D finite-element area model of the real rounded outline (independent library). \n")
w("| section | quantity | route 1 | route 2 (5.1) | route 3 (FE) | r1/r3 - 1 | r2/r3 - 1 |")
w("|---|---|---|---|---|---|---|")

from shapely.geometry import LineString
from sectionproperties.pre import Geometry
from sectionproperties.analysis import Section
def sect_props_from(pts, t):
    g = ec.line_props([(x, y, t) for x, y in pts])
    return {"cx": g.yc, "cy": g.zc, "x0": g.ys, "y0": g.zs, "phi": 0.0, "A": g.A, "Ixx": g.Iy, "Ixy": g.Iyz,
            "Iyy": g.Iz, "I11": g.Iy, "I22": g.Iz, "Cw": g.Iw, "J": g.It, "B1": 0.0, "B2": 0.0, "wn": np.array([])}

Q1_PASS = True
for s in SECS:
    g = ec.gross_props(s)
    # route 2: sharp corners x delta
    sharp = ec.Channel(s.name, s.h, s.b, s.c, s.t, 0.0, s.fyb)
    sharp_rm0 = ec.line_props(sharp.polyline(n_arc=1))
    d = ec.corner_delta(s)
    r2 = dict(A=sharp_rm0.A * (1 - d), Iy=sharp_rm0.Iy * (1 - 2 * d), Iz=sharp_rm0.Iz * (1 - 2 * d),
              Iw=sharp_rm0.Iw * (1 - 4 * d), It=sharp_rm0.It * (1 - d))
    # route 3: FE area model from the buffered midline
    pts = [(p[0], p[1]) for p in s.polyline(n_arc=16)]
    poly = LineString(pts).buffer(s.t / 2, cap_style="flat", join_style="round", resolution=16)
    geom = Geometry(poly).create_mesh(mesh_sizes=[0.6])
    sec = Section(geom)
    sec.calculate_geometric_properties()
    sec.calculate_warping_properties()
    ixx, iyy, ixy = sec.get_ic()
    A3 = sec.get_area()
    J3 = sec.get_j()
    Iw3 = sec.get_gamma()
    xs3, ys3 = sec.get_sc()
    cx3, cy3 = sec.get_c()
    # route 4: CUTWP
    rows = [("A [mm2]", g.A, r2["A"], A3),
            ("Iy [mm4]", g.Iy, r2["Iy"], ixx),
            ("Iz [mm4]", g.Iz, r2["Iz"], iyy),
            ("It [mm4]", g.It, r2["It"], J3),
            ("Iw [mm6]", g.Iw, r2["Iw"], Iw3),
            ("ys - yc (shear centre) [mm]", g.ys - g.yc, float("nan"), xs3 - cx3)]
    for name, a, b, c3 in rows:
        da = pct(a, c3)
        db = pct(b, c3) if b == b else float("nan")
        flag = "" if abs(da) < 2.0 else " **CHECK**"
        if abs(da) >= 2.0 and "shear" not in name:
            Q1_PASS = False
        w(f"| {s.name} | {name} | {a:.4g} | {b:.4g} | {c3:.4g} | {da:+.2f} %{flag} | {db:+.2f} % |")
w(f"\nQ1 verdict: route 1 (prototype) vs independent FE area model within 2 % on all A, I, It, Iw: **{'PASS' if Q1_PASS else 'FAIL'}**. "
  "Route 2 (the 5.1(4) approximation) is shown for information; it is what a hand calculation would use.\n")

# ----------------------------------------------------------------------------- Q2 elastic buckling
w("## Q2  Elastic critical stresses: EN 1993-1-3 closed forms vs finite strip (CUFSM)\n")
w("Finite strip (pycufsm, signature curve, S-S) on the rounded midline. Local minimum compared with the EN 1993-1-5 plate "
  "formula for the governing element (web, kσ = 4, uniform compression); distortional minimum compared with σcr,s of (5.15). "
  "EN 1993-1-3 5.5.3.1(8) explicitly allows σcr,s from such a numerical analysis, so a mismatch is a finding, not a failure.\n")
from cufsm_qa import signature_curve

w("| section | case | CUFSM local min: L_cr / σcr,l | EN plate σcr (web, kσ) | ratio | CUFSM dist. min: L_cr / σcr,d | σcr,s (5.15) | ratio |")
w("|---|---|---|---|---|---|---|")
Q2 = {}
for s in SECS[:3] + [SECS[3]]:
    for mode in ("P", "M"):
        L, sig, mins, drange = signature_curve(s, mode)
        loc = mins[0] if mins else (float("nan"), float("nan"))
        dist = mins[1] if len(mins) > 1 else drange
        dist_note = "" if len(mins) > 1 else " (no distinct minimum; curve value in 2h..8h)"
        if mode == "P":
            ks = 4.0
            plate = ec.sigma_cr_plate(s.bp_w, s.t, ks)
            scs = ec.edge_stiffener(s, kf=1.0).sigma_cr_s if s.c > 0 else float("nan")
        else:
            eb = ec.effective_bending_y(s)
            ks = ec.ksig_internal(eb.psi)
            plate_web = ec.sigma_cr_plate(s.hw, s.t, ks)
            plate_fl = ec.sigma_cr_plate(s.bp_f, s.t, 4.0) if s.c > 0 else ec.sigma_cr_plate(s.bp_f, s.t, 0.43)
            plate = min(plate_web, plate_fl)
            scs = ec.edge_stiffener(s, kf=0.0).sigma_cr_s if s.c > 0 else float("nan")
        Q2[(s.name, mode)] = dict(loc=loc, dist=dist, plate=plate, scs=scs, distinct=len(mins) > 1)
        w(f"| {s.name} | {'compression' if mode == 'P' else 'bending y-y'} | {loc[0]:.0f} mm / {loc[1]:.0f} MPa | "
          f"{plate:.0f} MPa (kσ={ks:.2f}) | {loc[1] / plate:.2f} | {dist[0]:.0f} mm / {dist[1]:.0f} MPa{dist_note} | "
          f"{scs:.0f} MPa | {dist[1] / scs if scs == scs else float('nan'):.2f} |")
w("\nReading: ratio > 1 means the closed form is conservative against the finite strip. For the plain U in compression the "
  "second minimum is the flange-tip (outstand) mode, not a stiffener mode - no σcr,s exists.\n")

# ----------------------------------------------------------------------------- Q3 hand checks
w("## Q3  Hand checks of the formula layer\n")
hand = [
    ("χ(λ=1.0, curve b)", ec.chi_curve(1.0, 0.34), 0.5970, 1e-3),
    ("χ(λ=0.2, curve b)", ec.chi_curve(0.2, 0.34), 1.0, 1e-9),
    ("χ(λ=1.5, curve c)", ec.chi_curve(1.5, 0.49), 0.3145, 1e-3),
    ("ρ internal, λp=1.0, ψ=1 (1-5 4.2)", ec.rho_internal(1.0, 1.0), 0.78, 1e-9),
    ("ρ outstand, λp=1.0 (1-5 4.3)", ec.rho_outstand(1.0), 0.812, 1e-9),
    ("kσ internal ψ=-1 (Table 4.1)", ec.ksig_internal(-1.0), 23.9, 1e-9),
    ("kσ internal ψ=-0.5 (Table 4.1)", ec.ksig_internal(-0.5), 7.81 + 6.29 * 0.5 + 9.78 * 0.25, 1e-9),
    ("χd(λd=1.0) (5.12b)", ec.chi_d(1.0), 0.747, 1e-9),
    ("χd(λd=2.0) (5.12c)", ec.chi_d(2.0), 0.33, 1e-9),
    ("σcr plate web C150 kσ=4 = 4·190000·(t/bp)²", ec.sigma_cr_plate(SECS[0].bp_w, 1.5, 4.0),
     4 * math.pi ** 2 * 210000 / (12 * 0.91) * (1.5 / SECS[0].bp_w) ** 2, 1e-6),
]
w("| check | prototype | expected | ok |")
w("|---|---|---|---|")
Q3_PASS = True
for name, got, exp, tol in hand:
    ok = abs(got - exp) <= tol + 1e-12
    Q3_PASS &= ok
    w(f"| {name} | {got:.4f} | {exp:.4f} | {'PASS' if ok else 'FAIL'} |")
w(f"\nQ3 verdict: **{'PASS' if Q3_PASS else 'FAIL'}**\n")

# ----------------------------------------------------------------------------- Q4 internal consistency
w("## Q4  Internal consistency and limit behaviour\n")
Q4 = []
thick = ec.Channel("C150x45x20x4 (fictitious, stocky)", 150, 45, 20, 4.0, 6.0)
g = ec.gross_props(thick); ecp = ec.effective_compression(thick)
Q4.append(("stocky C150x45x20x4: Aeff/Ag >= 0.95 (web rho = %.3f, flanges and lip fully effective)" % ecp.rho_w,
           ecp.Aeff / g.A >= 0.95 and ecp.rho_f == 1.0, f"Aeff/Ag = {ecp.Aeff / g.A:.3f}"))
thick2 = ec.Channel("C150x45x20x6 (fictitious, very stocky)", 150, 45, 20, 6.0, 9.0)
Q4.append(("very stocky C150x45x20x6: Aeff = Ag", abs(ec.effective_compression(thick2).Aeff / ec.gross_props(thick2).A - 1) < 1e-6,
           f"Aeff/Ag = {ec.effective_compression(thick2).Aeff / ec.gross_props(thick2).A:.4f}"))
for cs, us in ((SECS[0], SECS[3]),):
    Q4.append((f"physical floor: Aeff({cs.name}) >= Aeff({us.name}) (a lip cannot weaken the flange)",
               ec.effective_compression(cs).Aeff >= ec.effective_compression(us).Aeff,
               f"{ec.effective_compression(cs).Aeff:.1f} >= {ec.effective_compression(us).Aeff:.1f}"))
stub = ec.Channel("C150x45x10x3 (stub lip, bp,c/bp = 0.13)", 150, 45, 10, 3.0, 4.5)
stub_u = ec.Channel("U150x45x3", 150, 45, 0, 3.0, 4.5)
Q4.append(("stub lip C150x45x10x3 vs U150x45x3: lipped not weaker than plain (FINDING if FAIL: 5.5.3.2 has no floor)",
           ec.effective_compression(stub).Aeff >= ec.effective_compression(stub_u).Aeff,
           f"{ec.effective_compression(stub).Aeff:.0f} vs {ec.effective_compression(stub_u).Aeff:.0f} mm2"))
for s in SECS:
    ecp = ec.effective_compression(s)
    eb = ec.effective_bending_y(s)
    gs = ec.gross_props(s)
    Wel = gs.Iy / (gs.z_max + s.t / 2)
    Q4.append((f"{s.name}: Aeff <= Ag", ecp.Aeff <= gs.A, f"{ecp.Aeff:.1f} <= {gs.A:.1f}"))
    Q4.append((f"{s.name}: Weff <= Wel", min(eb.Weff_com, eb.Weff_ten) <= Wel * 1.001, f"{min(eb.Weff_com, eb.Weff_ten):.0f} <= {Wel:.0f}"))
    # independent recomputation of Aeff from the piece list (sum of length x thickness + corner arcs)
    A_sum = sum(math.hypot(ecp.nodes[i + 1][0] - ecp.nodes[i][0], ecp.nodes[i + 1][1] - ecp.nodes[i][1]) * ecp.nodes[i][2]
                for i in range(len(ecp.nodes) - 1))
    Q4.append((f"{s.name}: Aeff from line_props = sum(piece length x t)", abs(A_sum - ecp.Aeff) < 1e-6, f"{ecp.Aeff:.2f} = {A_sum:.2f}; eN = {ecp.eN:+.2f} mm (+ toward the web)"))
    if s.c > 0:
        st = ecp.stiff
        Q4.append((f"{s.name}: stiffener iteration converged, χd,n <= χd,n-1", st.history[-1][-1] >= st.chi_d - 1e-6 and st.iterations < 50,
                   f"n = {st.iterations}, χd = {st.chi_d:.3f}, λd = {st.lam_d:.3f}, σcr,s = {st.sigma_cr_s:.0f} MPa"))
# monotonic in thickness
a = ec.N_c_Rd(ec.Channel("C150x45x10x1.5", 150, 45, 10, 1.5, 2.25))
b = ec.N_c_Rd(ec.Channel("C150x45x10x2.0", 150, 45, 10, 2.0, 3.0))
Q4.append(("Nc,Rd increases with t (1.5 -> 2.0 mm)", b > a, f"{a / 1e3:.1f} -> {b / 1e3:.1f} kN"))
# length monotonic
s0 = SECS[0]
nb = [ec.N_b_Rd(s0, L, 0.92e3, 0.92e3).Nb_Rd for L in (1500, 2750, 4000)]
Q4.append(("Nb,Rd decreases with Ly (bridging fixed at 0.92 m)", nb[0] > nb[1] > nb[2], " > ".join(f"{x / 1e3:.1f}" for x in nb) + " kN"))
w("| check | ok | detail |")
w("|---|---|---|")
Q4_PASS = all(x[1] for x in Q4)
for name, ok, det in Q4:
    w(f"| {name} | {'PASS' if ok else 'FAIL'} | {det} |")
w(f"\nQ4 verdict: **{'PASS' if Q4_PASS else 'FAIL'}**\n")

# ----------------------------------------------------------------------------- Q5 DSM plausibility
w("## Q5  Plausibility band: EN 1993-1-3 effective width method vs AISI S100 Direct Strength Method\n")
w("Same elastic inputs (CUFSM Pcrl, Pcrd; Ncr,TF from the prototype), different design method. Wall stud case: "
  "C150x45x10x1.5, Ly = 2.75 m (floor to roof), Lz = LT = 0.92 m (bridging rows), pinned, no sheathing. "
  "A DSM nominal within about ±20 % of the EN design value (γM1 = 1.0) is the expected band for lipped channels.\n")


def dsm_column(Py, Pcre, Pcrl, Pcrd):
    lc = math.sqrt(Py / Pcre)
    Pne = Py * (0.658 ** (lc ** 2)) if lc <= 1.5 else Py * 0.877 / lc ** 2
    ll = math.sqrt(Pne / Pcrl)
    Pnl = Pne if ll <= 0.776 else (1 - 0.15 * (Pcrl / Pne) ** 0.4) * (Pcrl / Pne) ** 0.4 * Pne
    ld = math.sqrt(Py / Pcrd)
    Pnd = Py if ld <= 0.561 else (1 - 0.25 * (Pcrd / Py) ** 0.6) * (Pcrd / Py) ** 0.6 * Py
    return Pne, Pnl, Pnd, min(Pne, Pnl, Pnd)


w("| section | Ly/Lz [m] | EN Nb,Rd [kN] (mode, λ, χ) | DSM Pne / Pnl / Pnd / Pn [kN] | Pn / Nb,Rd |")
w("|---|---|---|---|---|")
for s, Ly, Lz in ((SECS[0], 2750, 920), (SECS[0], 2750, 1380), (SECS[1], 2900, 2900), (SECS[2], 2600, 2600)):
    br = ec.N_b_Rd(s, Ly, Lz, Lz)
    g = ec.gross_props(s)
    Py = g.A * s.fyb
    q = Q2[(s.name, "P")]
    Pcrl, Pcrd = q["loc"][1] * g.A, q["dist"][1] * g.A
    Pne, Pnl, Pnd, Pn = dsm_column(Py, br.Ncr_min, Pcrl, Pcrd)
    note = "" if q["distinct"] else "*"
    w(f"| {s.name} | {Ly / 1e3:.2f} / {Lz / 1e3:.2f} | {br.Nb_Rd / 1e3:.1f} ({br.mode}, λ={br.lam:.2f}, χ={br.chi:.2f}) | "
      f"{Pne / 1e3:.1f} / {Pnl / 1e3:.1f} / {Pnd / 1e3:.1f}{note} / {Pn / 1e3:.1f} | {Pn / br.Nb_Rd:.2f} |")
w("\n\\* Pcrd taken from the signature-curve value in the 2h..8h range because no distinct distortional minimum exists for these narrow-flange sections.")
w("")

# ----------------------------------------------------------------------------- Q6 engineering numbers for the house
w("## Q6  First numbers for the house members (PRELIMINARY, D-007) - for orientation only\n")
w("| section | Nc,Rd | Mc,Rd,y | Vb,Rd | Rw,Rd end (ss=45) | Rw,Rd interior (ss=45) | Mb,Rd (L=0.92) | Mb,Rd (L=3.0, C1=1.13) | Nb,Rd (Ly 2.75 / Lz 0.92) |")
w("|---|---|---|---|---|---|---|---|")
for s in SECS:
    mb1 = ec.M_b_Rd_y(s, 920)[0]
    mb2 = ec.M_b_Rd_y(s, 3000, C1=1.13)[0]
    nb = ec.N_b_Rd(s, 2750, 920, 920).Nb_Rd
    w(f"| {s.name} | {ec.N_c_Rd(s) / 1e3:.1f} kN | {ec.M_c_Rd_y(s) / 1e6:.2f} kNm | {ec.V_b_Rd(s) / 1e3:.1f} kN | "
      f"{ec.R_w_Rd(s, 45, True) / 1e3:.2f} kN | {ec.R_w_Rd(s, 45, False) / 1e3:.2f} kN | {mb1 / 1e6:.2f} kNm | {mb2 / 1e6:.2f} kNm | {nb / 1e3:.1f} kN |")
w("\nLimits of applicability (5.2 Table 5.1, 5.2a, 5.1(3), 6.14):\n")
for s in SECS:
    pc = s.proportion_checks()
    bad = [k for k, v in pc.items() if not v[2]]
    w(f"- {s.name}: " + ("all satisfied" if not bad else "NOT satisfied: " + "; ".join(f"{k} (value {pc[k][0]:.3g}, limit {pc[k][1]})" for k in bad)))
w("")
w(f"\nOverall mechanical QA: Q1 {'PASS' if Q1_PASS else 'FAIL'}, Q3 {'PASS' if Q3_PASS else 'FAIL'}, Q4 {'PASS' if Q4_PASS else 'FAIL'}; "
  "Q2 and Q5 are comparisons against other methods and are read in the assessment memo.")

with open(os.path.join(HERE, "QA_REPORT.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(OUT) + "\n")
