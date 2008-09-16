import pygame, random

import enemy
from animation import Animation
from constants import *

"""Popup subclasses entity.  Pops up randomly in the top half of the screen and saps your score for every second it is left alive.  """
class Popup(enemy.Enemy):
    def __init__(self):
    
        position = random.randint(10, PLAY_WIDTH - 130), random.randint(10, SCREEN_HEIGHT/2)
        imageFile = 'pop up window ' + str(random.randint(1,8)) + '.png'
        anims = {'idle': Animation(imageFile), 'death': Animation(imageFile, loops=False)}
        
        super(Popup, self).__init__('popup', position, anims, 'idle')
        
        self.health = 3
        
    def update(self):
        super(Popup, self).update()
    

                
    
