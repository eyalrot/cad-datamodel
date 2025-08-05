# CI/CD Pipeline Documentation

This directory contains the GitHub Actions workflows for the CAD Data Model project.

## Overview

The CI pipeline runs all tests and quality checks inside Docker containers to ensure consistency across different environments. It supports Python 3.11 and 3.12.

## Workflow: ci.yml

### Triggers
- Push to `main`, `master`, or `develop` branches
- Pull requests targeting these branches
- Manual workflow dispatch

### Jobs

1. **build-and-test**: Main job that runs for each Python version
   - Builds Docker image with caching
   - Runs linting (ruff)
   - Runs type checking (mypy)
   - Runs tests with coverage
   - Uploads coverage reports

2. **lint-dockerfile**: Validates Dockerfile syntax using Hadolint

3. **all-checks-passed**: Summary job that ensures all checks pass

### Features
- Matrix strategy for Python 3.11 and 3.12
- Docker layer caching for faster builds
- Coverage reporting with Codecov integration
- Artifact uploads for coverage reports

## Local Testing

You can test the CI pipeline locally using Docker Compose:

```bash
# Run all CI checks for both Python versions
./test-ci-local.sh

# Or use docker-compose directly:
# Python 3.11
docker-compose run --rm ci-py311 make ci

# Python 3.12
docker-compose run --rm ci-py312 make ci

# Run specific checks
docker-compose run --rm lint
docker-compose run --rm typecheck
docker-compose run --rm test-py311
docker-compose run --rm test-py312
```

## Docker Configuration

The project includes:
- **Dockerfile**: Multi-stage build supporting both Python versions
- **docker-compose.yml**: Services for development and CI testing

### Docker Stages
- `base`: Base image with dependencies
- `development`: Full development environment
- `ci`: CI-specific configuration
- `test`: Test runner
- `lint`: Linting tools
- `typecheck`: Type checking tools

## Debugging CI Failures

1. Check the GitHub Actions log for specific error messages
2. Reproduce locally using the same Python version:
   ```bash
   docker-compose run --rm py311 make ci
   ```
3. For interactive debugging:
   ```bash
   docker-compose run --rm py311 /bin/bash
   ```