import pygame

import utils.distance

START_FULLSCREEN = False
BACKGROUND_COLOR = 0xc9c0ae


class _Screen:
    screen: pygame.Surface = None
    background: pygame.Surface = None


def init(title: str):
    _Screen.screen = pygame.display.set_mode(
        (0, 0), pygame.FULLSCREEN if START_FULLSCREEN else pygame.RESIZABLE)
    pygame.display.set_caption(title)
    pygame.mouse.set_visible(True)

    # Create background
    _Screen.background = pygame.Surface(_Screen.screen.get_size()).convert()
    _Screen.background.fill(BACKGROUND_COLOR)

    # Display background
    _Screen.screen.blit(_Screen.background, (0, 0))
    pygame.display.flip()

    utils.distance.update_inch_size()


def wipe():
    screen = pygame.display.get_surface()
    screen.blit(_Screen.background, (0, 0))


def redraw():
    pygame.display.flip()


def size():
    screen = pygame.display.get_surface()
    return screen.get_size()


def get_surface():
    return pygame.display.get_surface()
