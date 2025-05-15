import pygame
import sys
from pygame.locals import *

pygame.init()
from game import MiniChess5x6
if __name__ == "__main__":
    game = MiniChess5x6()
    game.run()