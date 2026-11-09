#!/bin/bash
# Wallpaper Rotator Installation Script

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="$HOME/.local/bin"
SERVICE_DIR="$HOME/.config/systemd/user"
CONFIG_DIR="$HOME/.config/wallpaper-rotation"
PYTHON_SCRIPT="$SCRIPT_DIR/wallpaper_rotator.py"
SERVICE_FILE="$SCRIPT_DIR/wallpaper-rotator.service"

echo "Installing Wallpaper Rotator..."

# Create necessary directories
mkdir -p "$INSTALL_DIR"
mkdir -p "$SERVICE_DIR"
mkdir -p "$CONFIG_DIR"

# Copy Python script
cp "$PYTHON_SCRIPT" "$INSTALL_DIR/wallpaper-rotator"
chmod +x "$INSTALL_DIR/wallpaper-rotator"
echo "✓ Installed script to $INSTALL_DIR/wallpaper-rotator"

# Copy systemd service
cp "$SERVICE_FILE" "$SERVICE_DIR/wallpaper-rotator.service"
echo "✓ Installed systemd service to $SERVICE_DIR/wallpaper-rotator.service"

# Create default configuration if it doesn't exist
if [ ! -f "$CONFIG_DIR/config.json" ]; then
    cat > "$CONFIG_DIR/config.json" << EOF
{
  "wallpaper_dir": "$HOME/wallpapers",
  "rotation_interval": 600,
  "supported_formats": [".jpg", ".jpeg", ".png", ".bmp", ".gif"]
}
EOF
    echo "✓ Created default configuration at $CONFIG_DIR/config.json"
else
    echo "✓ Configuration already exists at $CONFIG_DIR/config.json"
fi

# Reload systemd
systemctl --user daemon-reload
echo "✓ Reloaded systemd user services"

# Enable and start the service
systemctl --user enable wallpaper-rotator.service
echo "✓ Enabled wallpaper-rotator to start on login"

# Ask user if they want to start now
read -p "Do you want to start the wallpaper rotator now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    systemctl --user start wallpaper-rotator.service
    echo "✓ Started wallpaper rotator"
    sleep 2
    systemctl --user status wallpaper-rotator.service || true
fi

echo ""
echo "Installation complete!"
echo ""
echo "Configuration file: $CONFIG_DIR/config.json"
echo "Log file: $HOME/.local/share/wallpaper-rotation/rotator.log"
echo ""
echo "To manage the service, use:"
echo "  systemctl --user start wallpaper-rotator"
echo "  systemctl --user stop wallpaper-rotator"
echo "  systemctl --user status wallpaper-rotator"
echo "  systemctl --user restart wallpaper-rotator"
echo "  journalctl --user -u wallpaper-rotator -f"
