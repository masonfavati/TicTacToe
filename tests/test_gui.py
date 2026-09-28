import tkinter as tk
from unittest.mock import patch

from tictactoe.game import GameStatus
from tictactoe.gui import TicTacToeGUI

def test_x_win_increases_score_and_resets_game() -> None:
    root = tk.Tk()
    root.withdraw()

    gui = TicTacToeGUI(root)

    gui.game.status = GameStatus.X_WON

    with patch("tictactoe.gui.messagebox.askyesno", return_value=True):
        gui._finish_game()

    assert gui.x_score == 1
    assert gui.o_score == 0
    assert gui.tie_score == 0
    assert gui.game.status == GameStatus.PLAYING

    root.destroy()

def test_o_win_increases_score_and_resets_game() -> None:
    root = tk.Tk()
    root.withdraw()

    gui = TicTacToeGUI(root)

    gui.game.status = GameStatus.O_WON

    with patch("tictactoe.gui.messagebox.askyesno", return_value=True):
        gui._finish_game()

    assert gui.x_score == 0
    assert gui.o_score == 1
    assert gui.tie_score == 0
    assert gui.game.status == GameStatus.PLAYING

    root.destroy()

def test_tie_increases_tie_score_and_resets_game() -> None:
    root = tk.Tk()
    root.withdraw()

    gui = TicTacToeGUI(root)

    gui.game.status = GameStatus.TIED

    with patch("tictactoe.gui.messagebox.askyesno", return_value=True):
        gui._finish_game()

    assert gui.x_score == 0
    assert gui.o_score == 0
    assert gui.tie_score == 1
    assert gui.game.status == GameStatus.PLAYING

    root.destroy()

def test_scores_persist_between_games() -> None:
    root = tk.Tk()
    root.withdraw()

    gui = TicTacToeGUI(root)

    with patch("tictactoe.gui.messagebox.askyesno", return_value=True):
        gui.game.status = GameStatus.X_WON
        gui._finish_game()

        gui.game.status = GameStatus.O_WON
        gui._finish_game()

        gui.game.status = GameStatus.X_WON
        gui._finish_game()

        gui.game.status = GameStatus.TIED
        gui._finish_game()

    assert gui.x_score == 2
    assert gui.o_score == 1
    assert gui.tie_score == 1

    root.destroy()

def test_declining_play_again_closes_window() -> None:
    root = tk.Tk()
    root.withdraw()

    gui = TicTacToeGUI(root)
    gui.game.status = GameStatus.X_WON

    with patch("tictactoe.gui.messagebox.askyesno", return_value=False):
        gui._finish_game()

    assert gui.x_score == 1