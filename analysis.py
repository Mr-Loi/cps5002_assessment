#imports
import os
import matplotlib.pyplot as plt
from statistics import mean
from environment import Environment
from simulation import run_simulation
from config import GRID_WIDTH, GRID_HEIGHT, NUM_RUNS, NUM_SIMULATION_STEPS, NUM_WILDLIFE, NUM_OBSTACLES


def batch_run():
    results = []

    for _ in range(NUM_RUNS):
        env = Environment(GRID_WIDTH, GRID_HEIGHT)
        env.populate(num_wildlife=NUM_WILDLIFE, num_obstacles=NUM_OBSTACLES)
        results.append(run_simulation(env, max_steps=NUM_SIMULATION_STEPS))

    survival = [r["survival_time"] for r in results]
    honour = [r["honour"] for r in results]

    print("Average survival:", mean(survival))
    print("Average honour:", mean(honour))

    os.makedirs("results", exist_ok=True)

    plt.figure()
    plt.plot(survival)
    plt.title("Survival Time per Run")
    plt.xlabel("Run")
    plt.ylabel("Steps survived")
    plt.savefig("results/survival_plot.png")
    plt.close()

    plt.figure()
    plt.plot(honour)
    plt.title("Final Honour per Run")
    plt.xlabel("Run")
    plt.ylabel("Final honour")
    plt.savefig("results/honour_plot.png")
    plt.close()

