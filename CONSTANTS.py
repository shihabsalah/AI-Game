import pygame

# A class of static constants
class CONSTANTS:
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    BLUE = (0, 0, 255)
    GRAY = (128, 128, 128)

    # Screen
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 800
    SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

    # Maze
    GRID_SIZE = 20
    CELL_SIZE = SCREEN_WIDTH // GRID_SIZE
    MAZE_WIDTH = SCREEN_WIDTH - 200
    MAZE_HEIGHT = SCREEN_HEIGHT
    RIGHT_COLUMN_WIDTH = SCREEN_WIDTH - MAZE_WIDTH
    COLS = MAZE_WIDTH // CELL_SIZE
    ROWS = MAZE_HEIGHT // CELL_SIZE

    @classmethod
    def set_screen_size(cls, mazeSize=GRID_SIZE):
        cls.SCREEN_WIDTH, cls.SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
        cls.GRID_SIZE = mazeSize
        cls.RIGHT_COLUMN_WIDTH = 300  # Fixed width for the right-side column
        cls.MAZE_WIDTH = cls.SCREEN_WIDTH - cls.RIGHT_COLUMN_WIDTH
        cls.MAZE_HEIGHT = cls.SCREEN_HEIGHT
        # Calculate dynamic columns and rows based on GRID_SIZE
        cls.CELL_SIZE = min(cls.MAZE_WIDTH // cls.GRID_SIZE, cls.MAZE_HEIGHT // cls.GRID_SIZE)  # Dynamic cell size
        cls.COLS = cls.GRID_SIZE  # Use GRID_SIZE directly for columns
        cls.CELL_SIZE = cls.MAZE_WIDTH // cls.COLS  # Dynamically calculate cell size
        cls.ROWS = cls.MAZE_HEIGHT // cls.CELL_SIZE  # Adjust rows to fit the height dynamically


    # Player
    PLAYER_COLOR = RED
    PLAYER_RADIUS = CELL_SIZE // 2

    # AI
    AI_COLOR = YELLOW
    AI_RADIUS = CELL_SIZE // 2

    # Button
    BUTTON_COLOR = (70, 130, 180)
    BUTTON_HOVER_COLOR = (100, 149, 237)
    BUTTON_TEXT_COLOR = WHITE

    
