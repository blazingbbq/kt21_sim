from typing import Callable, Tuple, Union
import pygame
import utils.distance
import game.preload
import game.state
from utils.distance.ruler import Ruler

DEFAULT_TOKEN_COLOR = 0xc54c21
CAPTURE_RANGE_OUTLINE_WIDTH = 1


class Objective(pygame.sprite.Sprite):
    def __init__(self, pos: Tuple[int, int],
                 pickup_able: bool = False,
                 once_per_turn: bool = False,
                 max_interactions: Union[int, None] = None):
        self.color = DEFAULT_TOKEN_COLOR
        self.capture_range_visible: bool = False
        self.capture_range = utils.distance.OBJECTIVE_CAPTURE_RANGE

        self.radius = utils.distance.from_mm(40).to_screen_size() / 2
        self.image, self.rect = game.preload.image("skull.png",
                                                   colorkey=game.preload.WHITE_COLORKEY,
                                                   scale_to=self.radius * 2)
        self.rect.center = pos
        self.ruler: Ruler = Ruler()

        from operatives import Operative
        self.on_capture_callbacks: Callable[[Objective, Operative], None] = []
        self.on_pickup_callbacks: Callable[[Objective, Operative], None] = []

        # Behavior
        self.pickup_able = pickup_able
        self.once_per_turn = once_per_turn
        self.turn_last_interacted_with = 0
        self.max_interactions = max_interactions
        self.current_interactions = 0

    def can_be_interacted_with(self):
        from state import GameState
        gamestate: GameState = game.state.get()
        if self.once_per_turn and gamestate.current_turn <= self.turn_last_interacted_with:
            return False

        return True

    def show_capture_range(self):
        self.capture_range_visible = True

    def hide_capture_range(self):
        self.capture_range_visible = False

    def move_to(self, center: Tuple[float, float]):
        self.rect.center = center

    def register_on_capture(self, cb):
        self.on_capture_callbacks.append(cb)

    def register_on_pickup(self, cb):
        self.on_pickup_callbacks.append(cb)

    def on_capture(self, op):
        from operatives import Operative
        operative: Operative = op

        for on_capture in self.on_capture_callbacks:
            on_capture(self, operative)

        self.turn_last_interacted_with = game.state.get().current_turn
        self.current_interactions += 1
        if self.max_interactions != None and self.current_interactions >= self.max_interactions:
            # Remove this objective from the field
            game.state.get().gameboard.objectives.remove(self)

    def on_pickup(self, op):
        from operatives import Operative
        operative: Operative = op

        # Set objective to be carried by operative and remove from gameboard
        operative.carried_objective = self
        operative.register_on_incapacitated(drop_objective)
        game.state.get().gameboard.objectives.remove(self)

        for on_pickup in self.on_pickup_callbacks:
            on_pickup(self, operative)

        self.turn_last_interacted_with = game.state.get().current_turn
        self.current_interactions += 1
        if self.max_interactions != None and self.current_interactions >= self.max_interactions:
            # TODO: Implement this if the situation comes up
            pass

    def redraw(self):
        if not self.color:
            return

        screen = pygame.display.get_surface()

        pygame.draw.circle(screen, self.color,
                           self.rect.center, self.radius)
        screen.blit(self.image, self.rect)

        if self.capture_range_visible:
            pygame.draw.circle(screen, self.color, self.rect.center,
                               self.capture_range.to_screen_size(), CAPTURE_RANGE_OUTLINE_WIDTH)

        self.ruler.redraw()

# Callback to drop objective on operative incapacitation


def drop_objective(op):
    from operatives import Operative
    operative: Operative = op

    if operative.carried_objective == None:
        # Unexpected, but its possible they don't have the objective anymore
        return False

    objective: Objective = operative.carried_objective
    # Operative no longer carries the objective
    operative.carried_objective = None

    # Add objective back to gameboard
    game.state.get().gameboard.objectives.append(objective)

    from state import GameState
    gamestate: GameState = game.state.get()

    # Place objective within TRIANGLE of the operative's location
    for click_loc in utils.player_input.wait_for_click():
        objective.ruler.measure_and_show(from_=operative.rect.center,
                                         towards=utils.player_input.mouse_pos(),
                                         max_length=utils.distance.TRIANGLE + operative.base_radius,
                                         color=0xffffff)

        if click_loc != None:
            break
        objective.move_to(objective.ruler.destination)
        gamestate.redraw()

    objective.ruler.hide()
    objective.move_to(objective.ruler.destination)
    gamestate.redraw()

    return True  # Return true in case this is used as an action callback
