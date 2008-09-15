import pygame, sys, os, random
import entity
from pygame.locals import *
from constants import *

"""Popup subclasses entity.  Pops up randomly in the top half of the screen and saps your score for every second it is left alive.  """
class Popup(entity.Entity):
    def __init__(self):
        position = random.randint(10,PLAY_WIDTH - 130), random.randint(10, SCREEN_HEIGHT/2)
        super(Popup, self).__init__(position, 'pop up window '+str(random.randint(1,8)) +'.png')
        self.typeofenemy = "popup"
        self.health = 3
        
    def update(self):
        super(Popup, self).update()
    

                
    
