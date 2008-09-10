#!/usr/bin/env python

import pygame, random
import entity
from pygame.locals import *

class CtrlAltDel(entity.Entity):
	def __init__(self,pos,image):
                self.id = random.randint(1, 3)
		entity.Entity.__init__(self,pos,image)
		
	def set_position(self,pos):
		entity.Entity.set_position(self,pos)

	def on_collision(self, player1):
		player1.collected_ctrlAltDel(self.id);
