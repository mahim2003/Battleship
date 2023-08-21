import pygame

pygame.init()
screen = pygame.display.set_mode((700, 750))

# load button images for main menu
main_menu_img = pygame.image.load("images/button_main-menu.png").convert_alpha()
settings_img = pygame.image.load("images/button_settings.png").convert_alpha()
play_img = pygame.image.load("images/button_play.png").convert_alpha()
start_img = pygame.image.load("images/button_start.png").convert_alpha()
resume_game_img = pygame.image.load('images/button_resume.png').convert_alpha()
stats_img = pygame.image.load('images/button_stats.png').convert_alpha()
tutorial_img = pygame.image.load('images/button_tutorial.png').convert_alpha()
quit_img = pygame.image.load('images/button_quit.png').convert_alpha()
prev_img = pygame.image.load('images/button_prev.png').convert_alpha()
next_img = pygame.image.load('images/button_next.png').convert_alpha()
join_game_img = pygame.image.load('images/button_join-game.png').convert_alpha()
randomize_img = pygame.image.load('images/button_randomize.png').convert_alpha()
create_game_img = pygame.image.load('images/button_create-game.png').convert_alpha()
reset_img = pygame.image.load('images/button_reset.png').convert_alpha()
signup_img = pygame.image.load('images/button_sign-up.png').convert_alpha()
aiLevel1_img = pygame.image.load('images/button_ai.png').convert_alpha()
aiLevel2_img = pygame.image.load('images/button_ai-2.png').convert_alpha()
aiLevel3_img = pygame.image.load('images/button_ai-3.png').convert_alpha()
delete_account_img = pygame.image.load('images/button_delete-account.png').convert_alpha()

# load button images for login page
login_img = pygame.image.load('images/button_login.png').convert_alpha()

# Labels
battleship_img = pygame.image.load("images/label_battleship.png").convert_alpha()
placeholder_img = pygame.image.load('images/placeholder.jpg').convert_alpha()


#Load images for settings Menu
ai_difficulty_img = pygame.image.load("images/button_ai-difficulty.png").convert_alpha()
music_intensity_images = [
    pygame.image.load("images/button_intense.png").convert_alpha(),
    pygame.image.load("images/button_relaxed.png").convert_alpha(),
]
difficulty_images = [
    pygame.image.load("images/button_easy.png").convert_alpha(),
    pygame.image.load("images/button_medium2.png").convert_alpha(),
    pygame.image.load("images/button_hard.png").convert_alpha(),
    pygame.image.load('images/button_challenge.png').convert_alpha()

]
music_vol_img = pygame.image.load("images/button_music-volume.png").convert_alpha()
soundfx_vol_img = pygame.image.load("images/button_sound-effects-volume.png").convert_alpha()
visualfx_img = pygame.image.load("images/button_visual-effects.png").convert_alpha()
accessibility_img = pygame.image.load("images/button_accessibility.png").convert_alpha()
account_img = pygame.image.load("images/button_account.png").convert_alpha()
general_img = pygame.image.load("images/button_general.png").convert_alpha()
on_img = pygame.image.load("images/button_on.png").convert_alpha()
off_img = pygame.image.load("images/button_off.png").convert_alpha()
easy_img = pygame.image.load("images/button_easy.png").convert_alpha()
medium_img = pygame.image.load("images/button_medium.png").convert_alpha()
hard_img = pygame.image.load("images/button_hard.png").convert_alpha()
contrast_img = pygame.image.load("images/button_contrast.png").convert_alpha()
dark_img = pygame.image.load("images/button_dark.png").convert_alpha()
delete_img = pygame.image.load("images/button_delete-account.png").convert_alpha()
game_elements_size_img = pygame.image.load("images/button_game-elements-size.png").convert_alpha()
light_img = pygame.image.load("images/button_light.png").convert_alpha()
save_img =pygame.image.load("images/button_save.png").convert_alpha()
text_size_img = pygame.image.load("images/button_text-size.png").convert_alpha()
theme_img = pygame.image.load("images/button_theme.png").convert_alpha()
voice_over_img = pygame.image.load("images/button_voice-over.png").convert_alpha()
display_name_img = pygame.image.load("images/button_display-name.png").convert_alpha()
username_img = pygame.image.load("images/button_username.png").convert_alpha()
password_img = pygame.image.load("images/button_password.png").convert_alpha()
back_img = pygame.image.load("images/button_back.png").convert_alpha()

# tutorial images
a = pygame.transform.scale(pygame.image.load("images/Playtext.png").convert_alpha(), (350, 250))
b = pygame.transform.scale(pygame.image.load("images/play_screen_dark.png").convert_alpha(), (350, 350))
p = pygame.transform.scale(pygame.image.load("images/stats.png").convert_alpha(), (350, 350))
c = pygame.transform.scale(pygame.image.load("images/configtext.png").convert_alpha(), (300, 250))
d = pygame.transform.scale(pygame.image.load('images/configuration_screen_dark.png').convert_alpha(), (325, 325))
e = pygame.transform.scale(pygame.image.load('images/howtoplay.png').convert_alpha(), (300, 300))
f = pygame.transform.scale(pygame.image.load('images/bombcard.png').convert_alpha(), (300, 300))
g = pygame.transform.scale(pygame.image.load('images/repaironecard.png').convert_alpha(), (300, 300))
h = pygame.transform.scale(pygame.image.load('images/fullrepaircard.png').convert_alpha(), (300, 300))
i = pygame.transform.scale(pygame.image.load('images/tripleshotcard.png').convert_alpha(), (300, 300))
j = pygame.transform.scale(pygame.image.load('images/singleshotcard.png').convert_alpha(), (300, 300))
k = pygame.transform.scale(pygame.image.load('images/doubledrawcard.png').convert_alpha(), (300, 300))
l = pygame.transform.scale(pygame.image.load('images/tripledrawcard.png').convert_alpha(), (300, 300))
m = pygame.transform.scale(pygame.image.load('images/fullshieldcard.png').convert_alpha(), (300, 300))
n = pygame.transform.scale(pygame.image.load('images/singleshieldcard.png').convert_alpha(), (300, 300))
o = pygame.transform.scale(pygame.image.load('images/outro.png').convert_alpha(), (300, 200))


tutorial_images = [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]

