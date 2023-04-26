# app.py

from flask import Flask, request, jsonify
import mancala_scripts
from flask_cors import CORS, cross_origin
from mancala import Mancala_game
from player import Player

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

game = None 
game_path = './stored_games/game.pickle'


@app.route('/api/new_game', methods=['POST']) 
@cross_origin()
def new_game():
    #innitialize a new game with the correct player types 
    #responds with game details 

    data = request.json
    player_1 = data["player_1"]
    player_2 = data["player_2"]

    mancala_game, board, cur_player = mancala_scripts.new_game(player_1, player_2)
    mancala_scripts.save_pickle(game_path, mancala_game)

    ##TODO need to save the mancala game to the pickle file 

    response = jsonify({'message': "starting game with players: " + player_1["player_name"] + " and " + player_2["player_name"] \
                        + " waiting for a move from player " + cur_player.player_name,\
                        'board': board, 'cur_player': cur_player.player_name})
    return response

@app.route('/api/move', methods=['POST'])
@cross_origin()
def move():
    
    data = request.json
    move = data["move"] 
    p_type = data["player_type"] 

    if move is None: # convert JS nonetype to python nontype
        move = None

    game = mancala_scripts.load_pickle(game_path)

    mancala_game, board, cur_player, winner = mancala_scripts.move(game, move, p_type)
    mancala_scripts.save_pickle(game_path, mancala_game)

    if winner:
        response = jsonify({'message': "Made move " + str(move) + ' waiting for move from ' + cur_player.player_name,\
                            'board': board, 'winner': winner.player_name, 'cur_player': cur_player.player_name})
    else:
        response = jsonify({'message': "Made move " + str(move) + ' waiting for move from ' + cur_player.player_name,\
                            'board': board, 'winner': winner, 'cur_player': cur_player.player_name})

    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug = True)