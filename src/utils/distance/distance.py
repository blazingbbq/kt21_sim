from math import sqrt
from typing import Tuple, Union
import pygame
import board.gameboard

MM_TO_INCH: float = 0.04  # Assume 25mm ~= 1"


class Distance:
    # Global tracker of pixels per inch
    inch_size = 1

    def __init__(self, distance):
        if isinstance(distance, Distance):
            distance = distance.distance
        self.distance = distance

    def __str__(self):
        return str(self.distance)

    def __add__(self, other):
        if isinstance(other, Distance):
            other = other.distance
        return Distance(self.distance + other)

    def __iadd__(self, other):
        if isinstance(other, Distance):
            self.distance += other.distance
        else:
            self.distance += other
        return self

    def __sub__(self, other):
        if isinstance(other, Distance):
            other = other.distance
        return Distance(self.distance + other)

    def __isub__(self, other):
        if isinstance(other, Distance):
            self.distance -= other.distance
        else:
            self.distance -= other
        return self

    def __mul__(self, other):
        if isinstance(other, Distance):
            other = other.distance
        return Distance(self.distance * other)

    def __rmul__(self, other):
        return other.__mul__(self)

    def __div__(self, other):
        if isinstance(other, Distance):
            other = other.distance
        return Distance(self.distance / other)

    def __truediv__(self, other):
        return self.__div__(other)

    def __floordiv__(self, other):
        if isinstance(other, Distance):
            other = other.distance
        return Distance(self.distance // other)

    def __lt__(self, other):
        if isinstance(other, Distance):
            return self.distance < other.distance
        return self.distance < other

    def __le__(self, other):
        if isinstance(other, Distance):
            return self.distance <= other.distance
        return self.distance <= other

    def __gt__(self, other):
        if isinstance(other, Distance):
            return self.distance > other.distance
        return self.distance > other

    def __ge__(self, other):
        if isinstance(other, Distance):
            return self.distance >= other.distance
        return self.distance >= other

    def __float__(self):
        return float(self.distance)

    def to_screen_size(self):
        return self.distance * self.inch_size

    def round_up(self, increment):
        if increment == None:
            increment = TRIANGLE
        if isinstance(increment, Distance):
            increment = increment.distance

        # Do not increment if the current distance value is exactly divisible by the increment
        if self.distance % increment != 0:
            self.distance += increment - (self.distance % increment)
        return self

    def copy(self):
        return Distance(self.distance)


# Distance conversions to inches
TRIANGLE: Distance = Distance(1.0)
CIRCLE: Distance = Distance(2.0)
SQUARE: Distance = Distance(3.0)
PENTAGON: Distance = Distance(6.0)
ENGAGEMENT_RANGE: Distance = TRIANGLE

MM: Distance = Distance(MM_TO_INCH)
INCH: Distance = Distance(1.0)


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


def between(from_: pygame.math.Vector2, to: pygame.math.Vector2, max_dist: Union[int, None] = None):
    px_distance = pygame.Vector2(from_).distance_to(pygame.Vector2(to))

    if max_dist != None:
        px_distance = min(max_dist, px_distance)
    return from_px(px_distance)


def between_line_and_point(line_from: Tuple[int, int], line_to: Tuple[int, int], point: Tuple[int, int]):
    # See https://stackoverflow.com/a/2233538
    x1 = line_from[0]
    x2 = line_to[0]
    x3 = point[0]
    y1 = line_from[1]
    y2 = line_to[1]
    y3 = point[1]

    px = x2-x1
    py = y2-y1
    norm = px*px + py*py
    if norm == 0:  # Basic attempt at preventing division by 0
        norm = 0.000000000001

    u = ((x3 - x1) * px + (y3 - y1) * py) / float(norm)

    # For line segments, only test values of u between 0 and 1
    u = max(0, u)
    u = min(u, 1)

    # The point of intersection
    x = x1 + u * px
    y = y1 + u * py

    # Find the distance between the point of intersection and the target point
    dx = x - x3
    dy = y - y3
    dist = sqrt(dx**2 + dy**2)

    return from_px(dist)


def between_infinite_line_and_point(line_from: Tuple[int, int], line_to: Tuple[int, int], point: Tuple[int, int]):
    # See https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line#Line_defined_by_two_points
    x2 = line_to[0]
    x1 = line_from[0]
    x0 = point[0]
    y2 = line_to[1]
    y1 = line_from[1]
    y0 = point[1]

    top_half = abs((x2 - x1) * (y1 - y0) - (x1 - x0) * (y2 - y1))
    bottom_half = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    distance = top_half / bottom_half

    return from_px(distance)
