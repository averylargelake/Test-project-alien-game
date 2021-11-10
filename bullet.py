#bullet

import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	"""class to manage bullets"""

	def __init__(self, ai_settings, screen, ship):
		"""create bullet at ships curr pos"""
		super().__init__()
		self.screen = screen

		#create bullet
		self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, 
			ai_settings.bullet_height)
		self.rect.centerx = ship.rect.centerx
		self.rect.top = ship.rect.top

		#store bullet pos
		self.y = float(self.rect.y)

		self.color = ai_settings.bullet_color
		self.speed_factor = ai_settings.bullet_speed_factor

	def update(self):
		#move bullet
		self.y -= self.speed_factor
		#update rect pos
		self.rect.y = self.y

	def draw_bullet(self):
		#draw bullet to screen
		pygame.draw.rect(self.screen, self.color, self.rect)