import pygame

class Renderer:
    def __init__(self, maze, tile_size=64):
        pygame.init()

        self.maze = maze
        self.tile_size = tile_size

        self.rows = len(maze.grid)
        self.cols = len(maze.grid[0])

        self.width = self.cols * tile_size
        self.height = self.rows * tile_size

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Maze Game")

        # Simple colours (no PNG yet)
        self.colours = {
            '.': (240, 240, 240),  # floor
            't': (200, 60, 60),    # trap
            'c': (255, 215, 0),    # coin
            'g': (60, 200, 60),    # goal
            'P': (50, 100, 255),   # player
            's': (240, 240, 240)   # start (treated as floor)
        }

    def draw(self):
        self.screen.fill((0, 0, 0))

        for row in range(self.rows):
            for col in range(self.cols):
                tile = self.maze.grid[row][col]
                colour = self.colours.get(tile, (100, 100, 100))

                rect = pygame.Rect(
                    col * self.tile_size,
                    row * self.tile_size,
                    self.tile_size,
                    self.tile_size
                )

                pygame.draw.rect(self.screen, colour, rect)
                pygame.draw.rect(self.screen, (30, 30, 30), rect, 1)

        pygame.display.flip()

    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    return 'w'
                if event.key == pygame.K_s:
                    return 's'
                if event.key == pygame.K_a:
                    return 'a'
                if event.key == pygame.K_d:
                    return 'd'

        return None