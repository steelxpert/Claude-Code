"""SVG rendering of a Layout (for the web UI and reports)."""
from __future__ import annotations

from .model import Layout, Plan


def layout_svg(layout: Layout, plan: Plan, width_px: int = 900) -> str:
    xs = [x for r in plan.regions for x, _ in r.polygon]
    ys = [y for r in plan.regions for _, y in r.polygon]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    pad = 600
    w, h = (maxx - minx) + 2 * pad, (maxy - miny) + 2 * pad
    k = width_px / w
    H = int(h * k)

    def X(x): return (x - minx + pad) * k
    def Y(y): return H - (y - miny + pad) * k

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width_px}" height="{H}" viewBox="0 0 {width_px} {H}" font-family="sans-serif">',
           f'<rect width="100%" height="100%" fill="#f7f6f2"/>']
    for r in plan.regions:
        pts = " ".join(f"{X(x):.1f},{Y(y):.1f}" for x, y in r.polygon)
        out.append(f'<polygon points="{pts}" fill="#e9e4d6" stroke="#555" stroke-width="1.5"/>')
    for j in layout.joists:
        col, sw = ("#2a6ebb", 1.2) if j.kind == "joist" else ("#0b3d91", 2.5)
        out.append(f'<line x1="{X(j.p1[0]):.1f}" y1="{Y(j.p1[1]):.1f}" x2="{X(j.p2[0]):.1f}" y2="{Y(j.p2[1]):.1f}" stroke="{col}" stroke-width="{sw}"/>')
    for b in layout.bearers:
        out.append(f'<line x1="{X(b.p1[0]):.1f}" y1="{Y(b.p1[1]):.1f}" x2="{X(b.p2[0]):.1f}" y2="{Y(b.p2[1]):.1f}" stroke="#c0392b" stroke-width="5" stroke-linecap="round"/>')
    for p in layout.piles:
        out.append(f'<circle cx="{X(p.x):.1f}" cy="{Y(p.y):.1f}" r="{max(4, 150 * k):.1f}" fill="#27ae60" stroke="#145a32" stroke-width="1.5"><title>{p.name} N_Ed={p.N_ed} kN</title></circle>')
    for pl in plan.point_loads:
        out.append(f'<g><circle cx="{X(pl.x):.1f}" cy="{Y(pl.y):.1f}" r="7" fill="none" stroke="#e67e22" stroke-width="2.5"/>'
                   f'<text x="{X(pl.x) + 9:.1f}" y="{Y(pl.y) - 6:.1f}" font-size="11" fill="#e67e22">{pl.P} kN {pl.label}</text></g>')
    y = 16
    for name, r in layout.meta.get("regions", {}).items():
        out.append(f'<text x="8" y="{y}" font-size="12" fill="#222">{name}: joists {r["joist_section"]} @ {r["spacing_mm"]} mm, '
                   f'{r["n_bays"]} bay(s) x {r["bay_mm"]} mm · bearers {r["bearer_section"]} · piles {r["pile"]} @ {r["pile_spacing_mm"]} mm</text>')
        y += 16
    out.append("</svg>")
    return "\n".join(out)
