from weapons.guardsmen.bayonet import Bayonet
from weapons.guardsmen.lasgun import Lasgun
from ..operative import *
import utils.distance


class TrooperVeteran(Operative):
    color = 0x000080  # Override color

    def __init__(self):
        datacard = Datacard(operative_type="Trooper Veteran",
                            physical_profile=PhysicalProfile(
                                movement=utils.distance.CIRCLE * 3,
                                action_point_limit=2,
                                group_activation=2,
                                defence=3,
                                save=5,
                                wounds=7,
                                base=utils.distance.MM * 25),
                            ranged_weapon_profiles=[Lasgun()],
                            melee_weapon_profiles=[Bayonet()],
                            abilities=[],
                            unique_actions=[],
                            keywords=[])
        super().__init__(datacard)
