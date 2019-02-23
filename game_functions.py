import sys
from time import sleep

import pygame
import random
from bullet import Bullet
from alien import Alien
from laser import Laser
from mystery import Mystery


def check_events(settings, screen, stats, sb, play_button, ship, aliens, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
        check_keydown_event(settings, screen, event, ship, bullets)
        check_keyup_event(event, ship)


def check_play_button(settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)

        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(settings, screen, ship, aliens)
        ship.center_ship()


def check_keydown_event(settings, screen, event, ship, bullets):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            fire_bullet(settings, screen, ship, bullets)
        elif event.key == pygame.K_q:
            sys.exit()


def check_keyup_event(event, ship):
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_RIGHT:
            ship.moving_right = False
        if event.key == pygame.K_LEFT:
            ship.moving_left = False


def get_number_aliens_x(settings, alien_width):
    available_space_x = settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (3 * alien_width))
    return number_aliens_x


def get_number_rows(settings, ship_height, alien_height):
    available_space_y = (settings.screen_height - (4 * alien_height) - ship_height)
    number_rows = int(available_space_y / (11 * alien_height))
    return number_rows


def create_alien(settings, screen, aliens, alien_number, row_number):
    if row_number < 2:
        alien_type = 1
    elif row_number < 4:
        alien_type = 2
    else:
        alien_type = 3
    alien = Alien(settings, screen, alien_type)
    alien_width = alien.rect.width
    alien.x = alien_width + 1.25 * alien_width * alien_number
    alien.rect.y = alien.rect.height + 1.25 * alien.rect.height * row_number
    alien.rect.x = alien.x
    alien.rect.y += int(settings.screen_height / 8)
    aliens.add(alien)


def create_fleet(settings, screen, ship, aliens):
    alien = Alien(settings, screen)
    number_aliens_x = get_number_aliens_x(settings, alien.rect.width)
    number_rows = get_number_rows(settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(settings, screen, aliens, alien_number, row_number)


def update_screen(settings, screen, stats, sb, ship, aliens, bullets, bunkers, lasers, play_button, mystery):
    """update images on screen and flip to the new screen"""
    screen.fill(settings.bg_color)

    aliens.draw(screen)
    check_bunker_collisions(lasers, bullets, bunkers)
    bunkers.update()
    for bullet in bullets.sprites():
        bullet.draw()
    if mystery:
        mystery.update()
        for mystery in mystery.sprites():
            mystery.blitme()
    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()
    for laser in lasers.sprites():
        laser.blitme()
    ship.blitme()
    pygame.display.flip()


def fire_bullet(settings, screen, ship, bullets):
    if len(bullets) < settings.bullets_allowed:
        new_bullet = Bullet(settings, screen, ship)
        bullets.add(new_bullet)


def update_bullets(settings, screen, stats, sb, ship, aliens, bullets, lasers, mystery):
    bullets.update()
    lasers.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    for laser in lasers.copy():
        if laser.rect.bottom > settings.screen_height:
            lasers.remove(laser)

    check_bullet_alien_collisions(settings, screen, stats, sb, ship, aliens, bullets, mystery)
    check_laser_ship_collisions(settings, screen, stats, sb, ship, aliens, lasers, bullets)


def check_bullet_alien_collisions(settings, screen, stats, sb, ship, aliens, bullets, mystery):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, False, collided=alien_check)

    if collisions:
        for aliens in collisions.values():
            for i in aliens:
                i.explosion()
            stats.score += settings.alien_points * len(aliens)
            sb.prep_score()

        check_high_score(stats, sb)

    if len(aliens) == 0:
        if mystery:
            for i in mystery.sprites():
                i.kill()
        # If the entire fleet is destroyed, start a new level.
        bullets.empty()
        settings.increase_speed()
        # Increase level
        stats.level += 1
        sb.prep_level()
        settings.increase_base_speed()
        settings.reset_alien_speed()
        create_fleet(settings, screen, ship, aliens)
        stats.speedup = len(aliens) - (len(aliens) // 5)

    mystery_collisions = pygame.sprite.groupcollide(bullets, mystery, True, False, collided=alien_check)
    if mystery_collisions:
        for mystery in mystery_collisions.values():
            for i in mystery:
                stats.score += i.score
                i.begin_death()
            sb.prep_score()
        check_high_score(stats, sb)

        create_fleet(settings, screen, ship, aliens)
    stats.aliens_left = len(aliens)


def check_fleet_edges(settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(settings, aliens)
            break


def change_fleet_direction(settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += settings.fleet_drop_speed
    settings.fleet_direction *= -1


def update_aliens(settings, stats, screen, sb, ship, aliens, bullets, lasers):
    check_fleet_edges(settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        print("Ship hit!!!")
        ship_hit(settings, stats, screen, sb, ship, aliens, bullets, lasers)

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(settings, stats, screen, sb, ship, aliens, bullets, lasers)
    if aliens.sprites():
        fire_laser(settings, screen, aliens, lasers)


def ship_hit(settings, stats, screen, sb, ship, aliens, bullets, lasers):
    """Respond to ship being hit by alien."""
    ship.explosions()
    ship.update()
    while ship.explosion:
        ship.blitme()
        ship.update()
        pygame.display.flip()
    if stats.ships_left > 0:
        # Decrement ships_left.
        stats.ships_left -= 1

        # Update scoreboard.
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        lasers.empty()
        # Create a new fleet and center the ship.
        create_fleet(settings, screen, ship, aliens)
        stats.alien_left = len(aliens.sprites())
        stats.next_speedup = len(aliens) - (len(aliens) // 5)
        ship.center_ship()
        # Pause.
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(settings, stats, screen, sb, ship, aliens, bullets, lasers):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(settings, stats, screen, sb, ship, aliens, bullets, lasers)
            break


def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_bunker_collisions(lasers, bullets, bunkers):
    collisions = pygame.sprite.groupcollide(bullets, bunkers, True, False)

    for blocks in collisions.values():
        for block in blocks:
            block.bunker_hit(top=False)

    collisions = pygame.sprite.groupcollide(lasers, bunkers, True, False)

    for blocks in collisions.values():
        for block in blocks:
            block.bunker_hit(top=True)


def fire_laser(settings, screen, aliens, lasers):
    alien = random.choice(aliens.sprites())
    if len(lasers) < settings.lasers_allowed and \
            (settings.laser_stamp is None or (abs(pygame.time.get_ticks() - settings.laser_stamp) > settings.laser_time)):
        laser = Laser(settings, screen, alien)
        lasers.add(laser)


def check_laser_ship_collisions(settings, screen, stats, sb, ship, aliens, lasers, bullets):
    collide = pygame.sprite.spritecollideany(ship, lasers)
    if collide:
        ship_hit(settings, stats, screen, sb, ship, aliens, bullets, lasers)


def init_music(settings, stats):
    if stats. game_active:
        settings.continue_music()


def alien_check(bullet, alien):
    if alien.dead:
        return False
    return pygame.sprite.collide_rect(bullet,alien)


def create_mystery(settings, screen):
    mystery = None
    if random.randrange(0, 100) <= 15:
        mystery = Mystery(settings, screen)
    time = pygame.time.get_ticks()
    return time, mystery


def mystery_check(settings, screen, group):
    if not settings.last and not group:
        settings.last_mystery, i = create_mystery(settings, screen)
        if i:
            group.add(i)
    elif abs(pygame.time.get_ticks() - settings.last) > settings.mystery_min and not group:
        settings.last, i = create_mystery(settings, screen)
        if i:
            group.add(i)


