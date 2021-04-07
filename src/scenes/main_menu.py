import pygame

from src.configuration import GAME_NAME, MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT
from src.gui import fonts
from src.gui.button import Button
from src.scenes.help import Help
from src.scenes.main_scene import MainScene
from src.scenes.scene import Scene, BUTTON_WIDTH, BUTTON_HEIGHT


class MainMenu(Scene):

    def __init__(self, width, height, game_controller):
        super().__init__(width, height, game_controller)

        self.title = fonts.fonts["TITLE_FONT"].render(GAME_NAME, False, (255, 255, 255))

        self.init_buttons()

    def init_buttons(self):
        self.buttons.add(
            Button((BUTTON_WIDTH, BUTTON_HEIGHT), (self.surface.get_width() // 2 - BUTTON_WIDTH // 2, 200), "START", self.start_game),
            Button((BUTTON_WIDTH, BUTTON_HEIGHT), (self.surface.get_width() // 2 - BUTTON_WIDTH // 2, 400), "HELP", self.help),
            Button((BUTTON_WIDTH, BUTTON_HEIGHT), (self.surface.get_width() // 2 - BUTTON_WIDTH // 2, 600), "EXIT", self.exit_game)
        )

    def draw(self):
        super().draw()

        # Print game title
        self.surface.blit(self.title, (self.surface.get_width() // 2 - self.title.get_width() // 2, 30))

        # Display buttons
        self.buttons.draw(self.surface)

    def start_game(self):
        game_scene = MainScene(MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT, self.controller)
        self.controller.switch_scene(game_scene)

    def help(self):
        help_scene = Help(MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT, self.controller, self)
        self.controller.switch_scene(help_scene)

    def exit_game(self):
        pygame.quit()
        exit()