# HandBrake Folder Watcher

An automated video encoding system that watches a folder for video files and encodes them using HandBrakeCLI with the "Very Fast 720p30" preset.

## Features

- **Automatic File Detection**: Watches the `input` folder for new video files
- **Fast Encoding**: Uses HandBrake's "Very Fast 720p30" preset for quick processing
- **Real-Time Progress Display**: Visual progress bar with percentage and ETA during encoding
- **File Management**: Automatically moves original files to `done` folder after encoding
- **Comprehensive Logging**: Logs all activities to both console and log files
- **File Stability Check**: Waits for files to be completely copied before processing
- **Multiple Format Support**: Supports common video formats (MP4, AVI, MKV, MOV, etc.)

## Directory Structure

```
handbrake/
├── input/                   # Drop video files here
├── output/                  # Encoded files will be saved here
├── done/                    # Original files moved here after encoding
├── logs/                    # Log files
├── venv/                    # Python virtual environment (auto-created)
├── handbrake_watcher.py     # Main script
├── requirements.txt         # Python dependencies
├── config.ini               # Configuration file
├── config.ini.example       # Example configuration
├── setup_mac.sh             # Setup script (macOS/Linux)
├── setup.bat                # Setup script (Windows Command Prompt)
├── setup.ps1                # Setup script (Windows PowerShell)
├── start_watcher_mac.sh     # Launcher script (macOS/Linux)
├── start_watcher.bat        # Launcher script (Windows Command Prompt)
└── start_watcher.ps1        # Launcher script (Windows PowerShell)
```

└── start_watcher.ps1 # Launcher script (Windows PowerShell)

````

## Prerequisites

- **Python 3.6+**
- **HandBrakeCLI**: The command-line version of HandBrake
- **watchdog**: Python library for file system monitoring (auto-installed by setup script)

## Installation

### Quick Setup (Recommended)

#### macOS/Linux:

#### macOS/Linux:
```bash
./setup_mac.sh
````

#### Windows (Command Prompt):

```cmd
setup.bat
```

#### Windows (PowerShell):

```powershell
.\setup.ps1
```

**Note for PowerShell users:** If you get an execution policy error, run this first:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

This will:

- Create a Python virtual environment
- Install all dependencies
- Verify HandBrake CLI installation
- **Create required directories** (input, output, done, logs)
- Make scripts executable (macOS/Linux)

### Manual Setup

1. **Install HandBrakeCLI**:

   **macOS:**

   ```bash
   brew install handbrake
   ```

   **Windows:**

   - Download from: https://handbrake.fr/downloads.php
   - Or use Chocolatey: `choco install handbrake`
   - Or use Winget: `winget install HandBrake.HandBrake`

   **Linux:**

   ```bash
   # Ubuntu/Debian
   sudo apt install handbrake-cli

   # Or download from: https://handbrake.fr/downloads.php
   ```

2. **Create virtual environment and install dependencies**:

   **macOS/Linux:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

   **Windows (Command Prompt):**

   ```cmd
   python -m venv venv
   venv\Scripts\activate.bat
   pip install -r requirements.txt
   ```

   **Windows (PowerShell):**

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

## Usage

1. **Start the folder watcher**:

   **macOS/Linux:**

   ```bash
   # Easiest method
   ./start_watcher_mac.sh

   # Or manually
   source venv/bin/activate
   python handbrake_watcher.py
   ```

   **Windows (Command Prompt):**

   ```cmd
   REM Easiest method
   start_watcher.bat

   REM Or manually
   venv\Scripts\activate.bat
   python handbrake_watcher.py
   ```

   **Windows (PowerShell):**

   ```powershell
   # Easiest method
   .\start_watcher.ps1

   # Or manually
   .\venv\Scripts\Activate.ps1
   python handbrake_watcher.py
   ```

2. **Drop video files** into the `input` directory

3. **Watch real-time progress** in the console:

   ```
   🔧 Checking directories...
   ✅ Created Input directory: /Users/username/handbrake/input
   ✅ Output directory: /Users/username/handbrake/output
   ✅ Done directory: /Users/username/handbrake/done

   ============================================================
   🎬 Encoding: my_video.mp4
   ============================================================
   📊 Progress: [████████████████████░░░░░░░░░░░░░░░░░░░░] 52.3% | ETA: 00h02m15s
   ```

4. **Find encoded files** in the `output` directory

5. **Original files** are moved to the `done` directory after successful encoding

## Configuration

The script can be customized using the `config.ini` file. If the file doesn't exist, the script will use default values and create directories in the default locations.

**Note:** The script automatically creates the configured directories (input, output, done, logs) if they don't exist, including any parent directories needed for custom paths.

### Creating Your Configuration File

1. Copy the example configuration:

   ```bash
   cp config.ini.example config.ini
   ```

2. Edit `config.ini` to customize settings

### Configuration Options

**Directories:**

- `input_dir` - Where to watch for new video files (default: `input`)
- `output_dir` - Where encoded files will be saved (default: `output`)
- `done_dir` - Where original files are moved after encoding (default: `done`)
- `log_dir` - Where log files are stored (default: `logs`)

All paths can be **relative** (to the script location) or **absolute**. The script will automatically create these directories if they don't exist, including any necessary parent directories.

**Encoding:**

- `preset` - HandBrake preset to use (default: `Very Fast 720p30`)

**File Handling:**

- `video_extensions` - File extensions to watch (default: `.mp4,.avi,.mkv,.mov,.wmv,.flv,.webm,.m4v,.mpg,.mpeg`)
- `stabilization_time` - Seconds to wait for file stability (default: `3`)
- `stabilization_check_interval` - Seconds between stability checks (default: `1`)

**Logging:**

- `log_level` - Logging verbosity: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` (default: `INFO`)

### Example Custom Configuration

```ini
[Directories]
# Use custom absolute paths
input_dir = /Users/username/Videos/ToEncode
output_dir = /Users/username/Videos/Encoded
done_dir = /Users/username/Videos/Archive

[Encoding]
# Use higher quality preset
preset = Fast 1080p30

[FileHandling]
# Only watch for MP4 and MOV files
video_extensions = .mp4,.mov
# Wait longer for large files
stabilization_time = 5
```

## Available HandBrake Presets

To see all available presets, run:

```bash
HandBrakeCLI --preset-list
```

Some popular fast presets:

- "Very Fast 720p30" (default)
- "Very Fast 480p30"
- "Very Fast 1080p30"
- "Fast 720p30"

## Supported Video Formats

- MP4
- AVI
- MKV
- MOV
- WMV
- FLV
- WebM
- M4V
- MPG/MPEG

## Troubleshooting

### HandBrakeCLI not found

Make sure HandBrake CLI is installed and available in your PATH:

```bash
which HandBrakeCLI
HandBrakeCLI --version
```

### Permission issues (macOS/Linux)

The executable permissions are stored in git and should work after cloning. If needed:

```bash
chmod +x setup_mac.sh start_watcher_mac.sh handbrake_watcher.py
```

### PowerShell execution policy (Windows)

If you get "cannot be loaded because running scripts is disabled" error:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

This is a one-time setting that allows locally-created scripts to run.

### Encoding failures

Check the logs for detailed error messages:

```bash
tail -f logs/handbrake_watcher.log
```

## Stopping the Watcher

Press `Ctrl+C` to stop the folder watcher gracefully.

## Safety Features

- **File stability check**: Waits for files to be completely copied before processing
- **Duplicate processing prevention**: Avoids processing the same file multiple times
- **Error handling**: Graceful error handling with detailed logging
- **Original file preservation**: Original files are only moved after successful encoding

## Example Output

```
2025-11-04 12:01:39 - INFO - Starting HandBrake Folder Watcher
2025-11-04 12:01:39 - INFO - Input directory: /Users/mdeeter/GIT/handbrake/input
2025-11-04 12:01:39 - INFO - Output directory: /Users/mdeeter/GIT/handbrake/output
2025-11-04 12:01:39 - INFO - Done directory: /Users/mdeeter/GIT/handbrake/done
2025-11-04 12:01:39 - INFO - HandBrakeCLI found: HandBrake 1.10.2
2025-11-04 12:01:39 - INFO - Watching for video files in: /Users/mdeeter/GIT/handbrake/input
2025-11-04 12:01:39 - INFO - Drop video files into the input directory to start encoding...

============================================================
🎬 Encoding: sample_video.mp4
============================================================
📊 Progress: [████████████████████████████████████████] 100.0% | ETA: 00h00m00s
✅ Encoding completed successfully!
📁 Original moved to: sample_video.mp4
📤 Encoded file: sample_video_encoded.mp4
============================================================
```

## Real-Time Progress Display

The script now shows live encoding progress with:

- **Visual Progress Bar**: Animated bar that fills as encoding progresses
- **Percentage Complete**: Real-time percentage (updates every 1%)
- **Estimated Time**: Shows remaining time (ETA) based on HandBrake calculations
- **Status Indicators**: Emoji-based status messages for quick recognition
  - 🎬 Starting encoding
  - 📊 Encoding in progress
  - ✅ Successfully completed
  - ❌ Failed encoding
  - 📁 Original file moved
  - 📤 Encoded file ready
