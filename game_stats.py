class GameStats():

	"""track statistisc for Alien Invasion"""

	def __init__(self, ai_settings):
		"""init statistics"""
		self.ai_settings = ai_settings
		self.reset_stats()
		#start in inactive state
		self.game_active = False
		self.high_score = 0
		self.level = 1


	def reset_stats(self):
		"""init stats that can change during the game"""
		self.ships_left = self.ai_settings.ship_limit
		self.score = 0