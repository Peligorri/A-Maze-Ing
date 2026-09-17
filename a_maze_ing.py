import random

class Cell:
	def __init__(self, up: bool, down: bool, right: bool, left: bool):
		self.up = up
		self.down = down
		self.right = right
		self.left = left

def create_cells(x: int, y: int) -> None:
	if (x < 5 or y < 5):
		print("The variables x and y must be greater than 5.")
	else:
		lst_cells = []
		for i in range(y):
			for j in range(x):
				lst_cells.append(Cell(random.choice([True, False]), random.choice([True, False]), random.choice([True, False]), random.choice([True, False])))
		for i, cell in enumerate(lst_cells):
			if i + 1 < len(lst_cells):
				compare_side_walls(cell, lst_cells[i + 1])
			if i + x < len(lst_cells):
				compare_updown_walls(cell, lst_cells[i + x])
		create_grid(lst_cells, x)

def compare_side_walls(cell_a: cell, cell_b: cell) -> None:
	cell_b.left = cell_a.right	

def compare_updown_walls(cell_a: cell, cell_b: cell) -> None:
	cell_b.up = cell_a.down			

def create_grid(lst_cells: list, x: int) -> None:
    for row_start in range(0, len(lst_cells), x):
        row = lst_cells[row_start:row_start + x]

        # Parte superior
        line = ""
        for cell in row:
            if cell.up:
                line += "████"
            else:
                line += "    "
        print(line)

        # Parte central
        line = ""
        for cell in row:
            if cell.left:
                line += "█"
            else:
                line += " "

            line += "  "

            if cell.right:
                line += "█"
            else:
                line += " "
        print(line)

        # Parte inferior
        line = ""
        for cell in row:
            if cell.down:
                line += "████"
            else:
                line += "    "
        print(line)



def main() -> None:
	print("=== A-Maze-Ing WIP ===")
	x = input("Insert how many colums do you want for the grid: ")
	y = input("Insert how many rows do you want for the grid: ")
	create_cells(int(x), int(y))
if __name__ == "__main__":
	main()