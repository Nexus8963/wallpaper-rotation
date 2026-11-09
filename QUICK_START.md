# Hurtig start

Programmet understøtter Cinnamon med X11. Installer først afhængighederne:

```bash
sudo apt install python3 python3-pil x11-xserver-utils libglib2.0-bin
./install.sh
```

Rediger `~/.config/wallpaper-rotation/config.json`, så `wallpaper_dir` peger på
din billedmappe. Linux skelner mellem store og små bogstaver i stier. Der skal
være mindst ét forskelligt billede pr. skærm. Standardintervallet er 600 sekunder.

```bash
python3 test_system.py
systemctl --user restart wallpaper-rotator
systemctl --user status wallpaper-rotator --no-pager
journalctl --user -u wallpaper-rotator -n 50 --no-pager
```

Programmet laver ét samlet baggrundsbillede med et forskelligt billede til hver
skærm. Det kræver udvidet skrivebord, ikke spejlede skærme. Slå Cinnamons eget
diasshow fra, så det ikke overskriver baggrunden. Se [README.md](README.md).
