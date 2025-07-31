"""Constants and default values for the CAD datamodel.

This module contains all constant values, default settings, and
system-wide limits used throughout the CAD system.
"""


from .types import Color, LineCap, LineJoin, Transform

# Default style values
DEFAULT_STROKE_WIDTH: float = 1.0
DEFAULT_STROKE_COLOR: Color = Color(red=0, green=0, blue=0, alpha=255)  # Black
DEFAULT_FILL_COLOR: Color = Color(red=255, green=255, blue=255, alpha=255)  # White
DEFAULT_STROKE_OPACITY: float = 1.0
DEFAULT_FILL_OPACITY: float = 1.0
DEFAULT_LINE_CAP: LineCap = LineCap.BUTT
DEFAULT_LINE_JOIN: LineJoin = LineJoin.MITER
DEFAULT_MITER_LIMIT: float = 4.0

# Coordinate system limits
MIN_COORDINATE: float = -1e6
MAX_COORDINATE: float = 1e6
COORDINATE_PRECISION: int = 6  # Decimal places for coordinate storage

# Canvas limits
MIN_CANVAS_SIZE: float = 1.0
MAX_CANVAS_SIZE: float = 100000.0
DEFAULT_CANVAS_WIDTH: float = 800.0
DEFAULT_CANVAS_HEIGHT: float = 600.0

# Shape constraints
MIN_SHAPE_SIZE: float = 0.001  # Minimum dimension for any shape
MAX_VERTICES_POLYGON: int = 10000  # Maximum vertices in a polygon/polyline
MIN_CIRCLE_RADIUS: float = 0.001
MAX_CIRCLE_RADIUS: float = 50000.0

# Layer constraints
MAX_LAYERS: int = 1000
DEFAULT_LAYER_OPACITY: float = 1.0
MIN_LAYER_OPACITY: float = 0.0
MAX_LAYER_OPACITY: float = 1.0

# Group constraints
MAX_GROUP_NESTING_DEPTH: int = 100  # Maximum depth of nested groups
MAX_SHAPES_PER_GROUP: int = 10000

# Color constants
NAMED_COLORS: dict[str, Color] = {
    "black": Color(red=0, green=0, blue=0),
    "white": Color(red=255, green=255, blue=255),
    "red": Color(red=255, green=0, blue=0),
    "green": Color(red=0, green=255, blue=0),
    "blue": Color(red=0, green=0, blue=255),
    "yellow": Color(red=255, green=255, blue=0),
    "cyan": Color(red=0, green=255, blue=255),
    "magenta": Color(red=255, green=0, blue=255),
    "gray": Color(red=128, green=128, blue=128),
    "lightgray": Color(red=211, green=211, blue=211),
    "darkgray": Color(red=169, green=169, blue=169),
    "orange": Color(red=255, green=165, blue=0),
    "purple": Color(red=128, green=0, blue=128),
    "brown": Color(red=165, green=42, blue=42),
    "pink": Color(red=255, green=192, blue=203),
    "transparent": Color(red=0, green=0, blue=0, alpha=0),
}

# Transform constants
IDENTITY_TRANSFORM: Transform = Transform.identity()
TRANSFORM_EPSILON: float = 1e-10  # Epsilon for transform comparisons

# SVG-related constants
SVG_NAMESPACE: str = "http://www.w3.org/2000/svg"
SVG_VERSION: str = "1.1"
SVG_DECIMAL_PLACES: int = 3  # Precision for SVG output

# Supported file formats
SUPPORTED_IMPORT_FORMATS: set[str] = {"svg", "json"}
SUPPORTED_EXPORT_FORMATS: set[str] = {"svg", "json", "png", "pdf"}

# Performance limits
MAX_SHAPES_PER_DOCUMENT: int = 1000000  # 1 million shapes
MAX_UNDO_HISTORY: int = 100
SPATIAL_INDEX_THRESHOLD: int = 1000  # Use spatial index above this shape count

# Validation constants
UUID_REGEX: str = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
COLOR_HEX_REGEX: str = r'^#?([0-9a-fA-F]{6}|[0-9a-fA-F]{8})$'

# Default metadata keys
METADATA_CREATED_AT: str = "created_at"
METADATA_MODIFIED_AT: str = "modified_at"
METADATA_AUTHOR: str = "author"
METADATA_DESCRIPTION: str = "description"
METADATA_TAGS: str = "tags"

# Error messages
ERROR_INVALID_COORDINATES: str = "Coordinates must be finite numbers within valid range"
ERROR_INVALID_DIMENSIONS: str = "Shape dimensions must be positive"
ERROR_LAYER_NOT_FOUND: str = "Layer with ID '{layer_id}' not found"
ERROR_SHAPE_NOT_FOUND: str = "Shape with ID '{shape_id}' not found"
ERROR_CIRCULAR_REFERENCE: str = "Circular reference detected in group hierarchy"
ERROR_MAX_NESTING_EXCEEDED: str = "Maximum group nesting depth exceeded"
