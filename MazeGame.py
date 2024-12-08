import pygame
import random

from CONSTANTS import CONSTANTS
from Maze import Maze
from Player import Player
from AI import AI
from View.GameView import GameView
from AIMetrics import AIMetrics

# Pygame initialization
pygame.init()
pygame.display.set_caption("Maze Game")



### --- GAME CLASS --- ###
class MazeGame:

    def __init__(self):
        
        CONSTANTS.set_screen_size()
        self.setup_ui()
        self.setup_game()
        


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

        self.player_position = self.player.position  # Ensure this is updated


        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
            # Handle grid size input
            self.view.grid_size_field.handle_event(event)

            # Check button clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.view.buttons:
                    if button.is_clicked(event.pos):
                        if button.text == "BFS":
                            self.ai_metrics = self.ai.bfs(tuple(self.player.position), self.maze.maze)
                        elif button.text == "DFS":
                            self.ai_metrics = self.ai.dfs(tuple(self.player.position), self.maze.maze)
                        elif button.text == "A*":
                            self.ai_metrics = self.ai.a_star(tuple(self.player.position), self.maze.maze)
                        elif button.text == "Refresh":
                            try:
                                new_grid_size = int(self.view.grid_size_field.text)
                                if new_grid_size > 5:
                                    CONSTANTS.set_screen_size(new_grid_size)
                                    # Re-initialize the game
                                    self.setup_game()
                            except ValueError:
                                print("Invalid grid size")
                        elif button.text == "Exit":
                            pygame.quit()
                            exit()



    def draw(self):
        # Draw the maze
        self.view.draw_maze(self.maze, self.player_position, self.exit_position, self.ai_metrics.path)
        # Draw the sidebar
        self.view.draw_sidebar(self.view.buttons, self.view.grid_size_field, self.ai_metrics.path_length if self.ai_metrics else 0)



    def update(self):
        # Check if player reached the exit
        if self.player.position == list(self.exit_position):
            self.game_over = True
            self.win = True
            print("You win!")

    def run(self):
        game = self
        running = True
        while running:
            self.screen.fill(CONSTANTS.BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                game.handle_input(event)

            game.draw()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()



    def setup_game(self):

        # Initialize the clock
        self.clock = pygame.time.Clock()

        # Initialize font
        self.font = pygame.font.Font(None, 36)

        self.set_models()     

    def set_models(self):
        """
        Reset the maze, player position, and AI helper path to start a new game.
        """
        # Regenerate the maze
        self.maze = Maze(CONSTANTS.ROWS, CONSTANTS.COLS, CONSTANTS.CELL_SIZE)

        # Reset player position
        self.player = Player((1, 1))
        self.player_position = [1, 1]

        # Reset exit position
        self.exit_position = [CONSTANTS.COLS - 2, CONSTANTS.ROWS - 2]

        # Reset AI path
        self.ai = AI((1, 1), tuple(self.exit_position))
        self.ai_metrics:AIMetrics = AIMetrics("A*", [], 0, 0, 0, 0, 0, 0)

        # Reset game state
        self.game_over = False

    def setup_ui(self):
        self.screen = pygame.display.set_mode((CONSTANTS.SCREEN_WIDTH, CONSTANTS.SCREEN_HEIGHT), pygame.FULLSCREEN)
        self.view = GameView(self.screen)