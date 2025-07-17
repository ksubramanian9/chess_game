from abc import ABC, abstractmethod

class GameRepository(ABC):
    @abstractmethod
    def save(self, game):
        pass

    @abstractmethod
    def find_by_id(self, game_id):
        pass

    @abstractmethod
    def list_game_ids(self):
        """Return a list of saved game IDs."""
        pass
