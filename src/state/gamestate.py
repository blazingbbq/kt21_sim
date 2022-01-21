import pygame
from .team import *
from board import *


class GameState:
    def __init__(self):
        self.teams: Team = []
        self.gameboard: GameBoard = GameBoard()

    def update(self):
        """"""

    def redraw(self):
        self.gameboard.redraw()
        for t in self.teams:
            t.redraw()

    def add_team(self, team: Team):
        self.teams.append(team)
