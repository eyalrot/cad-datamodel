# Multi-stage Dockerfile for CAD Data Model
# Supports Python 3.11 and 3.12 via build arguments

# Build argument for Python version
ARG PYTHON_VERSION=3.12

# Base stage with Python
FROM python:${PYTHON_VERSION}-slim AS base

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency files
COPY requirements.txt requirements-dev.txt pyproject.toml setup.py setup.cfg ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip==24.2 && \
    pip install --no-cache-dir -e ".[dev]" && \
    pip install --no-cache-dir -r requirements-dev.txt

# Development stage
FROM base AS development

# Copy source code
COPY cad_datamodel/ ./cad_datamodel/
COPY tests/ ./tests/
COPY docs/ ./docs/

# Copy configuration files
COPY ruff.toml mypy.ini tox.ini Makefile ./
COPY README.md CHANGELOG.md CONTRIBUTING.md COVERAGE.md LICENSE ./

# Create directories for coverage reports
RUN mkdir -p htmlcov

# Default command
CMD ["/bin/bash"]

# CI stage for running tests
FROM development AS ci

# Set environment variables for CI
ENV CI=true
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Run linting by default
CMD ["make", "ci"]

# Test stage
FROM development AS test

# Run tests by default
CMD ["python", "-m", "pytest", "tests/", "-v", "--cov=cad_datamodel", "--cov-report=term-missing", "--cov-report=xml"]

# Lint stage
FROM development AS lint

# Run linting by default
CMD ["python", "-m", "ruff", "check", "cad_datamodel/", "tests/"]

# Type check stage
FROM development AS typecheck

# Run type checking by default
CMD ["python", "-m", "mypy", "cad_datamodel"]