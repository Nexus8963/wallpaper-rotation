# Multi-Monitor Wallpaper Rotator

Rotate different local images across Cinnamon monitors on X11, every ten minutes
by default. The program detects the position and resolution of each active
monitor and creates one combined image, displayed using Cinnamon's `spanned`
background setting. Images are cropped to fill each monitor.

At least one distinct image file is required per monitor. Duplicate files with
identical contents count as one image. Mirrored or overlapping monitors cannot
display different wallpapers using this method. The program logs errors and
retries at the next interval. Disable Cinnamon's own wallpaper slideshow to
prevent it from overriding the rotation.

## Requirements

- Cinnamon on X11 (other desktop environments and Wayland are not supported)
- Python 3.8 or later and Pillow 9.1 or later
- `xrandr`, `gsettings` and systemd user services

On Debian/Ubuntu/Linux Mint install the dependencies with:

```bash
sudo apt install python3 python3-pil x11-xserver-utils libglib2.0-bin
```

## Installation

```bash
git clone https://github.com/Nexus8963/wallpaper-rotation.git
cd wallpaper-rotation
./install.sh
```

The installer copies the program to `~/.local/bin`, creates a configuration
file if needed, and enables the systemd user service for login. Start or
restart it with `systemctl --user restart wallpaper-rotator`. The program
applies a wallpaper immediately, then repeats at the configured interval.

## Configuration

Edit `~/.config/wallpaper-rotation/config.json`:

```json
{
  "wallpaper_dir": "/path/to/your/images",
  "rotation_interval": 600,
  "supported_formats": [".jpg", ".jpeg", ".png", ".bmp", ".gif"]
}
```

Paths are case-sensitive. Restart the service after changes:
`systemctl --user restart wallpaper-rotator`.

## Status and troubleshooting

```bash
python3 test_system.py
systemctl --user status wallpaper-rotator --no-pager
journalctl --user -u wallpaper-rotator -n 50 --no-pager
```

The combined wallpapers and log are stored in
`~/.local/share/wallpaper-rotation/`. If images do not change, verify that the
directory exists, contains enough distinct readable images, Cinnamon's slideshow
is disabled, and the monitors are configured as an extended desktop.

## Uninstallation

Stop and disable the service with `systemctl --user disable --now wallpaper-rotator`,
then remove `~/.local/bin/wallpaper-rotator` and
`~/.config/systemd/user/wallpaper-rotator.service`. Configuration and generated
images may be removed separately. Choose a new background in Cinnamon's settings.

## License

MIT; see [LICENSE](LICENSE).
