import pygame, sys, os, random
import entity
from pygame.locals import *


class Popup(entity.Entity):
    def __init__(self):
        position = random.randint(10,450), random.randint(10, 350)
        super(Popup, self).__init__(position, 'popup.bmp')
        self.lifetime = 1
		
    def update(self):
        super(Popup, self).update()
        self.lifetime += 1
    
    def collideWithPlayer(self, player):
        self.destroy()


    def destroy(self):
        del self
                
    
