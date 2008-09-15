#!/usr/bin/env python

import pygame, threading
import entity
from pygame.locals import *

class QuarantineMine(entity.Entity):
    def __init__(self,player,pos):
        self.player = player
        self.position = pos
        super(QuarantineMine, self).__init__(pos, 'quarintine mine.png')
        t = threading.Timer(5.0, self.explode)
        t.start()

    def set_position(self,pos):
        entity.Entity.set_position(self,pos)

    def explode(self):
        self.rect = self.rect.inflate(100, 100)
        self.player.quarantine_explode()
        print "boom"
