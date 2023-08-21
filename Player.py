from Card import *
import random
import pygame
from AI import AI

# Colors
BLACK = (0, 0, 0)
DARKERGREY = (50, 50, 50)
DARKGREY = (150, 150, 150)
GREY = (200, 200, 200)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
LIGHTBLUE = (173, 216, 230)


class Player:
    def __init__(self):
        self.hand = []
        self.card_prototypes = [
            (CardPrototype("Single Shot", "Attack 1 cell"), 0.5),
            (CardPrototype("Triple Draw", "Draw 3 cards"), 0.03),
            (CardPrototype("Triple Shot", "Attack any 3 cells"), 0.1),
            (CardPrototype("Double Draw", "Draw 2 cards"), 0.05),
            (CardPrototype("Single Shield", "Shield 1 ship cell"), 0.1),
            (CardPrototype("Single Repair", "Repair 1 ship cell"), 0.1),
            (CardPrototype("Bomb", "Attack 9 in a square"), 0.02),
            (CardPrototype("Full Shield", "Shield full ship"), 0.05),
            (CardPrototype("Full Repair", "Repair full ship"), 0.05)
        ]

    # Draw a random card from card prototypes and add it to player hand
    def add_card_to_hand(self):
        random_card = None
        random_value = random.random()

        for prototype, probability in self.card_prototypes:
            if random_value < probability:
                random_card = prototype.clone()
                break
            random_value -= probability
        # check if there is still room in hand to add card, max 5 cards
        if len(self.hand) < MAX_CARDS:
            self.hand.append(random_card)

    # Update displayed hand on screen after cards are added/removed
    def display_hand(self, screen):
        total_width = CARD_WIDTH * len(self.hand) + CARD_GAP * (len(self.hand) - 1)
        start_x = (700 - total_width) // 2
        y = 660

        for i, card in enumerate(self.hand):
            x = start_x + (CARD_WIDTH + CARD_GAP) * i
            card_rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
            if card_rect.collidepoint(pygame.mouse.get_pos()):
                card_rect.inflate_ip(10, 10)
                if pygame.mouse.get_pressed()[0]:
                    card.is_clicked = True
                    self.reset_card_click(card)
            else:
                card.is_clicked = False

            if card.is_clicked:
                card_color = GREY
            else:
                card_color = WHITE

            pygame.draw.rect(screen, card_color, card_rect)
            name_font = pygame.font.Font(pygame.font.get_default_font(), 16)
            description_font = pygame.font.Font(pygame.font.get_default_font(), 12)

            name_text = name_font.render(card.name, True, BLACK)
            description_text = description_font.render(card.description, True, BLACK)

            # Calculate centered positions for name and description
            name_x = x + (CARD_WIDTH - name_text.get_width()) // 2
            name_y = y + 10
            description_x = x + (CARD_WIDTH - description_text.get_width()) // 2
            description_y = y + 35

            screen.blit(name_text, (name_x, name_y))
            screen.blit(description_text, (description_x, description_y))

    # unselects cards
    def reset_card_click(self, clicked_card):
        for card in self.hand:
            if card is not None and card is not clicked_card:
                card.is_clicked = False

    def perform_action(self, card, screen, context):
        if card.name == "Single Shot":
            self.perform_single_shot(screen, context)
        elif card.name == "Triple Shot":
            self.perform_triple_shot(screen, context)
        elif card.name == "Triple Draw":
            self.perform_triple_draw(context)
        elif card.name == "Double Draw":
            self.perform_double_draw(context)
        elif card.name == "Single Shield":
            self.perform_single_shield(screen, context)
        elif card.name == "Single Repair":
            self.perform_single_repair(screen, context)
        elif card.name == "Bomb":
            self.perform_bomb_action(screen, context)
        elif card.name == "Full Shield":
            self.perform_full_shield_action(screen, context)
        elif card.name == "Full Repair":
            self.perform_full_repair_action(screen, context)
        pygame.display.update()

    def handle_player_interaction(self, screen, context, wait_for_click):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    result = context.gameboard.get_clickedLocation(pygame.mouse.get_pos(), wait_for_click)
                    if result is not None:
                        return result
                    else:
                        self.reset_card_click(self)
                        return
                if wait_for_click:
                    context.gameboard.UpdateButtons(screen)
                else:
                    context.gameboard.updatePlayerGrid(screen, context.gameplay.player_ship_positions)
            if wait_for_click:
                context.gameboard.UpdateButtons(screen)
            else:
                context.gameboard.updatePlayerGrid(screen, context.gameplay.player_ship_positions)

    # def perform_shots(self, screen, context):
    def perform_single_shot(self, screen, context):
        print("Single Shot")
        context.gameboard.selected_action = "single shot"

        result = self.handle_player_interaction(screen, context, True)
        if result is not None:
            print("selection made!")
            state = context.gameplay.detect_hit(result[1], False)
            if state:
                context.gameboard.redrawButton(screen, result[0], True)  # Hit
                result[0].state = "hit"
                return
            else:
                context.gameboard.redrawButton(screen, result[0], False)  # Miss
                result[0].state = "miss"
                return

    def perform_triple_shot(self, screen, context):
        print("Triple shot")
        context.gameboard.selected_action = "triple shot"

        for _ in range(3):
            result = self.handle_player_interaction(screen, context, True)

            print("selection made")
            if result is not None:
                state = context.gameplay.detect_hit(result[1], False)
                if state:
                    context.gameboard.redrawButton(screen, result[0], True)  # Hit
                    result[0].state = "hit"
                else:
                    context.gameboard.redrawButton(screen, result[0], False)  # Miss
                    result[0].state = "miss"
        return

    def perform_double_draw(self, context):
        print("Double Draw")
        context.gameboard.selected_action = "double draw"

        for i in range(2):
            context.player.add_card_to_hand()
        return

    def perform_triple_draw(self, context):
        print("Triple Draw")
        context.gameboard.selected_action = "triple draw"
        for i in range(3):
            context.player.add_card_to_hand()
        return

    def perform_single_shield(self, screen, context):
        print("Single Shield")
        context.gameboard.selected_action = "single shield"
        result = self.handle_player_interaction(screen, context, False)

        if result is not None:
            print("selection made")
            if result[1] in context.gameplay.player_ship_positions and result[0].state != "hit":
                result[0].draw(screen, LIGHTBLUE, "")  # Shield
                result[0].state = "shield"
                shieldSound = pygame.mixer.Sound("soundEffects/shield_sound.mp3")
                shieldSound.play()
                print("shielded")
                return
        return

    def perform_single_repair(self, screen, context):
        print("Single Repair")
        context.gameboard.selected_action = "single repair"

        result = self.handle_player_interaction(screen, context, False)
        if result is not None:
            print("selection made")
            if result[1] in context.gameplay.player_ship_positions and result[0].state == "hit":
                result[0].draw(screen, DARKGREY, "")  # Repair back to player position colour
                result[0].state = "player position"
                print("repaired")
                repairSound = pygame.mixer.Sound("soundEffects/repair_ship_sound.mp3")
                repairSound.play()
                # AI can guess this cell again since you repaired it
                context.gameplay.restore_ship_position(result[1], False)
                context.AI.alreadyGuessed.remove(result[1])
                return
            elif result[1] in context.gameplay.player_ship_positions and result[0].state != "hit":
                result[0].state = "player position"
                self.is_clicked = False
            else:
                result[0].state = "normal"
                self.is_clicked = False
        return

    def perform_bomb_action(self, screen, context):
        print("Bomb")
        context.gameboard.selected_action = "bomb"
        result = self.handle_player_interaction(screen, context, True)

        if result is not None:
            # Get the 3x3 buttons around the clicked button
            clicked_button = result[0]
            buttons_3x3 = context.gameboard.get_3x3_buttons(clicked_button)

            context.gameplay.detect_bomb_hit(screen, buttons_3x3)
        return

    def perform_full_shield_action(self, screen, context):
        print("Full Shield")
        context.gameboard.selected_action = "full shield"
        player_ship_dict = context.gameplay.ship_positions_dict
        result = self.handle_player_interaction(screen, context, False)
        ship = ""
        if result is not None:
            if result[1] in context.gameplay.player_ship_positions and result[0].state == "player position":
                for key, value in player_ship_dict.items():
                    if result[1] in value[1]:
                        ship = key
                        break
                # print(player_ship_dict[ship])
            for position in player_ship_dict[ship][1]:
                button = context.gameboard.find_button_by_location(position)
                if button.location in context.gameplay.player_ship_positions and button.state != "hit":
                    button.draw(screen, LIGHTBLUE, "")  # Shield
                    button.state = "shield"
                    print("shielded")
            shieldSound = pygame.mixer.Sound("soundEffects/shield_sound.mp3")
            shieldSound.play()
            return
        return

    def perform_full_repair_action(self, screen, context):
        print("Full Repair")
        context.gameboard.selected_action = "full repair"
        player_ship_dict = context.gameplay.ship_positions_dict
        result = self.handle_player_interaction(screen, context, False)
        ship = ""
        if result is not None:
            if result[1] in context.gameplay.player_ship_positions:
                for key, value in player_ship_dict.items():
                    if result[1] in value[1]:
                        ship = key
                        break
                # print(player_ship_dict[ship])
            for position in player_ship_dict[ship][1]:
                button = context.gameboard.find_button_by_location(position)
                if button.location in context.gameplay.player_ship_positions and button.state == "hit":
                    button.draw(screen, DARKGREY, "")  # Repair back to player position colour
                    button.state = "player position"
                    context.gameplay.restore_ship_position(position, False)
                    print("repaired")
                    # AI can guess this cell again since you repaired it
                    print(button.location)
                    print(context.AI.alreadyGuessed)
                    context.AI.alreadyGuessed.remove(button.location)
                else:
                    button.state = "player position"
            repairSound = pygame.mixer.Sound("soundEffects/repair_ship_sound.mp3")
            repairSound.play()
            return
        return

    def play_card(self, index, screen, context):
        if index < len(self.hand):
            card = self.hand[index]
            self.perform_action(card, screen, context)
            if card.is_clicked:
                self.hand.pop(index)

