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
        self.animFrame = 0
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
            
        self.loadAnimation(imageFilename, frameWidth)
        self.rect.topleft = position
    
    def loadAnimation(self, imageFilename = None, frameWidth = 0):
        if imageFilename is None:
            self.image = pygame.Surface((32, 32))
            color = (100, 100, 100)
            self.image.fill(color)
            self.rect = self.image.get_rect()
            self.animRects = [self.rect]
            
        else:
            #load the image
            self.image = pygame.image.load('data/images/' + imageFilename).convert_alpha()
            rectStrip = self.image.get_rect()
            
            if frameWidth == 0:
                frameWidth = rectStrip.width
            
            self.animRects = []
            for i in range(rectStrip.width / frameWidth):
                self.animRects.append(pygame.Rect(i * frameWidth, 0, frameWidth, rectStrip.height))
            
            self.animRect = self.animRects[0]
            self.rect = Rect(0, 0, self.animRect.width, self.animRect.height)
            
    
    def update(self):
        self.animRect = self.animRects[self.animFrame]
        self.frame += 1
        if self.frame % self.frameRate == 0:
            self.animFrame += 1
            self.animFrame %= len(self.animRects)
            
        newpos = self.rect.move((self.movex, self.movey))
        #moves to the left and the right the correct amount, as given above.
        if self.rect.left < 0 or self.rect.right > 500:
            #if the resulting frame is off the board, switch it into the other direction!
            self.movex = -self.movex
            newpos = self.rect.move((self.movex, 30))
            self.image = pygame.transform.flip(self.image, 1, 0)
        self.rect = newpos
    
    def draw(self, screen):
        screen.blit(self.image, self.rect, self.animRect)

    def set_position(self, pos):
        self.rect.center = pos

