import pygame, sys, os, random
import entity
from pygame.locals import *


class Popup(entity.Entity):
    def __init__(self, position):
        super(Popup, self).__init__(position, 'popup.gif')
        self.lifetime = 1
		
    def update(self):
        super(Popup, self).update()
        self.lifetime += 1
    
    def collideWithPlayer(self, player):
        self.destroy()


    def destroy(self):
        del self
                
    
