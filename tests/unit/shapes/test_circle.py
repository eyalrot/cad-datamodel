"""Unit tests for the Circle shape implementation."""

import pytest

from cad_datamodel.core.exceptions import ShapeValidationError
from cad_datamodel.core.types import ShapeType, Transform
from cad_datamodel.shapes.circle import Circle
from cad_datamodel.shapes.shape import Style


class TestCircle:
    """Test suite for Circle shape."""

    def test_circle_creation_valid(self):
        """Test creating a circle with valid parameters."""
        circle = Circle(
            cx=50.0,
            cy=50.0,
            radius=25.0,
            layer_id="layer1",
        )

        assert circle.cx == 50.0
        assert circle.cy == 50.0
        assert circle.radius == 25.0
        assert circle.layer_id == "layer1"
        assert circle.type == ShapeType.CIRCLE
        assert circle.visible is True
        assert circle.locked is False
        assert circle.id is not None

    def test_circle_creation_with_all_parameters(self):
        """Test creating a circle with all optional parameters."""
        style = Style(fill_color="#FF0000", stroke_color="#000000", stroke_width=2.0)
        transform = Transform.translation(10, 20)
        metadata = {"custom": "data"}

        circle = Circle(
            cx=100.0,
            cy=100.0,
            radius=50.0,
            layer_id="layer1",
            group_id="group1",
            visible=False,
            locked=True,
            style=style,
            transform=transform,
            metadata=metadata,
            shape_id="custom-id",
        )

        assert circle.cx == 100.0
        assert circle.cy == 100.0
        assert circle.radius == 50.0
        assert circle.layer_id == "layer1"
        assert circle.group_id == "group1"
        assert circle.visible is False
        assert circle.locked is True
        assert circle.style == style
        assert circle.transform == transform
        assert circle.metadata == metadata
        assert circle.id == "custom-id"

    def test_circle_invalid_radius_zero(self):
        """Test that zero radius raises validation error."""
        with pytest.raises(ShapeValidationError) as exc_info:
            Circle(cx=0, cy=0, radius=0, layer_id="layer1")

        assert "Radius must be positive" in str(exc_info.value)

    def test_circle_invalid_radius_negative(self):
        """Test that negative radius raises validation error."""
        with pytest.raises(ShapeValidationError) as exc_info:
            Circle(cx=0, cy=0, radius=-10, layer_id="layer1")

        assert "Radius must be positive" in str(exc_info.value)

    def test_circle_immutability(self):
        """Test that circle attributes are immutable."""
        circle = Circle(cx=50, cy=50, radius=25, layer_id="layer1")

        # Test that attributes cannot be modified
        with pytest.raises(AttributeError):
            circle.cx = 100

        with pytest.raises(AttributeError):
            circle.cy = 100

        with pytest.raises(AttributeError):
            circle.radius = 50

    def test_circle_bounds_no_transform(self):
        """Test bounds calculation without transformation."""
        circle = Circle(cx=50, cy=50, radius=25, layer_id="layer1")
        bounds = circle.get_bounds()

        assert bounds.min_point.x == pytest.approx(25.0)
        assert bounds.min_point.y == pytest.approx(25.0)
        assert bounds.max_point.x == pytest.approx(75.0)
        assert bounds.max_point.y == pytest.approx(75.0)

    def test_circle_bounds_with_translation(self):
        """Test bounds calculation with translation transform."""
        transform = Transform.translation(10, 20)
        circle = Circle(
            cx=50, cy=50, radius=25, layer_id="layer1", transform=transform
        )
        bounds = circle.get_bounds()

        assert bounds.min_point.x == pytest.approx(35.0)  # 25 + 10
        assert bounds.min_point.y == pytest.approx(45.0)  # 25 + 20
        assert bounds.max_point.x == pytest.approx(85.0)  # 75 + 10
        assert bounds.max_point.y == pytest.approx(95.0)  # 75 + 20

    def test_circle_bounds_with_scale(self):
        """Test bounds calculation with scale transform."""
        transform = Transform.scale(2.0)
        circle = Circle(
            cx=50, cy=50, radius=25, layer_id="layer1", transform=transform
        )
        bounds = circle.get_bounds()

        # Scaled circle: center at (100, 100), radius effectively 50
        assert bounds.min_point.x == pytest.approx(50.0)
        assert bounds.min_point.y == pytest.approx(50.0)
        assert bounds.max_point.x == pytest.approx(150.0)
        assert bounds.max_point.y == pytest.approx(150.0)

    def test_circle_apply_transform(self):
        """Test applying a transform to a circle."""
        original = Circle(cx=50, cy=50, radius=25, layer_id="layer1")
        transform = Transform.translation(20, 30)

        transformed = original.apply_transform(transform)

        # Original should be unchanged
        assert original.cx == 50
        assert original.cy == 50
        assert original.radius == 25
        assert original.transform == Transform.identity()

        # Transformed should have new transform but same geometry
        assert transformed.cx == 50
        assert transformed.cy == 50
        assert transformed.radius == 25
        assert transformed.transform == transform
        assert transformed.id == original.id  # ID preserved

    def test_circle_serialization(self):
        """Test to_dict and from_dict methods."""
        style = Style(fill_color="#FF0000", stroke_color="#000000")
        transform = Transform.rotation(45)

        original = Circle(
            cx=100,
            cy=200,
            radius=50,
            layer_id="layer1",
            group_id="group1",
            visible=False,
            locked=True,
            style=style,
            transform=transform,
            metadata={"key": "value"},
            shape_id="test-id",
        )

        # Serialize to dict
        data = original.to_dict()

        # Check all fields are present
        assert data["cx"] == 100
        assert data["cy"] == 200
        assert data["radius"] == 50
        assert data["type"] == "CIRCLE"
        assert data["layer_id"] == "layer1"
        assert data["group_id"] == "group1"
        assert data["visible"] is False
        assert data["locked"] is True
        assert data["id"] == "test-id"
        assert data["metadata"] == {"key": "value"}
        assert "style" in data
        assert "transform" in data

        # Deserialize from dict
        restored = Circle.from_dict(data)

        assert restored.cx == original.cx
        assert restored.cy == original.cy
        assert restored.radius == original.radius
        assert restored.layer_id == original.layer_id
        assert restored.group_id == original.group_id
        assert restored.visible == original.visible
        assert restored.locked == original.locked
        assert restored.id == original.id
        assert restored.metadata == original.metadata

    def test_circle_from_dict_invalid_data(self):
        """Test from_dict with invalid data."""
        # Missing required field
        with pytest.raises(ShapeValidationError) as exc_info:
            Circle.from_dict({"cx": 0, "cy": 0})  # missing radius
        assert "Invalid circle data" in str(exc_info.value)

        # Invalid type
        with pytest.raises(ShapeValidationError) as exc_info:
            Circle.from_dict({"cx": "not a number", "cy": 0, "radius": 10})
        assert "Invalid circle data" in str(exc_info.value)

    def test_circle_repr(self):
        """Test string representation of circle."""
        circle = Circle(
            cx=50, cy=50, radius=25, layer_id="layer1", shape_id="test-id"
        )
        repr_str = repr(circle)

        assert "Circle" in repr_str
        assert "id=test-id" in repr_str
        assert "cx=50" in repr_str
        assert "cy=50" in repr_str
        assert "radius=25" in repr_str

    @pytest.mark.parametrize(
        "cx,cy,radius",
        [
            (0, 0, 1),  # Unit circle at origin
            (-50, -50, 10),  # Negative coordinates
            (1000, 1000, 500),  # Large values
            (0.5, 0.5, 0.1),  # Small decimal values
        ],
    )
    def test_circle_various_valid_parameters(self, cx, cy, radius):
        """Test circle creation with various valid parameter combinations."""
        circle = Circle(cx=cx, cy=cy, radius=radius, layer_id="layer1")

        assert circle.cx == cx
        assert circle.cy == cy
        assert circle.radius == radius

        # Verify bounds are calculated correctly
        bounds = circle.get_bounds()
        assert bounds.min_point.x == pytest.approx(cx - radius)
        assert bounds.min_point.y == pytest.approx(cy - radius)
        assert bounds.max_point.x == pytest.approx(cx + radius)
        assert bounds.max_point.y == pytest.approx(cy + radius)
