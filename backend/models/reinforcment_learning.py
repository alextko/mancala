# import gymnasium as gym
# from mancala import Mancala_game
# from player import Player
import pickle
import os
import pandas as pd



# file = "./RL_model_top_4.pickle"
f1 = "./p1_1.pickle"
f2 = "./p1_2.pickle"
f3 = "./p1_3.pickle"
f4 = "./p1_4.pickle"

################ Helper functions ############



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



def view_pickle(file, num_view):
    f = load_pickle(file)

    count = 0
    for i in f.keys():
        print("\nKEY " + str(i) + " \n VALUE"  + str(f[i]) + "\n\n")
        count +=1
        if count == num_view:
            break

    


def clean_pickle(file):
    f = load_pickle(file)
    size = len(f.keys())

    if len(size > 50000000):
        #clean out the 10 million least common states
        
        for i in f.keys():
            None


def combine_pickles(f1, f2, f3, f4):
    file_1 = load_pickle(f1)
    file_2 = load_pickle(f2)
    file_3 = load_pickle(f3)
    file_4 = load_pickle(f4)

    combined_dict = {}
    for i in file_1.keys():
        combined_dict[i] = file_1[i]
    for i in file_2.keys():
        combined_dict[i] = file_2[i]
    for i in file_3.keys():
        combined_dict[i] = file_3[i]
    for i in file_4.keys():
        combined_dict[i] = file_4[i]

    save_pickle("trained_pickle.pickle", combined_dict)

def show_me_the_pickle(file, count):
    dict = load_pickle(file)
    c = 0
    for i in dict.keys():
        while c <= count:

            c+=1


    


    


# view_pickle(file,2)
# check_pickle_size(file)
# combine_pickles(f1,f2,f3,f4)





