@echo off
REM HandBrake Folder Watcher Launcher for Windows
REM This script provides an easy way to start the folder watcher

echo HandBrake Folder Watcher
echo =======================
echo.
echo Input folder:  %cd%\input
echo Output folder: %cd%\output
echo Done folder:   %cd%\done
echo.

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import watchdog" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies in virtual environment...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
    echo.
)

REM Check if HandBrakeCLI is available
HandBrakeCLI --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: HandBrakeCLI not found!
    echo Install from: https://handbrake.fr/downloads.php
    echo.
    choice /C YN /M "Continue anyway"
    if errorlevel 2 exit /b 1
    echo.
)

echo Starting folder watcher...
echo Drop video files into the 'input' directory to begin encoding.
echo Press Ctrl+C to stop.
echo.

python handbrake_watcher.py
