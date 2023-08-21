from Board import Gameboard
import pygame

cell_size = 35


# Ship Factory
class ShipFactory:
    def create_ship(self, ship_type, x, y):
        if ship_type == "carrier":
            return Carrier(x, y)
        elif ship_type == "battleship":
            return Battleship(x, y)
        elif ship_type == "destroyer":
            return Destroyer(x, y)
        elif ship_type == "submarine":
            return Submarine(x, y)
        elif ship_type == "patrolboat":
            return PatrolBoat(x, y)
        else:
            return None


# Ship Base Class
class Ship:
    def __init__(self, name, size, x, y):
        self.name = name
        self.size = size
        self.rect = pygame.Rect(x, y, size * cell_size + size*2, cell_size )

    def draw(self, surface):
        pygame.draw.rect(surface, (220, 220, 220), self.rect)


# Ship Subclasses
class Carrier(Ship):
    def __init__(self, x, y):
        super().__init__("Carrier", 5, x, y)


class Battleship(Ship):
    def __init__(self, x, y):
        super().__init__("Battleship", 4, x, y)


class Destroyer(Ship):
    def __init__(self, x, y):
        super().__init__("Destroyer", 3, x, y)


class Submarine(Ship):
    def __init__(self, x, y):
        super().__init__("Submarine", 3, x, y)


class PatrolBoat(Ship):
    def __init__(self, x, y):
        super().__init__("Patrol Boat", 2, x, y)
