"""Unit tests for the core module."""

from unittest.mock import Mock

import numpy as np
import pytest

from cad_datamodel.core import (
    DEFAULT_FILL_COLOR,
    DEFAULT_STROKE_COLOR,
    # Constants
    DEFAULT_STROKE_WIDTH,
    MAX_COORDINATE,
    MIN_COORDINATE,
    NAMED_COLORS,
    Bounds,
    # Exceptions
    CADError,
    Color,
    DocumentError,
    GeometryError,
    GroupError,
    IRenderer,
    ISerializer,
    # Base interfaces
    IShape,
    LayerError,
    LineCap,
    LineJoin,
    Point,
    ReferenceError,
    SerializationError,
    # Types
    ShapeType,
    ShapeValidationError,
    Transform,
    TransformError,
    Units,
)


class TestShapeType:
    """Test ShapeType enumeration."""

    def test_shape_types_exist(self):
        """Test all shape types are defined."""
        assert ShapeType.RECTANGLE
        assert ShapeType.CIRCLE
        assert ShapeType.LINE
        assert ShapeType.POLYGON
        assert ShapeType.POLYLINE
        assert ShapeType.GROUP

    def test_shape_type_uniqueness(self):
        """Test shape types have unique values."""
        values = [shape.value for shape in ShapeType]
        assert len(values) == len(set(values))


class TestLineCap:
    """Test LineCap enumeration."""

    def test_line_caps_exist(self):
        """Test all line cap styles are defined."""
        assert LineCap.BUTT.value == "butt"
        assert LineCap.ROUND.value == "round"
        assert LineCap.SQUARE.value == "square"


class TestLineJoin:
    """Test LineJoin enumeration."""

    def test_line_joins_exist(self):
        """Test all line join styles are defined."""
        assert LineJoin.MITER.value == "miter"
        assert LineJoin.ROUND.value == "round"
        assert LineJoin.BEVEL.value == "bevel"


class TestUnits:
    """Test Units enumeration."""

    def test_units_exist(self):
        """Test all units are defined."""
        assert Units.PIXELS.value == "px"
        assert Units.MILLIMETERS.value == "mm"
        assert Units.CENTIMETERS.value == "cm"
        assert Units.INCHES.value == "in"
        assert Units.POINTS.value == "pt"


class TestPoint:
    """Test Point class."""

    def test_point_creation(self):
        """Test creating a point."""
        p = Point(10.5, 20.3)
        assert p.x == 10.5
        assert p.y == 20.3

    def test_point_string_representation(self):
        """Test point string representation."""
        p = Point(10, 20)
        assert str(p) == "Point(10, 20)"

    def test_point_immutability(self):
        """Test that points are immutable."""
        p = Point(10, 20)
        with pytest.raises(AttributeError):
            p.x = 30


class TestBounds:
    """Test Bounds class."""

    def test_bounds_creation(self):
        """Test creating bounds."""
        b = Bounds(Point(0, 0), Point(100, 200))
        assert b.min_point == Point(0, 0)
        assert b.max_point == Point(100, 200)

    def test_bounds_width_height(self):
        """Test bounds width and height calculation."""
        b = Bounds(Point(10, 20), Point(110, 220))
        assert b.width == 100
        assert b.height == 200

    def test_bounds_center(self):
        """Test bounds center calculation."""
        b = Bounds(Point(0, 0), Point(100, 200))
        assert b.center == Point(50, 100)

    def test_bounds_contains_point(self):
        """Test point containment check."""
        b = Bounds(Point(0, 0), Point(100, 100))

        # Points inside
        assert b.contains_point(Point(50, 50))
        assert b.contains_point(Point(0, 0))
        assert b.contains_point(Point(100, 100))

        # Points outside
        assert not b.contains_point(Point(-1, 50))
        assert not b.contains_point(Point(101, 50))
        assert not b.contains_point(Point(50, -1))
        assert not b.contains_point(Point(50, 101))

    def test_bounds_intersection(self):
        """Test bounds intersection check."""
        b1 = Bounds(Point(0, 0), Point(100, 100))

        # Overlapping bounds
        b2 = Bounds(Point(50, 50), Point(150, 150))
        assert b1.intersects(b2)
        assert b2.intersects(b1)

        # Non-overlapping bounds
        b3 = Bounds(Point(200, 200), Point(300, 300))
        assert not b1.intersects(b3)
        assert not b3.intersects(b1)

        # Touching bounds
        b4 = Bounds(Point(100, 0), Point(200, 100))
        assert b1.intersects(b4)


class TestColor:
    """Test Color class."""

    def test_color_creation(self):
        """Test creating colors."""
        c = Color(red=255, green=128, blue=64)
        assert c.red == 255
        assert c.green == 128
        assert c.blue == 64
        assert c.alpha == 255  # Default alpha

    def test_color_with_alpha(self):
        """Test creating color with alpha."""
        c = Color(red=255, green=128, blue=64, alpha=128)
        assert c.alpha == 128

    def test_color_validation(self):
        """Test color value validation."""
        with pytest.raises(ValueError):
            Color(red=256, green=0, blue=0)
        with pytest.raises(ValueError):
            Color(red=-1, green=0, blue=0)

    def test_color_from_hex(self):
        """Test creating color from hex string."""
        # 6-digit hex
        c1 = Color.from_hex("#FF8040")
        assert c1.red == 255
        assert c1.green == 128
        assert c1.blue == 64
        assert c1.alpha == 255

        # Without hash
        c2 = Color.from_hex("FF8040")
        assert c2.red == 255
        assert c2.green == 128
        assert c2.blue == 64

        # 8-digit hex with alpha
        c3 = Color.from_hex("#FF804080")
        assert c3.red == 255
        assert c3.green == 128
        assert c3.blue == 64
        assert c3.alpha == 128

        # Invalid hex
        with pytest.raises(ValueError):
            Color.from_hex("GGGGGG")
        with pytest.raises(ValueError):
            Color.from_hex("FF")

    def test_color_to_hex(self):
        """Test converting color to hex string."""
        c = Color(red=255, green=128, blue=64, alpha=128)

        assert c.to_hex() == "#ff8040"
        assert c.to_hex(include_alpha=True) == "#ff804080"

    def test_color_to_rgba_tuple(self):
        """Test converting color to RGBA tuple."""
        c = Color(red=255, green=128, blue=64, alpha=192)
        assert c.to_rgba_tuple() == (255, 128, 64, 192)

    def test_color_with_alpha_method(self):
        """Test creating new color with different alpha."""
        c1 = Color(red=255, green=128, blue=64)
        c2 = c1.with_alpha(128)

        assert c2.red == 255
        assert c2.green == 128
        assert c2.blue == 64
        assert c2.alpha == 128
        assert c1.alpha == 255  # Original unchanged


class TestTransform:
    """Test Transform class."""

    def test_identity_transform(self):
        """Test identity transform creation."""
        t = Transform.identity()
        expected = np.eye(3)
        assert np.allclose(t.matrix, expected)

    def test_translation_transform(self):
        """Test translation transform."""
        t = Transform.translation(10, 20)
        p = t.apply_to_point(Point(5, 5))
        assert p.x == 15
        assert p.y == 25

    def test_rotation_transform(self):
        """Test rotation transform."""
        # 90 degree rotation around origin
        t = Transform.rotation(90)
        p = t.apply_to_point(Point(10, 0))
        assert abs(p.x - 0) < 1e-10
        assert abs(p.y - 10) < 1e-10

        # 90 degree rotation around center
        t2 = Transform.rotation(90, center=Point(10, 10))
        p2 = t2.apply_to_point(Point(20, 10))
        assert abs(p2.x - 10) < 1e-10
        assert abs(p2.y - 20) < 1e-10

    def test_scale_transform(self):
        """Test scale transform."""
        # Uniform scale
        t1 = Transform.scale(2)
        p1 = t1.apply_to_point(Point(10, 20))
        assert p1.x == 20
        assert p1.y == 40

        # Non-uniform scale
        t2 = Transform.scale(2, 3)
        p2 = t2.apply_to_point(Point(10, 20))
        assert p2.x == 20
        assert p2.y == 60

        # Scale with center
        t3 = Transform.scale(2, center=Point(10, 10))
        p3 = t3.apply_to_point(Point(20, 20))
        assert p3.x == 30
        assert p3.y == 30

    def test_transform_composition(self):
        """Test composing transforms."""
        t1 = Transform.translation(10, 0)
        t2 = Transform.rotation(90)
        t3 = t1.compose(t2)

        p = t3.apply_to_point(Point(0, 0))
        assert p.x == 10
        assert p.y == 0

    def test_transform_inverse(self):
        """Test transform inverse."""
        t = Transform.translation(10, 20)
        t_inv = t.inverse()

        p = Point(50, 60)
        p_transformed = t.apply_to_point(p)
        p_back = t_inv.apply_to_point(p_transformed)

        assert abs(p_back.x - p.x) < 1e-10
        assert abs(p_back.y - p.y) < 1e-10

    def test_non_invertible_transform(self):
        """Test error for non-invertible transform."""
        # Create singular matrix
        matrix = np.array([[1, 0, 0], [0, 0, 0], [0, 0, 1]])
        t = Transform(matrix)

        with pytest.raises(ValueError, match="Transform is not invertible"):
            t.inverse()

    def test_transform_equality(self):
        """Test transform equality comparison."""
        t1 = Transform.translation(10, 20)
        t2 = Transform.translation(10, 20)
        t3 = Transform.translation(10, 30)

        assert t1 == t2
        assert t1 != t3
        assert t1 != "not a transform"

    def test_transform_repr(self):
        """Test transform string representation."""
        t = Transform.identity()
        repr_str = repr(t)
        assert "Transform" in repr_str
        assert "[[1" in repr_str  # Check matrix is shown

    def test_invalid_matrix_shape(self):
        """Test error for invalid matrix shape."""
        with pytest.raises(ValueError, match="Transform matrix must be 3x3"):
            Transform(np.eye(2))


class TestExceptions:
    """Test exception hierarchy."""

    def test_cad_error_base(self):
        """Test CADError base exception."""
        err = CADError("Test error", {"key": "value"})
        assert str(err) == "Test error"
        assert err.message == "Test error"
        assert err.details == {"key": "value"}

    def test_shape_validation_error(self):
        """Test ShapeValidationError."""
        err = ShapeValidationError("Rectangle", "Invalid dimensions", "shape-123")
        assert "Rectangle" in str(err)
        assert "Invalid dimensions" in str(err)
        assert err.details["shape_id"] == "shape-123"

    def test_layer_error(self):
        """Test LayerError."""
        err = LayerError("add", "layer-123", "Layer already exists")
        assert "add" in str(err)
        assert "Layer already exists" in str(err)
        assert err.details["layer_id"] == "layer-123"

    def test_transform_error(self):
        """Test TransformError."""
        err = TransformError("rotation", "Invalid angle")
        assert "rotation" in str(err)
        assert "Invalid angle" in str(err)

    def test_serialization_error(self):
        """Test SerializationError."""
        err = SerializationError("serialize", "JSON", "Invalid data", "Shape")
        assert "serialize" in str(err)
        assert "JSON" in str(err)
        assert "Shape" in str(err)

    def test_group_error(self):
        """Test GroupError."""
        err = GroupError("group-123", "add_child", "Circular reference")
        assert "group-123" in str(err)
        assert "add_child" in str(err)
        assert "Circular reference" in str(err)

    def test_document_error(self):
        """Test DocumentError."""
        err = DocumentError("version", "Unsupported version", "doc-123")
        assert "version" in str(err)
        assert "Unsupported version" in str(err)
        assert err.details["document_id"] == "doc-123"

    def test_reference_error(self):
        """Test ReferenceError."""
        err = ReferenceError("layer", "layer-999", "shape-123")
        assert "layer" in str(err)
        assert "layer-999" in str(err)
        assert "shape-123" in str(err)

    def test_geometry_error(self):
        """Test GeometryError."""
        err = GeometryError(
            "intersection", "No intersection found", ["shape1", "shape2"]
        )
        assert "intersection" in str(err)
        assert "No intersection found" in str(err)
        assert err.details["shape_ids"] == ["shape1", "shape2"]


class TestConstants:
    """Test constants are properly defined."""

    def test_default_values(self):
        """Test default style values."""
        assert DEFAULT_STROKE_WIDTH == 1.0
        assert Color(red=0, green=0, blue=0, alpha=255) == DEFAULT_STROKE_COLOR
        assert Color(red=255, green=255, blue=255, alpha=255) == DEFAULT_FILL_COLOR

    def test_coordinate_limits(self):
        """Test coordinate system limits."""
        assert MIN_COORDINATE == -1e6
        assert MAX_COORDINATE == 1e6

    def test_named_colors(self):
        """Test named colors dictionary."""
        assert NAMED_COLORS["black"] == Color(red=0, green=0, blue=0)
        assert NAMED_COLORS["white"] == Color(red=255, green=255, blue=255)
        assert NAMED_COLORS["red"] == Color(red=255, green=0, blue=0)
        assert "transparent" in NAMED_COLORS


class TestIShape:
    """Test IShape interface."""

    def test_abstract_interface(self):
        """Test that IShape cannot be instantiated directly."""
        with pytest.raises(TypeError):
            IShape()

    def test_mock_implementation(self):
        """Test mocking IShape for testing."""
        # Create a mock shape
        mock_shape = Mock(spec=IShape)

        # Set up properties
        mock_shape.id = "shape-123"
        mock_shape.type = ShapeType.RECTANGLE
        mock_shape.layer_id = "layer-1"
        mock_shape.group_id = None
        mock_shape.visible = True
        mock_shape.locked = False
        mock_shape.transform = Transform.identity()
        mock_shape.metadata = {"custom": "data"}

        # Set up methods
        mock_shape.get_bounds.return_value = Bounds(Point(0, 0), Point(100, 100))
        mock_shape.contains_point.return_value = True

        # Test the mock
        assert mock_shape.id == "shape-123"
        assert mock_shape.type == ShapeType.RECTANGLE
        assert mock_shape.get_bounds() == Bounds(Point(0, 0), Point(100, 100))
        assert mock_shape.contains_point(Point(50, 50))


class TestIRenderer:
    """Test IRenderer interface."""

    def test_abstract_interface(self):
        """Test that IRenderer cannot be instantiated directly."""
        with pytest.raises(TypeError):
            IRenderer()

    def test_mock_implementation(self):
        """Test mocking IRenderer for testing."""
        mock_renderer = Mock(spec=IRenderer)
        mock_shape = Mock(spec=IShape)

        # Set up render methods
        mock_renderer.render_shape.return_value = "<rect/>"
        mock_renderer.render_layer.return_value = "<g></g>"
        mock_renderer.render_document.return_value = "<svg></svg>"

        # Test rendering
        assert mock_renderer.render_shape(mock_shape) == "<rect/>"
        assert mock_renderer.render_layer([mock_shape]) == "<g></g>"
        assert mock_renderer.render_document({}, 800, 600) == "<svg></svg>"


class TestISerializer:
    """Test ISerializer interface."""

    def test_abstract_interface(self):
        """Test that ISerializer cannot be instantiated directly."""
        with pytest.raises(TypeError):
            ISerializer()

    def test_mock_implementation(self):
        """Test mocking ISerializer for testing."""
        mock_serializer = Mock(spec=ISerializer)
        mock_shape = Mock(spec=IShape)

        # Set up serialization methods
        shape_data = {"id": "shape-123", "type": "rectangle"}
        mock_serializer.serialize_shape.return_value = shape_data
        mock_serializer.deserialize_shape.return_value = mock_shape

        # Test serialization
        assert mock_serializer.serialize_shape(mock_shape) == shape_data
        assert mock_serializer.deserialize_shape(shape_data) == mock_shape
