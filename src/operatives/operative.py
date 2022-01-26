from typing import Callable, List, Tuple
from enum import Enum
import pygame
from abc import ABC
from .datacard import *
from action import Action
from utils.distance.ruler import Ruler
import utils.player_input
import utils.distance


class Order(Enum):
    ENGAGE = 1
    CONCEAL = 2


class Operative(pygame.sprite.Sprite, ABC):
    color = 0xffffff  # Default sprite color
    outline_width = 2  # Default outline width

    def __init__(self, datacard: Datacard):
        from state.team import Team
        # Team is set by the team when this operative is added to that team
        self.team: Team = None

        # Game object init
        self.datacard = datacard
        self.render_group = pygame.sprite.RenderPlain()
        self.apl_modifier = 0
        self.ruler = Ruler()

        # Status
        self.deployed = False
        self.ready = False
        self.visible = False

        self.order = Order.CONCEAL
        self.action_points = 0

        # Sprite init
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, 0, 0).inflate(
            self.datacard.physical_profile.base.to_screen_size(), self.datacard.physical_profile.base.to_screen_size())
        self.outline_color = None

        # Callback hooks
        self.on_activation_end: Callable[[Operative], None] = []

        # Actions
        self.free_actions: List[str] = []  # Reference free actions by name
        self.actions_taken: List[Action] = []
        self.actions: List[Action] = []

        import action.universal
        self.actions.extend(action.universal.universal_actions)
        self.actions.extend(self.datacard.unique_actions)

    def on_added_to_team(self):
        """Callback for when this operative is added to a team. Used to register team-based callbacks and properties
        """
        pass

    def on_deployed(self):
        self.deployed = True
        self.visible = True
        self.select_order()

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def highlight(self, color):
        self.outline_color = color

    def unhighlight(self):
        self.outline_color = None

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, value):
        self.concealed = value == Order.CONCEAL
        self._order = value

    # Sets the position of the operative. Not to be confused with perform_move, the action callback.
    def move_to(self, center: Tuple[float, float]):
        self.rect.center = center

    def redraw(self):
        if not self.visible:
            return

        screen = pygame.display.get_surface()
        if self.color:
            pygame.draw.circle(screen, self.color,
                               self.rect.center, self.rect.width/2)
        if self.outline_color:
            pygame.draw.circle(screen, self.outline_color,
                               self.rect.center, self.rect.width/2, self.outline_width)

        # TODO: Display icon idicating current order

        self.render_group.draw(screen)
        self.ruler.redraw()

    @property
    def apl_modifier(self):
        return self._apl_modifier

    @apl_modifier.setter
    def apl_modifier(self, value):
        # APL modifier can never be more than +1/-1
        if value > 0:
            self._apl_modifier = 1
        elif value < 0:
            self._apl_modifier = -1
        else:
            self._apl_modifier = 0

    def activate(self):
        # Select engage/conceal order
        if self.team.gamestate.current_turn != 1:
            self.select_order()

        self.actions_taken = []
        self.action_points = self.datacard.physical_profile.action_point_limit + self.apl_modifier
        # While the operative has action points remaining, perform actions
        while self.action_points > -1:
            valid_actions = {
                a.name: a for a in self.actions if a.cost(self.free_actions) <= self.action_points and a.valid_this_turn(a, self)}
            if len(valid_actions) <= 0:
                # Nothing else to do!
                break

            # Passing is always a valid action
            import action.universal
            valid_actions[action.names.PASS] = action.universal.pass_action

            # Get player selection
            selected_action = None
            for selection in utils.player_input.select_from_list(relative_to=self.rect.center,
                                                                 items=valid_actions.keys()):
                if selection != None:
                    selected_action = valid_actions.get(selection)
                    break
                self.team.gamestate.redraw()

            # Perform action
            if selected_action.on_action(self):
                self.action_points -= selected_action.cost(self.free_actions)
                self.actions_taken.append(selected_action)

        # APL modifier reset at the end of the current/next activation
        self.APL_modifier = 0
        self.ready = False
        self.free_actions = []

        for on_activation_end in self.on_activation_end:
            on_activation_end(self)

    def select_order(self):
        orders = {"Engage": Order.ENGAGE, "Conceal": Order.CONCEAL}
        for selection in utils.player_input.select_from_list(relative_to=self.rect.center,
                                                             items=orders.keys()):
            if selection != None:
                self.order = orders.get(selection)
                break
            self.team.gamestate.redraw()

    def register_on_activation_end(self, cb):
        self.on_activation_end.append(cb)

    def enemies_within_engagement_range(self):
        within_engagement_range = []
        for enemy_team in [team for team in self.team.gamestate.teams if team != self.team]:
            for op in enemy_team.operatives:
                if utils.distance.between(self.rect.center, op.rect.center) < utils.distance.TRIANGLE + self.datacard.physical_profile.base/2 + op.datacard.physical_profile.base/2:
                    within_engagement_range.append(op)

        return within_engagement_range

    def perform_move(self, distance: utils.distance.Distance, falling_back: bool = False, charging: bool = False):
        # TODO: Save current position in case we want to cancel move

        # Create a new Distance object to prevent us from accidentally changing the reference we're given
        remaining_movement = utils.distance.Distance(distance)
        while remaining_movement > 0:
            for click_loc in utils.player_input.wait_for_click():
                # Check that operative can be placed at final destination
                # Cannot move over the edge of the killzone
                # Cannot move through another unit (unless flying ?)
                # Cannot move through terrain, must traverse or climb over
                #   - check for intersection with terrain, if it does, request cost_for_traversal() from it
                #   - Must jump or drop across gaps / ledges (see terrain)
                # Cannot move within engagement range of enemy operative

                # If falling_back, can move through engagement range of enemy units
                # If charging, must finish move within engagement range of enemy unit
                # If charging, cannot move through engagement range of other units unless another friendly operative is currently engaged with it

                # TODO: Check all required conditions for the move
                if click_loc != None:
                    break

                self.ruler.measure_and_show(
                    from_=self.rect.center,
                    towards=utils.player_input.mouse_pos(),
                    max_length=remaining_movement,
                )
                self.team.gamestate.redraw()

            self.ruler.hide()
            self.move_to(self.ruler.destination)
            self.team.gamestate.redraw()
            remaining_movement -= self.ruler.length.round_up(
                increment=utils.distance.TRIANGLE)

        return True
