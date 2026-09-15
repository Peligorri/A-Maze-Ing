import random

def create_grid(x: int, y: int) -> None:
	if (x < 5 or y < 5):
		print("The variables x and y must be greater than 5.")
	else:
		for j in range(x):
			print("+---", end="")
		print("+")
		cell: int = 0
		for i in range(y - 1):
			print("|", end="")
			print(f"{cell:03}", end="")
			cell = cell + 1
			for j in range(x - 1):
				if True is random.choice([True, False]):
					print("|", end="")
					print(f"{cell:03}", end="")
					cell = cell + 1
				else:
					print(" ", end="")
					print(f"{cell:03}", end="")
					cell = cell + 1
			print("|")
			for j in range(x):
				print("+", end="")
				if True is random.choice([True, False]):
					print("---", end="")
				else:
					print("   ", end="")
			print("+")
		print("|", end="")
		print(f"{cell:03}", end="")
		cell = cell + 1
		for j in range(x - 1):
			if True is random.choice([True, False]):
				print("|", end="")
				print(f"{cell:03}", end="")
				cell = cell + 1
			else:
				print(" ", end="")
				print(f"{cell:03}", end="")
				cell = cell + 1
		print("|")
		for j in range(x):
			print("+---", end="")
		print("+")
def main() -> None:
	print("=== A-Maze-Ing WIP ===")
	x = input("Insert how many colums do you want for the grid: ")
	y = input("Insert how many rows do you want for the grid: ")
	create_grid(int(x), int(y))
if __name__ == "__main__":
	main()