#!/bin/bash
# Run all tests for satellite imagery aesthetics MCP server

set -e

echo "Running tests..."
echo ""

# Run pytest if available, otherwise use custom runner
if command -v pytest &> /dev/null; then
    pytest tests/ -v --tb=short
else
    echo "pytest not found, using custom test runner..."
    python tests/test_server.py
fi

echo ""
echo "Tests complete!"
