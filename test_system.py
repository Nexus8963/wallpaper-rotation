#!/usr/bin/env python3
"""
Quick test script to verify wallpaper rotator functionality
"""

import subprocess
import sys
from pathlib import Path

def check_command(cmd):
    """Check if a command is available."""
    try:
        subprocess.run(['which', cmd], capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("Wallpaper Rotator - System Check")
    print("=" * 50)

    # Check Python version
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    print(f"✓ Python: {py_version}")

    # Check required tools
    print("\nRequired tools:")
    xrandr = check_command('xrandr')
    print(f"{'✓' if xrandr else '✗'} xrandr: {'installed' if xrandr else 'NOT FOUND'}")

    print("\nWallpaper setting tools (at least one required):")
    feh = check_command('feh')
    nitrogen = check_command('nitrogen')
    gsettings = check_command('gsettings')

    print(f"{'✓' if feh else '✗'} feh: {'installed' if feh else 'not installed'}")
    print(f"{'✓' if nitrogen else '✗'} nitrogen: {'installed' if nitrogen else 'not installed'}")
    print(f"{'✓' if gsettings else '✗'} gsettings: {'installed' if gsettings else 'not installed'}")

    if not (feh or nitrogen or gsettings):
        print("\n⚠️  WARNING: No wallpaper setting tool found!")
        print("Please install at least one: feh, nitrogen, or gsettings")
        return False

    # Check directories
    print("\nDirectories:")
    wallpaper_dir = Path.home() / 'wallpapers'
    print(f"{'✓' if wallpaper_dir.exists() else '✗'} ~/wallpapers: {'exists' if wallpaper_dir.exists() else 'not found'}")

    config_dir = Path.home() / '.config/wallpaper-rotation'
    print(f"{'✓' if config_dir.exists() else '✗'} ~/.config/wallpaper-rotation: {'exists' if config_dir.exists() else 'not found'}")

    # Check monitors
    print("\nMonitors detected:")
    try:
        result = subprocess.run(['xrandr', '--query'], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if ' connected' in line:
                print(f"  ✓ {line.split()[0]}")
    except Exception as e:
        print(f"  ✗ Error detecting monitors: {e}")
        return False

    print("\n" + "=" * 50)
    print("✓ System check complete!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
