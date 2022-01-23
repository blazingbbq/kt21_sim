import pygame_gui
from pygame_gui import *  # Proxy all pygame_gui.* imports as game.ui.*

import game.screen
import game.clock

manager: pygame_gui.UIManager = None


def init():
    game.ui.manager = pygame_gui.UIManager(game.screen.size())


def process(event):
    game.ui.manager.process_events(event)


def redraw():
    game.ui.manager.update(game.clock.delta() / 1000.0)
    game.ui.manager.draw_ui(game.screen.get_surface())


def remove(element: pygame_gui.core.ui_element.UIElement):
    element.kill()
