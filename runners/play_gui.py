from core.maze_env import Maze
from core.levels import Levels
from rendering.renderer import Renderer

import tkinter as tk
from tkinter import messagebox

quit = False

for level_name, level_grid in Levels.items():
    maze = Maze(level_grid, verbose = False)
    renderer = Renderer(maze)
    renderer.draw()
    level_complete = False
    if quit:
        break
    while  not level_complete and not quit:
        direction = renderer.get_input()
        if direction == "QUIT":
            quit = True
        elif direction:
            maze.move_player(direction)
        
        if maze.trap_triggered:
            maze.reset_level(level_grid)

        renderer.draw()

        if maze.goal_reached:
            messagebox.showinfo(f"Congratulations!", f"You've reached the goal in {maze.total_moves} moves!")
            level_complete = True