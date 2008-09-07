#!/usr/bin/env python

import pygame
from pygame.locals import *

class Entity(pygame.sprite.Sprite):
	def __init__(self,image):
		pygame.sprite.Sprite.__init__(self)
		if image is None:
			self.image = pygame.Surface([32, 32])
			color = (100, 100, 100)
			self.image.fill(color)
		else:
			self.image = image
			
		self.rect = self.image.get_rect()
	
	def set_position(self,pos):
		self.rect.move_ip(pos)
		self.rect.center = pos