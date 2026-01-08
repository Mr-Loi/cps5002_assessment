# evaluates hunts and awards/punishes
class YautjaCode:
    def evaluate_hunt(self, prey_worthy):
        if prey_worthy:
            return +5
        return -20

    def evaluate_retreat(self):
        return -5

# honour system
class ClanJudge:
    def judge(self, honour):
        if honour < -30:
            return "Execution"
        if honour < -10:
            return "Exile"
        return "Accepted"
