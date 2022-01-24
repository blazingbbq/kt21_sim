import pygame
import board.gameboard

MM_TO_INCH: float = 0.04  # Assume 25mm ~= 1"


class Distance:

    # Global tracker of pixels per inch
    inch_size = 1

    def __init__(self, distance):
        self.distance = distance

    def __add__(self, other):
        self.distance += other.distance
        return self

    def __sub__(self, other):
        self.distance += other.distance
        return self

    def __mul__(self, val):
        self.distance *= val
        return self

    def __rmul__(self, val):
        return self.__mul__(val)

    def __div__(self, val):
        self.distance /= val
        return self

    def __truediv__(self, val):
        return self.__div__(val)

    def __floordiv__(self, val):
        self.distance //= val
        return self

    def __lt__(self, other):
        return self.distance < other.distance

    def __gt__(self, other):
        return other < self

    def __float__(self):
        return float(self.distance)

    def to_screen_size(self):
        return self.distance * self.inch_size


# Distance conversions to inches
TRIANGLE: float = Distance(1.0)
CIRCLE: float = Distance(2.0)
SQUARE: float = Distance(3.0)
PENTAGON: float = Distance(6.0)
ENGAGEMENT_RANGE: float = TRIANGLE

def from_triangle(num: int):
    return Distance(TRIANGLE * num)


def from_circle(num: int):
    return Distance(CIRCLE * num)


def from_square(num: int):
    return Distance(SQUARE * num)


def from_pentagon(num: int):
    return Distance(PENTAGON * num)


def from_mm(num: int):
    return Distance(MM_TO_INCH * num)


def from_inch(num: int):
    return Distance(num)


def from_px(num: float):
    return Distance(num / Distance.inch_size)


def update_inch_size():
    Distance.inch_size = (pygame.display.get_surface().get_rect(
    ).height - board.gameboard.GAMEBOARD_PADDING * 2) // board.gameboard.GAMEBOARD_HEIGHT


def between(from_: pygame.math.Vector2, to: pygame.math.Vector2):
    px_distance = pygame.Vector2(from_).distance_to(pygame.Vector2(to))
    return from_px(px_distance)
