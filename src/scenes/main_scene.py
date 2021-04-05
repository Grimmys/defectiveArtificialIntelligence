import random

import pygame
from pygame import time

from src.configuration import MIN_CELLS, MAX_CELLS, GAME_SURFACE_WIDTH, \
    GAME_SURFACE_HEIGHT, MAIN_WINDOW_HEIGHT, MAIN_WINDOW_WIDTH, TWEAKING_MODE
from src.game_objects.artificial_engine import ArtificialEngine
from src.game_objects.artificial_cell import ArtificialCell
from src.gui import fonts
from src.scenes.scene import Scene


COLORS = (pygame.Color('red'), pygame.Color('blue'), pygame.Color('green'))


class MainScene(Scene):

    def __init__(self, width, height):
        super().__init__(width, height)

        self.header = pygame.Surface((MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT - GAME_SURFACE_HEIGHT))
        self.header_title = None
        self.header_tries = None

        self.victory = False
        self.tries = 0
        self.timer = 0
        self.current_elapsed_time = 0
        self.counter_before_text_disapear = -1

        self.game_space = pygame.Surface((GAME_SURFACE_WIDTH, GAME_SURFACE_HEIGHT))
        self.background = self.build_background()
        self.artificial_cells = pygame.sprite.Group()
        self.entities = pygame.sprite.Group()

        self.init_game()

    def build_background(self):
        floor = pygame.image.load("imgs/metal_floor.png")
        surface = self.game_space.copy()
        for x in range(0, surface.get_width(), 32):
            for y in range(0, surface.get_height(), 32):
                surface.blit(floor, (x, y))
        return surface

    def update_tries_display(self):
        self.header_tries = fonts.fonts["HEADER_FONT"].render(f"Tries: {self.tries}", False, (255, 255, 255))

    def init_header(self):
        self.header_title = fonts.fonts["HEADER_FONT"].render("Which one is the intruder...", False, (255, 255, 255))
        self.update_tries_display()

    def init_game(self):
        self.victory = False
        self.tries = 0
        self.timer = time.get_ticks()
        self.current_elapsed_time = 0
        self.counter_before_text_disapear = -1

        self.init_header()
        self.init_robots()

    def init_robots(self):
        self.artificial_cells.empty()
        self.entities.empty()
        number_cells = random.randint(MIN_CELLS, MAX_CELLS)
        common_artificial_engine = ArtificialEngine()
        for i in range(number_cells):
            while True:
                robot = ArtificialCell(common_artificial_engine)
                if pygame.sprite.spritecollideany(robot, self.entities) is None:
                    break

            self.artificial_cells.add(robot)
            self.entities.add(robot)
        # Generated the intruder trying to copy others
        while True:
            intruder = ArtificialCell(ArtificialEngine(common_artificial_engine), is_the_intruder=True)
            if pygame.sprite.spritecollideany(intruder, self.entities) is None:
                break
        self.artificial_cells.add(intruder)
        self.entities.add(intruder)

    def draw(self):
        super().draw()
        self.header.fill(pygame.Color("black"))
        self.header.blit(self.header_title, (self.header.get_width() // 2 - self.header_title.get_width() // 2,
                                             self.header.get_height() // 2 - self.header_title.get_height() // 2))
        self.header.blit(self.header_tries, (self.header.get_width() - self.header_tries.get_width() - 20,
                                             self.header.get_height() // 2 - self.header_title.get_height() // 2))
        header_timer = fonts.fonts["HEADER_FONT"].render(f"Timer: {self.current_elapsed_time} seconds", False, (255, 255, 255))
        self.header.blit(header_timer, (20, self.header.get_height() // 2 - header_timer.get_height() // 2))
        self.surface.blit(self.header, (0, 0))

        self.game_space.blit(self.background, (0, 0))
        for entity in self.entities:
            entity.draw(self.game_space)
        self.surface.blit(self.game_space, (0, MAIN_WINDOW_HEIGHT - GAME_SURFACE_HEIGHT))

    def update(self):
        super().update()
        if self.counter_before_text_disapear > -1:
            self.counter_before_text_disapear -= 1
            if self.counter_before_text_disapear == 0:
                if self.victory:
                    self.init_game()
                else:
                    self.init_header()

        self.current_elapsed_time = (time.get_ticks() - self.timer) // 1000

        for entity in self.entities:
            entity.update(self.entities, self.game_space.get_size())

    def key_down(self, key):
        if key == pygame.K_r:
            self.init_game()

    def mouse_button_down(self, button, pos):
        if button == 1:
            # Position should be relative to game space, so we decrement the position by the height of the header
            pos = (pos[0], pos[1] - self.header.get_height())
            print("Clicked pos :", pos)
            for cell in self.artificial_cells:
                print("Robot pos :", cell.rect)
                if cell.rect.collidepoint(pos):
                    self.tries += 1
                    self.update_tries_display()
                    self.counter_before_text_disapear = 120
                    if cell.is_intruder:
                        self.victory = True
                        self.header_title = fonts.fonts["HEADER_FONT"].render("You found it !", False, pygame.Color("green"))
                    else:
                        self.header_title = fonts.fonts["HEADER_FONT"].render("No... It's not the intruder, try again.",
                                                                              False, pygame.Color("red"))
                    break
