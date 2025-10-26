#!/bin/bash
# Setup script for Blink Camera Archiver

echo "Setting up Blink Camera Archiver..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or later."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Create config from example if it doesn't exist
if [ ! -f "config.json" ]; then
    echo "Creating config.json from example..."
    cp config.example.json config.json
    echo ""
    echo "IMPORTANT: Please edit config.json with your Blink credentials!"
    echo ""
fi

# Make run script executable
chmod +x run.sh

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit config.json with your Blink account credentials"
echo "2. Run: ./run.sh --once (for a single check)"
echo "   or: ./run.sh (for continuous monitoring)"
echo ""
echo "To run in background: nohup ./run.sh &"
echo ""
