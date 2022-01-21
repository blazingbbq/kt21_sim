#!/usr/bin/env python

import os
import pygame

if not pygame.font:
    print("Warning, fonts disabled")
if not pygame.mixer:
    print("Warning, sound disabled")


def main():
    # Initialize
    pygame.init()
    screen = pygame.display.set_mode((1280, 480), pygame.SCALED)
    pygame.display.set_caption("KT21 Sim")
    pygame.mouse.set_visible(True)

    # Create background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((170, 238, 187))

   # Create centered text
    if pygame.font:
        font = pygame.font.Font(None, 64)
        text = font.render("Hello, pygame!", True, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width() / 2, y=10)
        background.blit(text, textpos)

    # Display background
    screen.blit(background, (0, 0))
    pygame.display.flip()

    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(60)

        # Handle input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # Update game state

        # Draw
        screen.blit(background, (0, 0))
        pygame.display.flip()

    pygame.quit()


# Call 'main' function when script is executed
if __name__ == "__main__":
    main()
