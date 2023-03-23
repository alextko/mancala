from player import Player




class Mancala_game:
    def __init__(self, player1, player2):
        self.board = None
        self.player1 = player1
        self.player2 = player2
        self.score_player1 = 0 
        self.score_player2 = 0
        self.is_complete = False
        self.winner = None
        

    def build_board(self):
        self.board = [[0],[4,4,4,4,4,4],[0],[4,4,4,4,4,4]]

    def update_board(self, player, move):
        #check for valid move
        if type(move) != int or move < 0 or move > 5:
            print("Invalid move, move should be an int 0-5")
            return

        if player == self.player1:
            current_i = 1
        else:
            current_i = 3

        current_j = move
        #Player 1 is always on top
        #make the move on the board
        num_marbles = self.board[current_i][move]
        print("\n you have " + str(num_marbles) + " marbles \n")
        self.board[current_i][move] = 0
        count = 0
        while count < num_marbles:
            if current_i == 1:
                if current_j ==0:
                        current_i-=1
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
                    current_i -= 1
                    current_j = 0
                else:
                    current_j += 1
            # print("current i: " + str(current_i))
            # print("current j: " + str(current_j))
            self.board[current_i][current_j] +=1
            count+=1

        #Check for special cases 
        if player == self.player1:
            if current_i == 1:
                if self.board[current_i][current_j] == 1 and self.board[3][current_j] != 0:
                    self.board[0][0] = self.board[current_i][current_j] + self.board[3][current_j]
                    self.board[current_i][current_j] = 0
                    self.board[3][current_j] = 0 

        else:
            if current_i == 3:
                if self.board[current_i][current_j] == 1 and self.board[1][current_j] != 0:
                    self.board[0][0] = self.board[current_i][current_j] + self.board[1][current_j]
                    self.board[current_i][current_j] = 0
                    self.board[1][current_j] = 0 

        # check if the game is complete 
        if player == self.player1:
            is_done = True
            for i in self.board[1]:
                if i != 0:
                    is_done = False
            if is_done == True:
                self.is_complete = True 
                # clean up other side
                sum = 0
                for i in len(self.board[3]):
                    sum += self.board[3][i]
                    self.board[3][i] = 0 
                self.board[2][0] += sum        

        if player == self.player2:
            is_done = True
            for i in self.board[3]:
                if i != 0:
                    is_done = False
            if is_done == True:
                self.is_complete = True 
                # clean up other side
                sum = 0
                for i in len(self.board[1]):
                    sum += self.board[1][i]
                    self.board[1][i] = 0 
                self.board[0][0] += sum    

        #update scores 
        self.score_player1 = self.board[0][0]
        self.score_player2 = self.board[2][0]

        
        print("\n UPDATED BOARD \n")
        print(self.board)
        print("\n Score: "+ player1.player_name + ": " + str(self.score_player1) \
              + " " + player2.player_name + ": " + str(self.score_player2)  + " \n")
        
        if self.is_complete:
            if self.score_player1 > self.score_player2:
                self.winner = self.player1
            else:
                self.winner = self.player2
        
            print(" \n WINNER: " + str(self.winner.name) +  " \n ")
 

    def update_score(self):
        None

    def play_game(self):
        print("Starting Mancala game with players: " + player1.player_name + " and " + player2.player_name)
        self.build_board()
        self.update_board(player1, 2)
        self.update_board(player2, 2)


    


print("hello")
player1 = Player("Standard",  0, "Alex")
player2 = Player("Standard", 0)
# print(player1.player_name)
mancala_game = Mancala_game(player1, player2)
mancala_game.play_game()





 