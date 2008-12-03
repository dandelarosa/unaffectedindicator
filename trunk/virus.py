import pygame, random

import enemy
from animation import Animation
from world import *
from constants import *

"""Virus subclass of entity.  Starts at random position across the top and falls down."""
class Virus(enemy.Enemy):
    def __init__(self, position = 0, imagename = "virus.png"):
        
        if position is 0:
            position = random.randint(10,PLAY_WIDTH - 40), 10
        
        anims = {
            'idle': Animation(imagename),
            'death': Animation("virus death.png", 32, 2, False)
            }
        
        super(Virus, self).__init__('virus', position, anims, 'idle')
        
        self.health = 1
        self.movex = 0
        self.movey = 4

    def update(self):
        super(Virus, self).update()

class DoubleVirus(Virus):
    def __init__(self, world, position = 0, imagename = "doublevirus.png"):
        self.world = world
        if position is 0:
            position = random.randint(10,PLAY_WIDTH - 40), 10
        super(DoubleVirus, self).__init__(position, imagename)
        self.movey = 1.5
        
    def update(self):
        super(DoubleVirus, self).update()
        
    def takeHit(self, damage):
        super(DoubleVirus, self).takeHit(damage)
        if self.dead:
            self.world.spawnVirus((self.rect.center[0] - 25, self.rect.center[1] -10))
            self.world.spawnVirus((self.rect.center[0] + 25, self.rect.center[1] -10))
            
class TripleVirus(Virus):
    def __init__(self, world, imagename = "triplevirus.png"):
        self.world = world
        super(TripleVirus, self).__init__(0, imagename)
        self.movey = 1
        
    def update(self):
        super(TripleVirus, self).update()
        
    def takeHit(self, damage):
        super(TripleVirus, self).takeHit(damage)
        if self.dead:
            self.world.spawnDoubleVirus((self.rect.center[0] - 25, self.rect.center[1] -10))
            self.world.spawnDoubleVirus((self.rect.center[0] + 25, self.rect.center[1] -10))
