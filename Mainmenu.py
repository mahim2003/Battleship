import pygame.mixer
import sys
from Components import *
from images import *
from SettingsMenu import SettingsMenu
from DatabaseHelper import *
from Save_Load import *
import random

# define colours
BLUE = (50, 50, 255)
BLACK = (0, 0, 0)
DARKGREY = (100, 100, 100)
WHITE = (255, 255, 255)
LIGHT_MODE_COLORS = {
    'background': (174, 198, 208),
    'display_text': (0, 0, 0),
    'input_text': (0, 0, 0),
    'rect': (255, 255, 255),
}

# New dark mode colors:
DARK_MODE_COLORS = {
    'background': (52, 78, 91),
    'display_text': (255, 255, 255),  # (200, 200, 200),
    'input_text': (0, 0, 0),  # (240, 240, 240),
    'rect': (200, 200, 200),
}

CURRENT_MODE_COLORS = DARK_MODE_COLORS

BASE_FONT = pygame.font.SysFont("arialblack", 20)
FONT = pygame.font.SysFont("arialblack", 18)

clock = pygame.time.Clock()

# for background music and sound effects
pygame.mixer.init()
pygame.mixer.music.load("soundEffects/battleshipIntenseMusic.mp3")
pygame.mixer.music.play(-1)


class Mainmenu:
    def __init__(self, game_settings):
        self.alert = AlertBox(700, 750, screen)
        self.username = ""
        self.code = 0
        self.game_settings = game_settings
        self.menu_state = None
        self.level = 1
        self.game_state_info = None
        # self.music_state = "intense"

    def loginScreen(self, screen):
        battleship_label = Label(-180, -350, battleship_img, 1)
        login_button = MenuButton(250, 400, login_img, 1)

        invalidLogin = False

        username = False
        password = False
        username_input = pygame.Rect(200, 260, 300, 40)
        password_input = pygame.Rect(200, 340, 300, 40)
        username_text = ''
        password_text = ''

        run = False
        while not run:
            if not self.game_settings.theme:
                CURRENT_MODE_COLORS = DARK_MODE_COLORS
            else :
                CURRENT_MODE_COLORS = LIGHT_MODE_COLORS

            screen.fill(CURRENT_MODE_COLORS['background']) # (52, 78, 91) (174, 198, 208)

            pygame.draw.rect(screen, CURRENT_MODE_COLORS['rect'], username_input)
            pygame.draw.rect(screen, CURRENT_MODE_COLORS['rect'], password_input)

            text = BASE_FONT.render(username_text, True, CURRENT_MODE_COLORS['input_text'])
            screen.blit(text, (username_input.x + 5, username_input.y + 5))
            pass_text = BASE_FONT.render("*" * (len(password_text) % 25), True, CURRENT_MODE_COLORS['input_text'])
            screen.blit(pass_text, (password_input.x + 5, password_input.y + 7))

            username_font = BASE_FONT.render('Username', True, CURRENT_MODE_COLORS['display_text'])
            screen.blit(username_font, (username_input.x + 100, username_input.y - 30))

            password_font = BASE_FONT.render('Password', True, CURRENT_MODE_COLORS['display_text'])
            screen.blit(password_font, (password_input.x + 100, password_input.y - 30))
            signup_text = FONT.render("Don't have an account? - Sign Up", True, CURRENT_MODE_COLORS['display_text'])
            guest_text = FONT.render("Continue as guest", False, CURRENT_MODE_COLORS['display_text'])
            screen.blit(guest_text, (270, 680))
            screen.blit(signup_text, (210, 490))

            forgot_password = FONT.render("Forgot Password?", True, CURRENT_MODE_COLORS['display_text'])
            screen.blit(forgot_password, (270, 460))

            battleship_label.draw(screen)
            login_button.draw(screen)
            if login_button.handle_click():
                if validateUsernamePassword(username_text, hashPassword(password_text)):
                    self.username = username_text
                    return "logged", self.username
                else:
                    invalidLogin = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit", ""
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if username_input.collidepoint(event.pos):
                        username = True
                        password = False
                        invalidLogin = False
                    elif password_input.collidepoint(event.pos):
                        username = False
                        password = True
                        invalidLogin = False
                    elif forgot_password.get_rect(topleft=(270, 460)).collidepoint(event.pos):
                        return "reset_password", ""
                    elif signup_text.get_rect(topleft=(210, 490)).collidepoint(event.pos):
                        return "sign_up", ""
                    elif guest_text.get_rect(topleft=(270, 680)).collidepoint(event.pos):
                        self.username = "guest"
                        return "logged", self.username
                    else:
                        invalidLogin = False

                if event.type == pygame.KEYDOWN:
                    if username:
                        if event.key == pygame.K_BACKSPACE:
                            username_text = username_text[:-1]
                        else:
                            username_text += event.unicode
                        if len(username_text) == 25:
                            username = False

                    if password:
                        if event.key == pygame.K_BACKSPACE:
                            password_text = password_text[:-1]
                        else:
                            password_text += event.unicode

            if invalidLogin:
                self.alert.alert("Incorrect username or password")

            pygame.display.update()
            clock.tick(20)

        pygame.quit()

    def inputScreen(self, screen, forgot):

        battleship_label = Label(-180, -350, battleship_img, 1)
        if forgot:
            button = MenuButton(250, 480, reset_img, 1)
        else:
            button = MenuButton(250, 480, signup_img, 1)

        invalidUsername = False
        invalidPasswords = False

        username = False
        password = False
        validatePassword = False
        username_input = pygame.Rect(200, 260, 300, 40)
        password_input = pygame.Rect(200, 340, 300, 40)
        password_validation_input = pygame.Rect(200, 420, 300, 40)
        username_text = ''
        password_text = ''
        password_validation_text = ''

        run = False
        while not run:
            if not self.game_settings.theme:
                CURRENT_MODE_COLORS = DARK_MODE_COLORS
            else:
                CURRENT_MODE_COLORS = LIGHT_MODE_COLORS
            screen.fill(CURRENT_MODE_COLORS['background'])

            pygame.draw.rect(screen, CURRENT_MODE_COLORS['rect'], username_input)
            pygame.draw.rect(screen, CURRENT_MODE_COLORS['rect'], password_input)
            pygame.draw.rect(screen, CURRENT_MODE_COLORS['rect'], password_validation_input)

            text = BASE_FONT.render(username_text, True, CURRENT_MODE_COLORS['input_text'])
            screen.blit(text, (username_input.x + 5, username_input.y + 5))
            pass_text = BASE_FONT.render("*" * (len(password_text) % 25), True, CURRENT_MODE_COLORS['input_text'])
            screen.blit(pass_text, (password_input.x + 5, password_input.y + 7))
            pass_validate_text = BASE_FONT.render("*" * (len(password_validation_text) % 25), True, CURRENT_MODE_COLORS['input_text'])
            screen.blit(pass_validate_text, (password_validation_input.x + 5, password_validation_input.y + 7))

            username_font = BASE_FONT.render('Username', True, CURRENT_MODE_COLORS['display_text'])
            screen.blit(username_font, (username_input.x + 100, username_input.y - 30))

            password_font = BASE_FONT.render('Password', True, CURRENT_MODE_COLORS['display_text'])
            screen.blit(password_font, (password_input.x + 100, password_input.y - 30))
            screen.blit(password_font, (password_validation_input.x + 100, password_validation_input.y - 30))

            battleship_label.draw(screen)
            button.draw(screen)
            if button.handle_click():
                if not forgot:
                    if hashPassword(password_validation_text) != hashPassword(password_text) or password_text == '':
                        invalidPasswords = True
                    elif not addUser(username_text, hashPassword(password_text)):
                        invalidUsername = True
                    else:
                        return True
                else:
                    if hashPassword(password_validation_text) != hashPassword(password_text) or password_text == '':
                        invalidPasswords = True
                    elif not updatePassword(username_text, hashPassword(password_text)):
                        invalidUsername = True
                    else:
                        return True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if username_input.collidepoint(event.pos):
                        username = True
                        password = False
                        invalidUsername = False
                        validatePassword = False
                        invalidPasswords = False
                    elif password_input.collidepoint(event.pos):
                        username = False
                        password = True
                        invalidUsername = False
                        validatePassword = False
                    elif password_validation_input.collidepoint(event.pos):
                        username = False
                        password = False
                        invalidUsername = False
                        validatePassword = True
                        invalidPasswords = False
                    else:
                        if not button.handle_click():
                            return True

                if event.type == pygame.KEYDOWN:
                    if username:
                        if event.key == pygame.K_BACKSPACE:
                            username_text = username_text[:-1]
                        else:
                            username_text += event.unicode
                        if len(username_text) == 25:
                            username = False

                    if password:
                        if event.key == pygame.K_BACKSPACE:
                            password_text = password_text[:-1]
                        else:
                            password_text += event.unicode

                    if validatePassword:
                        if event.key == pygame.K_BACKSPACE:
                            password_validation_text = password_validation_text[:-1]
                        else:
                            password_validation_text += event.unicode

            if invalidUsername:
                if forgot:
                    self.alert.alert("Invalid username")
                else:
                    self.alert.alert("username is already taken")
            elif invalidPasswords:
                self.alert.alert("Passwords do not match")

            pygame.display.update()
            clock.tick(20)

        pygame.quit()

    def createMainMenu(self, screen, username):

        if not self.game_settings.theme:
            CURRENT_MODE_COLORS = DARK_MODE_COLORS
        else:
            CURRENT_MODE_COLORS = LIGHT_MODE_COLORS
        # game variables
        menu_state = "main"

        # define fonts
        font = pygame.font.SysFont("arialblack", 40)

        # Create the labels instances
        battleship_label = Label(-180, -350, battleship_img, 1)
        tutorial_index = 0
        tutorial_step = MenuButton(300, 250, tutorial_images[tutorial_index], 0.5)

        # create button instances
        play_button = MenuButton(250, 260, play_img, 1)
        stats_button = MenuButton(250, 330, stats_img, 1)
        settings_button = MenuButton(250, 400, settings_img, 1)
        tutorial_button = MenuButton(250, 470, tutorial_img, 1)
        quit_button = MenuButton(250, 540, quit_img, 1)
        prev_button = MenuButton(250, 600, prev_img, 0.8)
        next_button = MenuButton(450, 600, next_img, 0.8)

        ai_play_button = MenuButton(400, 470, start_img, 1)
        resume_game_button = MenuButton(400, 540, resume_game_img, 1)

        difficulty_index = 0  # Start at "Easy"
        difficulty_button = MenuButton(400, 330, difficulty_images[difficulty_index], 1)


        # randomize_button = MenuButton(278, 450, randomize_img, 1)

        mainmenu_components = [
            play_button,
            stats_button,
            settings_button,
            tutorial_button,
            quit_button
        ]


        main_menu = Menu()
        main_menu.add_component_list(mainmenu_components)

        ### want this to work with labels and menubuttons

        tutorial_submenu_components_list = [
            prev_button,
            next_button,
            tutorial_step
        ]

        tutorial_submenu = SubMenu()
        tutorial_submenu.add_component_list(tutorial_submenu_components_list)

        main_menu.add_submenu(tutorial_submenu)

        run = False
        while not run:
            if not self.game_settings.theme:
                CURRENT_MODE_COLORS = DARK_MODE_COLORS
            else:
                CURRENT_MODE_COLORS = LIGHT_MODE_COLORS
            screen.fill(CURRENT_MODE_COLORS['background'])

            # Logo and left side menu selection buttons always available
            battleship_label.draw(screen)

            main_menu.display(screen, True)

            if play_button.handle_click():
                menu_state = "play"
                main_menu.change_pos(10)

            if settings_button.handle_click():
                menu_state = "settings"
                main_menu.change_pos(10)

            if stats_button.handle_click():
                menu_state = "stats"

                main_menu.change_pos(10)

            if tutorial_button.handle_click():
                menu_state = "tutorial"
                main_menu.change_pos(10)

            if quit_button.handle_click():
                return True, None, None

                # Check menu state for additional buttons in submenu

            # Play menu
            if menu_state == "play":
                #ai_difficulty_button.draw(screen)
                font2 = pygame.font.SysFont("arialblack", 30)
                ai_difficulty_text = font2.render("AI Difficulty:", True, CURRENT_MODE_COLORS['display_text'])
                screen.blit(ai_difficulty_text, (410, 260))
                difficulty_button.image = difficulty_images[difficulty_index]
                difficulty_button.draw(screen)
                ai_play_button.draw(screen)
                resume_game_button.draw(screen)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if difficulty_button.is_clicked(event):
                        difficulty_index = (difficulty_index + 1) % len(difficulty_images)
                        print("difficulty changed from menu!", difficulty_index)
                        self.level = difficulty_index + 1
                if ai_play_button.handle_click():
                    return True, self.level, None
                if resume_game_button.handle_click():
                    self.game_state_info = load_game()
                    if username == self.game_state_info[5]:
                        return True, self.game_state_info[0][2], self.game_state_info
                    else:
                        return True, self.level, None

            # Stats menu
            if menu_state == "stats":
                totalPlayed, totalWon  = getStats(self.username)
                username = BASE_FONT.render("Username: " + self.username, True, CURRENT_MODE_COLORS['display_text'])
                screen.blit(username, (400, 300))
                totalGames_text = FONT.render("Total games played: " + str(totalPlayed), True, CURRENT_MODE_COLORS['display_text'])
                screen.blit(totalGames_text, (400, 350))
                totalWon_text = FONT.render("Total games won: " + str(totalWon), True, CURRENT_MODE_COLORS['display_text'])
                screen.blit(totalWon_text, (400, 400))
                # placeholder_label.draw(screen)

            # Settings menu
            if menu_state == "settings":

                settings_menu = SettingsMenu()
                return_to_previous_screen = settings_menu.create_settings_menu(screen, self.game_settings, username)
                if return_to_previous_screen:
                    menu_state = "main"
                    settings_menu.set_username(self.username)

            # Tutorial menu
            if menu_state == "tutorial":
                # menu_system.display(screen, False)
                tutorial_step.image = tutorial_images[tutorial_index]
                tutorial_step.draw(screen)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if prev_button.is_clicked(event):
                            print("Back!")
                            tutorial_index = (tutorial_index-1) % len(tutorial_images)
                            tutorial_step.draw(screen)

                        elif next_button.is_clicked(event):
                            print("Next!")
                            tutorial_index = (tutorial_index+1) % len(tutorial_images)
                            tutorial_step.draw(screen)
                tutorial_submenu.add_component_list(tutorial_submenu_components_list)
                main_menu.display(screen, False)
            # event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True, None, None

            pygame.display.update()
            clock.tick(20)

        pygame.quit()
        sys.exit()