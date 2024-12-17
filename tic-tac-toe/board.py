from constants import EMPTY, BOARD_SIZE

class Board:
    def __init__(self):
        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def update(self, row, col, player):
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and self.board[row][col] == EMPTY:
            self.board[row][col] = player
            return True
        return False
    
    def check_winner(self):
        # Check for a winner horizontally or vertically 
        for i in range(3):
            # Check horizontally
            if self.board[i][0] == self.board[i][1] == self.board[i][2] is not None:
                return self.board[i][0]
            # Check vertically 
            if self.board[0][i] == self.board[1][i] == self.board[2][i] is not None:
                return self.board[0][i]
        
        # Check diagonally
        if self.board[0][0] == self.board[1][1] == self.board[2][2] is not None:
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] is not None:
            return self.board[0][2]
        
        return None

    def is_full(self):
        return all(cell is not None for row in self.board for cell in row)
    
    def get_empty_cells(self):
        return [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) 
                if self.board[i][j] == EMPTY]