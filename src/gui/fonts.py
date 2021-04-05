import pygame

fonts_descs = {
    'FPS_FONT': {'default': True, 'size': 20},
    'HEADER_FONT': {'default': True, 'size': 30}
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
