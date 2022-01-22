import pygame
from abc import ABC
from .datacard import *


class Operative(pygame.sprite.Sprite, ABC):
    color = 0xffffff  # Default sprite color

    def __init__(self, datacard: Datacard):
        # Game object init
        self.datacard = datacard
        self.render_group = pygame.sprite.RenderPlain()

        # Sprite init
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(100, 100, 0, 0).inflate(
            self.datacard.physical_profile.base.to_screen_size(), self.datacard.physical_profile.base.to_screen_size())
        # FIXME: Change starting position

    def redraw(self):
        screen = pygame.display.get_surface()
        if self.color:
            pygame.draw.circle(screen, self.color,
                               self.rect.center, self.rect.width/2)
        self.render_group.draw(screen)
