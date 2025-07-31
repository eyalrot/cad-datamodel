"""Base classes and interfaces for CAD datamodel.

This module defines the fundamental abstract base classes and interfaces
that all CAD entities must implement.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional

from .types import Bounds, Point, ShapeType, Transform


class IShape(ABC):
    """Abstract base class for all shape types in the CAD system.

    This interface defines the contract that all shapes must implement.
    Shapes are the fundamental drawing elements in the CAD system.

    Attributes:
        id: Unique identifier for the shape (UUID)
        type: The type of shape (rectangle, circle, etc.)
        layer_id: ID of the layer this shape belongs to
        group_id: ID of the parent group (if any)
        visible: Whether the shape is visible
        locked: Whether the shape is locked for editing
        style: Visual styling properties
        transform: Transformation matrix
        metadata: Extensible metadata dictionary
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

    @property
    @abstractmethod
    def layer_id(self) -> str:
        """Get the ID of the layer this shape belongs to."""
        pass

    @property
    @abstractmethod
    def group_id(self) -> Optional[str]:
        """Get the ID of the parent group, if any."""
        pass

    @property
    @abstractmethod
    def visible(self) -> bool:
        """Check if the shape is visible."""
        pass

    @property
    @abstractmethod
    def locked(self) -> bool:
        """Check if the shape is locked for editing."""
        pass

    @property
    @abstractmethod
    def transform(self) -> Transform:
        """Get the transformation matrix for this shape."""
        pass

    @property
    @abstractmethod
    def metadata(self) -> dict[str, Any]:
        """Get the metadata dictionary for custom properties."""
        pass

    @abstractmethod
    def get_bounds(self) -> Bounds:
        """Calculate and return the bounding box of the shape.

        Returns:
            Bounds object containing min and max points
        """
        pass

    @abstractmethod
    def contains_point(self, point: Point) -> bool:
        """Check if a point lies within the shape.

        Args:
            point: The point to test

        Returns:
            True if the point is inside the shape
        """
        pass

    @abstractmethod
    def apply_transform(self, transform: Transform) -> None:
        """Apply a transformation to the shape.

        Args:
            transform: The transformation matrix to apply
        """
        pass

    @abstractmethod
    def validate(self) -> None:
        """Validate the shape's properties.

        Raises:
            ShapeValidationError: If the shape is invalid
        """
        pass


class IRenderer(ABC):
    """Abstract interface for rendering shapes to various output formats.

    This interface implements the Strategy pattern for rendering,
    allowing different rendering backends to be used interchangeably.
    """

    @abstractmethod
    def render_shape(self, shape: IShape) -> Any:
        """Render a single shape.

        Args:
            shape: The shape to render

        Returns:
            Format-specific representation of the shape
        """
        pass

    @abstractmethod
    def render_layer(self, shapes: list[IShape]) -> Any:
        """Render all shapes in a layer.

        Args:
            shapes: List of shapes in rendering order

        Returns:
            Format-specific representation of the layer
        """
        pass

    @abstractmethod
    def render_document(self, layers: dict[str, list[IShape]],
                       canvas_width: float, canvas_height: float) -> Any:
        """Render an entire document.

        Args:
            layers: Dictionary mapping layer IDs to shape lists
            canvas_width: Width of the canvas
            canvas_height: Height of the canvas

        Returns:
            Format-specific representation of the document
        """
        pass


class ISerializer(ABC):
    """Abstract interface for serializing and deserializing CAD data.

    This interface supports various persistence formats while maintaining
    data fidelity and relationships.
    """

    @abstractmethod
    def serialize_shape(self, shape: IShape) -> dict[str, Any]:
        """Serialize a shape to a dictionary.

        Args:
            shape: The shape to serialize

        Returns:
            Dictionary representation of the shape
        """
        pass

    @abstractmethod
    def deserialize_shape(self, data: dict[str, Any]) -> IShape:
        """Deserialize a shape from a dictionary.

        Args:
            data: Dictionary containing shape data

        Returns:
            Reconstructed shape object

        Raises:
            SerializationError: If deserialization fails
        """
        pass

    @abstractmethod
    def serialize_document(self, document: Any) -> dict[str, Any]:
        """Serialize an entire document.

        Args:
            document: The document to serialize

        Returns:
            Dictionary representation of the document
        """
        pass

    @abstractmethod
    def deserialize_document(self, data: dict[str, Any]) -> Any:
        """Deserialize a document from a dictionary.

        Args:
            data: Dictionary containing document data

        Returns:
            Reconstructed document object

        Raises:
            SerializationError: If deserialization fails
        """
        pass
