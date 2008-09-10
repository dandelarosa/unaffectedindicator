#!/usr/bin/env python

import pygame
import entity, player
from pygame.locals import *

class SafeMode(entity.Entity):
	def __init__(self,pos,image):
		entity.Entity.__init__(self,pos,image)
		
	def set_position(self,pos):
		entity.Entity.set_position(self,pos)
		
	def on_collision(self, player1):
		print "Safe Mode!"
		player1.init_safe_mode(5.0);
		
