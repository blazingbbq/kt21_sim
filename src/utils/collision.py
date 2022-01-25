from typing import List, Tuple
import pygame


def get_selected_sprite(loc: Tuple[int, int], targets: List[pygame.sprite.Sprite]):
    if loc != None:
        for target in targets:
            if target.rect.collidepoint(loc):
                return target
    return None
