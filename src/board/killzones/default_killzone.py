from board.gameboard import GameBoard
from board.terrain.low_wall import LowWall
from board.terrain.wall import Wall


class DefaultKillzone:
    def __init__(self, gameboard: GameBoard):
        gameboard.add_terrain(
            LowWall(gameboard.rect.center),
            Wall(gameboard.rect.center),
        )
