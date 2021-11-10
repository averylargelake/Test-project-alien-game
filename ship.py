#ship

import pygame
from pygame.sprite import Sprite

class Ship(Sprite):


	def __init__(self, ai_settings, screen,):
		"""init the ship and start pos"""

		super(Ship, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings

		#load ship and get rect
		self.image = pygame.image.load("images/ship.bmp")
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()

		#start new ship at bot
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom

		#store decimal value for ship center
		self.center = float(self.rect.centerx)

		#move flags
		self.moving_right = False
		self.moving_left = False

	def update(self):
		#update pos according to flag
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.center += self.ai_settings.ship_speed_factor
		if self.moving_left and self.rect.left > 0:
			self.center -= self.ai_settings.ship_speed_factor

		self.rect.centerx = self.center

	def blitme(self):
		#draw ship
		self.screen.blit(self.image, self.rect)

	def center_ship(self):
		self.center = self.screen_rect.centerx