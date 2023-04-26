import pickle
import os
from mancala import Mancala_game
from player import Player



def save_pickle(file, game):
    with open(file, 'wb') as handle:
        pickle.dump(game, handle, protocol=pickle.HIGHEST_PROTOCOL)

def load_pickle (file):
    if os.path.getsize(file) > 0:
        with open(file, 'rb') as handle:
            print("Loading pickle file ...")
            v = pickle.load(handle)
    return v

        

def check_pickle_size(file):
    if os.path.getsize(file) > 0:
            with open(file, 'rb') as handle:
                print("Loading pickle file ...")
                moves_dict = pickle.load(handle)
    pickle_size = len(moves_dict.keys())
    print("There are " + str(pickle_size) + " states in the dictionary ")
    return pickle_size



def new_game(player_1, player_2):
    player1 = Player(player_1["player_type"], player_1["player_name"])
    player2 = Player(player_2["player_type"], player_2["player_name"])

    mancala_game = Mancala_game(player1, player2)
    board, cur_player = mancala_game.start_game() 
     
    return  mancala_game, board, cur_player

def move(mancala_game, move=None, player_type=None):
    winner, cur_player, board = mancala_game.app_make_move(move, player_type)

    return mancala_game, board, cur_player, winner
     
     


# pickle_file =  "models/RL_model_top.pickle"
# check_pickle_size(pickle_file)