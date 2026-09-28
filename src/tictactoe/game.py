from enum import StrEnum


class Player(StrEnum):
    X = "X"
    O = "O"


class BoardStatus(StrEnum):
    OPEN = "open"
    X_WON = "x_won"
    O_WON = "o_won"
    TIED = "tied"

class GameStatus(StrEnum):
    PLAYING = "playing"
    X_WON = "x_won"
    O_WON = "o_won"
    TIED = "tied"


WINNING_LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


class MiniBoard:
    def __init__(self) -> None:
        self.cells: list[Player | None] = [None] * 9
        self.status = BoardStatus.OPEN

    def make_move(self, cell: int, player: Player) -> None:
        if self.status != BoardStatus.OPEN:
            raise ValueError("This miniboard is already finished.")

        if not 0 <= cell <= 8:
            raise ValueError("Cell must be between 0 and 8.")

        if self.cells[cell] is not None:
            raise ValueError("This cell is already occupied.")

        self.cells[cell] = player
        self._update_status()

    def _update_status(self) -> None:
        for first, second, third in WINNING_LINES:
            if (
                self.cells[first] is not None
                and self.cells[first] == self.cells[second]
                and self.cells[first] == self.cells[third]
            ):
                winner = self.cells[first]

                if winner == Player.X:
                    self.status = BoardStatus.X_WON
                else:
                    self.status = BoardStatus.O_WON

                return
            
        if all(cell is not None for cell in self.cells):
            self.status = BoardStatus.TIED

class Game:
    def __init__(self) -> None:
        self.boards = [MiniBoard() for _ in range(9)]
        self.current_player = Player.X
        self.required_board: int | None = None
        self.status = GameStatus.PLAYING
    
    def make_move(self, board: int, cell: int) -> None:
        if self.status != GameStatus.PLAYING:
            raise ValueError("The game is already finished.")
        if not 0 <= board <= 8:
            raise ValueError("Board must be between 0 and 8.")
        if self.required_board is not None and board != self.required_board:
            raise ValueError(
                f"You must play in miniboard {self.required_board}."
            )
        selected_board = self.boards[board]
        if selected_board.status != BoardStatus.OPEN:
            raise ValueError("This miniboard is already finished.")
        selected_board.make_move(cell, self.current_player)
        self._update_status()
        if self.status == GameStatus.PLAYING:
            self._set_next_required_board(cell)
            self._switch_player()

    def _set_next_required_board(self, cell: int) -> None:
        destination_board = self.boards[cell]
        if destination_board.status == BoardStatus.OPEN:
            self.required_board = cell
        else:
            self.required_board = None

    def _switch_player(self) -> None:
        if self.current_player == Player.X:
            self.current_player = Player.O
        else:
            self.current_player = Player.X

    def _board_owner(self, board: int) -> Player | None:
        status = self.boards[board].status
        if status == BoardStatus.X_WON:
            return Player.X
        if status == BoardStatus.O_WON:
            return Player.O
        return None
    
    def _update_status(self) -> None:
        for first, second, third in WINNING_LINES:
            first_owner = self._board_owner(first)
            if (
                first_owner is not None
                and first_owner == self._board_owner(second)
                and first_owner == self._board_owner(third)
            ):
                if first_owner == Player.X:
                    self.status = GameStatus.X_WON
                else:
                    self.status = GameStatus.O_WON
                return
        if all(board.status != BoardStatus.OPEN for board in self.boards):
            self.status = GameStatus.TIED