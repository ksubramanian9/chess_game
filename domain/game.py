class Game:
    def __init__(self, board, current_player):
        self.board = board
        self.current_player = current_player
        self.status = 'ONGOING'  # Could be ONGOING, CHECK, CHECKMATE, STALEMATE, etc.
        # Track the last move for rules like en passant. Stored as
        # (piece, from_square, to_square).
        self.last_move = None

    def move_piece(self, from_square, to_square):
        # from_square/to_square might be something like (row, col)
        (fr, fc) = from_square
        (tr, tc) = to_square
        piece = self.board.get_piece(fr, fc)

        # Handle en passant capture: if a pawn moves diagonally to an empty
        # square and the opponent's pawn made a two-step move to become
        # adjacent in the previous turn, remove that pawn.
        if (
            piece
            and piece.piece_type == 'P'
            and fc != tc
            and self.board.get_piece(tr, tc) is None
        ):
            capture_row = fr
            capture_col = tc
            self.board.grid[capture_row][capture_col] = None

        self.board.move_piece(fr, fc, tr, tc)

        # Handle castling: when king moves two squares horizontally,
        # move the corresponding rook as well.
        if piece and piece.piece_type == 'K' and abs(fc - tc) == 2:
            rook_from_col = 0 if tc < fc else 7
            rook_to_col = fc - 1 if tc < fc else fc + 1
            self.board.move_piece(fr, rook_from_col, fr, rook_to_col)

        # Record the move for future en passant checks
        if piece:
            self.last_move = (piece, from_square, to_square)
        self._switch_player()

    def _switch_player(self):
        if self.current_player == 'WHITE':
            self.current_player = 'BLACK'
        else:
            self.current_player = 'WHITE'
