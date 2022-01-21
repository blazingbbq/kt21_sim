import pygame
from .team import *
from .terrain import *


class GameState:
    def __init__(self):
        self.teams: Team = []
        self.terrain: Terrain = Terrain()
        # TODO: Make terrain a child of Board object

    def update(self):
        """"""

    def redraw(self):
        self.terrain.redraw()
        for t in self.teams:
            t.redraw()

    def add_team(self, team: Team):
        self.teams.append(team)
