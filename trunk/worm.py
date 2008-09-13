
import pygame, sys, os, random
import entity	
from pygame.locals import *



class Worm(entity.Entity):
    def __init__(self):
        
        position = random.randint(10,450),10
        
        super(Worm, self).__init__(position, 'worm.bmp')
        self.lifetime = 1
 


    def update(self):
        self.lifetime+=1
        super(Worm, self).update()
     
