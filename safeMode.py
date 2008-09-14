#!/usr/bin/env python

import pygame, random
import entity, player
from pygame.locals import *

class SafeMode(entity.Entity):
    def __init__(self):
        pos = random.randint(10,450),random.randint(10,450)
        image = "shield.png"
        entity.Entity.__init__(self,pos,image)
        self.typeofenemy = "cad"

    def set_position(self,pos):
        entity.Entity.set_position(self,pos)
        
    def update(self):
        super(SafeMode,self).update()
        
    def on_collision(self, player1):
        print "Safe Mode!"
        player1.init_safe_mode(5.0);
		
