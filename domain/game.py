class Game:
    def __init__(self, board, current_player):
        self.board = board
        self.current_player = current_player
        self.status = 'ONGOING'  # Could be ONGOING, CHECK, CHECKMATE, STALEMATE, etc.

    def move_piece(self, from_square, to_square):
        # from_square/to_square might be something like (row, col)
        (fr, fc) = from_square
        (tr, tc) = to_square
        self.board.move_piece(fr, fc, tr, tc)
        self._switch_player()

    def _switch_player(self):
        if self.current_player == 'WHITE':
            self.current_player = 'BLACK'
        else:
            self.current_player = 'WHITE'
