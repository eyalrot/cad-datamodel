#!/bin/bash
# Script to test CI locally using Docker

echo "=== Testing CI Pipeline Locally ==="
echo

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to run a test and check result
run_test() {
    local name=$1
    local command=$2
    echo -e "${YELLOW}Running: ${name}${NC}"
    if eval "${command}"; then
        echo -e "${GREEN}✓ ${name} passed${NC}\n"
        return 0
    else
        echo -e "${RED}✗ ${name} failed${NC}\n"
        return 1
    fi
}

# Track overall status
FAILED=0

# Test Python 3.11
echo "=== Testing Python 3.11 ==="
run_test "Build Python 3.11 image" "docker-compose build ci-py311" || ((FAILED++))
run_test "Lint (Python 3.11)" "docker-compose run --rm ci-py311 python -m ruff check cad_datamodel/ tests/" || ((FAILED++))
run_test "Type check (Python 3.11)" "docker-compose run --rm ci-py311 python -m mypy cad_datamodel" || ((FAILED++))
run_test "Tests (Python 3.11)" "docker-compose run --rm test-py311" || ((FAILED++))

echo
echo "=== Testing Python 3.12 ==="
run_test "Build Python 3.12 image" "docker-compose build ci-py312" || ((FAILED++))
run_test "Lint (Python 3.12)" "docker-compose run --rm ci-py312 python -m ruff check cad_datamodel/ tests/" || ((FAILED++))
run_test "Type check (Python 3.12)" "docker-compose run --rm ci-py312 python -m mypy cad_datamodel" || ((FAILED++))
run_test "Tests (Python 3.12)" "docker-compose run --rm test-py312" || ((FAILED++))

echo
echo "=== Summary ==="
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed! 🎉${NC}"
    exit 0
else
    echo -e "${RED}${FAILED} test(s) failed 😞${NC}"
    exit 1
fi