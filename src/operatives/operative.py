from typing import Tuple
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
        self.apl_modifier = 0

        # Status
        self.deployed = False
        self.ready = False
        self.visible = False

        # Sprite init
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, 0, 0).inflate(
            self.datacard.physical_profile.base.to_screen_size(), self.datacard.physical_profile.base.to_screen_size())
        # TODO: Choose starting position during deploy step

    def on_added_to_team(self):
        """Callback for when this operative is added to a team. Used to register team-based callbacks and properties
        """
        pass

    def on_deployed(self):
        self.deployed = True
        self.visible = True

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def move(self, center: Tuple[float, float]):
        self.rect.center = center

    def redraw(self):
        if not self.visible:
            return

        screen = pygame.display.get_surface()
        if self.color:
            pygame.draw.circle(screen, self.color,
                               self.rect.center, self.rect.width/2)
        self.render_group.draw(screen)

    @property
    def apl_modifier(self):
        return self._apl_modifier

    @apl_modifier.setter
    def apl_modifier(self, value):
        # APL modifier can never be more than +1/-1
        if value > 0:
            self._apl_modifier = 1
        elif value < 0:
            self._apl_modifier = -1
        else:
            self._apl_modifier = 0

    def activate(self):
        self.hide()
        self.team.gamestate.redraw()

        # TODO: Prompt player to select engage/conceal order

        action_points = self.datacard.physical_profile.action_point_limit + self.apl_modifier
        # While the operative has action points remaining, perform actions
        while action_points > 0:
            # TODO: Prompt player to select action
            action_points -= 1

        # APL modifier reset at the end of the current/next activation
        # TODO: Add hooks for on_activation_end
        self.APL_modifier = 0
        self.ready = False
