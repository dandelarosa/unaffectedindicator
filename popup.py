import pygame, random

import enemy
from animation import Animation, ResizeAnimation
from constants import *

"""Popup subclasses entity.  Pops up randomly in the top half of the screen and saps your score for every second it is left alive.  """
class Popup(enemy.Enemy):
    def __init__(self):
    
        position = random.randint(10, PLAY_WIDTH - 130), random.randint(10, SCREEN_HEIGHT/2)
        imageFile = 'pop up window ' + str(random.randint(1,8)) + '.png'
        anims = {
            'idle': Animation(imageFile),
            'spawn': ResizeAnimation(imageFile, 30, (0, 0), (1, 1)),
            'death': ResizeAnimation(imageFile, 10, (1, 1), (0, 0))
            }
        
        super(Popup, self).__init__('popup', position, anims, 'spawn')
        
        self.health = 3
        
    def update(self):
        super(Popup, self).update()
        
        if self.animName == 'spawn' and self.anim.done:
            self.changeAnimation('idle')
    

                
    
