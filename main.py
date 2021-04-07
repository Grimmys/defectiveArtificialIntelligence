import pygame

from src.gui import fonts
from src.game_controller import GameController

if __name__ == "__main__":
    pygame.init()

    # Load fonts
    fonts.init_fonts()

    # Initiate game controller
    GameController()
