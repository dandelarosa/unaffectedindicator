#!/usr/bin/env python
"""
sup.
"""



import pygame, sys, os, random
from pygame.locals import *


#class Enemy(pygame.sprite.Sprite):
	
	
class Virus(pygame.sprite.Sprite):
	def __init__(self):
		#image, rect, move
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('virus.bmp', -1)
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.rect.topleft = random.randint(10,630) , 10
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
	
	

class Worm(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('worm.bmp', -1)
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.rect.topleft = random.randint(10, 600), 0
		self.movex = 5
		self.movey = 30
		self.lifetime = 1
		
	def update(self):
		self.lifetime+=1
		self._move()
		
		
	def _move(self):
		#move virus down and right and left
		newpos = self.rect.move((self.movex, 0))
		if self.rect.left < self.area.left or self.rect.right > self.area.right:
			self.movex = -self.movex
			newpos = self.rect.move((self.movex, self.movey))
			self.image = pygame.transform.flip(self.image, 1, 0)
		self.rect = newpos
	

class Popup(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('popup.bmp', -1)
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.rect.topleft = random.randint(10, 630), random.randint(10, 280)
		self.lifetime = 1
		
	def update(self):
		self.lifetime+=1
		if (self.lifetime < 30):
			#need to still display pop up animation
			print "popping up"
			
		
		

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
    
    
def main():
	counter = 0
	pygame.init()
	
	screen = pygame.display.set_mode((640,480))
	clock = pygame.time.Clock()
	
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((255,255,255))
	
	screen.blit(background, (0,0))
	pygame.display.flip()
	
	
	virus = Virus()
	worm = Worm()
	sprites = pygame.sprite.RenderPlain((virus, worm))
	
	#print sprites
	
	while 1:
		clock.tick(30)
		counter +=1
		for e in pygame.event.get():
			if e.type == KEYDOWN and e.key == K_ESCAPE:
				return
		#	elif e.type == KEYDOWN and e.key == K_a:
		if counter % 35 == 0:
			sprites.add(Virus())
		if counter % 500 == 0:
			sprites.add(Worm())
			
		if counter % 80 == 0:
			sprites.add(Popup())
		
		sprites.update()
		
		screen.blit(background, (0,0))
		sprites.draw(screen)
		pygame.display.flip()
		
	return
	
if __name__ == '__main__': main()
