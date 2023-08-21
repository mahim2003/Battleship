import pygame
from DatabaseHelper import *
pygame.init()
BLACK = (0, 0, 0)
DARKGREY = (100, 100, 100)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
FONT = pygame.font.Font(pygame.font.get_default_font(), 25)

class MenuComponent:
    def draw(self, surface):
        pass

    def handle_click(self):
        pass

# Composite (menu is made of submenus and components(label and button),
# submenus are made of components(label and button));
# SubMenu, Label, MenuButton are MenuComponents
class Menu:
    def __init__(self):
        self.components = []
        self.submenus = []

    # Add
    def add_component(self, component):
        self.components.append(component)

    def add_component_list(self, component_list):
        for component in component_list:
            self.components.append(component)

    def add_submenu(self, submenu):
        self.submenus.append(submenu)

    def add_submenu_list(self, submenu_list):
        for submenu in submenu_list:
            self.submenus.append(submenu)

    # Remove
    def remove_submenu(self, submenu):
        self.submenus.remove(submenu)

    def remove_component(self, component):
        self.components.remove(component)

    # draw all components and submenus that make up the menu
    def display(self, surface, menu):
        if menu is True:
            for component in self.components:
                component.draw(surface)
        else:
            for submenu in self.submenus:
                for component in submenu.components:
                    component.draw(surface)

    def change_pos(self, xPos):
        for component in self.components:
            component.changePos(xPos)

    def handle_click(self):
        for submenu in self.submenus:
            for component in submenu.components:
                component.handle_click()


# inherits add/remove methods from menu
class SubMenu(Menu, MenuComponent):
    def __init__(self):
        self.components = []
        
    def draw(self, surface):
        for component in self.components:
            component.draw(surface)

    def handle_click(self):
        for component in self.components:
            component.handle_click()


class Label(MenuComponent):
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def handle_click(self):
        # Labels do not handle click events
        pass


class MenuButton(MenuComponent):
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def handle_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return self.clicked

    def changePos(self, x_pos):
        self.rect.x = x_pos

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
                return True
        return False

    def changePos(self, x_pos):
        self.rect.x = x_pos


class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, step, CURRENT_MODE_COLORS):
        self.rect = pygame.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.step = step
        self.val = max_val  # starting value
        self.grabbed = False
        self.color = CURRENT_MODE_COLORS

    def draw(self, screen):
        # draw the track
        pygame.draw.rect(screen, WHITE, self.rect)

        # draw the handle
        handle_x = ((self.val - self.min_val) / (self.max_val - self.min_val)) * self.rect.w + self.rect.x
        pygame.draw.circle(screen, BLUE, (int(handle_x), self.rect.centery), self.rect.h // 2)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.grabbed = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.grabbed = False
        elif event.type == pygame.MOUSEMOTION:
            if self.grabbed and pygame.mouse.get_pressed()[0]:  # check if mouse button is down
                x, y = event.pos
                if self.rect.x <= x <= self.rect.right:
                    # adjust value according to mouse position
                    self.val = ((x - self.rect.x) / self.rect.w) * (self.max_val - self.min_val) + self.min_val
                    self.val = round(self.val / self.step) * self.step  # to make it step-wise


class TextBox:
    def __init__(self, x, y, w, h, CURRENT_MODE_COLORS, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = CURRENT_MODE_COLORS['rect']
        self.text = text
        self.txt_surface = FONT.render(text, True, CURRENT_MODE_COLORS['input_text'])
        self.active = False

    def handle_event(self, event):  #, username, password ):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = WHITE if self.active else DARKGREY
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)

                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


class AlertBox:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.width = 300
        self.height = 150
        self.screen = screen

    def alert(self, message):
        self.screen.fill((200, 150, 150), (self.x/2 - self.width/2, self.y/2 - self.height, self.width, self.height))
        font = pygame.font.Font(pygame.font.get_default_font(), 18)
        text = font.render(message, True, (0, 0, 0))
        self.screen.blit(text, (self.x/2 - self.width/2+9, self.y/2 - self.height/2))
