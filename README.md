# MM7 Clone - HoMM3 Style

3D RPG game in the style of Might & Magic VII with Heroes of Might & Magic III atmosphere.

## Features

- **3D World**: First-person perspective like MM7
- **Sprite-based Objects**: Trees, buildings, and other objects use billboards (2D sprites that always face the camera)
- **4-Hero Party**: Classic party composition with different classes:
  - Knight (Warrior class)
  - Cleric (Holy magic user)
  - Ranger (Archer/Scout)
  - Sorcerer (Arcane magic user)
- **HoMM3 Atmosphere**: Medieval fantasy setting with appropriate visual style

## Controls

- **WASD**: Move the party
- **Mouse**: Look around
- **1-4**: Select hero
- **Space**: Rest with selected hero (restores HP/MP)
- **Tab**: Toggle UI visibility

## Installation

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .

# Run the game
python game.py
```

## Important Note

**This game requires a graphical display to run.** If you're running on a headless server or in an environment without X11/display support, the game will generate all assets but won't be able to open a window.

To play the game, you need:
- A machine with a graphical desktop environment (Windows, macOS, or Linux with X11)
- Proper graphics drivers installed

## Requirements

- Python >= 3.11
- Ursina Engine
- Pillow

## Technical Details

Built with the Ursina game engine, featuring:
- Procedurally generated sprite textures using PIL
- Billboard rendering for sprite objects
- First-person camera controls
- Party management system
- Dynamic UI with hero stats

## Project Structure

```
/workspace/
├── game.py              # Main game code
├── pyproject.toml       # Project configuration
├── README.md           # This file
└── assets/
    ├── sprites/        # Generated sprite textures
    │   ├── knight.png
    │   ├── cleric.png
    │   ├── ranger.png
    │   ├── sorcerer.png
    │   ├── tree.png
    │   └── building.png
    └── textures/       # Generated ground textures
        └── ground.png
```
