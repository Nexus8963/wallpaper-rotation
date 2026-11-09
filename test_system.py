#!/usr/bin/env python3
"""Check the Cinnamon wallpaper rotator's runtime requirements."""

import shutil
import subprocess
import sys

try:
    from PIL import Image
    from wallpaper_rotator import WallpaperRotator
except ImportError as error:
    print(f"Missing dependency: {error}. Install Python Pillow 9.1 or later.", file=sys.stderr)
    sys.exit(1)


def main():
    if not hasattr(Image, "Resampling"):
        print("Pillow 9.1 or later is required.", file=sys.stderr)
        return 1
    for command in ("xrandr", "gsettings"):
        if not shutil.which(command):
            print(f"Missing required command: {command}", file=sys.stderr)
            return 1
    try:
        rotator = WallpaperRotator()
        monitors = rotator.get_monitors()
        wallpapers = rotator.get_wallpapers()
        subprocess.run(["gsettings", "range", "org.cinnamon.desktop.background", "picture-options"],
                       check=True, capture_output=True, text=True)
        print(f"Wallpaper directory: {rotator.wallpaper_dir}")
        print(f"Active monitors: {', '.join(m.name for m in monitors)}")
        print(f"Distinct image files: {len(wallpapers)}")
        if len(wallpapers) < len(monitors):
            print("Not enough distinct images for all monitors.", file=sys.stderr)
            return 1
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print(f"System check failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
