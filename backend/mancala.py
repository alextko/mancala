from player import Player




class Mancala_game:
    def __init__(self, player1, player2, tournament = False):
        self.board = None
        self.player1 = player1
        self.player2 = player2
        self.score_player1 = 0 
        self.score_player2 = 0
        self.is_complete = False
        self.repeat_turn = False
        self.winner = None
        self.cur_player = None
        self.set_player_side(self.player1)
        self.set_player_side(self.player2)
        self.tournament = tournament
        self.training_mode = False

    def set_player_side(self, p):
        if  p == self.player1:
            p._player_side("top")
        else:
            p._player_side("bottom")

        

    def build_board(self):
        self.board = [[0],[4,4,4,4,4,4],[0],[4,4,4,4,4,4]]

    def move(self, player, move = None, player_type=None):
        if move == None and (player_type== None or player_type == "Smart" or player_type == "Random" or player_type == "RL"):
            valid_move = False
            while not valid_move and not self.is_complete:
                move = player.generate_move(self.board)         
                valid_move = self.check_valid_move(player, move)
                
        self.update_board(player, move)



    def check_valid_move(self, player, move): 
        is_valid = True
        if player == self.player1:
            current_i = 1
        else:
            current_i = 3

        current_j = move
        if type(move) != int or move < 0 or move > 5 or self.board[current_i][current_j] == 0:
            if player.player_type == "Normal":
                print("Invalid move, move should be an int 0-5 & cannot be empty")
            is_valid = False
        return is_valid
            
        
    

    def return_board(self):
        return self.board
    
    def print_helper(self, message):
        print(message)


    def pretty_print_board(self):
        print ("\n *********************************** \n")
        print ( "             " + self.player1.player_name + "        ")
        print ("      "+  str(self.board[1])  + "        ")
        print ( str(self.board[0]) + "                        " + str(self.board[2])) 
        print ("      " + str(self.board[3]) +"        ")
        print ( "             " + self.player2.player_name + "        ")
        print ("\n *********************************** \n")
        print(" Score: "+ self.player1.player_name + ": " + str(self.score_player1) \
              + " " + self.player2.player_name + ": " + str(self.score_player2)  + " \n")
 


    def update_board(self, player, move):
        self.repeat_turn = False
        points_scored = 0
        capture_points = 0
        repeat_turn_points = 0
        pre_move_state = str(self.board)

        if player == self.player1:
            current_i = 1
        else:
            current_i = 3

        current_j = move
        #Player 1 is always on top
        #make the move on the board
        num_marbles = self.board[current_i][move]
        self.board[current_i][move] = 0
        count = 0
        while count < num_marbles:
            if current_i == 1:
                if current_j ==0:
                        if player == self.player2: #check if the goal needs to be skipped
                            current_i = 3
                            current_j = 0
                        else:
                            current_i-=1
                            points_scored += 1
                else:
                    current_j -=1
            elif current_i == 0:
                current_i = 3
                current_j = 0
            elif current_i == 2:
                current_i = 1
                current_j = 5
            elif current_i == 3:
                if current_j == 5:
                        if player == self.player1: #check if the goal needs to be skipped
                            current_i = 1
                            current_j = 5
                        else:
                            current_i -= 1
                            current_j = 0
                            points_scored +=1
                else:
                    current_j += 1
            self.board[current_i][current_j] +=1
            count+=1

        #Check for special cases or replay
        if player == self.player1:
            if current_i == 1:
                if self.board[current_i][current_j] == 1 and self.board[3][current_j] != 0:
                    capture_points += self.board[3][current_j]
                    self.board[0][0] += self.board[current_i][current_j] + self.board[3][current_j]
                    self.board[current_i][current_j] = 0
                    self.board[3][current_j] = 0 
                    # self.repeat_turn = True
                    # repeat_turn_points = 1
                    if not self.tournament:
                        print( str(self.player1.player_name) + " gets a repeat turn \n")
            if current_i == 0:
                self.repeat_turn = True
                repeat_turn_points = 1
                if not self.tournament:
                    print( str(self.player1.player_name) + " gets a repeat turn \n")

        else:
            if current_i == 3:
                if self.board[current_i][current_j] == 1 and self.board[1][current_j] != 0:
                    capture_points += self.board[1][current_j]
                    self.board[2][0] += self.board[current_i][current_j] + self.board[1][current_j]
                    self.board[current_i][current_j] = 0
                    self.board[1][current_j] = 0 
                    # self.repeat_turn = True
                    # repeat_turn_points = 1
                    if not self.tournament:
                        print( str(self.player2.player_name) + " gets a repeat turn \n")
            if current_i == 2:
                self.repeat_turn = True
                repeat_turn_points = 1
                if not self.tournament:
                    print( str(self.player2.player_name) + " gets a repeat turn \n")


        # check if P1's board is empty
        is_done = True
        for i in self.board[1]:
            if i != 0:
                is_done = False
        if is_done == True:
            self.is_complete = True 
            # clean up other side
            sum = 0
            for i in range(0,len(self.board[3])):
                sum += self.board[3][i]
                self.board[3][i] = 0 
            self.board[2][0] += sum        

        if not is_done: #check if p2 board is empty
            is_done = True 
            for i in self.board[3]:
                if i != 0:
                    is_done = False
            if is_done == True:
                self.is_complete = True 
                # clean up other side
                sum = 0
                for i in range(0,len(self.board[1])):
                    sum += self.board[1][i]
                    self.board[1][i] = 0 
                self.board[0][0] += sum    

        #update scores 
        self.score_player1 = self.board[0][0]
        self.score_player2 = self.board[2][0]
        
        #update player understanding
        self.update_points(pre_move_state, move, player, points_scored, capture_points, repeat_turn_points)

        if not self.tournament:
            self.pretty_print_board()

        
        if self.is_complete:
            if self.score_player1 > self.score_player2:
                self.winner = self.player1
                self.player1.end_game_update(True)
                self.player2.end_game_update(False)
            else:
                self.winner = self.player2
                self.player1.end_game_update(False)
                self.player2.end_game_update(True)

            if not self.tournament:
                print("    !!!!!!!!!!!!!!        ")
                print(" \n   ~ WINNER: " + str(self.winner.player_name) +  " ~      \n ")
                print("    !!!!!!!!!!!!!!       \n ")


    def update_points(self, pre_move_state, move, player, points_scored, capture_points, repeat_turn):
        total_score = 0 
        capture_multiplier = 2 
        repeat_turn_multiplier  = 2
        total_score += points_scored + capture_points*capture_multiplier + repeat_turn*repeat_turn_multiplier

        if self.training_mode:
            player.update_dict(pre_move_state, move, total_score)

    def update_cur_player(self):
        if self.cur_player == self.player1:
            self.cur_player = self.player2
        else:
            self.cur_player = self.player1

    def start_game(self):
        # this function is for playing mancala from the UI
        self.build_board()
        self.cur_player = self.player1

        return self.board, self.cur_player

    
    def app_make_move(self, move = None, player_type = None):
        # make move from the UI
        self.move(self.cur_player, move, player_type)
        if self.repeat_turn != True:
            self.update_cur_player()

        return self.winner, self.cur_player, self.board


    def play_game(self):
        #this funciton is for playing mancala from the term
        if not self.tournament:
            print("\n Starting Mancala game with players: " + self.player1.player_name + " and " + self.player2.player_name + "\n")

        self.build_board()
        if not self.tournament:
            self.pretty_print_board()
        while not self.is_complete:
            self.move(self.player1)
            while self.repeat_turn:
                if self.is_complete:
                    break
                self.move(self.player1)
            if self.is_complete:
                break
            
            self.move(self.player2)
            while self.repeat_turn:
                if self.is_complete:
                    break
                self.move(self.player2)
                


    


# print(" \n Hello Welcome to Mancala :) \n ")
# player1 = Player("RL", "rl bot", training_mode=False, tournament= False)
# player2 = Player("Smart", "smart", training_mode=False, tournament= False)

# mancala_game = Mancala_game(player1, player2)
# mancala_game.play_game()





 