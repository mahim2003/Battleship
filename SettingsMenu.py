from Components import *
from images import *
from DatabaseHelper import *
import sys

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

DARK_MODE_COLORS = {
    'background': (52, 78, 91),
    'display_text': (255, 255, 255),  # (200, 200, 200),
    'input_text': (0, 0, 0), # (240, 240, 240),
    'rect': (200, 200, 200),
}

CURRENT_MODE_COLORS = DARK_MODE_COLORS
pygame.mixer.init()
clock = pygame.time.Clock()
BASE_FONT = pygame.font.SysFont("arialblack", 20)

class SettingsMenu:
    def __init__(self):
        self.settings_state = SettingsState()
        self.music_volume_slider = Slider(570, 100 + 2 * 80, 100, 30, 0, 1.0, 0.1, CURRENT_MODE_COLORS)
        self.soundfx_volume_slider = Slider(570, 200 + 2 * 80, 100, 30, 0, 1.0, 0.1, CURRENT_MODE_COLORS)
        self.active_slider = None
        self.username = ""
        self.password = ""
        self.alert = AlertBox(700, 750, screen)
        self.username_input = pygame.Rect(460, 105 + 1 * 80, 200, 32)  # 200, 260, 300, 40
        self.password_input = pygame.Rect(460, 105 + 2 * 80, 200, 32)  # 200, 340, 300, 40
        self.username_text = ''
        self.password_text = ''

        # Load setting images and create buttons
        self.back_button = MenuButton(10, 10, back_img, 1)  # Adjust the position as needed
        self.username_button = MenuButton(250, 100 + 2 * 80, username_img, 1)
        self.password_button = MenuButton(250, 100 + 3 * 80, password_img, 1)

        self.difficulty_images = [
            pygame.image.load("images/button_easy.png").convert_alpha(),
            pygame.image.load("images/button_medium2.png").convert_alpha(),
            pygame.image.load("images/button_hard.png").convert_alpha(),
            pygame.image.load('images/button_challenge.png').convert_alpha()
        ]
        self.settings_state.ai_difficulty_index = 0  # Start at "Easy"
        self.difficulty_button = MenuButton(450, 100 + 1 * 80, self.difficulty_images[self.settings_state.ai_difficulty_index], 1)
        self.settings_state.intensity_index = 0  # Start at "Intense"
        self.intensity_button = MenuButton(500, 100 + 4 * 80, music_intensity_images[self.settings_state.intensity_index], 1)

        self.general_button = MenuButton(10, 100 + 1 * 80, general_img, 1)
        self.account_button = MenuButton(10, 100 + 2 * 80, account_img, 1)
        self.ai_difficulty_button = MenuButton(250, 100 + 1 * 80, ai_difficulty_img, 1)
        self.music_vol_button = MenuButton(250, 100 + 2 * 80, music_vol_img, 1)
        self.soundfx_vol_button = MenuButton(250, 100 + 3 * 80, soundfx_vol_img, 1)
        self.dark_button = MenuButton(550, 100 + 5 * 80, dark_img, 1)
        self.light_button = MenuButton(550, 100 + 5 * 80, light_img, 1)
        self.theme_button = MenuButton(250, 100 + 5 * 80, theme_img, 1)
        self.save_button = MenuButton(500, 100 + 3 * 80, save_img, 1)
        self.delete_button = MenuButton(450, 100 + 4 * 80, delete_img, 1)
        self.current_screen = 'general'

    def display_general_settings(self, screen):
        if not self.settings_state.theme:
            CURRENT_MODE_COLORS = DARK_MODE_COLORS
        else:
            CURRENT_MODE_COLORS = LIGHT_MODE_COLORS
        font = pygame.font.SysFont("arialblack", 25)
        ai_difficulty_text = font.render("AI Difficulty:", True, CURRENT_MODE_COLORS['display_text'])
        screen.blit(ai_difficulty_text, (250, 100 + 1 * 80))

        music_vol_text = font.render("Music Volume:", True, CURRENT_MODE_COLORS['display_text'])
        screen.blit(music_vol_text, (250, 100 + 2 * 80))

        sound_fx_vol_text = font.render("SoundFX Volume:", True, CURRENT_MODE_COLORS['display_text'])
        screen.blit(sound_fx_vol_text, (250, 100 + 3 * 80))

        intensity_text = font.render("Music Intensity:", True, CURRENT_MODE_COLORS['display_text'])
        screen.blit(intensity_text, (250, 100 + 4 * 80))

        theme_text = font.render("Theme:", True, CURRENT_MODE_COLORS['display_text'])
        screen.blit(theme_text, (250, 100 + 5 * 80))

        self.music_volume_slider.draw(screen)
        self.soundfx_volume_slider.draw(screen)
        self.difficulty_button.image = self.difficulty_images[self.settings_state.ai_difficulty_index]
        self.difficulty_button.draw(screen)
        self.intensity_button.image = music_intensity_images[self.settings_state.intensity_index]
        self.intensity_button.draw(screen)

        if not self.settings_state.theme:
            self.dark_button.draw(screen)
        else:
            self.light_button.draw(screen)
        self.general_button.draw(screen)
        self.account_button.draw(screen)

    def display_account_settings(self, screen):
        if not self.settings_state.theme:
            CURRENT_MODE_COLORS = DARK_MODE_COLORS
        else:
            CURRENT_MODE_COLORS = LIGHT_MODE_COLORS
        font = pygame.font.SysFont("arialblack", 25)

        username_text = font.render("Username:", True, CURRENT_MODE_COLORS['display_text'])
        screen.blit(username_text, (250, 100 + 1 * 80))

        password_text = font.render("Password:", True, CURRENT_MODE_COLORS['display_text'])
        screen.blit(password_text, (250, 100 + 2 * 80))

        pygame.draw.rect(screen, CURRENT_MODE_COLORS['rect'], self.username_input)
        pygame.draw.rect(screen, CURRENT_MODE_COLORS['rect'], self.password_input)

        text = BASE_FONT.render(self.username_text, True, CURRENT_MODE_COLORS['input_text'])
        screen.blit(text, (self.username_input.x + 5, self.username_input.y + 5))
        pass_text = BASE_FONT.render("*" * (len(self.password_text) % 17), True, CURRENT_MODE_COLORS['input_text'])
        screen.blit(pass_text, (self.password_input.x + 5, self.password_input.y + 7))

        self.delete_button.draw(screen)
        self.save_button.draw(screen)

    def set_username(self, username):
        self.username = username

    def create_settings_menu(self, screen, settings_state, username):
        self.settings_state = settings_state  # to be passed to other methods here
        self.username = username
        # create game window
        SCREEN_WIDTH = 700
        SCREEN_HEIGHT = 750
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        username = False
        password = False
        invalid_username = False
        invalid_password = False

        return_to_previous_screen = False
        while not return_to_previous_screen:
            if not self.settings_state.theme:
                CURRENT_MODE_COLORS = DARK_MODE_COLORS
            else:
                CURRENT_MODE_COLORS = LIGHT_MODE_COLORS
            screen.fill(CURRENT_MODE_COLORS['background'])
            self.general_button.draw(screen)
            self.account_button.draw(screen)
            self.back_button.draw(screen)

            # Display the settings
            if self.current_screen == 'general':
                self.display_general_settings(screen)
            elif self.current_screen == 'account':
                self.display_account_settings(screen)

            # Event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.general_button.is_clicked(event):
                        self.current_screen = 'general'
                    elif self.account_button.is_clicked(event):
                        self.current_screen = 'account'
                    if self.back_button.is_clicked(event):
                        return_to_previous_screen = True
                    if self.current_screen == 'general' and not self.settings_state.theme and self.light_button.is_clicked(event):
                        settings_state.theme = True
                        print("Theme (Light):", settings_state.theme)
                    elif self.current_screen == 'general' and self.settings_state.theme and self.light_button.is_clicked(event):
                        settings_state.theme = False
                        print("Theme (Light):", settings_state.theme)
                    if self.current_screen == 'general' and self.difficulty_button.is_clicked(event):
                        self.settings_state.ai_difficulty_index = (self.settings_state.ai_difficulty_index + 1) % len(self.difficulty_images)
                        settings_state.ai_difficulty_index = self.settings_state.ai_difficulty_index
                        print("AI Difficulty Index:", settings_state.ai_difficulty_index)
                    if self.current_screen == 'general' and self.intensity_button.is_clicked(event):
                        self.settings_state.intensity_index = (self.settings_state.intensity_index + 1) % len(music_intensity_images)
                        settings_state.intensity_index = self.settings_state.intensity_index
                        if self.settings_state.intensity_index:
                            settings_state.music_intensity = "relaxed"
                            pygame.mixer.music.stop()
                            pygame.mixer.music.unload()
                            pygame.mixer.music.load("soundEffects/battleshipChillMusic.mp3")
                            pygame.mixer.music.play(-1)
                        else:
                            settings_state.music_intensity = "intense"
                            pygame.mixer.music.stop()
                            pygame.mixer.music.unload()
                            pygame.mixer.music.load("soundEffects/battleshipIntenseMusic.mp3")
                            pygame.mixer.music.play(-1)
                        print("Music Intensity Index:", settings_state.intensity_index, "Settings_state: ", settings_state.music_intensity)
                    if self.delete_button.is_clicked(event) and self.current_screen == 'account':
                        removeUser(self.username)
                        print("removed!")
                    if self.current_screen == 'account' and self.save_button.is_clicked(event):
                        if self.password_text == '' and self.username_text == '':
                            invalid_password = True
                            invalid_username = True
                            self.alert.alert("Username & Password are invalid")
                            print("Username & Password are invalid")
                        elif self.password_text == '' and self.username_text != '':
                            invalid_username = updateUsername(self.username, self.username_text)
                            if invalid_username:
                                self.alert.alert("Username is already taken or invalid")
                                print("Username is already taken or invalid")
                            else:
                                self.settings_state.username = self.username_text
                                print("Username updated!")
                                self.alert.alert("Username updated!")
                        elif self.username_text == '' and self.password_text != '':  # or
                            invalid_password = updatePassword(self.username_text, hashPassword(self.password_text))
                            if invalid_password:
                                self.alert.alert("Password is invalid")
                                print("Password is invalid")
                            else:
                                self.settings_state.password = self.password_text
                                print("Password updated!")
                                self.alert.alert("Password updated!")

                        elif self.username_text != '' and self.password_text != '':  # or self.settings_state.password == '':
                            invalid_password = updatePassword(self.username_text, hashPassword(self.password_text))
                            invalid_username = updateUsername(self.username, self.username_text)
                            if invalid_password and not invalid_username:
                                self.alert.alert("Password is invalid")
                                print("Password is invalid")
                            elif invalid_username and not invalid_password:
                                self.alert.alert("Username is already taken or invalid")
                                print("Username is already taken or invalid")
                            elif invalid_username and invalid_password:
                                self.alert.alert("Username & Password are invalid")
                                print("Username & Password are invalid")
                            else:
                                self.settings_state.username = self.username_text
                                self.settings_state.password = self.password_text
                                print("Username & Password updated!")
                                self.alert.alert("Username & Password updated!")
                        pygame.display.update()
                        clock.tick(20)

                elif self.current_screen == 'account' and event.type == pygame.MOUSEBUTTONDOWN:
                    if self.username_input.collidepoint(event.pos):
                        username = True
                        password = False
                        invalid_username = False
                        invalid_password = False
                    elif self.password_input.collidepoint(event.pos):
                        username = False
                        password = True
                        invalid_username = False
                        invalid_password = False
                    else:
                        username = False
                        password = False
                        invalid_username = False
                        invalid_password = False

                elif self.current_screen == 'account' and event.type == pygame.KEYDOWN:
                    if username:
                        if event.key == pygame.K_BACKSPACE:
                            self.username_text = self.username_text[:-1]
                        else:
                            self.username_text += event.unicode
                        if len(self.username_text) == 25:
                            username = False

                    if password:
                        if event.key == pygame.K_BACKSPACE:
                            self.password_text = self.password_text[:-1]
                        else:
                            self.password_text += event.unicode
                elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                    if self.current_screen == 'general' and self.music_volume_slider.rect.collidepoint(event.pos):
                        self.music_volume_slider.handle_event(event)
                        settings_state.music_volume = self.music_volume_slider.val
                        pygame.mixer.music.set_volume(self.music_volume_slider.val)
                        print("Music Volume:", settings_state.music_volume)

                    elif self.current_screen == 'general' and self.soundfx_volume_slider.rect.collidepoint(event.pos):
                        self.soundfx_volume_slider.handle_event(event)
                        settings_state.sound_effects_volume = self.soundfx_volume_slider.val
                        print("Sound Effects Volume:", settings_state.sound_effects_volume)

            pygame.display.update()
            clock.tick(20)
        return return_to_previous_screen, True


class SettingsState:
    def __init__(self):
        self.music_volume = 0.5  # 0 to 100%
        self.sound_effects_volume = 0.5  # 0 to 100%
        self.ai_difficulty_index = 0  # 0 for Easy , 1 for Medium 2 for Hard
        self.theme = False  # True for light theme, false for Dark theme
        self.password = ""
        self.music_intensity = "intense"  # or relaxed
        self.intensity_index = 0