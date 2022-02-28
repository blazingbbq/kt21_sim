from abc import ABC
from enum import Enum
from tokenize import Special
from typing import List, Tuple, Union
import utils.dice
import utils.distance
import game.ui
import game.state
import pygame
import game.console

NORMAL_DICE_SYMBOL = "·"
CRIT_DICE_SYMBOL = "!"


class SpecialRule(Enum):
    AP_1 = 1
    AP_2 = 2
    # 3-6 reserved for higher AP rules
    BARRAGE = 3  # TODO: Implement
    BALANCED = 4  # TODO: Implement
    BLAST_2 = 5  # TODO: Implement
    # 6-7 reserved for higher blast radiuses
    BRUTAL = 8  # TODO: Implement
    CEASELESS = 9
    FUSILLADE = 10  # TODO: Implement
    HEAVY = 11  # TODO: Implement
    HOT = 12
    INDIRECT = 13  # TODO: Implement
    INVULNERABLE_SAVE_2 = 14  # TODO: Implement
    INVULNERABLE_SAVE_3 = 15  # TODO: Implement
    INVULNERABLE_SAVE_4 = 16  # TODO: Implement
    INVULNERABLE_SAVE_5 = 17  # TODO: Implement
    INVULNERABLE_SAVE_6 = 18  # TODO: Implement
    # 19-21 reserved for higher lethal rules
    LETHAL_5 = 22
    LIMITED = 23  # TODO: Implement
    MW_1 = 24
    MW_2 = 25
    MW_3 = 26
    MW_4 = 27
    # 28-29 reserved for higher MW rules
    NO_COVER = 30  # TODO: Implement
    P_1 = 31  # TODO: Implement
    P_2 = 32  # TODO: Implement
    # 33-36 reserved for higher piercing rules
    REAP_1 = 37  # TODO: Implement
    # 38-39 reserved for higher reap rules
    RELENTLESS = 40  # TODO: Implement
    RENDING = 41
    # 42-43 reserved for shorter range rules
    RNG_6 = 44
    # 45-46 reserved for longer range rules
    SILENT = 47  # TODO: Implement
    SPLASH_1 = 48  # TODO: Implement
    # 49-50 reserved for higher splash rules
    STUN = 51
    TORRENT_2 = 52  # TODO: Implement
    # 53-54 reserved for higher torrent rules
    UNWIELDY = 53  # TODO: Implement


class Weapon(ABC):
    def __init__(self,
                 name: str,
                 attacks: int,
                 skill: int,  # Either BallisticSkill / WeaponSkill
                 damage: Tuple[int, int],  # Damage tuple: (Normal, Crit)
                 special_rules: List[SpecialRule] = [],
                 critical_hit_rules: List[SpecialRule] = [],
                 ):
        self.name = name
        self.attacks = attacks
        self.skill = skill
        self.damage = damage
        self.special_rules = special_rules
        self.critical_hit_rules = critical_hit_rules

        self.crit_on = 6
        if SpecialRule.LETHAL_5 in self.special_rules:
            self.crit_on = 5

    @property
    def description(self):
        return f"{self.name} (A: {self.attacks}, BS/WS: {self.skill}+, D: {self.damage[0]}/{self.damage[1]})"

    @property
    def range(self):
        if SpecialRule.RNG_6 in self.special_rules:
            return utils.distance.from_pentagon(1)
        return None

    @property
    def ap_modifier(self):
        if SpecialRule.AP_1 in self.special_rules:
            return -1
        if SpecialRule.AP_2 in self.special_rules:
            return -2
        return 0

    @property
    def normal_damage(self):
        return self.damage[0]

    @property
    def critical_damage(self):
        return self.damage[1]

    @property
    def mw(self):
        if SpecialRule.MW_1 in self.critical_hit_rules:
            return 1
        if SpecialRule.MW_2 in self.critical_hit_rules:
            return 2
        if SpecialRule.MW_3 in self.critical_hit_rules:
            return 3
        if SpecialRule.MW_4 in self.critical_hit_rules:
            return 4

        return 0

    def handle_special_rules(self, rolls: utils.dice.Dice, attacker, defender, fighting: bool = False, overwatching: bool = False):
        from operatives import Operative
        attacker: Operative = attacker
        defender: Operative = defender

        # Sort normal and critical hits
        normal_hits, critical_hits, failed_hits = self.sort_roll_results(rolls=rolls,
                                                                         attacker=attacker,
                                                                         defender=defender,
                                                                         fighting=fighting,
                                                                         overwatching=overwatching)

        # Dice reroll rules
        # TODO: Rerolls from abilities or team mechanics
        if SpecialRule.CEASELESS in self.special_rules:
            for roll in failed_hits:
                roll.reroll_eq(1)

        # Resort hits
        normal_hits, critical_hits, failed_hits = self.sort_roll_results(rolls=normal_hits + critical_hits + failed_hits,
                                                                         attacker=attacker,
                                                                         defender=defender,
                                                                         fighting=fighting,
                                                                         overwatching=overwatching)

        # Critical hit rules
        if len(critical_hits) > 0:

            if SpecialRule.RENDING in self.critical_hit_rules:
                if len(normal_hits) > 0:
                    game.console.debug("Rending")
                    normal_hits.pop()
                    critical_hits.append(utils.dice.Dice(6))

            mw = self.mw
            if mw:
                defender.deal_mortal_wounds(mw * len(critical_hits))

            # Stun is handled differently for shooting vs. fighting
            if SpecialRule.STUN in self.critical_hit_rules and not fighting:
                defender.apl_modifier -= 1

        # Additional hit rules (Blast, Reap, etc.)

        return normal_hits + critical_hits + failed_hits

    # Shooting

    def discard_attack_dice(self, roll: utils.dice.Dice, attacker):
        from operatives import Operative
        attacker: Operative = attacker

        if SpecialRule.HOT in self.special_rules:
            attacker.deal_mortal_wounds(3)

    def sort_roll_results(self, rolls, attacker, defender, fighting: bool = False, overwatching: bool = False):
        from operatives import Operative
        attacker: Operative = attacker
        defender: Operative = defender

        combat_support = attacker.combat_support_against(
            defender) if fighting else 0
        overwatch_modifier = attacker.overwatch_modifier if overwatching else 0

        normal_hits, critical_hits, failed_hits = [], [], []
        for roll in rolls:
            # Result of 1 is always a failed hit, else check BS
            # Result of 6 is always a successful hit
            if (roll == 1 or roll < self.skill + attacker.bs_ws_modifier + overwatch_modifier + combat_support) and roll != 6:
                failed_hits.append(roll)
                continue

            # Successful hit
            if roll >= self.crit_on:
                critical_hits.append(roll)
                continue
            normal_hits.append(roll)

        return normal_hits, critical_hits, failed_hits

    def roll_attack_dice(self, attacker, defender, fighting: bool = False, overwatching: bool = False) -> Tuple[List[utils.dice.Dice], List[utils.dice.Dice]]:
        rolls = [utils.dice.roll() for _ in range(self.attacks)]

        # Handle special rules
        rolls = self.handle_special_rules(rolls=rolls,
                                          attacker=attacker,
                                          defender=defender,
                                          fighting=fighting,
                                          overwatching=overwatching)

        # Sort normal and critical hits
        normal_hits, critical_hits, failed_hits = self.sort_roll_results(rolls=rolls,
                                                                         attacker=attacker,
                                                                         defender=defender,
                                                                         fighting=fighting,
                                                                         overwatching=overwatching)

        # Discard failed rolls
        for roll in failed_hits:
            self.discard_attack_dice(roll, attacker)

        return normal_hits, critical_hits

    def roll_defence_dice(self, attacker, defender) -> Tuple[List[utils.dice.Dice], List[utils.dice.Dice]]:
        from operatives import Operative
        attacker: Operative = attacker
        defender: Operative = defender
        normal_saves, critical_saves = [], []

        # Can retain 1 successful normal save if in cover
        retain_cover_dice = False
        # TODO: Include a Barrage option to in_cover util
        if utils.line_of_sight.in_cover(source=attacker, target=defender):
            retain_cover_dice = utils.player_input.prompt_true_false(
                msg=f"Retain one dice as a successful normal save?")
            normal_saves.append(utils.dice.Dice(5))

        cover_modifier = -1 if retain_cover_dice else 0
        rolls = [utils.dice.roll() for _ in range(
            defender.datacard.physical_profile.defence + self.ap_modifier + cover_modifier)]

        # TODO: Prompt rerolls from abilities or team mechanics

        # Sort normal and crit saves
        for roll in rolls:
            # Result of 1 is always a failed save, else check defender's Save
            if roll == 1 or roll < attacker.datacard.physical_profile.save:
                continue

            # Successful save
            if roll >= 6:
                critical_saves.append(roll)
                continue
            normal_saves.append(roll)

        return normal_saves, critical_saves

    def resolve_save_dice(self,
                          attack_dice: Tuple[List[utils.dice.Dice], List[utils.dice.Dice]],
                          defence_dice: Tuple[List[utils.dice.Dice], List[utils.dice.Dice]]) -> Tuple[List[utils.dice.Dice], List[utils.dice.Dice]]:
        text_height = 20
        element_padding = 5

        # Panel
        panel_rect = pygame.rect.Rect((0, 0), (400, 250))
        panel_rect.center = game.ui.layout.window.center
        panel = game.ui.elements.UIPanel(
            relative_rect=panel_rect,
            manager=game.ui.manager,
            starting_layer_height=0,
            container=game.ui.layout.window_container,
            margins=game.ui.layout.default_margins,
        )

        panel_inner_rect = pygame.rect.Rect(
            0, 0, panel_rect.width - panel.container_margins['left'] - panel.container_margins['right'], panel_rect.height - panel.container_margins['top'] - panel.container_margins['bottom'])
        # Top label
        label = game.ui.elements.UILabel(
            relative_rect=pygame.rect.Rect(
                0, 0, panel_rect.width, text_height),
            text="Resolve Successful Saves",
            container=panel,
            manager=game.ui.manager,
        )
        # Confirmation button
        done_button = game.ui.elements.UIButton(
            relative_rect=pygame.Rect(panel_inner_rect.width / 2, panel_inner_rect.bottom -
                                      text_height, panel_inner_rect.width / 2, text_height),
            text="Done",
            starting_height=1,
            container=panel,
            manager=game.ui.manager,
            visible=True,
        )
        # Dice lists
        defence_label = game.ui.elements.UILabel(
            relative_rect=pygame.rect.Rect(
                0, text_height + element_padding, panel_inner_rect.width / 2, text_height),
            text="Defence Dice",
            container=panel,
            manager=game.ui.manager,
        )
        attack_label = game.ui.elements.UILabel(
            relative_rect=pygame.rect.Rect(
                panel_inner_rect.width / 2, text_height + element_padding, panel_inner_rect.width / 2, text_height),
            text="Attack Dice",
            container=panel,
            manager=game.ui.manager,
        )
        list_height = panel_inner_rect.height - 3 * text_height - 3 * element_padding
        defence_dice_selection = game.ui.elements.UISelectionList(
            relative_rect=pygame.Rect(
                0, 2 * text_height + 2 * element_padding, panel_inner_rect.width / 2, list_height),
            item_list=[f"{CRIT_DICE_SYMBOL} {dice.value}" for dice in defence_dice[1]
                       ] + [f"{NORMAL_DICE_SYMBOL} {dice.value}" for dice in defence_dice[0]],
            allow_multi_select=True,
            container=panel,
            manager=game.ui.manager)
        attack_dice_selection = game.ui.elements.UISelectionList(
            relative_rect=pygame.Rect(panel_inner_rect.width / 2, 2 * text_height +
                                      2 * element_padding, panel_inner_rect.width / 2, list_height),
            item_list=[f"{CRIT_DICE_SYMBOL} {dice.value}" for dice in attack_dice[1]
                       ] + [f"{NORMAL_DICE_SYMBOL} {dice.value}" for dice in attack_dice[0]],
            allow_multi_select=True,
            container=panel,
            manager=game.ui.manager)

        # Wait for user to confirm selection
        while True:
            d_selections = defence_dice_selection.get_multi_selection()
            a_selections = attack_dice_selection.get_multi_selection()

            # Count selections
            norm_hits = sum(
                1 for a in a_selections if a.startswith(NORMAL_DICE_SYMBOL))
            crit_hits = sum(
                1 for a in a_selections if a.startswith(CRIT_DICE_SYMBOL))
            norm_saves = sum(
                1 for d in d_selections if d.startswith(NORMAL_DICE_SYMBOL))
            crit_saves = sum(
                1 for d in d_selections if d.startswith(CRIT_DICE_SYMBOL))

            # 1 crit save -> 1 crit hit or 1 norm hit
            # 1 norm save -> 1 norm hit
            # 2 norm save -> 1 crit hit
            if (crit_saves == 1 and (crit_hits == 1 or norm_hits == 1)) or \
                    (norm_saves == 1 and norm_hits == 1) or \
                    (norm_saves == 2 and crit_hits == 1):
                defence_dice_selection._raw_item_list.remove(d_selections[0])
                if norm_saves == 2:
                    defence_dice_selection._raw_item_list.remove(
                        d_selections[1])
                attack_dice_selection._raw_item_list.remove(a_selections[0])

                defence_dice_selection.set_item_list(
                    defence_dice_selection._raw_item_list)
                attack_dice_selection.set_item_list(
                    attack_dice_selection._raw_item_list)

            # Selection complete, return
            if done_button.check_pressed():
                remaining_norm_hits = sum(1 for a in attack_dice_selection._raw_item_list if a.startswith(
                    NORMAL_DICE_SYMBOL))
                remaining_crit_hits = sum(
                    1 for a in attack_dice_selection._raw_item_list if a.startswith(CRIT_DICE_SYMBOL))

                game.ui.remove(panel)
                game.state.redraw()
                return remaining_norm_hits, remaining_crit_hits

            game.state.redraw()

    def shoot(self, attacker, defender, overwatching=False):
        from operatives import Operative
        attacker: Operative = attacker
        defender: Operative = defender

        # Roll attack dice
        attack_dice = self.roll_attack_dice(
            attacker=attacker,
            defender=defender,
            overwatching=overwatching,
        )

        # Roll defence dice
        defence_dice = self.roll_defence_dice(
            attacker=attacker,
            defender=defender,
        )

        # Resolve successful saves
        remaining_normal_hits, remaining_crit_hits = self.resolve_save_dice(attack_dice=attack_dice,
                                                                            defence_dice=defence_dice)

        # Resolve successful hits
        defender.deal_damage(remaining_normal_hits * self.normal_damage +
                             remaining_crit_hits * self.critical_damage)

        # Remove incapacitated operatives
        attacker.remove_incapacitated()
        defender.remove_incapacitated()

        return True

    # Fighting

    def resolve_fight_attacks(self,
                              attacker,
                              defender,
                              defender_weapon,
                              attacker_dice: Tuple[List[utils.dice.Dice], List[utils.dice.Dice]],
                              defender_dice: Tuple[List[utils.dice.Dice], List[utils.dice.Dice]]):
        from operatives import Operative
        attacker: Operative = attacker
        defender: Operative = defender
        from weapons import Weapon
        defender_weapon: Weapon = defender_weapon

        text_height = 20
        button_height = 24
        element_padding = 5

        # Panel
        panel_rect = pygame.rect.Rect((0, 0), (400, 250))
        panel_rect.center = game.ui.layout.window.center
        panel = game.ui.elements.UIPanel(
            relative_rect=panel_rect,
            manager=game.ui.manager,
            starting_layer_height=0,
            container=game.ui.layout.window_container,
            margins=game.ui.layout.default_margins,
        )

        panel_inner_rect = pygame.rect.Rect(
            0, 0, panel_rect.width - panel.container_margins['left'] - panel.container_margins['right'], panel_rect.height - panel.container_margins['top'] - panel.container_margins['bottom'])
        # Top label
        label = game.ui.elements.UILabel(
            relative_rect=pygame.rect.Rect(
                0, 0, panel_rect.width, text_height),
            text="Resolve Successful Hits",
            container=panel,
            manager=game.ui.manager,
        )
        # Parry and Strike buttons
        parry_button = game.ui.elements.UIButton(
            relative_rect=pygame.Rect(
                0, panel_inner_rect.bottom - button_height, panel_inner_rect.width / 2, button_height),
            text="Parry",
            starting_height=1,
            container=panel,
            manager=game.ui.manager,
            visible=True,
        )
        strike_button = game.ui.elements.UIButton(
            relative_rect=pygame.Rect(panel_inner_rect.width / 2, panel_inner_rect.bottom -
                                      button_height, panel_inner_rect.width / 2, button_height),
            text="Strike",
            starting_height=1,
            container=panel,
            manager=game.ui.manager,
            visible=True,
        )

        # Dice lists
        defence_label = game.ui.elements.UILabel(
            relative_rect=pygame.rect.Rect(
                panel_inner_rect.width / 2, text_height + element_padding, panel_inner_rect.width / 2, text_height),
            text="Defender's Dice",
            container=panel,
            manager=game.ui.manager,
        )
        attack_label = game.ui.elements.UILabel(
            relative_rect=pygame.rect.Rect(
                0, text_height + element_padding, panel_inner_rect.width / 2, text_height),
            text="Attacker's Dice",
            container=panel,
            manager=game.ui.manager,
        )
        list_height = panel_inner_rect.height - 2 * \
            text_height - button_height - 3 * element_padding
        defender_dice_selection = game.ui.elements.UISelectionList(
            relative_rect=pygame.Rect(panel_inner_rect.width / 2, 2 * text_height +
                                      2 * element_padding, panel_inner_rect.width / 2, list_height),
            item_list=[f"{CRIT_DICE_SYMBOL} {dice.value}" for dice in defender_dice[1]
                       ] + [f"{NORMAL_DICE_SYMBOL} {dice.value}" for dice in defender_dice[0]],
            allow_multi_select=False,
            container=panel,
            manager=game.ui.manager)
        attacker_dice_selection = game.ui.elements.UISelectionList(
            relative_rect=pygame.Rect(
                0, 2 * text_height + 2 * element_padding, panel_inner_rect.width / 2, list_height),
            item_list=[f"{CRIT_DICE_SYMBOL} {dice.value}" for dice in attacker_dice[1]
                       ] + [f"{NORMAL_DICE_SYMBOL} {dice.value}" for dice in attacker_dice[0]],
            allow_multi_select=False,
            container=panel,
            manager=game.ui.manager)

        # Repeat until one operative is incapacitated
        resolve_for = None
        stun_count = {
            attacker: 0,
            defender: 0,
        }
        while not attacker.incapacitated and not defender.incapacitated:
            # Starting with the attacker, each player alternates resolving one of their successful hits.
            resolve_for = attacker if resolve_for != attacker else defender

            # Setup for next resolution
            if resolve_for == attacker:
                receiver = defender
                resolving_weapon = self

                resolver_dice_list = attacker_dice_selection
                other_dice_list = defender_dice_selection
            else:
                receiver = attacker
                resolving_weapon = defender_weapon

                resolver_dice_list = defender_dice_selection
                other_dice_list = attacker_dice_selection

            # Check number of remaining resolvable dice
            if len(resolver_dice_list._raw_item_list) <= 0:
                if len(other_dice_list._raw_item_list) <= 0:
                    # No dice left for either, all done
                    break
                # No dice left for resolver, skip
                continue

            resolver_dice_list.disable()
            other_dice_list.disable()
            parry_button.disable()
            strike_button.disable()

            # To resolve a successful hit, they select one of their retained attack dice,
            # choose for their operative to strike or parry, then discard that attack dice.
            while True:
                resolver_dice_list.enable()
                dice_selection = resolver_dice_list.get_single_selection()
                # Enable resolution buttons once a selection is made
                if dice_selection != None:
                    parry_button.enable()
                    strike_button.enable()

                if strike_button.check_pressed() and dice_selection != None:
                    striking = True
                    break
                if parry_button.check_pressed() and dice_selection != None:
                    striking = False
                    parry_button.disable()
                    break

                # Can use RETURN to automatically use the highest dice as a strike
                if utils.player_input.key_pressed(pygame.K_RETURN):
                    dice_selection = resolver_dice_list._raw_item_list[0]
                    striking = True
                    break

                game.state.redraw()

            resolver_dice_list.disable()

            critical_hit = dice_selection.startswith(CRIT_DICE_SYMBOL)
            # If they parry, one of their opponent’s successful hits is discarded
            while not striking:
                other_dice_list.enable()

                # Ensure that parry is possible
                if len(other_dice_list._raw_item_list) <= 0:
                    # Nothing to parry
                    break

                if strike_button.check_pressed():
                    # Switch attack dice to strike
                    striking = True
                    break

                # Select dice to parry
                selection = other_dice_list.get_single_selection()
                if selection != None:
                    if critical_hit:
                        # If the attack dice they select is a critical hit, they select one of their opponent’s normal hits or critical hits to be discarded.
                        other_dice_list._raw_item_list.remove(selection)
                        other_dice_list.set_item_list(
                            other_dice_list._raw_item_list)
                        break
                    elif selection.startswith(NORMAL_DICE_SYMBOL):
                        # If the attack dice they select is a normal hit, they select one of their opponent’s normal hits to be discarded.
                        other_dice_list._raw_item_list.remove(selection)
                        other_dice_list.set_item_list(
                            other_dice_list._raw_item_list)
                        break

                game.state.redraw()
            other_dice_list.disable()

            # If they strike, inflict damage on the target.
            if striking:
                if critical_hit:
                    # If the attack dice they select is a critical hit, inflict damage equal to their selected weapon’s Critical Damage.
                    receiver.deal_damage(resolving_weapon.critical_damage)

                    # Handle Stun rule
                    if SpecialRule.STUN in resolving_weapon.critical_hit_rules:
                        if stun_count[resolve_for] == 0:
                            # First stun removes a normal hit from the opponent
                            normal_hit = next((hit for hit in other_dice_list._raw_item_list if hit.startswith(
                                NORMAL_DICE_SYMBOL)), None)
                            if normal_hit != None:
                                other_dice_list.enable()
                                other_dice_list._raw_item_list.remove(
                                    normal_hit)
                                other_dice_list.set_item_list(
                                    other_dice_list._raw_item_list)
                            other_dice_list.disable()
                        elif stun_count[resolve_for] == 1:
                            # Second stun reduces target's APL by 1
                            receiver.apl_modifier -= 1
                        stun_count[resolve_for] += 1
                else:
                    # If the attack dice they select is a normal hit, inflict damage equal to their selected weapon’s Normal Damage.
                    receiver.deal_damage(resolving_weapon.normal_damage)

            # NOTE: Must enable list before updating its contents, otherwise it will fail to disable next time
            resolver_dice_list.enable()
            # Discard attack dice
            resolver_dice_list._raw_item_list.remove(dice_selection)
            resolver_dice_list.set_item_list(resolver_dice_list._raw_item_list)

            # Redraw (and clock game state)
            game.state.redraw()

        # Cleanup UI panel
        game.ui.remove(panel)
        game.state.redraw()

    def fight(self, attacker, defender, defender_weapon):
        from operatives import Operative
        attacker: Operative = attacker
        defender: Operative = defender
        defender_weapon: Union[Weapon, None] = defender_weapon

        # Roll attack dice (both weapons)
        attacker_dice = self.roll_attack_dice(
            attacker=attacker,
            defender=defender,
            fighting=True,
        )
        defender_dice = ([], []) if defender_weapon == None else defender_weapon.roll_attack_dice(
            attacker=defender,
            defender=attacker,
            fighting=True,
        )

        # Resolve successful hits
        self.resolve_fight_attacks(attacker=attacker,
                                   defender=defender,
                                   defender_weapon=defender_weapon,
                                   attacker_dice=attacker_dice,
                                   defender_dice=defender_dice)

        # Remove incapacitated operatives
        attacker.remove_incapacitated()
        defender.remove_incapacitated()

        return True
