from Board import Gameboard
from Player import Player
from AI import AI
from GameContext import GameContext
import pygame
import random
from DatabaseHelper import *
from Save_Load import *

# Constants
CARD_WIDTH = 125 
CARD_HEIGHT = 75

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 750

CARD_GAP = 15
MAX_CARDS = 5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKERGREY = (50, 50, 50)
DARKGREY = (100, 100, 100)
GREY = (150, 150, 150)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
LIGHTBLUE = (173, 216, 230)

LIGHT_MODE_COLORS = {
    'background': (174, 198, 208),
    'display_text': (0, 0, 0),
    'input_text': (0, 0, 0),
    'rect': (255, 255, 255),
}

# New dark mode colors:
DARK_MODE_COLORS = {
    'background': (19, 41, 72),  #(52, 78, 91),
    'display_text': (255, 255, 255),  # (200, 200, 200),
    'input_text': (0, 0, 0),  # (240, 240, 240),
    'rect': (200, 200, 200),
}

CURRENT_MODE_COLORS = DARK_MODE_COLORS

class Gameplay:
    # Initializer for running the main gameplay
    def __init__(self, player_positions, level, game_settings, username, game_info):
        self.game_settings = game_settings
        #self.music_state = music_state
        self.level = level
        self.game_info = game_info
        self.player_ship_positions = player_positions

        self.ship_positions_dict = {
            "carrier": (5, [], []),
            "battleship": (4, [], []),
            "destroyer": (3, [], []),
            "submarine": (3, [], []),
            "patrolboat": (2, [], []),
        }
        self.AI_ship_dict = {
            "carrier": (5, [], []),
            "battleship": (4, [], []),
            "destroyer": (3, [], []),
            "submarine": (3, [], []),
            "patrolboat": (2, [], []),
        }
        self.AI_ship_positions = []
        self.player_remaining_ships = 5
        self.ai_remaining_ships = 5

        self.AI_alreadyGuessed = []

        self.context = GameContext(self, Gameboard(self.game_settings), Player(), AI())
        self.clock = pygame.time.Clock()
        self.generate_random_positions()
        self.turn = "Your turn"
        self.inst = "Press enemy grid to attack "
        self.cardDrawn = False
        self.Finished = False
        self.username = username

    def player_ship_sunk(self, position):
        ship_type = None
        if position is not None:
            for ship, (size, positions, position_sunk) in self.ship_positions_dict.items():
                if position in positions and position not in position_sunk:
                    button = self.context.gameboard.find_button_by_location(position)
                    if button.state != "shield":
                        position_sunk.append(position)
                        ship_type = ship
                        break
            if ship_type:
                if self.ship_positions_dict[ship_type][0] == len(self.ship_positions_dict[ship_type][2]):
                    self.player_remaining_ships -= 1
        else:
            for ship, (size, positions, positons_sunk) in self.ship_positions_dict.items():
                if len(positons_sunk) >= size:
                    self.player_remaining_ships -= 1

    def ai_ship_sunk(self, position):
        ship_type = None
        if position is not None:
            for ship, (size, positions, positions_sunk) in self.AI_ship_dict.items():
                if position in positions and position not in positions_sunk:
                    positions_sunk.append(position)
                    ship_type = ship
                    break
            if ship_type:
                if len(self.AI_ship_dict[ship_type][1]) == len(self.AI_ship_dict[ship_type][2]):
                    self.ai_remaining_ships -= 1
        else:
            for ship, (size, positions, positons_sunk) in self.AI_ship_dict.items():
                if len(positons_sunk) >= size:
                    self.ai_remaining_ships -= 1

    def restore_ship_position(self, position, AI):
        if AI:
            ships = self.AI_ship_dict.items()
        else:
            ships = self.ship_positions_dict.items()

        for ship, (size, positions, positions_sunk) in ships:
            if position in positions_sunk:
                if len(positions_sunk) == len(positions):
                    if AI:
                        self.ai_remaining_ships += 1
                    else:
                        self.player_remaining_ships += 1
                positions_sunk.remove(position)
                break


    def generate_random_positions(self):
        ship_types = {
            "carrier": 5,
            "battleship": 4,
            "destroyer": 3,
            "submarine": 3,
            "patrolboat": 2,
        }

        possible_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

        for ship_type, size in ship_types.items():
            valid_position = False

            while not valid_position:
                letter = random.choice(possible_letters)
                number = random.randint(1, 10)

                # Generate random orientation (horizontal or vertical)
                is_horizontal = random.choice([True, False])

                # Generate possible ship positions based on orientation and size
                positions = []
                for i in range(size):
                    if is_horizontal and possible_letters.index(letter) + i < len(possible_letters):
                        positions.append((possible_letters[possible_letters.index(letter) + i], number))
                    elif not is_horizontal and number + i <= 10:
                        positions.append((letter, number + i))
                    else:
                        # Skip generating invalid positions and try again
                        break

                if len(positions) == size:
                    # Check if the positions are valid (not overlapping with AI's existing ship positions)
                    if all(pos not in self.AI_ship_positions for pos in positions):
                        valid_position = True
                        self.AI_ship_positions.extend(positions)  # Add the ship positions to the AI's ship positions list

        self.positions_to_dict(self.AI_ship_dict, self.AI_ship_positions)

    # Initial game setup
    def setup(self, screen):
        if not self.game_settings.theme:
            CURRENT_MODE_COLORS = DARK_MODE_COLORS
        else:
            CURRENT_MODE_COLORS = LIGHT_MODE_COLORS
        screen.fill(CURRENT_MODE_COLORS['background'])
        self.context.gameboard.drawScreen(screen)
        if self.game_info is None:
            self.context.gameboard.drawPlayerLocation(screen, self.player_ship_positions)
            self.positions_to_dict(self.ship_positions_dict, self.player_ship_positions)
        else:
            self.player_ship_positions = self.game_info[0][0]
            self.AI_ship_positions = self.game_info[0][1]
            self.level = self.game_info[0][2]
            self.context.gameboard.drawPlayerLocation(screen, self.player_ship_positions)
            self.positions_to_dict(self.ship_positions_dict, self.player_ship_positions)
            self.context.gameboard.playerGrid = self.game_info[2][0]
            self.context.gameboard.updatePlayerGrid(screen, self.player_ship_positions)
            self.context.gameboard.enemyGrid = self.game_info[2][1]
            self.context.gameboard.UpdateButtons(screen)
            self.context.player.hand = self.game_info[4]
            self.context.AI.alreadyGuessed = self.game_info[3]
            self.ship_positions_dict = self.game_info[1][0]
            self.AI_ship_dict = self.game_info[1][1]
            self.ai_ship_sunk(None)
            self.player_ship_sunk(None)
            self.username = self.game_info[5]

    # Check if position (which is stored in Button.location attribute as a tuple: (A, 1)) is one of the
    # opponent or player's ships
    def detect_hit(self, position, opponent):
        if opponent:
            positions = self.player_ship_positions
        else:
            positions = self.AI_ship_positions

        if position in positions:
            if self.game_settings.music_intensity == "relaxed":  # self.music_state
                hitSound = pygame.mixer.Sound("soundEffects/chillHitSound.mp3")
            else:
                hitSound = pygame.mixer.Sound("soundEffects/hit_sound.mp3")

            hitSound.set_volume(self.game_settings.sound_effects_volume)
            print("5 Sound Effects Volume passed:", self.game_settings.sound_effects_volume)
            vol = hitSound.get_volume()
            print("6 Sound Effects Volume actual:", vol)
            hitSound.play()
            if opponent:
                if self.context.gameboard.find_button_by_location(position).state != "shield":
                    self.player_ship_sunk(position)
            else:
                self.ai_ship_sunk(position)
            return True

        else:
            if self.game_settings.music_intensity == "relaxed": #  self.music_state
                missSound = pygame.mixer.Sound("soundEffects/chillMissSound.mp3")
            else:
                missSound = pygame.mixer.Sound("soundEffects/miss_sound.mp3")

            missSound.set_volume(self.game_settings.sound_effects_volume)
            print("11 Sound Effects Volume passed:", self.game_settings.sound_effects_volume)
            vol = missSound.get_volume()
            print("12 Sound Effects Volume actual:", vol)
            missSound.play()
            return False

    # Game logic
    def check_win_conditions(self, username):
        if self.player_remaining_ships == 0:
            updateStats(username, False)
            return "AI"
        elif self.ai_remaining_ships == 0:
            updateStats(username, True)
            return "Player"
        else:
            return None

    def display_win_message(self, screen, winner):
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 82)
        if winner == "Player":
            message = font.render("Player wins!", True, GREEN)
        elif winner == "AI":
            message = font.render("AI wins!", True, RED)
        else:
            return

        screen.blit(message, (SCREEN_WIDTH / 2 - message.get_width() / 2, SCREEN_HEIGHT / 2))
        pygame.display.flip()

    # play sound effect only once 
    def detect_bomb_hit(self, screen, buttons_3x3):
        sound_effect_played = False
        for button in buttons_3x3:

            if button.location in self.AI_ship_positions:
                self.ai_ship_sunk(button.location)
                if not sound_effect_played:
                    if self.game_settings.music_intensity == "relaxed": # self.music_state
                        hitSound = pygame.mixer.Sound("soundEffects/chillHitSound.mp3")
                    else:
                        hitSound = pygame.mixer.Sound("soundEffects/hit_sound.mp3")

                    hitSound.set_volume(self.game_settings.sound_effects_volume)
                    print("1 Sound Effects Volume passed:", self.game_settings.sound_effects_volume)
                    vol = hitSound.get_volume()
                    print("2 Sound Effects Volume actual:", vol)
                    hitSound.play()
                    sound_effect_played = True
                self.context.gameboard.redrawButton(screen, button, True)  # Hit
                button.state = "hit"

            else:
                if not sound_effect_played:

                    if self.game_settings.music_intensity == "relaxed": #  self.music_state
                        missSound = pygame.mixer.Sound("soundEffects/chillMissSound.mp3")
                    else:
                        missSound = pygame.mixer.Sound("soundEffects/miss_sound.mp3")

                    missSound.set_volume(self.game_settings.sound_effects_volume)
                    print("3 Sound Effects Volume passed:", self.game_settings.sound_effects_volume)
                    vol = missSound.get_volume()
                    print("4 Sound Effects Volume actual:", vol)
                    missSound.play()
                    sound_effect_played = True

                self.context.gameboard.redrawButton(screen, button, False)  # Miss
                button.state = "miss"

    def switch_to_ai_turn(self):
        self.turn = "AI's turn"
        self.inst = "AI thinking..."
        self.context.gameboard.reset_timer()

    def switch_to_player_turn(self):
        self.cardDrawn = False
        self.turn = "Your turn"
        self.inst = "Pick a card to play"
        self.context.gameboard.reset_timer()

    def ai_turn(self, screen, level):
        AI.play_card(self.context.AI, screen, self.context, level)
        self.switch_to_player_turn()

    def player_turn(self, screen):
        turnStatus = pygame.font.Font(pygame.font.get_default_font(), 25)
        instruction = pygame.font.Font(pygame.font.get_default_font(), 15)
        # Draw card
        if not self.cardDrawn:
            self.context.player.add_card_to_hand()
            self.cardDrawn = True

        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.context.player.display_hand(screen)

                # Handle card clicks
                for i, card in enumerate(self.context.player.hand):
                    if card.is_clicked:
                        self.context.player.play_card(i, screen, self.context)
                        self.context.player.reset_card_click(card)
                        if pygame.mouse.get_pressed()[2]:
                            self.context.player.hand.pop(i)
                        if not self.context.player.hand:
                            self.switch_to_ai_turn()
                        break

                if self.context.gameboard.button_dict["Main Menu"].isClicked(mouse_pos):
                    save_game(self.context.game_info())
                    return "back_to_main_menu"
                if self.context.gameboard.button_dict["Settings"].isClicked(mouse_pos):
                    save_game(self.context.game_info())
                    return "back_to_settings"
                if self.context.gameboard.button_dict["Save Game"].isClicked(mouse_pos):
                    save_game(self.context.game_info())
                if self.context.gameboard.button_dict["Surrender"].isClicked(mouse_pos):
                    return "surrendered"
                # button functionality on click
                if self.context.gameboard.button_dict["End Turn"].isClicked(mouse_pos):
                    self.switch_to_ai_turn()

        if self.context.gameboard.remaining_time <= 0:
            self.switch_to_ai_turn()
        if not self.game_settings.theme:
            CURRENT_MODE_COLORS = DARK_MODE_COLORS
        else:
            CURRENT_MODE_COLORS = LIGHT_MODE_COLORS
        screen.fill(CURRENT_MODE_COLORS['background'], (0, 650, screen.get_size()[0], 100))
        screen.fill(CURRENT_MODE_COLORS['background'], (0, 0, screen.get_size()[0], 50))
        pygame.draw.rect(screen, CURRENT_MODE_COLORS['background'], (480, 0, 220, 50))

        self.context.player.display_hand(screen)

        turn_status = turnStatus.render(self.turn, True, CURRENT_MODE_COLORS['display_text'])
        screen.blit(turn_status, (screen.get_size()[0] / 2 - 75, 5))

        instruction_text = instruction.render(self.inst, True, CURRENT_MODE_COLORS['display_text'])
        instruction_text_width = instruction_text.get_width()
        # Calculate the x position to center the text horizontally
        instruction_text_x_position = (screen.get_size()[
                                           0] - instruction_text_width) // 2 - 20  # off center to the left a bit

        screen.blit(instruction_text, (instruction_text_x_position, 30))

        self.context.player.display_hand(screen)

        timer_label = "Time Remaining: {}".format(self.context.gameboard.remaining_time)
        self.context.gameboard.display_text(screen, timer_label, 20, 480, 15, CURRENT_MODE_COLORS['display_text'])

    # Main gameplay loop
    def play(self, screen, username):
        self.setup(screen)
        player_remaining_ships_copy = 5
        ai_remaining_ships_copy = 5

        winner = None  # Initialize winner as None
        win_time = 0
        freeze_time = 5000
        while not self.Finished:
            self.context.gameboard.update_timer()
            if not winner and (self.ai_remaining_ships == 0 or self.player_remaining_ships == 0):
                winner = self.check_win_conditions(username)
                if winner:
                    win_time = pygame.time.get_ticks()  # Record the time win condition is met

            if winner:
                self.display_win_message(screen, winner)
                pygame.display.update()
                # Wait for 5 seconds
                current_time = pygame.time.get_ticks()
                if current_time - win_time >= freeze_time:
                    return "back_to_main_menu"
                while pygame.time.get_ticks() - win_time < freeze_time:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            return "quit"

            if self.turn == "AI's turn":
                # self.game_settings
                self.ai_turn(screen, self.level)

            if self.turn == "Your turn":
                gameplay_result = self.player_turn(screen)
                if gameplay_result == "back_to_main_menu":
                    return "back_to_main_menu"
                elif gameplay_result == "back_to_settings":
                    return "back_to_settings"
                elif gameplay_result == "surrendered":
                    return "surrendered"
                elif gameplay_result == "quit":
                    return "quit"

            if not self.game_settings.theme:
                CURRENT_MODE_COLORS = DARK_MODE_COLORS
            else:
                CURRENT_MODE_COLORS = LIGHT_MODE_COLORS

            if ai_remaining_ships_copy != self.ai_remaining_ships:
                screen.fill(CURRENT_MODE_COLORS['background'], (480, 120, 220, 20))
                opp_ships = "Opp. Ships Remaining: {}".format(self.ai_remaining_ships)
                self.context.gameboard.display_text(screen, opp_ships, 16, 480, 120,
                                                    CURRENT_MODE_COLORS['display_text'])
                ai_remaining_ships_copy = self.ai_remaining_ships
            if player_remaining_ships_copy != self.player_remaining_ships:
                screen.fill(CURRENT_MODE_COLORS['background'], (480, 180, 220, 20))
                player_ships = "Your Ships Remaining: {}".format(self.player_remaining_ships)
                self.context.gameboard.display_text(screen, player_ships, 16, 480, 180,
                                                    CURRENT_MODE_COLORS['display_text'])
                player_remaining_ships_copy = self.player_remaining_ships

            pygame.display.update()
            self.clock.tick(20)

        pygame.quit()

    def positions_to_dict(self, dict, positions):
        start = 0
        for key, value in dict.items():
            for i, position in enumerate(positions):
                i = i + start
                value[1].append(positions[i])
                if len(value[1]) == value[0]:
                    start = start + value[0]
                    break

    def return_info(self):
        return self.player_ship_positions, self.AI_ship_positions, self.level

    def return_guesses(self):
        return self.ship_positions_dict, self.AI_ship_dict

