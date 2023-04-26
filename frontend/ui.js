

var winner = null;
let player_1 = {'player_type': "Normal", 'player_name': 'Player 1'}
let player_2 = {'player_type': "Smart", 'player_name': 'Smart Robot'}
let current_player = player_1.player_name;

document.addEventListener('DOMContentLoaded', () => {


// Get the popup and its child elements
const popup = document.getElementById('popup');
const popup2 = document.getElementById('popup2');
const mySelector = document.getElementById('opponent_selection');
const player_1_name = document.getElementById('player_1_name');




function update_current_player(){
    console.log("updating current player")
    $('[name="next1"]').text("Next turn: " + current_player);
}

function display_invalid_move(){
    console.log("invalid move")
    $('[name="next1"]').text("Invalid move, go again " + current_player);
}

function new_game_popup(){
    popup2.style.display = 'block';

}

function start_game(player_1, player_2){
    update_player_names()

    try{
        fetch(' http://127.0.0.1:5000/api/new_game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({"player_1": player_1, "player_2": player_2})
        })
        .then(response => {
            return response.json();
        })
        .then(data => {
            console.log(data); // Output: 'User saved successfully'
            board = data.board;
            current_player = data.cur_player;
            update_board(board)
            update_current_player()
        })
        .catch(error => {
            console.error("Error fetching data:", error);
            console.log("Response status:", error.status);
        })

    } catch (error) {
        console.error("Error parsing JSON Response");
    }


};


function play_move(move=null){
    console.log("play_move function called with move: ", move);
    if(player_1.player_name === current_player){
        player_type = player_1.player_type
        opponent_type = player_2.player_type
    } else {
        player_type = player_2.player_type
        opponent_type = player_1.player_type
    }
    
    try{
        fetch(' http://127.0.0.1:5000/api/move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({"move": move, "player_type": player_type })
        })
        .then(response => {
            return response.json();
        })
        .then(data => {
            console.log(data); // Output: 'User saved successfully'
            board = data.board
            winner = data.winner
            current_player = data.cur_player
            update_board(board)
            update_current_player()
            if (winner !== null){
                 end_game_state(winner)
            }; 

        })
        .catch(error => {
            console.error("Error fetching data:", error);
            console.log("Response status:", error.status);
        })

    } catch (error) {
        console.error("Error parsing JSON Response");
    }

};
// console.log(player_1.player_name ,"   " ,player_1.player_type)

setInterval(function() {

    if(current_player === player_1.player_name && player_1.player_type === "Smart" && winner === null) {
        function play_next_move() {
            play_move();
        }
        setTimeout(play_next_move,1500);
    };
}, 2000);

setInterval(function() {
    if(current_player === player_2.player_name && player_2.player_type === "Smart" && winner === null) {
        function play_next_move() {
            play_move();
        }
        setTimeout(play_next_move,1500);
    };
}, 2000);




function update_board(board) {


    $('button[name="p1_goal"]').text(board[0][0]);

    $('button[name="p1_b0"]').text(board[1][0]);
    $('button[name="p1_b1"]').text(board[1][1]);
    $('button[name="p1_b2"]').text(board[1][2]);
    $('button[name="p1_b3"]').text(board[1][3]);
    $('button[name="p1_b4"]').text(board[1][4]);
    $('button[name="p1_b5"]').text(board[1][5]);

    $('button[name="p2_goal"]').text(board[2][0]);

    $('button[name="p2_b0"]').text(board[3][0]);
    $('button[name="p2_b1"]').text(board[3][1]);
    $('button[name="p2_b2"]').text(board[3][2]);
    $('button[name="p2_b3"]').text(board[3][3]);
    $('button[name="p2_b4"]').text(board[3][4]);
    $('button[name="p2_b5"]').text(board[3][5]);


};

function update_player_names() {
    console.log("updating player names")
    $('[name="p1"]').text(player_1["player_name"]);
    $('[name="p2"]').text(player_2["player_name"]);
}

function end_game_state(w){
    console.log(w + " is the winner!")
    $("[name = 'winner-msg']").text(`${w} wins!`);
    popup.style.display = 'block';

};


console.log("starting game")
new_game_popup()

$(document).ready(function() {
    console.log("document ready")
        console.log("in here player 1 world")

    $("[name='p1_b0']").click(function(){
        if (current_player === player_1.player_name) {
        play_move(0)
        }
    });
    $("[name='p1_b1']").click(function(){
        if (current_player === player_1.player_name) {
            play_move(1)
        }
    });
    $("[name='p1_b2']").click(function(){
        if (current_player === player_1.player_name) {
            play_move(2)
        }
    });
    $("[name='p1_b3']").click(function(){
        if (current_player === player_1.player_name) {
            play_move(3)
        }
    });
    $("[name='p1_b4']").click(function(){
        if (current_player === player_1.player_name) {
        play_move(4)
        }
    });
    $("[name='p1_b5']").click(function(){
        if (current_player === player_1.player_name) {
        play_move(5)
        }
    });



    $("[name='p2_b0']").click(function(){
        if (current_player === player_2.player_name) {
            play_move(0)
        }
    });
    $("[name='p2_b1']").click(function(){
        if (current_player === player_2.player_name) {
            play_move(1)
        }
    });
    $("[name='p2_b2']").click(function(){
        if (current_player === player_2.player_name) {
            play_move(2)
        }
    });
    $("[name='p2_b3']").click(function(){
        if (current_player === player_2.player_name) {
            play_move(3)
        }
    });
    $("[name='p2_b4']").click(function(){
        if (current_player === player_2.player_name) {
        play_move(4)
        }
    });
    $("[name='p2_b5']").click(function(){
        if (current_player === player_2.player_name) {
        play_move(5)
        }
    });

    // When the Play Again button is clicked, hide the popup and reset the game
    $("[name = 'play-again-btn'").click(function(){
        console.log("play again")
        popup.style.display = 'none';
        // Call a function to reset the game
        console.log("starting game")
        start_game(player_1, player_2)
    });
    $("[name = 'play'").click(function(){
        console.log("starting a game")
        popup2.style.display = 'none';
        // Set the correct player names based on inputs
        player_1.player_name = player_1_name.value
        if (mySelector.value === "robot"){
            player_2_name = "Smart Robot"
            player_2_type = "Smart"
        } else {
            player_2_name = "Smart Human"
            player_2_type = "Normal"
        }
        player_2.player_type = player_2_type
        player_2.player_name = player_2_name


        console.log("starting game")
        start_game(player_1, player_2)
    });
    

});
});

