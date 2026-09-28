import random

N, E, S, W = 1, 2, 4, 8
ALL_WALLS = N | E | S | W

DELTA = {N: (0, -1), E: (1, 0), S: (0, 1), W: (-1, 0)}
OPPOSITE = {N: S, E: W, S: N, W: E}

MIN_SIZE = 10
BLOCK = "██"
SPACE = "  "
PATTERN = "⣿⣿"


def create_pattern(width: int, height: int) -> list[list[int]]:
    pattern = [[0] * width for _ in range(height)]

    pattern_start_x = ((width - 1) // 2) - 3
    pattern_start_y = ((height - 1) // 2) - 2

    figure = [
        [1, 0, 0, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1],
        [0, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 1, 1],
    ]

    for y in range(5):
        for x in range(7):
            pattern[pattern_start_y + y][pattern_start_x + x] = figure[y][x]

    return pattern

def create_grid(width: int, height: int) -> list[list[int]]:     
    grid = []

    for _ in range(height):
        row = []

        for _ in range(width):
            row.append(ALL_WALLS)

        grid.append(row)

    return grid


def carve(grid: list[list[int]], x: int, y: int, direction: int) -> None:
    dx, dy = DELTA[direction]
    nx, ny = x + dx, y + dy
    grid[y][x] &= ~direction
    grid[ny][nx] &= ~OPPOSITE[direction]


def in_bounds(grid: list[list[int]], x: int, y: int) -> bool:
    return 0 <= y < len(grid) and 0 <= x < len(grid[0])


def neighbours(grid: list[list[int]], x: int,
               y: int) -> list[tuple[int, int, int]]:
    result = []
    for direction, (dx, dy) in DELTA.items():
        nx, ny = x + dx, y + dy
        if in_bounds(grid, nx, ny):
            result.append((direction, nx, ny))
    return result


def generate(grid: list[list[int]], pattern: list[list[int]], start: tuple[int, int] = (0, 0)) -> None:
    visited = [[False] * len(grid[0]) for _ in range(len(grid))]
    for y in range(len(pattern)):
        for x in range(len(pattern[0])):
            if pattern[y][x] == 1:
                visited[y][x] = True
    x, y = start
    visited[y][x] = True
    stack = [(x, y)]

    while stack:
        x, y = stack[-1]
        candidates = [(d, nx, ny) for d, nx, ny in neighbours(grid, x, y)
                      if not visited[ny][nx]]
        if candidates:
            direction, nx, ny = random.choice(candidates)
            carve(grid, x, y, direction)
            visited[ny][nx] = True
            stack.append((nx, ny))
        else:
            stack.pop()


def render_ascii(grid: list[list[int]], pattern: list[list[int]]) -> str:
    height = len(grid)
    width = len(grid[0])
    lines = []

    for y in range(height):
        top = ""
        for x in range(width):
            top += BLOCK
            top += BLOCK if grid[y][x] & N else SPACE
        top += BLOCK
        lines.append(top)

        mid = ""
        for x in range(width):
            mid += BLOCK if grid[y][x] & W else SPACE
            mid += PATTERN if pattern[y][x] == 1 else SPACE
        mid += BLOCK if grid[y][width - 1] & E else SPACE
        lines.append(mid)

    floor = ""
    for x in range(width):
        floor += BLOCK
        floor += BLOCK if grid[height - 1][x] & S else SPACE
    floor += BLOCK
    lines.append(floor)

    return "\n".join(lines)


def to_hex(grid: list[list[int]]) -> str:
    return "\n".join("".join(f"{cell:x}" for cell in row) for row in grid)


def ask_size(prompt: str) -> int:
    while True:
        raw = input(prompt)
        try:
            value = int(raw)
        except ValueError:
            print(f"'{raw}' is not an integer.")
            continue
        if value < MIN_SIZE:
            print(f"The value must be {MIN_SIZE} or greater.")
            continue
        return value


def main() -> None:
    print("=== A-Maze-Ing WIP ===")
    width = ask_size("Insert how many columns do you want for the grid: ")
    height = ask_size("Insert how many rows do you want for the grid: ")

    grid = create_grid(width, height)
    pattern = create_pattern(width, height)
    #print(render_ascii(grid))
    generate(grid, pattern)
    print(render_ascii(grid, pattern))


if __name__ == "__main__":
    main()
    
