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

        clock = pygame.time.Clock()
        while KT21Sim.running:
            clock.tick(60)
            KT21Sim.pump()

            # Update game state
            KT21Sim.gamestate.run()

            # Draw
            KT21Sim.redraw()

    def redraw():
        screen = pygame.display.get_surface()
        screen.blit(KT21Sim.background, (0, 0))
        KT21Sim.gamestate.redraw()
        pygame.display.flip()

    def pump():
        # Handle input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                KT21Sim.running = False
                pygame.quit()
                exit()
