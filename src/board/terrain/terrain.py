import pygame
import utils.distance
from abc import ABC
from typing import List, Tuple
from board.terrain.features.feature import Feature
from board.terrain.traits import TerrainTrait

class Terrain(pygame.rect.Rect, ABC):
    def __init__(self,
                 pos: Tuple[int, int],
                 orientation: Tuple[int, int] = (1, 1)):
        self.features: List[Feature] = []
        self.center = pos
        self.orientation = orientation

    def redraw(self):
        for feature in self.features:
            feature.redraw()

    def add_features(self, *features: Feature):
        for feature in features:
            self.features.append(feature)

    def show_outlines(self):
        for feature in self.features:
            feature.outline_visible = True

    def hide_outlines(self):
        for feature in self.features:
            feature.outline_visible = False

    @property
    def horizontal_orientation(self):
        return self.orientation[0]

    @property
    def vertical_orientation(self):
        return self.orientation[1]


def LShape(parent: Terrain,
           thickness: utils.distance.Distance,
           horizontal_side_length: utils.distance.Distance,
           vertical_side_length: utils.distance.Distance,
           orientation: Tuple[int, int],
           traits: List[TerrainTrait]):
    return [
        Feature(
            parent=parent,
            relative_rect=pygame.rect.Rect(
                0,
                0,
                horizontal_side_length.to_screen_size() * parent.horizontal_orientation,
                thickness.to_screen_size() * parent.vertical_orientation,
            ),
            traits=traits,
        ),
        Feature(
            parent=parent,
            relative_rect=pygame.rect.Rect(
                0,
                thickness.to_screen_size() * parent.vertical_orientation,
                thickness.to_screen_size() * parent.horizontal_orientation,
                vertical_side_length.to_screen_size() * parent.vertical_orientation,
            ),
            traits=traits,
        ),
    ]
