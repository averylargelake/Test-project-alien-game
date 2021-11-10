#game functions

import sys
from bullet import Bullet
from alien import Alien
from ship import Ship
import pygame
from time import sleep

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    #keydown presses
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """start new game when player clicks play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        stats.reset_stats()
        stats.game_active = True

        #reset settings
        ai_settings.initialize_dynamic_settings()

        #hide mouse
        pygame.mouse.set_visible(False)

        #reset scoreboard
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        #empty aliens and bullets
        aliens.empty()
        bullets.empty()

        #create a new fleet and center ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def fire_bullet(ai_settings, screen, ship, bullets):
    """fire bullet if limit not reached"""
    #create new bullet and add it to group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keyup_events(event, ship):
    #keydown presses
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """respond to keypresses and mouse events."""
    #watch keyboard events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    #update bullet pos
    bullets.update()

    #remove old bullets
    for bullet in bullets.copy():
        if bullet.rect.bottom <=0:
            bullets.remove(bullet)
    #check bullets that have hit enemies
    #if hit remove bullet and hit alien
    
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)
    

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullet):
    """respond to bullet alines collsions"""
    #remove any bullets and aliens that have collided
    collisions = pygame.sprite.groupcollide(bullet, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points
            sb.prep_score()
    check_high_score(stats, sb)
    if len(aliens) == 0:
        #destroy current bullets and create new fleet
        bullet.empty()
        ai_settings.increase_speed()

        #increase level
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)

def update_screen(ai_settings, screen, ship, stats, sb, aliens, bullets, play_button):
    """Update images on scrween and flip to new"""
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    sb.show_score()
    #draw play button if game is inactive
    if not stats.game_active:
        play_button.draw_button()

    #make the most recently drawn
    pygame.display.flip()

def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullet):
    """update pos of all aliens in fleet"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    #look for alien player collisions

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullet)

    #look for aliens hitting bottom of the screen
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullet)

def create_fleet(ai_settings, screen, ship, aliens):
    """create full fleet of aliens"""
    #create an alien and find the number of aliens in a  row
    #spacing between each alien is equal to one alien width
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_rows):

        #create the first row
        for alien_number in range(number_aliens_x):
            #create alien and place it in row
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def get_number_rows(ai_settings, ship_height, alien_height):
    """determine the number of rows of aliens"""
    avaiable_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(avaiable_space_y / (2 * alien_height))
    return number_rows

def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """drop entire fleet and change direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullet):
    """respond to ship being hit by alien"""
    if stats.ships_left > 0:
        stats.ships_left -= 1

        #update scoreboard
        sb.prep_ships()

        #empty the lsit of aliens and bullets
        aliens.empty()
        bullet.empty()

        #create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        #pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullet):
    """check if aliens have reachyed the bottom"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #treat this same as if ship got it
            ship_hit(ai_settings, stats, screen, ship, aliens, bullet)
            break

def check_high_score(stats, sb):

    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()