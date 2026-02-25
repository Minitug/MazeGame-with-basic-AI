import sys
import time
from core.maze_env import Maze
from maze_ai.ga import ga_agent
from core.levels import Levels
from rendering.renderer import Renderer

import tkinter as tk
from tkinter import messagebox

replay_speed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
level_name=sys.argv[2] if len(sys.argv) > 2 else "Level1"
population_size = int(sys.argv[3]) if len(sys.argv) > 3 else 50
max_steps = int(sys.argv[4]) if len(sys.argv) > 4 else 5
max_steps_increment_interval=int(sys.argv[5]) if len(sys.argv) > 5 else 5

level_grid = Levels[level_name]

improvements = ga_agent.run_ga(
    population_size = population_size,
    max_steps = max_steps,
    max_steps_increment_interval = max_steps_increment_interval,
    level_name = level_name
    )  

maze = Maze(level_grid, verbose = False)
renderer = Renderer(maze)
renderer.draw()
messagebox.showinfo("Replays", "Replays will now start.")

for gen_data in improvements:
    champion = gen_data["champion"]
    other_agents = gen_data["other_agents"]
    generation = gen_data["generation"]

    print (f"generation {generation}")
    # print (f"Champion {champion}")
    # print (f"other_agents {other_agents}")

    maze = Maze(level_grid, verbose = False)
    renderer = Renderer(maze)
    renderer.draw()

    for move in champion:
        maze.move_player(move)
        renderer.draw()
        time.sleep(1 / replay_speed)

    last_champion = champion

