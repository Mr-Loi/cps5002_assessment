class Thia:

    # setter
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.mobile = False
        self.carried = False

    # if in boss territory, sends warning
    def provide_warning(self, boss, env):
        if boss.in_territory(self.x, self.y, env):
            return True
        return False
