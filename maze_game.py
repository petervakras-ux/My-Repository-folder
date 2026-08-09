#!/usr/bin/env python3
"""Terminal maze game with 3 unique mazes and a countdown timer per level."""

import curses
import time

WALL = "#"
FLOOR = "."
START = "S"
EXIT = "X"
PLAYER = "@"

MAZES = [
    {
        "name": "Level 1 - The Courtyard",
        "time_limit": 30,
        "grid": [
            "###################",
            "#S......#.#.......#",
            "#######.#.#.#####.#",
            "#.....#.#.#.#...#.#",
            "#.#####.#.#.#.#.#.#",
            "#.#.....#...#.#...#",
            "#.#.#####.###.#####",
            "#...#...#.#.#.....#",
            "#.#####.#.#.#####.#",
            "#.....#.........#.#",
            "#####.###########.#",
            "#...#...#.......#.#",
            "#.#####.#.#####.#.#",
            "#.........#......X#",
            "###################",
        ],
    },
    {
        "name": "Level 2 - The Labyrinth",
        "time_limit": 45,
        "grid": [
            "#######################",
            "#S#...........#.#.....#",
            "#.###.#######.#.#.#.#.#",
            "#.....#...#.#.#.#.#.#.#",
            "#######.#.#.#.#.#.#.###",
            "#.....#.#...#.#...#...#",
            "#.#.#.#.###.#.#.#####.#",
            "#.#.#.#.#...#.#.#.....#",
            "#.#.#.#.#.###.###.###.#",
            "#.#.#.#.#...#.....#.#.#",
            "#.#.#.#.###########.#.#",
            "#.#.#.#.....#.......#.#",
            "#.#.#.#####.#.#####.#.#",
            "#.#.#.......#...#.#...#",
            "#.#.###########.#.#####",
            "#.#.....#.......#.....#",
            "#.#####.#.#########.#.#",
            "#.....#.............#X#",
            "#######################",
        ],
    },
    {
        "name": "Level 3 - The Gauntlet",
        "time_limit": 60,
        "grid": [
            "###########################",
            "#S....#.............#.....#",
            "#####.#.#####.#####.#.#####",
            "#...#.#...#.#.#...#.#.....#",
            "#.###.###.#.#.#.###.#.###.#",
            "#...#...#...#.#.....#.#.#.#",
            "#.#.###.#####.#.#####.#.#.#",
            "#.#...#.....#.#.#...#.#.#.#",
            "#.###.#####.#.#.#.###.#.#.#",
            "#.#...#.....#.#.#.......#.#",
            "#.#.###.#####.#.#########.#",
            "#.#...#.#.....#.........#.#",
            "#####.#.#.#############.#.#",
            "#.....#.#.......#.......#.#",
            "#.###.#.#######.###.#####.#",
            "#...#.#.......#...#.#.....#",
            "#.#.#########.###.#.#####.#",
            "#.#.....#.....#...#.....#.#",
            "#.###.###.#####.#######.#.#",
            "#...#...........#........X#",
            "###########################",
        ],
    },
]


def find_char(grid, char):
    for y, row in enumerate(grid):
        x = row.find(char)
        if x != -1:
            return x, y
    raise ValueError(f"Character {char!r} not found in maze")


def draw(stdscr, grid, player_pos, level_name, time_left, level_num, total_levels):
    stdscr.erase()
    stdscr.addstr(0, 0, f"{level_name}  (Maze {level_num}/{total_levels})")
    stdscr.addstr(1, 0, f"Time left: {int(time_left):>3}s   Move: arrow keys / WASD   Quit: q")

    px, py = player_pos
    for y, row in enumerate(grid):
        line = row if (0, y) != (px, py) else row[:px] + PLAYER + row[px + 1:]
        stdscr.addstr(3 + y, 0, line)

    stdscr.refresh()


def play_level(stdscr, level, level_num, total_levels):
    grid = [list(row) for row in level["grid"]]
    grid = ["".join(row) for row in grid]

    px, py = find_char(grid, START)
    ex, ey = find_char(grid, EXIT)
    time_limit = level["time_limit"]

    start_time = time.time()
    stdscr.nodelay(True)
    stdscr.timeout(100)

    while True:
        elapsed = time.time() - start_time
        time_left = time_limit - elapsed

        if time_left <= 0:
            return False

        if (px, py) == (ex, ey):
            return True

        draw(stdscr, grid, (px, py), level["name"], time_left, level_num, total_levels)

        key = stdscr.getch()
        nx, ny = px, py

        if key in (curses.KEY_UP, ord("w"), ord("W")):
            ny -= 1
        elif key in (curses.KEY_DOWN, ord("s"), ord("S")):
            ny += 1
        elif key in (curses.KEY_LEFT, ord("a"), ord("A")):
            nx -= 1
        elif key in (curses.KEY_RIGHT, ord("d"), ord("D")):
            nx += 1
        elif key in (ord("q"), ord("Q")):
            raise SystemExit(0)

        if 0 <= ny < len(grid) and 0 <= nx < len(grid[ny]) and grid[ny][nx] != WALL:
            px, py = nx, ny


def show_message(stdscr, lines, wait_key=True):
    stdscr.nodelay(False)
    stdscr.erase()
    for i, line in enumerate(lines):
        stdscr.addstr(i, 0, line)
    stdscr.refresh()
    if wait_key:
        stdscr.getch()


def main(stdscr):
    curses.curs_set(0)
    total_levels = len(MAZES)

    for i, level in enumerate(MAZES, start=1):
        show_message(
            stdscr,
            [
                f"{level['name']}",
                f"You have {level['time_limit']} seconds to reach the exit (X).",
                "",
                "Press any key to start...",
            ],
        )

        won = play_level(stdscr, level, i, total_levels)

        if not won:
            show_message(
                stdscr,
                [
                    "Time's up! You got trapped in the maze.",
                    "",
                    "Press any key to exit...",
                ],
            )
            return

    show_message(
        stdscr,
        [
            "Congratulations! You escaped all 3 mazes!",
            "",
            "Press any key to exit...",
        ],
    )


if __name__ == "__main__":
    curses.wrapper(main)
