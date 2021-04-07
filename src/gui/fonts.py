import pygame

fonts_descs = {
    'FPS_FONT': {'default': True, 'size': 20},
    'HEADER_FONT': {'name': 'fonts/GALS.ttf', 'size': 30},
    'TITLE_FONT': {'name': 'fonts/neuropol_x_rg.ttf', 'size': 50},
    'BUTTON_FONT': {'name': 'fonts/anita_semi_square.ttf', 'size': 26},
    'STANDARD_FONT': {'name': 'fonts/anita_semi_square.ttf', 'size': 20}
}

fonts = {}


def init_fonts():
    global fonts
    for font in fonts_descs:
        if 'default' in fonts_descs[font]:
            # Use pygame's default font
            fonts[font] = pygame.font.SysFont('arial', fonts_descs[font]['size'], True)
        else:
            fonts[font] = pygame.font.Font(fonts_descs[font]['name'], fonts_descs[font]['size'])
