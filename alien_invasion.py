import sys
import pygame

class AlienInvasion:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Alien Invasion")
