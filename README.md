# Multi-Monitor Wallpaper Rotator

Automatically rotate different wallpapers on each connected monitor every 10 minutes. Perfect for Linux desktops running Cinnamon, GNOME, KDE, XFCE, and other desktop environments.

## Features

✨ **Multi-Monitor Support** - Each monitor can display a different wallpaper
⏰ **Configurable Rotation** - Default 10 minutes, easily customizable
🎨 **Flexible Image Sources** - Supports JPG, PNG, BMP, and GIF formats
🚀 **Auto-Start** - Launches automatically at login via systemd
📋 **Logging** - Detailed logs for debugging and monitoring
⚙️ **Easy Configuration** - Simple JSON config file
🐧 **Linux Native** - Built with standard Linux tools (xrandr, gsettings, etc.)

## Requirements

- Linux system with X11 or Wayland
- Python 3.6+
- `xrandr` (usually pre-installed)
- One of: `feh`, `nitrogen`, `gsettings` (for wallpaper setting)

### Installation of dependencies

**Ubuntu/Debian:**
```bash
sudo apt install xrandr feh nitrogen python3
```

**Fedora:**
```bash
sudo dnf install xrandr feh nitrogen python3
```

**Arch:**
```bash
sudo pacman -S xrandr feh nitrogen python3
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Nexus8963/wallpaper-rotation.git
cd wallpaper-rotation
```

2. Make the install script executable:
```bash
chmod +x install.sh
```

3. Run the installation script:
```bash
./install.sh
```

The script will:
- Copy the Python script to `~/.local/bin/wallpaper-rotator`
- Install the systemd service to `~/.config/systemd/user/wallpaper-rotator.service`
- Create a configuration file at `~/.config/wallpaper-rotation/config.json`
- Enable the service to start at login
- Optionally start the service immediately

## Configuration

Edit `~/.config/wallpaper-rotation/config.json` to customize:

```json
{
  "wallpaper_dir": "/path/to/your/wallpapers",
  "rotation_interval": 600,
  "supported_formats": [".jpg", ".jpeg", ".png", ".bmp", ".gif"]
}
```

**Parameters:**
- `wallpaper_dir`: Path to your wallpaper directory
- `rotation_interval`: Time in seconds between rotations (600 = 10 minutes)
- `supported_formats`: Image formats to include in rotation

## Usage

### Start the service:
```bash
systemctl --user start wallpaper-rotator
```

### Stop the service:
```bash
systemctl --user stop wallpaper-rotator
```

### Check status:
```bash
systemctl --user status wallpaper-rotator
```

### View logs:
```bash
journalctl --user -u wallpaper-rotator -f
```

### Restart after config changes:
```bash
systemctl --user restart wallpaper-rotator
```

## Logs

Logs are stored at: `~/.local/share/wallpaper-rotation/rotator.log`

## Uninstallation

To remove the wallpaper rotator:

```bash
# Stop and disable the service
systemctl --user stop wallpaper-rotator
systemctl --user disable wallpaper-rotator

# Remove files
rm ~/.local/bin/wallpaper-rotator
rm ~/.config/systemd/user/wallpaper-rotator.service

# Optional: Remove config and logs
rm -rf ~/.config/wallpaper-rotation
rm -rf ~/.local/share/wallpaper-rotation
```

## How it works

1. **Monitor Detection**: Uses `xrandr` to detect connected monitors
2. **Image Selection**: Randomly selects images from your wallpaper directory
3. **Wallpaper Setting**: Uses available tools (feh, nitrogen, gsettings) to set wallpapers
4. **Rotation**: Repeats every configured interval (default: 10 minutes)
5. **Auto-Start**: Systemd service ensures it starts automatically at login

## Desktop Environment Support

- ✅ **Cinnamon** - Full support (primary)
- ✅ **GNOME** - Full support
- ✅ **KDE Plasma** - Good support
- ✅ **XFCE** - Good support
- ✅ **MATE** - Good support
- ✅ **i3/sway** - Supported via feh/nitrogen

## Troubleshooting

### Service won't start
```bash
journalctl --user -u wallpaper-rotator -n 50
```

### Wallpapers not rotating
- Ensure wallpaper directory exists and contains images
- Check that at least one wallpaper tool is installed (feh, nitrogen, etc.)
- Verify configuration path is correct in `config.json`

### Only one monitor gets wallpaper
This is normal behavior - each monitor gets a random wallpaper from your directory.

### Permission denied errors
Make sure the script is executable:
```bash
chmod +x ~/.local/bin/wallpaper-rotator
```

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Created with ❤️ for Linux desktop enthusiasts.
