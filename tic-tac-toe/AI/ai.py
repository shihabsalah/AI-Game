from AI.minmax import Minimax
from AI.alpha_beta import AlphaBeta

class AI:
    def __init__(self, symbol):
        self.symbol = symbol
        self.opponent = 'X' if symbol == 'O' else 'O'
        self.minimax = Minimax(symbol)
        self.alpha_beta = AlphaBeta(symbol)
    

    def use_alpha_beta(self, board):
        return self.alpha_beta.get_best_move(board)

    def use_minimax(self, board):
        return self.minimax.get_best_move(board)
