#!/usr/bin/env python

import pygame
from entity import Entity
from pygame.locals import *

class PlayerBullet(Entity):
    def __init__(self, pos):
        self.position = pos
        super(PlayerBullet, self).__init__(pos, None)
        
    def set_position(self,pos):
        Entity.set_position(self,pos)

    def update(self):
        self.position = (self.position[0], self.position[1] - 8)
        self.set_position(self.position)