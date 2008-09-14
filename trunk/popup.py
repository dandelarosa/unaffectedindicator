import pygame, sys, os, random
import entity
from pygame.locals import *

"""Popup subclasses entity.  Pops up randomly in the top half of the screen and saps your score for every second it is left alive.  """
class Popup(entity.Entity):
    def __init__(self):
        position = random.randint(10,399), random.randint(10, 350)
        super(Popup, self).__init__(position, 'pop up window 1.png')
        self.typeofenemy = "popup"
        
    def update(self):
        super(Popup, self).update()
    

                
    