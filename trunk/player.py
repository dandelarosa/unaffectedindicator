#!/usr/bin/env python

import pygame, threading
import entity
from pygame.locals import *

class Player(entity.Entity):
        
        def __init__(self,pos,image):
                entity.Entity.__init__(self,pos,image)
                pygame.mouse.set_visible(False)
                self.health = 100
                self.powerup = 0
                self.lives = 3
                self.invincible = False
                
        def set_position(self,pos):
                entity.Entity.set_position(self,pos)
                
        def update(self):
                pos = pygame.mouse.get_pos()
                self.set_position(pos)
        
        def shoot(self):
                print "Bang"
                
        def init_safe_mode(self, time):
                if not self.invincible:
                        self.invincible = True
                        t = threading.Timer(time, self.end_safe_mode)
                        t.start()
                
        def end_safe_mode(self):
                self.invincible = False
        
        def decrease_life(self):
                self.lives -= 1
        
        def increase_health(self, amount):
                self.health += amount
        
        def decrease_health(self, amount):
                if not self.invincible:
                        if (self.health - amount) > 0:
                                self.health -= amount
                        elif (self.health - amount) <= 0:
                                self.decrease_life()
                                self.health = 100

        def increase_powerup(self, amount):
                self.powerup += amount
