#!/bin/bash

# SSH Simulator Quick Start
# Run this script to start the SSH practice simulator

echo "🚀 Starting SSH Login Practice Simulator..."
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Please install Python 3.7 or later"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $PYTHON_VERSION found"

# Navigate to script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "✓ Working directory: $SCRIPT_DIR"
echo ""

# Start the server
echo "Starting server..."
python3 app.py

