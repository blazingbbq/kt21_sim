from ..operative import *
import utils.distance
import weapons.tyranids


class Hormagaunt(Operative):
    color = 0x2e2833  # Override color

    def __init__(self):
        datacard = Datacard(operative_type="Hormagaunt",
                            physical_profile=PhysicalProfile(
                                movement=utils.distance.CIRCLE * 3,
                                action_point_limit=2,
                                group_activation=2,
                                defence=3,
                                save=6,
                                wounds=7,
                                base=utils.distance.MM * 25),
                            ranged_weapon_profiles=[],
                            melee_weapon_profiles=[
                                weapons.tyranids.ScythingTalons()],
                            abilities=[],
                            unique_actions=[],
                            keywords=[])
        super().__init__(datacard)
