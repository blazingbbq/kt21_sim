from ..operative import *
import utils.distance
import weapons.tyranids
import action.names


class Genestealer(Operative):
    color = 0xc6b0a1  # Override color

    def __init__(self):
        datacard = Datacard(operative_type="Genestealer",
                            physical_profile=PhysicalProfile(
                                movement=utils.distance.CIRCLE * 3,
                                action_point_limit=2,
                                group_activation=1,
                                defence=3,
                                save=5,
                                wounds=9,
                                base=utils.distance.MM * 25),
                            ranged_weapon_profiles=[],
                            melee_weapon_profiles=[
                                weapons.tyranids.DoubleRendingClaws()],
                            abilities=[],
                            unique_actions=[],
                            keywords=[])
        super().__init__(datacard)

        # TODO: Other abilities / Special rules
        self.free_actions.append(action.names.DASH)
