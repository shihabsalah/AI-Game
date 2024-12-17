import pygame
from board import Board
from GameRenderer import GameRenderer
from AI.ai import AI
from constants import *

class Game:
    """
    Main game class handling game logic and state
    """
    def __init__(self):
        # Initialize game state
        self.board = Board()
        self.ai = AI(PLAYER_O)
        self.current_player = PLAYER_X
        self.is_game_over = False
        self.winner = None
        
        # Initialize renderer
        self.renderer = GameRenderer()

    def handle_events(self):
        """Handle input events and AI moves"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            # Handle mouse clicks - both for moves and restart
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.is_game_over:
                    self.__init__()  # Reset game
                    return True
                
                if self.current_player == PLAYER_X:
                    x, y = pygame.mouse.get_pos()
                    row = y // CELL_SIZE
                    col = x // CELL_SIZE
                    if self.make_move(row, col):
                        self.check_game_over()
                        self.switch_player()

        # Handle AI moves
        if not self.is_game_over and self.current_player == PLAYER_O:
            current_time = pygame.time.get_ticks()
            # if current_time - self.last_ai_move >= self.ai_delay:
            row, col = self.ai.use_alpha_beta(self.board)
            if self.make_move(row, col):
                # self.last_ai_move = current_time
                self.check_game_over()
                self.switch_player()

        return True

    def make_move(self, row, col):
        """Attempt to make a move at the specified position"""
        return self.board.update(row, col, self.current_player)

    def switch_player(self):
        """Switch between human and AI players"""
        self.current_player = PLAYER_O if self.current_player == PLAYER_X else PLAYER_X

    def check_game_over(self):
        """Check if the game has ended"""
        self.winner = self.board.check_winner()
        if self.winner or self.board.is_full():
            self.is_game_over = True

    def render(self, screen):
        """Render the current game state"""
        self.renderer.render_game(screen, self)