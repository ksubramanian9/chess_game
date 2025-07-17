import uuid
import pickle
from pathlib import Path
from ports.game_repository import GameRepository

class FileGameRepository(GameRepository):
    """Persist games to disk using pickle serialization."""
    def __init__(self, directory="saved_games"):
        self.directory = Path(directory)
        self.directory.mkdir(exist_ok=True)

    def save(self, game):
        game_id = getattr(game, 'id', None)
        if not game_id:
            game_id = str(uuid.uuid4())
            setattr(game, 'id', game_id)
        file_path = self.directory / f"{game_id}.pkl"
        with open(file_path, 'wb') as f:
            pickle.dump(game, f)
        return game_id

    def find_by_id(self, game_id):
        file_path = self.directory / f"{game_id}.pkl"
        if not file_path.exists():
            return None
        with open(file_path, 'rb') as f:
            game = pickle.load(f)
        return game

    def list_game_ids(self):
        return [p.stem for p in self.directory.glob('*.pkl')]
