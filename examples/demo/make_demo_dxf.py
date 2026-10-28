"""Write the client-demo footprints (mm, closed polylines on layer FLOOR, counter-clockwise)."""
from pathlib import Path

import ezdxf

SHAPES = {
    "01_rectangle_bungalow": [[(0, 0), (11000, 0), (11000, 8000), (0, 8000)]],
    "02_t_shape": [[(0, 0), (6000, 0), (6000, 5000), (14000, 5000), (14000, 10000),
                    (-2000, 10000), (-2000, 5000), (0, 5000)]],
    "03_u_shape_courtyard": [[(0, 0), (16000, 0), (16000, 11000), (11000, 11000), (11000, 5500),
                              (5000, 5500), (5000, 11000), (0, 11000)]],
    "04_stepped_z_plan": [[(0, 0), (8000, 0), (8000, 2750), (15000, 2750), (15000, 11000),
                           (7000, 11000), (7000, 8250), (0, 8250)]],
    "05_house_plus_terrace": [[(0, 0), (12000, 0), (12000, 9000), (0, 9000)],
                              [(12000, 2000), (16000, 2000), (16000, 7000), (12000, 7000)]],
}

if __name__ == "__main__":
    here = Path(__file__).parent
    for name, polys in SHAPES.items():
        doc = ezdxf.new("R2010")
        doc.units = ezdxf.units.MM
        doc.layers.add("FLOOR")
        for p in polys:
            doc.modelspace().add_lwpolyline(p, close=True, dxfattribs={"layer": "FLOOR"})
        doc.saveas(here / f"{name}.dxf")
        print("wrote", name)
