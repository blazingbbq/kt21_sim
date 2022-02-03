from typing import Callable, Tuple
import pygame
import utils.distance
import game.preload

DEFAULT_TOKEN_COLOR = 0xc54c21
CAPTURE_RANGE_OUTLINE_WIDTH = 1


class Objective(pygame.sprite.Sprite):
    def __init__(self, pos: Tuple[int, int]):
        self.color = DEFAULT_TOKEN_COLOR
        self.capture_range_visible: bool = False
        self.capture_range = utils.distance.OBJECTIVE_CAPTURE_RANGE

        self.radius = utils.distance.from_mm(40).to_screen_size() / 2
        self.image, self.rect = game.preload.image("skull.png",
                                                   colorkey=game.preload.WHITE_COLORKEY,
                                                   scale_to=self.radius * 2)
        self.rect.center = pos

        from operatives import Operative
        self.on_capture_callbacks: Callable[[Objective, Operative], None] = []
        self.on_pickup_callbacks: Callable[[Objective, Operative], None] = []

    def show_capture_range(self):
        self.capture_range_visible = True

    def hide_capture_range(self):
        self.capture_range_visible = False

    def on_capture(self, op):
        from operatives import Operative
        operative: Operative = op

        for on_capture in self.on_capture_callbacks:
            on_capture(self, operative)

    def on_pickup(self, op):
        from operatives import Operative
        operative: Operative = op

        for on_pickup in self.on_pickup_callbacks:
            on_pickup(self, operative)

    def redraw(self):
        if not self.color:
            return

        screen = pygame.display.get_surface()

        pygame.draw.circle(screen, self.color,
                           self.rect.center, self.radius)
        screen.blit(self.image, self.rect)

        if self.capture_range_visible:
            pygame.draw.circle(screen, self.color, self.rect.center,
                               self.capture_range.to_screen_size(), CAPTURE_RANGE_OUTLINE_WIDTH)
