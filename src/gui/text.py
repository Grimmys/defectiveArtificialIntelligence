import pygame
from pygame.surface import Surface

from src.gui import fonts


class Text(pygame.sprite.Sprite):

    def __init__(self, size, position, content):
        super().__init__()

        self.image = Surface((size[0], size[1]))

        self.content = fonts.fonts["STANDARD_FONT"].render(content, False, (255, 255, 255))
        self.image.blit(self.content, (self.image.get_width() // 2 - self.content.get_width() // 2,
                        self.image.get_height() // 2 - self.content.get_height() // 2))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position

