"""Document container for CAD drawings.

This module provides the Document class which serves as the root container
for all shapes and layers in a CAD drawing.
"""

from typing import Any, Optional

from cad_datamodel.core.types import ShapeType
from cad_datamodel.shapes.shape import Shape


class Document:
    """Root container for a CAD drawing.
    
    A simplified implementation for testing purposes.
    """
    
    def __init__(
        self,
        canvas_width: float = 800.0,
        canvas_height: float = 600.0,
        units: str = "px"
    ):
        """Initialize a new document.
        
        Args:
            canvas_width: Width of the canvas
            canvas_height: Height of the canvas
            units: Measurement units (default: pixels)
        """
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.units = units
        self.shapes: list[Shape] = []
        
    def add_shape(self, shape: Shape) -> None:
        """Add a shape to the document.
        
        Args:
            shape: The shape to add
        """
        self.shapes.append(shape)
        
    def get_all_shapes(self) -> list[Shape]:
        """Get all shapes in the document.
        
        Returns:
            List of all shapes
        """
        return self.shapes.copy()