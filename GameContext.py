class GameContext:
    def __init__(self, gameplay, gameboard, player, AI):
        self.gameplay = gameplay
        self.gameboard = gameboard
        self.player = player
        self.AI = AI

    # Used for saving/loading the game
    def game_info(self):
        return (self.gameplay.return_info(), self.gameplay.return_guesses(), self.gameboard.get_grids(),
                self.AI.alreadyGuessed, self.player.hand, self.gameplay.username)