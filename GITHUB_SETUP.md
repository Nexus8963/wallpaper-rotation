# Setup Guide: Push to GitHub

Dit projekt er klar til at blive pushet til GitHub! Her er step-by-step instruktionerne:

## Trin 1: Opret repository på GitHub

1. Gå til https://github.com/new
2. Udfyld følgende:
   - **Repository name**: `wallpaper-rotation`
   - **Description**: `Multi-Monitor Wallpaper Rotator - Automatically rotate different wallpapers on each connected monitor every 10 minutes`
   - **Public**: ✅ Vælg denne
   - **Initialize with**: Lad være tom (vi har allerede commits lokalt)
   - **License**: MIT (valgfrit - vi har allerede LICENSE fil)

3. Klik "Create repository"

## Trin 2: Push dit lokale repository til GitHub

Når du har oprettet repositoryet, vil GitHub vise dig instruktioner. Kør disse kommandoer:

```bash
cd /home/hitch/wallpaper-rotation

# Tilføj GitHub som remote
git remote add origin https://github.com/Nexus8963/wallpaper-rotation.git

# Skift branch navn hvis nødvendigt (GitHub bruger 'main' som standard)
git branch -M main

# Push til GitHub
git push -u origin main
```

## Trin 3: Verifikation

1. Besøg https://github.com/Nexus8963/wallpaper-rotation
2. Bekræft at alle filerne er der:
   - README.md
   - LICENSE (MIT)
   - wallpaper_rotator.py
   - install.sh
   - config.json.example
   - wallpaper-rotator.service
   - test_system.py
   - CONTRIBUTING.md

## Næste skridt

- ⭐ Giv projektet en stjerne (hvis du kan lide det!)
- 🔗 Del linket med venner
- 📝 Tilføj topics: `wallpaper` `linux` `cinnamon` `multi-monitor`
- 🐛 Åbn issues hvis du finder bugs
- 📦 Skab releases når der er nye features

Dit projekt er nu offentlig og andre kan klone det med:
```bash
git clone https://github.com/Nexus8963/wallpaper-rotation.git
```
