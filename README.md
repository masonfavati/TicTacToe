# Ultimate Tic-Tac-Toe

A graphical two-player Tic-Tac-Toe game built with Python and Tkinter. The game uses a 3×3 big board where each square contains its own 3×3 Tic-Tac-Toe miniboard.

## How to Play

The game begins with X, who may play in any cell on any miniboard.

After the first move, the cell a player chooses determines which miniboard the next player must play in. For example, if X plays in the top-right cell of a miniboard, O must make their next move in the top-right miniboard of the big board.

If a player is sent to a miniboard that has already been won or tied, they may instead play in any unfinished miniboard.

Winning a miniboard requires getting three marks in a row, just like regular Tic-Tac-Toe. A won miniboard becomes a large X or O on the big board. If a miniboard fills without a winner, it becomes a tie and does not belong to either player.

The overall game is won by claiming three miniboards in a row on the big board. If all nine miniboards finish without either player getting three in a row, the overall game ends in a tie.

## Features

- Graphical 9×9 playing interface
- Clickable Tic-Tac-Toe cells
- Forced-miniboard move system
- Miniboard win and tie detection
- Overall game win and tie detection
- Visual X, O, and TIE displays for completed miniboards
- Running score for X, O, and ties
- Play-again option that resets the board while preserving the score
- Automated tests for game logic and GUI behavior

## Requirements

- Python 3.14 or newer
- uv

Tkinter is used for the graphical interface.

## Running the Game

Clone the repository and enter the project directory.

Install the project dependencies:

```bash
uv sync
```

Run the game:

```bash
uv run tictactoe
```

## Running the Tests

Run the complete test suite with:

```bash
uv run pytest -v
```

## Project Structure

`game.py` contains the game rules and state management.

`gui.py` contains the Tkinter graphical interface and connects player clicks to the game logic.

`__init__.py` provides the application's entry point.

The `tests` directory contains automated tests for the game logic and graphical application behavior.