from typing import Callable, List, Tuple, Union
from enum import Enum
import pygame
from abc import ABC
from board.objectives.objective import Objective

from board.terrain.traits import TerrainTrait
from game.preload import WHITE_COLORKEY
from .datacard import *
from action import Action
from utils.distance.ruler import Ruler
import utils.player_input
import utils.distance
import utils.collision
import utils.line_of_sight
import utils.decorator
from game.console import bold, print, tag, with_color
import game.icon

ENGAGEMENT_RANGE_COLOR = 0x242726
ENGAGEMENT_RANGE_OUTLINE_WIDTH = 1

WEAPON_RANGE_COLOR = 0x242726
WEAPON_RANGE_OUTLINE_WIDTH = 1

VALID_MOVE_RULER_COLOR = 0xffffff
INVALID_MOVE_RULER_COLOR = 0xff0000

VALID_TARGET_HIGHLIGHT_COLOR = 0x00ff00

OPERATIVE_NAME_CONSOLE_COLOR = 0xc54c21

ORDER_READY_COLOR = 0xc54c21
ORDER_ACTIVATED_COLOR = 0x282d2f

ICON_OFFSET_PERCENT = 15
ORDER_ICON_RELATIVE_POS = (1, 1)

TRAVERSAL_COST = utils.distance.CIRCLE


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
        self.console_name_color = OPERATIVE_NAME_CONSOLE_COLOR

        # Game object init
        self.datacard = datacard
        self.render_group = pygame.sprite.RenderPlain()
        self.ruler: Ruler = Ruler()

        self.ghost_pos: Union[Tuple[int, int], None] = None
        self.range_radius: Union[utils.distance.Distance, None] = None

        # Properties
        self.apl_modifier = 0
        self.order = Order.CONCEAL
        self.action_points = 0
        self.carried_objective: Objective = None

        # Status
        self.deployed = False
        self.ready = False
        self.overwatched = False
        self.visible = False
        self.engagement_range_visible = False

        # Sprite init
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, 0, 0).inflate(
            self.datacard.physical_profile.base.to_screen_size(), self.datacard.physical_profile.base.to_screen_size())
        self.outline_color = None

        # Callback hooks
        self.on_activation_end: Callable[[Operative], None] = []
        self.on_incapacitated: Callable[[Operative], None] = []

        # Actions
        self.free_actions: List[str] = []  # Reference free actions by name
        self.actions_taken: List[Action] = []
        self.actions: List[Action] = []

        import action.universal
        self.actions.extend(action.universal.universal_actions)
        self.actions.extend(self.datacard.unique_actions)

        # Icons
        self.icon_size = (self.base_radius.to_screen_size(),
                          self.base_radius.to_screen_size())
        self.engage_icon_ready, _ = game.preload.image(game.icon.ENGAGE_ORDER,
                                                       colorkey=WHITE_COLORKEY,
                                                       color=ORDER_READY_COLOR,
                                                       scale_to=self.base_radius.to_screen_size())
        self.engage_icon_activated = game.preload.recolor(image=self.engage_icon_ready,
                                                          color=ORDER_ACTIVATED_COLOR)
        self.conceal_icon_ready, _ = game.preload.image(game.icon.CONCEAL_ORDER,
                                                        colorkey=WHITE_COLORKEY,
                                                        color=ORDER_READY_COLOR,
                                                        scale_to=self.base_radius.to_screen_size())
        self.conceal_icon_activated = game.preload.recolor(image=self.conceal_icon_ready,
                                                           color=ORDER_ACTIVATED_COLOR)

    def on_added_to_team(self):
        """Callback for when this operative is added to a team. Used to register team-based callbacks and properties
        """
        pass

    def on_deployed(self):
        self.deployed = True
        self.visible = True
        self.select_order()

    def ready_up(self):
        self.ready = True
        self.overwatched = False

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def highlight(self, color):
        self.outline_color = color

    def unhighlight(self):
        self.outline_color = None

    def show_engagement_range(self):
        self.engagement_range_visible = True

    def show_enemy_engagement_ranges(self):
        for team in self.team.gamestate.teams:
            if team == self.team:
                continue
            for operative in team.operatives:
                operative.show_engagement_range()

    def hide_engagement_range(self):
        self.engagement_range_visible = False

    def hide_enemy_engagement_ranges(self):
        for team in self.team.gamestate.teams:
            if team == self.team:
                continue
            for operative in team.operatives:
                operative.hide_engagement_range()

    def display_range(self, range: utils.distance.Distance):
        self.range_radius = range

    def hide_range(self):
        self.range_radius = None

    def deal_damage(self, num: int):
        self.wounds = self.wounds - num
        self.print(f"Suffered {num} wounds")
        self.datacard.update()

    def deal_mortal_wounds(self, num: int):
        self.deal_damage(num)

    @property
    def wounds(self):
        return self.datacard.current_wounds

    @wounds.setter
    def wounds(self, num: int):
        self.datacard.current_wounds = max(0, num)

    @property
    def injured(self):
        return self.wounds < self.datacard.physical_profile.wounds / 2

    @property
    def incapacitated(self):
        return self.wounds <= 0

    def remove_incapacitated(self):
        """Check if an operative is incapacitated and remove it if so.
        """
        if self.incapacitated:
            self.print(bold(with_color("Incapacited", 0xff0000)))

            # Call on incapacitated hooks
            for on_incapacitated in self.on_incapacitated:
                on_incapacitated(self)

            # Remove operative from team
            self.team.operatives.remove(self)
            self.team.incapacitated_operatives.append(self)

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

    @property
    def oneline_description(self):
        if self.incapacitated:
            return f"{self.console_name}: INCAPACITATED"

        injured_text = "(INJURED) " if self.injured else ""
        apl_text = f"APL{self.apl_modifier} " if self.apl_modifier != 0 else ""
        return f"{self.console_name}: W{self.wounds} {injured_text}{apl_text}"

    @property
    def console_name(self):
        return tag(self.datacard.operative_type, color=self.console_name_color)

    def print(self, msg: str):
        print(self.console_name + " " + str(msg))

    @property
    def base_radius(self):
        return self.datacard.physical_profile.base / 2

    def display_icon(self, icon: pygame.Surface, relative_pos: Tuple[int, int]):
        pygame.display.get_surface().blit(icon,
                                          (self.rect.center[0] - self.icon_size[0] / 2 + (self.base_radius.to_screen_size() * (1 + ICON_OFFSET_PERCENT / 100.0)) * relative_pos[0],
                                           self.rect.center[1] - self.icon_size[1] / 2 + (self.base_radius.to_screen_size() * (1 + ICON_OFFSET_PERCENT / 100.0)) * relative_pos[1]))

    def show_datacard(self):
        self.datacard.show()

    @utils.decorator.on_hover(show_datacard)
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

        if self.engagement_range_visible:
            pygame.draw.circle(screen, ENGAGEMENT_RANGE_COLOR, self.rect.center, self.rect.width /
                               2 + utils.distance.ENGAGEMENT_RANGE.to_screen_size(), ENGAGEMENT_RANGE_OUTLINE_WIDTH)

        if self.range_radius:
            pygame.draw.circle(screen, WEAPON_RANGE_COLOR, self.rect.center, self.range_radius.to_screen_size(
            ) + self.datacard.physical_profile.base.to_screen_size() / 2, WEAPON_RANGE_OUTLINE_WIDTH)

        # TODO: Injured icon

        if self.ready:
            if self.order == Order.ENGAGE:
                self.display_icon(icon=self.engage_icon_ready,
                                  relative_pos=ORDER_ICON_RELATIVE_POS)
            else:
                self.display_icon(icon=self.conceal_icon_ready,
                                  relative_pos=ORDER_ICON_RELATIVE_POS)
        else:
            if self.order == Order.ENGAGE:
                self.display_icon(icon=self.engage_icon_activated,
                                  relative_pos=ORDER_ICON_RELATIVE_POS)
            else:
                self.display_icon(icon=self.conceal_icon_activated,
                                  relative_pos=ORDER_ICON_RELATIVE_POS)

        self.render_group.draw(screen)
        if self.ghost_pos != None:
            pygame.draw.circle(screen, self.color, self.ghost_pos,
                               self.rect.width/2, self.outline_width)
        self.ruler.redraw()

    @property
    def carrying_objective(self):
        return self.carried_objective != None

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

    @property
    def bs_ws_modifier(self):
        overwatch_modifier = -1 if self.overwatched else 0
        injured_modifier = -1 if self.injured else 0

        return overwatch_modifier + injured_modifier

    def combat_support_against(self, defender):
        from operatives import Operative
        defender: Operative = defender

        combat_support = 0
        for ally in self.team.operatives:
            if ally == self:
                continue

            engaged_with = ally.enemies_within_engagement_range()
            if (len(engaged_with) == 1) and (defender in engaged_with):
                combat_support += 1

        return combat_support

    @property
    def movement_characteristic(self):
        movement_modifier = utils.distance.CIRCLE if self.injured else 0
        return self.datacard.physical_profile.movement - movement_modifier

    def activate(self, activation_num: int = 1):
        # Select engage/conceal order
        if self.team.gamestate.current_turn != 1:
            self.select_order()

        self.actions_taken = []
        self.action_points = self.datacard.physical_profile.action_point_limit + self.apl_modifier
        # While the operative has action points remaining, perform actions
        while self.action_points > -1:
            valid_actions = {
                a.description: a for a in self.actions if a.cost(self.free_actions) <= self.action_points and a.valid_this_turn(a, self)}
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
        self.apl_modifier = 0
        self.ready = False
        self.free_actions = []

        for on_activation_end in self.on_activation_end:
            on_activation_end(self)

        # If group activated, find another unit to activate
        while activation_num < self.datacard.physical_profile.group_activation:
            # Find another operative of the same type to group activate
            ready_operatives: list[Operative] = [op for op in self.team.operatives if (
                op.ready and op.datacard.operative_type == self.datacard.operative_type)]

            if len(ready_operatives) <= 0:
                # No more operatives left to group activate
                break

            # Get operative selection, highlight ready operatives
            for op in ready_operatives:
                op.highlight(self.team.ready_operative_highlight_color)
            for click_loc in utils.player_input.wait_for_click():
                if click_loc != None:
                    ga_operative = utils.collision.get_selected_sprite(
                        click_loc, ready_operatives)
                    if ga_operative != None:
                        break
                self.team.gamestate.redraw()
            [op.unhighlight() for op in ready_operatives]
            self.team.gamestate.redraw()

            # Activate operative
            activation_num += 1
            ga_operative.activate(activation_num=activation_num)

        ### End Operative.activate ###

    def overwatch(self):
        self.overwatched = True
        return self.perform_shoot()

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

    def register_on_incapacitated(self, cb):
        self.on_incapacitated.append(cb)

    def enemies_within_engagement_range(self, point: Tuple[int, int] = None):
        within_engagement_range = []
        for enemy_team in [team for team in self.team.gamestate.teams if team != self.team]:
            for op in enemy_team.operatives:
                if utils.distance.between(self.rect.center if point == None else point, op.rect.center) < utils.distance.TRIANGLE + self.base_radius + op.base_radius and \
                        utils.line_of_sight.visible(source=self, target=op):
                    within_engagement_range.append(op)

        return within_engagement_range

    def get_objective_in_capture_range(self):
        for o in self.team.gamestate.gameboard.objectives:
            if utils.distance.between(self.rect.center, o.rect.center) < self.base_radius + o.capture_range:
                return o

        # No objectives in range
        return None

    # Move Action

    def traversal_cost_to(self,
                          location: Tuple[int, int]):
        cost = utils.distance.Distance(0)
        if self.datacard.physical_profile.flying:
            # Flying units can ignore vertical distances, meaning they do not need to traverse terrain
            return cost

        for feature in self.team.gamestate.gameboard.features_with_trait(TerrainTrait.LIGHT) + self.team.gamestate.gameboard.features_with_trait(TerrainTrait.HEAVY):
            if feature.rect.clipline(self.rect.center, location):
                cost += TRAVERSAL_COST if feature.traversable else utils.distance.INFINITE

        return cost

    def valid_move_location(self,
                            location: Tuple[int, int],
                            falling_back: bool = False,
                            charging: bool = False):

        # Check that operative can be placed at final destination (not overlapping other operatives' base)
        for team in self.team.gamestate.teams:
            for operative in team.operatives:
                if operative == self:
                    continue
                if utils.distance.between(location, operative.rect.center) < self.base_radius + operative.base_radius:
                    return False

        # Cannot move over the edge of the killzone
        if not self.team.gamestate.gameboard.rect.collidepoint(location):
            return False

        # Cannot move through another unit (which is a subset of checking the engagement range)
        # NOTE: (Needs clarification) Flying operatives can ignore engagement ranges while moving
        # FIXME: If charging, cannot move through engagement range of other units unless another friendly operative is currently engaged with it
        if not self.datacard.physical_profile.flying:
            for team in self.team.gamestate.teams:
                for operative in team.operatives:
                    if operative == self:
                        continue

                    # No need to check against operatives we cannot see
                    if not utils.line_of_sight.visible(source=self, target=operative):
                        continue

                    distance = utils.distance.between_line_and_point(
                        self.ruler.source, self.ruler.destination, operative.rect.center)

                    # If charging or falling back, only check for overlapping bases
                    # Same if the unit is friendly
                    if charging or falling_back or team == self.team:
                        if distance < self.base_radius + operative.base_radius:
                            return False
                    elif distance < self.base_radius + operative.base_radius + utils.distance.ENGAGEMENT_RANGE:
                        return False

        # TODO: Ignore this rule if we're ontop of a vantage point (only check features that are TALL)
        # Cannot end move on top of terrain
        for feature in self.team.gamestate.gameboard.features_with_trait(TerrainTrait.LIGHT) + self.team.gamestate.gameboard.features_with_trait(TerrainTrait.HEAVY):
            if utils.collision.circle_rect_collide(circle=self.ruler.destination,
                                                   radius=self.base_radius,
                                                   rect=feature.rect):
                return False

        return True

    def perform_move(self,
                     distance: utils.distance.Distance,
                     falling_back: bool = False,
                     charging: bool = False):
        self.print("Moving up to " + distance.to_console_format())

        # Save current position in case we want to cancel move
        starting_pos = self.rect.center
        successful_move = True

        # Display engagement ranges of enemy operatives
        self.show_enemy_engagement_ranges()
        # Show objective capture ranges
        if not charging:
            self.team.gamestate.gameboard.show_objective_ranges()
        self.team.gamestate.gameboard.show_terrain_outlines()

        # Create a new Distance object to prevent us from accidentally changing the reference we're given
        remaining_movement = utils.distance.Distance(distance)
        while remaining_movement > 0:
            for click_loc in utils.player_input.wait_for_click():
                # Listen for ESCAPE and RETURN keys
                if utils.player_input.key_pressed(pygame.K_ESCAPE):
                    remaining_movement = -1
                    successful_move = False
                    break
                if utils.player_input.key_pressed(pygame.K_RETURN):
                    remaining_movement = -1
                    break

                mouse_pos = utils.player_input.mouse_pos()
                self.ruler.measure(
                    from_=self.rect.center,
                    towards=mouse_pos,
                    max_length=remaining_movement,
                )

                # Update the length of the ruler to factor in cost of traversals
                traversal_cost = self.traversal_cost_to(self.ruler.destination)
                can_traverse = traversal_cost <= remaining_movement
                self.ruler.measure_and_show(
                    from_=self.rect.center,
                    towards=mouse_pos,
                    max_length=remaining_movement -
                    traversal_cost if can_traverse else remaining_movement,
                )

                move_is_valid = can_traverse and self.valid_move_location(
                    self.ruler.destination, falling_back, charging)
                # If we receive a click, check that the location is valid for movement
                if click_loc != None and move_is_valid:
                    break

                self.ruler.color = VALID_MOVE_RULER_COLOR if move_is_valid else INVALID_MOVE_RULER_COLOR
                self.ghost_pos = self.ruler.destination  # Show ghost at target dest
                self.team.gamestate.redraw()

            if remaining_movement < 0:
                break

            # Move operative to end of the ruler's measured distance
            self.move_to(self.ruler.destination)
            self.team.gamestate.redraw()
            remaining_movement -= self.ruler.length.round_up(
                increment=utils.distance.TRIANGLE) + traversal_cost

        # Hide engagement ranges of enemy operatives
        self.hide_enemy_engagement_ranges()
        # Hide objective capture ranges and terrain outlines
        self.team.gamestate.gameboard.hide_objective_ranges()
        self.team.gamestate.gameboard.hide_terrain_outlines()

        # If charging, must finish move within engagement range of enemy unit
        num_enemies_within_engagement_range = len(
            self.enemies_within_engagement_range())
        if charging:
            if num_enemies_within_engagement_range <= 0:
                successful_move = False
        # Otherwise, cannot end move within engagement range of enemy operative
        elif num_enemies_within_engagement_range > 0:
            successful_move = False

        self.ghost_pos = None
        self.ruler.hide()
        if successful_move == False:
            self.move_to(starting_pos)
        self.team.gamestate.redraw()

        return successful_move

    # Shoot Action

    def select_ranged_weapon(self):
        ranged_weapons = {
            weapon.description: weapon for weapon in self.datacard.ranged_weapon_profiles}
        for selection in utils.player_input.select_from_list(relative_to=self.rect.center,
                                                             items=ranged_weapons.keys()):
            if selection != None:
                return ranged_weapons.get(selection)
            self.team.gamestate.redraw()

    def in_line_of_sight(self, op):
        from operatives import Operative
        enemy: Operative = op

        # An operative is in Line of Sight if it is:

        # 1. Visible
        if not utils.line_of_sight.visible(source=self, target=enemy):
            return False

        # 2. Not Obscured
        if utils.line_of_sight.obscured(source=self, target=enemy):
            return False

        # 3. Not in Cover (if it is concealed)
        if enemy.order == Order.CONCEAL and utils.line_of_sight.in_cover(source=self, target=enemy):
            return False

        return True

    def get_valid_targets(self, weapon: Weapon):
        valid_targets = []
        for team in self.team.gamestate.teams:
            if team == self.team:
                continue
            for operative in team.operatives:
                # Check weapon's range, if it has one
                if weapon.range and utils.distance.between(self.rect.center, operative.rect.center) > \
                        weapon.range + self.base_radius + operative.base_radius:
                    continue

                # Enemy is valid target if it is within Line of Sight
                # and has no friendly operatives within engagement range
                if self.in_line_of_sight(operative):
                    valid = True
                    enemy_engaged_with = operative.enemies_within_engagement_range()
                    for friendly in self.team.operatives:
                        if friendly in enemy_engaged_with:
                            valid = False
                            break
                    if valid:
                        valid_targets.append(operative)

        return valid_targets

    def perform_shoot(self):
        # Select ranged weapon
        if len(self.datacard.ranged_weapon_profiles) <= 0:
            return False  # Nothing to shoot with
        selected_weapon = self.select_ranged_weapon()

        # Select valid target
        valid_targets = self.get_valid_targets(selected_weapon)
        if len(valid_targets) <= 0:
            return False  # No valid targets

        self.display_range(selected_weapon.range)
        [op.highlight(VALID_TARGET_HIGHLIGHT_COLOR) for op in valid_targets]
        for click_loc in utils.player_input.wait_for_click():
            # Cancel action with ESCAPE
            if utils.player_input.key_pressed(pygame.K_ESCAPE):
                defender = None
                break

            if click_loc != None:
                defender = utils.collision.get_selected_sprite(
                    click_loc, valid_targets)
                if defender != None:
                    break
            self.team.gamestate.redraw()
        [op.unhighlight() for op in valid_targets]
        self.hide_range()
        self.team.gamestate.redraw()

        # If no target was selected, cancel shooting action
        if defender == None:
            return False
        self.print("Shooting " + defender.console_name)

        # Perform shoot action
        successful_shooting = selected_weapon.shoot(
            attacker=self,
            defender=defender,
        )

        return successful_shooting

    # Fight Action

    def get_valid_fight_targets(self):
        return self.enemies_within_engagement_range()

    def select_melee_weapon(self):
        melee_weapons = {
            weapon.description: weapon for weapon in self.datacard.melee_weapon_profiles}
        if len(melee_weapons) <= 0:
            return None

        for selection in utils.player_input.select_from_list(relative_to=self.rect.center,
                                                             items=melee_weapons.keys()):
            if selection != None:
                return melee_weapons.get(selection)
            self.team.gamestate.redraw()

    def perform_fight(self):
        # Select valid target
        valid_targets = self.get_valid_fight_targets()
        if len(valid_targets) <= 0:
            return False  # No valid fight targets

        self.show_engagement_range()
        [op.highlight(VALID_TARGET_HIGHLIGHT_COLOR) for op in valid_targets]
        for click_loc in utils.player_input.wait_for_click():
            # Cancel action with ESCAPE
            if utils.player_input.key_pressed(pygame.K_ESCAPE):
                defender = None
                break

            if click_loc != None:
                defender = utils.collision.get_selected_sprite(
                    click_loc, valid_targets)
                if defender != None:
                    break
            self.team.gamestate.redraw()
        [op.unhighlight() for op in valid_targets]
        self.hide_engagement_range()
        self.team.gamestate.redraw()

        # If no target was selected, cancel fighting action
        if defender == None:
            return False
        self.print("Fighting " + defender.console_name)

        # Select melee weapons (both players)
        if len(self.datacard.melee_weapon_profiles) <= 0:
            return False  # Nothing to fight with
        selected_weapon = self.select_melee_weapon()
        defender_selected_weapon = defender.select_melee_weapon()

        # Perform fight action
        return selected_weapon.fight(
            attacker=self,
            defender=defender,
            defender_weapon=defender_selected_weapon,
        )
