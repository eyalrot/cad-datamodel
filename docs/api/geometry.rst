Geometry Module
===============

.. module:: cad_datamodel.geometry

The geometry module provides geometric calculations and spatial operations.

.. note::
   This module is planned for implementation in Epic 5. This documentation
   serves as a placeholder for the upcoming geometry features.

Planned Features
----------------

SpatialIndex
~~~~~~~~~~~~

Fast spatial queries for shapes.

**Planned Methods:**

- ``insert()``: Add shape to index
- ``query()``: Find shapes in region
- ``nearest()``: Find nearest shapes
- ``remove()``: Remove shape from index

GeometryCalculator
~~~~~~~~~~~~~~~~~~

Geometric operations on shapes.

**Planned Methods:**

- ``intersection()``: Find shape intersections
- ``union()``: Combine shapes
- ``difference()``: Subtract shapes
- ``buffer()``: Expand/contract shapes
- ``simplify()``: Reduce complexity

HitTester
~~~~~~~~~

Point-in-shape and selection testing.

**Planned Methods:**

- ``hit_test()``: Test if point hits shape
- ``select_in_rect()``: Select shapes in rectangle
- ``select_in_polygon()``: Select shapes in polygon