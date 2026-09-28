import tkinter as tk
from tkinter import messagebox

from tictactoe.game import BoardStatus, Game, GameStatus

class TicTacToeGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.game = Game()
        self.x_score = 0
        self.o_score = 0
        self.tie_score = 0
        self.cell_buttons: list[list[tk.Button]] = []
        self.miniboard_frames: list[tk.Frame] = []
        self.winner_labels: list[tk.Label | None] = [None] * 9

        self.root.title("Ultimate Tic-Tac-Toe")
        self.root.geometry("800x850")
        self.root.minsize(650, 700)

        self._build_interface()

    def _build_interface(self) -> None:
        title = tk.Label(
            self.root,
            text="Ultimate Tic-Tac-Toe",
            font=("Helvetica", 28, "bold"),
        )
        title.pack(pady=20)
        
        self.score_label = tk.Label(
            self.root,
            text="X: 0    O: 0    Ties: 0",
            font=("Helvetica", 16, "bold"),
        )
        self.score_label.pack(pady=(0, 10))

        self.status_label = tk.Label(
            self.root,
            text="",
            font=("Helvetica", 16),
        )
        self.status_label.pack(pady=(0, 15))

        board_frame = tk.Frame(self.root)
        board_frame.pack(
            expand=True,
            fill="both",
            padx=30,
            pady=(0, 30),
        )
        for index in range(3):
            board_frame.rowconfigure(index, weight=1)
            board_frame.columnconfigure(index, weight=1)
        for board_index in range(9):
            row = board_index // 3
            column = board_index % 3

            miniboard_frame = tk.Frame(
                board_frame,
                borderwidth=3,
                relief="solid",
            )

            miniboard_frame.grid(
                row=row,
                column=column,
                sticky="nsew",
                padx=3,
                pady=3,
            )

            self.miniboard_frames.append(miniboard_frame)

            for index in range(3):
                miniboard_frame.rowconfigure(index, weight=1)
                miniboard_frame.columnconfigure(index, weight=1)

            board_buttons: list[tk.Button] = []

            for cell_index in range(9):
                cell_row = cell_index // 3
                cell_column = cell_index % 3

                button = tk.Button(
                    miniboard_frame,
                    text="",
                    font=("Helvetica", 20, "bold"),
                    command=lambda b=board_index, c=cell_index: self._handle_move(b, c),
                )

                button.grid(
                    row=cell_row,
                    column=cell_column,
                    sticky="nsew",
                )

                board_buttons.append(button)

            self.cell_buttons.append(board_buttons)
        
        self._refresh_board()

    def _handle_move(self, board: int, cell: int) -> None:
        try:
            self.game.make_move(board, cell)
        except ValueError:
            return

        self._refresh_board()

        if self.game.status != GameStatus.PLAYING:
            self._finish_game()

        self._refresh_board()
    
    def _refresh_board(self) -> None:
        for board_index in range(9):
            for cell_index in range(9):
                player = self.game.boards[board_index].cells[cell_index]
                button = self.cell_buttons[board_index][cell_index]

                if player is None:
                    button.config(text="")
                else:
                    button.config(text=player.value)

                board_is_open = (
                    self.game.boards[board_index].status == BoardStatus.OPEN
                )

                correct_board = (
                    self.game.required_board is None
                    or self.game.required_board == board_index
                )

                game_is_playing = (
                    self.game.status == GameStatus.PLAYING
                )

                if (
                    player is None
                    and board_is_open
                    and correct_board
                    and game_is_playing
                ):
                    button.config(state="normal")
                else:
                    button.config(state="disabled")

            board_status = self.game.boards[board_index].status

            if board_status == BoardStatus.X_WON:
                self._show_miniboard_result(board_index, "X")
            elif board_status == BoardStatus.O_WON:
                self._show_miniboard_result(board_index, "O")
            elif board_status == BoardStatus.TIED:
                self._show_miniboard_result(board_index, "TIE")

        if self.game.status == GameStatus.PLAYING:
            if self.game.required_board is None:
                message = (
                    f"{self.game.current_player.value}'s turn — "
                    "play in any open miniboard"
                )
            else:
                message = (
                    f"{self.game.current_player.value}'s turn — "
                    f"play in miniboard {self.game.required_board}"
                )

            self.status_label.config(text=message)
    
    def _show_miniboard_result(self, board_index: int, symbol: str) -> None:
        if self.winner_labels[board_index] is not None:
            return

        for button in self.cell_buttons[board_index]:
            button.grid_remove()

        font_size = 72 if symbol in ("X", "O") else 36

        winner_label = tk.Label(
            self.miniboard_frames[board_index],
            text=symbol,
            font=("Helvetica", font_size, "bold"),
        )

        winner_label.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
        )

        self.winner_labels[board_index] = winner_label

    def _refresh_score(self) -> None:
        self.score_label.config(
            text=(
                f"X: {self.x_score}    "
                f"O: {self.o_score}    "
                f"Ties: {self.tie_score}"
            )
        )
    
    def _finish_game(self) -> None:
        if self.game.status == GameStatus.X_WON:
            self.x_score += 1
            message = "X wins the game!"

        elif self.game.status == GameStatus.O_WON:
            self.o_score += 1
            message = "O wins the game!"

        else:
            self.tie_score += 1
            message = "The game is a tie!"

        self._refresh_score()
        self.status_label.config(text=message)

        play_again = messagebox.askyesno(
            "Game Over",
            f"{message}\n\nPlay again?",
        )

        if play_again:
            self._reset_game()
        else:
            self.root.destroy()
    
    def _reset_game(self) -> None:
        self.game = Game()

        for board_index in range(9):
            winner_label = self.winner_labels[board_index]

            if winner_label is not None:
                winner_label.destroy()
                self.winner_labels[board_index] = None

            for button in self.cell_buttons[board_index]:
                button.grid()

        self._refresh_board()
