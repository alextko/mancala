import pickle
import os



def check_pickle_size(file):
    if os.path.getsize(file) > 0:
            with open(file, 'rb') as handle:
                print("Loading pickle file ...")
                moves_dict = pickle.load(handle)
    print("There are " + str(len(moves_dict.keys())) + " states in the dictionary ")


pickle_file = "models/mancala_moves_dict_a_75.pickle"
check_pickle_size(pickle_file)