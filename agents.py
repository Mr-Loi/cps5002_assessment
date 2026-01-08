import random

# superclass
class Agent:
    def __init__(self, x, y, health, stamina):
        self.x = x
        self.y = y
        self.health = health
        self.stamina = stamina
        self.alive = True

    # taking damage
    def take_damage(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.alive = False

# yautja
class Predator(Agent):
    def __init__(self, x, y):
        super().__init__(x, y, 100, 100)
        self.honour = 0
        self.strength = 10

# dek
class Dek(Predator):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.trophies = 0
        self.carrying_thia = False

    # allows dek to move at the cost of stamina
    def move(self, dx, dy, env):
        cost = 2 if self.carrying_thia else 1
        if self.stamina < cost:
            return
        self.x, self.y = env.wrap(self.x + dx, self.y + dy)
        self.stamina -= cost

# boss class
class Boss:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 500
        self.strength = 50
        self.territory = 3
        self.alive = True

    # checks if agent present in boss territory
    def in_territory(self, x, y, env):
        dx = min(abs(self.x - x), env.width - abs(self.x - x))
        dy = min(abs(self.y - y), env.height - abs(self.y - y))
        return dx <= self.territory and dy <= self.territory
