from typing import Any, Callable, List, Tuple, Union
import functools
import pygame
import game.ui


def mouse_pos():
    """Wrapper for pygame's mouse.get_pos() function.

    Returns:
        Tuple[float, float]: The location of the mouse cursor.
    """
    return pygame.mouse.get_pos()


def left_mb_down():
    return pygame.mouse.get_pressed(num_buttons=3)[0]


def click_pos():
    """Get the current click position if currently clicking.
    """
    click_loc = None
    if left_mb_down():
        click_loc = mouse_pos()

    return click_loc


def wait_for_click():
    while True:
        yield click_pos()


def select_from_list(relative_to: Tuple[int, int], items: Union[List[str], List[Tuple[str, str]]]):
    longest_item = functools.reduce(max, [len(i) for i in items])
    # FIXME: Do not hardcode width / height of each list entry (item height + fixed border/shadow)
    list_dimensions: Tuple[int, int] = (
        longest_item * 10, len(items) * 20 + 6)
    selection_list = game.ui.elements.UISelectionList(
        relative_rect=pygame.Rect(relative_to, list_dimensions),
        item_list=items,
        manager=game.ui.manager)
    # TODO: Position top-right if list is too low

    while True:
        selection = selection_list.get_single_selection()
        if selection != None:
            game.ui.remove(selection_list)
        yield selection
