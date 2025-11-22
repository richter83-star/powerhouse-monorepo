
#!/bin/bash

# Start Backend API Server for Powerhouse Multi-Agent Platform
# This script starts the FastAPI backend server

echo "=================================="
echo "Powerhouse Multi-Agent Platform"
echo "Starting Backend API Server"
echo "=================================="
echo ""

# Navigate to backend directory
cd "$(dirname "$0")"

echo "Current directory: $(pwd)"
echo ""

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Error: Python is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "✓ Python version: $(python --version)"
echo ""

# Check if required packages are installed
echo "Checking dependencies..."
python -c "import fastapi" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Error: FastAPI not installed"
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

echo "✓ Dependencies installed"
echo ""

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Start the server
echo "Starting FastAPI server..."
echo "API will be available at:"
echo "  - Main API: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - Health Check: http://localhost:8000/health"
echo "  - Agents API: http://localhost:8000/api/v1/agents"
echo ""
echo "Press CTRL+C to stop the server"
echo ""

python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
