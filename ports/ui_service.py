from abc import ABC, abstractmethod

class ChessUIService(ABC):
    @abstractmethod
    def draw_board(self, game):
        pass

    @abstractmethod
    def get_player_input(self, current_player):
        pass
