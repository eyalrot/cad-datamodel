"""Shapes module for the CAD datamodel.

This module contains all shape implementations and the shape factory.
"""

from cad_datamodel.shapes.circle import Circle
from cad_datamodel.shapes.factory import ShapeFactory
from cad_datamodel.shapes.rectangle import Rectangle
from cad_datamodel.shapes.shape import IShape, Shape, Style

__all__ = [
    "IShape",
    "Shape",
    "Style",
    "Circle",
    "Rectangle",
    "ShapeFactory",
]
