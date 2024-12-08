import pygame
import sys

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
        

    def handle_player_movement(self):
        """
        Handle continuous player movement based on key states.
        """
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if current_time - self.last_move_time >= self.movement_cooldown:
            if keys[pygame.K_UP]:
                self.player.move(self.maze.maze, "UP")
                self.last_move_time = current_time
            elif keys[pygame.K_DOWN]:
                self.player.move(self.maze.maze, "DOWN")
                self.last_move_time = current_time
            elif keys[pygame.K_LEFT]:
                self.player.move(self.maze.maze, "LEFT")
                self.last_move_time = current_time
            elif keys[pygame.K_RIGHT]:
                self.player.move(self.maze.maze, "RIGHT")
                self.last_move_time = current_time

        self.player_position = self.player.position  # Ensure this is updated


    def handle_input(self, event):

        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
            # Handle grid size input
            self.view.grid_size_field.handle_event(event)

            # Check button clicks
            if event.type == pygame.MOUSEBUTTONDOWN:


                for button in self.view.difficulty_buttons:
                    if button.is_clicked(event.pos):
                        if button.text == "Decrease":
                            self.decrease_grid_size()
                        elif button.text == "Increase":
                            self.increase_grid_size()

                for button in self.view.buttons:
                    if button.is_clicked(event.pos):
                        if button.text == "Regenerate":
                            try:
                                new_grid_size = int(self.view.grid_size_field.text)
                                if new_grid_size > 5:
                                    CONSTANTS.set_screen_size(new_grid_size)
                                    # Re-initialize the game
                                    self.setup_game()
                            except ValueError:
                                print("Invalid grid size")
                        else:
                            if button.text == "BFS":
                                self.ai_metrics = self.ai.bfs(tuple(self.player.position), self.maze.maze)
                            elif button.text == "DFS":
                                self.ai_metrics = self.ai.dfs(tuple(self.player.position), self.maze.maze)
                            elif button.text == "A*":
                                self.ai_metrics = self.ai.a_star(tuple(self.player.position), self.maze.maze)
                            self.view.update_metrics(self.ai_metrics)
                
                if self.view.exit_button.is_clicked(event.pos):
                    self.game_over=True


    def draw(self):
        # Draw the maze
        self.view.draw_maze(self.maze, self.player_position, self.exit_position, self.ai_metrics.path)
        # Draw the sidebar
        self.view.draw_sidebar()



    def update(self):
        # Check if player reached the exit
        if self.player.position == list(self.exit_position):
            self.game_over = True
            self.win = True
            print("You win!")
            self.celebrate_victory()

    def celebrate_victory(self):
        for _ in range(3):  # Blink 10 times
            self.screen.fill(CONSTANTS.BLACK)
            pygame.display.flip()
            pygame.time.delay(300)  # Pause for 200ms

            font = pygame.font.Font(None, 72)
            text_surface = font.render("You Win!", True, CONSTANTS.GREEN)
            text_rect = text_surface.get_rect(center=(CONSTANTS.SCREEN_WIDTH // 2, CONSTANTS.SCREEN_HEIGHT // 2))
            self.screen.blit(text_surface, text_rect)
            pygame.display.flip()
            pygame.time.delay(300)  # Pause for 200ms

        self.start_game()


    def run(self):
        game = self
        running = True
        while running:
            self.screen.fill(CONSTANTS.BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                game.handle_input(event)

            if self.game_over:
                break  # Exit loop if the game is over

            game.handle_player_movement()

            game.update()

            self.screen.fill(CONSTANTS.BLACK)

            game.draw()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()



    def increase_grid_size(self):
        """
        Increase the grid size exponentially by squaring it, up to the upper limit.
        """
        if self.current_grid_size < self.max_grid_size:
            new_grid_size = int(self.current_grid_size * 2)
            self.current_grid_size = min(new_grid_size, self.max_grid_size)
            print(f"Grid size increased to: {self.current_grid_size}")
            self.apply_grid_size()

    def decrease_grid_size(self):
        """
        Decrease the grid size by taking the square root, down to the lower limit.
        """
        if self.current_grid_size > self.min_grid_size:
            new_grid_size = int(self.current_grid_size / 2)
            self.current_grid_size = max(new_grid_size, self.min_grid_size)
            print(f"Grid size decreased to: {self.current_grid_size}")
            self.apply_grid_size()


    def apply_grid_size(self):
            """
            Apply the updated grid size to the maze and UI.
            """
            CONSTANTS.set_screen_size(self.current_grid_size)
            self.view.grid_size_field.text = str(self.current_grid_size)
            self.start_game()


    def setup_game(self):

        self.movement_cooldown = 100  # Cooldown in milliseconds
        self.last_move_time = pygame.time.get_ticks()  # Timestamp of the last move
        self.current_grid_size = CONSTANTS.GRID_SIZE  # Track current grid size
        self.max_grid_size = 1000  # Upper limit for grid size
        self.min_grid_size = 6     # Lower limit for grid size

        # Initialize the clock
        self.clock = pygame.time.Clock()

        # Initialize font
        self.font = pygame.font.Font(None, 36)

        self.start_game()     

    def start_game(self):
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