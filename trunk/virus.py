
import pygame, sys, os, random
import entity
from pygame.locals import *

	
class Virus(pygame.sprite.Sprite):
	def __init__(self):
		#image, rect, move
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('virus.bmp', -1)
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.rect.topleft = random.randint(10,490) , 10
		self.move = 4
		self.lifetime = 1
	
	def update(self):
		self._fall()
		self.lifetime+=1
	
	def _fall(self):
		#move the virus down
		newpos = self.rect.move((0,self.move))
		#if self.rect.bottom > 480:
			##NEED TO ADD AMOUNT to CPU USAGE
			
		self.rect = newpos
	
	
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
    
