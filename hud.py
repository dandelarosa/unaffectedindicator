import pygame

class ScrollButton(pygame.sprite.Sprite):
	def __init__(self, pointUp):
		super(ScrollButton, self).__init__()
		
		self.image = pygame.Surface((32, 32))
		self.image.fill((128, 128, 128))
		self.rect = self.image.get_rect()
		pygame.draw.rect(self.image, (0, 0, 0), self.rect, 3)
		
		if not pointUp:
			self.image = pygame.transform.flip(self.image, False, True)
		
class ScrollBar(pygame.sprite.Sprite):
	def __init__(self, start, end):
		super(ScrollBar, self).__init__()
		
		assert start > end, "ScrollBar assumes we're scrolling up in a coord system where +y is down"
		
		self.image = pygame.Surface((32, 64))
		self.image.fill((128, 128, 128))
		self.rect = self.image.get_rect()
		pygame.draw.rect(self.image, (0, 0, 0), self.rect, 3)
		
		self.start = start
		self.end = end + self.rect.height
		self.rect.bottom = start
	
	def update(self, progress):
		self.rect.bottom = (self.end - self.start) * progress + self.start
		

class Hud (object):
	
	def __init__(self, world):
		super(Hud, self).__init__()
		
		self.world = world
		self.hudElements = pygame.sprite.Group()
	
	def createHudElements(self):
		
		self.scrollButtonUp = ScrollButton(True)
		self.scrollButtonDown = ScrollButton(False)
		self.scrollButtonUp.rect.topleft = (0, 0)
		self.scrollButtonDown.rect.bottomleft = (0, 768)
		
		self.scrollbar = ScrollBar(768 - self.scrollButtonUp.rect.height, self.scrollButtonDown.rect.height)
		
		self.hudElements.add(self.scrollButtonUp, self.scrollButtonDown, self.scrollbar)
	
	def update(self):
		self.scrollbar.update(self.world.scrollPosition / float(self.world.endPosition))
		print "pos ", self.world.scrollPosition, "scroll bar at ", self.scrollbar.rect.bottom
	
	def draw(self, screen):
		self.hudElements.draw(screen)
		
