import gymnasium as gym
from mancala import Mancala_game
from player import Player

set_of_actions = [0,1,2,3,4,5]
print(set_of_actions)

mancala_moves_dict = {}
player1 = Player("Random", "bot1")
player2 = Player("Random", "bot2")
mancala = Mancala_game(player1, player2)








