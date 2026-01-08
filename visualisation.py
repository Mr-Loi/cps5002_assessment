import tkinter as tk

# imports
from environment import EMPTY, WILDLIFE, PREDATOR, SYNTHETIC, BOSS, OBSTACLE, CLAN_PREDATOR

CELL_SIZE = 25  # pixels

# gui
class Visualiser:
    def __init__(self, environment):
        self.env = environment

        # tkinter init
        self.root = tk.Tk()
        self.root.title("sim")

        width_px = environment.width * CELL_SIZE
        height_px = environment.height * CELL_SIZE

        self.canvas = tk.Canvas(
            self.root,
            width=width_px,
            height=height_px,
            bg="black"
        )
        self.canvas.pack()

    def draw(self):
        # redraw grid
        self.canvas.delete("all")

        for y in range(self.env.height):
            for x in range(self.env.width):
                cell = self.env.grid[y][x]
                color = self.get_color(cell)

                x1 = x * CELL_SIZE
                y1 = y * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline="black"
                )

        self.root.update()

    def get_color(self, cell_type):
        # entity colours
        if cell_type == EMPTY:
            return "#d2b48c"  # desert sand
        elif cell_type == PREDATOR:
            return "green" # yautja
        elif cell_type == SYNTHETIC:
            return "blue"
        elif cell_type == WILDLIFE:
            return "orange"
        elif cell_type == BOSS:
            return "red"
        elif cell_type == OBSTACLE:
            return "gray"
        elif cell_type == CLAN_PREDATOR:
            return "dark green"
        return "black"

    def close(self):
        self.root.destroy()
