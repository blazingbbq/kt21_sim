import pygame


class _Clock:
    clock: pygame.time.Clock = pygame.time.Clock()


def tick(num):
    return _Clock.clock.tick(num)
