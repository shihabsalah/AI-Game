import pygame
from CONSTANTS import CONSTANTS
from View.UI.Button import Button
from View.UI.InputField import InputField

class GameView:

    def __init__(self, screen, font_size=36, metrics_font_size=28):
        """
        :param screen: Pygame screen object.
        :param font_size: Font size for buttons and other UI elements.
        :param metrics_font_size: Font size for the metrics display.
        """
        self.screen = screen
        self.font = pygame.font.Font(None, font_size)
        self.metrics_font = pygame.font.Font(None, metrics_font_size)  # Separate font for metrics
        self.buttons = []
        self.grid_size_field = None
        self.metrics_text = []
        self.column_start_x = CONSTANTS.SCREEN_WIDTH - CONSTANTS.RIGHT_COLUMN_WIDTH + 50
        self.column_start_y = 100
        self.element_height = 50
        self.vertical_spacing = 10
        self.create_ui()



    def _calculate_column_positions(self, count, start_y=None):
        """
        Calculate positions for elements in a vertical column layout.
        :param count: Number of elements in the column.
        :return: List of (x, y) positions.
        """
        if start_y is None:
            start_y = self.column_start_y
        positions = []
        y = start_y
        for _ in range(count):
            positions.append((self.column_start_x, y))
            y += self.element_height + self.vertical_spacing
        return positions

    def create_ui(self):
        # Define buttons
        button_labels = ["BFS", "DFS", "A*", "Regenerate"]
        button_positions = self._calculate_column_positions(len(button_labels))
        
        self.buttons = [
            Button(x, y, 200, self.element_height, label, self.font, CONSTANTS.BLUE, CONSTANTS.WHITE)
            for (x, y), label in zip(button_positions, button_labels)
        ]

        # Define input field for grid size
        grid_size_y = button_positions[-1][1] + self.element_height + self.vertical_spacing
        self.grid_size_field = InputField(
            self.column_start_x,
            grid_size_y,
            200,
            self.element_height,
            self.font,
            default_text=str(CONSTANTS.GRID_SIZE),
            text_color=CONSTANTS.BLACK,
            border_color=CONSTANTS.BLACK,
        )

         # Define difficulty buttons
        difficulty_y = grid_size_y + self.element_height + self.vertical_spacing
        self.difficulty_buttons = [
            Button(self.column_start_x, difficulty_y, 200, self.element_height, "Increase", self.font, CONSTANTS.GREEN, CONSTANTS.BLACK),
            Button(self.column_start_x, difficulty_y + self.element_height + self.vertical_spacing, 200, self.element_height, "Decrease", self.font, CONSTANTS.RED, CONSTANTS.BLACK),
        ]

        # Move Exit button to the bottom
        self.exit_button = Button(
            self.column_start_x,
            CONSTANTS.SCREEN_HEIGHT - self.element_height - self.vertical_spacing,
            200,
            self.element_height,
            "Exit",
            self.font,
            CONSTANTS.RED,
            CONSTANTS.WHITE,
        )

    def update_metrics(self, metrics):
        """
        Update metrics text to display in the sidebar.
        :param metrics: Instance of AIMetrics containing the metrics to display.
        """
        self.metrics_text = [
            f"Algorithm: {metrics.algorithm_name}",
            f"Nodes Explored: {metrics.nodes_explored}",
            f"Path Length: {metrics.path_length}",
            f"Execution Time: {metrics.execution_time:.4f}s",
            f"Memory Usage: {metrics.memory_usage:.2f} MB",
            f"Total Cells: {(CONSTANTS.ROWS-2)*(CONSTANTS.COLS-2)}"
        ]

    def draw_maze(self, maze, player_pos, exit_pos, ai_path):
        # Draw maze
        for y in range(maze.rows):
            for x in range(maze.cols):
                color = CONSTANTS.WHITE if maze.maze[y][x] == 0 else CONSTANTS.BLACK
                pygame.draw.rect(
                    self.screen,
                    color,
                    (x * maze.cell_size, y * maze.cell_size, maze.cell_size, maze.cell_size)
                )

        # Draw AI path
        for pos in ai_path:
            pygame.draw.rect(
                self.screen,
                CONSTANTS.RED,
                (pos[0] * maze.cell_size, pos[1] * maze.cell_size, maze.cell_size, maze.cell_size)
            )

        # Draw player
        pygame.draw.rect(
            self.screen,
            CONSTANTS.GREEN,
            (player_pos[0] * maze.cell_size, player_pos[1] * maze.cell_size, maze.cell_size, maze.cell_size)
        )

        # Draw exit
        pygame.draw.rect(
            self.screen,
            CONSTANTS.YELLOW,
            (exit_pos[0] * maze.cell_size, exit_pos[1] * maze.cell_size, maze.cell_size, maze.cell_size)
        )

    def draw_sidebar(self):
        # Draw right column background
        pygame.draw.rect(self.screen, CONSTANTS.GRAY, (CONSTANTS.MAZE_WIDTH, 0, CONSTANTS.RIGHT_COLUMN_WIDTH, CONSTANTS.SCREEN_HEIGHT))

        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)

        # Draw grid size input field
        self.grid_size_field.draw(self.screen)

        # Draw difficulty buttons
        for button in self.difficulty_buttons:
            button.draw(self.screen)

        # Draw Exit button
        self.exit_button.draw(self.screen)

        # Display metrics text
        metrics_y = self.difficulty_buttons[-1].rect.y + self.element_height + self.vertical_spacing
        for metric in self.metrics_text:
            text_surface = self.metrics_font.render(metric, True, CONSTANTS.BLACK)
            self.screen.blit(text_surface, (self.column_start_x, metrics_y))
            metrics_y += self.metrics_font.get_linesize() + self.vertical_spacing