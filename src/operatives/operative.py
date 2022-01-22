import pygame
from abc import ABC
from .datacard import *


class Operative(pygame.sprite.Sprite, ABC):
    color = 0xffffff  # Default sprite color

    def __init__(self, datacard: Datacard):
        from state.team import Team
        # Team is set by the team when this operative is added to that team
        self.team: Team = None

        # Game object init
        self.datacard = datacard
        self.render_group = pygame.sprite.RenderPlain()
        self.ready = False

        # Sprite init
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(100, 100, 0, 0).inflate(
            self.datacard.physical_profile.base.to_screen_size(), self.datacard.physical_profile.base.to_screen_size())
        # TODO: Choose starting position during deploy step

    def on_added_to_team(self):
        """Callback for when this operative is added to a team. Used to register team-based callbacks and properties
        """
        pass

    def redraw(self):
        screen = pygame.display.get_surface()
        if self.color and self.ready:
            pygame.draw.circle(screen, self.color,
                               self.rect.center, self.rect.width/2)
        self.render_group.draw(screen)
