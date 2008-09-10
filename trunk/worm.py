
import pygame, sys, os, random
import Entity	
from pygame.locals import *



class Worm(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('worm.bmp', -1)
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.rect.topleft = random.randint(10, 450), 0
		self.movex = 5
		self.movey = 30
		self.lifetime = 1
		
	def update(self):
		self.lifetime+=1
		self._move()
		
		
	def _move(self):
		#move virus down and right and left
		newpos = self.rect.move((self.movex, 0))
		if self.rect.left < self.area.left or self.rect.right > 500:
			self.movex = -self.movex
			newpos = self.rect.move((self.movex, self.movey))
			self.image = pygame.transform.flip(self.image, 1, 0)
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
    
