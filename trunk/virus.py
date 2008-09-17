import pygame, random

import enemy
from animation import Animation
from constants import *

"""Virus subclass of entity.  Starts at random position across the top and falls down."""
class Virus(enemy.Enemy):
    def __init__(self):
        
        position = random.randint(10,PLAY_WIDTH - 40), 10
        anims = {
            'idle': Animation("virus.png"),
            'death': Animation("virus death.png", 32, 2, False)
            }
        
        super(Virus, self).__init__('virus', position, anims, 'idle')
        
        self.health = 1
        self.movex = 0
        self.movey = 4
        

    def update(self):
        super(Virus, self).update()

	
	
