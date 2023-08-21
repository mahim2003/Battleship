# Constants
CARD_WIDTH = 125
CARD_HEIGHT = 75
CARD_GAP = 15
MAX_CARDS = 5


class Card:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.is_clicked = False  # Not to be confused with Button's isClicked method

    def clone(self):
        return Card(self.name, self.description)

        # Add more cases for new action cards as needed, must update the CardPrototype list in Player


class CardPrototype:
    def __init__(self, name, description):
        self.prototype = Card(name, description)

    def clone(self):
        return self.prototype.clone()







