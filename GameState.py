import pygame
from Configuration import Configuration
from Gameplay import Gameplay
from SettingsMenu import *
import sys

# GameState subclasses decide how to handle input based on substate
class GameState:
    def handle_input(self, screen, main_menu, game_settings):
        pass


class LoginState(GameState):
    def handle_input(self, screen, main_menu, game_settings):
        login_result, username = self.login_sequence(screen, main_menu)
        if login_result == "logged":
            print("Transitioning to main_menu")
            return MainMenuState(username)
        return self

    def login_sequence(self, screen, main_menu):
        login, username = main_menu.loginScreen(screen)
        if login == "quit":
            pygame.quit()
            sys.exit()
        while login == "sign_up" or login == "reset_password":
            logged = main_menu.inputScreen(screen, login == "reset_password")
            if logged:
                login, username = main_menu.loginScreen(screen)
        return login, username


class MainMenuState(GameState):
    def __init__(self, username):
        self.username = username

    def handle_input(self, screen, main_menu,  game_settings):
        menu_result, level, game_info = self.main_menu_sequence(screen, main_menu)
        if menu_result and game_info is None and level is not None:
            print("Transitioning to configuration")
            return ConfigurationState(level, game_settings, self.username)
        elif menu_result and game_info is not None:
            return GameplayState(game_info[0][0], level, game_info, self.username)
        elif menu_result and level is None and game_info is None:
            pygame.quit()
            sys.exit()
        return self

    def main_menu_sequence(self, screen, main_menu):
        play_pressed, level, game_info = main_menu.createMainMenu(screen, self.username)
        return play_pressed, level, game_info

class ConfigurationState(GameState):
    def __init__(self, level, game_settings, username):
        self.level = level
        self.game_settings = game_settings
        self.username = username

    def handle_input(self, screen, main_menu,  game_settings):
        config_result, player_positions = self.configuration_sequence(screen)
        if config_result == "go_to_gameplay":
            print("Transitioning to gameplay")
            return GameplayState(player_positions, self.level, None, self.username)
        elif config_result == "back_to_main_menu":
            print("Transitioning back to main_menu (from configuration)")
            return MainMenuState(self.username)
        elif config_result == "back_to_settings":
            print("Transitioning back to settings (from configuration)")
            return SettingsState([], "configuration", self.username)
        elif config_result == "quit":
            pygame.quit()
            sys.exit()
        return self

    def configuration_sequence(self, screen):
        configuration = Configuration(self.game_settings)
        config_over = configuration.display(screen)
        return config_over, configuration.getPlayerPositions()


class GameplayState(GameState):
    def __init__(self, player_positions, level, game_info, username):
        self.player_positions = player_positions
        self.level = level
        self.game_info = game_info
        self.username = username

    def handle_input(self, screen, main_menu, game_settings):
        gameplay_result = self.gameplay_sequence(screen, game_settings)
        if gameplay_result == "back_to_main_menu" or gameplay_result == "surrendered":
            print("Transitioning back to main_menu (from gameplay)")
            return MainMenuState(self.username)
        elif gameplay_result == "back_to_settings":
            print("Transitioning back to settings (from gameplay)")
            return SettingsState(self.player_positions, "gameplay", self.username)
        elif gameplay_result == "quit":
            pygame.quit()
            sys.exit()
        return self

    def gameplay_sequence(self, screen, game_settings):
        # Assuming empty enemy_positions
        gameplay = Gameplay(self.player_positions, self.level, game_settings, self.username, self.game_info)
        gameplay_result = gameplay.play(screen, self.username)
        return gameplay_result

class SettingsState(GameState):
    def __init__(self, player_positions, current_source, username):
        self.settings_source = current_source
        self.player_postions = player_positions
        self.settings_menu = SettingsMenu()
        self.username = username

    def handle_input(self, screen, main_menu, game_settings):
        return_to_previous_screen, done = self.settings_menu.create_settings_menu(screen,  game_settings, self.username)
        # passes object by reference
        if return_to_previous_screen and self.settings_source == "configuration":
            print("Transitioning back to configuration (from settings)")
            return ConfigurationState(main_menu.level, game_settings, self.username)
        elif return_to_previous_screen and self.settings_source == "gameplay":
            print("Transitioning back to gameplay (from settings)")
            return GameplayState(self.player_postions, game_settings.ai_difficulty_index +1, main_menu.game_state_info, self.username)

# Game state manager called in client code game.py
def game_state_manager(screen, main_menu, current_state, game_settings):
    state = LoginState()

    while current_state != "quit":
        state = state.handle_input(screen, main_menu, game_settings)

    pygame.quit()