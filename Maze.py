import pygame
import random
from queue import Queue
from CONSTANTS import *


class Maze:
    def __init__(self, rows, cols, cell_size):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.maze = self.generate_maze()


    def generate_maze(self):
        maze = [[1 for _ in range(self.cols)] for _ in range(self.rows)]

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
                if 1 <= nx < self.cols - 1 and 1 <= ny < self.rows - 1 and maze[ny][nx] == 1:
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
        goal_x, goal_y = self.cols - 2, self.rows - 2
        maze[goal_y][goal_x] = 0  # Make sure the goal is open
        maze[1][1] = 0  # Make sure the start is open
        # Connect the exit to the maze
        if not any(
            maze[goal_y + dy][goal_x + dx] == 0
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
        ):
            maze[goal_y - 1][goal_x] = 0  # Carve a path to the goal


        return maze

    def add_branches(self, maze):
        branch_count = (self.cols * self.rows) // 20  # Adjust for difficulty
        for _ in range(branch_count):
            x, y = random.randint(1, self.cols - 2), random.randint(1, self.rows - 2)

            # Only add branches in walls with enough space
            if maze[y][x] == 1:
                neighbors = []
                for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                    nx, ny = x + dx, y + dy
                    if 1 <= nx < self.cols - 1 and 1 <= ny < self.rows - 1 and maze[ny][nx] == 0:
                        neighbors.append((nx, ny))

                if len(neighbors) >= 2:  # Only create branches in dense areas
                    maze[y][x] = 0
                    for nx, ny in neighbors:
                        maze[(y + ny) // 2][(x + nx) // 2] = 0

    def add_dead_ends(self, maze):
        dead_end_count = (self.cols * self.rows) // 15  # Adjust for difficulty
        for _ in range(dead_end_count):
            x, y = random.randint(1, self.cols - 2), random.randint(1, self.rows - 2)

            # Only add dead ends to open spaces
            if maze[y][x] == 0 and self.is_valid_dead_end(maze, x, y):
                maze[y][x] = 1

    def is_valid_dead_end(self, maze, x, y):
        # A valid dead end is connected to exactly one path
        open_neighbors = 0
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.cols and 0 <= ny < self.rows and maze[ny][nx] == 0:
                open_neighbors += 1
        return open_neighbors == 1


    def draw(self, screen, player_pos, exit_pos, ai_path):
        for y in range(self.rows):
            for x in range(self.cols):
                color = CONSTANTS.WHITE if self.maze[y][x] == 0 else CONSTANTS.BLACK
                pygame.draw.rect(
                    screen,
                    color,
                    (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                )

        # Draw AI path
        for pos in ai_path:
            pygame.draw.rect(
                screen,
                CONSTANTS.RED,
                (pos[0] * self.cell_size, pos[1] * self.cell_size, self.cell_size, self.cell_size)
            )

        # Draw player
        pygame.draw.rect(
            screen,
            CONSTANTS.GREEN,
            (player_pos[0] * self.cell_size, player_pos[1] * self.cell_size, self.cell_size, self.cell_size)
        )

        # Draw exit
        pygame.draw.rect(
            screen,
            CONSTANTS.YELLOW,
            (exit_pos[0] * self.cell_size, exit_pos[1] * self.cell_size, self.cell_size, self.cell_size)
        )



# if __name__ == "__main__":
#     maze = Maze(GRID_SIZE)
#     for row in maze.maze:
#         print("".join([" " if cell == 0 else "#" for cell in row]))
