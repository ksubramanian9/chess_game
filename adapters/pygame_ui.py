import pygame
import sys
from ports.ui_service import ChessUIService

TILE_SIZE = 80
BOARD_SIZE = 8

WHITE_COLOR = (240, 217, 181)
BLACK_COLOR = (181, 136, 99)

class PygameChessUI(ChessUIService):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((TILE_SIZE*BOARD_SIZE, TILE_SIZE*BOARD_SIZE))
        pygame.display.set_caption("Chess - Hexagonal Architecture Demo")
        self.font = pygame.font.Font("dejavu-sans.book.ttf", 48)

    def draw_board(self, game):
        board = game.board
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                rect = (col*TILE_SIZE, row*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                color = WHITE_COLOR if (row+col) % 2 == 0 else BLACK_COLOR
                pygame.draw.rect(self.screen, color, rect)

                piece = board.get_piece(row, col)
                if piece:
                    text_surf = self.font.render(piece.unicode_symbol, True, (0, 0, 0))
                    text_rect = text_surf.get_rect(center=(col*TILE_SIZE + TILE_SIZE//2,
                                                           row*TILE_SIZE + TILE_SIZE//2))
                    self.screen.blit(text_surf, text_rect)
        pygame.display.flip()

    def get_player_input(self, current_player):
        # For simplicity, let's just do a basic event loop that waits for a click or keyboard
        # You could refine to handle board clicks
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Convert mouse click to board coordinates
                    x, y = pygame.mouse.get_pos()
                    col = x // TILE_SIZE
                    row = y // TILE_SIZE
                    # For demonstration, let's just return a single square
                    return (row, col)
