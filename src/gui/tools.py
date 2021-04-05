import random


def show_fps(screen, inner_clock, font):
    fps_text = font.render("FPS: " + str(round(inner_clock.get_fps())), True, (255, 255, 0))
    screen.blit(fps_text, (2, 2))


def generate_random_position(limits):
    return random.randint(0, limits[0]), random.randint(0, limits[1])


def format_size(size, min_size, max_size):
    new_size = [size[0], size[1]]
    if size[0] <= min_size:
        new_size[0] = min_size
    elif size[0] > max_size:
        new_size[0] = max_size
    if size[1] <= min_size:
        new_size[1] = min_size
    elif size[1] > max_size:
        new_size[1] = max_size
    return new_size
