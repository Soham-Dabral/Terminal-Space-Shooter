# Terminal Space Shooter v2

A terminal-based arcade shooter game built in Python using Object-Oriented Programming principles.

## Features

- Player movement system
- Enemy spawning and movement
- Bullet firing system
- Collision detection system
- Score and lives tracking
- Bomb/AoE projectile mechanic
- Shield power-up system
- Dynamic terminal rendering
- Game loop and state management
- Cross-platform terminal clearing support

## Controls

| Key | Action |
|---|---|
| A | Move Left |
| D | Move Right |
| F | Fire Bullet |
| Q | Quit Game |

## Gameplay Mechanics

### Standard Bullets
Regular bullets destroy enemies on collision.

### Bomb Shot
Every fourth bullet activates a bomb shot which destroys enemies within an area-of-effect radius.

### Shield Power-Up
Shield pickups temporarily protect the player from incoming enemy collisions.

## Technical Concepts Used

- Object-Oriented Programming (OOP)
- Classes and Objects
- Game State Management
- Collision Detection
- Nested Loops
- List Filtering
- Randomized Entity Spawning
- 2D Grid Rendering
- Area-of-Effect (AoE) Systems

## Technologies

- Python 3
- Standard Library Modules:
  - random
  - os

## Future Improvements

- Multiple enemy types
- Boss fights
- Difficulty scaling
- Sound effects
- Projectile animations
- Persistent high scores
- Expanded power-up system

## Running the Game

```bash
python filename.py