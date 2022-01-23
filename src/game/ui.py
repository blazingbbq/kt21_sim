import pygame
import pygame_gui
from pygame_gui import *  # Proxy all pygame_gui.* imports as game.ui.*

import game.screen
import game.clock
import board.gameboard
import utils.distance


class Layout:
    # Margins
    default_padding = 10
    default_margins = {'left': default_padding,
                       'right': default_padding,
                       'top': default_padding,
                       'bottom': default_padding}

    # Anchors
    top_right_anchors = {'left': 'right',
                         'right': 'right',
                         'top': 'top',
                         'bottom': 'top'}
    top_left_anchors = {'left': 'left',
                        'right': 'left',
                        'top': 'top',
                        'bottom': 'top'}
    stretch_anchors = {'left': 'left',
                       'right': 'right',
                       'top': 'top',
                       'bottom': 'bottom'}

    def __init__(self):
        self.update_layout()

    def update_layout(self):
        self.window = game.screen.get_surface().get_rect()
        self.window_container = pygame_gui.core.UIContainer(
            relative_rect=self.window, manager=game.ui.manager)

        # Side panels
        left_panel_rect = pygame.Rect(self.gameboard_padding, self.gameboard_padding,
                                      self.side_panel_width, self.window.height - self.gameboard_padding*2)
        right_panel_rect = pygame.Rect(-self.side_panel_width, self.gameboard_padding,
                                       self.side_panel_width, self.window.height - self.gameboard_padding*2)

        self.left_panel = game.ui.elements.ui_panel.UIPanel(relative_rect=left_panel_rect,
                                                            starting_layer_height=0,
                                                            container=self.window_container,
                                                            manager=game.ui.manager,
                                                            margins=self.default_margins,
                                                            anchors=self.top_left_anchors
                                                            )
        self.right_panel = game.ui.elements.ui_panel.UIPanel(relative_rect=right_panel_rect,
                                                             starting_layer_height=0,
                                                             container=self.window_container,
                                                             manager=game.ui.manager,
                                                             margins=self.default_margins,
                                                             anchors=self.top_right_anchors
                                                             )

    @property
    def side_panel_width(self):
        gameboard_width = utils.distance.from_inch(
            board.gameboard.GAMEBOARD_WIDTH).to_screen_size()
        return (self.window.width - gameboard_width) / 2 - self.gameboard_padding

    @property
    def gameboard_padding(self):
        return (self.window.height - utils.distance.from_inch(board.gameboard.GAMEBOARD_HEIGHT).to_screen_size()) / 2


manager: pygame_gui.UIManager = None
layout: Layout = None


def init():
    game.ui.manager = pygame_gui.UIManager(game.screen.size())
    game.ui.layout = Layout()


def process(event):
    game.ui.manager.process_events(event)


def redraw():
    game.ui.manager.update(game.clock.delta() / 1000.0)
    game.ui.manager.draw_ui(game.screen.get_surface())


def remove(element: pygame_gui.core.ui_element.UIElement):
    element.kill()
