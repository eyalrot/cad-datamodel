"""Circle shape implementation for the CAD system.

This module provides the Circle shape class with support for
bounds calculation and transformations.
"""

from typing import Any, Optional

import numpy as np

from cad_datamodel.core.exceptions import ShapeValidationError
from cad_datamodel.core.types import Bounds, Point, ShapeType, Transform
from cad_datamodel.shapes.shape import Shape, Style


class Circle(Shape):
    """A circular shape defined by center point and radius.

    Circles are defined by their center point (cx, cy) and radius.
    They support transformations and style properties.
    """

    def __init__(
        self,
        cx: float,
        cy: float,
        radius: float,
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
        """Initialize a circle shape.

        Args:
            cx: X-coordinate of center point
            cy: Y-coordinate of center point
            radius: Circle radius
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
        # Validate circle-specific parameters
        if radius <= 0:
            raise ShapeValidationError(
                "CIRCLE", f"Radius must be positive, got {radius}", shape_id
            )

        # Initialize base shape
        super().__init__(
            shape_type=ShapeType.CIRCLE,
            layer_id=layer_id,
            group_id=group_id,
            visible=visible,
            locked=locked,
            style=style,
            transform=transform,
            metadata=metadata,
            shape_id=shape_id,
        )

        # Store circle-specific attributes (immutable)
        self._cx = cx
        self._cy = cy
        self._radius = radius

    @property
    def cx(self) -> float:
        """Get X-coordinate of center point."""
        return self._cx

    @property
    def cy(self) -> float:
        """Get Y-coordinate of center point."""
        return self._cy

    @property
    def radius(self) -> float:
        """Get circle radius."""
        return self._radius

    def get_bounds(self) -> Bounds:
        """Calculate the axis-aligned bounding box of the circle.

        Takes into account the transformation matrix to compute
        the bounds of the transformed circle.

        Returns:
            Bounds object representing the circle's bounding box
        """
        # For a circle, we need to check the extrema after transformation
        # We'll check 4 cardinal points on the circle
        angles = [0, np.pi/2, np.pi, 3*np.pi/2]
        points = []

        for angle in angles:
            # Point on circle circumference
            x = self._cx + self._radius * np.cos(angle)
            y = self._cy + self._radius * np.sin(angle)
            point = Point(x, y)
            # Apply transformation
            transformed = self._transform.apply_to_point(point)
            points.append(transformed)

        # Also include the center point for completeness
        center = Point(self._cx, self._cy)
        transformed_center = self._transform.apply_to_point(center)
        points.append(transformed_center)

        # Find min and max coordinates
        x_coords = [p.x for p in points]
        y_coords = [p.y for p in points]

        min_point = Point(min(x_coords), min(y_coords))
        max_point = Point(max(x_coords), max(y_coords))

        return Bounds(min_point, max_point)

    def apply_transform(self, transform: Transform) -> "Circle":
        """Apply a transformation to create a new transformed circle.

        Args:
            transform: The transformation to apply

        Returns:
            New Circle instance with composed transformation
        """
        new_transform = self._transform.compose(transform)

        return Circle(
            cx=self._cx,
            cy=self._cy,
            radius=self._radius,
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
        """Serialize the circle to a dictionary.

        Returns:
            Dictionary representation of the circle
        """
        data = super().to_dict()
        data.update(
            {
                "cx": self._cx,
                "cy": self._cy,
                "radius": self._radius,
            }
        )
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Circle":
        """Deserialize a circle from a dictionary.

        Args:
            data: Dictionary containing circle data

        Returns:
            Circle instance

        Raises:
            ShapeValidationError: If the data is invalid
        """
        # Extract circle-specific attributes
        try:
            cx = float(data["cx"])
            cy = float(data["cy"])
            radius = float(data["radius"])
        except (KeyError, ValueError, TypeError) as e:
            raise ShapeValidationError(
                "CIRCLE", f"Invalid circle data: {e}", data.get("id")
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
            cx=cx,
            cy=cy,
            radius=radius,
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
        """String representation of the circle."""
        return (
            f"Circle(id={self._id}, cx={self._cx}, cy={self._cy}, "
            f"radius={self._radius})"
        )
