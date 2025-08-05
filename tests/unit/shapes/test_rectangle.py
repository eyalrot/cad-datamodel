"""Unit tests for the Rectangle shape implementation."""

import uuid

import numpy as np
import pytest

from cad_datamodel.core.exceptions import ShapeValidationError
from cad_datamodel.core.types import Point, ShapeType, Transform
from cad_datamodel.shapes import Rectangle, ShapeFactory, Style


class TestRectangleCreation:
    """Test rectangle creation and validation."""

    def test_create_basic_rectangle(self):
        """Test creating a basic rectangle with required parameters."""
        rect = Rectangle(x=10.0, y=20.0, width=100.0, height=50.0, layer_id="layer1")

        assert rect.x == 10.0
        assert rect.y == 20.0
        assert rect.width == 100.0
        assert rect.height == 50.0
        assert rect.corner_radius == 0.0
        assert rect.layer_id == "layer1"
        assert rect.type == ShapeType.RECTANGLE
        assert isinstance(rect.id, str)
        assert rect.visible is True
        assert rect.locked is False

    def test_create_rectangle_with_all_parameters(self):
        """Test creating a rectangle with all optional parameters."""
        style = Style(fill_color="#FF0000", stroke_color="#000000")
        transform = Transform.translation(5.0, 10.0)
        metadata = {"name": "Test Rectangle"}
        shape_id = str(uuid.uuid4())

        rect = Rectangle(
            x=0.0,
            y=0.0,
            width=200.0,
            height=100.0,
            corner_radius=10.0,
            layer_id="layer2",
            group_id="group1",
            visible=False,
            locked=True,
            style=style,
            transform=transform,
            metadata=metadata,
            shape_id=shape_id,
        )

        assert rect.x == 0.0
        assert rect.y == 0.0
        assert rect.width == 200.0
        assert rect.height == 100.0
        assert rect.corner_radius == 10.0
        assert rect.layer_id == "layer2"
        assert rect.group_id == "group1"
        assert rect.visible is False
        assert rect.locked is True
        assert rect.style == style
        assert rect.transform == transform
        assert rect.metadata == metadata
        assert rect.id == shape_id

    def test_rectangle_immutability(self):
        """Test that rectangle attributes are immutable."""
        rect = Rectangle(x=10, y=20, width=100, height=50, layer_id="layer1")

        # Test that attributes don't have setters
        with pytest.raises(AttributeError):
            rect.x = 20  # type: ignore

        with pytest.raises(AttributeError):
            rect.width = 200  # type: ignore

        with pytest.raises(AttributeError):
            rect.layer_id = "layer2"  # type: ignore

    def test_metadata_copy(self):
        """Test that metadata returns a copy, not the original."""
        metadata = {"key": "value"}
        rect = Rectangle(
            x=0, y=0, width=100, height=50, layer_id="layer1", metadata=metadata
        )

        # Modify the returned metadata
        returned_metadata = rect.metadata
        returned_metadata["key"] = "modified"

        # Original should be unchanged
        assert rect.metadata["key"] == "value"


class TestRectangleValidation:
    """Test rectangle parameter validation."""

    def test_negative_width_raises_error(self):
        """Test that negative width raises ShapeValidationError."""
        with pytest.raises(ShapeValidationError) as excinfo:
            Rectangle(x=0, y=0, width=-10, height=50, layer_id="layer1")

        assert "Width must be positive" in str(excinfo.value)
        assert excinfo.value.details["shape_type"] == "RECTANGLE"

    def test_zero_width_raises_error(self):
        """Test that zero width raises ShapeValidationError."""
        with pytest.raises(ShapeValidationError) as excinfo:
            Rectangle(x=0, y=0, width=0, height=50, layer_id="layer1")

        assert "Width must be positive" in str(excinfo.value)

    def test_negative_height_raises_error(self):
        """Test that negative height raises ShapeValidationError."""
        with pytest.raises(ShapeValidationError) as excinfo:
            Rectangle(x=0, y=0, width=100, height=-20, layer_id="layer1")

        assert "Height must be positive" in str(excinfo.value)

    def test_zero_height_raises_error(self):
        """Test that zero height raises ShapeValidationError."""
        with pytest.raises(ShapeValidationError) as excinfo:
            Rectangle(x=0, y=0, width=100, height=0, layer_id="layer1")

        assert "Height must be positive" in str(excinfo.value)

    def test_negative_corner_radius_raises_error(self):
        """Test that negative corner radius raises ShapeValidationError."""
        with pytest.raises(ShapeValidationError) as excinfo:
            Rectangle(
                x=0, y=0, width=100, height=50, corner_radius=-5, layer_id="layer1"
            )

        assert "Corner radius cannot be negative" in str(excinfo.value)

    def test_corner_radius_exceeds_limit(self):
        """Test that excessive corner radius raises ShapeValidationError."""
        with pytest.raises(ShapeValidationError) as excinfo:
            Rectangle(
                x=0,
                y=0,
                width=100,
                height=50,
                corner_radius=30,
                layer_id="layer1",  # Max should be 25
            )

        assert "exceeds maximum allowed" in str(excinfo.value)

    def test_empty_layer_id_raises_error(self):
        """Test that empty layer_id raises ShapeValidationError."""
        with pytest.raises(ShapeValidationError) as excinfo:
            Rectangle(x=0, y=0, width=100, height=50, layer_id="")

        assert "layer_id cannot be empty" in str(excinfo.value)

    def test_corner_radius_at_limit(self):
        """Test corner radius at exactly half the smaller dimension."""
        # Should not raise
        rect = Rectangle(
            x=0, y=0, width=100, height=50, corner_radius=25, layer_id="layer1"
        )
        assert rect.corner_radius == 25.0


class TestRectangleBounds:
    """Test rectangle bounds calculation."""

    def test_basic_bounds_no_transform(self):
        """Test bounds calculation without transformation."""
        rect = Rectangle(x=10, y=20, width=100, height=50, layer_id="layer1")
        bounds = rect.get_bounds()

        assert bounds.min_point == Point(10, 20)
        assert bounds.max_point == Point(110, 70)
        assert bounds.width == 100
        assert bounds.height == 50
        assert bounds.center == Point(60, 45)

    def test_bounds_with_translation(self):
        """Test bounds calculation with translation transform."""
        transform = Transform.translation(15, 25)
        rect = Rectangle(
            x=10, y=20, width=100, height=50, layer_id="layer1", transform=transform
        )
        bounds = rect.get_bounds()

        assert bounds.min_point == Point(25, 45)
        assert bounds.max_point == Point(125, 95)

    def test_bounds_with_rotation(self):
        """Test bounds calculation with rotation transform."""
        # 90-degree rotation around origin
        transform = Transform.rotation(90)
        rect = Rectangle(
            x=0, y=0, width=100, height=50, layer_id="layer1", transform=transform
        )
        bounds = rect.get_bounds()

        # After 90-degree rotation, the rectangle's bounds change
        assert bounds.min_point.x == pytest.approx(-50, abs=1e-10)
        assert bounds.min_point.y == pytest.approx(0, abs=1e-10)
        assert bounds.max_point.x == pytest.approx(0, abs=1e-10)
        assert bounds.max_point.y == pytest.approx(100, abs=1e-10)

    def test_bounds_with_scale(self):
        """Test bounds calculation with scale transform."""
        transform = Transform.scale(2.0, 3.0)
        rect = Rectangle(
            x=10, y=20, width=100, height=50, layer_id="layer1", transform=transform
        )
        bounds = rect.get_bounds()

        assert bounds.min_point == Point(20, 60)
        assert bounds.max_point == Point(220, 210)

    def test_bounds_with_complex_transform(self):
        """Test bounds with combined transformations."""
        # Scale then translate
        # When composing A.compose(B), B is applied first, then A
        t1 = Transform.scale(2.0)
        t2 = Transform.translation(50, 50)
        transform = t1.compose(t2)

        rect = Rectangle(
            x=10, y=20, width=100, height=50, layer_id="layer1", transform=transform
        )
        bounds = rect.get_bounds()

        # First translate by (50, 50), then scale by 2
        # So (10, 20) -> (60, 70) -> (120, 140)
        # And (110, 70) -> (160, 120) -> (320, 240)
        assert bounds.min_point == Point(120, 140)
        assert bounds.max_point == Point(320, 240)


class TestRectangleTransform:
    """Test rectangle transformation."""

    def test_apply_transform_creates_new_instance(self):
        """Test that apply_transform creates a new instance."""
        rect1 = Rectangle(x=10, y=20, width=100, height=50, layer_id="layer1")
        transform = Transform.translation(5, 10)

        rect2 = rect1.apply_transform(transform)

        assert rect1 is not rect2
        assert rect1.id == rect2.id  # ID is preserved
        assert rect1.transform != rect2.transform

    def test_apply_transform_preserves_properties(self):
        """Test that apply_transform preserves all properties except transform."""
        style = Style(fill_color="#FF0000")
        metadata = {"name": "test"}
        rect1 = Rectangle(
            x=10,
            y=20,
            width=100,
            height=50,
            corner_radius=5,
            layer_id="layer1",
            group_id="group1",
            visible=False,
            locked=True,
            style=style,
            metadata=metadata,
        )

        transform = Transform.rotation(45)
        rect2 = rect1.apply_transform(transform)

        # Shape properties preserved
        assert rect2.x == rect1.x
        assert rect2.y == rect1.y
        assert rect2.width == rect1.width
        assert rect2.height == rect1.height
        assert rect2.corner_radius == rect1.corner_radius

        # Common properties preserved
        assert rect2.layer_id == rect1.layer_id
        assert rect2.group_id == rect1.group_id
        assert rect2.visible == rect1.visible
        assert rect2.locked == rect1.locked
        assert rect2.style == rect1.style
        assert rect2.metadata == rect1.metadata

    def test_transform_composition(self):
        """Test that transforms compose correctly."""
        rect = Rectangle(x=0, y=0, width=100, height=50, layer_id="layer1")

        t1 = Transform.scale(2.0)
        t2 = Transform.translation(10, 20)

        rect_transformed = rect.apply_transform(t1).apply_transform(t2)

        # Check the final bounds
        bounds = rect_transformed.get_bounds()
        # First scale by 2: (0,0,100,50) -> (0,0,200,100)
        # Then translate by (10,20) - but translation happens after scale,
        # so the translation is also scaled
        assert bounds.min_point == Point(20, 40)
        assert bounds.max_point == Point(220, 140)


class TestRectangleSerialization:
    """Test rectangle serialization and deserialization."""

    def test_to_dict_basic(self):
        """Test serialization of basic rectangle."""
        rect = Rectangle(x=10, y=20, width=100, height=50, layer_id="layer1")
        data = rect.to_dict()

        assert data["type"] == "RECTANGLE"
        assert data["x"] == 10
        assert data["y"] == 20
        assert data["width"] == 100
        assert data["height"] == 50
        assert data["corner_radius"] == 0
        assert data["layer_id"] == "layer1"
        assert data["visible"] is True
        assert data["locked"] is False
        assert "id" in data
        assert "style" in data
        assert "transform" in data

    def test_to_dict_complete(self):
        """Test serialization with all properties."""
        style = Style(fill_color="#FF0000", stroke_width=2.0)
        transform = Transform.rotation(45)
        metadata = {"name": "Test", "category": "UI"}

        rect = Rectangle(
            x=0,
            y=0,
            width=200,
            height=100,
            corner_radius=15,
            layer_id="layer2",
            group_id="group1",
            visible=False,
            locked=True,
            style=style,
            transform=transform,
            metadata=metadata,
        )

        data = rect.to_dict()

        assert data["corner_radius"] == 15
        assert data["group_id"] == "group1"
        assert data["visible"] is False
        assert data["locked"] is True
        assert data["style"]["fill_color"] == "#FF0000"
        assert data["style"]["stroke_width"] == 2.0
        assert data["metadata"] == metadata
        assert len(data["transform"]) == 3  # 3x3 matrix

    def test_from_dict_basic(self):
        """Test deserialization of basic rectangle."""
        data = {
            "type": "RECTANGLE",
            "id": str(uuid.uuid4()),
            "x": 10,
            "y": 20,
            "width": 100,
            "height": 50,
            "layer_id": "layer1",
        }

        rect = Rectangle.from_dict(data)

        assert rect.id == data["id"]
        assert rect.x == 10
        assert rect.y == 20
        assert rect.width == 100
        assert rect.height == 50
        assert rect.corner_radius == 0
        assert rect.layer_id == "layer1"

    def test_from_dict_complete(self):
        """Test deserialization with all properties."""
        shape_id = str(uuid.uuid4())
        data = {
            "type": "RECTANGLE",
            "id": shape_id,
            "x": 0,
            "y": 0,
            "width": 200,
            "height": 100,
            "corner_radius": 15,
            "layer_id": "layer2",
            "group_id": "group1",
            "visible": False,
            "locked": True,
            "style": {
                "fill_color": "#FF0000",
                "stroke_color": "#000000",
                "stroke_width": 2.0,
            },
            "transform": [[1, 0, 5], [0, 1, 10], [0, 0, 1]],
            "metadata": {"name": "Test"},
        }

        rect = Rectangle.from_dict(data)

        assert rect.id == shape_id
        assert rect.corner_radius == 15
        assert rect.group_id == "group1"
        assert rect.visible is False
        assert rect.locked is True
        assert rect.style.fill_color == "#FF0000"
        assert rect.metadata["name"] == "Test"

        # Check transform was applied
        bounds = rect.get_bounds()
        assert bounds.min_point == Point(5, 10)

    def test_from_dict_missing_required_field(self):
        """Test deserialization with missing required fields."""
        data = {
            "type": "RECTANGLE",
            "x": 10,
            "y": 20,
            "width": 100,
            # Missing height
            "layer_id": "layer1",
        }

        with pytest.raises(ShapeValidationError) as excinfo:
            Rectangle.from_dict(data)

        assert "Invalid rectangle data" in str(excinfo.value)

    def test_from_dict_missing_layer_id(self):
        """Test deserialization with missing layer_id."""
        data = {
            "type": "RECTANGLE",
            "x": 10,
            "y": 20,
            "width": 100,
            "height": 50,
            # Missing layer_id
        }

        with pytest.raises(ShapeValidationError) as excinfo:
            Rectangle.from_dict(data)

        assert "layer_id cannot be empty" in str(excinfo.value)

    def test_from_dict_invalid_values(self):
        """Test deserialization with invalid values."""
        data = {
            "type": "RECTANGLE",
            "x": "not a number",  # Invalid type
            "y": 20,
            "width": 100,
            "height": 50,
            "layer_id": "layer1",
        }

        with pytest.raises(ShapeValidationError) as excinfo:
            Rectangle.from_dict(data)

        assert "Invalid rectangle data" in str(excinfo.value)

    def test_roundtrip_serialization(self):
        """Test that serialization roundtrip preserves all data."""
        style = Style(fill_color="#FF0000", stroke_width=3.0)
        transform = Transform.scale(1.5).compose(Transform.rotation(30))
        metadata = {"name": "Test", "tags": ["ui", "button"]}

        rect1 = Rectangle(
            x=15.5,
            y=25.5,
            width=150.5,
            height=75.5,
            corner_radius=12.5,
            layer_id="layer1",
            group_id="group1",
            visible=False,
            locked=True,
            style=style,
            transform=transform,
            metadata=metadata,
        )

        # Serialize and deserialize
        data = rect1.to_dict()
        rect2 = Rectangle.from_dict(data)

        # Compare all properties
        assert rect1.id == rect2.id
        assert rect1.x == rect2.x
        assert rect1.y == rect2.y
        assert rect1.width == rect2.width
        assert rect1.height == rect2.height
        assert rect1.corner_radius == rect2.corner_radius
        assert rect1.layer_id == rect2.layer_id
        assert rect1.group_id == rect2.group_id
        assert rect1.visible == rect2.visible
        assert rect1.locked == rect2.locked
        assert rect1.style.model_dump() == rect2.style.model_dump()
        assert rect1.metadata == rect2.metadata
        assert np.allclose(rect1.transform.matrix, rect2.transform.matrix)


class TestShapeFactory:
    """Test ShapeFactory with rectangles."""

    def test_create_rectangle_via_factory(self):
        """Test creating rectangle through factory."""
        rect = ShapeFactory.create_shape(
            ShapeType.RECTANGLE, "layer1", x=10, y=20, width=100, height=50
        )

        assert isinstance(rect, Rectangle)
        assert rect.x == 10
        assert rect.y == 20
        assert rect.width == 100
        assert rect.height == 50

    def test_create_rectangle_convenience_method(self):
        """Test factory convenience method."""
        rect = ShapeFactory.create_rectangle(
            x=10, y=20, width=100, height=50, layer_id="layer1", corner_radius=5
        )

        assert isinstance(rect, Rectangle)
        assert rect.corner_radius == 5

    def test_factory_from_dict(self):
        """Test creating shapes from dict via factory."""
        data = {
            "type": "RECTANGLE",
            "x": 10,
            "y": 20,
            "width": 100,
            "height": 50,
            "layer_id": "layer1",
        }

        shape = ShapeFactory.from_dict(data)

        assert isinstance(shape, Rectangle)
        assert shape.x == 10

    def test_factory_unsupported_type(self):
        """Test factory with unsupported shape type."""
        with pytest.raises(ShapeValidationError) as excinfo:
            ShapeFactory.create_shape(
                ShapeType.CIRCLE,  # Not implemented yet
                "layer1",
            )

        assert "Unsupported shape type" in str(excinfo.value)

    def test_factory_invalid_parameters(self):
        """Test factory with invalid parameters."""
        with pytest.raises(ShapeValidationError) as excinfo:
            ShapeFactory.create_shape(
                ShapeType.RECTANGLE,
                "layer1",
                # Missing required x, y, width, height
            )

        assert "Invalid parameters" in str(excinfo.value)

    def test_factory_supported_types(self):
        """Test getting supported shape types."""
        supported = ShapeFactory.get_supported_types()

        assert ShapeType.RECTANGLE in supported
        assert len(supported) >= 1


class TestRectangleRepresentation:
    """Test string representation of rectangles."""

    def test_repr(self):
        """Test __repr__ method."""
        rect = Rectangle(
            x=10.5,
            y=20.5,
            width=100.5,
            height=50.5,
            corner_radius=5.5,
            layer_id="layer1",
        )

        repr_str = repr(rect)
        assert "Rectangle" in repr_str
        assert f"id={rect.id}" in repr_str
        assert "x=10.5" in repr_str
        assert "y=20.5" in repr_str
        assert "width=100.5" in repr_str
        assert "height=50.5" in repr_str
        assert "corner_radius=5.5" in repr_str
