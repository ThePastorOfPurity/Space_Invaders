import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Class to manage the bullets fired from ship"""

    def __init__(self, settings, screen, ship):
        """Create a bullet obj at ship's current position"""
        super(Bullet, self).__init__()
        self.screen = screen

        self.rect = pygame.Rect(0, 0, settings.bullet_width, settings.bullet_height)

        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        self.y = float(self.rect.y)

        self.color = settings.bullet_color
        self.speed_factor = settings.bullet_speed_factor

    def update(self):
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
