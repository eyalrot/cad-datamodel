"""Factory for creating shapes in the CAD system.

This module implements the Factory pattern for shape creation,
providing a centralized way to create shapes of different types.
"""

from typing import Any, ClassVar, Optional

from cad_datamodel.core.exceptions import ShapeValidationError
from cad_datamodel.core.types import ShapeType
from cad_datamodel.shapes.circle import Circle
from cad_datamodel.shapes.rectangle import Rectangle
from cad_datamodel.shapes.shape import IShape, Shape, Style


class ShapeFactory:
    """Factory class for creating shapes.

    The ShapeFactory provides methods to create shapes by type,
    ensuring consistent creation and validation across the system.
    """

    # Registry of shape types to their corresponding classes
    _shape_registry: ClassVar[dict[ShapeType, type[Shape]]] = {
        ShapeType.RECTANGLE: Rectangle,
        ShapeType.CIRCLE: Circle,
    }

    @classmethod
    def register_shape(cls, shape_type: ShapeType, shape_class: type[Shape]) -> None:
        """Register a new shape type with the factory.

        Args:
            shape_type: The ShapeType enum value
            shape_class: The class that implements this shape type
        """
        cls._shape_registry[shape_type] = shape_class

    @classmethod
    def create_shape(
        cls, shape_type: ShapeType, layer_id: str, **kwargs: Any
    ) -> IShape:
        """Create a shape of the specified type.

        Args:
            shape_type: The type of shape to create
            layer_id: ID of the layer containing this shape
            **kwargs: Shape-specific parameters

        Returns:
            The created shape instance

        Raises:
            ShapeValidationError: If the shape type is not supported
                                or if shape creation fails
        """
        if shape_type not in cls._shape_registry:
            raise ShapeValidationError(
                shape_type.name,
                f"Unsupported shape type: {shape_type.name}",
                kwargs.get("shape_id"),
            )

        shape_class = cls._shape_registry[shape_type]

        try:
            # Add layer_id to kwargs if not already present
            kwargs["layer_id"] = layer_id
            return shape_class(**kwargs)
        except TypeError as e:
            raise ShapeValidationError(
                shape_type.name,
                f"Invalid parameters for {shape_type.name}: {e}",
                kwargs.get("shape_id"),
            ) from e

    @classmethod
    def create_rectangle(
        cls,
        x: float,
        y: float,
        width: float,
        height: float,
        layer_id: str,
        *,
        corner_radius: float = 0.0,
        group_id: Optional[str] = None,
        visible: bool = True,
        locked: bool = False,
        style: Optional[Style] = None,
        transform: Optional[Any] = None,
        metadata: Optional[dict[str, Any]] = None,
        shape_id: Optional[str] = None,
    ) -> Rectangle:
        """Convenience method to create a rectangle.

        Args:
            x: X coordinate of the top-left corner
            y: Y coordinate of the top-left corner
            width: Width of the rectangle
            height: Height of the rectangle
            layer_id: ID of the layer containing this shape
            corner_radius: Radius for rounded corners (default: 0.0)
            group_id: Optional ID of parent group
            visible: Whether the shape is visible
            locked: Whether the shape is locked for editing
            style: Visual styling information
            transform: Transformation matrix
            metadata: Additional user-defined metadata
            shape_id: Optional explicit ID (auto-generated if not provided)

        Returns:
            The created Rectangle instance
        """
        return Rectangle(
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

    @classmethod
    def create_circle(
        cls,
        cx: float,
        cy: float,
        radius: float,
        layer_id: str,
        *,
        group_id: Optional[str] = None,
        visible: bool = True,
        locked: bool = False,
        style: Optional[Style] = None,
        transform: Optional[Any] = None,
        metadata: Optional[dict[str, Any]] = None,
        shape_id: Optional[str] = None,
    ) -> Circle:
        """Convenience method to create a circle.

        Args:
            cx: X coordinate of the center point
            cy: Y coordinate of the center point
            radius: Radius of the circle
            layer_id: ID of the layer containing this shape
            group_id: Optional ID of parent group
            visible: Whether the shape is visible
            locked: Whether the shape is locked for editing
            style: Visual styling information
            transform: Transformation matrix
            metadata: Additional user-defined metadata
            shape_id: Optional explicit ID (auto-generated if not provided)

        Returns:
            The created Circle instance
        """
        return Circle(
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

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> IShape:
        """Create a shape from a dictionary representation.

        Args:
            data: Dictionary containing shape data

        Returns:
            The created shape instance

        Raises:
            ShapeValidationError: If the shape type is invalid or
                                data is malformed
        """
        try:
            shape_type_str = data["type"]
            shape_type = ShapeType[shape_type_str]
        except (KeyError, ValueError) as e:
            raise ShapeValidationError(
                "Unknown", f"Invalid or missing shape type: {e}", data.get("id")
            ) from e

        if shape_type not in cls._shape_registry:
            raise ShapeValidationError(
                shape_type.name,
                f"Unsupported shape type: {shape_type.name}",
                data.get("id"),
            )

        shape_class = cls._shape_registry[shape_type]
        return shape_class.from_dict(data)

    @classmethod
    def get_supported_types(cls) -> list[ShapeType]:
        """Get a list of all supported shape types.

        Returns:
            List of ShapeType enums that are currently supported
        """
        return list(cls._shape_registry.keys())
