from floorframe import catalog


def test_section_properties_increase_with_depth():
    c150 = catalog.section("C150-1.5")
    c200 = catalog.section("C200-1.5")
    assert c200.I_mm4 > c150.I_mm4 > 0
    assert 1.5 < c150.mass_kg_m < 5


def test_placeholder_spans_are_sane_and_ordered():
    s150 = catalog.joist_span(catalog.section("C150-1.2"), 600, "L35")
    s300 = catalog.joist_span(catalog.section("C300-2.5"), 600, "L35")
    assert 2000 < s150.span_mm < s300.span_mm < 9000
    assert s150.source == "PLACEHOLDER"
    assert catalog.joist_span(catalog.section("C200-2.0"), 400, "L35").span_mm > catalog.joist_span(catalog.section("C200-2.0"), 600, "L35").span_mm


def test_load_class_lookup():
    assert catalog.load_class_for(1.5, 2.0) == "L35"
    assert catalog.load_class_for(0.4, 2.0) == "L25"
