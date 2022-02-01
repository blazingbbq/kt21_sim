from typing import Tuple
from board.terrain.features.feature import Feature
from board.terrain.terrain import Terrain
from board.terrain.traits import TerrainTrait
import pygame
import utils.distance


class Wall(Terrain):
    def __init__(self, pos: Tuple[int, int]):
        super().__init__(pos)
        self.add_features(
            Feature(
                parent=self,
                relative_rect=pygame.rect.Rect(
                    -utils.distance.from_inch(8).to_screen_size(),
                    -utils.distance.from_inch(0.5).to_screen_size(),
                    utils.distance.from_inch(8).to_screen_size(),
                    utils.distance.from_inch(0.5).to_screen_size(),
                ),
                traits=[TerrainTrait.HEAVY,
                        TerrainTrait.TALL],
            ),
            Feature(
                parent=self,
                relative_rect=pygame.rect.Rect(
                    -utils.distance.from_inch(0.5).to_screen_size(),
                    -utils.distance.from_inch(2).to_screen_size(),
                    utils.distance.from_inch(0.5).to_screen_size(),
                    utils.distance.from_inch(2).to_screen_size(),
                ),
                traits=[TerrainTrait.HEAVY,
                        TerrainTrait.TALL,
                        TerrainTrait.SCALABLE],
            ),
        )
