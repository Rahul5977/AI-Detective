#!/bin/bash

# AI Detective - Startup Script

echo "=================================================="
echo "🕵️  AI Detective - CSP Investigation System"
echo "=================================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    echo ""
    echo "Installing dependencies..."
    source venv/bin/activate
    pip install -r backend/requirements.txt
    echo "✅ Dependencies installed"
else
    echo "✅ Virtual environment found"
fi

echo ""
echo "🚀 Starting backend server..."
echo ""

# Activate virtual environment and start server
source venv/bin/activate
cd backend
python app.py
