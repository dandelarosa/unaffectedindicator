import pygame

from constants import *

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

class DamageBar(pygame.sprite.Sprite):
	def __init__(self):
		super(DamageBar, self).__init__()
		
		self.images = [pygame.Surface((128, 32)) for i in range(MAX_DAMAGE + 1)]
		i = 0
		for image in self.images:
			image.fill((0,0,0))
			pygame.draw.rect(image, (0, 255, 0), (0, 0, int(i * 128.0 / MAX_DAMAGE), 32))
			i += 1
		
		self.image = self.images[0]
		self.rect = self.image.get_rect()
	
	def update(self, damage):
		self.image = self.images[min(MAX_DAMAGE, damage)]

        
class Lives(pygame.sprite.Sprite):
    def __init__(self):
        super(Lives,self).__init__()
        pygame.font.init()
        f = pygame.font.Font(None, 32)
        lvr = "Lives: "
        self.image = f.render(lvr, 1, (255,0,0))

        self.rect = self.image.get_rect()
        
    def update(self, lives):
        f = pygame.font.Font(None, 32)
        lnr = "Lives: " + str(lives)
        self.image = f.render(lnr, 1, (255,0,0))
        #nothing
        
class Destr(pygame.sprite.Sprite):
    def __init__(self):
        super(Destr, self).__init__()
        pygame.font.init()
        f = pygame.font.Font(None, 32)

        
    def update(self):
        
        f = pygame.font.Font(None, 32)
        txt1 = "Nukes Active"
        self.image = f.render(txt1, 1, (255,0,0))
        self.rect = self.image.get_rect()


class Hud (object):
	
    def __init__(self):
        super(Hud, self).__init__()
        self.hudElements = pygame.sprite.Group()
	
    def createHudElements(self):
		
        self.scrollButtonUp = ScrollButton(True)
        self.scrollButtonDown = ScrollButton(False)
        self.scrollButtonUp.rect.topleft = (0, 0)
        self.scrollButtonDown.rect.bottomleft = (0, SCREEN_HEIGHT)
		
        self.scrollbar = ScrollBar(SCREEN_HEIGHT - self.scrollButtonUp.rect.height, self.scrollButtonDown.rect.height)
		
        self.damageBar = DamageBar()
        self.damageBar.rect.topleft = (48, 0)
        
        self.lives = Lives()
        self.lives.rect.topleft = (48,40)
		
        self.destr = Destr()
        
        self.hudElements.add(self.scrollButtonUp, self.scrollButtonDown, self.scrollbar, self.damageBar, self.lives)
	
    def update(self, world):
        self.scrollbar.update(world.scrollPosition / float(world.endPosition))
        self.damageBar.update(world.damage)
        self.lives.update(world.lives)
        if world.player.destroyAllEnemies:
            self.destr.update()
            self.destr.rect.topleft = (48,80)
            self.hudElements.add(self.destr)
            
    def undestr(self, world):
        if world.player.destroyAllEnemies == False:
            self.hudElements.remove(self.destr)
            

	

    
    def draw(self, screen):
        self.hudElements.draw(screen)
		
