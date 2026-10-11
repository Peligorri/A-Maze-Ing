"""Main program: reads the config, builds the maze and prints it."""
import sys
from mazegen import MazeGenerator, N, E, S, W, MOVES

WALL = "██"
EMPTY = "  "
PATTERN_42 = "⣿⣿"
TRAIL = "••"
WALL_COLORS = ("\033[96m", "\033[92m", "\033[93m", "\033[95m")
RESET = "\033[0m"

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
    maze = MazeGenerator(
        width, height, seed, entry, exit_, perfect == "true"
    )
    return maze, perfect == "true", config["OUTPUT_FILE"]

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


def draw(maze: MazeGenerator, show_path: bool,
         wall_color: str = "") -> str:
    """Dibuja el laberinto, opcionalmente coloreando las paredes."""
    grid = maze.grid
    trail = path_cells(maze) if show_path else set()
    wall = f"{wall_color}{WALL}{RESET}" if wall_color else WALL
    lines = []

    for y in range(maze.height):
        # Linea de arriba: paredes norte
        top = ""
        for x in range(maze.width):
            top += wall
            top += wall if grid[y][x] & N else EMPTY
        lines.append(top + wall)

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
        lines.append(middle + (wall if last & E else EMPTY))

    # Ultima linea: paredes sur de la fila de abajo
    bottom = ""
    for cell in grid[-1]:
        bottom += wall
        bottom += wall if cell & S else EMPTY
    lines.append(bottom + wall)
    return "\n".join(lines)


def make_maze(config: dict[str, str], regenerate: bool) -> MazeGenerator:
    """Genera el laberinto y lo guarda. Si regenerate, ignora SEED."""
    if regenerate:
        config = {k: v for k, v in config.items() if k != "SEED"}
    maze, _, output_file = build_maze(config)
    maze.generate()
    save(maze, output_file)
    return maze


def main() -> None:
    """Usage: python3 a_maze_ing.py config.txt"""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return
    try:
        config = read_config(sys.argv[1])
        maze = make_maze(config, False)
    except ValueError as error:
        print(f"Error: {error}")
        return

    show_path = True
    color = 0
    while True:
        print(draw(maze, show_path, WALL_COLORS[color]))
        print("1. Re-generate  2. Show/Hide path  "
              "3. Change colors  4. Quit")
        try:
            choice = input("Choice (1-4): ").strip()
        except EOFError:
            return
        if choice == "1":
            try:
                maze = make_maze(config, True)
            except ValueError as error:
                print(f"Error: {error}")
                return
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            color = (color + 1) % len(WALL_COLORS)
        elif choice == "4":
            return
        else:
            print("Invalid choice, use 1, 2, 3 or 4.")



if __name__ == "__main__":
    main()
