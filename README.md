# Ultimate Tic-Tac-Toe

A web-based two-player Ultimate Tic-Tac-Toe game built with Python and Flask. The game uses a 3×3 big board where each square contains its own 3×3 Tic-Tac-Toe miniboard.

## How to Play

The game begins with X, who may play in any cell on any miniboard.

After the first move, the cell a player chooses determines which miniboard the next player must play in. For example, if X plays in the top-right cell of a miniboard, O must make their next move in the top-right miniboard of the big board.

If a player is sent to a miniboard that has already been won or tied, they may instead play in any unfinished miniboard.

Winning a miniboard requires getting three marks in a row, just like regular Tic-Tac-Toe. A won miniboard becomes a large X or O on the big board. If a miniboard fills without a winner, it becomes a tie and does not belong to either player.

The overall game is won by claiming three miniboards in a row on the big board. If all nine miniboards finish without either player getting three in a row, the overall game ends in a tie.

## Features

- Web-based 9×9 playing interface
- Clickable Tic-Tac-Toe cells
- Forced-miniboard move system
- Visual highlighting of currently playable miniboards
- User-facing miniboard numbering from 1–9
- Miniboard win and tie detection
- Animated winning lines for miniboard victories
- Large X, O, and TIE displays for completed miniboards
- Overall game win and tie detection
- Persistent animated winning line for overall victories
- Blue X and red O visual styling
- Color-coded turn indicator
- Running score for X, O, and ties
- Play Again option that resets the board while preserving the score
- Game state preserved when the browser page is refreshed
- Automated tests for game logic and web application behavior

## Requirements

- Python 3.14 or newer
- uv

Flask is used to provide the web application.

## Running the Game

Clone the repository and enter the project directory.

Install the project dependencies:

```bash
uv sync
```

Start the web application:

```bash
uv run tictactoe
```

Then open the following address in a web browser:

```text
http://127.0.0.1:5000
```

Press `Ctrl+C` in the terminal to stop the server.

## Running the Tests

Run the complete automated test suite with:

```bash
uv run pytest -v
```

## Project Structure

```text
src/
└── tictactoe/
    ├── __init__.py
    ├── game.py
    ├── web.py
    ├── templates/
    │   └── index.html
    └── static/
        ├── style.css
        └── game.js

tests/
├── test_game.py
└── test_web.py
```

`game.py` contains the core Ultimate Tic-Tac-Toe game logic.

`web.py` contains the Flask web application and routes.

`templates/index.html` contains the structure of the web interface.

`static/style.css` contains the visual styling and winning-line animations.

`static/game.js` handles browser interaction with the Flask server and updates the game interface.

The `tests` directory contains automated tests for the game logic and web application behavior.