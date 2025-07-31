"""SVG export functionality for CAD drawings.

This module provides SVG export capabilities for converting CAD shapes
to SVG format.
"""

from typing import Optional
from xml.etree import ElementTree as ET

from cad_datamodel.core.constants import SVG_NAMESPACE, SVG_VERSION
from cad_datamodel.document import Document
from cad_datamodel.shapes.rectangle import Rectangle
from cad_datamodel.shapes.shape import Shape


class SVGExporter:
    """Export CAD drawings to SVG format."""
    
    def __init__(self):
        """Initialize the SVG exporter."""
        self.svg_ns = SVG_NAMESPACE
        
    def export_document(self, document: Document) -> str:
        """Export a document to SVG string.
        
        Args:
            document: The document to export
            
        Returns:
            SVG string representation
        """
        # Create root SVG element
        svg = ET.Element('svg', {
            'xmlns': self.svg_ns,
            'version': SVG_VERSION,
            'width': str(document.canvas_width),
            'height': str(document.canvas_height),
            'viewBox': f"0 0 {document.canvas_width} {document.canvas_height}"
        })
        
        # Export all shapes
        for shape in document.get_all_shapes():
            if shape.visible:
                svg_element = self._shape_to_svg(shape)
                if svg_element is not None:
                    svg.append(svg_element)
        
        # Convert to string
        ET.register_namespace('', self.svg_ns)
        tree = ET.ElementTree(svg)
        ET.indent(tree, space='  ')
        
        # Convert to string
        svg_str = ET.tostring(svg, encoding='unicode', method='xml')
        
        # Add XML declaration
        return '<?xml version="1.0" encoding="UTF-8"?>\n' + svg_str
    
    def _shape_to_svg(self, shape: Shape) -> Optional[ET.Element]:
        """Convert a shape to SVG element.
        
        Args:
            shape: The shape to convert
            
        Returns:
            SVG element or None if shape type not supported
        """
        if isinstance(shape, Rectangle):
            return self._rectangle_to_svg(shape)
        return None
    
    def _rectangle_to_svg(self, rect: Rectangle) -> ET.Element:
        """Convert a rectangle to SVG rect element.
        
        Args:
            rect: The rectangle to convert
            
        Returns:
            SVG rect element
        """
        attrib = {
            'x': str(rect.x),
            'y': str(rect.y),
            'width': str(rect.width),
            'height': str(rect.height)
        }
        
        # Add corner radius if present
        if rect.corner_radius > 0:
            attrib['rx'] = str(rect.corner_radius)
            attrib['ry'] = str(rect.corner_radius)
        
        # Apply style
        style_parts = []
        if rect.style.fill_color:
            style_parts.append(f"fill:{rect.style.fill_color}")
            if rect.style.fill_opacity < 1.0:
                style_parts.append(f"fill-opacity:{rect.style.fill_opacity}")
        else:
            style_parts.append("fill:none")
            
        if rect.style.stroke_color:
            style_parts.append(f"stroke:{rect.style.stroke_color}")
            style_parts.append(f"stroke-width:{rect.style.stroke_width}")
            if rect.style.stroke_opacity < 1.0:
                style_parts.append(f"stroke-opacity:{rect.style.stroke_opacity}")
        
        if style_parts:
            attrib['style'] = ';'.join(style_parts)
        
        # Apply transform if not identity
        transform = rect.transform
        if transform and transform != transform.identity():
            matrix = transform.matrix
            # SVG transform format: matrix(a,b,c,d,e,f)
            transform_str = f"matrix({matrix[0,0]},{matrix[1,0]},{matrix[0,1]},{matrix[1,1]},{matrix[0,2]},{matrix[1,2]})"
            attrib['transform'] = transform_str
        
        return ET.Element('rect', attrib)