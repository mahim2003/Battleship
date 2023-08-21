from Ship import ShipFactory
from Button import Button
from Board import Gameboard
import pygame
import random

LEFT_CLICK = 1
RIGHT_CLICK = 3

BLUE = (50, 50, 255)
BLACK = (0, 0, 0)
DARKGREY = (100, 100, 100)
WHITE = (255, 255, 255)

LIGHT_MODE_COLORS = {
    'background': (174, 198, 208),
    'display_text': (0, 0, 0),
    'input_text': (0, 0, 0),
    'rect': (255, 255, 255),
    'board': (153, 153, 153),
}

DARK_MODE_COLORS = {
    'background': (19, 41, 72),  #(52, 78, 91),
    'display_text': (255, 255, 255),  # (200, 200, 200),
    'input_text': (0, 0, 0),  # (240, 240, 240),
    'rect': (200, 200, 200),
    'board': (100, 100, 100),
}

CURRENT_MODE_COLORS = DARK_MODE_COLORS

class Configuration:
    def __init__(self, game_settings):
        # draws the grid of buttons
        self.game_settings = game_settings
        self.playerGrid = []
        # stores the ships and their positions
        self.playerPositions = []
        self.cell_size = 37
        self.ships = []
        self.clock = pygame.time.Clock()
        self.shipFactory = ShipFactory()
        self.selected_ship = None

        self.buttons = {
            "Main Menu": Button(20, 50, 120, 40, None),
            "Settings": Button(20, 100, 120, 40, None),
            "Randomize": Button(220, 100, 120, 40, None),
            "Lock Ships": Button(350, 100, 120, 40, None)
        }

    def createShips(self):
        possible_ships = ["carrier", "battleship", "destroyer", "submarine", "patrolboat"]
        x = 25
        # adds a space between the ship images when drawn
        for ship in possible_ships:
            if ship == "carrier":
                x = 15
            elif ship == "battleship":
                x = x + 35 * 5 + 15
            elif ship == "destroyer":
                x = x + 35 * 4 + 15
            else:
                x = x + 35 * 3 + 15
            self.ships.append(self.shipFactory.create_ship(ship, x, 600))

    def drawScreen(self, screen):
        if not self.game_settings.theme:
            CURRENT_MODE_COLORS = DARK_MODE_COLORS
        else:
            CURRENT_MODE_COLORS = LIGHT_MODE_COLORS
        y = 185
        for a in ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J"):
            x = 150
            for n in range(1, 11):
                playerButton = Button(x, y, 35, 35, (a, n))
                self.playerGrid.append(playerButton)
                x = x + 37
            y = y + 37

        for grid_elem in self.playerGrid:
            grid_elem.draw(screen, CURRENT_MODE_COLORS['board'], "")

        for button_name, button in self.buttons.items():
            button.draw(screen, (255, 255, 255), button_name)

        font = pygame.font.Font(pygame.font.get_default_font(), 20)
        if not self.game_settings.theme:
            CURRENT_MODE_COLORS = DARK_MODE_COLORS
        else:
            CURRENT_MODE_COLORS = LIGHT_MODE_COLORS
        instruction = font.render("Drag ships onto game board and press lock ships to start playing", True,
                                  CURRENT_MODE_COLORS['display_text'])  # (200, 200, 200)
        right_click_instruction = font.render("Right click to rotate ship", True,
                                              CURRENT_MODE_COLORS['display_text'])
        overlap_message = font.render("Do not overlap ships", True, (205, 38, 38))
        screen.blit(instruction, (30, 650))
        right_click_instruction_x = (screen.get_width() - right_click_instruction.get_width()) // 2

        screen.blit(right_click_instruction, (right_click_instruction_x, 680))

        screen.blit(overlap_message, (250, 150))

        for ship in self.ships:
            ship.draw(screen)

    def check_ship_overlap(self, new_ship_positions):
        for pos in new_ship_positions:
            if pos in self.playerPositions:
                return True  # Ships overlap
        return False  # No overlap

    def placeShip(self, ship):
        isPlaced = False
        location = None

        # Find where the ship collides with the grid
        for grid in self.playerGrid:
            if grid.rect.colliderect(ship.rect):
                isPlaced = True
                location = grid.location
                break

        if isPlaced and location is not None:
            row = location[1]  # Extract the row number as an integer
            new_ship_positions = []  # Store the new ship's positions

            # Stores the ship position in new_ship_positions based on its orientation
            if ship.rect.width > ship.rect.height:
                for i in range(ship.size):
                    new_ship_positions.append((location[0], row + i))  # Use the integer row here
            elif ship.rect.height > ship.rect.width:
                for i in range(ship.size):
                    new_ship_positions.append((chr(ord(location[0]) + i), row))  # Use the integer row here

            # Check for overlap using the separate function
            if not self.check_ship_overlap(new_ship_positions):
                # Update playerPositions and return True if there's no overlap
                self.playerPositions.extend(new_ship_positions)
                return True
            else:
                # Attempt to move the ship to the closest free cells
                for i in range(1, 10):  # Try a maximum of 9 cells away from the original position
                    new_location = (ord(location[0]) + i, row)  # Increment the ASCII value
                    if new_location[0] <= ord("J"):  # Check if within grid bounds
                        new_ship_positions = []  # Calculate new ship positions
                        for j in range(ship.size):
                            new_ship_positions.append((chr(new_location[0]), row + j))
                        if not self.check_ship_overlap(new_ship_positions):
                            ship.rect.topleft = self.playerGrid[row - 1 + j * 10].rect.topleft
                            self.playerPositions.extend(new_ship_positions)
                            return True

                    new_location = (ord(location[0]) - i, row)  # Decrement the ASCII value
                    if new_location[0] >= ord("A"):  # Check if within grid bounds
                        new_ship_positions = []  # Calculate new ship positions
                        for j in range(ship.size):
                            new_ship_positions.append((chr(new_location[0]), row + j))
                        if not self.check_ship_overlap(new_ship_positions):
                            ship.rect.topleft = self.playerGrid[row - 1 + j * 10].rect.topleft
                            self.playerPositions.extend(new_ship_positions)
                            return True

                    new_location = (location[0], row + i)  # Increment the row
                    if new_location[1] <= 10:  # Check if within grid bounds
                        new_ship_positions = []  # Calculate new ship positions
                        for j in range(ship.size):
                            new_ship_positions.append((chr(ord(location[0])), new_location[1] + j))
                        if not self.check_ship_overlap(new_ship_positions):
                            ship.rect.topleft = self.playerGrid[new_location[1] - 1 + j * 10].rect.topleft
                            self.playerPositions.extend(new_ship_positions)
                            return True

                    new_location = (location[0], row - i)  # Decrement the row
                    if new_location[1] >= 1:  # Check if within grid bounds
                        new_ship_positions = []  # Calculate new ship positions
                        for j in range(ship.size):
                            new_ship_positions.append((chr(ord(location[0])), new_location[1] + j))
                        if not self.check_ship_overlap(new_ship_positions):
                            ship.rect.topleft = self.playerGrid[new_location[1] - 1 + j * 10].rect.topleft
                            self.playerPositions.extend(new_ship_positions)
                            return True

        # Return False if ship placement is not valid
        return False

    def display(self, screen):
        counter = 60

        active = False
        drag = None
        selected_ship = None
        ships_to_place = [2, 3, 3, 4, 5]
        placed_ships = []

        timer = pygame.USEREVENT + 1
        pygame.time.set_timer(timer, 1000)

        # Creates the five ships
        self.createShips()

        while not active:
            if not self.game_settings.theme:
                CURRENT_MODE_COLORS = DARK_MODE_COLORS
            else :
                CURRENT_MODE_COLORS = LIGHT_MODE_COLORS

            screen.fill(CURRENT_MODE_COLORS['background'])
            #screen.fill((19, 41, 72))
            font = pygame.font.Font(pygame.font.get_default_font(), 20)
            text_render = font.render("Time Remaining: " + str(counter), True, CURRENT_MODE_COLORS['display_text'])
            screen.blit(text_render, (480, 50))
            self.drawScreen(screen)
            for event in pygame.event.get():
                mouse_pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_CLICK:
                    # Selects the ship to be dragged
                    for ind, ship in enumerate(self.ships):
                        if ship.rect.collidepoint(mouse_pos):
                            drag = ind
                            selected_ship = self.ships[drag]

                    # go back to main menu
                    if self.buttons["Main Menu"].isClicked(mouse_pos):
                        return "back_to_main_menu"

                    # go to settings
                    if self.buttons["Settings"].isClicked(mouse_pos):
                        return "back_to_settings"

                    if self.buttons["Lock Ships"].isClicked(mouse_pos) and len(ships_to_place) == 0:
                        for ship in self.ships:
                            self.placeShip(ship)
                        return "go_to_gameplay"

                    # randomize ships
                    if self.buttons["Randomize"].isClicked(mouse_pos):
                        print("randomizing")
                        complete = False
                        while not complete:
                            # Create a new list to store randomized ship positions
                            new_ship_positions = []

                            for ship in self.ships:
                                # Snap ship to the nearest grid cell
                                x = random.randint(150, 520 - ship.rect.width)
                                y = random.randint(185, 555 - ship.rect.height)

                                ship.rect.x = (x // 37) * 37
                                ship.rect.y = (y // 37) * 37

                                # Randomly change orientation
                                if random.choice([True, False]):
                                    temp = ship.rect.width
                                    ship.rect.width = ship.rect.height
                                    ship.rect.height = temp
                                    self.checkBounds(ship)

                                # Append the ship's new position to the list
                                new_ship_positions.append((ship.rect.x // 37, ship.rect.y // 37))
                                placed_ships.append(ship)

                                if ship.size in ships_to_place:
                                    ships_to_place.remove(ship.size)

                            # Check if any ship positions overlap
                            if not self.check_ship_overlap(new_ship_positions):
                                # All ships have valid positions
                                # self.playerPositions = new_ship_positions  # Update playerPositions

                                complete = True
                            else:
                                # Reset ship positions and try again
                                for ship in self.ships:
                                    ship.rect.x = 0
                                    ship.rect.y = 0


                # right click to rotate ship
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT_CLICK:
                    if selected_ship:
                        temp = selected_ship.rect.width
                        selected_ship.rect.width = selected_ship.rect.height
                        selected_ship.rect.height = temp
                        self.checkBounds(selected_ship)

                # Releases the ship onto the grid
                if event.type == pygame.MOUSEBUTTONUP:
                    if selected_ship is not None and selected_ship.size in ships_to_place:
                        ships_to_place.remove(selected_ship.size)
                        placed_ships.append(selected_ship)
                    drag = None

                if event.type == timer:
                    counter = counter - 1
                    if counter == 0:
                        pygame.time.set_timer(timer, 0)
                        return True

                # Drags the ship with the mouse
                if event.type == pygame.MOUSEMOTION and drag is not None:
                    selected_ship.rect.move_ip(pygame.mouse.get_pos())
                    # snaps the ship to the grid
                    x, y = pygame.mouse.get_pos()
                    selected_ship.rect.x = (x // 37) * 37
                    selected_ship.rect.y = (y // 37) * 37
                    # Keeps the ships within the bounds of the grid
                    self.checkBounds(selected_ship)

                if event.type == pygame.QUIT:
                    return "quit"
            pygame.display.update()
            self.clock.tick(20)

    def getPlayerPositions(self):
        return self.playerPositions

    def checkBounds(self, selected_ship):
        if selected_ship.rect.x < 150:
            selected_ship.rect.x = 150
        if selected_ship.rect.y < 185:
            selected_ship.rect.y = 185
        if selected_ship.rect.x + selected_ship.rect.width > 520:
            selected_ship.rect.x = 520 - selected_ship.rect.width
        if selected_ship.rect.y + selected_ship.rect.height > 555:
            selected_ship.rect.y = 555 - selected_ship.rect.height