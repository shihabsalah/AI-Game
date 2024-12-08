import pygame
import random

from CONSTANTS import *
from Maze import Maze
from Player import Player
from AI import AI
from AIHelpButton import Button

# Pygame initialization
pygame.init()
pygame.display.set_caption("Maze Game")



### --- GAME CLASS --- ###
class MazeGame:
    def __init__(self):
        global SCREEN_WIDTH, SCREEN_HEIGHT, RIGHT_COLUMN_WIDTH, MAZE_WIDTH, MAZE_HEIGHT, GRID_SIZE, CELL_SIZE
        SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
        RIGHT_COLUMN_WIDTH = 300  # Fixed width for the right-side column
        MAZE_WIDTH = SCREEN_WIDTH - RIGHT_COLUMN_WIDTH
        MAZE_HEIGHT = SCREEN_HEIGHT
        # Calculate dynamic columns and rows based on GRID_SIZE
        GRID_SIZE = 200  # Number of maze cells along one dimension
        CELL_SIZE = min(MAZE_WIDTH // GRID_SIZE, MAZE_HEIGHT // GRID_SIZE)  # Dynamic cell size
        COLS = GRID_SIZE  # Use GRID_SIZE directly for columns
        CELL_SIZE = MAZE_WIDTH // COLS  # Dynamically calculate cell size
        ROWS = MAZE_HEIGHT // CELL_SIZE  # Adjust rows to fit the height dynamically
        

        self.game_over = False
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        
        self.clock = pygame.time.Clock()
        self.maze = Maze(ROWS, COLS, CELL_SIZE)
        self.player = Player((1,1))
        self.player_position = [1, 1]
        self.exit_position = [COLS - 2, ROWS - 2]
        self.ai = AI((1,1), tuple(self.exit_position))
        self.ai_help_path = []
        self.font = pygame.font.Font(None, 36)

        # Define buttons
        self.buttons = [
            Button(SCREEN_WIDTH - RIGHT_COLUMN_WIDTH + 50, 100, 200, 50, "BFS", self.font, BLUE, WHITE),
            Button(SCREEN_WIDTH - RIGHT_COLUMN_WIDTH + 50, 200, 200, 50, "DFS", self.font, BLUE, WHITE),
            Button(SCREEN_WIDTH - RIGHT_COLUMN_WIDTH + 50, 300, 200, 50, "A*", self.font, BLUE, WHITE),
            Button(SCREEN_WIDTH - RIGHT_COLUMN_WIDTH + 50, 400, 200, 50, "Exit", self.font, RED, WHITE)
        ]

    def handle_input(self, event):

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.player.move(self.maze.maze, "UP")
        elif keys[pygame.K_DOWN]:
            self.player.move(self.maze.maze, "DOWN")
        elif keys[pygame.K_LEFT]:
            self.player.move(self.maze.maze, "LEFT")
        elif keys[pygame.K_RIGHT]:
            self.player.move(self.maze.maze, "RIGHT")
        self.player_position = self.player.position
            
        if event.type == pygame.MOUSEBUTTONDOWN:

            for button in self.buttons:
                if button.is_clicked(event.pos):
                    if button.text == "BFS":
                        self.ai_help_path = self.ai.bfs(tuple(self.player.position),self.maze.maze)
                    elif button.text == "DFS":
                        self.ai_help_path = self.ai.dfs(tuple(self.player.position), self.maze.maze)
                        pass
                    elif button.text == "A*":
                        self.ai_help_path = self.ai.a_star(tuple(self.player.position), self.maze.maze)
                        pass
                    elif button.text == "Exit":
                        pygame.quit()
                        exit()


    def draw(self):
         # Draw the maze
        self.maze.draw(self.screen, self.player_position, self.exit_position, self.ai_help_path)

        # Draw the right column and buttons
        pygame.draw.rect(self.screen, GRAY, (MAZE_WIDTH, 0, RIGHT_COLUMN_WIDTH, SCREEN_HEIGHT))  # Right column background
        for button in self.buttons:
            button.draw(self.screen)


    def update(self):
        # Check if player reached the exit
        if self.player.position == list(self.exit_pos):
            self.game_over = True
            self.win = True

    def run(self):
        game = self
        running = True
        while running:
            self.screen.fill(BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                game.handle_input(event)

            game.draw()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

