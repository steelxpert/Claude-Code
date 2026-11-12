"""Finite-strip (pycufsm) helpers for the QA of ec3_1_3_proto.py."""
import math
import numpy as np
import ec3_1_3_proto as ec
import _cufsm_shim  # noqa: F401  (numpy-2 fix for the pure-Python solver)
from pycufsm.fsm import strip
from pycufsm.pre.stresses import stress_gen


def sect_props_from(pts, t):
    g = ec.line_props([(x, y, t) for x, y in pts])
    return {"cx": g.yc, "cy": g.zc, "x0": g.ys, "y0": g.zs, "phi": 0.0, "A": g.A, "Ixx": g.Iy, "Ixy": g.Iyz,
            "Iyy": g.Iz, "I11": g.Iy, "I22": g.Iz, "Cw": g.Iw, "J": g.It, "B1": 0.0, "B2": 0.0, "wn": np.array([])}


def midline_nodes(s: ec.Channel, n_arc=4, dmax=10.0):
    pts = [(p[0], p[1]) for p in s.polyline(n_arc=n_arc)]
    ref = [pts[0]]
    for a, b in zip(pts[:-1], pts[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        n = max(1, int(L // dmax))
        for k in range(1, n + 1):
            ref.append((a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n))
    return ref


def signature_curve(s: ec.Channel, mode: str, lengths=None):
    """Returns (lengths, sigma_cr(L) for max fibre stress, strict local minima [(L, sigma)],
    distortional-range minimum (min over 2*h..8*h, even if not a strict local minimum))."""
    pts = midline_nodes(s)
    nn = len(pts)
    nodes = np.array([[i, x, y, 1, 1, 1, 1, 0.0] for i, (x, y) in enumerate(pts)])
    elements = np.array([[i, i, i + 1, s.t, 0] for i in range(nn - 1)])
    props = np.array([[0, ec.E_STEEL, ec.E_STEEL, ec.NU, ec.NU, ec.G_STEEL]])
    sp = sect_props_from(pts, s.t)
    fy = s.fyb
    if mode == "P":
        forces = {"P": sp["A"] * fy, "Mxx": 0, "Myy": 0, "M11": 0, "M22": 0, "restrain": False, "offset": [0, 0]}
    else:
        ymax = max(abs(p[1] - sp["cy"]) for p in pts)
        forces = {"P": 0, "Mxx": fy * sp["Ixx"] / ymax, "Myy": 0, "M11": 0, "M22": 0, "restrain": False, "offset": [0, 0]}
    nodes_p = stress_gen(nodes=nodes, forces=forces, sect_props=sp)
    if lengths is None:
        lengths = np.unique(np.round(np.geomspace(30, 6000, 70)))
    gbt = {"glob": [0], "dist": [0], "local": [0], "other": [0], "o_space": 1, "couple": 1, "orth": 2, "norm": 0}
    sig, curve, shapes = strip(props=props, nodes=nodes_p, elements=elements, lengths=lengths, springs=np.array([]),
                               constraints=np.array([]), GBT_con=gbt, B_C="S-S", m_all=np.ones((len(lengths), 1)),
                               n_eigs=6, sect_props=sp)
    sig = np.asarray(sig).ravel() * fy
    mins = [(lengths[i], sig[i]) for i in range(1, len(sig) - 1) if sig[i] < sig[i - 1] and sig[i] <= sig[i + 1]]
    mask = (lengths >= 2 * s.h) & (lengths <= 8 * s.h)
    i = int(np.argmin(np.where(mask, sig, np.inf)))
    return lengths, sig, mins, (lengths[i], sig[i])
