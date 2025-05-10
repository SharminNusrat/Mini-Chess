import pygame
import sys
from pygame.locals import *

# Initialize pygame first
pygame.init()

# Now import the game module after pygame is initialized
from game import MiniChess5x6

if __name__ == "__main__":
    # Create and run the game
    game = MiniChess5x6()
    game.run()