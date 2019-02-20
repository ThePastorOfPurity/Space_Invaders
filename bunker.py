import pygame
from pygame.sprite import Sprite
from pygame import PixelArray
from pygame import Surface
from random import randrange
from pygame.sprite import Group


class Bunker(Sprite):

    def __init__(self, settings, screen, row, col):
        super(Bunker, self).__init__()
        self.screen = screen
        self.height = settings.bunker_size
        self.width = settings.bunker_size
        self.color = settings.bunker_color
        self.image = Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.row = row
        self.col = col
        self.hit = False

    def update(self):
        self.screen.blit(self.image, self.rect)

    def bunker_hit(self, top):
        if not self.hit:
            px_array = PixelArray(self.image)
            if top:
                for i in range(self.height * 3):
                    px_array[randrange(0, self.width - 1), randrange(0,self.height // 2)] = (0, 0 ,0 ,0)
            else:
                for i in range(self.height * 3):
                    px_array[randrange(0, self.width - 1), randrange(self.height // 2, self.height - 1)] = (0, 0, 0, 0)
            self.hit = True
        else:
            self.kill()


def create_bunker(settings, screen, position):
    bunker = Group()
    for row in range(5):
        for col in range(9):
            if not ((row > 3 and (1 < col < 7)) or
                    (row > 2 and (2 < col < 6)) or
                    (row == 0 and (col < 1 or col > 7))):
                block = Bunker(settings, screen, row, col)
                block.rect.x = int(settings.screen_width * 0.15) + (250 * position) + (col * block.width)
                block.rect.y = int(settings.screen_height * 0.8) + (row * block.height)
                bunker.add(block)
    return bunker








