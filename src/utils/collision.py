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


def circle_rect_collide(circle: Tuple[int, int], radius: utils.distance.Distance, rect: pygame.rect.Rect) -> bool:
    """Returns whether a circle collides with a rect

    Args:
        circle (Tuple[int, int]): The center of the circle
        radius (Distance): The circle's radius (as a Distance object)
        rect (pygame.rect.Rect): The rectangle to check

    Returns:
        bool: Whether the circle collides with the rect
    """
    # See: https://stackoverflow.com/a/402019
    return (rect.collidepoint(circle)) or \
        (utils.distance.between_line_and_point(line_from=rect.topleft, line_to=rect.topright, point=circle) < radius) or \
        (utils.distance.between_line_and_point(line_from=rect.topright, line_to=rect.bottomright, point=circle) < radius) or \
        (utils.distance.between_line_and_point(line_from=rect.bottomright, line_to=rect.bottomleft, point=circle) < radius) or \
        (utils.distance.between_line_and_point(
            line_from=rect.bottomleft, line_to=rect.topleft, point=circle) < radius)
