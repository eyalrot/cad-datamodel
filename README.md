# CAD Drawing Application Data Model

[![CI](https://github.com/eyalrot/cad-datamodel/actions/workflows/ci.yml/badge.svg)](https://github.com/eyalrot/cad-datamodel/actions/workflows/ci.yml)
[![Coverage: 92%](https://img.shields.io/badge/coverage-92%25-brightgreen.svg)](https://github.com/eyalrot/cad-datamodel/blob/master/COVERAGE.md)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

A comprehensive Python data model package for CAD drawing applications that supports geometric shapes, layers, groups, styling, and SVG rendering/persistence.

## 🎯 Features

- **📐 Shape System**: Rectangle, Circle, Line, Polygon, Polyline, and Group support
- **📑 Layer Management**: Organize shapes in layers with z-ordering
- **🎨 Style System**: Comprehensive styling with fill, stroke, and inheritance
- **🔄 Transform Support**: Translation, rotation, and scaling with matrix operations
- **📄 SVG Integration**: Clean import/export to SVG format
- **🔍 Type Safety**: Full type annotations and mypy strict mode support
- **⚡ Performance**: Optimized for handling 100,000+ shapes
- **🧩 Extensible**: Clean architecture with interfaces for custom shapes and renderers

## 📦 Installation

### From PyPI (Coming Soon)
```bash
pip install cad-datamodel
```

### From Source
```bash
git clone https://github.com/eyalrot/cad-datamodel.git
cd cad-datamodel
pip install -e .
```

## 🚀 Quick Start

Here's a simple example to get you started:

```python
from cad_datamodel.core import (
    Point, 
    Color,
    Transform,
    ShapeType
)

# Note: Shape implementations coming in next stories
# This example shows the planned API

# Create basic shapes (placeholder - actual implementation coming)
# rect = Rectangle(x=10, y=10, width=100, height=50)
# circle = Circle(center=Point(100, 100), radius=30)

# Work with colors
red = Color.from_hex("#FF0000")
blue = Color(red=0, green=0, blue=255, alpha=128)

# Create transforms
transform = Transform.translation(50, 50).compose(
    Transform.rotation(45, center=Point(50, 50))
)

# Apply transform to a point
original = Point(10, 10)
transformed = transform.apply_to_point(original)
```

## 🛠️ Development Setup

### Prerequisites

- Python 3.9 or higher
- Git

### Setting Up Development Environment

1. **Clone the repository**
   ```bash
   git clone https://github.com/eyalrot/cad-datamodel.git
   cd cad-datamodel
   ```

2. **Install in development mode**
   ```bash
   # Install with all development dependencies
   pip install -e ".[dev]"
   ```

3. **Install pre-commit hooks** (optional but recommended)
   ```bash
   pre-commit install
   ```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=cad_datamodel --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_core.py

# Run with verbose output
pytest -v
```

### Code Quality Checks

```bash
# Type checking
mypy cad_datamodel --strict

# Linting
ruff check cad_datamodel tests

# Format checking
ruff format --check cad_datamodel tests

# Auto-fix linting issues
ruff check --fix cad_datamodel tests

# Auto-format code
ruff format cad_datamodel tests
```

### Building Documentation

```bash
# Install documentation dependencies
pip install -e ".[docs]"

# Build HTML documentation
cd docs
make html

# View documentation
open _build/html/index.html  # macOS
xdg-open _build/html/index.html  # Linux
```

## 🧪 Testing

The project maintains high test coverage (92%) with a comprehensive test suite:

```bash
# Run tests with coverage report
pytest --cov=cad_datamodel --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=cad_datamodel --cov-report=html

# View coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

See [COVERAGE.md](COVERAGE.md) for detailed coverage information.

## 📚 Documentation

- [API Reference](https://cad-datamodel.readthedocs.io/) (Coming Soon)
- [Architecture Overview](docs/architecture.md)
- [Contributing Guide](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)
- [Coverage Report](COVERAGE.md)

## 🏗️ Project Structure

```
cad-datamodel/
├── cad_datamodel/         # Source code
│   ├── core/              # Base classes and interfaces
│   ├── shapes/            # Shape implementations
│   ├── layers/            # Layer management
│   ├── styles/            # Styling system
│   ├── transform/         # Geometric transformations
│   ├── geometry/          # Geometric calculations
│   └── persistence/       # Save/load functionality
├── tests/                 # Test suite
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   └── performance/      # Performance benchmarks
├── docs/                  # Documentation
└── examples/             # Example scripts
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:

- Code of Conduct
- Development process
- Submitting pull requests
- Coding standards

## 🗺️ Roadmap

### Current Status: Foundation Phase

- ✅ Project structure setup
- ✅ Core module with base interfaces
- ✅ CI/CD pipeline
- 🔄 Documentation (in progress)
- 🔲 Shape implementations
- 🔲 Layer management
- 🔲 SVG import/export

See our [project board](https://github.com/eyalrot/cad-datamodel/projects) for detailed progress.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with modern Python packaging standards (PEP 517/518)
- Inspired by industry-standard CAD applications
- Uses best practices from the Python community

## 📞 Support

- 📧 Email: eyal.rot1@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/eyalrot/cad-datamodel/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/eyalrot/cad-datamodel/discussions)

---

Made with ❤️ using Python