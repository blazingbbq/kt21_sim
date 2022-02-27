from typing import Union
import game.ui
import config

# Theming
KEYNAME_BACKGROUND_COLOR = "#666666"
ERROR_MESSAGE_BACKGROUND_COLOR = 0xff0000
ERROR_MESSAGE_COLOR = 0xff0000
DEBUG_MESSAGE_BACKGROUND_COLOR = 0xffff00
DEBUG_MESSAGE_COLOR = 0xffff00


def preload_fonts():
    game.ui.manager.preload_fonts([
        # {'name': 'fira_code', 'point_size': 14, 'style': 'regular'},
        {'name': 'fira_code', 'point_size': 14, 'style': 'italic'},
        {'name': 'fira_code', 'point_size': 14, 'style': 'bold'},
        {'name': 'fira_code', 'point_size': 14, 'style': 'bold_italic'},
    ])


def bold(str: str):
    return f"<b>{str}</b>"


def italic(str: str):
    return f"<i>{str}</i>"


def underline(str: str):
    return f"<u>{str}</u>"


def linebreak():
    return "<br>"


# Alias for linebreak
def newline():
    return linebreak()


def with_background(str: str, bgcolor: Union[str, int]):
    if isinstance(bgcolor, int):
        bgcolor = "#{0:06X}".format(bgcolor)
    return f"<body bgcolor='{bgcolor}'>{str}</body>"


# Wrapper for with_font to set just the text color
def with_color(str: str, color: Union[str, int]):
    return with_font(str=str, color=color)


def with_font(str: str,
              font: Union[str, None] = None,
              color: Union[str, int, None] = None,
              size: Union[int, None] = None):
    font_attribute = ""
    color_attribute = ""
    size_attribute = ""
    if font:
        font_attribute = f"face='{font}'"
    if color:
        if isinstance(color, int):
            color = "#{0:06X}".format(color)
        color_attribute = f"color='{color}'"
    if size:
        size_attribute = f"size='{size}'"
    return f"<font {font_attribute} {color_attribute} {size_attribute}>{str}</font>"


def print(str: str,
          end: str = "<br>"):
    game.ui.layout.console.append_html_text(f"{str}{end}")


def print_err(str: str):
    print(bold(with_background("ERROR:", ERROR_MESSAGE_BACKGROUND_COLOR)
               ) + " " + with_color(str, ERROR_MESSAGE_COLOR))


def debug(str: str):
    if config.DEBUG:
        print(bold(with_background("DEBUG:", DEBUG_MESSAGE_BACKGROUND_COLOR)
                   ) + " " + with_color(str, DEBUG_MESSAGE_COLOR))

# Misc console printing utils

def keyname(keyname: str):
    return bold(with_background(keyname.upper(), KEYNAME_BACKGROUND_COLOR))


def tag(str: str, color):
    return bold(with_color(str="[" + str.upper() + "]", color=color))
