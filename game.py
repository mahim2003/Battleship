import pygame
from Mainmenu import Mainmenu
from GameState import *
from SettingsMenu import *

# Constants
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 750

# Main
def main():

    # Initialize Game
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game_settings = SettingsState()
    main_menu = Mainmenu(game_settings)
    current_state = "login"

    # Run game
    game_state_manager(screen, main_menu, current_state, game_settings)

# Execute
if __name__ == "__main__":
    main()