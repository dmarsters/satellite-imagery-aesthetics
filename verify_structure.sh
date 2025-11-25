#!/bin/bash
# Verify standard MCP project structure

PACKAGE_NAME="satellite_imagery_aesthetics"
ERRORS=0

echo "Verifying project structure..."
echo ""

# Root level checks
echo "Checking root level files..."
for file in README.md pyproject.toml .gitignore LICENSE; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ MISSING: $file"
        ERRORS=$((ERRORS + 1))
    fi
done

# Directory structure checks
echo ""
echo "Checking directory structure..."
for dir in src tests docs "src/$PACKAGE_NAME" "src/$PACKAGE_NAME/ologs"; do
    if [ -d "$dir" ]; then
        echo "  ✓ $dir/"
    else
        echo "  ✗ MISSING: $dir/"
        ERRORS=$((ERRORS + 1))
    fi
done

# Python module checks
echo ""
echo "Checking Python modules..."
for file in "src/$PACKAGE_NAME/__init__.py" "tests/__init__.py"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ MISSING: $file"
        ERRORS=$((ERRORS + 1))
    fi
done

# Server file check
echo ""
echo "Checking core implementation files..."
for file in "src/$PACKAGE_NAME/server.py" "src/$PACKAGE_NAME/ologs/imagery_profiles.yaml"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ MISSING: $file (needs to be added manually)"
    fi
done

# Test files check
echo ""
echo "Checking test files..."
if [ -f "tests/run_tests.sh" ]; then
    echo "  ✓ tests/run_tests.sh"
else
    echo "  ✗ MISSING: tests/run_tests.sh (needs to be added manually)"
fi

if [ -f "tests/test_server.py" ]; then
    echo "  ✓ tests/test_server.py"
else
    echo "  ✗ MISSING: tests/test_server.py (needs to be added manually)"
fi

echo ""
if [ $ERRORS -eq 0 ]; then
    echo "✓ Structure verification passed!"
    echo ""
    echo "Next steps:"
    echo "1. Add server.py to src/$PACKAGE_NAME/"
    echo "2. Add imagery_profiles.yaml to src/$PACKAGE_NAME/ologs/"
    echo "3. Add test files to tests/"
    echo "4. Run: pip install -e '.[dev]'"
    echo "5. Run: ./tests/run_tests.sh"
else
    echo "✗ Structure verification failed with $ERRORS error(s)"
    exit 1
fi
