Core Module
===========

.. module:: cad_datamodel.core

The core module provides fundamental classes, interfaces, and types for the CAD system.

Base Interfaces
---------------

.. autoclass:: IShape
   :members:
   :show-inheritance:
   :special-members: __init__

.. autoclass:: IRenderer
   :members:
   :show-inheritance:

.. autoclass:: ISerializer
   :members:
   :show-inheritance:

Types
-----

Basic Types
~~~~~~~~~~~

.. autoclass:: Point
   :members:
   :show-inheritance:

.. autoclass:: Bounds
   :members:
   :show-inheritance:

.. autoclass:: Color
   :members:
   :show-inheritance:
   :special-members: __init__

.. autoclass:: Transform
   :members:
   :show-inheritance:
   :special-members: __init__

Enumerations
~~~~~~~~~~~~

.. autoclass:: ShapeType
   :members:
   :show-inheritance:

.. autoclass:: LineCap
   :members:
   :show-inheritance:

.. autoclass:: LineJoin
   :members:
   :show-inheritance:

.. autoclass:: Units
   :members:
   :show-inheritance:

Type Aliases
~~~~~~~~~~~~

.. autodata:: Coordinate
   :annotation: = float

.. autodata:: Angle
   :annotation: = float

.. autodata:: Opacity
   :annotation: = float

Exceptions
----------

.. autoexception:: CADError
   :members:
   :show-inheritance:

.. autoexception:: ShapeValidationError
   :members:
   :show-inheritance:

.. autoexception:: LayerError
   :members:
   :show-inheritance:

.. autoexception:: TransformError
   :members:
   :show-inheritance:

.. autoexception:: SerializationError
   :members:
   :show-inheritance:

.. autoexception:: GroupError
   :members:
   :show-inheritance:

.. autoexception:: DocumentError
   :members:
   :show-inheritance:

.. autoexception:: ReferenceError
   :members:
   :show-inheritance:

.. autoexception:: GeometryError
   :members:
   :show-inheritance:

Constants
---------

Style Defaults
~~~~~~~~~~~~~~

.. autodata:: DEFAULT_STROKE_WIDTH
.. autodata:: DEFAULT_STROKE_COLOR
.. autodata:: DEFAULT_FILL_COLOR
.. autodata:: DEFAULT_STROKE_OPACITY
.. autodata:: DEFAULT_FILL_OPACITY
.. autodata:: DEFAULT_LINE_CAP
.. autodata:: DEFAULT_LINE_JOIN

Coordinate Limits
~~~~~~~~~~~~~~~~~

.. autodata:: MIN_COORDINATE
.. autodata:: MAX_COORDINATE
.. autodata:: COORDINATE_PRECISION

Canvas Defaults
~~~~~~~~~~~~~~~

.. autodata:: DEFAULT_CANVAS_WIDTH
.. autodata:: DEFAULT_CANVAS_HEIGHT

Other Constants
~~~~~~~~~~~~~~~

.. autodata:: IDENTITY_TRANSFORM
.. autodata:: NAMED_COLORS