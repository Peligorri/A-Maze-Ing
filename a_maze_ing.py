

N, E, S, W = 1, 2, 4, 8
ALL_WALLS = N | E | S | W

DELTA = {N: (0, -1), E: (1, 0), S: (0, 1), W: (-1, 0)}
OPPOSITE = {N: S, E: W, S: N, W: E}

MIN_SIZE = 5
BLOCK = "██"
SPACE = "  "


def create_grid(width: int, height: int) -> list[list[int]]:
    return [[ALL_WALLS for _ in range(width)] for _ in range(height)]


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


def generate(grid: list[list[int]], start: tuple[int, int] = (0, 0)) -> None:
    # TODO: backtracker con pila
    raise NotImplementedError


def render_ascii(grid: list[list[int]]) -> str:
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
            mid += SPACE
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
    print(render_ascii(grid))


if __name__ == "__main__":
    main()
    