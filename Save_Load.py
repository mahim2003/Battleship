import pickle


def save_game(obj):
    with open("saveGame", "wb") as file:
        pickle.dump(obj, file)


def load_game():
    with open("saveGame", "rb") as file:
        obj = pickle.load(file)
        return obj
