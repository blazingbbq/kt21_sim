from ..operative import *
import utils.distance


class KommandoBoy(Operative):
    color = 0x484942  # Override color

    def __init__(self):
        datacard = Datacard(operative_type="Kommando Boy",
                            physical_profile=PhysicalProfile(
                                movement=utils.distance.CIRCLE * 3, action_point_limit=2, group_activation=1, defence=3, save=5, wounds=10, base=utils.distance.MM * 32),
                            ranged_weapon_profiles=[],
                            melee_weapon_profiles=[],
                            abilities=[],
                            unique_actions=[],
                            keywords=[])
        super().__init__(datacard)
