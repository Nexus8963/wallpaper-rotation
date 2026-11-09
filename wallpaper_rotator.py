#!/usr/bin/env python3
"""Rotate distinct wallpapers across Cinnamon monitors on X11."""

import hashlib
import json
import logging
import random
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageOps

logger = logging.getLogger(__name__)
SCHEMA = "org.cinnamon.desktop.background"
DEFAULT_FORMATS = [".jpg", ".jpeg", ".png", ".bmp", ".gif"]
GEOMETRY = re.compile(r"^(\S+) connected (?:primary )?(\d+)x(\d+)\+(\d+)\+(\d+)(?:\s|$)")


@dataclass(frozen=True)
class Monitor:
    name: str
    width: int
    height: int
    x: int
    y: int


def parse_monitors(output):
    monitors = []
    for line in output.splitlines():
        match = GEOMETRY.match(line)
        if match:
            name, width, height, x, y = match.groups()
            monitors.append(Monitor(name, int(width), int(height), int(x), int(y)))
    if not monitors:
        raise ValueError("No active X11 monitors found in xrandr output")
    for i, first in enumerate(monitors):
        for second in monitors[i + 1:]:
            if (first.x < second.x + second.width and second.x < first.x + first.width
                    and first.y < second.y + second.height and second.y < first.y + first.height):
                raise ValueError(f"Monitors {first.name} and {second.name} overlap; distinct backgrounds require an extended desktop")
    return monitors


def select_wallpapers(monitors, wallpapers, previous):
    """Choose distinct images and avoid each monitor's previous image when possible."""
    if len(wallpapers) < len(monitors):
        raise ValueError(f"Need at least {len(monitors)} distinct images; found {len(wallpapers)}")
    candidates = {monitor.name: random.sample(wallpapers, len(wallpapers)) for monitor in monitors}
    assigned = {}

    def assign(index, avoid_previous):
        if index == len(monitors):
            return True
        monitor = monitors[index]
        for image in candidates[monitor.name]:
            if image in assigned.values() or (avoid_previous and image == previous.get(monitor.name)):
                continue
            assigned[monitor.name] = image
            if assign(index + 1, avoid_previous):
                return True
            del assigned[monitor.name]
        return False

    if not assign(0, True):
        logger.warning("Not enough choices to change every monitor's previous image")
        if not assign(0, False):
            raise ValueError("Could not select distinct images")
    return assigned


class WallpaperRotator:
    def __init__(self, config_file=None):
        self.config_file = config_file or Path.home() / ".config/wallpaper-rotation/config.json"
        self.output_dir = Path.home() / ".local/share/wallpaper-rotation"
        self.previous = {}
        self.load_config()

    def load_config(self):
        if self.config_file.exists():
            with self.config_file.open(encoding="utf-8") as file:
                config = json.load(file)
        else:
            config = {"wallpaper_dir": str(Path.home() / "wallpapers"),
                      "rotation_interval": 600, "supported_formats": DEFAULT_FORMATS}
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            self.config_file.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
        self.wallpaper_dir = Path(config.get("wallpaper_dir", str(Path.home() / "wallpapers"))).expanduser()
        self.rotation_interval = config.get("rotation_interval", 600)
        self.supported_formats = config.get("supported_formats", DEFAULT_FORMATS)
        if (not isinstance(self.rotation_interval, (int, float))
                or isinstance(self.rotation_interval, bool) or self.rotation_interval <= 0):
            raise ValueError("rotation_interval must be a positive number")
        if not isinstance(self.supported_formats, list) or not all(
                isinstance(ext, str) and ext.startswith(".") for ext in self.supported_formats):
            raise ValueError("supported_formats must be a list of extensions starting with a dot")
        self.supported_formats = {ext.lower() for ext in self.supported_formats}

    def get_monitors(self):
        result = subprocess.run(["xrandr", "--query"], check=True, capture_output=True, text=True)
        return parse_monitors(result.stdout)

    def get_wallpapers(self):
        images = []
        seen = set()
        for path in sorted(self.wallpaper_dir.iterdir()):
            if not path.is_file() or path.suffix.lower() not in self.supported_formats:
                continue
            digest = hashlib.sha256()
            with path.open("rb") as file:
                for block in iter(lambda: file.read(1024 * 1024), b""):
                    digest.update(block)
            fingerprint = digest.digest()
            if fingerprint not in seen:
                seen.add(fingerprint)
                images.append(path)
        return images

    def rotate_wallpapers(self):
        monitors = self.get_monitors()
        wallpapers = self.get_wallpapers()
        selected = select_wallpapers(monitors, wallpapers, self.previous)
        width = max(m.x + m.width for m in monitors)
        height = max(m.y + m.height for m in monitors)
        canvas = Image.new("RGB", (width, height), "black")
        for monitor in monitors:
            with Image.open(selected[monitor.name]) as image:
                image = ImageOps.exif_transpose(image).convert("RGB")
                canvas.paste(ImageOps.fit(image, (monitor.width, monitor.height), method=Image.Resampling.LANCZOS),
                             (monitor.x, monitor.y))

        self.output_dir.mkdir(parents=True, exist_ok=True)
        current = subprocess.run(["gsettings", "get", SCHEMA, "picture-uri"],
                                 check=True, capture_output=True, text=True).stdout.strip().strip("'")
        first = self.output_dir / "wallpaper-0.png"
        second = self.output_dir / "wallpaper-1.png"
        target = second if current == first.as_uri() else first
        temporary = target.with_suffix(".tmp")
        try:
            canvas.save(temporary, format="PNG")
            temporary.replace(target)
        finally:
            temporary.unlink(missing_ok=True)
        subprocess.run(["gsettings", "set", SCHEMA, "picture-options", "spanned"], check=True)
        subprocess.run(["gsettings", "set", SCHEMA, "picture-uri", target.as_uri()], check=True)
        self.previous = selected
        for monitor in monitors:
            logger.info("Monitor %s (%dx%d+%d+%d): %s", monitor.name, monitor.width,
                        monitor.height, monitor.x, monitor.y, selected[monitor.name])
        logger.info("Applied combined wallpaper %s", target)

    def run(self):
        logger.info("Wallpaper directory: %s; interval: %s seconds", self.wallpaper_dir, self.rotation_interval)
        while True:
            try:
                self.rotate_wallpapers()
            except (OSError, ValueError, subprocess.SubprocessError) as error:
                logger.error("Wallpaper rotation failed: %s", error, exc_info=True)
            time.sleep(self.rotation_interval)


def main():
    log_file = Path.home() / ".local/share/wallpaper-rotation/rotator.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s",
                        handlers=[logging.FileHandler(log_file), logging.StreamHandler()])
    try:
        WallpaperRotator(Path(sys.argv[1]) if len(sys.argv) > 1 else None).run()
    except (OSError, ValueError, json.JSONDecodeError) as error:
        logger.error("Cannot start wallpaper rotator: %s", error)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
