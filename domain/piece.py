WHITE_PIECES = {
    'K': '♔',  # King
    'Q': '♕',  # Queen
    'R': '♖',  # Rook
    'B': '♗',  # Bishop
    'N': '♘',  # Knight
    'P': '♙',  # Pawn
}

BLACK_PIECES = {
    'K': '♚',  # King
    'Q': '♛',  # Queen
    'R': '♜',  # Rook
    'B': '♝',  # Bishop
    'N': '♞',  # Knight
    'P': '♟',  # Pawn
}

class Color:
    WHITE = 'WHITE'
    BLACK = 'BLACK'

class PieceType:
    KING = 'K'
    QUEEN = 'Q'
    ROOK = 'R'
    BISHOP = 'B'
    KNIGHT = 'N'
    PAWN = 'P'

class Piece:
    def __init__(self, color, piece_type):
        self.color = color
        self.piece_type = piece_type

    @property
    def unicode_symbol(self):
        if self.color == Color.WHITE:
            return WHITE_PIECES[self.piece_type]
        else:
            return BLACK_PIECES[self.piece_type]
