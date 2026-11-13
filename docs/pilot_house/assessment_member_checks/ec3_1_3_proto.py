"""
EN 1993-1-3:2006 member-check PROTOTYPE for lipped C and plain U cold-formed sections.
FLIN-008 assessment (owner question: can the AI run all C/U member checks itself?).

Status: PROTOTYPE / PRELIMINARY (STATE D-007). Not a verified design tool. Every clause
reference is to EN 1993-1-3:2006 (E) unless prefixed 1-5 (EN 1993-1-5:2006) or 1-1
(EN 1993-1-1:2005), read from the owner's licensed PDFs in this session.

Conventions: centreline model, y horizontal (web at y = 0, flanges toward +y), z vertical
(symmetry axis y-y of the channel is z = 0). Units N, mm, MPa.
"""
from __future__ import annotations
import math
from dataclasses import dataclass, field

E_STEEL = 210000.0
NU = 0.3
G_STEEL = E_STEEL / (2 * (1 + NU))

# EN 1993-1-3 2(3): recommended partial factors (HU NA to be confirmed)
GAMMA_M0 = 1.00
GAMMA_M1 = 1.00


# ----------------------------------------------------------------------------- geometry
@dataclass
class Channel:
    """Lipped C (c > 0) or plain U (c = 0). Dimensions are OUTSIDE nominal dimensions.
    h total depth, b flange width, c lip length (outside), t core thickness, r internal radius."""
    name: str
    h: float
    b: float
    c: float
    t: float
    r: float
    fyb: float = 350.0

    # --- midline distances between midline intersection points X (Fig. 5.1)
    @property
    def hw(self) -> float:          # web height between flange midlines (6.1.5(1), 6.1.7.2)
        return self.h - self.t

    @property
    def bf_mid(self) -> float:      # flange midline length from web midline to lip midline
        return self.b - self.t

    @property
    def c_mid(self) -> float:       # lip midline length from flange midline to lip tip
        return self.c - self.t / 2 if self.c > 0 else 0.0

    @property
    def rm(self) -> float:          # midline radius, Fig. 5.1(a)
        return self.r + self.t / 2

    # --- notional flat widths bp measured to the corner midpoints P (Fig. 5.1):
    # bp = L_X - rm*sin(phi/2) per adjacent 90 deg corner  (gr = rm[tan(phi/2) - sin(phi/2)])
    @property
    def bp_w(self) -> float:
        return self.hw - 2 * self.rm * math.sin(math.pi / 4)

    @property
    def bp_f(self) -> float:
        n = 2 if self.c > 0 else 1
        return self.bf_mid - n * self.rm * math.sin(math.pi / 4)

    @property
    def bp_c(self) -> float:
        return self.c_mid - self.rm * math.sin(math.pi / 4) if self.c > 0 else 0.0

    def proportion_checks(self) -> dict:
        """5.2 Table 5.1 and (5.2a) lip range; 5.1(3) corner neglect; 5.1(6) radius limit;
        6.1.7.2(1) web-crippling applicability."""
        t = self.t
        out = {
            "b/t<=60 (lipped) or <=50 (plain) [Table 5.1]": (self.b / t, 60 if self.c > 0 else 50),
            "c/t<=50 [Table 5.1]": (self.c / t, 50),
            "h/t<=500 [Table 5.1]": (self.h / t, 500),
            "hw/t<=200 [6.14a]": (self.hw / t, 200),
            "r/t<=6 [6.14b]": (self.r / t, 6),
            "r<=0.04 t E/fy [5.1(6)]": (self.r, 0.04 * t * E_STEEL / self.fyb),
        }
        res = {k: (v[0], v[1], v[0] <= v[1] + 1e-9) for k, v in out.items()}
        if self.c > 0:
            cb = self.c / self.b
            res["0.2<=c/b<=0.6 [5.2a]"] = (cb, "0.2..0.6", 0.2 <= cb <= 0.6)
        res["corners negligible for resistance (r<=5t and r<=0.10 bp) [5.1(3)]"] = (
            self.r, min(5 * t, 0.10 * min(x for x in (self.bp_w, self.bp_f, self.bp_c) if x > 0)),
            self.r <= 5 * t and self.r <= 0.10 * min(x for x in (self.bp_w, self.bp_f, self.bp_c) if x > 0))
        return res

    # --- discretised midline polyline (arcs in n_arc segments) with per-segment thickness
    def polyline(self, n_arc: int = 8, t_lip: float | None = None, t_be2: float | None = None,
                 be2: float | None = None) -> list[tuple[float, float, float]]:
        """Returns a list of (y, z, t_segment_to_next) node tuples along the midline from the
        bottom lip tip, round the section, to the top lip tip. Optional reduced thickness for
        the stiffener parts (lip and the adjacent be2 of the flange) - used for effective props."""
        rm = self.rm
        hw, bf, cm = self.hw, self.bf_mid, self.c_mid
        pts: list[tuple[float, float]] = []

        def arc(cy, cz, a0, a1):
            for k in range(1, n_arc):
                a = a0 + (a1 - a0) * k / n_arc
                pts.append((cy + rm * math.cos(a), cz + rm * math.sin(a)))

        zt = hw / 2
        # bottom half, starting at the bottom lip tip
        if self.c > 0:
            pts.append((bf, -zt + cm))
            pts.append((bf, -zt + rm))
            arc(bf - rm, -zt + rm, 0.0, -math.pi / 2)          # lip -> flange corner
            pts.append((bf - rm, -zt))
        else:
            pts.append((bf, -zt))
        pts.append((rm, -zt))
        arc(rm, -zt + rm, -math.pi / 2, -math.pi)               # flange -> web corner
        pts.append((0.0, -zt + rm))
        pts.append((0.0, zt - rm))
        arc(rm, zt - rm, math.pi, math.pi / 2)                  # web -> flange corner
        pts.append((rm, zt))
        pts.append((bf - rm if self.c > 0 else bf, zt))
        if self.c > 0:
            arc(bf - rm, zt - rm, math.pi / 2, 0.0)             # flange -> lip corner
            pts.append((bf, zt - rm))
            pts.append((bf, zt - cm))
        # thickness per segment
        out = []
        for i, (y, z) in enumerate(pts):
            tt = self.t
            if t_lip is not None and i < len(pts) - 1:
                y2, z2 = pts[i + 1]
                ym, zm = (y + y2) / 2, (z + z2) / 2
                in_lip = abs(ym - bf) < 1e-6 or (abs(zm) > zt - rm - 1e-6 and ym > bf - rm - 1e-6)
                in_be2 = be2 is not None and abs(abs(zm) - zt) < 1e-6 and ym > bf - be2 - 1e-6
                if in_lip:
                    tt = t_lip
                elif in_be2 and t_be2 is not None:
                    tt = t_be2
            out.append((y, z, tt))
        return out


# ---------------------------------------------------------------- thin-walled section constants
@dataclass
class SectionProps:
    A: float
    yc: float
    zc: float
    Iy: float
    Iz: float
    Iyz: float
    It: float
    Iw: float
    ys: float       # shear centre, y
    zs: float       # shear centre, z
    y_min: float = 0.0
    y_max: float = 0.0
    z_min: float = 0.0
    z_max: float = 0.0

    @property
    def iy(self):
        return math.sqrt(self.Iy / self.A)

    @property
    def iz(self):
        return math.sqrt(self.Iz / self.A)


def line_props(nodes: list[tuple[float, float, float]]) -> SectionProps:
    """EN 1993-1-3 Annex C.1 formulas for an open thin-walled polyline (parts i = 1..n between
    nodes i-1 and i, thickness t_i). Sectorial quantities give the shear centre and Iw."""
    n = len(nodes) - 1
    dA, A = [], 0.0
    for i in range(1, n + 1):
        y0, z0, t = nodes[i - 1][0], nodes[i - 1][1], nodes[i - 1][2]
        y1, z1 = nodes[i][0], nodes[i][1]
        a = t * math.hypot(y1 - y0, z1 - z0)
        dA.append(a)
        A += a
    Sy0 = sum((nodes[i][1] + nodes[i - 1][1]) * dA[i - 1] / 2 for i in range(1, n + 1))
    Sz0 = sum((nodes[i][0] + nodes[i - 1][0]) * dA[i - 1] / 2 for i in range(1, n + 1))
    zgc, ygc = Sy0 / A, Sz0 / A
    Iy0 = sum((nodes[i][1] ** 2 + nodes[i - 1][1] ** 2 + nodes[i][1] * nodes[i - 1][1]) * dA[i - 1] / 3
              for i in range(1, n + 1))
    Iz0 = sum((nodes[i][0] ** 2 + nodes[i - 1][0] ** 2 + nodes[i][0] * nodes[i - 1][0]) * dA[i - 1] / 3
              for i in range(1, n + 1))
    Iyz0 = sum((2 * nodes[i - 1][0] * nodes[i - 1][1] + 2 * nodes[i][0] * nodes[i][1]
                + nodes[i - 1][0] * nodes[i][1] + nodes[i][0] * nodes[i - 1][1]) * dA[i - 1] / 6
               for i in range(1, n + 1))
    Iy = Iy0 - A * zgc ** 2
    Iz = Iz0 - A * ygc ** 2
    Iyz = Iyz0 - Sy0 * Sz0 / A
    # sectorial coordinates (pole = origin), C.1
    om = [0.0]
    for i in range(1, n + 1):
        om.append(om[-1] + nodes[i - 1][0] * nodes[i][1] - nodes[i][0] * nodes[i - 1][1])
    Iom = sum((om[i - 1] + om[i]) * dA[i - 1] / 2 for i in range(1, n + 1))
    Iyom0 = sum((2 * nodes[i - 1][0] * om[i - 1] + 2 * nodes[i][0] * om[i]
                 + nodes[i - 1][0] * om[i] + nodes[i][0] * om[i - 1]) * dA[i - 1] / 6 for i in range(1, n + 1))
    Izom0 = sum((2 * om[i - 1] * nodes[i - 1][1] + 2 * om[i] * nodes[i][1]
                 + om[i - 1] * nodes[i][1] + om[i] * nodes[i - 1][1]) * dA[i - 1] / 6 for i in range(1, n + 1))
    Iomom0 = sum((om[i] ** 2 + om[i - 1] ** 2 + om[i] * om[i - 1]) * dA[i - 1] / 3 for i in range(1, n + 1))
    Iyom = Iyom0 - Sz0 * Iom / A
    Izom = Izom0 - Sy0 * Iom / A
    Iomom = Iomom0 - Iom ** 2 / A
    det = Iy * Iz - Iyz ** 2
    # shear centre relative to the gravity centre (Annex C.1)
    ysc = (Izom * Iz - Iyom * Iyz) / det
    zsc = (-Iyom * Iy + Izom * Iyz) / det
    Iw = Iomom + zsc * Iyom - ysc * Izom
    It = sum(dA[i - 1] * nodes[i - 1][2] ** 2 / 3 for i in range(1, n + 1))
    # NOTE (QA Q1 finding): with the sectorial constants referred to the centroidal axes and the
    # pole at the origin, the Annex C result is the shear centre relative to the POLE (origin),
    # not to the gravity centre. Verified against the FE area model (sectionproperties).
    ys_abs, zs_abs = ysc, zsc
    ys_list = [p[0] for p in nodes]
    zs_list = [p[1] for p in nodes]
    return SectionProps(A, ygc, zgc, Iy, Iz, Iyz, It, Iw, ys_abs, zs_abs,
                        min(ys_list), max(ys_list), min(zs_list), max(zs_list))


def gross_props(sec: Channel) -> SectionProps:
    return line_props(sec.polyline())


def corner_delta(sec: Channel) -> float:
    """5.1(4) eq (5.1d): delta = 0.43 * sum(r_j phi_j/90) / sum(bp_i)."""
    n_corners = 4 if sec.c > 0 else 2
    bps = [sec.bp_w, sec.bp_f, sec.bp_f] + ([sec.bp_c, sec.bp_c] if sec.c > 0 else [])
    return 0.43 * n_corners * sec.r / sum(bps)



def lip_effective(sec: Channel) -> bool:
    """5.2(2): if c/b < 0.2 the lip is ignored (c = 0). Also guards a vanishing notional lip width."""
    return sec.c > 0 and sec.c / sec.b >= 0.2 and sec.bp_c > 0 and (sec.c_mid - sec.rm) > 0.5


def effective_polyline(sec: Channel, web_td: list, fl_top: list, fl_bot: list, lip_top: list, lip_bot: list,
                       t_corner_lip_top: float | None = None, t_corner_lip_bot: float | None = None,
                       n_arc: int = 8) -> list[tuple[float, float, float]]:
    """Rounded-midline polyline with piecewise thickness, for effective section properties incl. corners.
    Pieces are (length, thickness) lists along each FLAT part:
      web_td  - from the TOP end of the web flat downward (length Lw = hw - 2 rm)
      fl_top / fl_bot - from the web corner toward the lip (Lf = bf_mid - 2 rm for a C, - rm for a U)
      lip_top / lip_bot - from the flange corner toward the free tip (Lc = c_mid - rm)
    Corner arcs are fully effective (5.1); the flange-lip corners take the stiffener's reduced thickness."""
    rm, t = sec.rm, sec.t
    hw, bf, cm = sec.hw, sec.bf_mid, sec.c_mid
    zt = hw / 2
    lipped = lip_effective(sec)
    nodes: list[tuple[float, float, float]] = []

    def add(y, z, tt):
        nodes.append((y, z, tt))

    def arc(cy, cz, a0, a1, tt):
        for k in range(1, n_arc):
            a = a0 + (a1 - a0) * k / n_arc
            add(cy + rm * math.cos(a), cz + rm * math.sin(a), tt)

    def flat(p0, p1, pieces, reverse):
        """straight run from p0 to p1 with pieces listed from p0 (reverse=False) or from p1 (True)"""
        L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        ux, uz = (p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L
        seq = list(pieces)
        if reverse:
            seq = seq[::-1]
        s = 0.0
        for ln, tt in seq:
            if ln <= 1e-9:
                continue
            add(p0[0] + ux * s, p0[1] + uz * s, tt)
            s += ln
        # the last node of the run is added by the caller (start of the next run)

    tcl_t = t_corner_lip_top if t_corner_lip_top is not None else t
    tcl_b = t_corner_lip_bot if t_corner_lip_bot is not None else t
    if lipped:
        # bottom lip: tip -> corner
        flat((bf, -zt + cm), (bf, -zt + rm), lip_bot, reverse=True)
        add(bf, -zt + rm, tcl_b)
        arc(bf - rm, -zt + rm, 0.0, -math.pi / 2, tcl_b)
        add(bf - rm, -zt, None)              # thickness set by the flange run below
        nodes.pop()
        flat((bf - rm, -zt), (rm, -zt), fl_bot, reverse=True)
    else:
        flat((bf, -zt), (rm, -zt), fl_bot, reverse=True)
    add(rm, -zt, t)
    arc(rm, -zt + rm, -math.pi / 2, -math.pi, t)
    add(0.0, -zt + rm, t)
    flat((0.0, -zt + rm), (0.0, zt - rm), web_td, reverse=True)
    add(0.0, zt - rm, t)
    arc(rm, zt - rm, math.pi, math.pi / 2, t)
    add(rm, zt, t)
    if lipped:
        flat((rm, zt), (bf - rm, zt), fl_top, reverse=False)
        add(bf - rm, zt, tcl_t)
        arc(bf - rm, zt - rm, math.pi / 2, 0.0, tcl_t)
        add(bf, zt - rm, tcl_t)
        flat((bf, zt - rm), (bf, zt - cm), lip_top, reverse=False)
        add(bf, zt - cm, 0.0)
    else:
        flat((rm, zt), (bf, zt), fl_top, reverse=False)
        add(bf, zt, 0.0)
    return nodes


# ------------------------------------------------------------------ plate reduction (EN 1993-1-5)
def eps_(fy: float) -> float:
    return math.sqrt(235.0 / fy)


def lam_p(bp: float, t: float, ksig: float, fy: float) -> float:
    return (bp / t) / (28.4 * eps_(fy) * math.sqrt(ksig))


def rho_internal(lam: float, psi: float) -> float:        # 1-5 (4.2)
    if lam <= 0.673:
        return 1.0
    return min(1.0, (lam - 0.055 * (3 + psi)) / lam ** 2)


def rho_outstand(lam: float) -> float:                    # 1-5 (4.3)
    if lam <= 0.748:
        return 1.0
    return min(1.0, (lam - 0.188) / lam ** 2)


def ksig_internal(psi: float) -> float:                   # 1-5 Table 4.1
    if psi >= 1:
        return 4.0
    if psi > 0:
        return 8.2 / (1.05 + psi)
    if psi == 0:
        return 7.81
    if psi > -1:
        return 7.81 - 6.29 * psi + 9.78 * psi ** 2
    if psi == -1:
        return 23.9
    return 5.98 * (1 - psi) ** 2


def ksig_outstand_tip_comp(psi: float) -> float:          # 1-5 Table 4.2, max stress at the tip
    return 0.57 - 0.21 * psi + 0.07 * psi ** 2


def chi_d(lam_d: float) -> float:                         # (5.12a-c)
    if lam_d <= 0.65:
        return 1.0
    if lam_d < 1.38:
        return 1.47 - 0.723 * lam_d
    return 0.66 / lam_d


# ----------------------------------------------------------- edge stiffener, 5.5.3.2 (lipped C)
@dataclass
class Stiffener:
    be1: float
    be2: float
    ceff: float
    As: float
    Is: float
    b1: float
    K: float
    sigma_cr_s: float
    lam_d: float
    chi_d: float
    iterations: int
    t_red: float
    history: list = field(default_factory=list)


def edge_stiffener(sec: Channel, kf: float, gamma_m0: float = GAMMA_M0, max_iter: int = 50) -> Stiffener:
    """5.5.3.2 procedure for a single edge fold, compression flange at sigma_com = fyb/gM0.
    kf = 1 for pure compression (symmetric), 0 for bending about y-y (5.5.3.1(5))."""
    t, fy, E = sec.t, sec.fyb, E_STEEL
    bp, bpc, hw = sec.bp_f, sec.bp_c, sec.hw
    # Step 1 (5.5.3.2(4),(5)): flange as doubly supported, psi = 1; lip with ksig (5.13b/c)
    lam_f = lam_p(bp, t, 4.0, fy)
    ratio = bpc / bp
    if ratio <= 0.35:
        ks_c = 0.5
    elif ratio <= 0.6:
        ks_c = 0.5 + 0.83 * ((ratio - 0.35) ** 2) ** (1 / 3)
    else:
        raise ValueError("bp,c/bp > 0.6 outside (5.13c)")
    lam_c = lam_p(bpc, t, ks_c, fy)
    rho_f = rho_internal(lam_f, 1.0)
    be1 = 0.5 * rho_f * bp
    chi_prev, hist = 1.0, []
    chi = 1.0
    for it in range(1, max_iter + 1):
        red = math.sqrt(chi)                               # (5.16) lam_p,red = lam_p sqrt(chi_d)
        be2 = 0.5 * rho_internal(lam_f * red, 1.0) * bp if it > 1 else 0.5 * rho_f * bp
        ceff = rho_outstand(lam_c * red) * bpc
        As = t * (be2 + ceff)                              # (5.14a)
        # stiffener centroid: flange part at (y from bp-be2..bp, z = 0 ref flange line), lip hangs down ceff
        yc_s = (be2 * (bp - be2 / 2) + ceff * bp) / (be2 + ceff)
        zc_s = (be2 * 0.0 + ceff * (-ceff / 2)) / (be2 + ceff)
        # Is about axis a-a (parallel to the flange) through the stiffener centroid
        Is = (be2 * t ** 3 / 12 + be2 * t * zc_s ** 2) + (t * ceff ** 3 / 12 + ceff * t * (-ceff / 2 - zc_s) ** 2)
        b1 = yc_s                                          # from web-flange junction (midline) to stiffener centroid
        b2 = b1                                            # symmetric section
        K = E * t ** 3 / (4 * (1 - NU ** 2)) / (b1 ** 2 * hw + b1 ** 3 + 0.5 * b1 * b2 * hw * kf)   # (5.10b)
        sig = 2 * math.sqrt(K * E * Is) / As               # (5.15)
        lam_d = math.sqrt(fy / sig)                        # (5.12d)
        chi_new = chi_d(lam_d)
        hist.append((it, be2, ceff, As, Is, K, sig, lam_d, chi_new))
        if it > 1 and (abs(chi_new - chi) < 1e-4 or chi_new > chi):
            # 5.5.3.2 Fig 5.8e: continue until chi_n ~ chi_(n-1) but chi_n <= chi_(n-1)
            chi = min(chi, chi_new)
            break
        chi = chi_new
    t_red = t * chi                                         # (5.17),(12): As,red = chi_d As at sigma_com = fyb/gM0
    return Stiffener(be1, be2, ceff, As, Is, b1, K, sig, lam_d, chi, it, t_red, hist)


# ------------------------------------------------------------------- effective section, compression
@dataclass
class EffComp:
    Aeff: float
    eN: float            # shift of the centroid along y, positive = toward the web
    rho_w: float
    rho_f: float
    stiff: Stiffener | None
    lam_e_over_lam_e0_max: float
    detail: dict
    nodes: list = field(default_factory=list)


def effective_compression(sec: Channel) -> EffComp:
    """Aeff for uniform compression sigma_com = fyb/gM0 (6.1.3(1), 5.5). Effective section built on
    the rounded midline with the corners fully effective (5.1(1),(5))."""
    t, fy, rm = sec.t, sec.fyb, sec.rm
    g = gross_props(sec)
    lam_w = lam_p(sec.bp_w, t, 4.0, fy)
    rho_w = rho_internal(lam_w, 1.0)
    Lw = sec.hw - 2 * rm
    be_w = min(0.5 * rho_w * sec.bp_w, Lw / 2)
    web = [(be_w, t), (Lw - 2 * be_w, 0.0), (be_w, t)]
    ratios = [lam_w / 0.673]
    if lip_effective(sec):
        st = edge_stiffener(sec, kf=1.0)
        lam_f = lam_p(sec.bp_f, t, 4.0, fy)
        ratios += [lam_f / 0.673, st.lam_d / 0.65]
        Lf = sec.bf_mid - 2 * rm
        Lc = sec.c_mid - rm
        be1, be2 = min(st.be1, Lf / 2), min(st.be2, Lf / 2)
        fl = [(be1, t), (max(Lf - be1 - be2, 0.0), 0.0), (be2, st.t_red)]
        ce = min(st.ceff, Lc)
        lip = [(ce, st.t_red), (Lc - ce, 0.0)]
        nodes = effective_polyline(sec, web, fl, fl, lip, lip, st.t_red, st.t_red)
        rho_f = (st.be1 + st.be2) / sec.bp_f
        detail = dict(lam_w=lam_w, lam_f=lam_f)
    else:
        st = None
        lam_f = lam_p(sec.bp_f, t, 0.43, fy)                 # outstand flange, uniform compression
        rho_f = rho_outstand(lam_f)
        ratios += [lam_f / 0.748]
        Lf = sec.bf_mid - rm
        bf_eff = min(rho_f * sec.bp_f, Lf)
        fl = [(bf_eff, t), (Lf - bf_eff, 0.0)]
        nodes = effective_polyline(sec, web, fl, fl, [], [])
        detail = dict(lam_w=lam_w, lam_f=lam_f, bf_eff=bf_eff)
    pe = line_props(nodes)
    eN = g.yc - pe.yc
    return EffComp(pe.A, eN, rho_w, rho_f, st, max(ratios), detail, nodes)


# --------------------------------------------------------------- effective section, bending about y-y
@dataclass
class EffBend:
    Ieff: float
    zc: float            # NA depth below the compression-flange midline
    Weff_com: float
    Weff_ten: float
    psi: float
    rho_w: float
    stiff: Stiffener | None
    iterations: int
    detail: dict
    nodes: list = field(default_factory=list)


def effective_bending_y(sec: Channel, n_iter: int = 4) -> EffBend:
    """Weff for bending about y-y, compression at the top flange, sigma_max = fyb/gM0 (6.1.4.1(4)).
    Web stress ratio psi from the effective compression flange + gross web first, then refined on
    the effective section (5.5.2(3), 6.1.4.1(5)); at least two steps."""
    t, fy, rm, hw = sec.t, sec.fyb, sec.rm, sec.hw
    Lw = hw - 2 * rm
    lipped = lip_effective(sec)
    if lipped:
        st = edge_stiffener(sec, kf=0.0)
        Lf = sec.bf_mid - 2 * rm
        Lc = sec.c_mid - rm
        be1, be2 = min(st.be1, Lf / 2), min(st.be2, Lf / 2)
        fl_top = [(be1, t), (max(Lf - be1 - be2, 0.0), 0.0), (be2, st.t_red)]
        ce = min(st.ceff, Lc)
        lip_top = [(ce, st.t_red), (Lc - ce, 0.0)]
        fl_bot = [(Lf, t)]
        lip_bot = [(Lc, t)]
        tcl = st.t_red
    else:
        st = None
        lam_f = lam_p(sec.bp_f, t, 0.43, fy)
        Lf = sec.bf_mid - rm
        bf_eff = min(rho_outstand(lam_f) * sec.bp_f, Lf)
        fl_top = [(bf_eff, t), (Lf - bf_eff, 0.0)]
        fl_bot = [(Lf, t)]
        lip_top = lip_bot = []
        tcl = t
    web = [(Lw, t)]                                           # gross web for the first psi
    zc = psi = rho_w = float("nan")
    nodes = []
    hist = []
    for it in range(1, n_iter + 1):
        nodes = effective_polyline(sec, web, fl_top, fl_bot, lip_top, lip_bot, tcl, t)
        pe = line_props(nodes)
        zc = hw / 2 - pe.zc                                   # NA depth below the top flange midline
        psi = -(hw - zc) / zc
        ks = ksig_internal(psi)
        lam_w = lam_p(sec.bp_w, t, ks, fy)
        rho_w = rho_internal(lam_w, psi)
        beff = rho_w * zc                                     # Table 4.1: beff = rho * bc, bc = zc
        be1, be2 = 0.4 * beff, 0.6 * beff
        zc_flat = zc - rm                                     # compression depth on the web flat
        top = max(min(be1 - rm, zc_flat), 0.0)                # be1 measured from the flange midline
        bot_c = min(be2, zc_flat - top)
        hole = max(zc_flat - top - bot_c, 0.0)
        web = [(top, t), (hole, 0.0), (bot_c, t), (Lw - zc_flat, t)]
        hist.append(dict(it=it, zc=zc, psi=psi, ksig=ks, lam_w=lam_w, rho_w=rho_w, beff=beff, be1=be1, be2=be2))
    nodes = effective_polyline(sec, web, fl_top, fl_bot, lip_top, lip_bot, tcl, t)
    pe = line_props(nodes)
    zc = hw / 2 - pe.zc
    Ieff = pe.Iy
    Weff_com = Ieff / (zc + t / 2)
    Weff_ten = Ieff / (hw - zc + t / 2)
    return EffBend(Ieff, zc, Weff_com, Weff_ten, psi, rho_w, st, n_iter, dict(A_eff_bend=pe.A, hist=hist), nodes)


# ------------------------------------------------------------------------- resistances
def N_c_Rd(sec: Channel) -> float:                         # (6.2) (Aeff < Ag assumed for these sections)
    return effective_compression(sec).Aeff * sec.fyb / GAMMA_M0


def M_c_Rd_y(sec: Channel) -> float:                       # (6.4)
    eb = effective_bending_y(sec)
    return min(eb.Weff_com, eb.Weff_ten) * sec.fyb / GAMMA_M0


def V_b_Rd(sec: Channel, stiffened_support: bool = False) -> float:   # 6.1.5, Table 6.1
    sw = sec.hw                                             # vertical web, phi = 90 deg
    lam_w = 0.346 * sw / sec.t * math.sqrt(sec.fyb / E_STEEL)         # (6.10a)
    fy = sec.fyb
    if lam_w <= 0.83:
        fbv = 0.58 * fy
    elif lam_w < 1.40:
        fbv = 0.48 * fy / lam_w
    else:
        fbv = 0.48 * fy / lam_w if stiffened_support else 0.67 * fy / lam_w ** 2
    return sec.hw * sec.t * fbv / GAMMA_M0                  # (6.8), sin(phi) = 1


def R_w_Rd(sec: Channel, ss: float, near_free_end: bool) -> float:
    """6.1.7.2, single local load or support reaction, web rotation NOT prevented (Fig. 6.7a).
    near_free_end: c <= 1.5 hw. Stiffened flanges (lipped C) -> (6.15a) / (6.15d,e);
    unstiffened flanges (plain U) -> (6.15b,c) / (6.15d,e)."""
    t, fy, hw, r = sec.t, sec.fyb, sec.hw, sec.r
    k = fy / 228.0
    k1 = 1.33 - 0.33 * k
    k2 = min(1.0, max(0.5, 1.15 - 0.15 * r / t))
    k3 = 0.7 + 0.3 * (90 / 90) ** 2
    k4 = 1.22 - 0.22 * k
    k5 = min(1.0, 1.06 - 0.06 * r / t)
    sst = ss / t
    if near_free_end:
        if sec.c > 0:
            R = k1 * k2 * k3 * (9.04 - hw / t / 60) * (1 + 0.01 * sst) * t ** 2 * fy          # (6.15a)
        elif sst <= 60:
            R = k1 * k2 * k3 * (5.92 - hw / t / 132) * (1 + 0.01 * sst) * t ** 2 * fy         # (6.15b)
        else:
            R = k1 * k2 * k3 * (5.92 - hw / t / 132) * (0.71 + 0.015 * sst) * t ** 2 * fy     # (6.15c)
    else:
        if sst <= 60:
            R = k3 * k4 * k5 * (14.7 - hw / t / 49.5) * (1 + 0.007 * sst) * t ** 2 * fy       # (6.15d)
        else:
            R = k3 * k4 * k5 * (14.7 - hw / t / 49.5) * (0.75 + 0.011 * sst) * t ** 2 * fy    # (6.15e)
    return R / GAMMA_M1


# ------------------------------------------------------------------------- member buckling
def chi_curve(lam: float, alpha: float) -> float:          # 1-1 (6.49) / (6.56)
    phi = 0.5 * (1 + alpha * (lam - 0.2) + lam ** 2)
    return min(1.0, 1 / (phi + math.sqrt(max(phi ** 2 - lam ** 2, 0.0))))


ALPHA = {"a0": 0.13, "a": 0.21, "b": 0.34, "c": 0.49, "d": 0.76}   # 1-1 Table 6.1 / 6.3


@dataclass
class BucklingResult:
    Ncr_y: float
    Ncr_z: float
    Ncr_T: float
    Ncr_TF: float
    Ncr_min: float
    mode: str
    lam: float
    chi: float
    Nb_Rd: float


def N_b_Rd(sec: Channel, Ly: float, Lz: float, LT: float, curve: str = "b") -> BucklingResult:
    """6.2.2 / 6.2.3 with EN 1993-1-1 6.3.1.2; curve b for C-sections (Table 6.3, fyb used).
    Ncr,T (6.33a), Ncr,TF (6.35) for a section symmetric about y-y (zo = 0)."""
    g = gross_props(sec)
    E, G = E_STEEL, G_STEEL
    Aeff = effective_compression(sec).Aeff
    Ncr_y = math.pi ** 2 * E * g.Iy / Ly ** 2
    Ncr_z = math.pi ** 2 * E * g.Iz / Lz ** 2
    yo = g.ys - g.yc
    io2 = g.iy ** 2 + g.iz ** 2 + yo ** 2                   # (6.33b), zo = 0
    Ncr_T = (G * g.It + math.pi ** 2 * E * g.Iw / LT ** 2) / io2
    beta = 1 - (yo ** 2 / io2)
    Ncr_TF = Ncr_y / (2 * beta) * (1 + Ncr_T / Ncr_y - math.sqrt((1 - Ncr_T / Ncr_y) ** 2
                                                                 + 4 * (yo ** 2 / io2) * Ncr_T / Ncr_y))
    cands = {"flexural y": Ncr_y, "flexural z": Ncr_z, "torsional": Ncr_T, "torsional-flexural": Ncr_TF}
    mode = min(cands, key=cands.get)
    Ncr = cands[mode]
    lam = math.sqrt(Aeff * sec.fyb / Ncr)
    chi = chi_curve(lam, ALPHA[curve])
    return BucklingResult(Ncr_y, Ncr_z, Ncr_T, Ncr_TF, Ncr, mode, lam, chi, chi * Aeff * sec.fyb / GAMMA_M1)


def M_cr_y(sec: Channel, L: float, C1: float = 1.0, zg: float = 0.0, C2: float = 0.0) -> float:
    """Elastic critical moment, bending about y-y, section symmetric about y-y (zj = 0),
    fork supports, load at zg above the shear centre (zg > 0 destabilising)."""
    g = gross_props(sec)
    E, G = E_STEEL, G_STEEL
    a = math.pi ** 2 * E * g.Iz / L ** 2
    root = math.sqrt(g.Iw / g.Iz + L ** 2 * G * g.It / (math.pi ** 2 * E * g.Iz) + (C2 * zg) ** 2)
    return C1 * a * (root - C2 * zg)


def M_b_Rd_y(sec: Channel, L: float, C1: float = 1.0, curve: str = "b") -> tuple[float, float, float]:
    """6.2.4: EN 1993-1-1 6.3.2.2 with lateral buckling curve b. Returns (Mb_Rd, lam_LT, chi_LT)."""
    Weff = min(effective_bending_y(sec).Weff_com, effective_bending_y(sec).Weff_ten)
    Mcr = M_cr_y(sec, L, C1)
    lam_LT = math.sqrt(Weff * sec.fyb / Mcr)
    chi_LT = chi_curve(lam_LT, ALPHA[curve])
    return chi_LT * Weff * sec.fyb / GAMMA_M1, lam_LT, chi_LT


def interaction_6_36(NEd: float, Nb_Rd: float, MEd: float, Mb_Rd: float) -> float:
    return (NEd / Nb_Rd) ** 0.8 + (MEd / Mb_Rd) ** 0.8          # (6.36)


# ------------------------------------------------------------------------ elastic plate stresses
def sigma_cr_plate(bp: float, t: float, ksig: float) -> float:
    """1-5 (A.1): sigma_cr = ksig * pi^2 E t^2 / (12 (1-nu^2) bp^2) = ksig * 190000 (t/bp)^2."""
    return ksig * math.pi ** 2 * E_STEEL / (12 * (1 - NU ** 2)) * (t / bp) ** 2


if __name__ == "__main__":
    for s in (Channel("C150x45x10x1.5", 150, 45, 10, 1.5, 2.25),
              Channel("C200x60x15x2.0", 200, 60, 15, 2.0, 3.0),
              Channel("U150x45x1.5", 150, 45, 0, 1.5, 2.25)):
        g = gross_props(s)
        ec = effective_compression(s)
        eb = effective_bending_y(s)
        print(f"{s.name}: A={g.A:.1f} Iy={g.Iy/1e4:.2f}e4 Iz={g.Iz/1e4:.2f}e4 It={g.It:.0f} Iw={g.Iw/1e6:.2f}e6 "
              f"ys={g.ys:.2f} | Aeff={ec.Aeff:.1f} ({ec.Aeff/g.A:.3f}) Weff={min(eb.Weff_com, eb.Weff_ten)/1e3:.2f}e3 "
              f"NcRd={N_c_Rd(s)/1e3:.1f} kN McRd={M_c_Rd_y(s)/1e6:.2f} kNm VbRd={V_b_Rd(s)/1e3:.1f} kN")
