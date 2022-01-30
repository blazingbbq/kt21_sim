

from abc import ABC
from enum import Enum
from tokenize import Special
from typing import List, Tuple
import utils.dice
import utils.distance


class SpecialRule(Enum):
    RNG_6 = 1
    LETHAL_5 = 2
    HOT = 3
    AP_1 = 4
    AP_2 = 5


class Weapon(ABC):
    def __init__(self,
                 name: str,
                 attacks: int,
                 skill: int,  # Either BallisticSkill / WeaponSkill
                 damage: Tuple[int, int],  # Damage tuple: (Normal, Crit)
                 # TODO: Add special rules and crit callbacks
                 special_rules: List[SpecialRule] = [],
                 critical_hit_rules: List[int] = [],
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

    def discard_attack_dice(self, roll: utils.dice.Dice, op):
        from operatives import Operative
        attacker: Operative = op

        if SpecialRule.HOT in self.special_rules:
            attacker.deal_mortal_wounds(3)

    def roll_attack_dice(self, attacker, defender):
        from operatives import Operative
        attacker: Operative = attacker
        defender: Operative = defender
        normal_hits, critical_hits = [], []

        rolls = [utils.dice.roll() for _ in range(self.attacks)]

        # TODO: Prompt rerolls for special rules
        # TODO: Prompt rerolls from abilities or team mechanics

        # Sort normal and crit hits
        for roll in rolls:
            # Result of 1 is always a failed hit, else check BS
            # Result of 6 is always a successful hit
            if (roll == 1 or roll < self.skill + attacker.bs_ws_modifier) and roll != 6:
                self.discard_attack_dice(roll, attacker)
                continue

            # Successful hit
            if roll >= self.crit_on:
                critical_hits.append(roll)
                continue
            normal_hits.append(roll)

        return normal_hits, critical_hits

    def roll_defence_dice(self, attacker, defender):
        from operatives import Operative
        attacker: Operative = attacker
        defender: Operative = defender
        normal_saves, critical_saves = [], []

        # TODO: Can retain 1 successful normal save if in cover

        rolls = [utils.dice.roll() for _ in range(
            defender.datacard.physical_profile.defence + self.ap_modifier)]

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

    def shoot(self, attacker, defender):
        # Roll attack dice
        normal_hits, critical_hits = self.roll_attack_dice(
            attacker=attacker,
            defender=defender,
        )

        # Roll defence dice
        normal_saves, critical_saves = self.roll_defence_dice(
            attacker=attacker,
            defender=defender,
        )

        # Resolve successful saves

        # Resolve successful hits

        # Remove incapacitated operatives

        return True
