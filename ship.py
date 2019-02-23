import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, settings, screen):
        super(Ship, self).__init__()

        self.screen = screen
        self.settings = settings

        self.ship = pygame.image.load('resources/ship.png')
        self.image = self.ship
        self.death_frames = [
            pygame.image.load('resources/ship-2.png'),
            pygame.image.load('resources/ship-3.png'),
            pygame.image.load('resources/ship-4.png'),
            pygame.image.load('resources/ship-5.png'),
            pygame.image.load('resources/ship-6.png'),
            pygame.image.load('resources/ship-7.png'),
            pygame.image.load('resources/ship-8.png'),
            pygame.image.load('resources/ship-9.png')
        ]
        self.index = None
        self.last = None
        self.rect = self.image.get_rect()

        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.center = float(self.rect.centerx)

        self.moving_right = False
        self.moving_left = False

        self.explosion = False

    def update(self):
        if not self.explosion:
            if self.moving_right and self.rect.right < self.screen_rect.right:
                self.rect.centerx += self.settings.ship_speed_factor
            elif self.moving_left and self.rect.left > 0:
                self.rect.centerx -= self.settings.ship_speed_factor
        else:
            test = pygame.time.get_ticks()
            if abs(test - self.last) > 250:
                self.index += 1
                if self.index < len(self.death_frames):
                    self.image = self.death_frames[self.index]
                    self.last = test
                else:
                    self.explosion = False
                    self.image = self.ship

    def blitme(self):
        """draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen."""
        self.center = self.screen_rect.centerx

    def explosions(self):
        self.explosion = True
        self.index = 0
        self.image = self.death_frames[self.index]
        self.last = pygame.time.get_ticks()
