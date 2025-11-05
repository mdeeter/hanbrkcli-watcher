# HandBrake Folder Watcher Setup Script for Windows (PowerShell)
# This script will install the required dependencies and set up the environment

Write-Host "HandBrake Folder Watcher Setup" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Python is not installed. Please install Python 3.6 or later first." -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    pause
    exit 1
}

# Check if HandBrakeCLI is installed
Write-Host ""
Write-Host "Checking for HandBrakeCLI..." -ForegroundColor Yellow
try {
    $hbVersion = HandBrakeCLI --version 2>&1 | Select-String "HandBrake"
    Write-Host "HandBrakeCLI found: $hbVersion" -ForegroundColor Green
} catch {
    Write-Host ""
    Write-Host "WARNING: HandBrakeCLI not found in PATH!" -ForegroundColor Yellow
    Write-Host "Please install HandBrake CLI from: https://handbrake.fr/downloads.php" -ForegroundColor Yellow
    Write-Host "Or use Chocolatey: choco install handbrake" -ForegroundColor Yellow
    Write-Host "Or use Winget: winget install HandBrake.HandBrake" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "You can continue setup and install HandBrake later." -ForegroundColor Yellow
    pause
}

# Create virtual environment
Write-Host ""
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to create virtual environment" -ForegroundColor Red
    pause
    exit 1
}

# Activate virtual environment and install dependencies
Write-Host ""
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to install dependencies" -ForegroundColor Red
    pause
    exit 1
}

Write-Host ""
Write-Host "==============================" -ForegroundColor Cyan
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "==============================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start the folder watcher, run:" -ForegroundColor Yellow
Write-Host "  .\start_watcher.ps1" -ForegroundColor White
Write-Host ""
Write-Host "Or manually with:" -ForegroundColor Yellow
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "  python handbrake_watcher.py" -ForegroundColor White
Write-Host ""
Write-Host "Then drop video files into the 'input' directory to start encoding." -ForegroundColor Yellow
Write-Host ""
pause
