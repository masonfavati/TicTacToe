from enum import StrEnum


class Player(StrEnum):
    X = "X"
    O = "O"


class BoardStatus(StrEnum):
    OPEN = "open"
    X_WON = "x_won"
    O_WON = "o_won"
    TIED = "tied"