import pygame
import random

from entity import Entity

SCREEN_WIDTH = 700
PLAY_WIDTH = 500
HUD_WIDTH = 200
SCREEN_HEIGHT = 768
		
class World (object):
	
	def __init__(self):
		super(World, self).__init__()
		
		self.frames = 0

		self.scrollPosition = 0
		self.scrollSpeed = 3
		
		self.sprites = pygame.sprite.Group()
		self.enemies = pygame.sprite.Group()
	
	def spawnWorld(self):
		self.player = Entity((SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50))
		self.sprites.add(self.player)
		
	def spawnEnemy(self):
		enemy = Entity((random.randint(0, PLAY_WIDTH), -50))
		self.sprites.add(enemy)
		self.enemies.add(enemy)
	
	def update(self):
		self.scrollPosition += self.scrollSpeed
		
		for enemy in self.enemies:
			enemy.rect.move_ip((0, self.scrollSpeed))
		
		self.sprites.update()
		
		if self.frames % 50 == 0:
			self.spawnEnemy()
		
		self.frames += 1
		
	def draw(self, screen):
		self.sprites.draw(screen)
		
		for i in range(10):
			pos = (i * 100 + self.scrollPosition) % 1000 - 100
			pygame.draw.circle(screen, (255,0,0), (50, int(pos)), 20)
		
