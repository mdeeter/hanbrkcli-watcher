# HandBrake Folder Watcher - RESOLVED SETUP

✅ **The script is now working!** The environment issue has been resolved by using a Python virtual environment.

## 🚀 Quick Start (WORKING SOLUTION)

1. **Run the setup script** (installs everything automatically):

   ```bash
   cd /Users/mdeeter/GIT/handbrake
   ./setup.sh
   ```

2. **Start the folder watcher**:

   ```bash
   ./start_watcher.sh
   ```

3. **Drop video files** into the `input` folder and they'll be automatically encoded!

## 📁 What the Setup Creates

```
handbrake/
├── input/              # 📥 Drop your videos here
├── output/             # 📤 Encoded videos appear here
├── done/               # ✅ Original files moved here after encoding
├── logs/               # 📋 Activity logs stored here
├── venv/               # 🐍 Python virtual environment (auto-created)
├── handbrake_watcher.py # 🔧 Main watcher script
├── start_watcher.sh     # 🚀 Easy launcher
└── setup.sh            # ⚙️ Initial setup
```

## ✨ Features

- **🔍 Auto-detection**: Watches for new video files automatically
- **⚡ Fast encoding**: Uses "Very Fast 720p30" preset for speed
- **🔄 Smart file handling**: Waits for files to finish copying before processing
- **📝 Comprehensive logging**: All activity logged to console and files
- **🎬 Multiple formats**: Supports MP4, AVI, MKV, MOV, WMV, FLV, WebM, M4V, MPG, MPEG
- **🛡️ Safe processing**: Originals only moved after successful encoding

## 🔧 How It Works

1. You drop a video file into `input/` folder
2. Script detects the new file and waits for it to stabilize
3. HandBrakeCLI encodes using "Very Fast 720p30" preset
4. Encoded file saved to `output/` folder
5. Original file moved to `done/` folder
6. Everything logged for review

## 📋 Requirements Met

- ✅ **HandBrakeCLI**: Installed and working (v1.10.2)
- ✅ **Python environment**: Virtual environment created and configured
- ✅ **Dependencies**: watchdog library installed in venv
- ✅ **Fast preset**: "Very Fast 720p30" configured for quick encoding

## 🐛 Issue Resolution

**Problem**: Python module conflicts between different Python versions (3.11 vs 3.13) on macOS with Homebrew-managed Python.

**Solution**: Created isolated virtual environment (`venv/`) that:

- Contains its own Python interpreter
- Has watchdog library properly installed
- Avoids system Python conflicts
- Works consistently across different setups

## 🎯 Usage Examples

**Basic usage:**

```bash
# Start the watcher
./start_watcher.sh

# In another terminal, drop files
cp ~/Movies/video.mp4 input/
```

**Monitor progress:**

```bash
# Watch logs in real-time
tail -f logs/handbrake_watcher.log
```

**Manual start (alternative):**

```bash
source venv/bin/activate
python handbrake_watcher.py
```

## ⚙️ Configuration

Want to change settings? Edit `handbrake_watcher.py`:

```python
# Change encoding preset
HANDBRAKE_PRESET = "Fast 1080p30"  # or any other preset

# Add more video formats
VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mkv', '.custom_format'}
```

## 🔍 Available Presets

Run this to see all available presets:

```bash
HandBrakeCLI --preset-list
```

Some fast options:

- `"Very Fast 720p30"` (current - fastest)
- `"Very Fast 1080p30"` (better quality, still fast)
- `"Fast 720p30"` (good balance)

## 🛟 Troubleshooting

### Script won't start

```bash
# Make sure virtual environment is set up
./setup.sh

# Check HandBrake installation
which HandBrakeCLI
```

### Files not being detected

- Make sure files are copied into `input/` folder
- Check file extensions are supported
- Look at logs: `tail -f logs/handbrake_watcher.log`

### Encoding fails

- Check if input file is a valid video
- Look at detailed error in logs
- Verify HandBrake can process the file manually

## 🎉 Success!

Your HandBrake folder watcher is now ready to automatically encode video files with fast processing using the "Very Fast 720p30" preset. Just run `./start_watcher.sh` and start dropping video files into the `input/` directory!
