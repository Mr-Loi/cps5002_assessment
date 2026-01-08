import time

# imports
from environment import Environment
from simulation import Simulation, run_simulation
from visualisation import Visualiser
from analysis import batch_run

# runs sim
def run_visual_simulation():
    env = Environment(width=20, height=20)

    # populates grid with wildlife and obstacles
    env.populate(num_wildlife=30, num_obstacles=25)

    # max steps until sim ends
    sim = Simulation(env, max_steps=500)
    visualiser = Visualiser(env)

    step_delay = 0.1

    # loop
    while not sim.done:
        sim.step()

        # prints stats for current run
        print(f"Step {sim.step_count} | Honour: {sim.dek.honour:.2f} | Stamina: {sim.dek.stamina} | HP: {sim.dek.health}")

        visualiser.draw()
        time.sleep(step_delay)

    print("Visual simulation ended:", sim.end_reason)
    visualiser.close()

def main():
    MODE = 2  # 1 = visual, 2 = batch run

    if MODE == 1:
        run_visual_simulation()
    else:
        batch_run()



if __name__ == "__main__":
    main()

