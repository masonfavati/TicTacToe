import logging

from flask import Flask, jsonify, render_template, request

from tictactoe.game import BoardStatus, Game, GameStatus

app = Flask(__name__)

logging.getLogger("werkzeug").setLevel(logging.ERROR)

game = Game()

x_score = 0
o_score = 0
tie_score = 0


@app.route("/")
def index() -> str:
    is_first_move = all(
        cell is None
        for board in game.boards
        for cell in board.cells
    )

    return render_template(
        "index.html",
        game=game,
        x_score=x_score,
        o_score=o_score,
        tie_score=tie_score,
        is_first_move=is_first_move,
    )


@app.route("/move", methods=["POST"])
def move():
    global x_score, o_score, tie_score
    data = request.get_json()

    board = data["board"]
    cell = data["cell"]

    try:
        game.make_move(board, cell)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    board_status = game.boards[board].status

    if board_status == BoardStatus.X_WON:
        board_result = "X"
    elif board_status == BoardStatus.O_WON:
        board_result = "O"
    elif board_status == BoardStatus.TIED:
        board_result = "TIE"
    else:
        board_result = None

    winning_line = game.boards[board].winning_line

    if game.status == GameStatus.X_WON:
        x_score += 1
        game_result = "X"
    elif game.status == GameStatus.O_WON:
        o_score += 1
        game_result = "O"
    elif game.status == GameStatus.TIED:
        tie_score += 1
        game_result = "TIE"
    else:
        game_result = None

    return jsonify(
        {
            "board": board,
            "cell": cell,
            "player": game.boards[board].cells[cell].value,
            "winning_line": winning_line,
            "game_winning_line": game.winning_line,
            "current_player": game.current_player.value,
            "required_board": game.required_board,
            "board_result": board_result,
            "game_result": game_result,
            "x_score": x_score,
            "o_score": o_score,
            "tie_score": tie_score,
        }
    )

@app.route("/reset", methods=["POST"])
def reset():
    global game

    game = Game()

    return jsonify(
        {
            "x_score": x_score,
            "o_score": o_score,
            "tie_score": tie_score,
        }
    )


def main() -> None:
    app.run(debug=False)