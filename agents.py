# superclass
class Agent:
    def __init__(self, x, y, health, stamina):
        self.x = x
        self.y = y
        self.health = health
        self.stamina = stamina
        self.alive = True

    def take_damage(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.alive = False

# yautja default class
class Predator(Agent):
    def __init__(self, x=5, y=5):
        super().__init__(x, y, 100, 100)
        self.honour = 0.0
        self.strength = 10

# dek class
class Dek(Predator):
    def __init__(self, x=5, y=5):
        super().__init__(x, y)
        self.trophies = 0
        self.carrying_thia = False

    # moving at cost of stamina
    def move(self, dx, dy, env, stamina_cost=None):
        cost = stamina_cost if stamina_cost is not None else (2 if self.carrying_thia else 1)
        if self.stamina < cost:
            return False
        self.x, self.y = env.wrap(self.x + dx, self.y + dy)
        self.stamina -= cost
        return True

    def gain_trophy(self):
        self.trophies += 1

# hostile yautja class
class ClanPredator(Predator):
    def __init__(self, x=1, y=1, name="ClanPred"):
        super().__init__(x, y)
        self.name = name
        self.strength = 12

    def move(self, dx, dy, env):
        if self.stamina <= 0:
            return False
        self.x, self.y = env.wrap(self.x + dx, self.y + dy)
        self.stamina -= 1
        return True

# boss class, stationary and holds territory
class Boss:
    def __init__(self, x=10, y=10):
        self.x = x
        self.y = y
        self.health = 500
        self.strength = 50
        self.territory = 3
        self.alive = True

    def in_territory(self, x, y, env):
        dx = min(abs(self.x - x), env.width - abs(self.x - x))
        dy = min(abs(self.y - y), env.height - abs(self.y - y))
        return dx <= self.territory and dy <= self.territory
