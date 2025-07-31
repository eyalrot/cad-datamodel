Getting Started
===============

This guide will help you get started with the CAD Datamodel library.

Installation
------------

From PyPI (Coming Soon)
~~~~~~~~~~~~~~~~~~~~~~~

The easiest way to install CAD Datamodel is via pip::

    pip install cad-datamodel

From Source
~~~~~~~~~~~

To install from source or for development::

    git clone https://github.com/eyalrot/cad-datamodel.git
    cd cad-datamodel
    pip install -e .

For development with all tools::

    pip install -e ".[dev]"

Basic Concepts
--------------

The CAD Datamodel library is built around several core concepts:

**Shapes**
    Basic geometric entities like rectangles, circles, lines, etc.

**Layers**
    Organizational containers for shapes with z-ordering

**Styles**
    Visual properties like colors, stroke width, and opacity

**Transforms**
    Geometric transformations (translation, rotation, scaling)

**Documents**
    Top-level container holding layers and shapes

Core Types
----------

The library provides several fundamental types:

.. code-block:: python

   from cad_datamodel.core import Point, Bounds, Color, Transform

   # Points represent 2D coordinates
   p1 = Point(10, 20)
   p2 = Point(100, 200)

   # Bounds define rectangular regions
   bounds = Bounds(p1, p2)
   print(f"Width: {bounds.width}, Height: {bounds.height}")
   print(f"Center: {bounds.center}")

   # Colors support multiple formats
   red = Color.from_hex("#FF0000")
   semi_transparent_blue = Color(red=0, green=0, blue=255, alpha=128)

   # Transforms can be composed
   t1 = Transform.translation(50, 50)
   t2 = Transform.rotation(45)
   combined = t1.compose(t2)

Working with Transforms
-----------------------

Transforms are a powerful feature for manipulating geometry:

.. code-block:: python

   from cad_datamodel.core import Point, Transform

   # Create a point
   point = Point(10, 10)

   # Translate
   translated = Transform.translation(20, 30).apply_to_point(point)
   # Result: Point(30, 40)

   # Rotate around origin
   rotated = Transform.rotation(90).apply_to_point(point)
   # Result: Point(-10, 10)

   # Rotate around a center
   center = Point(50, 50)
   rotated_around = Transform.rotation(90, center=center).apply_to_point(point)

   # Scale from origin
   scaled = Transform.scale(2).apply_to_point(point)
   # Result: Point(20, 20)

   # Combine transforms
   transform = (Transform.translation(50, 0)
                .compose(Transform.rotation(45))
                .compose(Transform.scale(2)))
   
   result = transform.apply_to_point(Point(0, 0))

Error Handling
--------------

The library provides a comprehensive exception hierarchy:

.. code-block:: python

   from cad_datamodel.core import (
       CADError,
       ShapeValidationError,
       LayerError,
       TransformError
   )

   try:
       # Your CAD operations
       pass
   except ShapeValidationError as e:
       print(f"Shape validation failed: {e.message}")
       print(f"Details: {e.details}")
   except CADError as e:
       # Catch all CAD-related errors
       print(f"CAD error: {e}")

Next Steps
----------

- Read the :doc:`user_guide` for detailed usage examples
- Explore the :doc:`api/index` for complete API documentation
- Check out the example scripts in the ``examples/`` directory