import pygame, sys, os, random
import entity
from pygame.locals import *


class Popup(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('images/popup.bmp', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = random.randint(10, 450), random.randint(10, 280)
        self.lifetime = 1
		
    def update(self):
        self.lifetime+=1
       # if (self.lifetime < 30):
            #need to still display pop up animation
          #      print "popping up"


    def destroy(self):
        del self
                
                
                
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()
    
