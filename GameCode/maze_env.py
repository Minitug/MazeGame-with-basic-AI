class Maze:
    def __init__(self, grid):
        self.grid = [row.copy() for row in grid]
        self.player_row = 0
        self.player_col = 0
        self.total_moves = 0
        self.coins_missing = 0
        # self.previous_tile = '.'
        self.goal_row = 0
        self.goal_col = 0
        self.goal_reached = False
        self.trap_triggered = False
        self.find_start_and_end()
        self.find_coins()

    def find_start_and_end(self):
        found_start = found_goal = False
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == 's':
                    self.player_row = y
                    self.player_col = x
                    self.grid[y][x] = 'P'
                    found_start = True
                elif cell == 'g':
                    self.goal_row = y
                    self.goal_col = x
                    found_goal = True

                if found_start and found_goal:
                    return
                
    def find_coins(self):
        self.coins_missing = sum(row.count('c') for row in self.grid)
    
    def print_level(self):
        print("You've spent {} moves in the current level.".format(self.total_moves))
        for row in self.grid:
            print(' '.join(row))

    def move_player(self, direction):
        new_row, new_col = self.player_row, self.player_col

        if direction == 'w':  # Up
            new_row -= 1
        elif direction == 's':  # Down
            new_row += 1
        elif direction == 'a':  # Left
            new_col -= 1
        elif direction == 'd':  # Right
            new_col += 1
        else:
            print("Invalid input. Please enter W, A, S, or D.")
            return

        if (0 > new_row or new_row >= len(self.grid) or 0 > new_col or new_col >= len(self.grid[0])):
            print("You can't move outside the maze!")
            return
        
        if self.grid[new_row][new_col] == 't':
            self.total_moves += 1
            self.trap_triggered = True
            print("Bummer! You've stepped on a trap in {} moves! Go to start.".format(self.total_moves))
            return
        
        if self.grid[new_row][new_col] == 'c':
            self.coins_missing -= 1

        if self.grid[new_row][new_col] == 'g' and self.coins_missing == 0:
            self.total_moves += 1
            self.goal_reached = True
            print("Congratulations! You've reached the goal in {} moves!".format(self.total_moves))
            return
        
        if self.grid[new_row][new_col] == 'g' and self.coins_missing > 0:
            print("You need to collect all coins before reaching the goal!")
            
        if (self.player_row, self.player_col) == (self.goal_row, self.goal_col):
            self.grid[self.player_row][self.player_col] = 'g'
        else:
            self.grid[self.player_row][self.player_col] = '.'
        self.grid[new_row][new_col] = 'P'
        self.player_row, self.player_col = new_row, new_col
        self.total_moves += 1

    def reset_level(self, new_grid):
        self.grid = [row.copy() for row in new_grid]
        self.total_moves = 0
        self.goal_reached = False
        self.trap_triggered = False
        self.find_start_and_end()
        self.find_coins()