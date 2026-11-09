import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from PIL import Image

from wallpaper_rotator import Monitor, WallpaperRotator, parse_monitors, select_wallpapers


class RotationTests(unittest.TestCase):
    def setUp(self):
        self.monitors = [Monitor("right", 4, 4, 3, 0), Monitor("left", 3, 2, 0, 1)]

    def test_parse_active_monitor_geometry(self):
        output = ("right connected primary 4x4+3+0 (normal)\n"
                  "left connected 3x2+0+1 (normal)\n"
                  "unused connected (normal)\n"
                  "disconnected disconnected (normal)\n")
        self.assertEqual(parse_monitors(output), self.monitors)

    def test_overlapping_monitors_rejected(self):
        with self.assertRaisesRegex(ValueError, "overlap"):
            parse_monitors("a connected 4x4+0+0 (normal)\nb connected 3x2+0+1 (normal)")

    def test_selection_distinct_and_changes_on_each_rotation(self):
        images = [Path("a"), Path("b"), Path("c")]
        previous = {}
        for _ in range(100):
            selected = select_wallpapers(self.monitors, images, previous)
            self.assertEqual(len(set(selected.values())), 2)
            for name in previous:
                self.assertNotEqual(selected[name], previous[name])
            previous = selected

    def test_too_few_images_rejected(self):
        with self.assertRaisesRegex(ValueError, "at least 2"):
            select_wallpapers(self.monitors, [Path("a")], {})

    def test_combined_image_and_alternating_uri(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            image_dir = root / "images"
            image_dir.mkdir()
            Image.new("RGB", (10, 10), "red").save(image_dir / "red.png")
            Image.new("RGB", (10, 10), "blue").save(image_dir / "blue.png")
            (image_dir / "copy.png").write_bytes((image_dir / "red.png").read_bytes())
            config = root / "config.json"
            config.write_text(json.dumps({"wallpaper_dir": str(image_dir)}))
            rotator = WallpaperRotator(config)
            rotator.output_dir = root / "output"
            current_uri = ""
            calls = []

            def run(args, **kwargs):
                nonlocal current_uri
                calls.append(args)
                if args[:2] == ["gsettings", "get"]:
                    return SimpleNamespace(stdout=f"'{current_uri}'\n")
                if args[:2] == ["gsettings", "set"] and args[-2] == "picture-uri":
                    current_uri = args[-1]
                return SimpleNamespace(stdout="")

            with patch.object(rotator, "get_monitors", return_value=self.monitors), \
                    patch("wallpaper_rotator.subprocess.run", side_effect=run):
                self.assertEqual(len(rotator.get_wallpapers()), 2)
                rotator.rotate_wallpapers()
                first = rotator.output_dir / "wallpaper-0.png"
                with Image.open(first) as result:
                    self.assertEqual(result.size, (7, 4))
                    self.assertEqual(result.getpixel((0, 0)), (0, 0, 0))
                    self.assertNotEqual(result.getpixel((1, 1)), result.getpixel((4, 1)))
                rotator.rotate_wallpapers()
                self.assertEqual(current_uri, (rotator.output_dir / "wallpaper-1.png").as_uri())
                self.assertIn(["gsettings", "set", "org.cinnamon.desktop.background",
                               "picture-options", "spanned"], calls)


if __name__ == "__main__":
    unittest.main()
