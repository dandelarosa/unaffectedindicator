#!/usr/bin/env python

import pygame, threading
import entity
from pygame.locals import *

class QuarantineMine(entity.Entity):
	def __init__(self,pos):
                print "mine set"
                super(QuarantineMine, self).__init__(pos, None)
		t = threading.Timer(5.0, self.explode)
		
	def set_position(self,pos):
		entity.Entity.set_position(self,pos)

	def explode(self):
                print "boom"
