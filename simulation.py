import random

# imports
from agents import Dek, Boss, ClanPredator
from clan_code import YautjaCode, ClanJudge
from environment import (
    EMPTY, WILDLIFE, PREDATOR, SYNTHETIC, BOSS as BOSS_CELL,
    OBSTACLE, CLAN_PREDATOR
)
from synthetics import Thia

# manhattan adjacency test, checks neighboring cells so that detection for boss territory and hostile yautja behaves properly
def is_adjacent(ax, ay, bx, by, env):
    dx_raw = abs(ax - bx)
    dy_raw = abs(ay - by)
    dx = min(dx_raw, env.width - dx_raw)
    dy = min(dy_raw, env.height - dy_raw)
    return (dx + dy) == 1  # exactly 1 step away

# sim setter
class Simulation:
    def __init__(
        self,
        env,
        max_steps=500,
        dek_start=(5, 5),
        boss_start=(10, 10),
        thia_start=(2, 2),
        clan_starts=((1, 1), (18, 18)),   # two clan predators
        wildlife_worthy_prob=0.7,
    ):
        self.env = env
        self.max_steps = max_steps
        self.step_count = 0
        self.done = False
        self.end_reason = "Running"

        self.code = YautjaCode()
        self.judge = ClanJudge()

        self.dek = Dek(*dek_start)
        self.boss = Boss(*boss_start)
        self.thia = Thia(*thia_start)

        # hostile yautja
        self.father = ClanPredator(*clan_starts[0], name="Father")
        self.brother = ClanPredator(*clan_starts[1], name="Brother")
        self.clan_predators = [self.father, self.brother]

        self.wildlife_worthy_prob = wildlife_worthy_prob
        self.honour_history = []

        # place entities on the grid (move them if start cell occupied)
        self._place_entity_safe(self.dek.x, self.dek.y, PREDATOR, owner="dek")
        self._place_entity_safe(self.boss.x, self.boss.y, BOSS_CELL, owner="boss")
        self._place_entity_safe(self.thia.x, self.thia.y, SYNTHETIC, owner="thia")

        self._place_entity_safe(self.father.x, self.father.y, CLAN_PREDATOR, owner="father")
        self._place_entity_safe(self.brother.x, self.brother.y, CLAN_PREDATOR, owner="brother")

    # find empty unoccupied cells
    def _find_empty_cell(self):
        for _ in range(self.env.width * self.env.height * 3):
            x = random.randrange(self.env.width)
            y = random.randrange(self.env.height)
            if self.env.grid[y][x] == EMPTY:
                return x, y
        return 0, 0

    # places entities
    def _place_entity_safe(self, x, y, cell_type, owner=None):
        if self.env.grid[y][x] != EMPTY:
            x, y = self._find_empty_cell()
        self.env.grid[y][x] = cell_type

        if owner == "dek":
            self.dek.x, self.dek.y = x, y
        elif owner == "boss":
            self.boss.x, self.boss.y = x, y
        elif owner == "thia":
            self.thia.x, self.thia.y = x, y
        elif owner == "father":
            self.father.x, self.father.y = x, y
        elif owner == "brother":
            self.brother.x, self.brother.y = x, y

    def _clear_if_matches(self, x, y, expected):
        if self.env.grid[y][x] == expected:
            self.env.grid[y][x] = EMPTY

    def _move_grid_marker(self, old_x, old_y, new_x, new_y, marker):
        self._clear_if_matches(old_x, old_y, marker)
        self.env.grid[new_y][new_x] = marker

    def _attack(self, attacker, defender, damage):
        defender.take_damage(damage)
        # optional stamina cost
        attacker.stamina = max(0, attacker.stamina - 2)

    # calculates honour gain for prey
    def _wildlife_encounter(self, predator, x, y, is_dek=False):
        prey_worthy = (random.random() < self.wildlife_worthy_prob)
        if is_dek:
            predator.honour += self.code.evaluate_hunt(prey_worthy)
            if prey_worthy:
                predator.gain_trophy()
        # wildlife removed after encounter
        self.env.grid[y][x] = EMPTY

    def _clan_ai_move(self, cp):
        if not cp.alive:
            return

        if random.random() < 0.5:
            # pursue dek: choose dx/dy that reduces wrapped distance
            options = [(1,0), (-1,0), (0,1), (0,-1)]
            best = None
            best_dist = 10**9

            for dx, dy in options:
                nx, ny = self.env.wrap(cp.x + dx, cp.y + dy)

                # avoid stepping onto obstacles
                if self.env.grid[ny][nx] == OBSTACLE:
                    continue

                dx_raw = abs(nx - self.dek.x)
                dy_raw = abs(ny - self.dek.y)
                ddx = min(dx_raw, self.env.width - dx_raw)
                ddy = min(dy_raw, self.env.height - dy_raw)
                dist = ddx + ddy

                if dist < best_dist:
                    best_dist = dist
                    best = (dx, dy)

            if best is None:
                dx, dy = random.choice(options)
            else:
                dx, dy = best
        else:
            dx, dy = random.choice([(1,0), (-1,0), (0,1), (0,-1)])

        old_x, old_y = cp.x, cp.y
        moved = cp.move(dx, dy, self.env)
        if not moved:
            return

        nx, ny = cp.x, cp.y

        # obstacle -> revert
        if self.env.grid[ny][nx] == OBSTACLE:
            cp.x, cp.y = old_x, old_y
            return

        # wildlife encounter
        if self.env.grid[ny][nx] == WILDLIFE:
            self._wildlife_encounter(cp, nx, ny, is_dek=False)

        # update grid marker
        self._move_grid_marker(old_x, old_y, cp.x, cp.y, CLAN_PREDATOR)

    # boss territory effect
    def _boss_pressure(self, agent):
        if not agent.alive:
            return
        if self.boss.in_territory(agent.x, agent.y, self.env):
            agent.stamina = max(0, agent.stamina - 5)
            if random.random() < 0.3:
                agent.take_damage(self.boss.strength)

    def step(self):
        if self.done:
            return

        if not self.dek.alive:
            self.done = True
            self.end_reason = "Dek died"
            return

        if self.step_count >= self.max_steps:
            self.done = True
            self.end_reason = "Max steps reached"
            return

        # dex moves
        dx, dy = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
        old_x, old_y = self.dek.x, self.dek.y
        moved = self.dek.move(dx, dy, self.env)

        if moved:
            nx, ny = self.dek.x, self.dek.y

            # obstacle -> revert
            if self.env.grid[ny][nx] == OBSTACLE:
                self.dek.x, self.dek.y = old_x, old_y
                nx, ny = old_x, old_y
            else:
                # pick up thia
                if (not self.thia.carried) and (nx == self.thia.x and ny == self.thia.y):
                    self.thia.carried = True
                    self.dek.carrying_thia = True
                    self.env.grid[self.thia.y][self.thia.x] = EMPTY

                # keep thia with dek if carried
                if self.thia.carried:
                    self.thia.x, self.thia.y = self.dek.x, self.dek.y

                # wildlife encounter
                if self.env.grid[ny][nx] == WILDLIFE:
                    self._wildlife_encounter(self.dek, nx, ny, is_dek=True)

                # update grid marker for dek
                self._move_grid_marker(old_x, old_y, self.dek.x, self.dek.y, PREDATOR)

        # small honour drift so graphs aren't flat
        self.dek.honour += 0.02

        for cp in self.clan_predators:
            if cp.alive:
                self._clan_ai_move(cp)


        for cp in self.clan_predators:
            if cp.alive and self.dek.alive and is_adjacent(cp.x, cp.y, self.dek.x, self.dek.y, self.env):
                # mutual combat (simple)
                self._attack(cp, self.dek, damage=cp.strength)
                if self.dek.alive:
                    self._attack(self.dek, cp, damage=self.dek.strength)

                # death cleanup
                if not cp.alive:
                    self._clear_if_matches(cp.x, cp.y, CLAN_PREDATOR)
                    # honour for surviving clan combat (optional)
                    self.dek.honour += 5

        # boss pressure
        self._boss_pressure(self.dek)
        for cp in self.clan_predators:
            self._boss_pressure(cp)
            if not cp.alive:
                self._clear_if_matches(cp.x, cp.y, CLAN_PREDATOR)


        # clan judgement
        verdict = self.judge.judge(self.dek.honour)
        if verdict in ["Exile", "Execution"]:
            self.done = True
            self.end_reason = verdict

        # record
        self.honour_history.append(self.dek.honour)
        self.step_count += 1


def run_simulation(env, max_steps=500):
    sim = Simulation(env, max_steps=max_steps)
    while not sim.done:
        sim.step()

    # count clan predator survivals
    clan_alive = sum(1 for cp in sim.clan_predators if cp.alive)

    return {
        "survival_time": sim.step_count,
        "honour": sim.dek.honour,
        "honour_history": sim.honour_history,
        "alive": sim.dek.alive,
        "end_reason": sim.end_reason,
        "trophies": sim.dek.trophies,
        "thia_carried": sim.thia.carried,
        "clan_alive": clan_alive,
    }

