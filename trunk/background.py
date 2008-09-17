import pygame, random

import entity
from constants import *

class Bkg(entity.StaticEntity):
    def __init__(self):
    
        imageFilename = random.choice(BACKGROUND_IMAGE_FILES)
        position = (random.randint(1, PLAY_WIDTH / 64) * 64, -64)
        
        super(Bkg, self).__init__(position, imageFilename)
        
        fade = pygame.Surface(self.rect.size)
        fade.fill(PLAY_BG_COLOR)
        fade.set_alpha(196)
        self.image.blit(fade, (0, 0))
        
        self.movey = 2

