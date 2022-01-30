from typing import List
from .physical_profile import *
from action import Action
from weapons import Weapon


class Datacard:
    def __init__(self,
                 operative_type: str,
                 physical_profile: PhysicalProfile,
                 ranged_weapon_profiles: List[Weapon],
                 # TODO: Add classes for these parameters
                 melee_weapon_profiles,
                 abilities,
                 unique_actions: List[Action],
                 keywords,
                 ):
        self.operative_type = operative_type
        self.physical_profile = physical_profile
        self.ranged_weapon_profiles = ranged_weapon_profiles
        self.melee_weapon_profiles = melee_weapon_profiles
        self.abilities = abilities
        self.unique_actions = unique_actions
        self.keywords = keywords
