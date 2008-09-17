import pygame

from constants import *

class ScrollButton(pygame.sprite.Sprite):
	def __init__(self, pointUp):
		super(ScrollButton, self).__init__()
		
		self.image = pygame.image.load("data/images/scroll bar arrows.png").convert_alpha()
		self.rect = self.image.get_rect()
		
		if not pointUp:
			self.image = pygame.transform.flip(self.image, False, True)
		
class ScrollBar(pygame.sprite.Sprite):
	def __init__(self, start, end):
		super(ScrollBar, self).__init__()
		
		assert start > end, "ScrollBar assumes we're scrolling up in a coord system where +y is down"
		
		self.image = pygame.image.load("data/images/scroll bar.png").convert_alpha()
		self.rect = self.image.get_rect()
		
		self.start = start
		self.end = end + self.rect.height
		self.rect.bottom = start
	
	def update(self, progress):
		self.rect.bottom = (self.end - self.start) * progress + self.start

class DamageBar(pygame.sprite.Sprite):
    def __init__(self):
        super(DamageBar, self).__init__()
        pygame.font.init()
        
        self.images = [pygame.Surface((160, 64)) for i in range(MAX_HEALTH + 1)]
        i = 0
        for image in self.images:
            image.fill(HUD_BG_COLOR)
		
            f = pygame.font.Font(None, 32)
            image.blit(f.render("Memory Usage:", 1, (255, 0, 0)), (0, 0))
            
            pygame.draw.rect(image, (0, 0, 0), (0, 32, 160, 32))
            pygame.draw.rect(image, (0, 255, 0), (0, 32, int(i * 160.0 / MAX_HEALTH), 32))
			
            i += 1
		
        self.image = self.images[0]
        self.rect = self.image.get_rect()
	
    def update(self, health):
        self.image = self.images[max(0, MAX_HEALTH - health)]

        
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
        txt1 = "Nukes Active"
        self.image = f.render(txt1, 1, (255,0,0))
        self.rect = self.image.get_rect()
        
class Score(pygame.sprite.Sprite):
    def __init__(self, score):
        super(Score,self).__init__()
        pygame.font.init()
        f = pygame.font.Font(None,32)
        txt = "Score: " +str(score)
        self.image = f.render(txt,1,(255,0,0))
        self.rect = self.image.get_rect()
        
    def update(self,score):
        f = pygame.font.Font(None,32)
        txt = "Score: " + str(score)
        self.image = f.render(txt,1,(255,0,0))

class hasCtrl(pygame.sprite.Sprite):
    def __init__(self):
        super(hasCtrl,self).__init__()
        pygame.font.init()
        f = pygame.font.Font(None,32)
        txt = "CTRL"
        self.image = f.render(txt, 1, (255,0,0))
        self.rect = self.image.get_rect()
        
class hasAlt(pygame.sprite.Sprite):
    def __init__(self):
        super(hasAlt,self).__init__()
        pygame.font.init()
        f = pygame.font.Font(None,32)
        txt = "ALT"
        self.image = f.render(txt, 1, (255,0,0))
        self.rect = self.image.get_rect()
        
    
class hasDel(pygame.sprite.Sprite):
    def __init__(self):
        super(hasDel,self).__init__()
        pygame.font.init()
        f = pygame.font.Font(None,32)
        txt = "DEL"
        self.image = f.render(txt, 1, (255,0,0))
        self.rect = self.image.get_rect()
        
    
class invincible(pygame.sprite.Sprite):
    def __init__(self):
        super(invincible, self).__init__()
        pygame.font.init()
        f = pygame.font.Font(None,32)
        txt = "SAFE MODE"
        self.image = f.render(txt,1,(255,0,0))
        self.rect = self.image.get_rect()

class mines(pygame.sprite.Sprite):
    def __init__(self, amt):
        super(mines, self).__init__()
        pygame.font.init()
        f = pygame.font.Font(None, 32)
        txt = "Quarantines: " + str(amt)
        self.image = f.render(txt,1,(255,0,0))
        self.rect = self.image.get_rect()
        
    def update(self, amt):
        f = pygame.font.Font(None,32)
        txt = "Quarantines: " + str(amt)
        self.image = f.render(txt, 1, (255,0,0))

class Hud (object):
	
    def __init__(self):
        #just initialize the group
        super(Hud, self).__init__()
        self.hudElements = pygame.sprite.Group()
	
    def createHudElements(self):
		#initialize everything.
        self.scrollButtonUp = ScrollButton(True)
        self.scrollButtonDown = ScrollButton(False)
        self.scrollButtonUp.rect.topleft = (0, 0)
        self.scrollButtonDown.rect.bottomleft = (0, SCREEN_HEIGHT)
		
        self.scrollbar = ScrollBar(SCREEN_HEIGHT - self.scrollButtonUp.rect.height, self.scrollButtonDown.rect.height)
		
        #initialize the damage bar
        self.damageBar = DamageBar()
        self.damageBar.rect.topleft = (32, 16)
        
        #initialize the box displaying amount of lives
        self.lives = Lives()
        self.lives.rect.topleft = (32, 96)
        
        #initialize the rect displaying amount of mines left
        self.mines = mines(3)
        self.mines.rect.topleft = (32,128)
		
        #initialize the box displaying whether nukes are active or not
        self.destr = Destr()
        self.destr.rect.topleft = (32,160)
        
        #initialize the rect displaying the score
        self.score = Score(0)
        self.score.rect.topleft = (32, 700)
        
        #initialize the rect displaying whether or not Ctrl has been picked up
        self.ctrl = hasCtrl()
        self.ctrl.rect.topleft = (32, 200)
        
        #initialize the rect displaying whether or not Alt has been picked up
        self.alt = hasAlt()
        self.alt.rect.topleft = (32, 230)
        
        #initialize the rect displaying whether or not Del has been picked up
        self.dele = hasDel()
        self.dele.rect.topleft = (32, 260)
        
        #initialize the rect displaying whether or not god mode is active
        self.invincible = invincible()
        self.invincible.rect.topleft = (32, 300)
        
        #add all these elements to the group
        self.hudElements.add(self.scrollButtonUp, self.scrollButtonDown, self.scrollbar, self.damageBar, self.lives, self.score, self.mines)
	
    def update(self, world):
        #update all the elements
        self.scrollbar.update(world.scrollPosition / float(world.endPosition))
        self.damageBar.update(world.player.health)
        self.lives.update(world.player.lives)
        self.score.update(world.score)
        self.mines.update(world.player.mines)
        
        if world.player.hasCtrl:
            self.hudElements.add(self.ctrl)
        else:
            self.hudElements.remove(self.ctrl)
            
        if world.player.hasAlt:
            self.hudElements.add(self.alt)
        else:
            self.hudElements.remove(self.alt)
            
        if world.player.hasDel:
            self.hudElements.add(self.dele)
        else:
            self.hudElements.remove(self.dele)
            
        if world.player.destroyAllEnemies:
            self.hudElements.add(self.destr)
        else:
            self.hudElements.remove(self.destr)
            
        if world.player.invincible:
            self.hudElements.add(self.invincible)
        else:
            self.hudElements.remove(self.invincible)
        
    
    def draw(self, screen, offset):
        pygame.draw.rect(screen, (128, 128, 128), (offset, 0, self.scrollbar.rect.width, SCREEN_HEIGHT))
        for element in self.hudElements:
            screen.blit(element.image, (element.rect.left + offset, element.rect.top))
		
