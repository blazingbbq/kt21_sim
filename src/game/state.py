class _GlobalState:
    gamestate = None


def init():
    from state import GameState
    _GlobalState.gamestate = GameState()

    return _GlobalState.gamestate


def get():
    return _GlobalState.gamestate


def redraw():
    _GlobalState.gamestate.redraw()
