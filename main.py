import pygame
import random

from CONSTANTS import *
from Maze import Maze
from Player import Player
from AI import AI
from AIHelpButton import Button

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze of Logic")
clock = pygame.time.Clock()


### --- GAME CLASS --- ###
class MazeGame:
    def __init__(self):
        self.maze = Maze(GRID_SIZE)
        self.player = Player((1, 1))
        self.exit_pos = (GRID_SIZE - 2, GRID_SIZE - 2)
        self.ai = AI((1, 1), self.exit_pos)
        self.ai_help_path = []
        self.font = pygame.font.Font(None, 36)
        self.algorithm = "bfs"  # Default algorithm

        # Buttons for algorithm selection
        self.bfs_button = Button(WIDTH - 200, 10, 150, 40, "BFS", self.font, BLUE, WHITE)
        self.dfs_button = Button(WIDTH - 200, 60, 150, 40, "DFS", self.font, BLUE, WHITE)
        self.a_star_button = Button(WIDTH - 200, 110, 150, 40, "A*", self.font, BLUE, WHITE)

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
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.bfs_button.is_clicked(event.pos):
                self.algorithm = "bfs"
            elif self.dfs_button.is_clicked(event.pos):
                self.algorithm = "dfs"
            elif self.a_star_button.is_clicked(event.pos):
                self.algorithm = "a_star"

            # Trigger AI help
            if self.algorithm == "bfs":
                self.ai_help_path = self.ai.bfs(self.maze.maze)
            elif self.algorithm == "dfs":
                self.ai_help_path = self.ai.dfs(self.maze.maze)
            elif self.algorithm == "a_star":
                self.ai_help_path = self.ai.a_star(self.maze.maze)

    def draw(self):
        self.maze.draw(screen, self.player.position, self.exit_pos, self.ai_help_path)

        # Draw buttons
        self.bfs_button.draw(screen)
        self.dfs_button.draw(screen)
        self.a_star_button.draw(screen)

        # Display selected algorithm
        text = self.font.render(f"Algorithm: {self.algorithm.upper()}", True, YELLOW)
        screen.blit(text, (10, HEIGHT - 40))


    def update(self):
        # Check if player reached the exit
        if self.player.position == list(self.exit_pos):
            self.game_over = True
            self.win = True

    def run(self):
        running = True
        while running:
            screen.fill(BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
            self.handle_input(event)
            self.update()
            self.draw()
            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()


### --- RUN THE GAME --- ###
if __name__ == "__main__":
    game = MazeGame()
    game.run()