"""CAD Drawing Application Data Model.

A comprehensive data model for CAD drawing applications that supports
geometric shapes, layers, groups, styling, and SVG rendering/persistence.
"""

from cad_datamodel.document import Document
from cad_datamodel.shapes import IShape, Rectangle, Shape, ShapeFactory, Style

__version__ = "0.1.0"
__all__ = [
    "__version__",
    "Document",
    "IShape",
    "Shape",
    "Style",
    "Rectangle",
    "ShapeFactory",
]
