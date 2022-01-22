import pygame
from state.gamestate import *
from state.team import *
from operatives import *
from utils.distances import *

START_FULLSCREEN = False


def gamestate():
    return KT21Sim.gamestate


class KT21Sim:
    # Pygame management
    background: pygame.Surface = None
    clock: pygame.time.Clock = None
    running: bool = True

    # Game state
    gamestate: GameState = None

    def start():
        # Init display
        # NOTE: Can get pygame screen using pygame.display.get_surface()
        screen = pygame.display.set_mode(
            (0, 0), pygame.FULLSCREEN if START_FULLSCREEN else pygame.RESIZABLE)
        pygame.display.set_caption("KT21 Sim")
        pygame.mouse.set_visible(True)

        Distance.update_inch_size()

        # Init clock
        KT21Sim.clock = pygame.time.Clock()

        # Create background
        KT21Sim.background = pygame.Surface(
            screen.get_size()).convert()
        KT21Sim.background.fill((170, 238, 187))

        # Display background
        screen.blit(KT21Sim.background, (0, 0))
        pygame.display.flip()

        # Init gamestate
        KT21Sim.gamestate = GameState()

        # Populate teams
        team1 = Team()
        team2 = Team()
        KT21Sim.gamestate.add_teams(team1, team2)

        team1.add_operatives(TrooperVeteran())
        team2.add_operatives(TrooperVeteran())

        # Run through game phases
        KT21Sim.pump()
        KT21Sim.gamestate.redraw()
        KT21Sim.gamestate.run()

        # Spin once game is over
        # TODO: Do something once game is over
        while KT21Sim.running:
            KT21Sim.pump()
            KT21Sim.gamestate.redraw()

    def wipe():
        screen = pygame.display.get_surface()
        screen.blit(KT21Sim.background, (0, 0))

    def pump():
        # Handle input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                KT21Sim.running = False
                pygame.quit()
                exit()

        # Tick clock to prevent spinning too fast
        KT21Sim.clock.tick(60)
