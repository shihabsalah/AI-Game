def get_best_move(board, player):
    best_score = float('-inf')
    best_move = None
    
    for row in range(3):
        for col in range(3):
            if board.board[row][col] is None:
                board.board[row][col] = player
                score = minimax(board, 0, False, player)
                board.board[row][col] = None
                
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    
    return best_move

def minimax(board, depth, is_maximizing, ai_player):
    human_player = 'X' if ai_player == 'O' else 'O'
    
    # Terminal states
    winner = board.check_winner()
    if winner == ai_player:
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
                    board.board[row][col] = ai_player
                    score = minimax(board, depth + 1, False, ai_player)
                    board.board[row][col] = None
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(3):
            for col in range(3):
                if board.board[row][col] is None:
                    board.board[row][col] = human_player
                    score = minimax(board, depth + 1, True, ai_player)
                    board.board[row][col] = None
                    best_score = min(score, best_score)
        return best_score
