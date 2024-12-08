import pygame
import random

from CONSTANTS import CONSTANTS
from Maze import Maze
from Player import Player
from AI import AI
from AIHelpButton import Button
from InputField import InputField

# Pygame initialization
pygame.init()
pygame.display.set_caption("Maze Game")



### --- GAME CLASS --- ###
class MazeGame:
    def __init__(self):
        
        CONSTANTS.set_screen_size()
        self.iniate_services_and_variables()
        
        # Define buttons
        self.buttons = [
            Button(CONSTANTS.SCREEN_WIDTH - CONSTANTS.RIGHT_COLUMN_WIDTH + 50, 100, 200, 50, "BFS", self.font, CONSTANTS.BLUE, CONSTANTS.WHITE),
            Button(CONSTANTS.SCREEN_WIDTH - CONSTANTS.RIGHT_COLUMN_WIDTH + 50, 200, 200, 50, "DFS", self.font, CONSTANTS.BLUE, CONSTANTS.WHITE),
            Button(CONSTANTS.SCREEN_WIDTH - CONSTANTS.RIGHT_COLUMN_WIDTH + 50, 300, 200, 50, "A*", self.font, CONSTANTS.BLUE, CONSTANTS.WHITE),
            Button(CONSTANTS.SCREEN_WIDTH - CONSTANTS.RIGHT_COLUMN_WIDTH + 50, 400, 200, 50, "Refresh", self.font, CONSTANTS.GREEN, CONSTANTS.WHITE),  # New Refresh button
            Button(CONSTANTS.SCREEN_WIDTH - CONSTANTS.RIGHT_COLUMN_WIDTH + 50, 500, 200, 50, "Exit", self.font, CONSTANTS.RED, CONSTANTS.WHITE)
        ]
        # Define input field for grid size
        self.grid_size_field = InputField(
            CONSTANTS.SCREEN_WIDTH - CONSTANTS.RIGHT_COLUMN_WIDTH + 50,
            600,
            200,
            50,
            self.font,
            default_text=str(CONSTANTS.GRID_SIZE),  # Show default grid size
            text_color=CONSTANTS.BLACK,
            border_color=CONSTANTS.BLACK
        )


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

        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
            # Pass events to the input field
            self.grid_size_field.handle_event(event)

            # Check button clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.is_clicked(event.pos):
                        if button.text == "BFS":
                            self.ai_help_path = self.ai.bfs(tuple(self.player.position), self.maze.maze)
                        elif button.text == "DFS":
                            self.ai_help_path = self.ai.dfs(tuple(self.player.position), self.maze.maze)
                        elif button.text == "A*":
                            self.ai_help_path = self.ai.a_star(tuple(self.player.position), self.maze.maze)
                        elif button.text == "Refresh":
                            # Use the value from the input field as the new grid size
                            try:
                                new_grid_size = int(self.grid_size_field.text)
                                if new_grid_size > 5:  # Ensure grid size is reasonable
                                    print(f"Refreshing maze with grid size: {new_grid_size}")
                                    CONSTANTS.set_screen_size(new_grid_size)
                                    self.reset_game()
                                else:
                                    print("Error: Grid size must be greater than 5.")
                            except ValueError:
                                print("Error: Invalid grid size entered.")
                        elif button.text == "Exit":
                            pygame.quit()
                            exit()

    def draw(self):
        # Draw the maze
        self.maze.draw(self.screen, self.player_position, self.exit_position, self.ai_help_path)

        # Draw the right column and buttons
        pygame.draw.rect(self.screen, CONSTANTS.GRAY, (CONSTANTS.MAZE_WIDTH, 0, CONSTANTS.RIGHT_COLUMN_WIDTH, CONSTANTS.SCREEN_HEIGHT))  # Right column background
        for button in self.buttons:
            button.draw(self.screen)

        # Draw the grid size input field
        self.grid_size_field.draw(self.screen)



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



    def iniate_services_and_variables(self):

        self.game_over = False
        
        self.screen = pygame.display.set_mode((CONSTANTS.SCREEN_WIDTH, CONSTANTS.SCREEN_HEIGHT), pygame.FULLSCREEN)
        
        self.clock = pygame.time.Clock()
        self.maze = Maze(CONSTANTS.ROWS, CONSTANTS.COLS, CONSTANTS.CELL_SIZE)

        # Initialize player
        self.player = Player((1,1))
        self.player_position = [1, 1]
        self.exit_position = [CONSTANTS.COLS - 2, CONSTANTS.ROWS - 2]

        # Initialize AI
        self.ai = AI((1,1), tuple(self.exit_position))
        self.ai_help_path = []

        # Initialize font
        self.font = pygame.font.Font(None, 36)

    def reset_game(self):
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
        self.ai_help_path = []

        # Reset game state
        self.game_over = False
        print("Game has been reset.")
