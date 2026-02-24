from core.maze_env import Maze
from core.levels import Levels

for level_name, level_grid in Levels.items():
    maze = Maze(level_grid)
    maze.print_level()
    level_complete = False
    while not level_complete:
        direction = input ("Enter your move (W/A/S/D): ").lower()
        maze.move_player(direction)
        if maze.trap_triggered:
            print("You've been reset to the start. Try again!")
            maze.reset_level(level_grid)
        level_complete = maze.goal_reached
        if not level_complete:
            maze.print_level()