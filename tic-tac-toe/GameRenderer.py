import pygame
from constants import *

class GameRenderer:
    """
    Handles all rendering operations for the Tic-Tac-Toe game
    """
    def __init__(self):
        # Initialize fonts with dynamic size
        self.game_over_font = pygame.font.Font(None, GAME_OVER_FONT_SCALE)

    def render_game(self, screen, game_state):
        """
        Main render function that draws the entire game state
        
        Args:
            screen: Pygame surface to draw on
            game_state: Current game state containing board and game status
        """
        # Clear screen with background color
        screen.fill(COLOR_EMPTY)
        
        # Draw game elements
        self._draw_grid(screen)
        self._draw_pieces(screen, game_state.board)
        
        # Draw game over screen if needed
        if game_state.is_game_over:
            self._draw_game_over(screen, game_state.winner)
            
        # Update display
        pygame.display.update()

    def _draw_grid(self, screen):
        """Draws the game grid lines"""
        for i in range(1, BOARD_SIZE):
            # Draw vertical lines
            pygame.draw.line(
                screen, 
                (0, 0, 0),
                (i * CELL_SIZE, 0), 
                (i * CELL_SIZE, WINDOW_SIZE),
                2
            )
            # Draw horizontal lines
            pygame.draw.line(
                screen,
                (0, 0, 0),
                (0, i * CELL_SIZE),
                (WINDOW_SIZE, i * CELL_SIZE),
                2
            )

    def _draw_pieces(self, screen, board):
        """Draws X's and O's on the board"""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x = col * CELL_SIZE + CELL_SIZE // 2
                y = row * CELL_SIZE + CELL_SIZE // 2
                
                if board.board[row][col] == PLAYER_X:
                    self._draw_x(screen, x, y)
                elif board.board[row][col] == PLAYER_O:
                    self._draw_o(screen, x, y)

    def _draw_x(self, screen, x, y):
        """Draws an X symbol at the specified position"""
        size = CELL_SIZE // 3
        pygame.draw.line(
            screen,
            COLOR_X,
            (x - size, y - size),
            (x + size, y + size),
            3
        )
        pygame.draw.line(
            screen,
            COLOR_X,
            (x + size, y - size),
            (x - size, y + size),
            3
        )

    def _draw_o(self, screen, x, y):
        """Draws an O symbol at the specified position"""
        size = CELL_SIZE // 3
        pygame.draw.circle(screen, COLOR_O, (x, y), size, 3)

    def _draw_game_over(self, screen, winner):
        """Draws the game over screen with winner announcement"""
        # Create game over message with padding
        text = f"Winner: {winner}" if winner else "Draw!"
        text_surface = self.game_over_font.render(text, True, COLOR_GRID)
        
        # Center text with padding
        padding = WINDOW_SIZE // 20  # 5% padding
        text_rect = text_surface.get_rect(
            center=(WINDOW_SIZE//2, WINDOW_SIZE//2 - padding)
        )
        
        # Create semi-transparent overlay
        overlay = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
        overlay.set_alpha(128)
        overlay.fill(COLOR_EMPTY)
        
        # Draw overlay and text
        screen.blit(overlay, (0, 0))
        screen.blit(text_surface, text_rect)