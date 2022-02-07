from typing import List, Tuple, Union
import functools
import pygame
import game.ui
import game.clock
import game.state

# Minimum time stationary before considering it a hover (in Milliseconds)
MIN_HOVER_TIME_MS = 20


class _InputState:
    last_key_states: List[bool] = []
    last_mouse_pos: Tuple[int, int] = (0, 0)
    time_hovering = 0


def update_input_state():
    update_key_statuses()
    update_mouse_status()


def update_key_statuses():
    _InputState.last_key_states = pygame.key.get_pressed()


def update_mouse_status():
    new_pos = mouse_pos()
    if new_pos == _InputState.last_mouse_pos:
        # Increment hover timer
        _InputState.time_hovering += game.clock.delta()
    else:
        # Otherwise, reset hover timer
        _InputState.time_hovering = 0

    _InputState.last_mouse_pos = new_pos


def key_pressed(key_code: int) -> bool:
    """Check that a key was pressed. Only full key presses count (i.e. key down -> key up).

    Args:
        key_code (int): The pygame key code corresponding to the key to check.

    Returns:
        bool: Returns whether the key was pressed.
    """
    return _InputState.last_key_states[key_code] == True and pygame.key.get_pressed()[key_code] == False


def hovering() -> bool:
    return _InputState.time_hovering > MIN_HOVER_TIME_MS


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
    """Waits for the player to complete a full mouse click (i.e. mouse up -> mouse down -> mouse up).

    Yields:
        Union[Tuple[int, int] | None]: Yields None while waiting for a full mouse click to be performed, then yields the location of the mouse click.
    """
    while True:
        # Wait for mouse down
        while not left_mb_down():
            yield None
        # Wait for mouse to be released
        while left_mb_down():
            yield None
        # Finally, yield mouse position for click
        yield mouse_pos()


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


def prompt_true_false(msg: str,
                      truthy_text: str = "Yes",
                      falsy_text: str = "No"):
    # Panel
    panel_rect = pygame.rect.Rect((0, 0), (400, 100))
    panel_rect.center = game.ui.layout.window.center
    panel = game.ui.elements.UIPanel(
        relative_rect=panel_rect,
        manager=game.ui.manager,
        starting_layer_height=0,
        container=game.ui.layout.window_container,
        # margins=game.ui.layout.default_margins,
    )

    # Prompt text
    label_padding_top = 12
    label_padding_sides = 10
    label_text_height = 24
    label = game.ui.elements.UILabel(
        relative_rect=pygame.Rect(
            label_padding_sides, label_padding_top, panel_rect.width - 2 * label_padding_sides, label_text_height),
        text=msg,
        manager=game.ui.manager,
        container=panel,
    )

    # Buttons
    button_padding = 2
    button_offset_centery = 8
    button_width = 100
    button_height = 24
    yes_button = game.ui.elements.UIButton(
        relative_rect=pygame.Rect(
            panel_rect.width/2 + button_padding, panel_rect.height/2 + button_offset_centery, button_width, button_height),
        text=truthy_text,
        starting_height=1,
        container=panel,
        manager=game.ui.manager,
        visible=True,
    )
    no_button = game.ui.elements.UIButton(
        relative_rect=pygame.Rect(
            panel_rect.width/2 - button_width - button_padding, panel_rect.height/2 + button_offset_centery, button_width, button_height),
        text=falsy_text,
        starting_height=1,
        container=panel,
        manager=game.ui.manager,
        visible=True,
    )

    result = False
    while True:
        if key_pressed(pygame.K_ESCAPE) or no_button.check_pressed():
            result = False
            break
        if key_pressed(pygame.K_RETURN) or yes_button.check_pressed():
            result = True
            break
        game.state.get().redraw()

    # Cleanup panel
    game.ui.remove(panel)
    game.state.get().redraw()
    return result
