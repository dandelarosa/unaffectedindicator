#!/usr/bin/env python

import pygame, threading
import entity
from pygame.locals import *

class QuarantineMine(entity.Entity):
	def __init__(self,player,pos):
                self.player = player
                super(QuarantineMine, self).__init__(pos, None)
		t = threading.Timer(5.0, self.explode)
		t.start()
		
	def set_position(self,pos):
		entity.Entity.set_position(self,pos)

	def explode(self):
                self.player.quarantine_explode()
                print "boom"
