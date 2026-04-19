import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def check_edges(self):
        """Return True if ship hits left edge."""
        screen_rect = self.screen.get_rect()
        return self.rect.left <= 0

    def update(self):
        """Move the alien to the left while still bouncing up and down."""
        self.x += self.settings.alien_speed * self.settings.fleet_direction

        self.rect.x = self.x
        self.rect.y = self.y