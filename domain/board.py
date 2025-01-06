class Board:
    def __init__(self):
        # 8x8, each entry either None or a Piece
        self.grid = [[None for _ in range(8)] for _ in range(8)]

    def place_piece(self, row, col, piece):
        self.grid[row][col] = piece
    
    def get_piece(self, row, col):
        return self.grid[row][col]
    
    def move_piece(self, from_row, from_col, to_row, to_col):
        piece = self.grid[from_row][from_col]
        self.grid[from_row][from_col] = None
        self.grid[to_row][to_col] = piece
