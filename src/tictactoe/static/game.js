function createWinningLine(winningLine, player) {
    const line = document.createElement("div");

    line.classList.add("winning-line", player.toLowerCase());

    const first = winningLine[0];
    const third = winningLine[2];

    const firstRow = Math.floor(first / 3);
    const firstColumn = first % 3;

    const thirdRow = Math.floor(third / 3);
    const thirdColumn = third % 3;

    const startX = (firstColumn + 0.5) * (100 / 3);
    const startY = (firstRow + 0.5) * (100 / 3);

    const endX = (thirdColumn + 0.5) * (100 / 3);
    const endY = (thirdRow + 0.5) * (100 / 3);

    const deltaX = endX - startX;
    const deltaY = endY - startY;

    const length = Math.sqrt(
        deltaX * deltaX + deltaY * deltaY
    );

    const angle = Math.atan2(deltaY, deltaX) * (180 / Math.PI);

    line.style.left = `${startX}%`;
    line.style.top = `${startY}%`;
    line.style.width = `${length}%`;

    line.style.transformOrigin = "left center";

    line.style.setProperty("--line-angle", `${angle}deg`);

    return line;
}

function createBigWinningLine(winningLine, player) {
    const line = document.createElement("div");

    line.classList.add(
        "big-winning-line",
        player.toLowerCase()
    );

    const first = winningLine[0];
    const third = winningLine[2];

    const firstRow = Math.floor(first / 3);
    const firstColumn = first % 3;

    const thirdRow = Math.floor(third / 3);
    const thirdColumn = third % 3;

    const startX = (firstColumn + 0.5) * (100 / 3);
    const startY = (firstRow + 0.5) * (100 / 3);

    const endX = (thirdColumn + 0.5) * (100 / 3);
    const endY = (thirdRow + 0.5) * (100 / 3);

    const deltaX = endX - startX;
    const deltaY = endY - startY;

    const length = Math.sqrt(
        deltaX * deltaX + deltaY * deltaY
    );

    const angle =
        Math.atan2(deltaY, deltaX) * (180 / Math.PI);

    line.style.left = `${startX}%`;
    line.style.top = `${startY}%`;
    line.style.width = `${length}%`;

    line.style.setProperty(
        "--line-angle",
        `${angle}deg`
    );

    return line;
}

const cells = document.querySelectorAll(".cell");
const miniboards = document.querySelectorAll(".miniboard");
const gameBoard = document.querySelector("#game-board");
const statusMessage = document.querySelector("#status-message");
const xScore = document.querySelector("#x-score");
const oScore = document.querySelector("#o-score");
const tieScore = document.querySelector("#tie-score");
const playAgainButton = document.querySelector("#play-again");

cells.forEach((cell) => {
    cell.addEventListener("click", async () => {
        const board = Number(cell.dataset.board);
        const cellIndex = Number(cell.dataset.cell);

        const response = await fetch("/move", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                board: board,
                cell: cellIndex,
            }),
        });

        const data = await response.json();

        if (!response.ok) {
            return;
        }

        const mark = document.createElement("span");
        mark.classList.add("mark", data.player.toLowerCase());
        mark.textContent = data.player;

        cell.replaceChildren(mark);

        xScore.textContent = data.x_score;
        oScore.textContent = data.o_score;
        tieScore.textContent = data.tie_score;

        if (data.board_result !== null) {
            const finishedBoard = miniboards[data.board];
        
            if (
                data.board_result !== "TIE" &&
                data.winning_line !== null
            ) {
                const winningLine = createWinningLine(
                    data.winning_line,
                    data.board_result
                );
        
                finishedBoard.appendChild(winningLine);
        
                await new Promise((resolve) => {
                    setTimeout(resolve, 850);
                });
            }
        
            finishedBoard.innerHTML = "";
        
            const result = document.createElement("div");
            result.classList.add("miniboard-result");
        
            if (data.board_result === "TIE") {
                result.classList.add("tie");
            } else if (data.board_result === "X") {
                result.classList.add("x");
            } else if (data.board_result === "O") {
                result.classList.add("o");
            }
        
            result.textContent = data.board_result;
        
            finishedBoard.appendChild(result);
        }

        miniboards.forEach((miniboard) => {
            miniboard.classList.remove("playable");
        });
        
        if (data.required_board === null) {
            miniboards.forEach((miniboard) => {
                if (miniboard.querySelector(".cell") !== null) {
                    miniboard.classList.add("playable");
                }
            });
        
            statusMessage.innerHTML =
                `<span class="status-player ${data.current_player.toLowerCase()}">` +
                `${data.current_player}</span>'s turn — play in any open miniboard`;
        } else {
            miniboards[data.required_board].classList.add("playable");
        
            statusMessage.innerHTML =
                `<span class="status-player ${data.current_player.toLowerCase()}">` +
                `${data.current_player}</span>'s turn — play in miniboard ` +
                `${data.required_board + 1}`;
        }

        if (
            data.game_result === "X" ||
            data.game_result === "O"
        ) {
            statusMessage.innerHTML =
                `<span class="status-player ${data.game_result.toLowerCase()}">` +
                `${data.game_result}</span> wins the game!`;
        
            if (data.game_winning_line !== null) {
                const bigWinningLine = createBigWinningLine(
                    data.game_winning_line,
                    data.game_result
                );
        
                gameBoard.appendChild(bigWinningLine);
            }
        
            playAgainButton.hidden = false;
        } else if (data.game_result === "TIE") {
            statusMessage.textContent = "The game is a tie!";
            playAgainButton.hidden = false;
        }
    });
});

playAgainButton.addEventListener("click", async () => {
    const response = await fetch("/reset", {
        method: "POST",
    });

    if (!response.ok) {
        return;
    }

    window.location.reload();
});

const savedBigWinningLine =
    document.querySelector("#saved-big-winning-line");

if (savedBigWinningLine !== null) {
    const winningLine = [
        Number(savedBigWinningLine.dataset.first),
        Number(savedBigWinningLine.dataset.second),
        Number(savedBigWinningLine.dataset.third),
    ];

    const player = savedBigWinningLine.dataset.player;

    const bigWinningLine = createBigWinningLine(
        winningLine,
        player
    );
    
    bigWinningLine.classList.add("restored");
    
    gameBoard.appendChild(bigWinningLine);
}