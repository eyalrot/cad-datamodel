# CAD Drawing Application Data Model

A comprehensive Python data model package for CAD drawing applications that supports geometric shapes, layers, groups, styling, and SVG rendering/persistence.

## Features

- **Shape System**: Rectangle, Circle, Line, Polygon, Polyline, and Group support
- **Layer Management**: Organize shapes in layers with z-ordering
- **Style System**: Comprehensive styling with fill, stroke, and inheritance
- **Transform Support**: Translation, rotation, and scaling with matrix operations
- **SVG Integration**: Clean import/export to SVG format
- **Type Safety**: Full type annotations for better IDE support
- **Performance**: Optimized for handling 100,000+ shapes

## Installation

```bash
pip install cad-datamodel
```

## Development Setup

```bash
# Clone the repository
git clone <repository-url>
cd cad-datamodel

# Install in development mode (in devcontainer or system Python)
pip3 install -e ".[dev]"

# Run tests
pytest

# Run type checking
mypy src/cad_datamodel

# Run linting
ruff check src tests
ruff format src tests
```

## Quick Start

```python
from cad_datamodel import Document, Layer, Rectangle, Circle

# Create a new document
doc = Document()

# Add a layer
layer = Layer(name="Main Layer")
doc.add_layer(layer)

# Create shapes
rect = Rectangle(x=10, y=10, width=100, height=50)
circle = Circle(cx=100, cy=100, radius=30)

# Add shapes to layer
layer.add_shape(rect)
layer.add_shape(circle)

# Export to SVG
svg_content = doc.to_svg()
```

## License

MIT License - see LICENSE file for details

## Contributing

See CONTRIBUTING.md for guidelines on how to contribute to this project.