import pygame


class Scene:
    def __init__(self, width, height):
        self.surface = pygame.Surface((width, height))

    def draw(self):
        self.surface.fill(pygame.Color("black"))

    def update(self):
        pass

    def key_down(self, key):
        pass

    def mouse_button_down(self, button, pos):
        pass
