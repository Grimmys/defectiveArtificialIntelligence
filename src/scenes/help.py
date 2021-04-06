import pygame

from src.configuration import GAME_NAME
from src.gui import fonts
from src.gui.button import Button
from src.gui.text import Text
from src.scenes.scene import BUTTON_WIDTH, BUTTON_HEIGHT, Scene


class Help(Scene):

    def __init__(self, width, height, game_controller, caller):
        super().__init__(width, height, game_controller)

        self.title = fonts.fonts["TITLE_FONT"].render(GAME_NAME, False, (255, 255, 255))
        self.caller = caller
        self.text_lines = pygame.sprite.Group()

        self.init_text()
        self.init_buttons()

    def init_text(self):
        self.text_lines.add(
            Text((self.surface.get_width(), 50), (0, 200), "April 2035")
        )

        self.text_lines.add(
            Text((self.surface.get_width(), 50), (0, 300), "The biggest international research center in artificial intelligence")
        )

        self.text_lines.add(
            Text((self.surface.get_width(), 50), (0, 350), "succeeded in the creation of an intelligence able to generate artificial cells following the same model.")
        )

        self.text_lines.add(
            Text((self.surface.get_width(), 50), (0, 450), "But there are rumors about a hacker gang that is trying to inject a malicious artificial cell among the originals.")
        )

        self.text_lines.add(
            Text((self.surface.get_width(), 50), (0, 500), "You have been preselected to take a few tests that will evaluate your skill at spotting intruders in simulated situations.")

        )

        self.text_lines.add(
            Text((self.surface.get_width(), 50), (0, 600), "Will you be observant enough to find the intruder?")
        )

    def init_buttons(self):
        self.buttons.add(
            Button((BUTTON_WIDTH, BUTTON_HEIGHT), (self.surface.get_width() // 2 - BUTTON_WIDTH // 2, 700), "BACK TO MAIN MENU", self.back_to_main_menu),
        )

    def draw(self):
        super().draw()

        # Print game title
        self.surface.blit(self.title, (self.surface.get_width() // 2 - self.title.get_width() // 2, 50))

        # Print help text
        self.text_lines.draw(self.surface)

        # Display buttons
        self.buttons.draw(self.surface)

    def back_to_main_menu(self):
        self.controller.switch_scene(self.caller)