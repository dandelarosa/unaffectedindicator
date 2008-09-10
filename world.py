import pygame
import random

from entity import Entity
from player import Player
from hud import Hud
from constants import *

class World (object):
	
	def __init__(self):
		super(World, self).__init__()
		
		self.frames = 0
		
		self.playSurface = pygame.Surface((PLAY_WIDTH, SCREEN_HEIGHT))
		self.hudSurface = pygame.Surface((HUD_WIDTH, SCREEN_HEIGHT))

		self.scrollPosition = 0
		self.scrollSpeed = 3
		self.endPosition = 500
		
		self.damage = 0
		
		self.sprites = pygame.sprite.Group()
		self.enemies = pygame.sprite.Group()
	
		self.hud = Hud()
	
	def spawnWorld(self):
		self.player = Player((SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50), None)
		self.sprites.add(self.player)
		
		self.hud.createHudElements()
		
	def spawnEnemy(self):
		enemy = Entity((random.randint(0, PLAY_WIDTH), -50))
		self.sprites.add(enemy)
		self.enemies.add(enemy)
	
	def update(self):
		
		for enemy in self.enemies:
			enemy.rect.move_ip((0, self.scrollSpeed))
			if enemy.rect.top > SCREEN_HEIGHT:
				self.enemies.remove(enemy)
				self.damage += 1
		
		self.sprites.update()
		self.hud.update(self)
		
		if self.frames % 50 == 0:
			self.spawnEnemy()
		
		self.scrollPosition += self.scrollSpeed
		self.scrollPosition = min(self.scrollPosition, self.endPosition)
		
		self.frames += 1
		
	def draw(self, screen):
		self.playSurface.fill((255, 255, 255))
		self.hudSurface.fill((100, 100, 255))
		
		self.sprites.draw(self.playSurface)
		self.hud.draw(self.hudSurface)
		
		for i in range(10):
			pos = (i * 100 + self.scrollPosition) % 1000 - 100
			pygame.draw.circle(self.playSurface, (255,0,0), (50, int(pos)), 20)
		
		screen.blit(self.playSurface, (0, 0))
		screen.blit(self.hudSurface, (PLAY_WIDTH, 0))
		