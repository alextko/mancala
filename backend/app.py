# app.py

from flask import Flask, request, jsonify
import mancala_scripts
from flask_cors import CORS, cross_origin
from mancala import Mancala_game
from player import Player
import time

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

global_game = None 
game_path = './stored_games/game.pickle'

# model_path = "models/nd1.pickle"
model_path = "models/RL_model_top_4.pickle"
model = None


@app.route('/api/new_game', methods=['POST']) 
@cross_origin()
def new_game():
    #innitialize a new game with the correct player types 
    #responds with game details 

    data = request.json
    player_1 = data["player_1"]
    player_2 = data["player_2"]

    mancala_game, board, cur_player = mancala_scripts.new_game(player_1, player_2, model)
    global global_game 
    global_game = mancala_game
    # mancala_scripts.save_pickle(game_path, mancala_game)

    ##TODO need to save the mancala game to the pickle file 

    response = jsonify({'message': "starting game with players: " + player_1["player_name"] + " and " + player_2["player_name"] \
                        + " waiting for a move from player " + cur_player.player_name,\
                        'board': board, 'cur_player': cur_player.player_name})
    return response

@app.route('/api/move', methods=['POST'])
@cross_origin()
def move():
    global global_game
    
    data = request.json
    move = data["move"] 
    p_type = data["player_type"] 

    if move is None: # convert JS nonetype to python nontype
        move = None
    # game = mancala_scripts.load_pickle(game_path)
    mancala_game, board, cur_player, winner, move = mancala_scripts.move(global_game, move, p_type)
    global_game = mancala_game
    # mancala_scripts.save_pickle(game_path, mancala_game)

    if winner:
        response = jsonify({'message': "Made move " + str(move) + ' waiting for move from ' + cur_player.player_name,\
                            'board': board, 'winner': winner.player_name, 'cur_player': cur_player.player_name, \
                            'move': move})
    else:
        response = jsonify({'message': "Made move " + str(move) + ' waiting for move from ' + cur_player.player_name,\
                            'board': board, 'winner': winner, 'cur_player': cur_player.player_name,\
                            'move': move})
    

    return response



@app.route('/api/load_model', methods=['POST'])
@cross_origin()
def load_model():
    model = mancala_scripts.load_pickle(model_path)
    if model != None:
        success = True
    else:
        success = False

    response = jsonify({'message': "RL BOT loaded successfully, you may now play",\
                            'success': success})

    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug = True)