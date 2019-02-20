import sys

import pygame

import game_functions as gf

from settings import Settings
from game_stats import GameStats
from ship import Ship
from button import Button
from scoreboard import Scoreboard
from pygame.sprite import Group
from bunker import create_bunker


def run_game():
    pygame.init()
    settings = Settings()
    screen_size = (settings.screen_width, settings.screen_height)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Space Invaders")

    stats = GameStats(settings)
    sb = Scoreboard(settings, screen, stats)

    play_button = Button(settings, screen, "Play")

    ship = Ship(settings, screen)

    bullets = Group()
    lasers = Group()
    aliens = Group()
    bunkers = Group(create_bunker(settings, screen, 0),
                    create_bunker(settings, screen, 1),
                    create_bunker(settings, screen, 2),
                    create_bunker(settings, screen, 3))

    clock = pygame.time.Clock()

    gf.create_fleet(settings, screen, ship, aliens)

    while True:
        clock.tick(60)
        gf.check_events(settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(settings, screen, stats, sb, ship, aliens, bullets, lasers)
            gf.update_aliens(settings, stats, screen, sb, ship, aliens, bullets, lasers)

        gf.update_screen(settings, screen, stats, sb, ship, aliens, bullets, bunkers, lasers, play_button)


run_game()
