import game.ui

# Theming
KEYNAME_BACKGROUND_COLOR = "#666666"


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


def with_background(str: str, bgcolor: str):
    return f"<body bgcolor='{bgcolor}'>{str}</body>"


# Wrapper for with_font to set just the text color
def with_color(str: str, color: str):
    return with_font(str=str, color=color)


def with_font(str: str,
              font: str = None,
              color: str = None,
              size: int = None):
    font_attribute = ""
    color_attribute = ""
    size_attribute = ""
    if font:
        font_attribute = f"face='{font}'"
    if color:
        color_attribute = f"color='{color}'"
    if size:
        size_attribute = f"size='{size}'"
    return f"<font {font_attribute} {color_attribute} {size_attribute}>{str}</font>"


def print(str: str):
    game.ui.layout.console.append_html_text(f"{str}<br>")


# Misc console printing utils

def keyname(keyname: str):
    return bold(with_background(keyname.upper(), KEYNAME_BACKGROUND_COLOR))
