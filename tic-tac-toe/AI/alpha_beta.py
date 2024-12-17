class AlphaBeta:
    def __init__(self, player):
        self.player = player

    def get_best_move(self, board):
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')

        for row in range(3):
            for col in range(3):
                if board.board[row][col] is None:
                    board.board[row][col] = self.player
                    score = self.minimax(board, 0, False, alpha, beta)
                    board.board[row][col] = None

                    if score > best_score:
                        best_score = score
                        best_move = (row, col)

        return best_move

    def minimax(self, board, depth, is_maximizing, alpha, beta):
        human_player = 'X' if self.player == 'O' else 'O'

        winner = board.check_winner()
        if winner == self.player:
            return 1
        elif winner == human_player:
            return -1
        elif board.is_full():
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for row in range(3):
                for col in range(3):
                    if board.board[row][col] is None:
                        board.board[row][col] = self.player
                        score = self.minimax(board, depth + 1, False, alpha, beta)
                        board.board[row][col] = None
                        best_score = max(score, best_score)
                        alpha = max(alpha, score)
                        if beta <= alpha:
                            break
            return best_score
        else:
            best_score = float('inf')
            for row in range(3):
                for col in range(3):
                    if board.board[row][col] is None:
                        board.board[row][col] = human_player
                        score = self.minimax(board, depth + 1, True, alpha, beta)
                        board.board[row][col] = None
                        best_score = min(score, best_score)
                        beta = min(beta, score)
                        if beta <= alpha:
                            break
            return best_score