import pygame
import board.gameboard


class Distance:
    # Distance conversions to inches
    TRIANGLE: float = 1.0
    CIRCLE: float = 2.0
    SQUARE: float = 3.0
    PENTAGON: float = 6.0

    MM_TO_INCH: float = 0.04  # Assume 25mm ~= 1"

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

    def __float__(self):
        return self.distance

    def to_screen_size(self):
        return self.distance * self.inch_size


def from_triangle(num: int):
    return Distance(Distance.TRIANGLE * num)


def from_circle(num: int):
    return Distance(Distance.CIRCLE * num)


def from_square(num: int):
    return Distance(Distance.SQUARE * num)


def from_pentagon(num: int):
    return Distance(Distance.PENTAGON * num)


def from_mm(num: int):
    return Distance(Distance.MM_TO_INCH * num)


def from_inch(num: int):
    return Distance(num)


def update_inch_size():
    Distance.inch_size = (pygame.display.get_surface().get_rect(
    ).height - board.gameboard.GAMEBOARD_PADDING * 2) // board.gameboard.GAMEBOARD_HEIGHT
