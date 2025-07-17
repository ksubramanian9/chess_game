# Chess Game (DDD + Hexagonal Architecture)

This repository contains a 2-player chess game built in **Python**, leveraging **Domain-Driven Design (DDD)** and a **Hexagonal (Ports and Adapters) architecture**. It uses **Pygame** for the graphical user interface and **Unicode characters** to represent chess pieces.

## Table of Contents

1. [Overview](#overview)
2. [Project Structure](#project-structure)  
3. [Installation](#installation)  
4. [Running the Game](#running-the-game)  
5. [How It Works](#how-it-works)  
   - [Domain Layer](#domain-layer)  
   - [Application Layer (Use Cases)](#application-layer-use-cases)  
   - [Ports and Adapters](#ports-and-adapters)  
   - [Pygame UI](#pygame-ui)  
6. [Next Steps](#next-steps)  
7. [License](#license)

---

## Overview

The goal of this project is to demonstrate how **DDD** and **Hexagonal Architecture** can help keep your chess game’s logic well-organized, testable, and maintainable. The code is separated into clear layers:

1. **Domain Layer** – Encapsulates core chess logic (entities, value objects, services).  
2. **Application Layer** – Coordinates use cases like starting a game or making a move.  
3. **Ports and Adapters** – Connects the domain to external concerns (e.g., Pygame UI, repositories).

### Key Features

- **DDD** organization: Entities (Piece, Board, Game), Value Objects (Square, Move), and a `MovementService` for rules.  
- **Hexagonal Architecture**: Ports (interfaces) and Adapters (in-memory repository, Pygame UI).  
- **Pygame** rendering: Renders an 8×8 board with colored tiles and Unicode chess pieces.  
- **Use Cases**:  
  - **StartGameUseCase** – sets up initial pieces and returns a game ID.  
  - **MovePieceUseCase** – validates and executes a requested move.  
- **Unicode Pieces**: White pieces (`♔♕♖♗♘♙`), Black pieces (`♚♛♜♝♞♟`).

---

## Project Structure

- **`domain/`**: Contains the core entities (`Board`, `Piece`, `Game`), value objects, and domain services (e.g. `MovementService`).
- **`application/`**: Contains the **use cases** or **application services** (e.g. `StartGameUseCase`, `MovePieceUseCase`).
- **`ports/`**: Contains definitions for **interfaces** (e.g. `GameRepository`, `ChessUIService`).
- **`adapters/`**: Contains concrete **implementations** of those interfaces (e.g. `FileGameRepository`, `PygameChessUI`).
- **`main.py`**: Ties everything together and starts the game loop.

---
## Installation
1. **Clone** this repository to your local machine:
   ```bash
   git clone https://github.com/ksubramanian9/chess_game.git
   cd chess_game

2. Install dependencies (we assume Python 3.8+):
   ```bash
    pip install pygame

You may also set up a virtual environment if desired:
    
    python -m venv venv
    source venv/bin/activate  # (on macOS/Linux
    pip install pygame


Check that you have all standard library dependencies (like uuid, unittest, etc.). Typically, Python already includes them.

## Running the Game
From the project root, run:

    python main.py

This will:

1. Create a new game using StartGameUseCase.
2. Open a Pygame window showing the chessboard.
3. Allow basic user interaction to select two squares:
- First click is the piece you want to move.
- Second click is the destination square.

If everything is set up correctly, you’ll see an 8×8 board with Unicode pieces. You can make moves (though some advanced rules might not be fully implemented by default).
## How It Works
### Domain Layer
- **Piece** : Stores color (white/black), piece type (king, queen, etc.), and can return its Unicode symbol.
- **Board** : An 8×8 array that can place, move, and retrieve pieces.
- **Game** : The root entity storing the board, current player, and game status.
- **MovementService** : Contains the main chess rules logic (valid moves, check detection, checkmate detection, etc.).
### Application Layer (Use Cases)
- **StartGameUseCase** : Initializes a standard board layout with pawns and major pieces, saves it in a GameRepository, and returns the game_id.
- **MovePieceUseCase** : Validates a move (via MovementService) and, if valid, updates the Game. Also checks for check/checkmate.
### Ports and Adapters
- **GameRepository (port)**: Defines how we load/save a Game.
- **FileGameRepository (adapter)**: Stores games on disk using pickle files.
- **ChessUIService (port)**: Defines how we draw the board and handle user input.
- **PygameChessUI (adapter)**: Uses Pygame to draw squares, pieces, and detect mouse clicks.
### Pygame UI
- **Initialization**: Creates a window of 8×8 tiles.
- **Rendering**: Displays each piece using its Unicode character, centered in the tile.
- **Input**: Waits for user mouse clicks, converting screen coordinates to board squares (row, col)

## Next Steps

- **Advanced Chess Rules** : Implement castling, en passant, promotion choices, and draw mechanics (stalemate, threefold repetition).
- **AI** : Add a separate AI adapter that makes moves, or integrate a chess engine.
- **Persistence** : Swap out the in-memory repository for a database or file-based storage.
- **Network Play** : Create a network adapter to sync moves across players online.
- **Testing** : Enhance coverage with unit tests for domain logic (MovementService), integration tests for use cases, etc.

## License
MIT © 2023 Your Name or Company.

Feel free to use or modify this code to suit your needs. If you use it in a public project, we’d love to hear about it!

