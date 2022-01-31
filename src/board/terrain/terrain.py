from abc import ABC
from typing import List, Tuple
from board.terrain.features.feature import Feature

import pygame


class Terrain(pygame.rect.Rect, ABC):
    def __init__(self, pos: Tuple[int, int]):
        self.features: List[Feature] = []
        self.center = pos

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
