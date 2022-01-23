import pygame
import game.ui


def pump():
    # Handle input events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        game.ui.process(event)
