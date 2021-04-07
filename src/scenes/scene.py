import pygame

BUTTON_WIDTH = 400
BUTTON_HEIGHT = 80

class Scene:
    def __init__(self, width, height, game_controller):
        self.surface = pygame.Surface((width, height))
        self.controller = game_controller
        self.buttons = pygame.sprite.Group()

    def draw(self):
        self.surface.fill(pygame.Color("black"))

    def update(self):
        pass

    def key_down(self, key):
        pass

    def mouse_button_down(self, button, pos):
        for button in self.buttons:
            if button.rect.collidepoint(pos):
                button.trigger()

    def mouse_motion(self, pos):
        for button in self.buttons:
            button.switch_appearance(button.rect.collidepoint(pos))