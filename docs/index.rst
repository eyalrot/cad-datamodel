.. CAD Datamodel documentation master file

CAD Drawing Application Data Model
==================================

Welcome to the CAD Datamodel documentation! This library provides a comprehensive 
Python data model for CAD drawing applications with support for geometric shapes, 
layers, groups, styling, and SVG rendering/persistence.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting_started
   user_guide
   api/index
   development
   changelog

Overview
--------

The CAD Datamodel package is designed to provide a robust foundation for CAD 
applications with:

* **Type-safe interfaces** - Full type annotations and mypy strict mode support
* **Extensible architecture** - Clean interfaces for custom shapes and renderers
* **Performance focused** - Optimized for handling 100,000+ shapes
* **Industry standards** - SVG import/export with full fidelity

Key Features
------------

**Shape System**
   Support for Rectangle, Circle, Line, Polygon, Polyline, and Group shapes

**Layer Management**
   Organize shapes in layers with z-ordering and visibility control

**Style System**
   Comprehensive styling with fill, stroke, and style inheritance

**Transform Support**
   Translation, rotation, and scaling with matrix composition

**Persistence**
   Clean SVG import/export and JSON serialization

Quick Example
-------------

.. code-block:: python

   from cad_datamodel.core import Point, Color, Transform

   # Create colors
   red = Color.from_hex("#FF0000")
   blue = Color(red=0, green=0, blue=255, alpha=128)

   # Create and compose transforms
   transform = Transform.translation(50, 50).compose(
       Transform.rotation(45, center=Point(50, 50))
   )

   # Apply transform to a point
   original = Point(10, 10)
   transformed = transform.apply_to_point(original)

Installation
------------

Install from PyPI (coming soon)::

   pip install cad-datamodel

Or install from source::

   git clone https://github.com/eyalrot/cad-datamodel.git
   cd cad-datamodel
   pip install -e .

Getting Help
------------

* **Documentation**: You're reading it!
* **GitHub Issues**: https://github.com/eyalrot/cad-datamodel/issues
* **Discussions**: https://github.com/eyalrot/cad-datamodel/discussions

License
-------

This project is licensed under the MIT License. See the LICENSE file for details.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`