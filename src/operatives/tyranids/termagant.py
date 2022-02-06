from ..operative import *
import utils.distance
import weapons.tyranids


class Termagant(Operative):
    color = 0x644a5d  # Override color

    def __init__(self):
        datacard = Datacard(operative_type="Termagant",
                            physical_profile=PhysicalProfile(
                                movement=utils.distance.CIRCLE * 3,
                                action_point_limit=2,
                                group_activation=2,
                                defence=3,
                                save=6,
                                wounds=7,
                                base=utils.distance.MM * 25),
                            ranged_weapon_profiles=[
                                # TODO: Select between weapon options
                                weapons.tyranids.Devourer(),
                                # weapons.tyranids.Fleshborer(),
                                # weapons.tyranids.Spinefists(),
                            ],
                            melee_weapon_profiles=[weapons.tyranids.Claws()],
                            abilities=[],
                            unique_actions=[],
                            keywords=[])
        super().__init__(datacard)
