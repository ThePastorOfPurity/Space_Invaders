import pygame
from pygame.sprite import Sprite
from random import choice


class Mystery(Sprite):
    def __init__(self, settings, screen):
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.score_range = settings.ufo_scores
        self.score = None
        self.image = pygame.image.load('resources/mystery.png')
        self.rect = self.image.get_rect()
        self.score_image = None
        self.prep_score()
        self.death_frames = []
        self.index = None
        self.death_frames.append(pygame.image.load('resources/mystery-2.png'))
        self.death_frames.append(self.score_image)
        self.last = None
        self.wait = 500
        self.speed = settings.mystery_speed * (choice([-1, 1]))
        self.rect.x = 0 if self.speed > 0 else settings.screen_width
        self.rect.y = settings.screen_height * 0.1
        self.dead = False

    def explosion(self):
        self.dead = True
        self.index = 0
        self.image = self.death_frames[self.index]
        self.last = pygame.time.get_ticks()

    def get_score(self):
        self.score = choice(self.score_range)
        return self.score

    def update(self):
        if not self.dead:
            self.rect.x += self.speed
            if self.speed > 0 and self.rect.left > self.settings.screen.width:
                self.kill()
            else:
                self.image = self.death_frames[self.index]
                self.wait += 500

    def blitme(self):
        self.screen.blit(self.image, self.rect)

