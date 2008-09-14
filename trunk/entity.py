#!/usr/bin/env python

import pygame
from pygame.locals import *
import math

"""Entity subclasses sprite.  It takes care of movement of all the enemies"""
class Entity(pygame.sprite.Sprite):

    def __init__(self, position = (0, 0), imageFilename = None, frameWidth = 0, frameRate = 1):
        super(Entity, self).__init__()
        self.typed = imageFilename
        self.frame = 0
        self.frameRate = frameRate
        if imageFilename == 'virus.png':
            #virus moves in the downward direction only 
            self.movex = 0
            self.movey = 4
        elif imageFilename == 'worm.bmp':
            #worms move to the right and left, then jump down when it hits an edge
            self.movex = 5
            self.movey = 0
        else:
            #nothing else moves.
            self.movex = 0
            self.movey = 0
        if imageFilename is None:
            self.image = pygame.Surface((32, 32))
            color = (100, 100, 100)
            self.image.fill(color)
            self.rect = self.image.get_rect()
            self.images = [self.image]
            
        else:
            #load the image
            self.imageStrip = pygame.image.load('data/images/' + imageFilename).convert()
            self.rectStrip = self.imageStrip.get_rect()
            self.images = []
            
            if frameWidth == 0:
                frameWidth = self.rectStrip.width
            
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
        newpos = self.rect.move((self.movex, self.movey))
        #moves to the left and the right the correct amount, as given above.
        if self.rect.left < 0 or self.rect.right > 500:
            #if the resulting frame is off the board, switch it into the other direction!
            self.movex = -self.movex
            newpos = self.rect.move((self.movex, 30))
            self.image = pygame.transform.flip(self.image, 1, 0)
        self.rect = newpos

    def set_position(self, pos):
        self.rect.center = pos

