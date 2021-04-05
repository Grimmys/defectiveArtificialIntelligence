import pygame

from src.configuration import GAME_NAME, MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT
from src.gui import fonts
from src.gui.tools import show_fps
from src.scenes.main_scene import MainScene

if __name__ == "__main__":
    pygame.init()

    # Load fonts
    fonts.init_fonts()

    # Window parameters
    pygame.display.set_caption(GAME_NAME)
    window = pygame.display.set_mode((MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT))

    # Create first scene of the game
    active_scene = MainScene(MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)

    clock = pygame.time.Clock()

    quit_game = False
    while not quit_game:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit_game = True
            if e.type == pygame.KEYDOWN:
                active_scene.key_down(e.key)
            if e.type == pygame.MOUSEBUTTONDOWN:
                active_scene.mouse_button_down(e.button, e.pos)
        window.fill(pygame.Color("black"))
        active_scene.update()
        active_scene.draw()
        window.blit(active_scene.surface, (0, 0))
        show_fps(window, clock, fonts.fonts["FPS_FONT"])
        pygame.display.update()
        clock.tick(60)
    raise SystemExit
