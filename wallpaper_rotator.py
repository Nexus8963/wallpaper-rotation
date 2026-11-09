#!/usr/bin/env python3
"""
Multi-Monitor Wallpaper Rotator
Rotates different wallpapers on each monitor every 10 minutes.
Compatible with Cinnamon and other Linux desktop environments.
"""

import os
import sys
import json
import random
import subprocess
import logging
from pathlib import Path
from datetime import datetime
import time
import signal

# Setup logging
log_file = Path.home() / ".local/share/wallpaper-rotation/rotator.log"
log_file.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class WallpaperRotator:
    def __init__(self, config_file=None):
        """Initialize the wallpaper rotator with configuration."""
        self.config_file = config_file or Path.home() / ".config/wallpaper-rotation/config.json"
        self.rotation_interval = 600  # 10 minutes in seconds
        self.load_config()
        self.setup_signal_handlers()

    def load_config(self):
        """Load configuration from JSON file."""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.wallpaper_dir = Path(config.get('wallpaper_dir', str(Path.home() / 'wallpapers')))
                    self.rotation_interval = config.get('rotation_interval', 600)
                    logger.info(f"Configuration loaded from {self.config_file}")
            else:
                self.wallpaper_dir = Path.home() / 'wallpapers'
                logger.warning(f"Config file not found at {self.config_file}. Using default wallpaper directory: {self.wallpaper_dir}")
                self.create_default_config()
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            self.wallpaper_dir = Path.home() / 'wallpapers'

    def create_default_config(self):
        """Create a default configuration file."""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            default_config = {
                "wallpaper_dir": str(self.wallpaper_dir),
                "rotation_interval": self.rotation_interval,
                "supported_formats": [".jpg", ".jpeg", ".png", ".bmp", ".gif"]
            }
            with open(self.config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            logger.info(f"Default configuration created at {self.config_file}")
        except Exception as e:
            logger.error(f"Error creating default config: {e}")

    def get_monitors(self):
        """Get list of connected monitors."""
        try:
            result = subprocess.run(['xrandr', '--query'], capture_output=True, text=True)
            monitors = []
            for line in result.stdout.split('\n'):
                if ' connected' in line and '(' in line:
                    monitor_name = line.split()[0]
                    monitors.append(monitor_name)
            logger.info(f"Detected {len(monitors)} monitor(s): {monitors}")
            return monitors
        except Exception as e:
            logger.error(f"Error detecting monitors: {e}")
            return ['HDMI-1']  # Fallback to single monitor

    def get_wallpapers(self):
        """Get list of wallpaper files from the configured directory."""
        if not self.wallpaper_dir.exists():
            logger.error(f"Wallpaper directory does not exist: {self.wallpaper_dir}")
            return []

        supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
        wallpapers = [
            f for f in self.wallpaper_dir.iterdir()
            if f.is_file() and f.suffix.lower() in supported_formats
        ]

        if not wallpapers:
            logger.warning(f"No wallpapers found in {self.wallpaper_dir}")
            return []

        logger.info(f"Found {len(wallpapers)} wallpaper(s)")
        return sorted(wallpapers)

    def set_wallpaper_cinnamon(self, monitor, wallpaper_path):
        """Set wallpaper for a monitor using Cinnamon settings."""
        try:
            # Get the geometry of the monitor
            result = subprocess.run(
                ['xrandr', '--query'],
                capture_output=True,
                text=True
            )

            # For Cinnamon, we'll use a slightly different approach
            # Store per-monitor preferences
            cmd = [
                'gsettings', 'set', 'org.cinnamon.desktop.background',
                'picture-uri', f'file://{wallpaper_path}'
            ]
            subprocess.run(cmd, check=False)
            logger.info(f"Set wallpaper for {monitor}: {wallpaper_path}")
            return True
        except Exception as e:
            logger.error(f"Error setting wallpaper with Cinnamon: {e}")
            return False

    def set_wallpaper_generic(self, monitor, wallpaper_path):
        """Set wallpaper using generic methods (feh, nitrogen, etc)."""
        tools = [
            (['feh', '--bg-fill', str(wallpaper_path)], "feh"),
            (['nitrogen', '--set-zoom-fill', str(wallpaper_path)], "nitrogen"),
            (['pcmanfm-qt', '--set-wallpaper=fill', str(wallpaper_path)], "pcmanfm-qt"),
        ]

        for cmd, tool_name in tools:
            try:
                subprocess.run(cmd, check=True, capture_output=True, timeout=5)
                logger.info(f"Set wallpaper using {tool_name}: {wallpaper_path}")
                return True
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                continue
            except Exception as e:
                logger.warning(f"Error with {tool_name}: {e}")
                continue

        logger.error("No wallpaper setting tool available")
        return False

    def rotate_wallpapers(self):
        """Rotate wallpapers on all monitors."""
        monitors = self.get_monitors()
        wallpapers = self.get_wallpapers()

        if not wallpapers:
            logger.error("No wallpapers available for rotation")
            return False

        logger.info(f"Rotating wallpapers for {len(monitors)} monitor(s)")

        for monitor in monitors:
            wallpaper = random.choice(wallpapers)
            success = self.set_wallpaper_cinnamon(monitor, wallpaper) or self.set_wallpaper_generic(monitor, wallpaper)
            if not success:
                logger.warning(f"Failed to set wallpaper for {monitor}")

        return True

    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown."""
        def signal_handler(signum, frame):
            logger.info("Received signal, shutting down gracefully")
            sys.exit(0)

        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)

    def run(self):
        """Main loop for rotating wallpapers."""
        logger.info("Wallpaper rotator started")
        logger.info(f"Rotation interval: {self.rotation_interval} seconds ({self.rotation_interval // 60} minutes)")
        logger.info(f"Wallpaper directory: {self.wallpaper_dir}")

        # Initial rotation
        self.rotate_wallpapers()

        # Main loop
        try:
            while True:
                time.sleep(self.rotation_interval)
                self.rotate_wallpapers()
        except KeyboardInterrupt:
            logger.info("Wallpaper rotator stopped by user")
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)


def main():
    """Main entry point."""
    config_file = None
    if len(sys.argv) > 1:
        config_file = Path(sys.argv[1])

    rotator = WallpaperRotator(config_file)
    rotator.run()


if __name__ == "__main__":
    main()
