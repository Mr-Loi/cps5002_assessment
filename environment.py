import random

# enumeration
EMPTY, WILDLIFE, PREDATOR, SYNTHETIC, BOSS, OBSTACLE = range(6)

# sets grid environment
class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[EMPTY for _ in range(width)] for _ in range(height)]

    # wrapping around edges
    def wrap(self, x, y):
        return x % self.width, y % self.height

    # randomly places entities
    def place_random(self, entity, count):
        placed = 0
        while placed < count:
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            if self.grid[y][x] == EMPTY:
                self.grid[y][x] = entity
                placed += 1
