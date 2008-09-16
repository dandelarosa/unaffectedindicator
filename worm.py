import pygame, sys, os, random
from pygame.locals import *

import entity
from constants import *

"""class Worm subclasses entity.  Position starts randomly across the top of the screen, moves to the left until it hits the edge of the game scren, falls down a little, then moves to the right. Back and forth."""
class Worm(entity.Entity):
    def __init__(self, position, image):
        self.typeofenemy = "worm"
        
        super(Worm, self).__init__(position, image)
        self.health = 2
        self.movex = 5
        self.movey = 0

    def update(self):
        super(Worm, self).update()
        if self.rect.left < 0 or self.rect.right > PLAY_WIDTH:
            self.movex = -self.movex
            self.rect.move_ip((self.movex, 30))
     
