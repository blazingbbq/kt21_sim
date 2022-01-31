from typing import Tuple
from board.terrain.features.feature import Feature
from board.terrain.terrain import Terrain
from board.terrain.traits import TerrainTraits
import pygame
import utils.distance


class LowWall(Terrain):
    def __init__(self, pos: Tuple[int, int]):
        super().__init__(pos)
        self.add_features(
            Feature(
                parent=self,
                relative_rect=pygame.rect.Rect(
                    0,
                    0,
                    utils.distance.from_inch(6).to_screen_size(),
                    utils.distance.from_inch(0.5).to_screen_size(),
                ),
                traits=[TerrainTraits.LIGHT, TerrainTraits.TRAVERSABLE],
            ),
            Feature(
                parent=self,
                relative_rect=pygame.rect.Rect(
                    0,
                    0,
                    utils.distance.from_inch(0.5).to_screen_size(),
                    utils.distance.from_inch(2).to_screen_size(),
                ),
                traits=[TerrainTraits.LIGHT, TerrainTraits.TRAVERSABLE],
            ),
        )
