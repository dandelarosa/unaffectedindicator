import pygame

class World (object):
	
	def __init__(self):
		super(World, self).__init__()
		
		self.sprites = pygame.sprite.Group()
		
		self.scrollPosition = 0
		self.scrollSpeed = 2.5
	
	def update(self):
		self.scrollPosition += self.scrollSpeed
		self.sprites.update()
		
		
	def draw(self, screen):
		self.sprites.draw(screen)
		
		#for pos in [x + self.scrollPosition % 600 for x in range(-100, 600) if x % 100 == 0]:
		for i in range(8):
			pos = (i * 100 + self.scrollPosition) % 800 - 100
			pygame.draw.circle(screen, (255,0,0), (50, pos), 20)
		
