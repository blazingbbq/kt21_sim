from board.gameboard import GameBoard
from board.terrain.low_wall import LowWall
from board.terrain.wall import Wall
import utils.distance


class DefaultKillzone:
    def __init__(self, gameboard: GameBoard):
        gameboard.add_terrain(
            LowWall(gameboard.rect.center),
            Wall(gameboard.rect.center),
            Wall((gameboard.rect.centerx, gameboard.rect.centery -
                  utils.distance.from_inch(2.5).to_screen_size())),
        )
