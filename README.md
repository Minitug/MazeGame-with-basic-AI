# MazeGame with Basic AI
Python-based AI playground implementing a custom Genetic Algorithm to solve grid-based maze environments, visualised in real-time using Pygame.

This is my first project combining game development and AI.  
- **Game**: Maze game with traps and coins.  
- **AI**: Running Genetic Algorithm to semi randomly find better and better solutions.

## How to run
1. Clone the repo  
2. Run "py -3.11 -m runners.play_gui" to play manually
4. Run AI from root with "py -3.11 -m runners.ga_visualiser"

## Core
- Python 3.11
- Pygame (rendering + GUI)
- Custom Genetic Algorithm implementation

## Project Structure / Architecture
- Modular package structure (core, maze_ai, rendering, runners)
- CLI execution via python -m
- OOP design (Maze environment, Renderer, GA agent)

## Concepts / Techniques
- Genetic Algorithms (selection, crossover, mutation)
- Fitness function engineering
- Grid-based pathfinding
- Replay visualisation system
