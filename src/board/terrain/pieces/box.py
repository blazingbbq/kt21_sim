from typing import Tuple

import pygame
from board.terrain.features.feature import Feature
from board.terrain.terrain import Terrain, LShape
from board.terrain.traits import TerrainTrait
import utils.distance


class Box(Terrain):
    def __init__(self,
                 pos: Tuple[int, int],
                 horizontal_side_length: utils.distance.Distance,
                 vertical_side_length: utils.distance.Distance,
                 orientation: Tuple[int, int] = (1, 1),
                 heavy: bool = False):
        super().__init__(pos, orientation=orientation)

        self.add_features(
            Feature(
                parent=self,
                relative_rect=pygame.rect.Rect(
                    0,
                    0,
                    horizontal_side_length.to_screen_size() * self.horizontal_orientation,
                    vertical_side_length.to_screen_size() * self.vertical_orientation,
                ),
                traits=[TerrainTrait.HEAVY,
                        TerrainTrait.TALL,
                        TerrainTrait.SCALABLE] if heavy
                else [
                    TerrainTrait.LIGHT,
                    TerrainTrait.TRAVERSABLE],
            ),
        )
