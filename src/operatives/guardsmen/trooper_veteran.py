from ..operative import *
import utils.distance
import weapons.guardsmen


class TrooperVeteran(Operative):
    color = 0x000080  # Override color

    def __init__(self):
        datacard = Datacard(operative_type="Trooper Veteran",
                            physical_profile=PhysicalProfile(
                                movement=utils.distance.CIRCLE * 3, action_point_limit=2, group_activation=2, defence=3, save=5, wounds=7, base=utils.distance.MM * 25),
                            ranged_weapon_profiles=[
                                weapons.guardsmen.Lasgun(),
                            ],
                            melee_weapon_profiles=[],
                            abilities=[],
                            unique_actions=[],
                            keywords=[])
        super().__init__(datacard)
