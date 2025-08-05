"""Unit tests for Circle SVG export functionality."""

import xml.etree.ElementTree as ET

from cad_datamodel.core.types import Transform
from cad_datamodel.document import Document
from cad_datamodel.persistence.svg import SVGExporter
from cad_datamodel.shapes.circle import Circle
from cad_datamodel.shapes.shape import Style


class TestCircleSVGExport:
    """Test suite for exporting circles to SVG."""

    def test_basic_circle_export(self):
        """Test exporting a basic circle to SVG."""
        doc = Document()
        circle = Circle(cx=50, cy=50, radius=25, layer_id="layer1")
        doc.add_shape(circle)

        exporter = SVGExporter()
        svg_string = exporter.export_document(doc)

        # Parse the SVG
        root = ET.fromstring(svg_string)
        # Need to handle namespace
        ns = {"svg": "http://www.w3.org/2000/svg"}
        circles = root.findall(".//svg:circle", ns)

        assert len(circles) == 1
        circle_elem = circles[0]

        assert circle_elem.get("cx") == "50"
        assert circle_elem.get("cy") == "50"
        assert circle_elem.get("r") == "25"

    def test_circle_with_style_export(self):
        """Test exporting a circle with custom style."""
        doc = Document()
        style = Style(
            fill_color="#FF0000",
            fill_opacity=0.8,
            stroke_color="#000000",
            stroke_width=2.0,
            stroke_opacity=0.9,
        )
        circle = Circle(
            cx=100, cy=100, radius=50, layer_id="layer1", style=style
        )
        doc.add_shape(circle)

        exporter = SVGExporter()
        svg_string = exporter.export_document(doc)

        root = ET.fromstring(svg_string)
        ns = {"svg": "http://www.w3.org/2000/svg"}
        circle_elem = root.findall(".//svg:circle", ns)[0]

        style_attr = circle_elem.get("style")
        assert style_attr is not None
        assert "fill:#FF0000" in style_attr
        assert "fill-opacity:0.8" in style_attr
        assert "stroke:#000000" in style_attr
        assert "stroke-width:2.0" in style_attr
        assert "stroke-opacity:0.9" in style_attr

    def test_circle_with_transform_export(self):
        """Test exporting a circle with transformation."""
        doc = Document()
        transform = Transform.translation(20, 30)
        circle = Circle(
            cx=50, cy=50, radius=25, layer_id="layer1", transform=transform
        )
        doc.add_shape(circle)

        exporter = SVGExporter()
        svg_string = exporter.export_document(doc)

        root = ET.fromstring(svg_string)
        ns = {"svg": "http://www.w3.org/2000/svg"}
        circle_elem = root.findall(".//svg:circle", ns)[0]

        transform_attr = circle_elem.get("transform")
        assert transform_attr is not None
        # Should be matrix(1,0,0,1,20,30)
        assert "matrix" in transform_attr
        assert "20" in transform_attr
        assert "30" in transform_attr

    def test_invisible_circle_not_exported(self):
        """Test that invisible circles are not exported."""
        doc = Document()
        circle = Circle(
            cx=50, cy=50, radius=25, layer_id="layer1", visible=False
        )
        doc.add_shape(circle)

        exporter = SVGExporter()
        svg_string = exporter.export_document(doc)

        root = ET.fromstring(svg_string)
        ns = {"svg": "http://www.w3.org/2000/svg"}
        circles = root.findall(".//svg:circle", ns)

        assert len(circles) == 0

    def test_multiple_circles_export(self):
        """Test exporting multiple circles."""
        doc = Document()

        circles = [
            Circle(cx=50, cy=50, radius=25, layer_id="layer1"),
            Circle(cx=150, cy=150, radius=50, layer_id="layer1"),
            Circle(cx=250, cy=250, radius=75, layer_id="layer2"),
        ]

        for circle in circles:
            doc.add_shape(circle)

        exporter = SVGExporter()
        svg_string = exporter.export_document(doc)

        root = ET.fromstring(svg_string)
        ns = {"svg": "http://www.w3.org/2000/svg"}
        circle_elems = root.findall(".//svg:circle", ns)

        assert len(circle_elems) == 3

        # Check each circle
        assert circle_elems[0].get("cx") == "50"
        assert circle_elems[0].get("r") == "25"

        assert circle_elems[1].get("cx") == "150"
        assert circle_elems[1].get("r") == "50"

        assert circle_elems[2].get("cx") == "250"
        assert circle_elems[2].get("r") == "75"
