
import pygame, sys, os, random
import entity
from pygame.locals import *

	
class Virus(entity.Entity):
    def __init__(self):
        
        position = random.randint(10,450), 10
        
        super(Virus, self).__init__(position, 'virus.bmp')
        self.lifetime = 1
        self.move = 5
        

    def update(self):
        super(Virus, self).update()
       # self._fall()
        self.lifetime+=1
	
    def _fall(self):
		#move the virus down
        newpos = self.rect.move((0,self.move))
        self.rect = newpos
	
	
