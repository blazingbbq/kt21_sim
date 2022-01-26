from typing import Tuple, Union
import pygame
import utils.distance


class Ruler:
    def __init__(self, width: int = 2):
        self.visible = False
        self.color = 0xffffff
        self.start_pos = (0, 0)
        self.end_pos = (0, 0)
        self.width = width
        self.length = 0

    def hide(self):
        self.visible = False

    @property
    def destination(self):
        return self.end_pos

    def measure(self,
                from_: Tuple[int, int],
                towards: Tuple[int, int],
                max_length: Union[utils.distance.Distance, None] = None):
        self.start_pos = from_
        self.end_pos = towards
        self.length = utils.distance.from_px(
            abs(pygame.Vector2(
                self.end_pos[0] - self.start_pos[0],
                self.end_pos[1] - self.start_pos[1]
            ).length())
        )

        # Cap length if measuring beyond max
        if max_length != None and self.length > max_length and from_ != towards:
            scaled_line = pygame.Vector2(
                towards[0] - from_[0],
                towards[1] - from_[1],
            )
            scaled_line.scale_to_length(max_length.to_screen_size())
            self.end_pos = (from_[0] + scaled_line.x,
                            from_[1] + scaled_line.y)
            self.length = max_length

        return self.length

    def measure_and_show(self,
                         from_: Tuple[int, int],
                         towards: Tuple[int, int],
                         max_length: Union[Tuple[int, int], None] = None,
                         color=None):
        if color != None:
            self.color = color
        self.visible = True

        return self.measure(from_=from_, towards=towards, max_length=max_length)

    def redraw(self):
        if self.visible:
            # TODO: Print out length of ruler underneath
            pygame.draw.line(
                # TODO: Use different surface for drawing this so that its rendered above everything else
                surface=pygame.display.get_surface(),
                color=self.color,
                start_pos=self.start_pos,
                end_pos=self.end_pos,
                width=self.width,
            )
