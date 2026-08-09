# Terminal Maze Game

A simple terminal-based maze game written in Python using the built-in `curses` module.

## How to play

```
python3 maze_game.py
```

- Move with the arrow keys or `W`/`A`/`S`/`D`.
- Reach the exit (`X`) before the timer runs out.
- Press `q` at any time to quit.

## Levels

The game contains 3 unique mazes of increasing size and difficulty, each with its own time limit:

1. **Level 1 - The Courtyard** — 30 seconds
2. **Level 2 - The Labyrinth** — 45 seconds
3. **Level 3 - The Gauntlet** — 60 seconds

Complete all three mazes before time runs out on each one to win the game. If the timer hits zero before you reach the exit, it's game over.

## Requirements

- Python 3
- A terminal that supports `curses` (standard on Linux/macOS; on Windows use WSL or install `windows-curses`)
