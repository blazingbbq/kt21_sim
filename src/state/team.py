from operatives import *


class Team:
    def __init__(self):
        self.victory_points = 0
        self.command_points = 0
        self.operatives: list[Operative] = []

    def redraw(self):
        for op in self.operatives:
            op.redraw()

    def add_operative(self, operative: Operative):
        self.operatives.append(operative)
