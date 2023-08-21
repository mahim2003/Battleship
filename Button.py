import pygame

class Button:
    def __init__(self, x, y, width, height, location):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.location = location # tuple (A, 1)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.state = "normal"   # Possible states: "normal", "selected", "hit", "miss"
                            # Corresponding colour:  DARKERGREY, ORANGE, RED, WHITE

        self.is_hovered = False # not used yet, need for bomb(9square) and air strike (3 or 5 in a row) alternate hover

    def draw(self, screen, colour, text):
        pygame.draw.rect(screen, colour, self.rect)
        if text != "":
            buttonText = pygame.font.Font(pygame.font.get_default_font(), 17)
            text_surface = buttonText.render(text, True, (255 - colour[0], 255 - colour[1], 255 - colour[2]))
              # Center text both horizontally and vertically in the button
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)
            
    def isHovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def isClicked(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False
    
    def get_location(self):
        return self.location