import random
import pickle
import os


class Player:

    def __init__(self, player_type = "Random", player_name = "Robot", moves_dict = None):
        self.player_type = player_type
        self.player_name = player_name
        self.list_of_moves = []
        self.alpha = 1    
        self.beta = 0
        self.moves_dict = moves_dict
        self.file = "models/mancala_moves_dict_a_75.pickle"

    def generate_move(self, board):
        if self.player_type == "Normal":
            move = int(input(self.player_name + " input your move: "))
        elif self.player_type == "Random":
            move = random.randint(0,5)
        elif self.player_type == "RL_Bot":
            move = self.check_for_known_move(board)
            self.list_of_moves += [[str(board),move]]
             
        return move
            
    def refresh_moves_dict(self, updated_dict):
        self.moves_dict = updated_dict
            
    def check_for_known_move(self, board):
        self.set_impossible_moves_to_0(board)

        if str(board) in self.moves_dict.keys():

            r = random.random()
            if r <= self.alpha:
                #chose best option 
                max_score = max(self.moves_dict[str(board)])
                max_index = []
                # print("Max score is:  " + str(max_score))
                # print(self.moves_dict[str(board)])
                # input()
                for i in range(0, len(self.moves_dict[str(board)])):
                    if self.moves_dict[str(board)][i] == max_score:
                        max_index.append(i)
                #if there are 2 with the same score chose randomly 
                index = random.randint(0,len(max_index)-1)
                move = max_index[index]
            else:
                #explore
                move = random.randint(0,5)
            
        else:
            #if we havent seen the move before then play randomly 
            self.moves_dict[str(board)] = [0,0,0,0,0,0]
            move = random.randint(0,5)

        return move

    def set_impossible_moves_to_0(self, board):
        if str(board) in self.moves_dict.keys():
            for i in range(0,len(board[1])):
                if board[1][i] == 0:
                    self.moves_dict[str(board)][i] = 0
        else:
            #if we havent seen the move before then play randomly 
            self.moves_dict[str(board)] = [0,0,0,0,0,0]
        



    def update_dict(self, board, move, points):
        if self.player_type == "RL_Bot":


            self.moves_dict[str(board)][move] = points

        else:
            None



    def end_game_update(self, is_winner):

        if self.player_type == "RL_Bot" and is_winner:
            # print(self.list_of_moves)
            # input()
            for m in range(0, len(self.list_of_moves)):
                board = self.list_of_moves[m][0]
                move = self.list_of_moves[m][1]
                self.moves_dict[board][move]+=100



    def collect_final_dict(self):
        return self.moves_dict


            



        
        

        





                

    


#initialize mancala moves dict
# mancala_moves_dict = {}
# with open('models/mancala_moves_dict_a_0.75.pickle', 'wb') as handle:
#     pickle.dump(mancala_moves_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
