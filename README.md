# kt21_sim

## Roadmap

- [ ] Top level gamestate namespace class with utilities:
    - [ ] Pump utility for use while game objects are spinning (e.g. waiting for user input). Should pump pygame / check quit events
    - [ ] Callbacks for team wide action events?
        - [ ] `on_shoot`, `on_damage`, `on_fight` ?
            - Maybe models check these whenever they perform their own state change callbacks
    - [ ] Utility for determining valid movement destinations
        - [ ] Include support for difficult terrain traversal
    - [ ] Utilites for determining valid targets
        - [ ] shoot
            - [ ] Include support for cover / obscuring
        - [ ] charge
        - [ ] fight
    - [ ] Utility for rolling dice
    - [ ] Utility for determining which team controls objective based on models within range
    - [ ] Have chain activation queue that can insert other units so that they are activated immediately following another operative's activation.
        - [ ] Or, make this a callback that gets registered in the operative's `on_activation_end` and removes itself from the list after being called
    - [ ] Maintain list of strategic ploys that can be used by each player
    - [ ] Save gamestate between each activation for rolling back actions
    - [ ] Add TacOps
        - [ ] Allow players to pick tacops at start of game
        - [ ] Allow choice between the available archetypes satisfied by faction / fireteam
    - [ ] Add utilities for scoring victory points
- [ ] Add standalone utility classes for resolving shooting / fighting
    - [ ] Retaining dice for cover (include callback for special handling like retaining 2 dice instead of one?)
- [ ] Turnphase objects for each phase in the game. Loop through these until all turns have elapsed
    - [ ] Callback hooks for different phases of the game where armies could have actions to take (e.g. guardsmen orders)
    - [ ] Roll initiative
- [ ] Character objects.
    - [ ] Include all stats exposed on game card as property.
    - [ ] Maintain list of Actions that can be performed (include description and callback)
    - [ ] List of Abilities (passive and active)
    - [ ] List of Equipement
    - [ ] List of Weapons
    - [ ] List of Tags this unit qualifies, helps when determining validity of target selection
    - [ ] Callbacks for character state changes:
        - [ ] `after_activation` or `on_activation_end`
    - [ ] Handle "injured" state
    - [ ] Manage engage/conceal order
- [ ] Strategic Ploy object
- [ ] Weapon Object
    - [ ] `on_crit` callback
    - [ ] Add support for special rules (ceaseless, relentless, etc.)
- [ ] Equipement Object
- [ ] Tags namespace that manages all possible model tags
- [ ] Mission objective objects
    - [ ] Add special interact Action to units within range
- [ ] Terrain
    - [ ] Add different height levels
    - [ ] Vantage points
    - [ ] Climbing / dropping
    - [ ] Heavy + Light terrain types
- [ ] Add team builder
- [ ] Add narrative play mode
    - [ ] Exp, battle honours/scars, rare equipment, assets, requisitions
    - [ ] Progression trees for character archetype and faction specific
