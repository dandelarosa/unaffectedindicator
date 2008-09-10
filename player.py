#!/usr/bin/env python

import pygame, threading
import entity
from pygame.locals import *

class Player(entity.Entity):
    
    def __init__(self, pos):
        entity.Entity.__init__(self, pos, "data/images/down.png", 50, 10)
        pygame.mouse.set_visible(False)
        self.health = 100
        self.powerup = 0
        self.lives = 3
        self.hasCtrl = False
        self.hasAlt = False
        self.hasDel = False
        self.invincible = False
        
    def set_position(self,pos):
        entity.Entity.set_position(self,pos)
        
    def update(self):
        super(Player, self).update()
        pos = pygame.mouse.get_pos()
        self.set_position(pos)
    
    def shoot(self):
        print "Bang"

    def collected_ctrlAltDel(self, cadId):
        if cadId is 1:
            self.hasCtrl = True
        elif cadId is 2:
            self.hasAlt = True
        elif cadId is 3:
            self.hasDel = True
        if self.hasCtrl and self.hasAlt and self.hasDel:
            self.increase_health(50)
        
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
