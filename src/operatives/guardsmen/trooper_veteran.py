from ..operative import *


class TrooperVeteran(Operative):
    datacard = Datacard(operative_type="Trooper Veteran",
                        physical_profile=PhysicalProfile(
                            movement=3, action_point_limit=2, group_activation=2, defence=3, save=5, wounds=7, base=25),
                        ranged_weapon_profiles=[],
                        melee_weapon_profiles=[],
                        abilities=[],
                        unique_actions=[],
                        keywords=[])

    def __init__(self):
        super().__init__(TrooperVeteran.datacard)
