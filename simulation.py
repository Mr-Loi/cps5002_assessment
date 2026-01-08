import random
from clan_code import YautjaCode, ClanJudge

# running sim
def run_simulation(env, dek, boss, max_steps=500):
    code = YautjaCode()
    judge = ClanJudge()

    # holds honour gain/deduction
    honour_history = []

    # breaks loop if dek dies
    for step in range(max_steps):
        if not dek.alive:
            break

        dx, dy = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
        dek.move(dx, dy, env)

        # debuffs dek if in boss territory
        if boss.in_territory(dek.x, dek.y, env):
            dek.stamina -= 5
            if random.random() < 0.3:
                dek.take_damage(boss.strength)

        honour_history.append(dek.honour)

        # breaks loop if dek has too low honour (-10 <= x)
        verdict = judge.judge(dek.honour)
        if verdict in ["Exile", "Execution"]:
            break

    # sim statistics
    return {
        "survival_time": step,
        "honour": dek.honour,
        "honour_history": honour_history,
        "alive": dek.alive
    }
