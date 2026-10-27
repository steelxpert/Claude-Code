import json

import ezdxf
from fastapi.testclient import TestClient

from floorframe import io_dxf
from floorframe.api import app
from floorframe.engine.layout import generate_layout
from floorframe.fea import campaign

client = TestClient(app)


def test_api_layout_json():
    r = client.post("/api/layout", json={"regions": [{"polygon": [[0, 0], [8000, 0], [8000, 5000], [0, 5000]]}]})
    assert r.status_code == 200, r.text
    d = r.json()
    assert d["svg"].startswith("<svg") and d["bom"]["steel_total_kg"] > 0 and d["layout"]["piles"]


def test_api_rejects_bad_polygon():
    r = client.post("/api/layout", json={"regions": [{"polygon": [[0, 0], [1, 1], [0, 0]]}]})
    assert r.status_code == 422


def test_dxf_roundtrip(tmp_path):
    src = tmp_path / "house.dxf"
    io_dxf.write_sample_house(src)
    plan = io_dxf.read_plan(src)
    assert len(plan.regions) == 1 and len(plan.regions[0].polygon) == 6
    lay = generate_layout(plan)
    out = tmp_path / "layout.dxf"
    io_dxf.write_layout(lay, out, plan)
    doc = ezdxf.readfile(out)
    assert len(doc.modelspace().query('CIRCLE[layer=="PILES"]')) == len(lay.piles)
    with open(src, "rb") as f:
        r = client.post("/api/layout/dxf", files={"file": ("house.dxf", f, "application/dxf")}, data={"g": "1.5", "q": "2.0"})
    assert r.status_code == 200, r.text


def test_campaign_matrix_and_tables(tmp_path):
    n = campaign.write_case_matrix(tmp_path / "cases.json", spans=[3000, 4000])
    assert n == 7 * 2 * 4 * 2
    cases = json.loads((tmp_path / "cases.json").read_text())["cases"]
    # fake results: strength passes at 3000 only, deflection passes at both
    res = [{**c, "w_peak_kN_m": c["w_Ed_kN_m"] * (1.3 if c["span_mm"] == 3000 else 0.9), "deflection_at_w_sls_mm": 5.0}
           for c in cases if c["section"] == "C200-1.5"]
    t = campaign.results_to_tables(res)
    row = next(r for r in t["joists"] if r["spacing_mm"] == 600 and r["load_class"] == "L35")
    assert row["span_strength_mm"] == 3000 and row["span_deflection_mm"] == 4000
