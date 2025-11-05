#!/bin/bash

# HandBrake Folder Watcher Launcher
# This script provides an easy way to start the folder watcher

cd "$(dirname "$0")"

echo "HandBrake Folder Watcher"
echo "======================="
echo ""
echo "Input folder:  $(pwd)/input"
echo "Output folder: $(pwd)/output" 
echo "Done folder:   $(pwd)/done"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and check dependencies
source venv/bin/activate

# Check if dependencies are installed in venv
if ! python -c "import watchdog" &> /dev/null; then
    echo "Installing dependencies in virtual environment..."
    pip install -r requirements.txt
    echo ""
fi

# Check if HandBrakeCLI is available
if ! command -v HandBrakeCLI &> /dev/null; then
    echo "Warning: HandBrakeCLI not found!"
    echo "Install with: brew install handbrake"
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "Starting folder watcher..."
echo "Drop video files into the 'input' directory to begin encoding."
echo "Press Ctrl+C to stop."
echo ""

python handbrake_watcher.py