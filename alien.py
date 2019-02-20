import pygame
from pygame.sprite import Sprite
from random import choice


class Alien(Sprite):

    def __init__(self, settings, screen, alien_type=3):
        super(Alien, self).__init__()
        self.screen = screen
        self.settings = settings
        self.alien_type = alien_type

        self.image = None
        self.images = None
        self.alien_index = None
        self.explosion_index = None
        self.last = None
        self.death_frames = None

        self.rect = None
        self.init_images()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

        self.alien_speed_factor = 1
        self.dead = False

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        else:
            return False

    def update(self):
        self.x += (self.settings.alien_speed_factor * self.settings.fleet_direction)
        self.rect.x = self.x
        test = pygame.time.get_ticks()
        if not self.dead:
            if abs(self.last - test) > 1000:
                self.last = test
                self.alien_index = (self.alien_index + 1) % len(self.images)
                self.image = self.images[self.alien_index]
        else:
            if abs(self.last - test) > 20:
                self.last = test
                self.explosion_index += 1
                if self.explosion_index >= len(self.death_frames):
                    self.kill()
                else:
                    self.image = self.death_frames[self.explosion_index]

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def init_images(self):
        if self.alien_type == 1:
            self.images = [
                pygame.image.load('resources/alien1-1.png'),
                pygame.image.load('resources/alien1-2.png')
            ]
            self.death_frames = [
                pygame.image.load('resources/alien1-3.png'),
                pygame.image.load('resources/alien1-4.png'),
                pygame.image.load('resources/alien1-5.png'),
                pygame.image.load('resources/alien1-6.png')
            ]
        elif self.alien_type == 2:
            self.images = [
                pygame.image.load('resources/alien2-1.png'),
                pygame.image.load('resources/alien2-2.png')
            ]
            self.death_frames = [
                pygame.image.load('resources/alien2-3.png'),
                pygame.image.load('resources/alien2-4.png'),
                pygame.image.load('resources/alien2-5.png'),
                pygame.image.load('resources/alien2-6.png')
            ]
        else:
            self.images = [
                pygame.image.load('resources/alien3-1.png'),
                pygame.image.load('resources/alien3-2.png')
            ]
            self.death_frames = [
                pygame.image.load('resources/alien3-3.png'),
                pygame.image.load('resources/alien3-4.png'),
                pygame.image.load('resources/alien3-5.png'),
                pygame.image.load('resources/alien3-6.png')
                ]
        self.alien_index = 0
        self.image = self.images[self.alien_index]
        self.rect = self.image.get_rect()
        self.last = pygame.time.get_ticks()

    def explosion(self):
        self.dead = True
        self.explosion_index = 0
        self.image = self.death_frames[self.explosion_index]
        self.last = pygame.time.get_ticks()



