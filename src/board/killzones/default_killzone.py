from board.gameboard import GameBoard
from board.terrain.pieces import *
import utils.distance


class DefaultKillzone:
    def __init__(self, gameboard: GameBoard):
        gameboard.add_terrain(
            Wall(
                pos=gameboard.rect.center,
                orientation=(1, 1),
                horizontal_side_length=utils.distance.INCH * 4,
                vertical_side_length=utils.distance.INCH * 3,
            ),
            LowWall(
                pos=gameboard.rect.center,
                orientation=(-1, 1),
                horizontal_side_length=utils.distance.INCH * 4,
                vertical_side_length=utils.distance.INCH * 3,
            ),
            Pipe(
                pos=gameboard.rect.center,
                orientation=(1, -1),
                horizontal_side_length=utils.distance.INCH * 4,
                vertical_side_length=utils.distance.INCH * 3,
            ),
            Box(
                pos=gameboard.rect.center,
                orientation=(-1, -1),
                horizontal_side_length=utils.distance.INCH * 4,
                vertical_side_length=utils.distance.INCH * 3,
            ),
        )
