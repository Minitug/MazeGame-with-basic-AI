import sys
import time
import random
from copy import deepcopy
from core.maze_env import Maze
from core.levels import Levels

def crossover(parent1, parent2):
    if len(parent1) > 1:
        cut = random.randint(1, len(parent1)-1)
    else:
        cut = 1
    return parent1[:cut] + parent2[cut:]

def mutate(sequence, rate=0.15):
    for i in range(len(sequence)):
        if random.random() < rate:
            sequence[i] = random.choice(['w','a','s','d'])

def replay_sequence(sequence, level_grid):
    maze = Maze(level_grid, verbose=True)

    print("\n--- Replaying sequence ---")
    print("Sequence:", sequence)

    for i, move in enumerate(sequence, 1):
        maze.move_player(move)
        maze.print_level()

        if maze.trap_triggered:
            print("💥 Trap triggered!")
            break

        if maze.goal_reached:
            print("🏁 Goal reached!")
            break

POPULATION = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() and int(sys.argv[1]) > 0 else 50
MAX_GENERATIONS = 200000
# MAX_FITNESS = [92, 88, 96, 120]
MAX_FITNESS = [9984, 9976, 10122, 10560, 11094]
MAX_STEPS = 100

start_time = time.time()
last_champion_time = start_time
max_steps = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() and int(sys.argv[2]) > 0 else 5
max_steps_increment_interval = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3].isdigit() and int(sys.argv[3]) > 0 else 5

population = [[random.choice(['w','a','s','d']) for _ in range(max_steps)] for _ in range(POPULATION)]
generation = 1
last_generation_print = 0
last_best_fitness = float('-inf')
agent_found_goal = False
current_champions_generation = 0
distance_to_coins = []
generational_improvements = []

level_name = "Level5"
level_grid = Levels[level_name]
last_char = level_name[-1]
if last_char.isdigit():
    level_num = int(last_char)
    max_fitness = MAX_FITNESS[(level_num - 1)]
print("Starting GA Agent...")

while generation <= MAX_GENERATIONS:

    results = []

    for sequence in population:
        maze = Maze(level_grid, verbose=False)
        starting_coins = maze.coins_missing
        steps_taken = 0
        invalid_moves = 0
        used_sequence = sequence
        distance_to_coins = []

        for step, move in enumerate(sequence):
            maze.move_player(move)
            steps_taken += 1
            invalid_moves += 0 if maze.is_move_valid else 1

            if maze.goal_reached: 
                used_sequence = sequence[:step+1]
                break
            if maze.trap_triggered:
                break

        if maze.coins_missing > 0:
            for coin in maze.coin_positions:
                distance = abs(maze.player_row - coin[0]) + abs(maze.player_col - coin[1])
                distance_to_coins.append(distance)

            min_distance_to_coin = min(distance_to_coins) if distance_to_coins else 0   

        fitness = (starting_coins - maze.coins_missing) * 150
        fitness -= invalid_moves
        if maze.coins_missing > 0:
            fitness -= min_distance_to_coin 

        if maze.trap_triggered:
            fitness -= 150
        elif maze.goal_reached:
            fitness += 10000 - steps_taken  
            fitness -= invalid_moves * 9  
            agent_found_goal = True
        elif maze.coins_missing == 0:
            distance = abs(maze.player_row - maze.goal_row) + abs(maze.player_col - maze.goal_col)
            fitness -= distance

        results.append((used_sequence, fitness, steps_taken, invalid_moves))

    results.sort(key=lambda x: x[1], reverse=True)

    champion_sequence, champion_fitness, champion_steps, champion_invalid = results[0]

    if champion_fitness > last_best_fitness:
        last_best_fitness = champion_fitness

        generational_improvements.append({
            "generation": generation,
            "champion": champion_sequence,
            "other_agents": [seq for seq, *_ in results[1:]]
        })

        print(f"Generation {generation}: New champion: Fitness {champion_fitness}, Steps {champion_steps}, Invalid {champion_invalid}, Sequence: {champion_sequence}")
        last_champion_time = time.time()
        print(f"Time since start: {int(time.time() - start_time)} seconds")
        print(f"Generations since last champion: {generation - last_generation_print}")
        last_generation_print = generation
        current_champions_generation = generation
        if agent_found_goal:
            max_steps = champion_steps - 1
    elif champion_fitness < last_best_fitness:
        print(f"Warning: Champion fitness decreased from {last_best_fitness} to {champion_fitness}!")
        last_best_fitness = champion_fitness
        print(f"Last champion: {last_champion}")
        for seq, fit, steps, inv in results:
            print(f"Seq: {seq}, Fit: {fit}, Steps: {steps}, Invalid: {inv}")


    if time.time() - last_champion_time > 10:
        last_champion_time = time.time()
        print (f"No improvement for 10 seconds, working on generation {generation}...")
        print(f"Generations since last check in: {generation - last_generation_print}")
        last_generation_print = generation
        print(f"Time since last start: {int(time.time() - start_time)} seconds")

    elite_count = max(2, POPULATION // 5)
    elites = [seq for seq, fit, s, inv in results[:elite_count]]

    new_population = [deepcopy(champion_sequence)]  
    while len(new_population) < POPULATION:
        parent1 = random.choice(elites)
        parent2 = random.choice(elites)
        child = crossover(parent1, parent2)
        mutate(child, rate=0.15 * (2 + generation / MAX_GENERATIONS))
        new_population.append(child)

    population = new_population

    if generation % max_steps_increment_interval == 0 and not agent_found_goal:
        if max_steps < MAX_STEPS:
            max_steps += 2
        for seq in population:
            if seq != champion_sequence:
                while len(seq) < max_steps:
                    seq.append(random.choice(['w','a','s','d']))
                if len(seq) > max_steps:
                    del seq[max_steps:]

    generation += 1
    
    if champion_fitness >= max_fitness:
        print("Good sequence found!")
        break

    last_champion = deepcopy(results[0])

print("Best sequence:", champion_sequence)
print("Best fitness:", champion_fitness)
print("Found in generation:", current_champions_generation)

replay_sequence(champion_sequence, level_grid)