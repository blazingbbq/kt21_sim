import pygame


class _Clock:
    clock: pygame.time.Clock = pygame.time.Clock()
    last_delta = 0.0  # Delta since last tick, in s


def tick(num):
    _Clock.last_delta = _Clock.clock.tick(num)
    return _Clock.last_delta


def delta():
    return _Clock.last_delta
