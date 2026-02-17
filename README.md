# pokemon-space-invader

A simple, local Space-Invader-style game implemented in Python using Pygame and Pokemon-themed sprites.

This repository contains a small arcade game built for practice and learning. The game is data-driven via phase JSON files and includes enemies, bosses, power-ups, and visual/audio effects.

## Features

- Player spaceship with health and multiple fire modes
- Multiple alien types and bosses
- Power-ups and collectible "hong bao"
- Explosion/animation effects and sound
- Phase/level definitions in `phases/*.json`

## Requirements

- Python 3.8+ (or your system Python 3)
- pygame

Install pygame with pip if you don't have it:

```bash
pip install pygame
```

On some systems you may need `python3` and `pip3` instead of `python`/`pip`.

## Running the game

From the project root run:

```bash
python main.py
```

If that doesn't work, try:

```bash
python3 main.py
```

## Controls

Controls are implemented in the spaceship object. For the definitive control mapping, check `objects/Spaceship.py`.

## Project layout

- `main.py` — game entry point and main loop
- `objects/` — game object classes (Alien, Spaceship, Bullet, Boss, Powerup, etc.)
- `phases/` — JSON files describing level/phase configuration
- `img/` — images and sprite sheets used by the game
- `config/` — constants and sound manager
- `scripts/` — helper scripts used to spawn bosses/animations
- `collisions.py` — collision resolver

## TODO

- Add a `requirements.txt` for pinning dependencies
- Add a short controls section to the README (after confirming mapping)
- Add screenshots and/or a short recorded GIF to show gameplay
- Add packaging or a simple launcher script
- Add unit tests for non-graphical logic (collision resolver, spawn logic)

## References & Assets

Check the `img/Red Envelope Starter Pack/READ ME CC-BY-NC.txt` (and other image credit files) for asset credits and license details. Respect asset licenses when redistributing.

## License

This repository does not include a license file by default. Add a LICENSE file if you plan to publish or share the project publicly.

---

If you'd like, I can also:

- add a minimal `requirements.txt` with `pygame`,
- add a short controls subsection (I can inspect `objects/Spaceship.py` and document exact keys),
- or add one screenshot and update the README with it.

Feel free to tell me which of those you'd like next.