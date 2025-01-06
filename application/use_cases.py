# use_cases.py

from domain.board import Board
from domain.piece import Piece, Color, PieceType
from domain.game import Game
from domain.services import MovementService

class StartGameUseCase:
    """
    Sets up a new Game with all pieces in standard positions and returns a game_id.
    """
    def __init__(self, game_repository):
        self.game_repository = game_repository

    def execute(self):
        board = self._create_initial_board()
        game = Game(board, Color.WHITE)  # White moves first
        game_id = self.game_repository.save(game)
        return game_id

    def _create_initial_board(self):
        board = Board()

        # --- Place Black pieces (top side) ---
        # Row 0: R, N, B, Q, K, B, N, R
        board.place_piece(0, 0, Piece(Color.BLACK, PieceType.ROOK))
        board.place_piece(0, 1, Piece(Color.BLACK, PieceType.KNIGHT))
        board.place_piece(0, 2, Piece(Color.BLACK, PieceType.BISHOP))
        board.place_piece(0, 3, Piece(Color.BLACK, PieceType.QUEEN))
        board.place_piece(0, 4, Piece(Color.BLACK, PieceType.KING))
        board.place_piece(0, 5, Piece(Color.BLACK, PieceType.BISHOP))
        board.place_piece(0, 6, Piece(Color.BLACK, PieceType.KNIGHT))
        board.place_piece(0, 7, Piece(Color.BLACK, PieceType.ROOK))

        # Row 1: Pawns
        for col in range(8):
            board.place_piece(1, col, Piece(Color.BLACK, PieceType.PAWN))

        # --- Place White pieces (bottom side) ---
        # Row 7: R, N, B, Q, K, B, N, R
        board.place_piece(7, 0, Piece(Color.WHITE, PieceType.ROOK))
        board.place_piece(7, 1, Piece(Color.WHITE, PieceType.KNIGHT))
        board.place_piece(7, 2, Piece(Color.WHITE, PieceType.BISHOP))
        board.place_piece(7, 3, Piece(Color.WHITE, PieceType.QUEEN))
        board.place_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        board.place_piece(7, 5, Piece(Color.WHITE, PieceType.BISHOP))
        board.place_piece(7, 6, Piece(Color.WHITE, PieceType.KNIGHT))
        board.place_piece(7, 7, Piece(Color.WHITE, PieceType.ROOK))

        # Row 6: Pawns
        for col in range(8):
            board.place_piece(6, col, Piece(Color.WHITE, PieceType.PAWN))

        return board


class MovePieceUseCase:
    """
    Tries to move a piece from 'from_square' to 'to_square'.
    Leverages the MovementService to check if the move is valid,
    then updates the game state accordingly.
    """
    def __init__(self, game_repository, movement_service=None):
        self.game_repository = game_repository
        # If no movement_service is passed in, create a default one.
        self.movement_service = movement_service or MovementService()

    def execute(self, game_id, from_square, to_square):
        """
        from_square, to_square are tuples like (row, col).
        """
        game = self.game_repository.find_by_id(game_id)
        if not game:
            raise Exception(f"Game with id={game_id} not found.")

        # Validate the move
        if not self.movement_service.is_valid_move(game, from_square, to_square):
            raise Exception("Invalid move")

        # Perform the move
        game.move_piece(from_square, to_square)

        # Check if it’s checkmate
        if self.movement_service.is_checkmate(game):
            game.status = 'CHECKMATE'

        # Save updated game
        self.game_repository.save(game)
        return game
