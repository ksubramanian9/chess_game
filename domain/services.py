# services.py

from copy import deepcopy
from domain.piece import Color, PieceType

class MovementService:
    """
    A 'fully' implemented MovementService that covers:
      - Basic piece movement (pawn, knight, bishop, rook, queen, king)
      - Captures
      - Checking for checks
      - Basic checkmate detection
    Does NOT handle all advanced rules (castling, en passant, underpromotion, etc.).
    """

    def is_valid_move(self, game, from_square, to_square):
        """
        Checks if the move from 'from_square' to 'to_square' is valid according 
        to standard chess movement rules, and does not leave the moving player's 
        own king in check.
        
        :param game: The Game entity containing board and current player
        :param from_square: (row, col)
        :param to_square: (row, col)
        :return: True if valid, otherwise False
        """
        board = game.board
        (fr, fc) = from_square
        (tr, tc) = to_square

        # Check if squares are in range
        if not self._in_bounds(fr, fc) or not self._in_bounds(tr, tc):
            return False

        piece = board.get_piece(fr, fc)
        if piece is None:
            return False

        # Check if it's the correct player's turn
        if piece.color != game.current_player:
            return False

        # If target square has a piece of the same color, invalid
        target_piece = board.get_piece(tr, tc)
        if target_piece and target_piece.color == piece.color:
            return False

        # Check if move is valid for that piece type or via en passant
        if not self._can_move_piece(piece, from_square, to_square, board, game):
            # Special case: en passant capture
            if not self._is_en_passant(game, piece, from_square, to_square):
                return False

        # Additional castling-specific checks
        if piece.piece_type == PieceType.KING and abs(tc - fc) == 2:
            # King cannot castle out of or through check
            if self._is_in_check(board, piece.color):
                return False
            step = 1 if tc > fc else -1
            if self._would_leave_king_in_check(game, from_square, (fr, fc + step)):
                return False

        # Check if the move leaves our king in check
        if self._would_leave_king_in_check(game, from_square, to_square):
            return False

        return True

    def is_checkmate(self, game):
        """
        Returns True if the current player's king is in checkmate.
        Otherwise, False.

        The logic:
          1. Check if current player's king is in check.
          2. If not in check, return False.
          3. If in check, see if there's ANY legal move that can remove the check.
        """
        board = game.board
        color = game.current_player

        # If king is not in check, can't be checkmate
        if not self._is_in_check(board, color):
            return False

        # Try every possible move to see if it removes check
        for row in range(8):
            for col in range(8):
                piece = board.get_piece(row, col)
                if piece and piece.color == color:
                    from_square = (row, col)

                    # Check all squares on the board as potential moves
                    for to_row in range(8):
                        for to_col in range(8):
                            to_square = (to_row, to_col)
                            # Create a "fake" move to see if it's valid
                            if self.is_valid_move(game, from_square, to_square):
                                # Simulate the move
                                temp_game = self._simulate_move(game, from_square, to_square)
                                # If after this move, the king is not in check, it's not checkmate
                                if not self._is_in_check(temp_game.board, color):
                                    return False
        return True

    # -------------------------------------------------------------------------
    #                          INTERNAL / HELPER METHODS
    # -------------------------------------------------------------------------
    def _can_move_piece(self, piece, from_square, to_square, board, game=None):
        """
        Returns True if the piece can move from 'from_square' to 'to_square'
        ignoring check-scenarios. Strictly piece movement logic + path checking.
        """
        (fr, fc) = from_square
        (tr, tc) = to_square
        piece_type = piece.piece_type

        # General direction/offset
        row_diff = tr - fr
        col_diff = tc - fc
        abs_row_diff = abs(row_diff)
        abs_col_diff = abs(col_diff)

        if piece_type == PieceType.PAWN:
            return self._can_move_pawn(piece, from_square, to_square, board)

        elif piece_type == PieceType.KNIGHT:
            # Knight moves in an 'L': 2 in one direction, 1 in the other
            return (abs_row_diff, abs_col_diff) in [(2, 1), (1, 2)]

        elif piece_type == PieceType.BISHOP:
            # Bishop moves diagonally
            if abs_row_diff == abs_col_diff:
                return self._is_path_clear(board, from_square, to_square)
            return False

        elif piece_type == PieceType.ROOK:
            # Rook moves horizontally or vertically
            if (fr == tr) or (fc == tc):
                return self._is_path_clear(board, from_square, to_square)
            return False

        elif piece_type == PieceType.QUEEN:
            # Queen = Rook or Bishop
            if (fr == tr) or (fc == tc) or (abs_row_diff == abs_col_diff):
                return self._is_path_clear(board, from_square, to_square)
            return False

        elif piece_type == PieceType.KING:
            # King can move 1 square in any direction
            if abs_row_diff <= 1 and abs_col_diff <= 1:
                return True

            # Castling logic: king moves two squares horizontally and neither
            # king nor rook have moved and the path is clear.
            if abs_row_diff == 0 and abs_col_diff == 2 and not piece.has_moved:
                rook_col = 0 if tc < fc else 7
                rook = board.get_piece(fr, rook_col)
                if rook and rook.piece_type == PieceType.ROOK and not rook.has_moved:
                    step = -1 if tc < fc else 1
                    for c in range(fc + step, rook_col, step):
                        if board.get_piece(fr, c) is not None:
                            return False
                    return True
            return False

        return False

    def _can_move_pawn(self, piece, from_square, to_square, board):
        """
        Pawn move logic (basic). 
        DOES NOT handle en passant or promotion in detail.
        """
        (fr, fc) = from_square
        (tr, tc) = to_square
        row_diff = tr - fr
        col_diff = tc - fc
        target_piece = board.get_piece(tr, tc)

        direction = -1 if piece.color == Color.WHITE else 1  # White moves up (row decreases), Black down

        # 1. Move forward (no capture)
        #    - One square forward
        if col_diff == 0 and row_diff == direction and target_piece is None:
            return True

        # 2. Two squares forward from initial rank
        #    - White from row=6, Black from row=1
        #    - Must be clear path, and no capture
        if col_diff == 0 and ((piece.color == Color.WHITE and fr == 6 and row_diff == -2) or
                              (piece.color == Color.BLACK and fr == 1 and row_diff == 2)):
            if target_piece is None:
                # Check the square in between is empty too
                mid_row = fr + (direction)
                if board.get_piece(mid_row, fc) is None:
                    return True

        # 3. Capture move (diagonals)
        if abs(col_diff) == 1 and row_diff == direction and target_piece is not None:
            # Opponent piece
            return target_piece.color != piece.color

        return False

    def _is_en_passant(self, game, piece, from_square, to_square):
        """Check if the pawn move is a valid en passant capture."""
        if piece.piece_type != PieceType.PAWN:
            return False
        (fr, fc) = from_square
        (tr, tc) = to_square
        row_diff = tr - fr
        col_diff = tc - fc

        direction = -1 if piece.color == Color.WHITE else 1

        # Must be moving diagonally one square to an empty square
        if abs(col_diff) != 1 or row_diff != direction:
            return False
        if game.board.get_piece(tr, tc) is not None:
            return False

        last = getattr(game, "last_move", None)
        if not last:
            return False
        last_piece, last_from, last_to = last
        if last_piece.piece_type != PieceType.PAWN:
            return False
        if last_piece.color == piece.color:
            return False
        # Last move must be a two-square pawn advance ending adjacent to the capturing pawn
        if abs(last_to[0] - last_from[0]) != 2:
            return False
        if last_to[0] != fr or last_to[1] != tc:
            return False
        return True

    def _is_path_clear(self, board, from_square, to_square):
        """
        Checks if all squares between 'from_square' and 'to_square' are empty 
        (does not check 'to_square' because capturing an opponent is allowed).
        For bishops, rooks, queens.
        """
        (fr, fc) = from_square
        (tr, tc) = to_square

        row_step = (tr - fr)
        col_step = (tc - fc)

        # Normalize to direction -1, 0, or 1
        if row_step != 0:
            row_step = row_step // abs(row_step)
        if col_step != 0:
            col_step = col_step // abs(col_step)

        current_r = fr + row_step
        current_c = fc + col_step

        while (current_r, current_c) != (tr, tc):
            if board.get_piece(current_r, current_c) is not None:
                return False
            current_r += row_step
            current_c += col_step

        return True

    def _would_leave_king_in_check(self, game, from_square, to_square):
        """
        Simulate the move and check if the current player's king is in check afterwards.
        """
        simulated_game = self._simulate_move(game, from_square, to_square)
        return self._is_in_check(simulated_game.board, game.current_player)

    def _is_in_check(self, board, color):
        """
        Checks if 'color' player's king is in check.
        That means there's an opponent piece that can capture the king next move.
        """
        # 1. Find king position
        king_pos = self._find_king(board, color)
        if not king_pos:
            return False  # Shouldn't happen in a real game, but let's just say not in check

        # 2. For each enemy piece, check if it can move to king position
        for row in range(8):
            for col in range(8):
                piece = board.get_piece(row, col)
                if piece and piece.color != color:
                    if self._can_move_piece(piece, (row, col), king_pos, board):
                        # Also need to check if path is clear (for rook, bishop, queen).
                        # For a direct capture, we ignore if the king is there, but let's do the same path check:
                        if piece.piece_type in [PieceType.ROOK, PieceType.BISHOP, PieceType.QUEEN]:
                            if not self._is_path_clear(board, (row, col), king_pos):
                                continue
                        return True
        return False

    def _simulate_move(self, game, from_square, to_square):
        """
        Returns a *deep copy* of the game with the move applied.
        This way we can check for hypothetical scenarios (like check).
        """
        new_game = deepcopy(game)
        new_board = new_game.board

        (fr, fc) = from_square
        (tr, tc) = to_square

        piece = new_board.grid[fr][fc]
        new_board.grid[fr][fc] = None
        # Handle en passant in simulation
        if self._is_en_passant(game, piece, from_square, to_square):
            capture_row = fr
            capture_col = tc
            new_board.grid[capture_row][capture_col] = None

        new_board.grid[tr][tc] = piece

        # Record last move in the simulated game
        new_game.last_move = (piece, from_square, to_square)

        # Switch player in the simulated game
        new_game._switch_player()  # or however your real code does it
        return new_game

    def _find_king(self, board, color):
        """
        Find the square (row, col) of the king of 'color'.
        """
        for row in range(8):
            for col in range(8):
                piece = board.get_piece(row, col)
                if piece and piece.color == color and piece.piece_type == PieceType.KING:
                    return (row, col)
        return None

    def _in_bounds(self, r, c):
        """
        Utility to check if a square is within the 8x8 board.
        """
        return 0 <= r < 8 and 0 <= c < 8
