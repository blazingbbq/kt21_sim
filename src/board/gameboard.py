from .terrain import *


class GameBoard:
    def __init__(self):
        self.terrain = Terrain()

    def redraw(self):
        """"""
        # TODO: Draw game board

        # Redraw terrain
        self.terrain.redraw()
