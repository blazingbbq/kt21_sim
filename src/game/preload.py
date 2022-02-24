import os
from typing import Tuple
import pygame

ASSET_DIR = "assets"
IMAGE_DIR = os.path.join(ASSET_DIR, "images")

PNG_EXTENSION = ".png"

WHITE_COLORKEY = 0xffffff


def recolor(image: pygame.Surface, color) -> pygame.Surface:
    colored_surface = image.copy()
    arr = pygame.surfarray.pixels3d(colored_surface)
    arr[:, :, 0] = (color & 0xff0000) >> 16
    arr[:, :, 1] = (color & 0x00ff00) >> 8
    arr[:, :, 2] = (color & 0x0000ff) >> 0

    return colored_surface


def image(name, colorkey=None, color=None, scale=1, scale_to=None) -> Tuple[pygame.Surface, pygame.Rect]:
    fullname = os.path.join(IMAGE_DIR, name)
    image = pygame.image.load(fullname)

    size = image.get_size()
    if scale_to:
        # Scale to size (both axis scaled by factor proportional to largest axis)
        scale = scale_to / max(size[0], size[1])
    size = (size[0] * scale, size[1] * scale)
    image = pygame.transform.scale(image, size)

    if fullname.endswith(PNG_EXTENSION):
        image = image.convert_alpha()
    else:
        image = image.convert()

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)

    if color is not None:
        image = recolor(image, color)

    return image, image.get_rect()
