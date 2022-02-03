import os
import pygame

ASSET_DIR = "assets"
IMAGE_DIR = os.path.join(ASSET_DIR, "images")

PNG_EXTENSION = ".png"

WHITE_COLORKEY = 0xffffff


def image(name, colorkey=None, scale=1, scale_to=None):
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
    return image, image.get_rect()
