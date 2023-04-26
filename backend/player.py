import random
import pickle
import os


class Player:

    def __init__(self, player_type = "Random", player_name = "Robot", player_side = "top", moves_dict = None, tournament = False, training_mode = False):
        self.player_type = player_type
        self.player_name = player_name
        self.player_side = player_side
        self.game_count = 0
        self.move_log = []
        self.reward_log = []
        self.action_log = []
        self.random_move_prob = 0
        self.move_count = 0
        self.seen_move_count = 0
        self.end_discount = 0.99
        self.gamma = 0.9
        self.beta = 0
        self.training_mode = training_mode
        self.tournament = tournament
        self.moves_dict = moves_dict
        self.file = None
        self.message = ""
        self.file_top = "models/RL_model_top_4.pickle"
        self.file_bottom = "models/RL_model_bottom.pickle"
        
        self._player_side(self.player_side)
        if moves_dict == None and tournament == False and player_type == "RL":
            if not moves_dict:
                self.load_pickle()
        if not self.training_mode:
            self.random_move_prob = 0



    def _player_side(self, side):
        self.player_side = side
        if self.player_side == "top":
            self.file = self.file_top
        else:
            self.file = self.file_bottom

    def generate_move(self, board):
        if self.player_type == "Normal":
            move = int(input(self.player_name + " input your move: "))
        elif self.player_type == "Random":
            move = random.randint(0,5)
        elif self.player_type == "RL":
            self.move_count += 1
            board_temp = [board[1], board[3]]
            move = self.check_for_known_move(board_temp)
            
            if not self.tournament:
                print(self.player_name + " played move " + str(move))
        elif self.player_type == "Smart":
            move = self.smartest_move(board)
            if not self.tournament:
                print(self.player_name + " played move " + str(move))
             
        return move
            
    def refresh_moves_dict(self, updated_dict):
        self.moves_dict = updated_dict
            
    def check_for_known_move(self, board):

        self.set_impossible_moves_to_0(board)

        if str(board) in self.moves_dict:
            # print(board)
            # print("IN HERE CHECKING FOR A KNOWN MOVE FOR RL BOT")
            #collect list of impossible moves
            impos_moves_list = []
            for i in range(0,len(board[0])):
                if board[0][i] == 0:                    
                     impos_moves_list.append(i)

            r = random.random()
            if r >= self.random_move_prob:
                
                #chose best option 
                r = self.moves_dict[str(board)]["reward"]
                reward_list = [abs(ele) for ele in r]
                max_ = max(reward_list)
                indices = [index for index, value in enumerate(reward_list) if value == max_]

                index = random.randint(0,len(indices)-1)
                move = indices[index]
                if move in impos_moves_list:
                    move = self.smartest_move([[0],board[0], [0], board[1]])
            else:
                #explore
                move = self.smartest_move([[0],board[0], [0], board[1]])
            
        else:
            #if we havent seen the move before then play randomly 
            if self.training_mode:
                self.moves_dict[str(board)] = {}
                self.moves_dict[str(board)]["reward"] = [0,0,0,0,0,0]
                self.moves_dict[str(board)]["frequency"] = 1
            else:
                # move = random.randint(0,5)
                move = self.smartest_move([[0],board[0], [0], board[1]])

        return move

    def set_impossible_moves_to_0(self, board):
        if len(self.moves_dict) > 0 and str(board) in self.moves_dict:
            self.seen_move_count += 1
            for i in range(0,len(board[0])):
                if board[0][i] == 0:                    #CHANGED TEMPORARILY 1-> 0
                    self.moves_dict[str(board)]["reward"][i] = 0
        else:
            #if we havent seen the move before then play randomly 
            if self.training_mode:
                self.moves_dict[str(board)] = {}
                self.moves_dict[str(board)]["reward"] = [0,0,0,0,0,0]
                self.moves_dict[str(board)]["frequency"] = 1

        


    def update_dict(self, board, move:int, points):
    
        if self.player_type == "RL" and self.training_mode:
            self.move_log.append(str(board))
            self.reward_log.append(points)
            self.action_log.append(move)
            self.moves_dict[str(board)]["frequency"] += 1
        else:
            None



    def end_game_update(self, is_winner):
        if self.player_type == "RL" and self.training_mode:
            for m in range(len(self.move_log)-1, -1, -1):
                board = self.move_log[m]
                move = self.action_log[m]
                points = self.reward_log[m]
                if is_winner:
                    cur_game_score = points + 10*(self.end_discount**(len(self.move_log)-m))
                        
                else:
                    cur_game_score = points 

                self.moves_dict[board]["reward"][move] = self.moves_dict[board]["reward"][move]*0.75 + cur_game_score*0.25



        if not self.tournament:
            if self.player_type == "RL" and self.training_mode:
                self. update_pickle_file()


    def collect_final_dict(self):
        return self.moves_dict
    
    def smartest_move(self, board):
        move = None
        move = self.check_for_capture(board)
        if move == None:
            move = self.check_for_goal(board)
        if move == None:
            move = self.chose_high_marble_count(board)
        return move


    def check_for_capture(self, board):
        
        if self.player_side == "top":
            index = 1 
            if 0 not in board[index]:
                return None
            else:
                for i in range(0, len(board[index])):
                    marbles = board[index][i]
                    if marbles != 0 and  marbles < i+1 and board[index][i-marbles] == 0 and board[3][i-marbles] != 0:
                        #capture identified
                        return i
        else:
            index = 3
            if 0 not in board[index]:
                return None
            else:
                for i in range(0, len(board[index])):
                    marbles = board[index][i]
                    if marbles !=0 and marbles < 6-i and board[index][i+marbles] == 0 and board[1][i+marbles] != 0:
                        #capture identified
                        return i
                    

        return None

    
    def check_for_goal(self, board):
        if self.player_side == "top":
            index = 1 
            for i in range(0, len(board[index])):
                if board[index][i] == i+1:
                    return i
        else:
            index = 3
            for i in range(0, len(board[index])):
                if board[index][i] + i == 6:
                    return i
       
        return None
    
    def chose_high_marble_count(self, board):
        if self.player_side == "top":
            index = 1 
        else:
            index = 3

        max_val = 0
        max_index = 0
        for i in range(0, len(board[index])):
            if board[index][i] > max_val:
                max_val = board[index][i]
                max_index = i
        return max_index
    
    def create_new_pickle(self):
        mancala_moves_dict = {}
        with open(self.file, 'wb') as handle:
            pickle.dump(mancala_moves_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load_pickle (self):
        try:
            if os.path.getsize(self.file) > 0:               #TODO this line needs to check for the existance of a picke file (not just if empty)
                with open(self.file, 'rb') as handle:
                    print("Loading pickle file ...")
                    self.moves_dict = pickle.load(handle)
            else:
                self.moves_dict = {}
        except:
            self.create_new_pickle()
            self.moves_dict = {}
            

    def update_pickle_file(self):
        print("saving Pickle")
        with open(self.file, 'wb') as handle:
            pickle.dump(self.moves_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    



                

    


#initialize mancala moves dict
# mancala_moves_dict = {}
# with open('models/mancala_moves_dict_a_0.75.pickle', 'wb') as handle:
#     pickle.dump(mancala_moves_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
