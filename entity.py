#!/usr/bin/env python

import pygame
from pygame.locals import *
import math

class Entity(pygame.sprite.Sprite):

    def __init__(self, position = (0, 0), imageFilename = None, frameWidth = 0, frameRate = 1):
        super(Entity, self).__init__()
        
        self.frame = 0
        self.frameRate = frameRate
        
        if imageFilename is None:
            self.image = pygame.Surface((32, 32))
            color = (100, 100, 100)
            self.image.fill(color)
            self.rect = self.image.get_rect()
            self.images = [self.image]
            
        else:
            self.imageStrip = pygame.image.load(imageFilename).convert()
            self.rectStrip = self.imageStrip.get_rect()
            self.images = []
            for i in range(self.rectStrip.width / frameWidth):
                image = pygame.Surface((frameWidth, self.rectStrip.height))
                image.blit(self.imageStrip, (0, 0), (i * frameWidth, 0, frameWidth, self.rectStrip.height))
                self.images.append(image)
                
            self.image = self.images[0]
            self.rect = self.image.get_rect()
                
        self.rect.topleft = position
    
    def update(self):
        self.image = self.images[(self.frame / self.frameRate) % len(self.images)]
        self.frame += 1
    
    def set_position(self, pos):
        self.rect.center = pos

