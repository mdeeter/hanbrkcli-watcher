#!/usr/bin/env python3
"""
HandBrake Folder Watcher

This script watches a folder for video files, encodes them using HandBrakeCLI
with a configurable preset, and moves them to a done directory.

Usage:
    python handbrake_watcher.py

Requirements:
    - HandBrakeCLI must be installed and available in PATH
    - watchdog library: pip install watchdog

Configuration:
    - Edit config.ini to customize directories, encoding preset, and other settings
"""

import os
import sys
import time
import subprocess
import logging
import configparser
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Load configuration
def load_config():
    """Load configuration from config.ini file."""
    config = configparser.ConfigParser()
    config_file = Path(__file__).parent / "config.ini"
    
    # Default configuration
    defaults = {
        'input_dir': 'input',
        'output_dir': 'output',
        'done_dir': 'done',
        'log_dir': 'logs',
        'preset': 'Very Fast 720p30',
        'video_extensions': '.mp4,.avi,.mkv,.mov,.wmv,.flv,.webm,.m4v,.mpg,.mpeg',
        'stabilization_time': '3',
        'stabilization_check_interval': '1',
        'log_level': 'INFO'
    }
    
    # Try to read config file
    if config_file.exists():
        try:
            config.read(config_file)
            logger_temp = logging.getLogger(__name__)
            logger_temp.info(f"Loaded configuration from: {config_file}")
        except Exception as e:
            print(f"Warning: Could not read config file: {e}")
            print("Using default configuration")
    else:
        print(f"Config file not found: {config_file}")
        print("Using default configuration")
    
    # Get configuration values with fallbacks
    script_dir = Path(__file__).parent
    
    input_dir = config.get('Directories', 'input_dir', fallback=defaults['input_dir'])
    output_dir = config.get('Directories', 'output_dir', fallback=defaults['output_dir'])
    done_dir = config.get('Directories', 'done_dir', fallback=defaults['done_dir'])
    log_dir = config.get('Directories', 'log_dir', fallback=defaults['log_dir'])
    
    # Convert to Path objects, handling both relative and absolute paths
    input_dir = Path(input_dir) if Path(input_dir).is_absolute() else script_dir / input_dir
    output_dir = Path(output_dir) if Path(output_dir).is_absolute() else script_dir / output_dir
    done_dir = Path(done_dir) if Path(done_dir).is_absolute() else script_dir / done_dir
    log_dir = Path(log_dir) if Path(log_dir).is_absolute() else script_dir / log_dir
    
    # Get other settings
    preset = config.get('Encoding', 'preset', fallback=defaults['preset'])
    
    extensions_str = config.get('FileHandling', 'video_extensions', fallback=defaults['video_extensions'])
    video_extensions = set(ext.strip() for ext in extensions_str.split(','))
    
    stabilization_time = int(config.get('FileHandling', 'stabilization_time', fallback=defaults['stabilization_time']))
    stabilization_check_interval = int(config.get('FileHandling', 'stabilization_check_interval', fallback=defaults['stabilization_check_interval']))
    
    log_level = config.get('Logging', 'log_level', fallback=defaults['log_level'])
    
    return {
        'INPUT_DIR': input_dir,
        'OUTPUT_DIR': output_dir,
        'DONE_DIR': done_dir,
        'LOG_DIR': log_dir,
        'HANDBRAKE_PRESET': preset,
        'VIDEO_EXTENSIONS': video_extensions,
        'STABILIZATION_TIME': stabilization_time,
        'STABILIZATION_CHECK_INTERVAL': stabilization_check_interval,
        'LOG_LEVEL': log_level
    }

# Load configuration
CONFIG = load_config()

# Configuration variables (for backward compatibility)
INPUT_DIR = CONFIG['INPUT_DIR']
OUTPUT_DIR = CONFIG['OUTPUT_DIR']
DONE_DIR = CONFIG['DONE_DIR']
LOG_DIR = CONFIG['LOG_DIR']
VIDEO_EXTENSIONS = CONFIG['VIDEO_EXTENSIONS']
HANDBRAKE_PRESET = CONFIG['HANDBRAKE_PRESET']
STABILIZATION_TIME = CONFIG['STABILIZATION_TIME']
STABILIZATION_CHECK_INTERVAL = CONFIG['STABILIZATION_CHECK_INTERVAL']

# Setup logging
LOG_DIR.mkdir(exist_ok=True)

# Convert log level string to logging constant
log_level_str = CONFIG['LOG_LEVEL'].upper()
log_level = getattr(logging, log_level_str, logging.INFO)

logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / 'handbrake_watcher.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class VideoFileHandler(FileSystemEventHandler):
    """Handle file system events for video files."""
    
    def __init__(self):
        self.processing_files = set()
    
    def on_created(self, event):
        """Handle file creation events."""
        if not event.is_directory:
            self.process_file(event.src_path)
    
    def on_moved(self, event):
        """Handle file move events (like when a file is copied completely)."""
        if not event.is_directory:
            self.process_file(event.dest_path)
    
    def process_file(self, file_path):
        """Process a video file if it's valid and not already being processed."""
        file_path = Path(file_path).resolve()  # Resolve to absolute canonical path
        
        # Check if it's a video file
        if file_path.suffix.lower() not in VIDEO_EXTENSIONS:
            return
        
        # Avoid processing the same file multiple times
        if str(file_path) in self.processing_files:
            return
        
        # Verify file exists
        if not file_path.exists():
            logger.warning(f"File does not exist: {file_path}")
            return
        
        # Wait for file to be completely written
        self.wait_for_file_stable(file_path)
        
        # Add to processing set
        self.processing_files.add(str(file_path))
        
        try:
            self.encode_video(file_path)
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
        finally:
            # Remove from processing set
            self.processing_files.discard(str(file_path))
    
    def wait_for_file_stable(self, file_path, check_interval=None, stable_duration=None):
        """Wait for file to be stable (not being written to)."""
        # Use config values if not provided
        if check_interval is None:
            check_interval = STABILIZATION_CHECK_INTERVAL
        if stable_duration is None:
            stable_duration = STABILIZATION_TIME
            
        logger.info(f"Waiting for file to stabilize: {file_path.name}")
        
        previous_size = 0
        stable_count = 0
        
        while stable_count < stable_duration:
            try:
                current_size = file_path.stat().st_size
                if current_size == previous_size and current_size > 0:
                    stable_count += 1
                else:
                    stable_count = 0
                    previous_size = current_size
                
                time.sleep(check_interval)
            except (OSError, FileNotFoundError):
                # File might be in the process of being written
                time.sleep(check_interval)
                stable_count = 0
        
        logger.info(f"File stabilized: {file_path.name}")
    
    def encode_video(self, input_file):
        """Encode video using HandBrakeCLI."""
        input_file = Path(input_file).resolve()  # Resolve to absolute path
        output_file = OUTPUT_DIR / f"{input_file.stem}_encoded.mp4"
        done_file = DONE_DIR / input_file.name
        
        logger.info(f"Starting encoding: {input_file.name}")
        print(f"\n{'='*60}")
        print(f"🎬 Encoding: {input_file.name}")
        print(f"{'='*60}")
        
        # Check if HandBrakeCLI is available
        try:
            subprocess.run(['HandBrakeCLI', '--version'], 
                         capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.error("HandBrakeCLI not found. Please install HandBrake CLI.")
            return False
        
        # Verify input file exists before encoding
        if not input_file.exists():
            logger.error(f"Input file not found: {input_file}")
            print(f"❌ Error: Input file not found!")
            return False
        
        # Build HandBrake command
        cmd = [
            'HandBrakeCLI',
            '--input', str(input_file),
            '--output', str(output_file),
            '--preset', HANDBRAKE_PRESET
        ]
        
        try:
            # Run HandBrake encoding with real-time progress
            logger.info(f"Encoding command: {' '.join(cmd)}")
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Track progress
            last_progress = -1
            for line in process.stdout:
                # HandBrake outputs progress in stderr/stdout with patterns like:
                # "Encoding: task 1 of 1, 45.67 % (23.45 fps, avg 24.12 fps, ETA 00h05m23s)"
                if 'Encoding:' in line and '%' in line:
                    try:
                        # Extract percentage
                        percent_start = line.find(',') + 1
                        percent_end = line.find('%', percent_start)
                        if percent_start > 0 and percent_end > 0:
                            percent_str = line[percent_start:percent_end].strip()
                            percent = float(percent_str)
                            
                            # Only update if progress changed by at least 1%
                            if int(percent) > int(last_progress):
                                last_progress = percent
                                
                                # Extract ETA if available
                                eta = "calculating..."
                                if 'ETA' in line:
                                    eta_start = line.find('ETA') + 4
                                    eta_end = line.find(')', eta_start)
                                    if eta_end > eta_start:
                                        eta = line[eta_start:eta_end].strip()
                                
                                # Create progress bar
                                bar_length = 40
                                filled = int(bar_length * percent / 100)
                                bar = '█' * filled + '░' * (bar_length - filled)
                                
                                # Print progress (overwrite same line)
                                print(f"\r📊 Progress: [{bar}] {percent:.1f}% | ETA: {eta}", end='', flush=True)
                    except (ValueError, IndexError):
                        pass
                
                # Log other important messages
                elif 'error' in line.lower() or 'warning' in line.lower():
                    logger.debug(line.strip())
            
            process.wait()
            
            if process.returncode == 0:
                print(f"\n✅ Encoding completed successfully!")
                logger.info(f"Encoding completed successfully: {input_file.name}")
                
                # Verify input file still exists before moving
                if not input_file.exists():
                    logger.error(f"Input file disappeared: {input_file}")
                    print(f"⚠️  Warning: Original file not found, cannot move to done folder")
                    print(f"📤 Encoded file: {output_file.name}")
                    print(f"{'='*60}\n")
                    return True
                
                # Move original file to done directory
                try:
                    done_file.parent.mkdir(exist_ok=True)
                    input_file.rename(done_file)
                    logger.info(f"Original file moved to: {done_file}")
                    print(f"📁 Original moved to: {done_file.name}")
                    print(f"📤 Encoded file: {output_file.name}")
                    print(f"{'='*60}\n")
                except Exception as move_error:
                    logger.error(f"Failed to move original file: {move_error}")
                    print(f"⚠️  Warning: Could not move original file: {move_error}")
                    print(f"📤 Encoded file: {output_file.name}")
                    print(f"{'='*60}\n")
                
                return True
            else:
                print(f"\n❌ Encoding failed!")
                logger.error(f"HandBrake encoding failed for {input_file.name}")
                
                # Clean up failed output file
                if output_file.exists():
                    output_file.unlink()
                
                return False
            
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            logger.error(f"Unexpected error encoding {input_file.name}: {e}")
            
            # Clean up failed output file if it exists
            try:
                if output_file.exists():
                    output_file.unlink()
                    logger.info(f"Cleaned up partial output file: {output_file}")
            except Exception as cleanup_error:
                logger.error(f"Failed to clean up output file: {cleanup_error}")
            
            return False


def check_handbrake_installation():
    """Check if HandBrakeCLI is installed and available."""
    try:
        result = subprocess.run(['HandBrakeCLI', '--version'], 
                              capture_output=True, text=True, check=True)
        version_line = result.stdout.split('\n')[0]
        logger.info(f"HandBrakeCLI found: {version_line}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.error("HandBrakeCLI not found!")
        logger.error("Please install HandBrake CLI:")
        logger.error("  macOS: brew install handbrake")
        logger.error("  Or download from: https://handbrake.fr/downloads.php")
        return False


def check_preset_availability():
    """Check if the specified preset is available."""
    try:
        result = subprocess.run(['HandBrakeCLI', '--preset-list'], 
                              capture_output=True, text=True, check=True)
        
        # Look for preset name in the output lines
        preset_found = False
        for line in result.stdout.split('\n'):
            line = line.strip()
            if line == HANDBRAKE_PRESET:
                preset_found = True
                break
        
        if preset_found:
            logger.info(f"Preset '{HANDBRAKE_PRESET}' is available")
            return True
        else:
            logger.warning(f"Preset '{HANDBRAKE_PRESET}' not found in available presets")
            logger.info("Available General presets (first few):")
            in_general = False
            count = 0
            for line in result.stdout.split('\n'):
                line = line.strip()
                if line == "General/":
                    in_general = True
                    continue
                elif line.endswith("/") and in_general:
                    break
                elif in_general and line and count < 10:
                    logger.info(f"  {line}")
                    count += 1
            return False
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.error("Could not check HandBrake presets")
        return False


def main():
    """Main function to start the folder watcher."""
    logger.info("Starting HandBrake Folder Watcher")
    logger.info(f"Encoding preset: {HANDBRAKE_PRESET}")
    logger.info(f"Video extensions: {', '.join(sorted(VIDEO_EXTENSIONS))}")
    
    # Create directories if they don't exist (with parent directories)
    print("\n🔧 Checking directories...")
    directories = {
        'Input': INPUT_DIR,
        'Output': OUTPUT_DIR,
        'Done': DONE_DIR
    }
    
    for name, directory in directories.items():
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created {name.lower()} directory: {directory.absolute()}")
            print(f"✅ Created {name} directory: {directory.absolute()}")
        else:
            logger.info(f"{name} directory: {directory.absolute()}")
            print(f"✅ {name} directory: {directory.absolute()}")
    
    print()
    
    # Check HandBrake installation
    if not check_handbrake_installation():
        sys.exit(1)
    
    # Check preset availability (informational only)
    check_preset_availability()
    
    # Set up file watcher
    event_handler = VideoFileHandler()
    
    # Scan for existing files in input directory
    logger.info(f"Scanning input directory for existing files...")
    existing_files = []
    for file_path in INPUT_DIR.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in VIDEO_EXTENSIONS:
            existing_files.append(file_path)
    
    if existing_files:
        logger.info(f"Found {len(existing_files)} existing video file(s) to process")
        print(f"\n📁 Found {len(existing_files)} existing video file(s) in input folder")
        print(f"{'='*60}")
        for file_path in existing_files:
            print(f"  • {file_path.name}")
        print(f"{'='*60}\n")
        
        # Process existing files
        for file_path in existing_files:
            logger.info(f"Processing existing file: {file_path.name}")
            event_handler.process_file(str(file_path))
    else:
        logger.info("No existing video files found in input directory")
    
    # Set up file system observer
    observer = Observer()
    observer.schedule(event_handler, str(INPUT_DIR), recursive=False)
    
    # Start watching
    observer.start()
    logger.info(f"Watching for video files in: {INPUT_DIR}")
    logger.info("Drop video files into the input directory to start encoding...")
    logger.info("Press Ctrl+C to stop")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping folder watcher...")
        observer.stop()
    
    observer.join()
    logger.info("Folder watcher stopped")


if __name__ == "__main__":
    main()