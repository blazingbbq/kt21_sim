from ..weapon import SpecialRule, Weapon


class ScythingTalons(Weapon):
    def __init__(self):
        super().__init__(
            name="Scything Talons",
            attacks=4,
            skill=4,
            damage=(3, 5),
            special_rules=[SpecialRule.RELENTLESS],
            critical_hit_rules=[],
        )
