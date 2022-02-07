from typing import Tuple

import pygame
from board.dropzone import DropZone
from board.terrain.features.feature import TERRAIN_OUTLINE_WIDTH, Feature
from board.terrain.terrain import Terrain, LShape
from board.terrain.traits import TerrainTrait
from utils.collision import circle_rect_collide
import utils.distance
import game.state

BARRICADE_THICKNESS = utils.distance.from_inch(0.2)
BARRICADE_LENGTH = utils.distance.from_inch(2)

BARRICADE_VALID_DEPLOY_COLOR = 0x00ff00
BARRICADE_INVALID_DEPLOY_COLOR = 0xff0000


class Barricade(Terrain):
    def __init__(self,
                 pos: Tuple[int, int],
                 orientation: Tuple[int, int] = (1, 1),
                 thickness: utils.distance.Distance = BARRICADE_THICKNESS):
        super().__init__(pos, orientation=orientation)

        self.outline_color = None

        self.add_features(
            Feature(
                parent=self,
                relative_rect=pygame.rect.Rect(
                    0,
                    0,
                    thickness.to_screen_size() * self.horizontal_orientation,
                    BARRICADE_LENGTH.to_screen_size() * self.vertical_orientation,
                ),
                traits=[TerrainTrait.LIGHT,
                        TerrainTrait.TRAVERSABLE],
            ),
        )

    @property
    def feature(self):
        return self.features[0]

    def validate_deployment(self, dropzone: DropZone) -> bool:
        # Must be within PENTAGON of dropzone
        within_dropzone = False
        for zone in dropzone.barricade_deployment_zones:
            if zone.inflate(
                    -self.feature.rect.width,
                    -self.feature.rect.height,
            ).collidepoint(self.feature.rect.center):
                within_dropzone = True
                break

        if not within_dropzone:
            self.highlight(color=BARRICADE_INVALID_DEPLOY_COLOR)
            return False

        # Check that operative does not overlap terrain
        for terrain in game.state.get().gameboard.terrain:
            if terrain == self:
                continue

            for feature in terrain.features:
                if self.feature.rect.colliderect(feature.rect):
                    self.highlight(color=BARRICADE_INVALID_DEPLOY_COLOR)
                    return False

        # Both conditions hold, deployment is valid
        self.highlight(color=BARRICADE_VALID_DEPLOY_COLOR)
        return True

    def highlight(self, color):
        self.outline_color = color

    def unhighlight(self):
        self.outline_color = None

    def redraw(self):
        super().redraw()

        if self.outline_color != None:
            pygame.draw.rect(
                surface=pygame.display.get_surface(),
                color=self.outline_color,
                rect=self.feature.rect,
                border_radius=self.feature.border_radius,
                width=TERRAIN_OUTLINE_WIDTH,
            )

    def move_to(self, pos: Tuple[int, int]):
        self.center = (
            pos[0] - self.feature.rect.width / 2,
            pos[1] - self.feature.rect.height / 2,
        )

    def rotate(self):
        # Swap width and height
        width = self.feature.relative_rect.width
        self.feature.relative_rect.width = self.feature.relative_rect.height
        self.feature.relative_rect.height = width
