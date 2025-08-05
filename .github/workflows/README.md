# GitHub Actions Workflows

This directory contains the CI/CD pipeline configurations for the CAD Datamodel project.

## Workflows

### CI Pipeline (`ci.yml`)
- **Triggers**: Push to master/main/develop branches and all pull requests
- **Purpose**: Validate code quality and run tests
- **Matrix Testing**: Python 3.9, 3.10, 3.11, and 3.12
- **Steps**:
  1. Code checkout
  2. Python setup with pip caching
  3. Dependency installation
  4. Ruff linting and formatting check
  5. Mypy type checking (strict mode)
  6. Pytest with coverage reporting
  7. Package build verification
  8. Installation verification in fresh environment
  9. Artifact uploads (coverage reports and built packages)

### Release Pipeline (`release.yml`)
- **Status**: Placeholder (disabled) - will be activated in future story
- **Triggers**: Version tags (v*.*.*)
- **Purpose**: Build and publish releases to PyPI
- **Future Features**:
  - Automated PyPI publishing
  - GitHub release creation
  - Release notes generation

## Local Testing

To test the CI pipeline locally:

```bash
# Install all development dependencies
pip install -e ".[dev]"

# Run linting
ruff check cad_datamodel tests
ruff format --check cad_datamodel tests

# Run type checking
mypy cad_datamodel --strict

# Run tests with coverage
pytest tests/unit -v --cov=cad_datamodel --cov-report=term-missing

# Build package
python -m build
```

## Caching Strategy

The CI pipeline uses intelligent caching:
- Python pip packages are cached based on `pyproject.toml` and `requirements*.txt`
- Cache is specific to each Python version
- Build artifacts are only uploaded for Python 3.12 to save storage

## Security

- Workflows use minimal permissions (read-only by default)
- Release workflow will use PyPI trusted publishing (no stored secrets)
- All actions use specific versions (not latest) for reproducibility