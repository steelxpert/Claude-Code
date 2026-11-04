"""Structural detail figures for the FlexInSheet floor (Hungarian labels, indicative geometry).

The joints and the system are modelled as solids (CadQuery / OpenCascade) and drawn as
hidden-line projections: visible edges solid, hidden edges dashed. The build-ups, section
profiles and the framing plan are 2D drawings. Dimensions come from the development catalogue
and FLINS-CFS-002/004/006; values marked [ind.] are indicative placeholders, not design values.

    python docs/figures_details.py --out docs/figures/details
"""
from __future__ import annotations

import argparse
from pathlib import Path

import cadquery as cq
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Rectangle
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt, gp_Pnt2d
from OCP.HLRAlgo import HLRAlgo_Projector
from OCP.HLRBRep import HLRBRep_Algo, HLRBRep_HLRToShape

W, H, DPI = 12.8, 7.2, 150
NAVY, ORANGE, INK, MUTED = "#14213D", "#D9622B", "#1F2A3C", "#5A6577"
COL = {"cfs": "#C9D1DE", "cfs2": "#C9D1DE", "hot": "#8C9AAD"}
NOTE = "Indikatív részlet, nem kiviteli rajz. Folytonos vonal: látható él; szaggatott vonal: takart él."
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.unicode_minus": True})

X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
C200 = (200, 50, 15, 1.5)      # joist C200-1.5 (demo layout)
C300 = (300, 60, 18, 2.5)      # deepest catalogue section, bearer concept 1
HEA140 = (133, 140, 5.5, 8.5)  # bearer concept 2
RIM = (206, 60, 1.5)           # rim track [ind.]


# ---------------------------------------------------------------- profiles: (u, v) outlines, u = flange direction, v = height
def c_outline(h, b, c, t):
    return [(0, 0), (b, 0), (b, c), (b - t, c), (b - t, t), (t, t), (t, h - t), (b - t, h - t), (b - t, h - c), (b, h - c), (b, h), (0, h)]


def u_outline(h, b, t):
    return [(0, 0), (b, 0), (b, t), (t, t), (t, h - t), (b, h - t), (b, h), (0, h)]


def i_outline(h, b, tw, tf):
    return [(-b / 2, 0), (b / 2, 0), (b / 2, tf), (tw / 2, tf), (tw / 2, h - tf), (b / 2, h - tf), (b / 2, h), (-b / 2, h),
            (-b / 2, h - tf), (-tw / 2, h - tf), (-tw / 2, tf), (-b / 2, tf)]


def l_outline(a, b, t):
    """Angle: leg a along u, leg b along v."""
    return [(0, 0), (a, 0), (a, t), (t, t), (t, b), (0, b)]


# 2D rectangle lists for the section-profile figure
def c_rects(h, b, c, t, mirror=False):
    r = [(0, t, 0, h), (0, b, 0, t), (0, b, h - t, h), (b - t, b, t, c), (b - t, b, h - c, h - t)]
    return [(-u1, -u0, v0, v1) for u0, u1, v0, v1 in r] if mirror else r


def u_rects(h, b, t):
    return [(0, t, 0, h), (0, b, 0, t), (0, b, h - t, h)]


def i_rects(h, b, tw, tf):
    return [(-b / 2, b / 2, 0, tf), (-b / 2, b / 2, h - tf, h), (-tw / 2, tw / 2, tf, h - tf)]


def rhs_rects(h, b, t):
    return [(-b / 2, b / 2, 0, t), (-b / 2, b / 2, h - t, h), (-b / 2, -b / 2 + t, t, h - t), (b / 2 - t, b / 2, t, h - t)]


# ---------------------------------------------------------------- solids
class Model:
    def __init__(self):
        self.solids, self.labels = [], []

    def extrude(self, outline, origin, axis, eu, ev, length):
        """Extrude a (u, v) outline from origin along axis; eu, ev are the global directions of u and v."""
        a, eu, ev = np.array(axis, float), np.array(eu, float), np.array(ev, float)
        ydir = np.cross(a, eu)
        sgn = 1.0 if ydir @ ev > 0 else -1.0
        pl = cq.Plane(origin=tuple(map(float, origin)), xDir=tuple(eu), normal=tuple(a))
        wp = cq.Workplane(pl).polyline([(u, sgn * v) for u, v in outline]).close().extrude(float(length))
        self.solids.append(wp.val())
        return wp

    def box(self, x0, y0, z0, dx, dy, dz):
        self.solids.append(cq.Solid.makeBox(dx, dy, dz, pnt=cq.Vector(x0, y0, z0)))

    def cyl(self, base, axis, r, length):
        self.solids.append(cq.Solid.makeCylinder(r, length, pnt=cq.Vector(*base), dir=cq.Vector(*axis)))

    def add(self, shape):
        self.solids.append(shape)

    def tag(self, n, p, off=(30, 30)):
        self.labels.append((n, p, off))

    # members ------------------------------------------------------------
    def joist(self, x, y0, length, z0):
        """C200 along +y, web at x, flanges toward +x."""
        self.extrude(c_outline(*C200), (x, y0, z0), Y, X, Z, length)

    def boxed_bearer(self, x0, length, z0, y=0.0):
        """Two C300-2.5 toe to toe along x, centred on y."""
        h, b, c, t = C300
        self.extrude(c_outline(h, b, c, t), (x0, y - b, z0), X, Y, Z, length)
        self.extrude(c_outline(h, b, c, t), (x0, y + b, z0), X, (0, -1, 0), Z, length)

    def hea(self, x0, length, z0, y=0.0):
        self.extrude(i_outline(*HEA140), (x0, y, z0), X, Y, Z, length)

    def pile(self, x, y, length=450):
        self.cyl((x, y, -length), Z, 44.5, length)

    def cap_plate(self, x, y, slots, a=200, b=260, t=12):
        plate = (cq.Workplane("XY").box(a, b, t, centered=(True, True, False)).translate((x, y, 0))
                 .faces(">Z").workplane().pushPoints([(x + sx, y + sy) for sx, sy in slots]).slot2D(64, 14).cutThruAll())
        self.solids.append(plate.val())

    def bolt(self, x, y, z0, length=40, axis=Z):
        """Bolt with head at z0 + length (axis up) or at the given point for other axes."""
        a = np.array(axis, float)
        base = np.array((x, y, z0), float)
        self.cyl(tuple(base), tuple(a), 6, length)
        self.cyl(tuple(base + a * length), tuple(a), 12, 8)

    def screw(self, p, axis, length=20):
        """Self-drilling screw: shank into the part along axis, washer head at p."""
        p, a = np.array(p, float), np.array(axis, float)
        self.cyl(tuple(p), tuple(a), 2.75, length)
        self.cyl(tuple(p - a * 4), tuple(a), 7, 4)

    # drawing ------------------------------------------------------------
    def draw(self, ax, direction, hidden=True, lw=0.8):
        comp = cq.Compound.makeCompound(self.solids)
        n = np.array(direction, float); right = np.cross((0, 0, 1), n)          # screen x; screen y = n x right = world up
        proj = HLRAlgo_Projector(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(*n), gp_Dir(*right)))
        algo = HLRBRep_Algo(); algo.Add(comp.wrapped); algo.Projector(proj); algo.Update(); algo.Hide()
        h = HLRBRep_HLRToShape(algo)
        groups = [(h.VCompound(), dict(color=INK, lw=lw)), (h.OutLineVCompound(), dict(color=INK, lw=lw * 1.4)),
                  (h.Rg1LineVCompound(), dict(color=INK, lw=lw * 0.6))]
        if hidden:
            groups += [(h.HCompound(), dict(color="#9AA3AF", lw=lw * 0.6, ls=(0, (3, 2)))),
                       (h.OutLineHCompound(), dict(color="#9AA3AF", lw=lw * 0.6, ls=(0, (3, 2))))]
        xs, ys = [], []
        for shape, style in groups:
            if shape is None or shape.IsNull():
                continue
            for e in cq.Shape.cast(shape).Edges():
                pts = np.array([e.positionAt(u).toTuple() for u in np.linspace(0, 1, 2 if e.geomType() == "LINE" else 24)])
                ax.plot(pts[:, 0], pts[:, 1], solid_capstyle="round", **style)
                xs += list(pts[:, 0]); ys += list(pts[:, 1])
        ax.set_aspect("equal"); ax.axis("off")
        pad = 0.06 * max(max(xs) - min(xs), max(ys) - min(ys))
        ax.set_xlim(min(xs) - pad, max(xs) + pad); ax.set_ylim(min(ys) - pad, max(ys) + pad)
        for n, p, off in self.labels:
            q = gp_Pnt2d(); proj.Project(gp_Pnt(*map(float, p)), q)
            ax.plot(q.X(), q.Y(), "o", ms=4, color=ORANGE, zorder=10)
            ax.annotate(str(n), (q.X(), q.Y()), xytext=off, textcoords="offset points", fontsize=10.5, fontweight="bold",
                        color="white", ha="center", va="center", zorder=11,
                        bbox=dict(boxstyle="circle,pad=0.28", fc=ORANGE, ec="white", lw=1.2),
                        arrowprops=dict(arrowstyle="-", color=ORANGE, lw=1.3, shrinkA=0, shrinkB=0))


# ---------------------------------------------------------------- figure frame
def frame(title, items, n_axes=1, subtitles=None, note=NOTE):
    fig = plt.figure(figsize=(W, H), dpi=DPI)
    fig.patch.set_facecolor("#FFFFFF")
    fig.text(0.03, 0.94, title, fontsize=19, fontweight="bold", color=NAVY)
    fig.text(0.03, 0.025, note, fontsize=9, color=MUTED, style="italic")
    axes = []
    w = 0.66 / n_axes
    for i in range(n_axes):
        ax = fig.add_axes([0.015 + i * w, 0.07, w - 0.01, 0.78])
        if subtitles:
            fig.text(0.015 + i * w + w / 2, 0.875, subtitles[i], ha="center", fontsize=12.5, fontweight="bold", color=INK)
        axes.append(ax)
    legend(fig, items)
    return fig, axes


def legend(fig, items, x=0.69, top=0.86):
    fig.add_artist(FancyBboxPatch((x - 0.01, 0.07), 0.31, top - 0.03, boxstyle="round,pad=0.005", transform=fig.transFigure,
                                  fc="#F6F5F1", ec="#C9D1DE", lw=1))
    y = top - 0.03
    for n, text in items:
        lines = text.count("\n") + 1
        if n is None:
            fig.text(x, y, text, fontsize=10.5, fontweight="bold", color=NAVY, va="top", linespacing=1.25)
            y -= 0.02 + 0.026 * lines; continue
        fig.text(x + 0.008, y - 0.008, str(n), fontsize=9.5, fontweight="bold", color="white", ha="center", va="center",
                 bbox=dict(boxstyle="circle,pad=0.25", fc=ORANGE, ec="none"))
        fig.text(x + 0.025, y, text, fontsize=10, color=INK, va="top", linespacing=1.25)
        y -= 0.024 + 0.026 * lines


def save(fig, out, name):
    fig.savefig(out / name, dpi=DPI, facecolor=fig.get_facecolor())
    plt.close(fig)
    print("wrote", name)


# ---------------------------------------------------------------- hidden-line figures
ISO = (1.0, -1.25, 0.95)   # camera from +x, -y, above


def fig_system(out):
    m = Model()
    zb = 12                                   # bearer on the 12 mm cap plate
    zj = zb + C300[0]                         # joists bear on top of the bearers
    for yb in (60, 3060):                     # edge bearer (outer face at y = 0) and interior bearer
        for xp in (0, 2500):
            m.pile(xp, yb, 500); m.cap_plate(xp, yb, [(-40, -105), (40, -105), (-40, 105), (40, 105)])
        m.boxed_bearer(-150, 2950, zb, y=yb)
    m.extrude(u_outline(*RIM), (-150, 0, zj), X, Y, Z, 2950)                        # rim track on the edge bearer
    for xj in range(100, 2700, 600):
        m.joist(xj, 1.5, 4300, zj + 1.5)                                            # continuous over the interior bearer
    m.box(1300, 1600, zj + 1.5 + 200, 1500, 2700, 22)                               # OSB deck on top of the joists (part)
    m.tag(1, (0, 60, -350), (-40, -10)); m.tag(2, (2500, -70, 12), (40, -20)); m.tag(3, (1900, 0, zb + 150), (20, -40))
    m.tag(4, (700, 2200, zj + 150), (-30, 30)); m.tag(5, (500, 0, zj + 150), (-35, 25)); m.tag(6, (2400, 3500, zj + 223), (35, 25))
    m.tag("A", (-90, 60, 12), (-45, 25)); m.tag("B", (700, 3060, zj + 30), (-35, 35)); m.tag("C", (1300, 0, zj + 100), (0, 45))
    m.tag("D", (625, 0, zb + 60), (-15, -45))
    fig, (ax,) = frame("1. ábra: A födémrendszer felépítése (sarokrészlet)", [
        (None, "Elemek (alulról felfelé)"),
        (1, "Csavarcölöp SP89-2500\n(szárátmérő Ø89 mm, csavarlevél Ø300 mm)"),
        (2, "Cölöpfejlemez ±25 mm-es hosszlyukakkal"),
        (3, "Főtartó; 1. változat: 2×C300-2,5 zárt\nszelvénypár, 2. változat: HEA 140 (3. ábra)"),
        (4, "C200-1,5 födémgerenda 600 mm-es\ntengelytávolsággal, a főtartókra felfekszik"),
        (5, "U-szelvényű peremprofil a gerendavégeken"),
        (6, "OSB födémlap a gerendák felső övén\n(részlegesen ábrázolva)"),
        (None, "Csomópontok"),
        ("A", "Főtartó–cölöpfej (3. ábra)"),
        ("B", "Födémgerenda–közbenső főtartó (4. ábra)"),
        ("C", "Födémgerenda–peremprofil (5. ábra)"),
        ("D", "Főtartótoldás a negyedpontban (6. ábra)"),
    ], note="Indikatív részlet, nem kiviteli rajz. A takart élek nincsenek ábrázolva.")
    m.draw(ax, ISO, hidden=False, lw=0.6)
    save(fig, out, "D01_rendszer.png")


def pile_head(concept):
    m = Model()
    m.pile(0, 0, 450)
    if concept == 1:
        h, b, c, t = C300
        m.cap_plate(0, 0, [(-30, -105), (30, -105), (-30, 105), (30, 105)])
        m.boxed_bearer(-450, 900, 12)
        for side in (-1, 1):
            # bearing stiffener: short vertical C stud nested against each web (web along x, flanges toward the centre)
            m.extrude(c_outline(150, 40, 10, 1.5), (-75, side * (b - t), 12 + t), Z, (0, -side, 0), X, h - 2 * t)
            # seat angle 80x80x6 on the plate against the outer web face, 120 long
            m.extrude(l_outline(80, 80, 6), (-60, side * b, 12), X, (0, side, 0), Z, 120)
            for dx in (-30, 30):
                m.bolt(dx, side * 105, 12, 14)
                for zz in (45, 70):
                    m.screw((dx, side * (b + 6), 12 + zz), (0, -side, 0), 14)
        m.tag(1, (0, -44.5, -250), (-35, 0)); m.tag(2, (95, 120, 12), (45, 10)); m.tag(3, (-420, -b, 250), (-30, 30))
        m.tag(4, (75, b - t - 20, 200), (45, 35)); m.tag(5, (30, -105, 26), (40, -30)); m.tag(6, (-60, -b - 40, 6 + 12), (-40, -25))
    else:
        m.cap_plate(0, 0, [(-60, -45), (60, -45), (-60, 45), (60, 45)])
        m.hea(-450, 900, 12)
        for dx in (-60, 60):
            for dy in (-45, 45):
                m.bolt(dx, dy, 12, 8.5 + 14)
        m.tag(1, (0, -44.5, -250), (-35, 0)); m.tag(2, (100, -130, 12), (40, -25)); m.tag(3, (-420, -70, 120), (-30, 30))
        m.tag(7, (60, -45, 12 + 8.5 + 22), (40, -30))
    return m


def fig_pile_head(out):
    fig, axes = frame("3. ábra: Főtartó–cölöpfej csomópont (A)", [
        (None, "Közös elemek"),
        (1, "Csavarcölöp, szárátmérő Ø89 mm"),
        (2, "Cölöpfejlemez, a főtartó irányában ≥150 mm,\n±25 mm-es hosszlyukakkal [ind. 200×260×12]"),
        (3, "Főtartó, legalább két cölöpön átmenő"),
        (None, "1. változat: hidegen hajlított"),
        (4, "Teherátadó merevítő mindkét gerinclemeznél:\nrövid C-szelvény a zárt szelvényen belül (takart)"),
        (5, "Csavarok a fejlemezbe; önfúró csavarok\na szögacélon át a gerinclemezbe"),
        (6, "Rögzítő szögacél mindkét oldalon [ind. L80×80×6]"),
        (None, "2. változat: melegen hengerelt"),
        (7, "4 db csavar az alsó övön át, hosszlyukban"),
        (None, "Kísérleti vizsgálat: T5 (nyomás, kiemelés,\nnyírás, külpontosság); merevítő: T2b"),
    ], n_axes=2, subtitles=["1. változat: 2×C300-2,5 zárt szelvénypár", "2. változat: HEA 140, tűzihorganyzott"])
    pile_head(1).draw(axes[0], ISO); pile_head(2).draw(axes[1], ISO)
    save(fig, out, "D03_colopfej.png")


def joist_bearer(concept):
    """Joists bear on top of the bearer; an L clip sits on the joist bottom flange inside the C (open side, +x)."""
    m = Model()
    if concept == 1:
        m.boxed_bearer(-450, 900, 0); top = C300[0]; face = -C300[1]
    else:
        m.hea(-450, 900, 0); top = HEA140[0]; face = -HEA140[1] / 2
    for xj in (-300, 300):
        m.joist(xj, -400, 800, top)
        zf = top + 1.5                                                        # top of the joist bottom flange
        m.extrude(l_outline(40, 64, 4), (xj + 1.5, -40, zf), Y, X, Z, 80)     # clip: leg on the flange, leg on the web
        for dy in (-20, 20):
            if concept == 1:
                m.screw((xj + 28, dy, zf + 4), (0, 0, -1), 22)                # through clip, joist flange and bearer flange
            else:
                m.bolt(xj + 28, dy, zf + 4 - 30, 30)                          # bolt through the HEA top flange
            m.screw((xj + 5.5, dy, zf + 40), (-1, 0, 0), 12)                  # through the clip into the joist web
    m.tag(1, (0, face, top * 0.35), (-20, -45)); m.tag(2, (-300 + 40, 360, top + 200), (30, 30))
    m.tag(3, (300 + 40, 40, top + 5), (45, 25)); m.tag(4, (300 + 28, -20, top + 6), (45, -30))
    return m


def fig_joist_bearer(out):
    fig, axes = frame("4. ábra: Gerenda–főtartó csomópont (B)", [
        (None, "Elemek"),
        (1, "Főtartó (1.: 2×C300-2,5 zárt szelvénypár;\n2.: HEA 140)"),
        (2, "C200-1,5 födémgerenda, a főtartóra\nfelfekszik, azon folytatólagosan átmegy"),
        (3, "Kapcsolószögacél a gerenda alsó övén,\na C-szelvény nyitott oldalán [ind. 40×64×4]"),
        (4, "Kötőelemek: önfúró csavar a gerinclemezbe;\n1.: önfúró csavar mindkét övön át,\n2.: csavar a HEA felső övén át"),
        (None, "Kísérleti vizsgálat: T4 (gerendabekötések);\na kapcsolat elcsúszása befolyásolja\na födém merevségét és rezgését"),
    ], n_axes=2, subtitles=["1. változat: 2×C300-2,5 zárt szelvénypár", "2. változat: HEA 140"])
    joist_bearer(1).draw(axes[0], ISO); joist_bearer(2).draw(axes[1], ISO)
    save(fig, out, "D04_gerenda_fotarto.png")


def fig_joist_rim(out):
    """Rim track on the edge bearer (outer face at y = 0); joists end in the track. Viewed from inside the floor."""
    m = Model()
    m.boxed_bearer(-400, 950, -C300[0], y=C300[1])
    m.extrude(u_outline(*RIM), (-400, 0, 0), X, Y, Z, 950)
    for xj in (-200, 300):
        m.joist(xj, 1.5, 700, 1.5)
        # clip angle inside the C: one leg on the rim web, one on the joist web
        m.extrude(l_outline(45, 70, 4), (xj + 1.5, 1.5, 30), Z, X, Y, 140)
        # web stiffener at the joist end on the outer face of the joist web: short vertical C stud
        m.extrude(c_outline(60, 40, 10, 1.5), (xj, 1.5, 3), Z, (-1, 0, 0), Y, 196)
        for zz in (70, 130):
            m.screw((xj + 30, 0, 30 + zz - 30), (0, 1, 0), 14)                # through the rim web into the clip
            m.screw((xj + 5.5, 45, 30 + zz - 30), (-1, 0, 0), 12)             # through the clip into the joist web
        m.screw((xj + 25, 25, 206), (0, 0, -1), 18)                           # rim flange into joist flange
    m.tag(1, (500, 120, -150), (40, -15)); m.tag(2, (-350, 30, 206), (-35, 30)); m.tag(3, (300 + 25, 650, 201.5), (30, 25))
    m.tag(4, (325, 25, 210), (25, 40)); m.tag(5, (-200 - 40, 30, 120), (-45, -20)); m.tag(6, (300 + 25, 5.5, 160), (45, 25))
    fig, (ax,) = frame("5. ábra: Gerenda–peremprofil csomópont (C)", [
        (None, "Elemek (nézet a födém belseje felől)"),
        (1, "Szélső főtartó a cölöpsoron"),
        (2, "U-szelvényű peremprofil a főtartón\n[ind. U206-1,5]"),
        (3, "C200-1,5 födémgerenda, vége\na peremprofilba illeszkedik"),
        (4, "Önfúró csavar a peremprofil övén át\na gerenda övébe"),
        (5, "Gerinchorpadás elleni merevítő a gerendavégen\n(szükség szerint, AISI S240-15, B2.5)"),
        (6, "Kapcsolószögacél [ind. 45×70×4], csavarozva\na gerenda és a peremprofil gerinclemezéhez"),
        (None, "Vizsgált kialakítások (T4): szögacél,\nkihajtott fül, bemetszett gerendavég"),
    ])
    m.draw(ax, (1.0, 1.4, 1.9))
    save(fig, out, "D05_gerenda_perem.png")


def splice(concept):
    m = Model()
    xs, x_end = 625, 1500                    # splice at L/4 for a 2,5 m pile spacing; bearer drawn to 1,5 m
    m.pile(0, 0, 350)
    if concept == 1:
        h, b = C300[0], C300[1]
        m.cap_plate(0, 0, [(-30, -105), (30, -105), (-30, 105), (30, 105)])
        m.boxed_bearer(-300, xs + 300 - 3, 12); m.boxed_bearer(xs + 3, x_end - xs - 3, 12)
        for side in (-1, 1):                 # cover plates on both outer web faces, screwed
            m.box(xs - 300, side * b if side > 0 else -b - 4, 12 + 30, 600, 4, h - 60)
            for dx in (-240, -160, -80, 80, 160, 240):
                for zz in (90, 210):
                    m.screw((xs + dx, side * (b + 4), 12 + zz), (0, -side, 0), 12)
        m.tag(3, (xs, -b - 4, 12 + 150), (0, -50))
    else:
        h = HEA140[0]
        m.cap_plate(0, 0, [(-60, -45), (60, -45), (-60, 45), (60, 45)])
        m.hea(-300, xs + 300 - 3, 12); m.hea(xs + 3, x_end - xs - 3, 12)
        for side in (-1, 1):                 # web cover plates both sides, bolted
            m.box(xs - 200, 2.75 if side > 0 else -10.75, 12 + 20, 400, 8, h - 40)
            for dx in (-150, -60, 60, 150):
                if side < 0:
                    m.bolt(xs + dx, -10.75, 12 + h / 2, 30, axis=(0, -1, 0))
        m.box(xs - 200, -70, 12 + h, 400, 140, 8)                                 # flange cover plate
        m.tag(3, (xs, -10.75, 12 + h / 2), (0, -50))
    m.tag(1, (0, -44.5, -200), (-35, 0)); m.tag(2, (1200, 0, 12 + (C300[0] if concept == 1 else HEA140[0])), (20, 35))
    return m


def fig_splice(out):
    fig, axes = frame("6. ábra: Főtartó folytatólagossága és toldása (D)", [
        (None, "Kialakítási szabályok (FLINS-CFS-006)"),
        (1, "Cölöp; cölöptávolság 2,0–3,0 m\n(az ábrán 2,5 m, a toldás 625 mm-re)"),
        (2, "A főtartó legalább két cölöpön\nát folytatólagos"),
        (3, "Toldás a negyedpontban (L/4-re a cölöptől),\nahol a hajlítónyomaték kicsi"),
        (None, "1.: kétoldali hevederlemez önfúró\ncsavarokkal [ind.]; 2.: csavarozott\ngerinc- és övheveder [ind.]"),
    ], n_axes=2, subtitles=["1. változat: 2×C300-2,5 zárt szelvénypár", "2. változat: HEA 140"])
    splice(1).draw(axes[0], (0.9, -1.4, 0.8)); splice(2).draw(axes[1], (0.9, -1.4, 0.8))
    save(fig, out, "D06_toldas.png")


# ---------------------------------------------------------------- build-ups: 2D sections across the joists
def section(ax, layers, width=600, wool="full"):
    """2D section across two C200 joists; layers top-down as (label, t, fill, hatch); fill None = joist zone."""
    total = sum(t for _, t, _, _ in layers)
    z = total
    ylab = np.linspace(total + 160, -160, len(layers))
    for (name, t, fc, hatch), yl in zip(layers, ylab):
        z0 = z - t
        if fc is None:                          # joist zone, with mineral wool full depth or in the upper part only
            ax.add_patch(Rectangle((0, z0), width, t, fc="white", ec=INK, lw=0.6))
            if wool == "full":
                ax.add_patch(Rectangle((0, z0), width, t, fc="#F6EEC8", ec=INK, lw=0.6, hatch="oo"))
            elif wool == "upper":
                ax.add_patch(Rectangle((0, z0 + t - 100), width, 100, fc="#F6EEC8", ec=INK, lw=0.6, hatch="oo"))
            for xc in (100, 500):
                ax.add_patch(Rectangle((xc - 25, z0), 50, t, fc="white", ec="none"))
                for u0, u1, v0, v1 in c_rects(C200[0], C200[1], C200[2], 3):
                    ax.add_patch(Rectangle((xc - 25 + u0, z0 + v0), u1 - u0, v1 - v0, fc=INK, ec="none"))
        else:
            ax.add_patch(Rectangle((0, z0), width, t, fc=fc, ec=INK, lw=0.6, hatch=hatch))
        ax.plot([width, width + 60, width + 110], [z0 + t / 2, z0 + t / 2, yl], color=MUTED, lw=0.7)
        ax.text(width + 125, yl, name, fontsize=10, color=INK, va="center", linespacing=1.2)
        z = z0
    ax.annotate("", (-40, 0), (-40, total), arrowprops=dict(arrowstyle="<->", lw=0.8, color=MUTED))
    ax.text(-55, total / 2, f"≈ {total:g} mm".replace(".", ","), rotation=90, ha="right", va="center", fontsize=10, color=MUTED)
    ax.set_xlim(-130, width + 900); ax.set_ylim(-260, total + 220)
    return total


def fig_fire(out):
    fig = plt.figure(figsize=(W, H), dpi=DPI)
    fig.patch.set_facecolor("#FFFFFF")
    fig.text(0.03, 0.94, "9. ábra: Tűzvédelmi rétegrendek alulról érő tűzhatásra", fontsize=19, fontweight="bold", color=NAVY)
    fig.text(0.03, 0.025, "Előtervezési ökölszabály (SCI P402, 2.2.2), nem osztályba sorolás. A minősítés osztályba sorolt gyártói "
             "rendszerből vagy MSZ EN 1365-2 szerinti vizsgálatból származik (FLINS-CFS-004).", fontsize=9, color=MUTED, style="italic")
    deck = ("Nútféderes födémlap, 18 mm\n(OSB vagy forgácslap)", 18, "#E9D9B8", "////")
    joists = ("C200-1,5 gerendák; az ásványgyapot nem\na tűz felőli (alsó) övre fekszik [ind.]", 200, None, None)
    b1 = ("Tűzgátló gipszkarton, 12,5 mm", 12.5, "#F3D9D0", "...")
    b2 = ("2. réteg tűzgátló gipszkarton, 12,5 mm,\neltolt illesztésekkel", 12.5, "#F3D9D0", "xxx")
    for k, (layers, sub) in enumerate([([deck, joists, b1], "REI 30 (pl. családi ház; ellenőrizendő)"),
                                       ([deck, joists, b2, b1], "REI 60 (lakáselválasztó födém)")]):
        ax = fig.add_axes([0.03 + k * 0.49, 0.30, 0.46, 0.56]); ax.set_aspect("equal"); ax.axis("off")
        fig.text(0.03 + k * 0.49 + 0.23, 0.875, sub, ha="center", fontsize=12.5, fontweight="bold", color=INK)
        section(ax, layers, wool="upper")
        for xf in (80, 230, 380, 530):          # fire exposure from below
            ax.annotate("", (xf, -12), (xf, -150), arrowprops=dict(arrowstyle="-|>", color="#C0392B", lw=2))
        ax.text(300, -215, "tűzhatás", ha="center", fontsize=10, color="#C0392B", fontweight="bold")
    notes = ("A tűzállóságot a burkolat és annak rögzítése adja, nem az acélszerkezet: védelem nélkül a födém R 15-re sem alkalmas\n(a gerenda néhány perc alatt eléri a 350 °C-ot).\n"
             "• A tűzállóság a burkolat leválásával ér véget; a lemeztípus, a rétegszám, a csavarkiosztás és az eltolt illesztés a meghatározó.\n"
             "• Az alsó övre fektetett hőszigetelés visszatartja a hőt, és csökkentheti a tűzállóságot (queenslandi kísérletek).\n"
             "• A főtartónak és a cölöpfejnek ugyanazt a tűzállóságot kell biztosítania; nyitott kúszótérben a csupasz acél védelem nélküli.\n"
             "• Emeleti födémnél, felülről érő tűzhatásra: OSB és nem éghető réteg (gipszrost lemez vagy száraz esztrich), ha előírás.")
    fig.text(0.04, 0.09, notes, fontsize=10, color=INK, linespacing=1.45)
    save(fig, out, "D09_tuzvedelem.png")


def fig_buildup(out):
    fig = plt.figure(figsize=(W, H), dpi=DPI)
    fig.patch.set_facecolor("#FFFFFF")
    fig.text(0.03, 0.94, "7. ábra: Födémrétegrendek (metszet a gerendákra merőlegesen)", fontsize=19, fontweight="bold", color=NAVY)
    fig.text(0.03, 0.025, "Indikatív rétegrendek; [ind.] = feltételezett vastagság. Az elválasztó födém rétegrendje az SCI P320–P322 "
             "alapján felvett, a FlexInSheet-födémen nem mért kialakítás.", fontsize=9, color=MUTED, style="italic")
    single = [("Padlóburkolat (nem része a rendszernek)", 10, "white", ""),
              ("OSB födémlap [ind. 22 mm]", 22, "#E9D9B8", "////"),
              ("C200-1,5 gerendák, 600 mm-es tengely-\ntávolság; közöttük ásványgyapot\n[ind. 100 mm]", 200, None, None),
              ("Gipszkarton álmennyezet, egy réteg [ind. 12,5 mm]", 12.5, "#EEEEEE", "...")]
    separ = [("Nehéz felső réteg: gipszrost lemez vagy\nszáraz esztrich [ind. 25 mm]", 25, "#DDD6C8", "xx"),
             ("Rugalmas alátétréteg [ind. 10 mm]", 10, "#D6E4F0", "---"),
             ("OSB födémlap [ind. 22 mm]", 22, "#E9D9B8", "////"),
             ("C200-1,5 gerendák, közöttük\n100 mm ásványgyapot", 200, None, None),
             ("Rugalmas akusztikai sín [ind. 25 mm]", 25, "white", ""),
             ("2 × 15 mm hanggátló gipszkarton", 30, "#EEEEEE", "...")]
    for k, (layers, sub) in enumerate([(single, "Családi ház (száraz rétegrend)"), (separ, "Lakáselválasztó födém (többlakásos épület)")]):
        ax = fig.add_axes([0.03 + k * 0.49, 0.08, 0.46, 0.78]); ax.set_aspect("equal"); ax.axis("off")
        fig.text(0.03 + k * 0.49 + 0.23, 0.875, sub, ha="center", fontsize=12.5, fontweight="bold", color=INK)
        width = 600
        total = sum(t for _, t, _, _ in layers)
        z = total
        ylab = np.linspace(total + 160, -160, len(layers))
        for (name, t, fc, hatch), yl in zip(layers, ylab):
            z0 = z - t
            if fc is None:                      # joist zone: wool between C200 sections
                ax.add_patch(Rectangle((0, z0), width, t, fc="#F6EEC8", ec=INK, lw=0.6, hatch="oo"))
                for xc in (100, 500):
                    ax.add_patch(Rectangle((xc - 25, z0), 50, t, fc="white", ec="none"))
                    for u0, u1, v0, v1 in c_rects(C200[0], C200[1], C200[2], 3):
                        ax.add_patch(Rectangle((xc - 25 + u0, z0 + v0), u1 - u0, v1 - v0, fc=INK, ec="none"))
            else:
                ax.add_patch(Rectangle((0, z0), width, t, fc=fc, ec=INK, lw=0.6, hatch=hatch))
            ax.plot([width, width + 60, width + 110], [z0 + t / 2, z0 + t / 2, yl], color=MUTED, lw=0.7)
            ax.text(width + 125, yl, name, fontsize=10, color=INK, va="center", linespacing=1.2)
            z = z0
        ax.annotate("", (-40, 0), (-40, total), arrowprops=dict(arrowstyle="<->", lw=0.8, color=MUTED))
        ax.text(-55, total / 2, f"≈ {total:g} mm".replace(".", ","), rotation=90, ha="right", va="center", fontsize=10, color=MUTED)
        ax.set_xlim(-130, width + 900); ax.set_ylim(-220, total + 220)
    fig.text(0.52, 0.09, "Akusztikai követelmény: R'w + C ≥ 51 dB, L'n,w ≤ 55 dB\n(MSZ 15601-1, ellenőrizendő).\n"
             "Tűzvédelem: osztályba sorolt rendszer (30 perc) vagy\nMSZ EN 1365-2 szerinti kemencevizsgálat (60 perc).", fontsize=10, color=INK)
    save(fig, out, "D07_retegrendek.png")


def fig_profiles(out):
    fig = plt.figure(figsize=(W, H), dpi=DPI)
    fig.patch.set_facecolor("#F6F5F1")
    fig.text(0.03, 0.94, "2. ábra: Szelvények keresztmetszete (egységes léptékben)", fontsize=19, fontweight="bold", color=NAVY)
    fig.text(0.03, 0.025, "Hidegen hajlított szelvények: S350GD+Z; a fejlesztői katalógus ideiglenes szelvénycsaládja, a hengerlő profilkészlete "
             "alapján véglegesítendő. A peremprofil mérete indikatív.", fontsize=9, color=MUTED, style="italic")
    ax = fig.add_axes([0.02, 0.08, 0.96, 0.8]); ax.set_aspect("equal"); ax.axis("off")

    def draw_rects(rects, ox, oy, color):
        for u0, u1, v0, v1 in rects:
            ax.add_patch(Rectangle((ox + u0, oy + v0), u1 - u0, v1 - v0, fc=color, ec=INK, lw=0.6))

    def dim_v(x, y0, y1, txt):
        ax.annotate("", (x, y0), (x, y1), arrowprops=dict(arrowstyle="<->", lw=0.8, color=MUTED))
        ax.text(x - 8, (y0 + y1) / 2, txt, rotation=90, ha="right", va="center", fontsize=9.5, color=MUTED)

    def dim_h(y, x0, x1, txt):
        ax.annotate("", (x0, y), (x1, y), arrowprops=dict(arrowstyle="<->", lw=0.8, color=MUTED))
        ax.text((x0 + x1) / 2, y - 10, txt, ha="center", va="top", fontsize=9.5, color=MUTED)

    def real_c(h, b, c, t, mirror=False):
        r = [(0, t, 0, h), (0, b, 0, t), (0, b, h - t, h), (b - t, b, t, c), (b - t, b, h - c, h - t)]
        return [(-u1, -u0, v0, v1) for u0, u1, v0, v1 in r] if mirror else r

    items = [
        (0, real_c(*C200), "C200-1,5\nfödémgerenda", 200, 50, COL["cfs"]),
        (230, real_c(300, 60, 18, 2.5), "C300-2,5\nlegnagyobb magasság", 300, 60, COL["cfs"]),
        (500, real_c(300, 60, 18, 2.5) + [(u0 + 120, u1 + 120, v0, v1) for u0, u1, v0, v1 in real_c(300, 60, 18, 2.5, True)],
         "2×C300-2,5 zárt\nszelvénypár, 1. változat", 300, 120, COL["cfs"]),
        (790, [(u0 + 70, u1 + 70, v0, v1) for u0, u1, v0, v1 in i_rects(*HEA140)], "HEA 140, tűzihorg.,\n2. változat", 133, 140, COL["hot"]),
        (1060, [(u0 + 50, u1 + 50, v0, v1) for u0, u1, v0, v1 in rhs_rects(150, 100, 5)], "RHS 150×100×5\nkorlátozott magasságnál", 150, 100, COL["hot"]),
        (1290, [(0, 1.5, 0, 206), (0, 60, 0, 1.5), (0, 60, 204.5, 206)],
         "U206-1,5 peremprofil\n[ind.]", 206, 60, COL["cfs2"]),
    ]
    for ox, rects, label, h, b, color in items:
        draw_rects(rects, ox, 0, color)
        dim_v(ox - 22, 0, h, f"{h:g}")
        dim_h(-22, ox, ox + b, f"{b:g}")
        ax.text(ox + b / 2, -70, label, ha="center", va="top", fontsize=11, color=INK, fontweight="bold")
    ax.text(300, 255, "c = 18", fontsize=9.5, color=MUTED); ax.text(60, 140, "c = 15", fontsize=9.5, color=MUTED)
    ax.set_xlim(-60, 1420); ax.set_ylim(-170, 340)
    save(fig, out, "D02_szelvenyek.png")


def fig_plan(out, dxf):
    from floorframe import io_dxf
    from floorframe.engine.layout import generate_layout
    plan = io_dxf.read_plan(dxf)
    lay = generate_layout(plan)
    fig = plt.figure(figsize=(W, H), dpi=DPI)
    fig.patch.set_facecolor("#F6F5F1")
    fig.text(0.03, 0.94, "8. ábra: Kiosztási alaprajz a csomópontok jelölésével (U alakú mintaház)", fontsize=19, fontweight="bold", color=NAVY)
    fig.text(0.03, 0.025, "A tervezőprogram eredménye ideiglenes fesztávtáblázatokkal (GMNIA-számítással és Eurocode szerint még nem ellenőrzött). A toldás helye példa.",
             fontsize=9, color=MUTED, style="italic")
    ax = fig.add_axes([0.02, 0.07, 0.64, 0.84]); ax.set_aspect("equal"); ax.axis("off")
    for r in plan.regions:
        ax.add_patch(Polygon(r.polygon, closed=True, fc="#ECE6DA", ec=NAVY, lw=1.5))
    for j in lay.joists:
        ax.plot([j.p1[0], j.p2[0]], [j.p1[1], j.p2[1]], color="#3C78C3" if j.kind == "joist" else NAVY, lw=0.7 if j.kind == "joist" else 1.6)
    for b in lay.bearers:
        ax.plot([b.p1[0], b.p2[0]], [b.p1[1], b.p2[1]], color="#C0392B", lw=3)
    for p in lay.piles:
        ax.add_patch(Circle((p.x, p.y), 150, fc="#2E9E5B", ec=INK, lw=0.8, zorder=5))
    xs = sorted({p.x for p in lay.piles}); ys = sorted({p.y for p in lay.piles})
    pa = min(lay.piles, key=lambda p: (abs(p.x - xs[1]) + abs(p.y - ys[0])))
    b0 = min(lay.bearers, key=lambda b: abs(b.p1[1] - ys[1]))
    marks = {"A": (pa.x, pa.y), "B": (xs[0] + 1200, b0.p1[1]), "C": (xs[0] + 1500, max(ys)), "D": (xs[0] + (xs[1] - xs[0]) / 4, ys[0])}
    for k, (x, y) in marks.items():
        ax.add_patch(Circle((x, y), 420, fc="none", ec=ORANGE, lw=2.2, zorder=6))
        ax.text(x + 380, y + 380, k, fontsize=14, fontweight="bold", color="white", ha="center", va="center", zorder=7,
                bbox=dict(boxstyle="circle,pad=0.3", fc=ORANGE, ec="white"))
    allx = [v[0] for r in plan.regions for v in r.polygon]; ally = [v[1] for r in plan.regions for v in r.polygon]
    ax.set_xlim(min(allx) - 900, max(allx) + 900); ax.set_ylim(min(ally) - 900, max(ally) + 900)
    import re
    info = lay.flags[0].text.split(": ", 1)[-1] if lay.flags else ""
    mt = re.match(r"(\S+) @ (\d+) mm, (\d+) bay\(s\) of (\d+) mm \(util\. ([\d.]+)\), bearers (\S+), piles (\S+) @ (\d+) mm", info)
    hu = lambda v: v.replace(".", ",")
    info_hu = (f"Födémgerenda: {hu(mt[1])}, {mt[2]} mm-enként\n{mt[3]} mező × {mt[4]} mm (kihasználtság {hu(mt[5])})\n"
               f"Főtartó: {hu(mt[6]).replace('x', '×')}\nCölöp: {mt[7]}, {mt[8]} mm-enként") if mt else info
    legend(fig, [
        (None, "Jelmagyarázat"),
        (1, "Födémgerendák (kék), 600 mm-es\ntengelytávolsággal"),
        (2, "Főtartók (piros) a cölöpsorokon"),
        (3, "Csavarcölöpök (zöld)"),
        (None, "Csomópontok"),
        ("A", "Főtartó–cölöpfej (3. ábra)"),
        ("B", "Födémgerenda–főtartó (4. ábra)"),
        ("C", "Födémgerenda–peremprofil (5. ábra)"),
        ("D", "Főtartótoldás a negyedpontban (6. ábra)"),
        (None, "A program eredménye:\n" + info_hu),
    ])
    save(fig, out, "D08_alaprajz.png")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(Path(__file__).parent / "figures" / "details"))
    ap.add_argument("--dxf", default=str(Path(__file__).parents[1] / "examples" / "demo" / "03_u_shape_courtyard.dxf"))
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    fig_system(out); fig_profiles(out); fig_pile_head(out); fig_joist_bearer(out)
    fig_joist_rim(out); fig_splice(out); fig_buildup(out); fig_plan(out, a.dxf); fig_fire(out)
