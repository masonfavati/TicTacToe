import pytest

from tictactoe.game import BoardStatus, Game, GameStatus, MiniBoard, Player

def test_new_miniboard_is_empty_and_open() -> None:
    board = MiniBoard()

    assert board.cells == [None] * 9
    assert board.status == BoardStatus.OPEN

def test_miniboard_accepts_move() -> None:
    board = MiniBoard()

    board.make_move(4, Player.X)

    assert board.cells[4] == Player.X

def test_miniboard_rejects_occupied_cell() -> None:
    board = MiniBoard()
    board.make_move(4, Player.X)

    with pytest.raises(ValueError, match="This cell is already occupied."):
        board.make_move(4, Player.O)

    assert board.cells[4] == Player.X

def test_x_can_win_miniboard() -> None:
    board = MiniBoard()

    board.make_move(0, Player.X)
    board.make_move(1, Player.X)
    board.make_move(2, Player.X)

    assert board.status == BoardStatus.X_WON

def test_o_can_win_miniboard() -> None:
    board = MiniBoard()

    board.make_move(0, Player.O)
    board.make_move(4, Player.O)
    board.make_move(8, Player.O)

    assert board.status == BoardStatus.O_WON

def test_miniboard_can_tie() -> None:
    board = MiniBoard()

    moves = [
        (0, Player.X),
        (1, Player.O),
        (2, Player.X),
        (3, Player.X),
        (4, Player.O),
        (5, Player.O),
        (6, Player.O),
        (7, Player.X),
        (8, Player.X),
    ]

    for cell, player in moves:
        board.make_move(cell, player)

    assert board.status == BoardStatus.TIED

def test_new_game_starts_with_x_and_no_required_board() -> None:
    game = Game()

    assert len(game.boards) == 9
    assert game.current_player == Player.X
    assert game.required_board is None
    assert game.status == GameStatus.PLAYING

def test_move_sends_opponent_to_corresponding_board() -> None:
    game = Game()

    game.make_move(4, 2)

    assert game.boards[4].cells[2] == Player.X
    assert game.current_player == Player.O
    assert game.required_board == 2

def test_player_cannot_use_wrong_miniboard() -> None:
    game = Game()

    game.make_move(4, 2)

    with pytest.raises(ValueError, match="You must play in miniboard 2."):
        game.make_move(3, 0)

    assert game.current_player == Player.O
    assert game.required_board == 2

def test_finished_destination_allows_free_choice() -> None:
    game = Game()

    game.boards[2].status = BoardStatus.X_WON

    game.make_move(4, 2)

    assert game.required_board is None
    assert game.current_player == Player.O

def test_tied_destination_allows_free_choice() -> None:
    game = Game()

    game.boards[6].status = BoardStatus.TIED

    game.make_move(4, 6)

    assert game.required_board is None
    assert game.current_player == Player.O

def test_x_can_win_game() -> None:
    game = Game()

    game.boards[0].status = BoardStatus.X_WON
    game.boards[1].status = BoardStatus.X_WON

    game.current_player = Player.X
    game.required_board = None

    game.boards[2].cells[0] = Player.X
    game.boards[2].cells[1] = Player.X

    game.make_move(2, 2)

    assert game.boards[2].status == BoardStatus.X_WON
    assert game.status == GameStatus.X_WON

def test_finished_game_rejects_moves() -> None:
    game = Game()
    game.status = GameStatus.X_WON

    with pytest.raises(ValueError, match="The game is already finished."):
        game.make_move(4, 4)

def test_game_can_end_in_tie() -> None:
    game = Game()

    finished_statuses = [
        BoardStatus.X_WON,
        BoardStatus.O_WON,
        BoardStatus.TIED,
        BoardStatus.O_WON,
        BoardStatus.TIED,
        BoardStatus.X_WON,
        BoardStatus.TIED,
        BoardStatus.X_WON,
        BoardStatus.OPEN,
    ]

    for index, status in enumerate(finished_statuses):
        game.boards[index].status = status

    game.current_player = Player.O
    game.required_board = None

    game.boards[8].cells[0] = Player.X
    game.boards[8].cells[1] = Player.O
    game.boards[8].cells[2] = Player.X
    game.boards[8].cells[3] = Player.X
    game.boards[8].cells[4] = Player.O
    game.boards[8].cells[5] = Player.O
    game.boards[8].cells[6] = Player.O
    game.boards[8].cells[7] = Player.X

    game.make_move(8, 8)

    assert game.boards[8].status == BoardStatus.TIED
    assert game.status == GameStatus.TIED

def test_miniboard_stores_winning_line() -> None:
    board = MiniBoard()

    board.make_move(0, Player.X)
    board.make_move(3, Player.O)
    board.make_move(1, Player.X)
    board.make_move(4, Player.O)
    board.make_move(2, Player.X)

    assert board.status == BoardStatus.X_WON
    assert board.winning_line == (0, 1, 2)

def test_game_stores_winning_line() -> None:
    game = Game()

    game.boards[0].status = BoardStatus.X_WON
    game.boards[1].status = BoardStatus.X_WON
    game.boards[2].status = BoardStatus.X_WON

    game._update_status()

    assert game.status == GameStatus.X_WON
    assert game.winning_line == (0, 1, 2)