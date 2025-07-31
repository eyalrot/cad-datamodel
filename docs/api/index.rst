API Reference
=============

This is the complete API reference for the CAD Datamodel library.

.. toctree::
   :maxdepth: 2
   :caption: API Modules:

   core
   shapes
   layers
   styles
   transform
   geometry
   persistence

Overview
--------

The CAD Datamodel API is organized into several modules:

**Core Module** (:doc:`core`)
   Base classes, interfaces, types, and exceptions

**Shapes Module** (:doc:`shapes`)
   Shape implementations (Rectangle, Circle, Line, etc.)

**Layers Module** (:doc:`layers`)
   Layer management and organization

**Styles Module** (:doc:`styles`)
   Visual styling and appearance

**Transform Module** (:doc:`transform`)
   Geometric transformations

**Geometry Module** (:doc:`geometry`)
   Geometric calculations and spatial operations

**Persistence Module** (:doc:`persistence`)
   Save/load functionality and format converters

Module Import Structure
-----------------------

.. code-block:: python

   # Core functionality
   from cad_datamodel.core import (
       Point, Bounds, Color, Transform,
       IShape, IRenderer, ISerializer,
       ShapeType, LineCap, LineJoin,
       CADError, ShapeValidationError,
   )

   # Shape implementations (coming soon)
   from cad_datamodel.shapes import (
       Rectangle, Circle, Line,
       Polygon, Polyline, Group,
   )

   # Layer management (coming soon)
   from cad_datamodel.layers import (
       Layer, LayerManager,
   )

   # Style management (coming soon)
   from cad_datamodel.styles import (
       Style, StyleManager,
   )

Quick Reference
---------------

Common Types
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Type
     - Description
   * - ``Point``
     - 2D coordinate (x, y)
   * - ``Bounds``
     - Axis-aligned bounding box
   * - ``Color``
     - RGBA color representation
   * - ``Transform``
     - 2D affine transformation matrix
   * - ``Coordinate``
     - Type alias for float
   * - ``Angle``
     - Type alias for float (degrees)
   * - ``Opacity``
     - Type alias for float (0.0-1.0)

Common Exceptions
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Exception
     - Description
   * - ``CADError``
     - Base exception for all CAD errors
   * - ``ShapeValidationError``
     - Invalid shape parameters
   * - ``LayerError``
     - Layer operation failed
   * - ``TransformError``
     - Transform operation failed
   * - ``SerializationError``
     - Save/load operation failed