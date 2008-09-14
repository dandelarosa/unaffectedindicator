
import pygame, sys, os, random
import entity	
from pygame.locals import *



class Worm(entity.Entity):
    def __init__(self):
        self.typeofenemy = "worm"
        position = random.randint(10,450),10
        
        super(Worm, self).__init__(position, 'worm.bmp')
        
        self.movex = 5
        self.movey = 0
 


    def update(self):
        super(Worm, self).update()
     
