import pygame
from CONSTANTS import CONSTANTS
from View.UI.Button import Button
from View.UI.InputField import InputField

class GameView:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.buttons = []
        self.grid_size_field = None
        self.create_ui()  # Initialize UI components

    def create_ui(self):
        # Define buttons
        self.buttons = [
            Button(CONSTANTS.SCREEN_WIDTH - CONSTANTS.RIGHT_COLUMN_WIDTH + 50, 100, 200, 50, "BFS", self.font, CONSTANTS.BLUE, CONSTANTS.WHITE),
            Button(CONSTANTS.SCREEN_WIDTH - CONSTANTS.RIGHT_COLUMN_WIDTH + 50, 200, 200, 50, "DFS", self.font, CONSTANTS.BLUE, CONSTANTS.WHITE),
            Button(CONSTANTS.SCREEN_WIDTH - CONSTANTS.RIGHT_COLUMN_WIDTH + 50, 300, 200, 50, "A*", self.font, CONSTANTS.BLUE, CONSTANTS.WHITE),
            Button(CONSTANTS.SCREEN_WIDTH - CONSTANTS.RIGHT_COLUMN_WIDTH + 50, 400, 200, 50, "Refresh", self.font, CONSTANTS.GREEN, CONSTANTS.WHITE),
            Button(CONSTANTS.SCREEN_WIDTH - CONSTANTS.RIGHT_COLUMN_WIDTH + 50, 500, 200, 50, "Exit", self.font, CONSTANTS.RED, CONSTANTS.WHITE),
        ]

        # Define input field for grid size
        self.grid_size_field = InputField(
            CONSTANTS.SCREEN_WIDTH - CONSTANTS.RIGHT_COLUMN_WIDTH + 50,
            600,
            200,
            50,
            self.font,
            default_text=str(CONSTANTS.GRID_SIZE),
            text_color=CONSTANTS.BLACK,
            border_color=CONSTANTS.BLACK,
        )

    def draw_maze(self, maze, player_pos, exit_pos, ai_path):
        for y in range(maze.rows):
            for x in range(maze.cols):
                color = CONSTANTS.WHITE if maze.maze[y][x] == 0 else CONSTANTS.BLACK
                pygame.draw.rect(
                    self.screen,
                    color,
                    (x * maze.cell_size, y * maze.cell_size, maze.cell_size, maze.cell_size)
                )

        for pos in ai_path:
            pygame.draw.rect(
                self.screen,
                CONSTANTS.RED,
                (pos[0] * maze.cell_size, pos[1] * maze.cell_size, maze.cell_size, maze.cell_size)
            )

        pygame.draw.rect(
            self.screen,
            CONSTANTS.GREEN,
            (player_pos[0] * maze.cell_size, player_pos[1] * maze.cell_size, maze.cell_size, maze.cell_size)
        )

        pygame.draw.rect(
            self.screen,
            CONSTANTS.YELLOW,
            (exit_pos[0] * maze.cell_size, exit_pos[1] * maze.cell_size, maze.cell_size, maze.cell_size)
        )

    def draw_sidebar(self, buttons, grid_size_field, ai_steps):
        # Draw right column background
        pygame.draw.rect(self.screen, CONSTANTS.GRAY, (CONSTANTS.MAZE_WIDTH, 0, CONSTANTS.RIGHT_COLUMN_WIDTH, CONSTANTS.SCREEN_HEIGHT))

        # Draw buttons
        for button in buttons:
            button.draw(self.screen)

        # Draw grid size input field
        grid_size_field.draw(self.screen)

        # Display AI step count
        step_text = self.font.render(f"AI Steps: {ai_steps}", True, CONSTANTS.BLACK)
        self.screen.blit(step_text, (CONSTANTS.SCREEN_WIDTH - CONSTANTS.RIGHT_COLUMN_WIDTH + 50, 700))
