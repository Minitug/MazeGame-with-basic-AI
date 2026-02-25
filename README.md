# MazeGame with Basic AI
Python-based AI playground implementing a custom Genetic Algorithm to solve grid-based maze environments, visualised in real-time using Pygame.

This is my first project combining game development and AI.  

## Features
- **Game**: Maze game with traps and coins.  
- **AI**: Running Genetic Algorithm to semi randomly find better and better solutions.
- **Visualisation** – Replay system showing generational improvements  

## How to run
1. Clone the repo  
2. Run "py -3.11 -m runners.play_gui" in CMD/PowerShell/bash from root to play manually
4. Run AI in CMD/PowerShell/bash from root with "py -3.11 -m runners.ga_visualiser"

## Tech Stack
- Python 3.11
- Pygame (rendering + GUI)
- Custom Genetic Algorithm implementation

## Architecture
- Modular package structure (core, maze_ai, rendering, runners)
- CLI execution via python -m
- OOP design (Maze environment, Renderer, GA agent)

## Concepts & Techniques
- Genetic Algorithms (selection, crossover, mutation)
- Fitness function engineering
- Grid-based pathfinding mechanics
- Evolution replay visualisation
