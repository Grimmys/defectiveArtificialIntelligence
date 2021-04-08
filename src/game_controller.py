import pygame

from src.configuration import MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT, GAME_NAME, FPS, SHOW_FPS
from src.gui import fonts
from src.gui.tools import show_fps
from src.scenes.main_menu import MainMenu


class GameController:

    def __init__(self):
        # Window parameters
        pygame.display.set_caption(GAME_NAME)
        self.window = pygame.display.set_mode((MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT))

        # Create first scene of the game
        self.active_scene = MainMenu(MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT, self)

        self.clock = pygame.time.Clock()

        self.quit_game = False

        # Main loop of the app
        self.run()

    def run(self):
        while not self.quit_game:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.quit_game = True
                if e.type == pygame.KEYDOWN:
                    self.active_scene.key_down(e.key)
                if e.type == pygame.MOUSEBUTTONDOWN:
                    self.active_scene.mouse_button_down(e.button, e.pos)
                if e.type == pygame.MOUSEMOTION:
                    self.active_scene.mouse_motion(e.pos)
            self.window.fill(pygame.Color("black"))
            self.active_scene.update()
            self.active_scene.draw()
            self.window.blit(self.active_scene.surface, (0, 0))
            if SHOW_FPS:
                show_fps(self.window, self.clock, fonts.fonts["FPS_FONT"])
            pygame.display.update()
            self.clock.tick(FPS)
        raise SystemExit

    def switch_scene(self, scene):
        self.active_scene = scene
