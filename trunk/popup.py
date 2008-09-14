import pygame, sys, os, random
import entity
from pygame.locals import *


class Popup(entity.Entity):
    def __init__(self):
        position = random.randint(10,450), random.randint(10, 350)
        super(Popup, self).__init__(position, 'popup.bmp')
        self.typeofenemy = "popup"
        
    def update(self):
        super(Popup, self).update()
    

                
    
