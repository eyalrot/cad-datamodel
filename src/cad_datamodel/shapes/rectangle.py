"""Rectangle shape implementation for the CAD system.

This module provides the Rectangle shape class with support for
corner radius, bounds calculation, and transformations.
"""

from typing import Any, Optional

import numpy as np

from cad_datamodel.core.exceptions import ShapeValidationError
from cad_datamodel.core.types import Bounds, Point, ShapeType, Transform
from cad_datamodel.shapes.shape import Shape, Style


class Rectangle(Shape):
    """A rectangular shape with optional rounded corners.
    
    Rectangles are defined by their top-left corner position (x, y),
    dimensions (width, height), and optional corner radius.
    """

    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        corner_radius: float = 0.0,
        *,
        layer_id: str,
        group_id: Optional[str] = None,
        visible: bool = True,
        locked: bool = False,
        style: Optional[Style] = None,
        transform: Optional[Transform] = None,
        metadata: Optional[dict[str, Any]] = None,
        shape_id: Optional[str] = None,
    ):
        """Initialize a rectangle shape.
        
        Args:
            x: X-coordinate of top-left corner
            y: Y-coordinate of top-left corner
            width: Rectangle width
            height: Rectangle height
            corner_radius: Optional corner radius for rounded rectangles
            layer_id: ID of the layer containing this shape
            group_id: Optional ID of parent group
            visible: Whether the shape is visible
            locked: Whether the shape is locked for editing
            style: Visual styling information
            transform: Transformation matrix
            metadata: Additional user-defined metadata
            shape_id: Optional explicit ID (auto-generated if not provided)
            
        Raises:
            ShapeValidationError: If parameters are invalid
        """
        # Validate rectangle-specific parameters
        if width <= 0:
            raise ShapeValidationError(
                "RECTANGLE",
                f"Width must be positive, got {width}",
                shape_id
            )

        if height <= 0:
            raise ShapeValidationError(
                "RECTANGLE",
                f"Height must be positive, got {height}",
                shape_id
            )

        if corner_radius < 0:
            raise ShapeValidationError(
                "RECTANGLE",
                f"Corner radius cannot be negative, got {corner_radius}",
                shape_id
            )

        # Validate corner radius doesn't exceed half of the smallest dimension
        max_radius = min(width, height) / 2
        if corner_radius > max_radius:
            raise ShapeValidationError(
                "RECTANGLE",
                f"Corner radius {corner_radius} exceeds maximum allowed {max_radius}",
                shape_id
            )

        # Initialize base shape
        super().__init__(
            shape_type=ShapeType.RECTANGLE,
            layer_id=layer_id,
            group_id=group_id,
            visible=visible,
            locked=locked,
            style=style,
            transform=transform,
            metadata=metadata,
            shape_id=shape_id,
        )

        # Store rectangle-specific attributes (immutable)
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._corner_radius = corner_radius

    @property
    def x(self) -> float:
        """Get X-coordinate of top-left corner."""
        return self._x

    @property
    def y(self) -> float:
        """Get Y-coordinate of top-left corner."""
        return self._y

    @property
    def width(self) -> float:
        """Get rectangle width."""
        return self._width

    @property
    def height(self) -> float:
        """Get rectangle height."""
        return self._height

    @property
    def corner_radius(self) -> float:
        """Get corner radius."""
        return self._corner_radius

    def get_bounds(self) -> Bounds:
        """Calculate the axis-aligned bounding box of the rectangle.
        
        Takes into account the transformation matrix to compute
        the bounds of the transformed rectangle.
        
        Returns:
            Bounds object representing the rectangle's bounding box
        """
        # Define the four corners of the rectangle
        corners = [
            Point(self._x, self._y),  # Top-left
            Point(self._x + self._width, self._y),  # Top-right
            Point(self._x + self._width, self._y + self._height),  # Bottom-right
            Point(self._x, self._y + self._height),  # Bottom-left
        ]

        # Apply transformation to each corner
        transformed_corners = [
            self._transform.apply_to_point(corner) for corner in corners
        ]

        # Find min and max coordinates
        x_coords = [p.x for p in transformed_corners]
        y_coords = [p.y for p in transformed_corners]

        min_point = Point(min(x_coords), min(y_coords))
        max_point = Point(max(x_coords), max(y_coords))

        return Bounds(min_point, max_point)

    def apply_transform(self, transform: Transform) -> "Rectangle":
        """Apply a transformation to create a new transformed rectangle.
        
        Args:
            transform: The transformation to apply
            
        Returns:
            New Rectangle instance with composed transformation
        """
        new_transform = self._transform.compose(transform)

        return Rectangle(
            x=self._x,
            y=self._y,
            width=self._width,
            height=self._height,
            corner_radius=self._corner_radius,
            layer_id=self._layer_id,
            group_id=self._group_id,
            visible=self._visible,
            locked=self._locked,
            style=self._style,
            transform=new_transform,
            metadata=self._metadata,
            shape_id=self._id,  # Preserve the same ID
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize the rectangle to a dictionary.
        
        Returns:
            Dictionary representation of the rectangle
        """
        data = super().to_dict()
        data.update({
            "x": self._x,
            "y": self._y,
            "width": self._width,
            "height": self._height,
            "corner_radius": self._corner_radius,
        })
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Rectangle":
        """Deserialize a rectangle from a dictionary.
        
        Args:
            data: Dictionary containing rectangle data
            
        Returns:
            Rectangle instance
            
        Raises:
            ShapeValidationError: If the data is invalid
        """
        # Extract rectangle-specific attributes
        try:
            x = float(data["x"])
            y = float(data["y"])
            width = float(data["width"])
            height = float(data["height"])
            corner_radius = float(data.get("corner_radius", 0.0))
        except (KeyError, ValueError, TypeError) as e:
            raise ShapeValidationError(
                "RECTANGLE",
                f"Invalid rectangle data: {e}",
                data.get("id")
            ) from e

        # Extract common shape attributes
        layer_id = data.get("layer_id", "")
        group_id = data.get("group_id")
        visible = data.get("visible", True)
        locked = data.get("locked", False)
        shape_id = data.get("id")
        metadata = data.get("metadata", {})

        # Reconstruct style
        style_data = data.get("style", {})
        style = Style(**style_data) if style_data else None

        # Reconstruct transform
        transform_data = data.get("transform")
        transform = Transform(np.array(transform_data)) if transform_data else None

        return cls(
            x=x,
            y=y,
            width=width,
            height=height,
            corner_radius=corner_radius,
            layer_id=layer_id,
            group_id=group_id,
            visible=visible,
            locked=locked,
            style=style,
            transform=transform,
            metadata=metadata,
            shape_id=shape_id,
        )

    def __repr__(self) -> str:
        """String representation of the rectangle."""
        return (
            f"Rectangle(id={self._id}, x={self._x}, y={self._y}, "
            f"width={self._width}, height={self._height}, "
            f"corner_radius={self._corner_radius})"
        )

