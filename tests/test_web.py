import tictactoe.web as web
from tictactoe.game import Game, Player


def setup_function() -> None:
    web.game = Game()
    web.x_score = 0
    web.o_score = 0
    web.tie_score = 0


def test_home_page_loads() -> None:
    client = web.app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Ultimate Tic-Tac-Toe" in response.data


def test_legal_move() -> None:
    client = web.app.test_client()

    response = client.post(
        "/move",
        json={"board": 0, "cell": 4},
    )

    data = response.get_json()

    assert response.status_code == 200
    assert data["player"] == "X"
    assert data["current_player"] == "O"
    assert data["required_board"] == 4
    assert web.game.boards[0].cells[4] == Player.X


def test_illegal_move_returns_error() -> None:
    client = web.app.test_client()

    client.post(
        "/move",
        json={"board": 0, "cell": 4},
    )

    response = client.post(
        "/move",
        json={"board": 0, "cell": 0},
    )

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_reset_creates_new_game_and_keeps_score() -> None:
    client = web.app.test_client()

    web.x_score = 2
    web.o_score = 1
    web.tie_score = 1

    client.post(
        "/move",
        json={"board": 0, "cell": 4},
    )

    response = client.post("/reset")

    data = response.get_json()

    assert response.status_code == 200
    assert web.game.current_player == Player.X
    assert all(
        cell is None
        for board in web.game.boards
        for cell in board.cells
    )

    assert data["x_score"] == 2
    assert data["o_score"] == 1
    assert data["tie_score"] == 1