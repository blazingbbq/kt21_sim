from board.gameboard import GameBoard
from board.terrain.pieces import *
import utils.distance


class LootAndSalvageKillzone:
    def __init__(self, gameboard: GameBoard):
        gameboard.add_terrain(
            # Bottom left quad
            Wall(
                pos=(gameboard.rect.left + utils.distance.from_inch(6).to_screen_size(),
                     gameboard.rect.bottom - utils.distance.from_inch(4).to_screen_size()),
                orientation=(-1, -1),
                horizontal_side_length=utils.distance.INCH * 4,
                vertical_side_length=utils.distance.INCH * 6,
            ),
            Pipe(
                pos=(gameboard.rect.left + utils.distance.from_inch(5).to_screen_size(),
                     gameboard.rect.bottom - utils.distance.from_inch(5).to_screen_size()),
                orientation=(-1, 1),
                horizontal_side_length=utils.distance.ZERO,
                vertical_side_length=utils.distance.INCH * 2,
            ),

            # Bottom right quad
            Pipe(
                pos=(gameboard.rect.right - utils.distance.from_inch(4).to_screen_size(),
                     gameboard.rect.bottom - utils.distance.from_inch(4).to_screen_size()),
                orientation=(-1, -1),
                horizontal_side_length=utils.distance.INCH * 6.5,
                vertical_side_length=utils.distance.INCH * 0.5,
            ),
            Box(
                pos=(gameboard.rect.right - utils.distance.from_inch(3).to_screen_size(),
                     gameboard.rect.bottom - utils.distance.from_inch(5.5).to_screen_size()),
                orientation=(-1, -1),
                horizontal_side_length=utils.distance.INCH * 3,
                vertical_side_length=utils.distance.INCH * 2,
                heavy=True,
            ),

            # Center
            Pipe(
                pos=(gameboard.rect.centerx - utils.distance.from_inch(0).to_screen_size(),
                     gameboard.rect.bottom - utils.distance.from_inch(5.7).to_screen_size()),
                orientation=(1, -1),
                horizontal_side_length=utils.distance.INCH * 0,
                vertical_side_length=utils.distance.INCH * 5,
                thickness=utils.distance.INCH * 0.8,
            ),
            Wall(
                pos=(gameboard.rect.centerx + utils.distance.from_inch(1.5).to_screen_size(),
                     gameboard.rect.centery + utils.distance.from_inch(3.5).to_screen_size()),
                orientation=(-1, -1),
                horizontal_side_length=utils.distance.INCH * 3,
                vertical_side_length=utils.distance.INCH * 4,
            ),

            # Mid right
            Pipe(
                pos=(gameboard.rect.right - utils.distance.from_inch(5).to_screen_size(),
                     gameboard.rect.centery + utils.distance.from_inch(2).to_screen_size()),
                orientation=(1, 1),
                horizontal_side_length=utils.distance.INCH * 2,
                vertical_side_length=utils.distance.INCH * 3,
            ),

            # Mid left
            Pipe(
                pos=(gameboard.rect.centerx - utils.distance.from_inch(3).to_screen_size(),
                     gameboard.rect.centery + utils.distance.from_inch(3).to_screen_size()),
                orientation=(-1, -1),
                horizontal_side_length=utils.distance.INCH * 3.5,
                vertical_side_length=utils.distance.INCH * 0.75,
                thickness=utils.distance.INCH * 0.75,
            ),
            Pipe(
                pos=(gameboard.rect.left + utils.distance.from_inch(3).to_screen_size(),
                     gameboard.rect.centery - utils.distance.from_inch(4).to_screen_size()),
                orientation=(1, 1),
                horizontal_side_length=utils.distance.INCH * 0,
                vertical_side_length=utils.distance.INCH * 4,
                thickness=utils.distance.INCH * 0.8,
            ),
            Pipe(
                pos=(gameboard.rect.centerx - utils.distance.from_inch(1.25).to_screen_size(),
                     gameboard.rect.centery - utils.distance.from_inch(2.5).to_screen_size()),
                orientation=(-1, 1),
                horizontal_side_length=utils.distance.INCH * 3,
                vertical_side_length=utils.distance.INCH * 0.5,
                thickness=utils.distance.INCH * 0.6,
            ),

            # Top left quad
            Wall(
                pos=(gameboard.rect.left + utils.distance.from_inch(5).to_screen_size(),
                     gameboard.rect.top + utils.distance.from_inch(9).to_screen_size()),
                orientation=(1, -1),
                horizontal_side_length=utils.distance.INCH * 4,
                vertical_side_length=utils.distance.INCH * 6,
            ),
            Box(
                pos=(gameboard.rect.centerx - utils.distance.from_inch(0.5).to_screen_size(),
                     gameboard.rect.top + utils.distance.from_inch(4.5).to_screen_size()),
                orientation=(1, 1),
                horizontal_side_length=utils.distance.INCH * 1.5,
                vertical_side_length=utils.distance.INCH * 3,
                heavy=False,
            ),

            # Mid right
            Pipe(
                pos=(gameboard.rect.right - utils.distance.from_inch(5).to_screen_size(),
                     gameboard.rect.centery + utils.distance.from_inch(0).to_screen_size()),
                orientation=(1, -1),
                horizontal_side_length=utils.distance.INCH * 0,
                vertical_side_length=utils.distance.INCH * 2.5,
                thickness=utils.distance.INCH * 0.8,
            ),

            # Top right quad
            Wall(
                pos=(gameboard.rect.right - utils.distance.from_inch(7).to_screen_size(),
                     gameboard.rect.top + utils.distance.from_inch(4).to_screen_size()),
                orientation=(1, 1),
                horizontal_side_length=utils.distance.INCH * 5,
                vertical_side_length=utils.distance.INCH * 2.5,
            ),
            LowWall(
                pos=(gameboard.rect.right - utils.distance.from_inch(6).to_screen_size(),
                     gameboard.rect.centery - utils.distance.from_inch(3.25).to_screen_size()),
                orientation=(1, -1),
                horizontal_side_length=utils.distance.INCH * 4,
                vertical_side_length=utils.distance.INCH * 1,
            ),
            Pipe(
                pos=(gameboard.rect.right - utils.distance.from_inch(4).to_screen_size(),
                     gameboard.rect.centery - utils.distance.from_inch(5).to_screen_size()),
                orientation=(1, -1),
                horizontal_side_length=utils.distance.INCH * 0,
                vertical_side_length=utils.distance.INCH * 2.5,
                thickness=utils.distance.INCH * 0.65,
            ),
        )
