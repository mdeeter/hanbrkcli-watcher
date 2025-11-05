@echo off
REM HandBrake Folder Watcher Setup Script for Windows
REM This script will install the required dependencies and set up the environment

echo HandBrake Folder Watcher Setup
echo ==============================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed. Please install Python 3.6 or later first.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python found!
python --version

REM Check if HandBrakeCLI is installed
echo.
echo Checking for HandBrakeCLI...
HandBrakeCLI --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo WARNING: HandBrakeCLI not found in PATH!
    echo Please install HandBrake CLI from: https://handbrake.fr/downloads.php
    echo Or use Chocolatey: choco install handbrake
    echo Or use Winget: winget install HandBrake.HandBrake
    echo.
    echo You can continue setup and install HandBrake later.
    pause
) else (
    echo HandBrakeCLI found!
    HandBrakeCLI --version 2>&1 | findstr "HandBrake"
)

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment and install dependencies
echo.
echo Installing Python dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ==============================
echo Setup complete!
echo ==============================
echo.
echo To start the folder watcher, run:
echo   start_watcher.bat
echo.
echo Or manually with:
echo   venv\Scripts\activate.bat
echo   python handbrake_watcher.py
echo.
echo Then drop video files into the 'input' directory to start encoding.
echo.
pause
