import pygame
from pygame.surface import Surface

from src.gui import fonts


class Button(pygame.sprite.Sprite):

    def __init__(self, size, position, title, callback):
        super().__init__()

        self.standard_image = Surface((size[0], size[1]))
        self.standard_image.blit(pygame.transform.scale(pygame.image.load("imgs/metallic_button.png"), (size)), (0, 0))

        self.mouse_over_image = Surface((size[0], size[1]))
        self.mouse_over_image.blit(pygame.transform.scale(pygame.image.load("imgs/metallic_button_hover.png"), (size)), (0, 0))

        self.image = self.standard_image

        self.title = fonts.fonts["BUTTON_FONT"].render(title, False, (255, 255, 255))
        self.init_text(self.standard_image)
        self.init_text(self.mouse_over_image)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position

        self.callback = callback

    def init_text(self, surface):
        surface.blit(self.title, (self.image.get_width() // 2 - self.title.get_width() // 2,
                                  self.image.get_height() // 2 - self.title.get_height() // 2))

    def switch_appearance(self, mouse_is_over):
        self.image = self.mouse_over_image if mouse_is_over else self.standard_image

    def trigger(self):
        self.callback()
