from typing import List
import pygame
from board.terrain.traits import TerrainTraits

LIGHT_TERRAIN_COLOR = 0x354c29
HEAVY_TERRAIN_COLOR = 0x323848
VANTAGE_POINT_COLOR = 0x553c34

TRAVERSABLE_TERRAIN_OUTLINE_COLOR = LIGHT_TERRAIN_COLOR + 0x333333
SCALABLE_TERRAIN_OUTLINE_COLOR = HEAVY_TERRAIN_COLOR + 0x333333

TERRAIN_OUTLINE_WIDTH = 2
TERRAIN_BORDER_RADIUS = 2


class Feature(pygame.sprite.Sprite):
    def __init__(self,
                 parent,
                 relative_rect: pygame.rect.Rect,
                 traits: List[TerrainTraits]):
        from board.terrain import Terrain
        self.parent: Terrain = parent

        self.relative_rect = relative_rect
        self.traits = traits

        self.border_radius = TERRAIN_BORDER_RADIUS
        self.outline_visible = False

    def get_rect(self):
        return pygame.rect.Rect(
            self.parent.center[0] + self.relative_rect.left,
            self.parent.center[1] + self.relative_rect.top,
            self.relative_rect.width,
            self.relative_rect.height,
        )

    def show_outline(self):
        self.outline_visible = True

    def hide_outline(self):
        self.outline_visible = False

    def redraw(self):
        pygame.draw.rect(
            surface=pygame.display.get_surface(),
            color=self.color,
            rect=self.get_rect(),
            border_radius=self.border_radius,
        )

        # Draw terrain outlines
        if self.outline_visible:
            if self.traversable:
                pygame.draw.rect(
                    surface=pygame.display.get_surface(),
                    color=TRAVERSABLE_TERRAIN_OUTLINE_COLOR,
                    rect=self.get_rect(),
                    border_radius=self.border_radius,
                    width=TERRAIN_OUTLINE_WIDTH,
                )
            if self.scalable:
                pygame.draw.rect(
                    surface=pygame.display.get_surface(),
                    color=SCALABLE_TERRAIN_OUTLINE_COLOR,
                    rect=self.get_rect(),
                    border_radius=self.border_radius,
                    width=TERRAIN_OUTLINE_WIDTH,
                )

    @property
    def color(self):
        return LIGHT_TERRAIN_COLOR if self.light else (VANTAGE_POINT_COLOR if self.vantage_point else HEAVY_TERRAIN_COLOR)

    # Traits

    @property
    def heavy(self):
        return TerrainTraits.HEAVY in self.traits

    @property
    def light(self):
        return TerrainTraits.LIGHT in self.traits

    @property
    def traversable(self):
        return TerrainTraits.TRAVERSABLE in self.traits

    @property
    def scalable(self):
        return TerrainTraits.SCALABLE in self.traits

    @property
    def vantage_point(self):
        return TerrainTraits.VANTAGE_POINT in self.traits
