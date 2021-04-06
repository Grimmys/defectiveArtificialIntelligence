from enum import Enum

import pygame

from src.configuration import GAME_SURFACE_WIDTH, GAME_SURFACE_HEIGHT
from src.gui.tools import generate_random_position


class Entity(pygame.sprite.Sprite):
    directions = Enum('DIRECTIONS', 'UP DOWN LEFT RIGHT')

    def __init__(self, size, position=None):
        super().__init__()

        self.image = pygame.Surface((size[0], size[1]), pygame.SRCALPHA)

        self.rect = self.image.get_rect()
        if position:
            self.rect.x, self.rect.y = position
        else:
            self.rect.x, self.rect.y = generate_random_position((GAME_SURFACE_WIDTH - self.rect.width,
                                                                 GAME_SURFACE_HEIGHT - self.rect.height))

        self.current_action = None

    def position_is_valid(self, other_entities, bounds):
        return len(pygame.sprite.spritecollide(self, other_entities, False)) == 1 \
               and 0 <= self.rect.x < bounds[0] - self.rect.width \
               and 0 <= self.rect.y < bounds[1] - self.rect.height

    def move(self, direction):
        if direction is Entity.directions.UP:
            self.rect.y -= 1
        elif direction is Entity.directions.DOWN:
            self.rect.y += 1
        elif direction is Entity.directions.LEFT:
            self.rect.x -= 1
        else:
            self.rect.x += 1

    def draw(self, screen):
        screen.blit(self.image, self.rect)
