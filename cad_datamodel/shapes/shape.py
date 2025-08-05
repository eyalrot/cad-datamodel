"""Base shape class and shape interface for the CAD system.

This module defines the abstract base class for all shapes in the CAD system,
providing common attributes and methods that all shapes must implement.
"""

import uuid
from abc import ABC, abstractmethod
from typing import Any, Optional

from pydantic import BaseModel

from cad_datamodel.core.exceptions import ShapeValidationError
from cad_datamodel.core.types import Bounds, ShapeType, Transform


class Style(BaseModel):
    """Visual styling properties for shapes.

    This is a placeholder until the full styles module is implemented.
    """

    fill_color: Optional[str] = None
    stroke_color: Optional[str] = None
    stroke_width: float = 1.0
    fill_opacity: float = 1.0
    stroke_opacity: float = 1.0


class IShape(ABC):
    """Abstract base class for all shape types in the CAD system.

    This interface defines the contract that all shapes must follow,
    ensuring consistent behavior across different shape types.
    """

    @property
    @abstractmethod
    def id(self) -> str:
        """Get the unique identifier of the shape."""
        pass

    @property
    @abstractmethod
    def type(self) -> ShapeType:
        """Get the type of the shape."""
        pass

    @abstractmethod
    def get_bounds(self) -> Bounds:
        """Calculate the axis-aligned bounding box of the shape.

        Returns:
            Bounds object representing the shape's bounding box
        """
        pass

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Serialize the shape to a dictionary.

        Returns:
            Dictionary representation of the shape
        """
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> "IShape":
        """Deserialize a shape from a dictionary.

        Args:
            data: Dictionary containing shape data

        Returns:
            Shape instance

        Raises:
            ShapeValidationError: If the data is invalid
        """
        pass


class Shape(IShape):
    """Base implementation of a shape with common attributes.

    This class provides the foundation for all concrete shape types,
    implementing common functionality and enforcing immutability.
    """

    def __init__(
        self,
        *,
        shape_type: ShapeType,
        layer_id: str,
        group_id: Optional[str] = None,
        visible: bool = True,
        locked: bool = False,
        style: Optional[Style] = None,
        transform: Optional[Transform] = None,
        metadata: Optional[dict[str, Any]] = None,
        shape_id: Optional[str] = None,
    ):
        """Initialize a shape with common attributes.

        Args:
            shape_type: The type of shape being created
            layer_id: ID of the layer containing this shape
            group_id: Optional ID of parent group
            visible: Whether the shape is visible
            locked: Whether the shape is locked for editing
            style: Visual styling information
            transform: Transformation matrix
            metadata: Additional user-defined metadata
            shape_id: Optional explicit ID (auto-generated if not provided)
        """
        self._id = shape_id or str(uuid.uuid4())
        self._type = shape_type
        self._layer_id = layer_id
        self._group_id = group_id
        self._visible = visible
        self._locked = locked
        self._style = style or Style()
        self._transform = transform or Transform.identity()
        self._metadata = metadata or {}

        # Validate layer_id is not empty
        if not layer_id:
            raise ShapeValidationError(
                shape_type.name, "layer_id cannot be empty", self._id
            )

    @property
    def id(self) -> str:
        """Get the unique identifier of the shape."""
        return self._id

    @property
    def type(self) -> ShapeType:
        """Get the type of the shape."""
        return self._type

    @property
    def layer_id(self) -> str:
        """Get the ID of the layer containing this shape."""
        return self._layer_id

    @property
    def group_id(self) -> Optional[str]:
        """Get the ID of the parent group, if any."""
        return self._group_id

    @property
    def visible(self) -> bool:
        """Check if the shape is visible."""
        return self._visible

    @property
    def locked(self) -> bool:
        """Check if the shape is locked for editing."""
        return self._locked

    @property
    def style(self) -> Style:
        """Get the shape's visual styling."""
        return self._style

    @property
    def transform(self) -> Transform:
        """Get the shape's transformation matrix."""
        return self._transform

    @property
    def metadata(self) -> dict[str, Any]:
        """Get the shape's metadata."""
        return self._metadata.copy()  # Return a copy to maintain immutability

    def apply_transform(self, transform: Transform) -> "Shape":
        """Apply a transformation to create a new transformed shape.

        This method must be overridden by concrete shape classes to
        handle shape-specific transformation logic.

        Args:
            transform: The transformation to apply

        Returns:
            New shape instance with applied transformation
        """
        raise NotImplementedError("Concrete shapes must implement apply_transform")

    def to_dict(self) -> dict[str, Any]:
        """Serialize the shape to a dictionary.

        Returns:
            Dictionary representation of the shape
        """
        return {
            "id": self._id,
            "type": self._type.name,
            "layer_id": self._layer_id,
            "group_id": self._group_id,
            "visible": self._visible,
            "locked": self._locked,
            "style": self._style.model_dump(),
            "transform": self._transform.matrix.tolist(),
            "metadata": self._metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Shape":
        """Base deserialization method.

        This should be overridden by concrete shape classes.
        """
        raise NotImplementedError("Concrete shapes must implement from_dict")

    def __repr__(self) -> str:
        """String representation of the shape."""
        return f"{self.__class__.__name__}(id={self._id}, type={self._type.name})"
