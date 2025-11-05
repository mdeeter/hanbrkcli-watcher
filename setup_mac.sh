#!/bin/bash

# HandBrake Folder Watcher Setup Script
# This script will install the required dependencies and set up the environment

echo "HandBrake Folder Watcher Setup"
echo "=============================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if HandBrakeCLI is installed
if ! command -v HandBrakeCLI &> /dev/null; then
    echo "HandBrakeCLI not found. Installing via Homebrew..."
    if command -v brew &> /dev/null; then
        brew install handbrake
    else
        echo "Homebrew not found. Please install HandBrake CLI manually:"
        echo "https://handbrake.fr/downloads.php"
        exit 1
    fi
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies in virtual environment..."
pip install -r requirements.txt

# Make scripts executable
chmod +x handbrake_watcher.py
chmod +x start_watcher.sh

echo ""
echo "Setup complete!"
echo ""
echo "To start the folder watcher, run:"
echo "  ./start_watcher.sh"
echo ""
echo "Or manually with:"
echo "  source venv/bin/activate && python handbrake_watcher.py"
echo ""
echo "Then drop video files into the 'input' directory to start encoding."