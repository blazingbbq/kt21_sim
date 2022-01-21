import pygame
from abc import ABC
from .datacard import *


class Operative(pygame.sprite.Sprite, ABC):
    color = (255, 255, 255)  # Default sprite color

    def __init__(self, datacard: Datacard):
        # Game object init
        self.datacard = datacard
        self.render_group = pygame.sprite.RenderPlain()

        # Sprite init
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(100, 100, 0, 0).inflate(
            self.datacard.physical_profile.base, self.datacard.physical_profile.base)
        # FIXME: Change starting position, inflate proportionaly to game board size

    def redraw(self):
        screen = pygame.display.get_surface()

        if self.color:
            pygame.draw.rect(screen, self.color, self.rect)
        self.render_group.draw(screen)
