import uuid
from ports.game_repository import GameRepository

class InMemoryGameRepository(GameRepository):
    def __init__(self):
        self.storage = {}

    def save(self, game):
        # either generate new ID or use existing
        game_id = getattr(game, 'id', None)
        if not game_id:
            game_id = str(uuid.uuid4())
            setattr(game, 'id', game_id)
        self.storage[game_id] = game
        return game_id

    def find_by_id(self, game_id):
        return self.storage.get(game_id, None)

    def list_game_ids(self):
        return list(self.storage.keys())
