# ----------------------------------------------------------------------------------------------------------------------
import pickle


def pickle_in(obj_name, obj):
    with open(obj_name + '.pkl', 'wb') as pickle_file:
        pickle.dump(obj, pickle_file)


# ----------------------------------------------------------------------------------------------------------------------
def pickle_out(obj_name):
    with open(obj_name + '.pkl', 'rb') as pickle_file:
        return pickle.load(pickle_file)
