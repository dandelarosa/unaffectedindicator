#!/usr/bin/env python

import pygame
import entity
from pygame.locals import *

class CtrlAltDel(entity.Entity):
	def __init__(self,pos,image):
		entity.Entity.__init__(self,pos,image)
		
	def set_position(self,pos):
		entity.Entity.set_position(self,pos)

	def on_collision(self, player1):
		print "Ctrl Alt Delete!"
		player1.increase_health(30);
