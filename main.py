import pygame

from src.gui import fonts
from src.game_controller import GameController

if __name__ == "__main__":
    print("---------------------------------------------------------------------------------------------")
    print("Defective Artificial Intelligence has been made for the Pygame Community Easter Jam in 2021")
    print("Development: Grimmys")
    print("Sound & Music: Jessica Robo")
    print("Don't forget to read the README if you need help")
    print("Enjoy the game!")
    print("---------------------------------------------------------------------------------------------")

    pygame.init()

    # Load fonts
    fonts.init_fonts()

    # Initiate game controller
    GameController()
