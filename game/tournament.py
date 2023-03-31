from mancala import Mancala_game
from player import Player
import pickle
import os


class Tournament:
    def __init__(self, player1, player2, num_games = 10000):
        self.player1 = player1
        self.player2 = player2
        self.num_games  = num_games
        self.player1_win_count = 0
        self.player2_win_count = 0
        self.p1_win_ratio = 0
        self.p2_win_ratio = 0
        self.tournament_winner = None
        self.winner_ratio = 0
        self.pickle_file = "models/mancala_moves_dict_a_75.pickle"
        self.moves_dict = None

    def create_new_pickle(self):
        mancala_moves_dict = {}
        with open(self.pickle_file, 'wb') as handle:
            pickle.dump(mancala_moves_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load_pickle (self):
        if os.path.getsize(self.pickle_file) > 0:
            with open(self.pickle_file, 'rb') as handle:
                print("Loading pickle file ...")
                self.moves_dict = pickle.load(handle)
        else:
            self.moves_dict = {}
            

    def update_pickle_file(self):
        print("saving Pickle")
        with open(self.pickle_file, 'wb') as handle:
            pickle.dump(self.moves_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    


    def play_tournament(self):
        #check if either player requires the pickle to be loaded
        if self.player1.player_type == "RL_Bot" :
            # print("loading pickle")
            self.load_pickle()

        for i in range(0, self.num_games):
            if self.player1.player_type == "RL_Bot" :
                self.player1.refresh_moves_dict(self.moves_dict)
            mancala_game = Mancala_game(self.player1, self.player2)
            mancala_game.play_game()
            if mancala_game.winner == self.player1:
                self.player1_win_count += 1
            else:
                self.player2_win_count +=1
            if self.player1.player_type == "RL_Bot" :
                self.moves_dict = self.player1.collect_final_dict()
                if i%1000 == 0 and i != 0:
                    self.moves_dict = self.player1.collect_final_dict()
                    self.update_pickle_file()

        self.p1_win_ratio = self.player1_win_count/self.num_games
        self.p2_win_ratio = self.player2_win_count/self.num_games

        if self.player1_win_count> self.player2_win_count:
            self.tournament_winner = self.player1
            self.winner_ratio  = self.p1_win_ratio
        else:
            self.tournament_winner = self.player2
            self.winner_ratio = self.p2_win_ratio

        #save the final dict
        if self.player1.player_type == "RL_Bot" :
            self.moves_dict = self.player1.collect_final_dict()
            self.update_pickle_file()

        print("win count player 1: " + str(self.player1_win_count))
        print("win count player 2: " + str(self.player2_win_count))
        
        print("\n !!!!!!!!!! ")
        print(self.tournament_winner.player_name + " is the winner with with ratio " + str(self.winner_ratio))
        print(" !!!!!!!!!! \n")

        


print(" \n Hello Welcome to Mancala :) \n ")
player1 = Player("RL_Bot", "RL Bot")
player2 = Player("Random", "Random Bot")

tournament = Tournament(player1, player2) 
tournament.play_tournament()



        

