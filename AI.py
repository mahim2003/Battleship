import GameContext
from Card import *
import random
import pygame

# Colors
GREY = (150, 150, 150)
LIGHTBLUE = (173, 216, 230)

class AI:
    def __init__(self):
        self.hand = []
        self.alreadyGuessed = []
        self.card_prototypes = [
            (CardPrototype("Single Shot", "Attack 1 cell"), 0.8),
            (CardPrototype("Triple Shot", "Attack any 3 cells"), 0.19),
            (CardPrototype("Bomb", "Attack 9 in a square"), 0.01),
        ]
    def add_cards_to_hand(self, level):
        for _ in range(level):
            random_value = random.random()
            for prototype, probability in self.card_prototypes:
                if random_value < probability:
                    random_card = prototype.clone()
                    self.hand.append(random_card)
                    break
                random_value -= probability

    def perform_action(self, card, screen, context):
        if card.name == "Single Shot":
            self.perform_shot_action(screen, context, 1)
        if card.name == "Triple Shot":
            self.perform_shot_action(screen, context, 3)
        if card.name == "Bomb":
            self.perform_bomb_action(screen, context)

    def perform_shot_action(self, screen, context, guesses):
        pygame.time.delay(500)
        while guesses > 0:
            target_location = self.guess()
            self.alreadyGuessed.append(target_location)
            self.check_hit(screen, context, target_location)
            if len(self.alreadyGuessed) == len(context.gameboard.playerGrid):
                break
            guesses = guesses - 1
        return

    def perform_bomb_action(self, screen, context):
        pygame.time.delay(500)
        guesses = []
        target_location = self.guess()
        guesses.append(target_location)

        button = context.gameboard.find_button_by_location(target_location)
        center_index = context.gameboard.playerGrid.index(button)
        center_row = center_index // 10
        center_col = center_index % 10

        for row_offset in range(-1, 2):
            for col_offset in range(-1, 2):
                row = center_row + row_offset
                col = center_col + col_offset
                if 0 <= row < 10 and 0 <= col < 10:
                    index = row * 10 + col
                    guesses.append(context.gameboard.playerGrid[index].location)

        for guess in guesses:
            if guess not in self.alreadyGuessed:
                self.alreadyGuessed.append(guess)
            self.check_hit(screen, context, guess)
        return

    def check_hit(self, screen, context, target_location):
        target_button = context.gameboard.find_button_by_location(target_location)
        if context.gameplay.detect_hit(target_location, True):
            if target_button.state == "shield":
                target_button.draw(screen, GREY, "")  # Hit breaks shield, back to player position colour
                target_button.state = "player position"
                print("shield broken")
                AIHitSheildSound = pygame.mixer.Sound("soundEffects/AI_hit_shield_sound.mp3")
                AIHitSheildSound.play()
                # AI can guess this cell again since it only broke the shield
                self.alreadyGuessed.remove(target_location)
                pygame.display.flip()
            else:
                context.gameboard.redrawPlayerGrid(screen, True, target_location)
                target_button.state = "hit"
                pygame.display.flip()
                return True
        else:
            context.gameboard.redrawPlayerGrid(screen, False, target_location)
            target_button.state = "miss"
            pygame.display.flip()
            return False

    def guess(self):
        possibleLetters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        letter = random.choice(possibleLetters)
        number = random.randrange(1, 11)

        while (letter, number) in self.alreadyGuessed:
            letter = random.choice(possibleLetters)
            number = random.randrange(1, 11)

        target_location = (letter, number)
        return target_location

    def challenge_level(self, screen, context):
        target_location = random.choice(context.gameplay.player_ship_positions)
        print(target_location)
        while target_location in self.alreadyGuessed:
            target_location = random.choice(context.gameplay.player_ship_positions)
        self.alreadyGuessed.append(target_location)
        self.check_hit(screen, context, target_location)

    def play_card(self, screen, context, level):
        if level == 4:
            self.challenge_level(screen, context)
        else:
            self.add_cards_to_hand(level)
            while len(self.hand) > 0:
                self.perform_action(self.hand[len(self.hand)-1], screen, context)
                self.hand.remove(self.hand[len(self.hand)-1])








