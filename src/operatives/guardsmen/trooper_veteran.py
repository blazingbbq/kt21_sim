from ..operative import *
from utils.distances import *


class TrooperVeteran(Operative):
    color = 0x000080  # Override color
    datacard = Datacard(operative_type="Trooper Veteran",
                        physical_profile=PhysicalProfile(
                            movement=Distance.from_circle(3), action_point_limit=2, group_activation=2, defence=3, save=5, wounds=7, base=Distance.from_mm(25)),
                        ranged_weapon_profiles=[],
                        melee_weapon_profiles=[],
                        abilities=[],
                        unique_actions=[],
                        keywords=[])

    def __init__(self):
        super().__init__(TrooperVeteran.datacard)