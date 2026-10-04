"""Main program: reads the config, builds the maze and prints it."""
import random
import sys

from mazegen import MazeGenerator, N, E, S, W, MOVES

WALL = "██"
EMPTY = "  "
PATTERN_42 = "⣿⣿"
TRAIL = "••"


def read_config(path: str) -> dict[str, str]:
    """Lee las lineas CLAVE=valor, saltando vacias y comentarios (#)."""
    config: dict[str, str] = {}
    try:
        with open(path, encoding="utf-8") as file:
            for number, line in enumerate(file, start=1):
                line = line.strip()
                if line == "" or line.startswith("#"):
                    continue
                if "=" not in line:
                    raise ValueError(f"line {number}: missing '='")
                key, value = line.split("=", 1)
                config[key.strip().upper()] = value.strip()
    except OSError as error:
        raise ValueError(f"cannot read '{path}': {error}") from error
    return config


def read_point(text: str, name: str) -> tuple[int, int]:
    """Convierte 'x,y' en dos numeros."""
    parts = text.split(",")
    if len(parts) != 2:
        raise ValueError(f"{name} must be x,y")
    try:
        return int(parts[0]), int(parts[1])
    except ValueError:
        raise ValueError(f"{name} must be x,y with numbers") from None


def build_maze(config: dict[str, str]) -> tuple[MazeGenerator, bool, str]:
    """Check the config and return (maze, is_perfect, output file)."""
    required = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
    for key in required:
        if key not in config:
            raise ValueError(f"missing key {key}")

    try:
        width = int(config["WIDTH"])
        height = int(config["HEIGHT"])
        seed = int(config["SEED"]) if "SEED" in config else None
    except ValueError:
        raise ValueError("WIDTH, HEIGHT and SEED must be numbers") from None
    if width < 2 or height < 2:
        raise ValueError("WIDTH and HEIGHT must be at least 2")

    perfect = config["PERFECT"].lower()
    if perfect != "true" and perfect != "false":
        raise ValueError("PERFECT must be True or False")

    entry = read_point(config["ENTRY"], "ENTRY")
    exit_ = read_point(config["EXIT"], "EXIT")
    maze = MazeGenerator(width, height, seed, entry, exit_)
    return maze, perfect == "true", config["OUTPUT_FILE"]


def open_walls(maze: MazeGenerator) -> None:
    """PROVISIONAL (modo no perfecto): quita paredes al azar para hacer
    bucles. Todavia no cumple todo lo que pide el subject."""
    grid = maze.grid
    for y in range(maze.height):
        for x in range(maze.width):
            if maze.pattern[y][x] == 1:
                continue
            if maze.rng.random() > 0.15:
                continue
            if maze.rng.random() < 0.5:
                direction, opposite = S, N
            else:
                direction, opposite = E, W
            nx = x + MOVES[direction][0]
            ny = y + MOVES[direction][1]
            if nx < maze.width and ny < maze.height:
                if maze.pattern[ny][nx] == 0:
                    grid[y][x] &= ~direction
                    grid[ny][nx] &= ~opposite


def to_hex(grid: list[list[int]]) -> str:
    """Una cifra hexadecimal por celda, una fila por linea."""
    rows = []
    for row in grid:
        rows.append("".join(f"{cell:X}" for cell in row))
    return "\n".join(rows)


def save(maze: MazeGenerator, path: str) -> None:
    """Escribe el archivo de salida que pide el subject."""
    text = to_hex(maze.grid) + "\n\n"
    text += f"{maze.entry[0]},{maze.entry[1]}\n"
    text += f"{maze.exit[0]},{maze.exit[1]}\n"
    text += maze.solve() + "\n"
    try:
        with open(path, "w", encoding="utf-8") as file:
            file.write(text)
    except OSError as error:
        raise ValueError(f"cannot write '{path}': {error}") from error


def path_cells(maze: MazeGenerator) -> set[tuple[int, int]]:
    """Todas las celdas por las que pasa la solucion."""
    directions = {"N": N, "E": E, "S": S, "W": W}
    x, y = maze.entry
    cells = {(x, y)}
    for letter in maze.solve():
        dx, dy = MOVES[directions[letter]]
        x, y = x + dx, y + dy
        cells.add((x, y))
    return cells


def draw(maze: MazeGenerator, show_path: bool) -> str:
    """Dibuja el laberinto con texto."""
    grid = maze.grid
    trail = path_cells(maze) if show_path else set()
    lines = []

    for y in range(maze.height):
        # Linea de arriba: paredes norte
        top = ""
        for x in range(maze.width):
            top += WALL
            top += WALL if grid[y][x] & N else EMPTY
        lines.append(top + WALL)

        # Linea del medio: pared oeste + contenido de la celda
        middle = ""
        for x in range(maze.width):
            middle += WALL if grid[y][x] & W else EMPTY
            if (x, y) == maze.entry:
                middle += "EN"
            elif (x, y) == maze.exit:
                middle += "EX"
            elif maze.pattern[y][x] == 1:
                middle += PATTERN_42
            elif (x, y) in trail:
                middle += TRAIL
            else:
                middle += EMPTY
        last = grid[y][maze.width - 1]
        lines.append(middle + (WALL if last & E else EMPTY))

    # Ultima linea: paredes sur de la fila de abajo
    bottom = ""
    for cell in grid[-1]:
        bottom += WALL
        bottom += WALL if cell & S else EMPTY
    lines.append(bottom + WALL)
    return "\n".join(lines)


def main() -> None:
    """Usage: python3 a_maze_ing.py config.txt"""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return
    try:
        config = read_config(sys.argv[1])
        maze, perfect, output_file = build_maze(config)
        if maze.seed is None:
            maze.rng = random.Random()
        maze.generate()
        if not perfect:
            open_walls(maze)
        save(maze, output_file)
    except ValueError as error:
        print(f"Error: {error}")
        return
    print(draw(maze, show_path=True))


if __name__ == "__main__":
    main()
