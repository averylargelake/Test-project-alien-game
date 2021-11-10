#Alien invasion

import sys
from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


import pygame
from pygame.sprite import Group

def run_game():
    #init game and create screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alienit tulee!")

    #make play button
    play_button = Button(ai_settings, screen, "Play")

    #create an instance to store game stats
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    #make ship
    ship = Ship(ai_settings, screen)
    #make group for bullets and aliens
    aliens = Group()
    bullets = Group()
    #create a fleet of aliens hhh
    gf.create_fleet(ai_settings, screen, ship, aliens)

    #Main loop
    while True:

        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:

            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets)
            
        gf.update_screen(ai_settings, screen, ship, stats, sb, aliens, bullets, play_button)
    

run_game()