from Button import Button
import pygame
import time

# Colors
BLACK = (0, 0, 0)
DARKERGREY = (50, 50, 50)
DARKGREY = (100, 100, 100)
GREY = (200, 200, 200)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
LIGHTBLUE = (173, 216, 230)

LIGHT_MODE_COLORS = {
    'background': (174, 198, 208),
    'display_text': (0, 0, 0),
    'input_text': (0, 0, 0),
    'rect': (255, 255, 255),
    'board': (125, 125, 125),
    'hovered': (100, 100, 100),
    'ships': (200, 200, 200),
}

DARK_MODE_COLORS = {
    'background': (19, 41, 72),  #(52, 78, 91),
    'display_text': (255, 255, 255),  # (200, 200, 200),
    'input_text': (0, 0, 0),  # (240, 240, 240),
    'rect': (200, 200, 200),
    'board': (100, 100, 100),
    'hovered': (200, 200, 200),
    'ships': (150, 150, 150),
}

# Constants
CARD_WIDTH = 125
CARD_HEIGHT = 75
CARD_GAP = 15
MAX_CARDS = 5


class Gameboard:
    def __init__(self, game_settings):
        self.enemyGrid = []
        self.playerGrid = []
        self.game_settings = game_settings
        self.selected_action = None
        if not self.game_settings.theme:
            CURRENT_MODE_COLORS = DARK_MODE_COLORS
        else:
            CURRENT_MODE_COLORS = LIGHT_MODE_COLORS

        self.button_dict = {
            "Main Menu": Button(40, 50, 120, 40, None),
            "Settings": Button(40, 100, 120, 40, None),
            "Save Game": Button(40, 150, 120, 40, None),
            "Surrender": Button(520, 50, 120, 40, None),
            "End Turn": Button(40, 575, 120, 40, None)
        }

        self.text_list = [
            ("Enemy Grid", 20, 275, 55, CURRENT_MODE_COLORS['display_text']),
            ("Player Grid", 20, 275, 355, CURRENT_MODE_COLORS['display_text']),
            ("Opponent: Level 1 AI", 16, 480, 100, CURRENT_MODE_COLORS['display_text']),
            ("Opp. Ships Remaining: 5", 16, 480, 120, CURRENT_MODE_COLORS['display_text']),
            ("You: Player 1", 16, 480, 160, CURRENT_MODE_COLORS['display_text']),
            ("Your Ships Remaining: 5", 16, 480, 180, CURRENT_MODE_COLORS['display_text'])
        ]
        self.remaining_time=30
        self.start_time=time.time()

    def update_timer(self):
        current_time=time.time()
        elapsed_time= current_time - self.start_time
        self.remaining_time=max(0, 30 - int(elapsed_time))
    
    def reset_timer(self):
        self.start_time=time.time()        

    # Function to display text on the gameboard
    def display_text(self, screen, text, font_size, x, y, color):
    
        font = pygame.font.Font(pygame.font.get_default_font(), font_size)
        text_render = font.render(text, True, color)
        screen.blit(text_render, (x, y))

    # Function to display the main gameplay interface
    def drawScreen(self, screen):
        y1 = 75
        y2 = 375
        for a in ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J"):
            x = 200
            for n in range(1, 11):
                enemyButton = Button(x, y1, 25, 25, (a, n))
                playerButton = Button(x, y2, 25, 25, (a, n))

                self.playerGrid.append(playerButton)
                self.enemyGrid.append(enemyButton)
                x = x + 27

            y1 = y1 + 27
            y2 = y2 + 27

        self.drawGrid(screen)

        for button_name, button in self.button_dict.items():
            button.draw(screen, WHITE, button_name)

        for tuple in self.text_list:
            self.display_text(screen, *tuple)

    # Draws the buttons for the grid on the board
    def drawGrid(self, screen):
        if not self.game_settings.theme:
            CURRENT_MODE_COLORS = DARK_MODE_COLORS
        else:
            CURRENT_MODE_COLORS = LIGHT_MODE_COLORS
        for button in self.enemyGrid:
            button.draw(screen, CURRENT_MODE_COLORS['board'], "") #(100, 100, 100)
        for button in self.playerGrid:
            button.draw(screen, CURRENT_MODE_COLORS['board'], "")


    # Changes player grid colour on hit/miss
    def redrawPlayerGrid(self, screen, hit, position):
        for button in self.playerGrid:
            if button.location == position and hit:
                button.state = "hit"
                button.draw(screen, RED, "")
            elif button.location == position and not hit:
                button.state = "miss"
                button.draw(screen, WHITE, "")

    # Draws player grid based on grid elem state
    def updatePlayerGrid(self, screen, positions):
        if not self.game_settings.theme:
            CURRENT_MODE_COLORS = DARK_MODE_COLORS
        else:
            CURRENT_MODE_COLORS = LIGHT_MODE_COLORS
        for button in self.playerGrid:
            if button.isHovered(pygame.mouse.get_pos()) and button.location in positions:
                button.draw(screen, CURRENT_MODE_COLORS['hovered'], "")  # Light grey color when hovered GREY
            elif button.state == "normal":
                button.draw(screen, CURRENT_MODE_COLORS['board'], "")  # Dark grey -> normal DARKGREY
            elif button.state == "player position":
                button.draw(screen, CURRENT_MODE_COLORS['ships'], "")  # (150, 150, 150)
            elif button.state == "shield":
                button.draw(screen, LIGHTBLUE, "")
            elif button.state == "selected":
                button.draw(screen, ORANGE, "")
            elif button.state == "hit":
                button.draw(screen, RED, "")
            elif button.state == "miss":
                button.draw(screen, WHITE, "")
            else:
                continue
        pygame.display.flip()
    
    # Update enemy button state on hover, and colour based on button state
    def UpdateButtons(self, screen):
        if not self.game_settings.theme:
            CURRENT_MODE_COLORS = DARK_MODE_COLORS
        else:
            CURRENT_MODE_COLORS = LIGHT_MODE_COLORS

        for button in self.enemyGrid:

            if button.isHovered(pygame.mouse.get_pos()) and button.state == "normal":

                if self.selected_action == "bomb":
                    # Highlight the 3x3 buttons
                    buttons_3x3 = self.get_3x3_buttons(button)
                    for btn in buttons_3x3:
                        btn.draw(screen, CURRENT_MODE_COLORS['hovered'] , "")  # Hover color 3x3 cells for bomb  GREY
                else:
                    button.draw(screen, CURRENT_MODE_COLORS['hovered'], "")  # Hover color single cell  GREY

            elif button.state == "normal":
                button.draw(screen, CURRENT_MODE_COLORS['board'], "")  # Dark grey -> normal DARKGREY

            elif button.state == "selected":
                button.draw(screen, ORANGE, "")  # Orange -> hovered

            elif button.state == "hit":
                button.draw(screen, RED, "")  # Red -> hit
            elif button.state == "miss":
                button.draw(screen, WHITE, "")  #  White -> miss
            else:
                continue

        pygame.display.flip()
    
    # used for bomb action card
    def get_3x3_buttons(self, center_button):
        buttons_3x3 = []
        center_index = self.enemyGrid.index(center_button)
        center_row = center_index // 10
        center_col = center_index % 10

        for row_offset in range(-1, 2):
            for col_offset in range(-1, 2):
                row = center_row + row_offset
                col = center_col + col_offset
                if 0 <= row < 10 and 0 <= col < 10:
                    index = row * 10 + col
                    buttons_3x3.append(self.enemyGrid[index])

        return buttons_3x3
    
    # testing, just for player grid
    def find_button_by_location(self, target_location):
        for button in self.playerGrid:
            if button.location == target_location:
                return button
        return None  # Button not found

    # Changes enemy button colour on hit/miss
    def redrawButton(self, screen, button, hit):
        if hit:
            # button.state = "hit"
            button.draw(screen, RED, "")
        else:
            # button.state = "miss"
            button.draw(screen, WHITE, "")

    # Draw for setup
    def drawPlayerLocation(self, screen, positions):
        if not self.game_settings.theme:
            CURRENT_MODE_COLORS = DARK_MODE_COLORS
        else:
            CURRENT_MODE_COLORS = LIGHT_MODE_COLORS
        for position in positions:
            for button in self.playerGrid:
                if button.location == position:
                    button.state = "player position"
                    button.draw(screen, CURRENT_MODE_COLORS["ships"], "")

    # Gets the button and location of the pressed button
    def get_clickedLocation(self, mouse_pos, guess):
        if guess:
            for button in self.enemyGrid:
                if button.isClicked(mouse_pos):
                    location = button.get_location()
                    return button, location
        else:
            for button in self.playerGrid:
                if button.isClicked(mouse_pos):
                    location = button.get_location()
                    return button, location

    def get_grids(self):
        return self.playerGrid, self.enemyGrid
