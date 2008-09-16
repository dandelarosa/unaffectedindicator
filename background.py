import pygame, random

import entity
from constants import *

class Bkg(entity.Entity):
    def __init__(self):
    
        imageFilename = random.choice(BACKGROUND_IMAGE_FILES)
        position = (random.randint(10,PLAY_WIDTH-32), -32)
        super(Bkg, self).__init__(position, imageFilename)
        
        fade = pygame.Surface(self.rect.size)
        fade.fill(PLAY_BG_COLOR)
        fade.set_alpha(128)
        self.image.blit(fade, (0, 0))
        
        self.movey = 2

