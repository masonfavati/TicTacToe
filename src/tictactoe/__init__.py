import tkinter as tk

from tictactoe.gui import TicTacToeGUI


def main() -> None:
    root = tk.Tk()
    TicTacToeGUI(root)
    root.mainloop()