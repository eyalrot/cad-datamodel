# CAD Data Model Makefile
# Development and testing automation

.PHONY: help install test coverage lint type-check pre-commit clean docs all

# Default target - show help
help:
	@echo "CAD Data Model - Development Commands"
	@echo "====================================="
	@echo ""
	@echo "Installation:"
	@echo "  make install       Install package in development mode"
	@echo "  make install-dev   Install package with all dev dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  make test          Run all unit tests"
	@echo "  make test-v        Run tests with verbose output"
	@echo "  make test-file F=<file>  Run specific test file"
	@echo "  make coverage      Run tests with coverage report"
	@echo "  make coverage-html Generate HTML coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint          Run ruff linter"
	@echo "  make lint-fix      Run ruff and auto-fix issues"
	@echo "  make type-check    Run mypy type checking"
	@echo "  make format        Format code with ruff"
	@echo ""
	@echo "Pre-commit:"
	@echo "  make pre-commit    Run all pre-commit checks"
	@echo "  make pc-install    Install pre-commit hooks"
	@echo "  make pc-update     Update pre-commit hooks"
	@echo ""
	@echo "Documentation:"
	@echo "  make docs          Build documentation"
	@echo "  make docs-serve    Build and serve docs locally"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean         Remove build artifacts and caches"
	@echo "  make clean-all     Remove all generated files"
	@echo ""
	@echo "Combined:"
	@echo "  make all           Run lint, type-check, and tests"
	@echo "  make check         Same as 'make all'"
	@echo "  make ci            Run all CI checks (lint, type, test, coverage)"

# Installation targets
install:
	python3 -m pip install -e .

install-dev:
	python3 -m pip install -e ".[dev]"
	python3 -m pip install -r requirements-dev.txt

# Testing targets
test:
	python3 -m pytest tests/

test-v:
	python3 -m pytest tests/ -v

test-file:
	python3 -m pytest $(F) -v

# Coverage targets
coverage:
	python3 -m pytest tests/ --cov=cad_datamodel --cov-report=term-missing

coverage-html:
	python3 -m pytest tests/ --cov=cad_datamodel --cov-report=html --cov-report=term
	@echo "Coverage report generated in htmlcov/index.html"

coverage-report: coverage-html
	@python3 -m http.server 8000 --directory htmlcov

# Code quality targets
lint:
	python3 -m ruff check cad_datamodel/ tests/

lint-fix:
	python3 -m ruff check --fix cad_datamodel/ tests/

type-check:
	python3 -m mypy cad_datamodel

format:
	python3 -m ruff format cad_datamodel/ tests/

# Pre-commit targets
pre-commit: lint type-check test
	@echo "All pre-commit checks passed!"

pc-install:
	pre-commit install

pc-update:
	pre-commit autoupdate

pc-run:
	pre-commit run --all-files

# Documentation targets
docs:
	cd docs && make html

docs-serve: docs
	@echo "Serving documentation at http://localhost:8001"
	@python3 -m http.server 8001 --directory docs/_build/html

docs-clean:
	cd docs && make clean

# Cleanup targets
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/

clean-all: clean docs-clean
	find . -type d -name ".tox" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true

# Combined targets
all: lint type-check test

check: all

ci: lint type-check coverage
	@echo "All CI checks passed!"

# Development workflow shortcuts
fix: lint-fix format
	@echo "Code formatting and linting fixes applied!"

dev: install-dev pc-install
	@echo "Development environment setup complete!"

# Quick test during development
qt:
	python3 -m pytest tests/ -x --ff

# Watch tests (requires pytest-watch)
watch:
	python3 -m pytest_watch tests/ -- -x

.DEFAULT_GOAL := help