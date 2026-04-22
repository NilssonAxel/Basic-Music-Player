# Basic Music Player

A simple desktop music player built with Python, featuring a clean GUI and shuffle functionality.

## Features

- Play, pause, and skip MP3 files
- Shuffle mode with persistent playlist tracking
- Search bar to filter songs
- Auto-renames MP3 files containing non-ASCII characters
- Remembers shuffle state between sessions

## Requirements

- Python 3.x
- `pygame`
- `Pillow`
- `tkinter` (included with most Python installations)

Install dependencies:

```bash
pip install pygame Pillow
```

## Setup

1. Place your MP3 files in the `assets/mp3_folder/` directory.
2. Optionally, add a `logo.png` to the `assets/` directory for a custom window icon.

## Usage

```bash
python MusicPlayer.py
```

## Controls

| Button | Action |
|--------|--------|
| ⏮️ | Restart current song |
| ▶ / ⏸ | Play / Pause |
| ⏭️ | Next song |
| 🔀 | Toggle shuffle mode |

- **Double-click** a song in the playlist to play it directly.
- Use the **search bar** to filter songs by name.

## File Structure

```
Basic-Music-Player/
├── MusicPlayer.py
├── assets/
│   ├── mp3_folder/   # Place your MP3 files here
│   └── logo.png      # Optional window icon
├── cfg.txt           # Auto-generated config (shuffle state)
├── data.txt          # Auto-generated playback history
└── random.txt        # Auto-generated shuffle queue
```

## Author

Richard Gunnarsson
