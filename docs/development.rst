Development Guide
=================

This guide covers development practices for contributing to CAD Datamodel.

Setting Up Development Environment
----------------------------------

Prerequisites
~~~~~~~~~~~~~

- Python 3.9 or higher
- Git
- A code editor (VS Code, PyCharm, etc.)

Initial Setup
~~~~~~~~~~~~~

1. Fork and clone the repository::

    git clone https://github.com/yourusername/cad-datamodel.git
    cd cad-datamodel

2. Create a virtual environment (optional if using devcontainer)::

    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install in development mode::

    pip install -e ".[dev]"

4. Install pre-commit hooks::

    pre-commit install

Development Workflow
--------------------

Making Changes
~~~~~~~~~~~~~~

1. Create a feature branch::

    git checkout -b feature/your-feature-name

2. Make your changes following the coding standards

3. Run tests locally::

    pytest

4. Check code quality::

    ruff check src tests
    mypy src/cad_datamodel --strict

5. Commit with a descriptive message::

    git commit -m "feat: add new feature"

Commit Message Convention
~~~~~~~~~~~~~~~~~~~~~~~~~

We follow conventional commits:

- ``feat:`` New feature
- ``fix:`` Bug fix
- ``docs:`` Documentation changes
- ``test:`` Test additions or changes
- ``refactor:`` Code refactoring
- ``style:`` Code style changes
- ``chore:`` Build process or auxiliary tool changes

Testing
-------

Running Tests
~~~~~~~~~~~~~

Run all tests::

    pytest

Run with coverage::

    pytest --cov=src/cad_datamodel --cov-report=term-missing

Run specific test module::

    pytest tests/unit/test_core.py

Run specific test::

    pytest tests/unit/test_core.py::TestColor::test_color_from_hex

Writing Tests
~~~~~~~~~~~~~

Follow the AAA pattern (Arrange, Act, Assert):

.. code-block:: python

   def test_point_creation():
       # Arrange
       x, y = 10.5, 20.3
       
       # Act
       point = Point(x, y)
       
       # Assert
       assert point.x == x
       assert point.y == y

Code Quality
------------

Linting
~~~~~~~

We use Ruff for linting and formatting::

    # Check for issues
    ruff check src tests

    # Auto-fix issues
    ruff check --fix src tests

    # Format code
    ruff format src tests

Type Checking
~~~~~~~~~~~~~

We use mypy in strict mode::

    mypy src/cad_datamodel --strict

All public APIs must have type annotations.

Documentation
-------------

Writing Documentation
~~~~~~~~~~~~~~~~~~~~~

- Use Google-style docstrings
- Include examples in docstrings
- Document all public APIs

Building Documentation
~~~~~~~~~~~~~~~~~~~~~~

Build the docs locally::

    cd docs
    make clean
    make html

View the built documentation::

    open _build/html/index.html

Continuous Integration
----------------------

Our CI pipeline runs on every push and PR:

- Tests on Python 3.9, 3.10, 3.11, 3.12
- Linting with Ruff
- Type checking with mypy
- Coverage reporting

All checks must pass before merging.

Architecture Guidelines
-----------------------

Design Principles
~~~~~~~~~~~~~~~~~

1. **Interface Segregation**: Small, focused interfaces
2. **Dependency Inversion**: Depend on abstractions
3. **Open/Closed**: Open for extension, closed for modification
4. **Single Responsibility**: Each class has one reason to change

Adding New Features
~~~~~~~~~~~~~~~~~~~

1. Start with interfaces in the core module
2. Implement concrete classes in appropriate modules
3. Write comprehensive tests
4. Document all public APIs
5. Ensure backward compatibility

Performance Considerations
~~~~~~~~~~~~~~~~~~~~~~~~~~

- Use ``__slots__`` for frequently created objects
- Prefer composition over inheritance
- Cache expensive computations
- Use numpy for numerical operations

Release Process
---------------

Version Numbering
~~~~~~~~~~~~~~~~~

We use semantic versioning (MAJOR.MINOR.PATCH):

- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

Release Checklist
~~~~~~~~~~~~~~~~~

1. Update version in ``pyproject.toml`` and ``__init__.py``
2. Update CHANGELOG.md
3. Run full test suite
4. Build and test package
5. Create git tag
6. Push to GitHub
7. CI will handle PyPI deployment

Getting Help
------------

- GitHub Issues: Bug reports and feature requests
- GitHub Discussions: General questions and discussions
- Email: eyal.rot1@gmail.com