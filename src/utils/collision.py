from typing import List, Tuple, Union
import pygame
import utils.distance


def get_selected_sprite(loc: Tuple[int, int], targets: List[pygame.sprite.Sprite]):
    if loc != None:
        for target in targets:
            if target.rect.collidepoint(loc):
                return target
    return None


def line_bounding_box(line_from: Tuple[int, int], line_to: Tuple[int, int], padding: Union[int, utils.distance.Distance, None] = None):
    if padding == None:
        padding = 0
    if isinstance(padding, utils.distance.Distance):
        padding = padding.to_screen_size()

    left = min(line_from[0], line_to[0]) - padding
    right = max(line_from[0], line_to[0]) + padding
    top = min(line_from[1], line_to[1]) - padding
    bottom = max(line_from[1], line_to[1]) + padding
    bounding_box = pygame.Rect(left, top, right - left, bottom - top)

    return bounding_box
