from typing import Any, Callable, List, Tuple
import pygame


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


def get_click_blocking(spin: Callable[[], None]):
    """Wait for the mouse to perform a mouse click.

    Args:
        spin (Callable[[], None]): A callback to use while the waiting for mouse input.

    Returns:
        Tuple[float, float]: The location of the mouse click, on release.
    """
    # Wait for mouse down
    while not left_mb_down():
        if spin != None:
            spin()

    # Get mouse position until mouse button released
    click_loc = mouse_pos()
    while left_mb_down():
        if spin != None:
            spin()

    return click_loc


def wait_for_selection(validate: Callable[[Tuple[float, float]], bool], spin: Callable[[], None]):
    while True:
        click_loc = get_click_blocking(spin)
        if validate(click_loc):
            break

    return click_loc


def wait_for_sprite_selection(targets: List[pygame.sprite.Sprite], spin: Callable[[], None]):
    while True:
        click_loc = get_click_blocking(spin=spin)
        for target in targets:
            if target.rect.collidepoint(click_loc):
                return target
