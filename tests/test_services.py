# test_services.py

import unittest

from copy import deepcopy

# Assuming your code is structured like:
# from chess_game.domain.board import Board
# from chess_game.domain.game import Game
# from chess_game.domain.piece import Piece, PieceType, Color
# from chess_game.domain.services import MovementService

# For this example, we'll pretend they're imported as follows:
from domain.board import Board
from domain.game import Game
from domain.piece import Piece, PieceType, Color
from domain.services import MovementService

class TestMovementService(unittest.TestCase):
    def setUp(self):
        """
        Create a fresh board and MovementService for each test.
        """
        self.board = Board()
        self.movement_service = MovementService()
        # We'll create a game with White to move by default
        self.game = Game(self.board, Color.WHITE)
    
    def test_white_pawn_single_step_forward(self):
        """
        White pawn at row=6, col=0 should move to row=5, col=0 if empty.
        """
        # Place a white pawn on the board
        self.board.place_piece(6, 0, Piece(Color.WHITE, PieceType.PAWN))
        from_square = (6, 0)
        to_square = (5, 0)

        # Should be valid
        self.assertTrue(self.movement_service.is_valid_move(self.game, from_square, to_square))

    def test_white_pawn_double_step_forward_initial(self):
        """
        White pawn on row=6 can move to row=4 if both row=5 and row=4 are empty.
        """
        self.board.place_piece(6, 0, Piece(Color.WHITE, PieceType.PAWN))
        from_square = (6, 0)
        to_square = (4, 0)

        # Should be valid
        self.assertTrue(self.movement_service.is_valid_move(self.game, from_square, to_square))

    def test_white_pawn_capture_diagonally(self):
        """
        White pawn can capture a black piece diagonally.
        """
        self.board.place_piece(6, 0, Piece(Color.WHITE, PieceType.PAWN))
        self.board.place_piece(5, 1, Piece(Color.BLACK, PieceType.PAWN))

        from_square = (6, 0)
        to_square = (5, 1)

        # Should be valid (diagonal capture)
        self.assertTrue(self.movement_service.is_valid_move(self.game, from_square, to_square))

    def test_white_pawn_cannot_capture_forward(self):
        """
        Pawn cannot capture straight ahead if there's an opponent piece directly in front.
        """
        self.board.place_piece(6, 0, Piece(Color.WHITE, PieceType.PAWN))
        # Put a black pawn directly in front
        self.board.place_piece(5, 0, Piece(Color.BLACK, PieceType.PAWN))

        from_square = (6, 0)
        to_square = (5, 0)

        # Should be invalid (pawns don't capture forward)
        self.assertFalse(self.movement_service.is_valid_move(self.game, from_square, to_square))

    def test_rook_horizontal_move(self):
        """
        Rook at (7,0) can move horizontally if path is clear.
        """
        self.board.place_piece(7, 0, Piece(Color.WHITE, PieceType.ROOK))
        from_square = (7, 0)
        to_square = (7, 5)

        # Path is clear
        self.assertTrue(self.movement_service.is_valid_move(self.game, from_square, to_square))

    def test_rook_cannot_move_through_piece(self):
        """
        Rook cannot jump over pieces. If blocked, move should be invalid.
        """
        self.board.place_piece(7, 0, Piece(Color.WHITE, PieceType.ROOK))
        # Place a piece in the path
        self.board.place_piece(7, 2, Piece(Color.WHITE, PieceType.PAWN))

        from_square = (7, 0)
        to_square = (7, 5)

        # Should fail because a friendly pawn at (7,2) blocks the rook
        self.assertFalse(self.movement_service.is_valid_move(self.game, from_square, to_square))

    def test_knight_can_jump_over_pieces(self):
        """
        Knights can jump over pieces.
        """
        self.board.place_piece(7, 1, Piece(Color.WHITE, PieceType.KNIGHT))
        # Place some pieces in the 'path'
        self.board.place_piece(6, 1, Piece(Color.WHITE, PieceType.PAWN))
        self.board.place_piece(5, 1, Piece(Color.WHITE, PieceType.PAWN))

        from_square = (7, 1)
        to_square = (5, 2)  # L-shaped move

        self.assertTrue(self.movement_service.is_valid_move(self.game, from_square, to_square))

    def test_bishop_diagonal_move(self):
        """
        Bishop moves diagonally if path is clear.
        """
        self.board.place_piece(7, 2, Piece(Color.WHITE, PieceType.BISHOP))
        from_square = (7, 2)
        to_square = (4, 5)  # up-right diagonal

        self.assertTrue(self.movement_service.is_valid_move(self.game, from_square, to_square))

    def test_king_one_square(self):
        """
        King can move only one square in any direction.
        """
        self.board.place_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        from_square = (7, 4)
        # Move 2 squares should fail
        to_square_far = (5, 4)
        self.assertFalse(self.movement_service.is_valid_move(self.game, from_square, to_square_far))

        # Move 1 square should pass
        to_square_close = (6, 4)
        self.assertTrue(self.movement_service.is_valid_move(self.game, from_square, to_square_close))

    def test_move_would_leave_king_in_check(self):
        """
        If moving a piece away exposes our king to an opposing rook, it should be invalid.
        """
        # White king at (7,4), White rook at (7,0), Black rook at (7,7)
        # If we move the White rook away from the 7th rank, the black rook directly checks the king.
        self.board.place_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        self.board.place_piece(7, 0, Piece(Color.WHITE, PieceType.ROOK))
        self.board.place_piece(7, 7, Piece(Color.BLACK, PieceType.ROOK))

        from_square = (7, 0)
        to_square = (6, 0)  # Rook moves up, leaving king exposed
        self.assertFalse(self.movement_service.is_valid_move(self.game, from_square, to_square))

    def test_check_detection(self):
        """
        If a black rook can capture the white king, white king is in check.
        """
        # White king at (7,4); black rook at (7,7)
        self.board.place_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        self.board.place_piece(7, 7, Piece(Color.BLACK, PieceType.ROOK))

        # White to move, but let's directly check if White is in check
        self.assertTrue(self.movement_service._is_in_check(self.board, Color.WHITE))

    def test_checkmate_scenario(self):
        """
        A simple checkmate scenario:
          - White king cornered at (7,4)
          - Black rook at (7,7)
          - White cannot move any piece to escape check
        For simplicity, we remove other pieces so there's no way to block/capture.
        """
        # White king in corner
        self.board.grid = [[None for _ in range(8)] for _ in range(8)]
        self.board.place_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        self.board.place_piece(7, 7, Piece(Color.BLACK, PieceType.ROOK))

        # It's White's turn and the king is in line of the rook. 
        # The king has no squares to move that aren't also in the rook's line or off board.
        self.assertTrue(self.movement_service._is_in_check(self.board, Color.WHITE))
        self.assertFalse(self.movement_service.is_checkmate(self.game))

        # If we nudge the king to (6,4) and it's not in line with the rook, 
        # checkmate would no longer apply. Let's confirm that fails:
        self.board.grid[7][4] = None
        self.board.grid[6][4] = Piece(Color.WHITE, PieceType.KING)
        # Now the rook is not attacking the king directly
        self.assertFalse(self.movement_service._is_in_check(self.board, Color.WHITE))
        self.assertTrue(self.movement_service.is_checkmate(self.game))


if __name__ == '__main__':
    unittest.main()
