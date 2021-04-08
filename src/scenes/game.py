import random

import pygame
from pygame import time

from src.configuration import MIN_CELLS, MAX_CELLS, GAME_SURFACE_WIDTH, \
    GAME_SURFACE_HEIGHT, MAIN_WINDOW_HEIGHT, MAIN_WINDOW_WIDTH, TWEAKING_MODE, MAX_TRIES, FPS
from src.game_objects.artificial_engine import ArtificialEngine
from src.game_objects.artificial_cell import ArtificialCell
from src.gui import fonts
from src.scenes.scene import Scene

COLORS = (pygame.Color('red'), pygame.Color('blue'), pygame.Color('green'))


class Game(Scene):

    def __init__(self, width, height, game_controller):
        super().__init__(width, height, game_controller)
        self.level = 1
        self.victory = False
        self.defeat = False
        self.tries = 0
        self.timer = 0
        self.current_elapsed_time = 0
        self.counter_before_text_disapear = -1

        self.header = pygame.Surface((MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT - GAME_SURFACE_HEIGHT))
        self.header_title = None
        self.header_tries = None
        self.header_level = None

        self.game_space = pygame.Surface((GAME_SURFACE_WIDTH, GAME_SURFACE_HEIGHT))
        self.background = self.build_background()
        self.artificial_cells = pygame.sprite.Group()
        self.entities = pygame.sprite.Group()

        pygame.mixer.music.load("sounds/soundtrack.ogg")
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play(loops=-1)

        self.hit_effect = pygame.mixer.Sound("sounds/hit_effect.ogg")
        self.miss_effect = pygame.mixer.Sound("sounds/miss_effect.ogg")
        self.init_game()

    def build_background(self):
        floor = pygame.image.load("imgs/metal_floor.png")
        surface = self.game_space.copy()
        for x in range(0, surface.get_width(), 32):
            for y in range(0, surface.get_height(), 32):
                surface.blit(floor, (x, y))
        return surface

    def update_level_display(self):
        self.header_level = fonts.fonts["HEADER_FONT"].render(f"LVL.{self.level}", False, (255, 255, 255))

    def update_tries_display(self):
        self.header_tries = fonts.fonts["HEADER_FONT"].render(f"Remaining tries: {MAX_TRIES - self.tries}", False,
                                                              (255, 255, 255))

    def init_header(self):
        self.header_title = fonts.fonts["HEADER_FONT"].render("Which one is the intruder...", False, (255, 255, 255))
        self.update_tries_display()
        self.update_level_display()

    def init_game(self):
        self.victory = False
        self.defeat = False
        self.tries = 0
        self.timer = time.get_ticks()
        self.current_elapsed_time = 0
        self.counter_before_text_disapear = -1

        self.init_header()
        self.init_cells()

    def init_cells(self):
        self.artificial_cells.empty()
        self.entities.empty()
        number_cells = random.randint(MIN_CELLS, MAX_CELLS)
        # All cells but one will have the same artificial engine
        common_artificial_engine = ArtificialEngine(self.level)
        for i in range(number_cells):
            while True:
                robot = ArtificialCell(common_artificial_engine)
                if pygame.sprite.spritecollideany(robot, self.entities) is None:
                    break

            self.artificial_cells.add(robot)
            self.entities.add(robot)

        # Generated the intruder trying to copy others
        while True:
            intruder = ArtificialCell(ArtificialEngine(self.level, common_artificial_engine), is_the_intruder=True)
            if pygame.sprite.spritecollideany(intruder, self.entities) is None:
                break
        self.artificial_cells.add(intruder)
        self.entities.add(intruder)

    def draw(self):
        super().draw()

        # Draw elements of the header
        # -> Clean the header before all
        self.header.fill(pygame.Color("black"))

        # -> Timer
        header_timer = fonts.fonts["HEADER_FONT"].render(f"Timer: {self.current_elapsed_time} seconds", False,
                                                         (255, 255, 255))
        self.header.blit(header_timer, (10, self.header.get_height() // 2 - header_timer.get_height() // 2))

        # -> Last game message if any
        self.header.blit(self.header_title, (self.header.get_width() // 2 - self.header_title.get_width() // 2,
                                             self.header.get_height() // 2 - self.header_title.get_height() // 2))

        # -> Level
        self.header.blit(self.header_level, (self.header.get_width() - self.header_level.get_width() - 10,
                                             self.header.get_height() // 4 - self.header_level.get_height() // 2))

        # -> Tries
        self.header.blit(self.header_tries, (self.header.get_width() - self.header_tries.get_width() - 10,
                                             3 * self.header.get_height() // 4 - self.header_tries.get_height() // 2))
        # Blit the updated header on the scene
        self.surface.blit(self.header, (0, 0))

        # Display tha game!
        self.game_space.blit(self.background, (0, 0))
        for entity in self.entities:
            entity.draw(self.game_space)
        self.surface.blit(self.game_space, (0, MAIN_WINDOW_HEIGHT - GAME_SURFACE_HEIGHT))

    def update(self):
        super().update()
        if self.counter_before_text_disapear > -1:
            self.counter_before_text_disapear -= 1
            if self.counter_before_text_disapear == 0:
                if self.victory or self.defeat:
                    self.init_game()
                else:
                    self.init_header()

        if not self.victory and not self.defeat:
            self.current_elapsed_time = (time.get_ticks() - self.timer) // 1000

        for entity in self.entities:
            entity.update(self.entities, self.game_space.get_size())

    def key_down(self, key):
        super().key_down(key)
        if TWEAKING_MODE and key == pygame.K_r:
            self.init_game()

    def mouse_button_down(self, button, pos):
        super().mouse_button_down(button, pos)
        if button == 1 and not (self.victory or self.defeat):
            # Position should be relative to game space, so we decrement the position by the height of the header
            pos = (pos[0], pos[1] - self.header.get_height())
            for cell in self.artificial_cells:
                if cell.rect.collidepoint(pos):
                    self.tries += 1
                    self.update_tries_display()
                    self.counter_before_text_disapear = FPS * 2
                    if cell.is_intruder:
                        self.level += 1
                        self.victory = True
                        self.hit_effect.play()
                        self.header_title = fonts.fonts["HEADER_FONT"].render("You found it !", False,
                                                                              pygame.Color("green"))
                    elif self.tries == MAX_TRIES:
                        self.level = 1
                        self.defeat = True
                        self.miss_effect.play()
                        self.header_title = fonts.fonts["HEADER_FONT"].render("No, you lost. Back to first level.",
                                                                              False, pygame.Color("red"))
                    else:
                        self.miss_effect.play()
                        self.header_title = fonts.fonts["HEADER_FONT"].render("No... It's not the intruder. Try again.",
                                                                              False, pygame.Color("orange"))
                    break

