"""Maze generator: builds a maze and finds its shortest path."""
import random
from collections import deque

# Cada pared es un bit: Norte=1, Este=2, Sur=4, Oeste=8
N, E, S, W = 1, 2, 4, 8
ALL_WALLS = N | E | S | W

# Cuanto me muevo en (x, y) al ir en cada direccion
MOVES = {N: (0, -1), E: (1, 0), S: (0, 1), W: (-1, 0)}
OPPOSITE = {N: S, E: W, S: N, W: E}
LETTER = {N: "N", E: "E", S: "S", W: "W"}

# El dibujo del "42" (1 = celda cerrada)
FIGURE = [
    [1, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 1, 1],
]


class MazeGenerator:
    """Generates a perfect maze and solves it."""
    def __init__(self, width: int, height: int, seed: int | None = None,
                 entry: tuple[int, int] = (0, 0),
                 exit_: tuple[int, int] | None = None,
                 perfect: bool = True) -> None:
        """Store the parameters and check entry and exit are valid."""
    
        self.width = width
        self.height = height
        self.perfect = perfect
        self.entry = entry
        if exit_ is None:
            exit_ = (width - 1, height - 1)
        self.exit = exit_
        self.seed = seed
        self.rng = random.Random(seed)
        self.grid: list[list[int]] = []
        self.pattern: list[list[int]] = []
        self._check_points()

    def _check_points(self) -> None:
        """Raise ValueError if entry or exit are wrong."""
        for name, (x, y) in (("ENTRY", self.entry), ("EXIT", self.exit)):
            if x < 0 or x >= self.width or y < 0 or y >= self.height:
                raise ValueError(f"{name} is outside the maze")
        if self.entry == self.exit:
            raise ValueError("ENTRY and EXIT must be different cells")

    def generate(self) -> None:
        """Build the whole maze."""
        self.grid = [[ALL_WALLS] * self.width for _ in range(self.height)]
        self.pattern = self._make_pattern()
        for x, y in (self.entry, self.exit):
            if self.pattern[y][x] == 1:
                raise ValueError("ENTRY or EXIT is inside the 42 pattern")
        self._carve()
        if not self.perfect:
            self._remove_dead_ends()
            self._add_second_route()

    def _make_pattern(self) -> list[list[int]]:
        """Pone el 42 en el centro. Si no cabe, avisa y lo deja vacio."""
        pattern = [[0] * self.width for _ in range(self.height)]
        # Con menos de 9x8 el 42 tapa casi todo y no queda sitio para
        # dos rutas independientes
        if self.width < 9 or self.height < 8:
            print("Warning: maze too small (needs at least 9x8), "
                  "the 42 pattern is left out.")
            return pattern
        start_x = (self.width - 1) // 2 - 3
        start_y = (self.height - 1) // 2 - 2
        for y in range(5):
            for x in range(7):
                pattern[start_y + y][start_x + x] = FIGURE[y][x]
        return pattern

    def _carve(self) -> None:
        """Abre pasillos con DFS (recorrido en profundidad con una pila)."""
        # Las celdas del 42 cuentan como ya visitadas para no tocarlas
        visited = [[cell == 1 for cell in row] for row in self.pattern]
        x, y = self.entry
        visited[y][x] = True
        stack = [(x, y)]

        while stack:
            x, y = stack[-1]
            neighbours = []
            for direction, (dx, dy) in MOVES.items():
                nx, ny = x + dx, y + dy
                inside = 0 <= nx < self.width and 0 <= ny < self.height
                if inside and not visited[ny][nx]:
                    neighbours.append((direction, nx, ny))

            if len(neighbours) == 0:
                stack.pop()  # callejon sin salida, vuelvo atras
                continue

            direction, nx, ny = self.rng.choice(neighbours)
            # Quito la pared en las dos celdas, si no quedaria incoherente
            self.grid[y][x] &= ~direction
            self.grid[ny][nx] &= ~OPPOSITE[direction]
            visited[ny][nx] = True
            stack.append((nx, ny))

    def solve(self) -> str:
        """Shortest path from entry to exit (BFS), for example 'ESSEN'."""
        # came_from[cell] = (celda anterior, letra del paso)
        came_from: dict[tuple[int, int], tuple[tuple[int, int], str]] = {}
        seen = {self.entry}
        queue = deque([self.entry])

        while queue:
            x, y = queue.popleft()
            if (x, y) == self.exit:
                break
            for direction, (dx, dy) in MOVES.items():
                nxt = (x + dx, y + dy)
                wall = self.grid[y][x] & direction
                if not wall and nxt not in seen:
                    seen.add(nxt)
                    came_from[nxt] = ((x, y), LETTER[direction])
                    queue.append(nxt)

        if self.exit not in seen:
            return ""

        # Voy de la salida hacia atras hasta la entrada y le doy la vuelta
        path = []
        current = self.exit
        while current != self.entry:
            current, letter = came_from[current]
            path.append(letter)
        path.reverse()
        return "".join(path)

    def _count_walls(self, x: int, y: int) -> int:
        """Cuantas paredes tiene la celda (0 a 4)."""
        return bin(self.grid[y][x]).count("1")

    def _inside(self, x: int, y: int) -> bool:
        """True si (x, y) esta dentro de la rejilla."""
        return 0 <= x < self.width and 0 <= y < self.height

    def _is_open_block(self, x0: int, y0: int) -> bool:
        """True si el bloque 3x3 con esquina (x0, y0) no tiene paredes."""

    def _makes_big_area(self, x: int, y: int) -> bool:
        """True si alrededor de la celda hay una zona abierta de 3x3."""

    def _has_two_routes(self) -> bool:
        """True si hay un segundo camino que no repite pasillos del corto."""

    def _add_second_route(self) -> None:
        """Abre paredes hasta que haya dos rutas independientes."""

    def _try_open(self, x: int, y: int, direction: int) -> bool:
        """Abre una pared si no forma un 3x3. Devuelve si lo consiguio."""

    def _remove_dead_ends(self) -> None:
        """Abre una pared en cada callejon sin salida (celda de 3 paredes)."""

    