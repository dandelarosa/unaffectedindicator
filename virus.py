
import pygame, sys, os, random
import entity
from pygame.locals import *

	
class Virus(entity.Entity):
    def __init__(self):
        self.typeofenemy = "virus"
        position = random.randint(10,450), 10
        
        super(Virus, self).__init__(position, 'virus.bmp')
        
        self.movex = 0
        self.movey = 4
        

    def update(self):
        super(Virus, self).update()

	
	
