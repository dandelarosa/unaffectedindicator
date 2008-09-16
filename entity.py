import pygame
from pygame.locals import *
import math

import animation
from constants import *
            
"""Entity subclasses sprite.  It takes care of movement of all the enemies"""
class Entity(pygame.sprite.Sprite):

    def __init__(self, position = (0, 0), animations = {'default': animation.Animation()}, startAnim = 'default'):
        super(Entity, self).__init__()
        
        self.animations = animations
        self.animName = startAnim
        self.anim = self.animations[self.animName]
        self.image = self.anim.image
        self.rect = self.anim.rect
        
        self.rect.center = position
        self.movex = 0
        self.movey = 0
        self.frame = 0
    
    def update(self):
        self.anim.update()
        self.rect.move_ip((self.movex, self.movey))
        self.frame += 1
    
    def draw(self, screen):
        screen.blit(self.image, self.rect, self.anim.animRect)
        
    def changeAnimation(self, animName):
        self.anim.reset()
        self.animName = animName
        self.anim = self.animations[self.animName]
        self.image = self.anim.image
        self.rect = Rect(self.rect.topleft, self.anim.rect.size)
        self.animRect = self.anim.animRect

    def set_position(self, pos):
        self.rect.center = pos


# Entity with no animations (for convenience)
class StaticEntity(Entity):
    def __init__(self, position=(0,0), imageFile = None):
        anims = {'default': animation.Animation(imageFile)}
        super(StaticEntity, self).__init__(position, anims)

