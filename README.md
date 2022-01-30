# kt21_sim

## Dependencies

```sh
pip install pygame pygame_gui -U
```

## Running

```sh
./run
```

## Gameplay Notes

Wherever applicable, use `ESCAPE` to cancel actions and `RETURN` to confirm actions (and end them early)

## Core Rules

- [ ] Tools of War
    - [x] Operatives
    - [ ] Kill Teams
    - [x] Distances
    - [ ] Killzones
    - [x] Dice
- [x] Datacards
    - [x] Engagement Range
    - [x] Modifying Characteristics
    - [ ] Fire Teams
- [x] Battle Structure
- [x] Initiative Phase
    - [x] Ready Operatives
    - [x] Determine Initiative
- [x] Strategy Phase
    - [x] Generate Command Points
    - [ ] Play Strategic Ploys
    - [ ] Target Reveal
- [ ] Firefight Phase
    - [x] Perform Actions
    - [ ] Overwatch
    - [x] Actions
        - [x] Normal Move
        - [x] Fly
        - [x] Charge
        - [x] Fall Back
        - [x] Dash
        - [x] Pass
        - [ ] Overwatch
        - [ ] Pick Up
        - [x] Shoot
        - [x] Fight
- [x] Wounds and Damage
- [ ] Controlling Objective Markers and Tokens
- [ ] Line of Sight
    - [ ] Visible
    - [ ] Obscured
    - [ ] Cover
- [ ] Killzones
    - [ ] Terrain Traits
        - [ ] Heavy
        - [ ] Light
        - [ ] Traversable
        - [ ] Insignificant
        - [ ] Scalable
        - [ ] Barricades
        - [ ] Vantage Point
    - [ ] Moving Through Terrain
        - [ ] Traverse
        - [ ] Jump
        - [ ] Climb
        - [ ] Drop
        - [ ] Flying Over Terrain
    - [ ] Example Boards
    - [ ] Example Terrain Features
- [ ] Ways to Play
    - [ ] Open Play
    - [ ] Matched Play
    - [ ] Narrative Play

## Development Roadmap

- [x] Top level gamestate namespace class with utilities:
    - [x] Pump utility for use while game objects are spinning (e.g. waiting for user input). Should pump pygame / check quit events
    - [ ] Callbacks for team wide action events?
        - [ ] `on_shoot`, `on_damage`, `on_fight` ?
            - Maybe models check these whenever they perform their own state change callbacks
    - [x] Utility for determining valid movement destinations
        - [ ] Include support for difficult terrain traversal
    - [x] Utilites for determining valid targets
        - [x] shoot
            - [ ] Include support for cover / obscuring
        - [x] charge
        - [x] fight
    - [x] Utility for rolling dice
    - [ ] Utility for determining which team controls objective based on models within range
    - [ ] Have chain activation queue that can insert other units so that they are activated immediately following another operative's activation.
        - [ ] Or, make this a callback that gets registered in the operative's `on_activation_end` and removes itself from the list after being called
    - [ ] Maintain list of strategic ploys that can be used by each player
    - [ ] Save gamestate between each activation for rolling back actions
    - [ ] Add TacOps
        - [ ] Allow players to pick tacops at start of game
        - [ ] Allow choice between the available archetypes satisfied by faction / fireteam
    - [ ] Add utilities for scoring victory points
- [x] Add standalone utility classes for resolving shooting / fighting
    - [ ] Retaining dice for cover (include callback for special handling like retaining 2 dice instead of one?)
- [x] Turnphase objects for each phase in the game. Loop through these until all turns have elapsed
    - [ ] Callback hooks for different phases of the game where armies could have actions to take (e.g. guardsmen orders)
    - [x] Roll initiative
- [ ] Character objects.
    - [x] Include all stats exposed on game card as property.
    - [x] Maintain list of Actions that can be performed (include description and callback)
        - [ ] Show action description on hover?
    - [ ] List of Abilities (passive and active)
    - [ ] List of Equipement
    - [x] List of Weapons
    - [ ] List of Tags this unit qualifies, helps when determining validity of target selection
    - [ ] Callbacks for character state changes:
        - [ ] `after_activation` or `on_activation_end`
    - [x] Handle "injured" state
    - [x] Manage engage/conceal order
- [ ] Strategic Ploy object
- [x] Weapon Object
    - [ ] `on_crit` callback
    - [ ] Add support for all special rules (ceaseless, relentless, etc.)
- [ ] Equipement Object
- [ ] Tags namespace that manages all possible model tags
- [ ] Mission objective objects
    - [ ] Add special interact Action to units within range
- [ ] Terrain
    - [ ] Add different height levels
    - [ ] Vantage points
    - [ ] Climbing / dropping
    - [ ] Heavy + Light terrain types
    - [ ] Add legend to game UI showing colors for terrain types
- [ ] Add team builder
- [ ] Add narrative play mode
    - [ ] Exp, battle honours/scars, rare equipment, assets, requisitions
    - [ ] Progression trees for character archetype and faction specific
