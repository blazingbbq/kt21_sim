import pygame
from state.gamestate import *
from state.team import *
from operatives import *

START_FULLSCREEN = False


class KT21Sim:
    # Pygame management
    background: pygame.Surface = None
    running: bool = True

    # Game state
    gamestate: GameState = None

    def start():
        # Init display
        # Can get pygame screen using pygame.display.get_surface()
        screen = pygame.display.set_mode(
            (0, 0), pygame.FULLSCREEN if START_FULLSCREEN else pygame.RESIZABLE)
        pygame.display.set_caption("KT21 Sim")
        pygame.mouse.set_visible(True)

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
        team1.add_operative(TrooperVeteran())

        KT21Sim.gamestate.add_team(team1)
        # KT21Sim.gamestate.add_team(Team())

        clock = pygame.time.Clock()
        while KT21Sim.running:
            clock.tick(60)
            KT21Sim.pump()

            # Update game state
            KT21Sim.gamestate.update()

            # Draw
            # FIXME: Do not blit every frame...
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
