

var winner = null;
let player_1 = {'player_type': "Normal", 'player_name': 'Player 1'}
let player_2 = {'player_type': "Smart", 'player_name': 'Smart Robot'}
let current_player = player_1.player_name;
let active = false 

document.addEventListener('DOMContentLoaded', () => {


// Get the popup and its child elements
const popup = document.getElementById('popup3');
const RL_popup = document.getElementById('RL_Popup');
const start_game_window = document.getElementById('login-box');




async function show_me_the_pickle() {
    try{
        fetch(' http://127.0.0.1:5000/api/load_model', {
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
            console.log(data); 
            message = data.message;
            success = data.success;

            if (success === true){
                RL_popup.style.display = 'block';
            }
            //if this was succcessful then we can allow people to play against RL BOT
        })
        .catch(error => {
            console.error("Error fetching data:", error);
            console.log("Response status:", error.status);
        })

    } catch (error) {
        console.error("Error parsing JSON Response");
    }

  }

function get_last_player(){
    if(player_1.player_name === current_player){
        return player_2
    } else {
        return player_1
    }

}

function update_current_player(){
    console.log("updating current player to be " + current_player)
    $('[name="next1"]').text("Next turn: " + current_player);
    if (current_player === player_1.player_name) {
        console.log("trying to change the colors")
        document.getElementById("p1_name").style.color = "#23DB47";
        document.getElementById("p2_name").style.color = "black";
    } else {
        document.getElementById("p2_name").style.color = "#23DB47";
        document.getElementById("p1_name").style.color = "black";
    }
    
    // $('[name="next1"]').text("Next turn: " + current_player);
}


function new_game_popup(){
    RL_popup.style.display = 'none';
    start_game_window.style.display = 'block';

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
            console.log(data); 
            board = data.board;
            current_player = data.cur_player;
            update_board(board)
            update_current_player()
            winner = null
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
    p_name = current_player
    current_player = null
    active = true    
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
            console.log(data); 
            board = data.board
            winner = data.winner
            current_player = data.cur_player
            last_move_player = get_last_player()
            move = data.move
            update_board(board, move, p_name)
            update_current_player()
            if (winner !== null){
                 end_game_state(winner)
            }; 
            active = false

        })
        .catch(error => {
            console.error("Error fetching data:", error);
            console.log("Response status:", error.status);
        })

    } catch (error) {
        console.error("Error parsing JSON Response");
    }

};

setInterval(function() {

    if(active === false && current_player === player_1.player_name && (player_1.player_type === "Smart" || player_1.player_type === "RL") && winner === null) {
        console.log("p1 is playing again")
        function play_next_move() {
            play_move();
        }
        setTimeout(play_next_move,50);
    };
}, 3000);

setInterval(function() {
    if(active === false && current_player === player_2.player_name && (player_2.player_type === "Smart" || player_2.player_type === "RL") && winner === null) {
        console.log("p2 is playing again")
        function play_next_move() {
            play_move();
        }
        setTimeout(play_next_move,50);
    };
}, 3000);




function update_board(board, move = null, last_player = null) {


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

    if(move != null && last_player != null){
        if (player_1.player_name === last_player) {
            index = 1;
            p_ = "p1"
        }else {
            index = 3;
            p_ = "p2"
        }
        button_string = p_ + "_b" + String(move);

        function highlight_last_move() {
            document.querySelector('[name="' + button_string + '"]').focus();
        }
        async function fade_last_move_highlight() {
            document.querySelector('[name="' + button_string + '"]').blur();
        }

        highlight_last_move()
        setTimeout(fade_last_move_highlight,500);
        
        
    }



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
    RL_popup.style.display = 'block';
    start_game_window.style.display = 'none'

};


console.log("starting game")
show_me_the_pickle()
console.log("loading pick in the background")
new_game_popup()
popup.style.display = 'none'

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
        RL_popup.style.display = 'block';
        // Call a function to reset the game
        console.log("starting game")
        start_game(player_1, player_2)
    });
    $("[name = 'play'").click(function(){
        const player_1_selector = document.getElementById('player_1_selection');
        const player_2_selector = document.getElementById('player_2_selection');
        const player_1_name = document.getElementById('player_1_name');
        const player_2_name = document.getElementById('player_2_name'); 

        console.log("starting a game")
        start_game_window.style.display = 'none';
        // Set the correct player names based on inputs

        if (player_1_selector.value === "human"){
            player_1.player_type = 'Normal'
            if (player_1_name.value === "" ){
                player_1.player_name = "Smart Human 1"
            } else {
                player_1.player_name = player_1_name.value
            }
        }
        else {
            player_1.player_type = "Smart"
            if (player_1_name.value === "" ){
                player_1.player_name = "Smart Robot 1"
            } else {
                player_1.player_name = player_1_name.value
            }
        }


        if (player_2_selector.value === "human"){
            player_2.player_type = 'Normal';
            if (player_2_name.value === "" ){
                player_2.player_name = "Smart Human 2"
            } else {
                player_2.player_name = player_2_name.value
            }

        } else {
            player_2.player_type = "Smart"
            if (player_2_name.value === "" ){
                player_2.player_name = "Smart Robot 2"
            } else {
                player_2.player_name = player_2_name.value
            }
        }

        console.log("starting game")
        start_game(player_1, player_2)
    });

    $("[name = 'play_RL'").click(function(){
        start_game_window.style.display = 'none';
        RL_popup.style.display = 'none';
        popup.style.display = 'none';

        console.log("starting a game game with RL bot")
        if (player_1.player_type === "Normal" ){
            player_2.player_name = player_1.player_name
            player_2.player_type = "Normal"
        } else if (player_2.player_type === "Normal"){
            //keep player 2 the same
        } else {
            player_2.player_name = "Human"
            player_2.player_type = "Normal"
        }

        player_1.player_name = "RL Bot"
        player_1.player_type = "RL"

        console.log("starting game")
        start_game(player_1, player_2)
    });
    

});
});

