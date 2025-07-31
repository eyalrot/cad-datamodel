"""Type definitions for the CAD datamodel.

This module contains all type definitions, enumerations, and type aliases
used throughout the CAD system.
"""

from enum import Enum, auto
from typing import NamedTuple, Optional

import numpy as np
from pydantic import BaseModel, Field
from typing_extensions import TypeAlias


class ShapeType(Enum):
    """Enumeration of all supported shape types."""

    RECTANGLE = auto()
    CIRCLE = auto()
    LINE = auto()
    POLYGON = auto()
    POLYLINE = auto()
    GROUP = auto()


class LineCap(Enum):
    """Line cap styles for strokes."""

    BUTT = "butt"
    ROUND = "round"
    SQUARE = "square"


class LineJoin(Enum):
    """Line join styles for strokes."""

    MITER = "miter"
    ROUND = "round"
    BEVEL = "bevel"


class Units(Enum):
    """Measurement units for the document."""

    PIXELS = "px"
    MILLIMETERS = "mm"
    CENTIMETERS = "cm"
    INCHES = "in"
    POINTS = "pt"


# Type aliases for clarity and type safety
Coordinate: TypeAlias = float
Angle: TypeAlias = float  # In degrees
Opacity: TypeAlias = float  # 0.0 to 1.0


class Point(NamedTuple):
    """2D point representation."""

    x: Coordinate
    y: Coordinate

    def __str__(self) -> str:
        return f"Point({self.x}, {self.y})"


class Bounds(NamedTuple):
    """Axis-aligned bounding box."""

    min_point: Point
    max_point: Point

    @property
    def width(self) -> float:
        """Calculate the width of the bounds."""
        return self.max_point.x - self.min_point.x

    @property
    def height(self) -> float:
        """Calculate the height of the bounds."""
        return self.max_point.y - self.min_point.y

    @property
    def center(self) -> Point:
        """Calculate the center point of the bounds."""
        return Point(
            (self.min_point.x + self.max_point.x) / 2,
            (self.min_point.y + self.max_point.y) / 2
        )

    def contains_point(self, point: Point) -> bool:
        """Check if a point is within the bounds.

        Args:
            point: The point to test

        Returns:
            True if the point is inside the bounds
        """
        return (self.min_point.x <= point.x <= self.max_point.x and
                self.min_point.y <= point.y <= self.max_point.y)

    def intersects(self, other: 'Bounds') -> bool:
        """Check if this bounds intersects with another.

        Args:
            other: The other bounds to test

        Returns:
            True if the bounds intersect
        """
        return not (self.max_point.x < other.min_point.x or
                   self.min_point.x > other.max_point.x or
                   self.max_point.y < other.min_point.y or
                   self.min_point.y > other.max_point.y)


class Color(BaseModel):
    """Color representation with support for various formats.

    Colors can be created from hex strings, RGB tuples, or named colors.
    Internal representation is always RGBA with values 0-255.
    """

    red: int = Field(ge=0, le=255)
    green: int = Field(ge=0, le=255)
    blue: int = Field(ge=0, le=255)
    alpha: int = Field(default=255, ge=0, le=255)

    @classmethod
    def from_hex(cls, hex_string: str) -> 'Color':
        """Create a color from a hex string.

        Args:
            hex_string: Hex color string (e.g., "#FF0000" or "FF0000")

        Returns:
            Color object
        """
        hex_string = hex_string.lstrip('#')
        if len(hex_string) == 6:
            r, g, b = int(hex_string[0:2], 16), int(hex_string[2:4], 16), int(hex_string[4:6], 16)
            return cls(red=r, green=g, blue=b)
        elif len(hex_string) == 8:
            r, g, b, a = (int(hex_string[0:2], 16), int(hex_string[2:4], 16),
                         int(hex_string[4:6], 16), int(hex_string[6:8], 16))
            return cls(red=r, green=g, blue=b, alpha=a)
        else:
            raise ValueError(f"Invalid hex color string: {hex_string}")

    def to_hex(self, include_alpha: bool = False) -> str:
        """Convert color to hex string.

        Args:
            include_alpha: Whether to include alpha channel

        Returns:
            Hex color string
        """
        if include_alpha:
            return f"#{self.red:02x}{self.green:02x}{self.blue:02x}{self.alpha:02x}"
        return f"#{self.red:02x}{self.green:02x}{self.blue:02x}"

    def to_rgba_tuple(self) -> tuple[int, int, int, int]:
        """Convert to RGBA tuple."""
        return (self.red, self.green, self.blue, self.alpha)

    def with_alpha(self, alpha: int) -> 'Color':
        """Create a new color with different alpha value.

        Args:
            alpha: New alpha value (0-255)

        Returns:
            New Color object with updated alpha
        """
        return Color(red=self.red, green=self.green, blue=self.blue, alpha=alpha)


class Transform:
    """2D affine transformation matrix.

    Represents transformations using a 3x3 matrix for 2D homogeneous coordinates.
    Supports translation, rotation, scaling, and arbitrary affine transformations.
    """

    def __init__(self, matrix: Optional[np.ndarray[tuple[int, int], np.dtype[np.float64]]] = None):
        """Initialize transform with optional matrix.

        Args:
            matrix: 3x3 numpy array, or None for identity transform
        """
        if matrix is None:
            self._matrix = np.eye(3, dtype=np.float64)
        else:
            if matrix.shape != (3, 3):
                raise ValueError("Transform matrix must be 3x3")
            self._matrix = matrix.astype(np.float64)

    @classmethod
    def identity(cls) -> 'Transform':
        """Create an identity transform."""
        return cls()

    @classmethod
    def translation(cls, dx: float, dy: float) -> 'Transform':
        """Create a translation transform.

        Args:
            dx: X-axis translation
            dy: Y-axis translation

        Returns:
            New Transform object
        """
        matrix = np.array([
            [1, 0, dx],
            [0, 1, dy],
            [0, 0, 1]
        ], dtype=np.float64)
        return cls(matrix)

    @classmethod
    def rotation(cls, angle: float, center: Optional[Point] = None) -> 'Transform':
        """Create a rotation transform.

        Args:
            angle: Rotation angle in degrees
            center: Center of rotation (default: origin)

        Returns:
            New Transform object
        """
        rad = np.radians(angle)
        cos_a = np.cos(rad)
        sin_a = np.sin(rad)

        if center is None:
            matrix = np.array([
                [cos_a, -sin_a, 0],
                [sin_a, cos_a, 0],
                [0, 0, 1]
            ], dtype=np.float64)
        else:
            # Translate to origin, rotate, translate back
            cx, cy = center.x, center.y
            matrix = np.array([
                [cos_a, -sin_a, cx - cx * cos_a + cy * sin_a],
                [sin_a, cos_a, cy - cx * sin_a - cy * cos_a],
                [0, 0, 1]
            ], dtype=np.float64)

        return cls(matrix)

    @classmethod
    def scale(cls, sx: float, sy: Optional[float] = None,
              center: Optional[Point] = None) -> 'Transform':
        """Create a scale transform.

        Args:
            sx: X-axis scale factor
            sy: Y-axis scale factor (default: same as sx)
            center: Center of scaling (default: origin)

        Returns:
            New Transform object
        """
        if sy is None:
            sy = sx

        if center is None:
            matrix = np.array([
                [sx, 0, 0],
                [0, sy, 0],
                [0, 0, 1]
            ], dtype=np.float64)
        else:
            # Translate to origin, scale, translate back
            cx, cy = center.x, center.y
            matrix = np.array([
                [sx, 0, cx * (1 - sx)],
                [0, sy, cy * (1 - sy)],
                [0, 0, 1]
            ], dtype=np.float64)

        return cls(matrix)

    def compose(self, other: 'Transform') -> 'Transform':
        """Compose this transform with another.

        Args:
            other: Transform to compose with

        Returns:
            New Transform representing the composition
        """
        return Transform(self._matrix @ other._matrix)

    def apply_to_point(self, point: Point) -> Point:
        """Apply transform to a point.

        Args:
            point: Point to transform

        Returns:
            Transformed point
        """
        vec = np.array([point.x, point.y, 1])
        result = self._matrix @ vec
        return Point(result[0], result[1])

    def inverse(self) -> 'Transform':
        """Calculate the inverse transform.

        Returns:
            Inverse transform

        Raises:
            ValueError: If transform is not invertible
        """
        try:
            inv_matrix = np.linalg.inv(self._matrix)
            return Transform(inv_matrix)
        except np.linalg.LinAlgError as e:
            raise ValueError("Transform is not invertible") from e

    @property
    def matrix(self) -> np.ndarray[tuple[int, int], np.dtype[np.float64]]:
        """Get the underlying transformation matrix."""
        return self._matrix.copy()

    def __eq__(self, other: object) -> bool:
        """Check if two transforms are equal."""
        if not isinstance(other, Transform):
            return False
        return np.allclose(self._matrix, other._matrix)

    def __repr__(self) -> str:
        """String representation of the transform."""
        return f"Transform({self._matrix.tolist()})"
