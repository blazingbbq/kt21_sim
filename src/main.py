#!/usr/bin/env python

import pygame
from kt21sim import *

if not pygame.font:
    print("Warning, fonts disabled")
if not pygame.mixer:
    print("Warning, sound disabled")


def main():
    pygame.init()
    KT21Sim.start()
    pygame.quit()


# Call 'main' function when script is executed
if __name__ == "__main__":
    main()
