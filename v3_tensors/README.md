# Terminal Space Shooter v0.3 (PyTorch)

A simple terminal-based arcade shooter built in Python using **PyTorch tensors** to manage game objects. The player moves across the bottom of the screen, shoots descending enemies, collects shields, and survives as long as possible.

Although PyTorch is typically used for machine learning, this project demonstrates how tensor operations can efficiently manage game state and collision detection.

---

## Features

- Terminal-based gameplay
- Player movement
- Bullet firing
- Random enemy spawning
- Shield power-ups
- Collision detection using PyTorch tensor operations
- Score and lives system
- Object-oriented design with layered game state classes

---

## Gameplay

### Objective

Destroy enemies before they reach the player's row.

Each enemy destroyed awards **10 points**.

The game ends when the player loses all lives or quits.

---

## Controls

| Key | Action |
|------|--------|
| `A` | Move left |
| `D` | Move right |
| `F` | Fire a bullet |
| `Q` | Quit the game |

---

## Symbols

| Symbol | Meaning |
|---------|---------|
| `A` | Player |
| `@` | Shielded player |
| `V` | Enemy |
| `|` | Bullet |
| `O` | Shield power-up |
| `.` | Empty space |

---

## Requirements

- Python 3.10+
- PyTorch

Install PyTorch:

```bash
pip install torch
```

---

## Running the Game

```bash
python game.py
```

---

## Game Mechanics

### Player

- Starts with **3 lives**
- Can move horizontally across the bottom row
- Fires bullets upward

### Enemies

Enemies:

- Spawn randomly at the top of the board
- Move downward one tile per turn
- Damage the player when:
  - they collide with the player, or
  - they reach the player's row

### Shields

Shields:

- Spawn randomly
- Fall toward the player
- Grant one-time protection against the next hit

### Bullets

Bullets:

- Travel upward
- Destroy enemies on contact
- Disappear after a collision

---

## Scoring

- +10 points per enemy destroyed

There is currently no score multiplier or level progression.

---

## Project Structure

The game is organized using inheritance, where each class adds a specific layer of functionality.

```
GameState1
│
├── Stores game data
│
GameState2
│
├── Input handling
├── Bullet firing
├── Enemy spawning
└── Shield spawning
│
GameState3
│
├── Bullet movement
├── Enemy movement
└── Shield movement
│
GameState4
│
└── Bullet–enemy collision detection
│
GameState5
│
├── Player–enemy collisions
└── Player–shield collisions
│
GameState6
│
└── Rendering
│
GameState
│
├── Main game loop
└── Turn management
```

---

## Why PyTorch?

Instead of storing objects as Python lists, enemies, bullets, and shields are stored as **PyTorch tensors**.

This enables:

- vectorized movement
- efficient collision detection
- concise tensor-based logic
- experimentation with tensor programming outside machine learning

For example, bullet–enemy collisions are computed by comparing every bullet against every enemy simultaneously using tensor broadcasting.

---

## Future Improvements

Potential additions include:

- Multiple enemy types
- Enemy shooting
- Increasing difficulty over time
- Boss battles
- High-score saving
- Sound effects
- Colored terminal graphics
- Animation with timed updates
- Better game architecture (composition instead of deep inheritance)

---

## Example

```
==============================
Turn: 12    Score: 40    Lives: 2
==============================
. . . . . V . . . . .
. . . . . . . . . . .
. . . . | . . . . . .
. . . . . . . . . . .
. . O . . . . . . . .
. . . . . . . . . . .
. . . . . . . . . . .
. . . . . . . . . . .
. . . . . . . . . . .
. . . . . . . . . . .
. . . . A . . . . . .
==============================
Bullets: 1
Enemies: 1
Shield Activation Status: False
```

---
