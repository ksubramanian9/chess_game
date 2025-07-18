from adapters.file_game_repository import FileGameRepository
from adapters.pygame_ui import PygameChessUI
from application.use_cases import StartGameUseCase, MovePieceUseCase
from domain.services import MovementService

def main():
    # Setup
    game_repository = FileGameRepository()
    movement_service = MovementService()
    ui = PygameChessUI()

    start_game_uc = StartGameUseCase(game_repository)
    move_piece_uc = MovePieceUseCase(game_repository, movement_service)

    game_id = None
    saved_games = game_repository.list_game_ids()
    if saved_games:
        print("Saved games:")
        for idx, gid in enumerate(saved_games, 1):
            print(f"{idx}. {gid}")
        choice = input("Select game number to load or press Enter for new game: ")
        if choice.isdigit() and 1 <= int(choice) <= len(saved_games):
            game_id = saved_games[int(choice)-1]

    if not game_id:
        game_id = start_game_uc.execute()

    running = True
    selected_square = None

    while running:
        game = game_repository.find_by_id(game_id)
        ui.draw_board(game)
        
        # Get a square selection from player
        square = ui.get_player_input(game.current_player)

        if selected_square is None:
            selected_square = square
        else:
            # Attempt to move from selected_square to square
            try:
                move_piece_uc.execute(game_id, selected_square, square)
            except Exception as ex:
                ui.show_message(str(ex))
            selected_square = None

        # If the game ended, you might break or show a winner screen, etc.
        if game.status == 'CHECKMATE':
            print("Checkmate! " + game.current_player + " loses.")
            running = False

if __name__ == "__main__":
    main()
