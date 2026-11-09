# Wallpaper Rotation - Quick Start Guide

## Hurtig opsætning (5 minutter)

### 1. Klon eller download projektet
```bash
git clone https://github.com/Nexus8963/wallpaper-rotation.git
cd wallpaper-rotation
```

### 2. Installer
```bash
chmod +x install.sh
./install.sh
```

Scriptet vil:
- Kopiere programmet til `~/.local/bin/`
- Installere systemd service
- Oprette konfigurationsfil
- Spørge om du vil starte nu

### 3. Lad være! 🎨
Dit desktop vil nu få nyt billede hver 10. minut på hver monitor!

---

## Konfiguration

Rediger `~/.config/wallpaper-rotation/config.json`:

```json
{
  "wallpaper_dir": "/home/hitch/wallpapers",
  "rotation_interval": 600,
  "supported_formats": [".jpg", ".jpeg", ".png", ".bmp", ".gif"]
}
```

**Eksempler:**
- **Hver 5 minutter**: `"rotation_interval": 300`
- **Hver 30 minutter**: `"rotation_interval": 1800`
- **Anden mappe**: `"wallpaper_dir": "/path/to/your/images"`

### Genstarter efter ændring:
```bash
systemctl --user restart wallpaper-rotator
```

---

## Vigtige kommandoer

```bash
# Se status
systemctl --user status wallpaper-rotator

# Se logs i realtid
journalctl --user -u wallpaper-rotator -f

# Stop
systemctl --user stop wallpaper-rotator

# Start igen
systemctl --user start wallpaper-rotator

# Deaktiver auto-start
systemctl --user disable wallpaper-rotator
```

---

## Forudsætninger

✅ Du har mindst ét af disse installeret:
- `feh` (standard på de fleste Linux distros)
- `nitrogen`
- `gsettings`

Hvis du ikke har noget:
```bash
sudo apt install feh        # Ubuntu/Debian
sudo dnf install feh        # Fedora
sudo pacman -S feh          # Arch
```

---

## Troubleshooting

**Problemet**: Billeder skifter ikke
**Løsning**: 
1. Tjek at billeder er i `/home/hitch/wallpapers/`
2. Kør: `systemctl --user status wallpaper-rotator`
3. Tjek logs: `journalctl --user -u wallpaper-rotator -n 20`

**Problemet**: Kun én monitor får billeder
**Løsning**: Dette er normalt - hver monitor får et *forskelligt* tilfældigt billede!

**Problemet**: Service starter ikke efter login
**Løsning**: 
```bash
systemctl --user enable wallpaper-rotator
systemctl --user start wallpaper-rotator
```

---

## Aflæsning af logs

```bash
# Se alle logs
journalctl --user -u wallpaper-rotator

# Se de seneste 50 linjer
journalctl --user -u wallpaper-rotator -n 50

# Luk og afslut med 'q'
```

---

Mere hjælp? Se [README.md](README.md)
