# HandBrake Folder Watcher Launcher for Windows (PowerShell)
# This script provides an easy way to start the folder watcher

Write-Host "HandBrake Folder Watcher" -ForegroundColor Cyan
Write-Host "=======================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Input folder:  $(Get-Location)\input" -ForegroundColor Yellow
Write-Host "Output folder: $(Get-Location)\output" -ForegroundColor Yellow
Write-Host "Done folder:   $(Get-Location)\done" -ForegroundColor Yellow
Write-Host ""

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Failed to create virtual environment" -ForegroundColor Red
        pause
        exit 1
    }
}

# Activate virtual environment
& .\venv\Scripts\Activate.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to activate virtual environment" -ForegroundColor Red
    pause
    exit 1
}

# Check if dependencies are installed
try {
    python -c "import watchdog" 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw
    }
} catch {
    Write-Host "Installing dependencies in virtual environment..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Failed to install dependencies" -ForegroundColor Red
        pause
        exit 1
    }
    Write-Host ""
}

# Check if HandBrakeCLI is available
try {
    HandBrakeCLI --version 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw
    }
} catch {
    Write-Host "WARNING: HandBrakeCLI not found!" -ForegroundColor Yellow
    Write-Host "Install from: https://handbrake.fr/downloads.php" -ForegroundColor Yellow
    Write-Host ""
    $response = Read-Host "Continue anyway? (y/N)"
    if ($response -ne "y" -and $response -ne "Y") {
        exit 1
    }
    Write-Host ""
}

Write-Host "Starting folder watcher..." -ForegroundColor Green
Write-Host "Drop video files into the 'input' directory to begin encoding." -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop." -ForegroundColor Yellow
Write-Host ""

python handbrake_watcher.py
