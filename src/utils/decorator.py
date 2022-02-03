import utils.player_input


def on_hover(hover_callback):
    def _on_hover(func):
        def wrapper(self, *args, **kwargs):
            # Call base function
            func_output = func(self, *args, **kwargs)

            # Check and trigger hover callback
            try:
                if utils.player_input.hovering() and self.rect.collidepoint(utils.player_input.mouse_pos()):
                    hover_callback(self)
            except:
                # Do nothing if the hover callback fails
                pass

            # Return expected func output
            return func_output
        return wrapper
    return _on_hover
