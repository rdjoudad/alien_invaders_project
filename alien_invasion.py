"""
Alien Invasion Game, Milestone 2
Ryma Djoudad
Game that has bullet-firing ship that moves up and down
Starter code from participation activity (Python crash course, 3rd edition)
4/11/2026
"""


import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import Gamestats
from ship import Ship
from bullet import Bullet
from alien import Alien




class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initialize the game and create game resources"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics.
        self.stats = Gamestats(self)

        self.screen_rect = self.screen.get_rect()

        self.ship = Ship(ai_game=self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        # Start Alien Invasion in an active state.
        self.game_active = True

    def run_game(self):
        """Start the main loop of the game"""
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(60)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.right <= 0 or bullet.rect.left >= self.screen_rect.right:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)

    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        # Ship collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Aliens reach left edge
        self._check_aliens_left()


    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
        # Decrement ships_left.
            self.stats.ships_left -= 1

        # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

        # Create a new fleet and put the ship to the left
            self._create_fleet()
            self.ship.left_ship()

        # Pause.
            sleep(0.5)

        else: 
            self.game_active = False

    # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

    # Look for aliens hitting the left side of the screen.
        self._check_aliens_left()


    def _check_fleet_edges(self):
        """Respond if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Change the fleet direction so it bounces up-down"""
        self.settings.fleet_direction *= -1

    def left_ship(self):
        """Put the ship on the left edge of the screen."""
        self.rect.midleft = self.screen_rect.midleft
        self.x = float(self.rect.x)

    def _check_aliens_left(self):
        """Check if any aliens have reached the left end of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.left <= 0:
                self._ship_hit()
                break

    def _check_events(self):
        """Respond to keypresses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        """Create a new bullet."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """Create a full fleet of aliens."""
        self.aliens.empty()

        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_y = alien_height

        while current_y < (self.settings.screen_height - alien_height):

            current_x = self.settings.screen_width - alien_width

            while current_x > 0:
                self._create_alien(current_x, current_y)
                current_x -= 4 * alien_width

            current_y += 2 * alien_height  

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it."""
        new_alien = Alien(self)
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        new_alien.x = float(x_position)
        new_alien.y = float(y_position)
        self.aliens.add(new_alien)

    def _update_screen(self):
        """Update images and flip screen"""
        self.screen.fill(self.settings.bg_color)

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.ship.blitme()
        self.aliens.draw(self.screen)

        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()