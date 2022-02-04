# kt21_sim

## Running

Run using:

```sh
./kt21sim
```

Use the `--dependencies` flag to install required dependencies.

## Gameplay Notes

Wherever applicable, use `ESCAPE` to cancel actions and `RETURN` to confirm actions (and end them early).
Can also use `RETURN` while resolving attack dices in fights to automatically strike with the highest dice rolled.

## Core Rules

- [x] Tools of War
    - [x] Operatives
    - [x] Kill Teams
    - [x] Distances
    - [x] Killzones
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
- [x] Firefight Phase
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
        - [x] Pick Up
        - [x] Capture Objective
        - [x] Shoot
        - [x] Fight
- [x] Wounds and Damage
- [x] Controlling Objective Markers and Tokens
- [x] Line of Sight
    - [x] Visible
    - [x] Obscured
    - [x] Cover
- [x] Killzones
    - [x] Terrain Traits
        - [x] Heavy
        - [x] Light
        - [x] Traversable
        - [x] Insignificant
        - [x] Scalable
        - [ ] Barricades
        - [x] Vantage Point
    - [ ] Moving Through Terrain
        - [x] Traverse
        - [ ] Jump
        - [ ] Climb
        - [ ] Drop
        - [x] Flying Over Terrain
    - [ ] Example Boards
    - [x] Example Terrain Features
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
        - [x] Include support for difficult terrain traversal
    - [x] Utilites for determining valid targets
        - [x] shoot
            - [x] Include support for cover / obscuring
        - [x] charge
        - [x] fight
    - [x] Utility for rolling dice
    - [x] Utility for determining which team controls objective based on models within range
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
- [x] Character objects.
    - [x] Include all stats exposed on game card as property.
    - [x] Maintain list of Actions that can be performed (include description and callback)
        - [ ] Show action description on hover?
    - [ ] List of Abilities (passive and active)
    - [ ] List of Equipement
    - [x] List of Weapons
    - [ ] List of Tags this unit qualifies, helps when determining validity of target selection
    - [ ] Callbacks for character state changes:
        - [x] `on_activation_end`
        - [x] `on_incapacitated`
    - [x] Handle "injured" state
    - [x] Manage engage/conceal order
- [ ] Strategic Ploy object
- [x] Weapon Object
    - [ ] `on_crit` callback
    - [ ] Add support for all special rules (ceaseless, relentless, etc.)
- [ ] Equipement Object
- [ ] Tags namespace that manages all possible model tags
- [x] Mission objective objects
    - [x] Add special interact Action to units within range
- [x] Terrain
    - [x] Add different height levels
    - [ ] Vantage points
    - [ ] Climbing / dropping
    - [x] Heavy + Light terrain types
    - [ ] Add legend to game UI showing colors for terrain types
- [ ] Add team builder
- [ ] Add narrative play mode
    - [ ] Exp, battle honours/scars, rare equipment, assets, requisitions
    - [ ] Progression trees for character archetype and faction specific
