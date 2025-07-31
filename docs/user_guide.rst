User Guide
==========

This guide provides detailed information on using the CAD Datamodel library.

.. note::
   Shape implementations are coming in the next development stories. This guide
   shows the planned API and currently available core functionality.

Core Module
-----------

The core module provides the foundation for all CAD operations.

Type System
~~~~~~~~~~~

The library uses a comprehensive type system for safety and clarity:

.. code-block:: python

   from cad_datamodel.core import (
       Coordinate,  # Type alias for float
       Angle,       # Type alias for float (degrees)
       Opacity,     # Type alias for float (0.0-1.0)
       ShapeType,   # Enum of shape types
       LineCap,     # Enum for line end styles
       LineJoin,    # Enum for line join styles
   )

   # ShapeType enumeration
   print(list(ShapeType))  # All available shape types

   # Style enumerations
   cap = LineCap.ROUND
   join = LineJoin.MITER

Points and Bounds
~~~~~~~~~~~~~~~~~

Working with 2D coordinates and bounding boxes:

.. code-block:: python

   from cad_datamodel.core import Point, Bounds

   # Points are immutable
   p1 = Point(10, 20)
   p2 = Point(100, 200)
   
   # Bounds represent axis-aligned rectangles
   bounds = Bounds(p1, p2)
   
   # Bounds properties
   print(f"Width: {bounds.width}")
   print(f"Height: {bounds.height}")
   print(f"Center: {bounds.center}")
   
   # Test point containment
   test_point = Point(50, 50)
   if bounds.contains_point(test_point):
       print("Point is inside bounds")
   
   # Test bounds intersection
   other_bounds = Bounds(Point(50, 50), Point(150, 150))
   if bounds.intersects(other_bounds):
       print("Bounds overlap")

Color Management
~~~~~~~~~~~~~~~~

The Color class provides flexible color handling:

.. code-block:: python

   from cad_datamodel.core import Color, NAMED_COLORS

   # Create colors various ways
   red = Color(red=255, green=0, blue=0)  # RGB
   semi_blue = Color(red=0, green=0, blue=255, alpha=128)  # RGBA
   
   # From hex string
   green = Color.from_hex("#00FF00")
   with_alpha = Color.from_hex("#00FF0080")  # With alpha
   
   # Using named colors
   black = NAMED_COLORS["black"]
   white = NAMED_COLORS["white"]
   
   # Color operations
   color = Color.from_hex("#FF8040")
   hex_str = color.to_hex()  # "#ff8040"
   hex_with_alpha = color.to_hex(include_alpha=True)  # "#ff8040ff"
   rgba = color.to_rgba_tuple()  # (255, 128, 64, 255)
   
   # Create variant with different alpha
   transparent = color.with_alpha(64)

Transformations
~~~~~~~~~~~~~~~

The Transform class handles 2D affine transformations:

.. code-block:: python

   from cad_datamodel.core import Transform, Point
   import math

   # Basic transforms
   t1 = Transform.identity()
   t2 = Transform.translation(100, 50)
   t3 = Transform.rotation(45)  # Degrees
   t4 = Transform.scale(2)  # Uniform scale
   t5 = Transform.scale(2, 3)  # Non-uniform scale

   # Transforms with custom centers
   center = Point(50, 50)
   t6 = Transform.rotation(90, center=center)
   t7 = Transform.scale(2, center=center)

   # Compose transforms (order matters!)
   # First translate, then rotate
   combined = Transform.translation(100, 0).compose(
       Transform.rotation(45)
   )

   # Apply to points
   p = Point(10, 10)
   p_transformed = combined.apply_to_point(p)

   # Inverse transforms
   inverse = t2.inverse()
   p_back = inverse.apply_to_point(
       t2.apply_to_point(p)
   )
   # p_back == p (approximately)

   # Access transformation matrix
   matrix = t2.matrix  # 3x3 numpy array

Exception Handling
~~~~~~~~~~~~~~~~~~

Comprehensive error handling with detailed context:

.. code-block:: python

   from cad_datamodel.core import (
       CADError,
       ShapeValidationError,
       LayerError,
       TransformError,
       SerializationError,
       GroupError,
       DocumentError,
       ReferenceError,
       GeometryError,
   )

   # All exceptions derive from CADError
   try:
       # CAD operations
       pass
   except ShapeValidationError as e:
       print(f"Shape type: {e.details['shape_type']}")
       print(f"Validation error: {e.details['validation_error']}")
       print(f"Shape ID: {e.details.get('shape_id', 'N/A')}")
   except LayerError as e:
       print(f"Layer operation failed: {e.details['operation']}")
       print(f"Reason: {e.details.get('reason', 'Unknown')}")
   except TransformError as e:
       print(f"Transform type: {e.details['transform_type']}")
       print(f"Error: {e.details['error']}")
   except CADError as e:
       # Catch-all for CAD errors
       print(f"General CAD error: {e.message}")
       print(f"Details: {e.details}")

Constants and Defaults
~~~~~~~~~~~~~~~~~~~~~~

The library provides sensible defaults:

.. code-block:: python

   from cad_datamodel.core import (
       DEFAULT_STROKE_WIDTH,
       DEFAULT_STROKE_COLOR,
       DEFAULT_FILL_COLOR,
       MIN_COORDINATE,
       MAX_COORDINATE,
       COORDINATE_PRECISION,
   )

   print(f"Default stroke width: {DEFAULT_STROKE_WIDTH}")
   print(f"Coordinate range: [{MIN_COORDINATE}, {MAX_COORDINATE}]")
   print(f"Coordinate precision: {COORDINATE_PRECISION} decimal places")

Best Practices
--------------

Type Annotations
~~~~~~~~~~~~~~~~

Always use type annotations for better IDE support and type safety:

.. code-block:: python

   from cad_datamodel.core import Point, Color, Transform, Bounds
   from typing import List, Optional

   def create_grid_points(
       rows: int, 
       cols: int, 
       spacing: float = 10.0
   ) -> List[Point]:
       """Create a grid of points."""
       points: List[Point] = []
       for row in range(rows):
           for col in range(cols):
               points.append(Point(col * spacing, row * spacing))
       return points

   def apply_transform_to_bounds(
       bounds: Bounds, 
       transform: Transform
   ) -> Bounds:
       """Apply transform to bounds corners."""
       corners = [
           bounds.min_point,
           Point(bounds.max_point.x, bounds.min_point.y),
           bounds.max_point,
           Point(bounds.min_point.x, bounds.max_point.y),
       ]
       transformed = [transform.apply_to_point(p) for p in corners]
       
       xs = [p.x for p in transformed]
       ys = [p.y for p in transformed]
       
       return Bounds(
           Point(min(xs), min(ys)),
           Point(max(xs), max(ys))
       )

Performance Tips
~~~~~~~~~~~~~~~~

1. **Reuse transforms**: Create transforms once and reuse them
2. **Compose efficiently**: Combine multiple transforms before applying
3. **Use bounds checking**: Test bounds intersection before detailed checks
4. **Batch operations**: Process multiple shapes together when possible

Coming Soon
-----------

The following features are planned for upcoming releases:

- Shape implementations (Rectangle, Circle, Line, etc.)
- Layer management system
- Style inheritance and management
- SVG import/export
- Document persistence
- Spatial indexing for performance
- Group operations