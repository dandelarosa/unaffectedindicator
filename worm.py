import pygame

import enemy
from animation import Animation
from constants import *

"""class Worm subclasses entity.  Position starts randomly across the top of the screen, moves to the left until it hits the edge of the game scren, falls down a little, then moves to the right. Back and forth."""
class Worm(enemy.Enemy):
    def __init__(self, position, subtype):
        
        imageName = "worm " + subtype + ".png"
        deathImageName = "worm " + subtype + " death.png"
        anims = {'idle': Animation(imageName), 'death': Animation(deathImageName, 32, 1, False)}
        
        super(Worm, self).__init__("worm", position, anims, 'idle')
        
        self.health = 2
        self.movex = 5
        self.movey = 0

    def update(self):
        super(Worm, self).update()
        if self.rect.left < 0 or self.rect.right > PLAY_WIDTH:
            self.movex = -self.movex
            self.rect.move_ip((self.movex, 30))
     
