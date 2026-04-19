"""
Game Stats Class
Ryma Djoudad
Class that initializes and keeps track of changes during game
Copied from book instructions
4/19/2026
"""

class Gamestats:
        
 def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

 def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit