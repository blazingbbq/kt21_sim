from typing import Callable, List, Tuple
from enum import Enum
import pygame
from abc import ABC
from .datacard import *
from .action import Action, ActionNames
from .action_conditions import ActionConditions
import utils.player_input


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
        self.actions: List[Action] = [
            Action(name=ActionNames.NORMAL_MOVE,
                   ap_cost=1,
                   on_action=self.perform_normal_move,
                   valid_this_turn=ActionConditions.can_move()),
            Action(name=ActionNames.SHOOT,
                   ap_cost=1,
                   on_action=self.perform_shoot,
                   valid_this_turn=ActionConditions.can_shoot()),
            Action(name=ActionNames.CHARGE,
                   ap_cost=1,
                   on_action=self.perform_charge,
                   valid_this_turn=ActionConditions.can_charge()),
            Action(name=ActionNames.FIGHT,
                   ap_cost=1,
                   on_action=self.perform_fight,
                   valid_this_turn=ActionConditions.can_fight()),
            Action(name=ActionNames.DASH,
                   ap_cost=1,
                   on_action=self.perform_dash,
                   valid_this_turn=ActionConditions.can_dash()),
            Action(name=ActionNames.FALL_BACK,
                   ap_cost=2,
                   on_action=self.perform_fall_back,
                   valid_this_turn=ActionConditions.can_fall_back()),
            Action(name=ActionNames.PICK_UP,
                   ap_cost=1,
                   on_action=self.perform_pick_up,
                   valid_this_turn=ActionConditions.can_pick_up()),
        ]
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

    # Sets the position of the operative. Not to be confused with normal_move, the action callback.
    def move(self, center: Tuple[float, float]):
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
            valid_actions[ActionNames.PASS] = Action(name=ActionNames.PASS,
                                                     ap_cost=0,
                                                     on_action=self.perform_pass,
                                                     valid_this_turn=ActionConditions.can_pass())

            # Get player selection
            selected_action = None
            for selection in utils.select_from_list(relative_to=self.rect.center,
                                                    items=valid_actions.keys()):
                if selection != None:
                    selected_action = valid_actions.get(selection)
                    break
                self.team.gamestate.redraw()

            # Perform action
            if selected_action.on_action():
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
        for selection in utils.select_from_list(relative_to=self.rect.center,
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

    # Action callbacks
        # TODO: Implement action callbacks

    def perform_normal_move(self):
        return True

    def perform_shoot(self):
        return True

    def perform_charge(self):
        return True

    def perform_fight(self):
        return True

    def perform_dash(self):
        return True

    def perform_fall_back(self):
        return True

    def perform_pick_up(self):
        return True

    def perform_pass(self):
        self.action_points = -1
        return True
