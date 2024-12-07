import pygame
import random
from queue import Queue
from CONSTANTS import *


class Maze:
    def __init__(self, grid_size, cell_size):
        self.cell_size = cell_size
        self.grid_size = grid_size
        self.maze = self.generate_maze()


    def generate_maze(self):
        maze = [[1 for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        # Start at (1, 1)
        stack = [(1, 1)]
        maze[1][1] = 0

        while stack:
            cx, cy = stack[-1]
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            random.shuffle(directions)

            carved = False
            for dx, dy in directions:
                nx, ny = cx + dx * 2, cy + dy * 2
                if 1 <= nx < self.grid_size - 1 and 1 <= ny < self.grid_size - 1 and maze[ny][nx] == 1:
                    maze[cy + dy][cx + dx] = 0  # Carve passage
                    maze[ny][nx] = 0  # Move to new cell
                    stack.append((nx, ny))
                    carved = True
                    break

            if not carved:  # Backtrack if no direction is valid
                stack.pop()

        # Add branches for complexity
        self.add_branches(maze)

        # Add dead ends
        self.add_dead_ends(maze)

        # Ensure the exit is reachable
        exit_x, exit_y = self.grid_size - 2, self.grid_size - 2
        maze[exit_y][exit_x] = 0

        # Connect the exit to the main maze
        if not any(maze[exit_y + dy][exit_x + dx] == 0 for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]):
            maze[exit_y - 1][exit_x] = 0


        return maze

    def add_branches(self, maze):
        branch_count = (self.grid_size * self.grid_size) // 20  # Adjust for difficulty
        for _ in range(branch_count):
            x, y = random.randint(1, self.grid_size - 2), random.randint(1, self.grid_size - 2)

            # Only add branches in walls with enough space
            if maze[y][x] == 1:
                neighbors = []
                for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                    nx, ny = x + dx, y + dy
                    if 1 <= nx < self.grid_size - 1 and 1 <= ny < self.grid_size - 1 and maze[ny][nx] == 0:
                        neighbors.append((nx, ny))

                if len(neighbors) >= 2:  # Only create branches in dense areas
                    maze[y][x] = 0
                    for nx, ny in neighbors:
                        maze[(y + ny) // 2][(x + nx) // 2] = 0

    def add_dead_ends(self, maze):
        dead_end_count = (self.grid_size * self.grid_size) // 15  # Adjust for difficulty
        for _ in range(dead_end_count):
            x, y = random.randint(1, self.grid_size - 2), random.randint(1, self.grid_size - 2)

            # Only add dead ends to open spaces
            if maze[y][x] == 0 and self.is_valid_dead_end(maze, x, y):
                maze[y][x] = 1

    def is_valid_dead_end(self, maze, x, y):
        # A valid dead end is connected to exactly one path
        open_neighbors = 0
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size and maze[ny][nx] == 0:
                open_neighbors += 1
        return open_neighbors == 1


    def draw(self, screen, player_pos, exit_pos, ai_path):
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                color = WHITE if cell == 0 else BLACK
                pygame.draw.rect(
                    screen,
                    color,
                    (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                )

        # Draw AI path
        for pos in ai_path:
            pygame.draw.rect(
                screen,
                RED,
                (pos[0] * self.cell_size, pos[1] * self.cell_size, self.cell_size, self.cell_size)
            )

        # Draw player
        pygame.draw.rect(
            screen,
            GREEN,
            (player_pos[0] * self.cell_size, player_pos[1] * self.cell_size, self.cell_size, self.cell_size)
        )

        # Draw exit
        pygame.draw.rect(
            screen,
            YELLOW,
            (exit_pos[0] * self.cell_size, exit_pos[1] * self.cell_size, self.cell_size, self.cell_size)
        )


# if __name__ == "__main__":
#     maze = Maze(GRID_SIZE)
#     for row in maze.maze:
#         print("".join([" " if cell == 0 else "#" for cell in row]))
