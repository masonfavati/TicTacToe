from enum import StrEnum


class Player(StrEnum):
    X = "X"
    O = "O"


class BoardStatus(StrEnum):
    OPEN = "open"
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