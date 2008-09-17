import pygame, threading

from playerBullet import PlayerBullet
from quarantineMine import QuarantineMine
import entity
from animation import Animation, ColorFadeAnimation
from constants import *

class Player(entity.Entity):
    
    def __init__(self, world, pos):
        self.bullets = []
        self.respawnPos = pos
        self.gameWorld = world
        
        self.safeModeTime = 5
        anims = {
            'idle': Animation("player icon.png", 32), 
            'shoot': Animation("fire.png", 32, 2, False),
            'death': Animation("player death.png", 32, 2, False),
            'revive': Animation("player revive.png", 32, 3, False),
            'respawn': Animation("respawn.png", 32, 3, False),
            'safemode': ColorFadeAnimation("player icon.png", 32, (self.safeModeTime*2)*32, (0, 255, 0, 0))
            }
        
        super(Player, self).__init__(pos, anims, 'idle')
        
        pygame.mouse.set_visible(False)
        
        self.health = MAX_HEALTH
        self.powerup = 0
        self.lives = 3
        self.mines = 3
        self.hasCtrl = False
        self.hasAlt = False
        self.hasDel = False
        self.invincible = False
        self.destroyAllEnemies = False
        
        
    def update(self):
        super(Player, self).update()
        
        if self.animName == 'death':
            if self.anim.done:
                self.changeAnimation('respawn')
                self.set_position(self.respawnPos)
                
        elif self.animName == 'respawn':
            if self.anim.done:
                self.changeAnimation('revive')
        
        elif self.animName == 'revive':
            if self.anim.done:
                self.changeAnimation('idle')
                self.end_safe_mode()
                pygame.mouse.set_pos(self.respawnPos)
        
        else:
            if self.anim.done and self.animName == 'shoot':
                self.changeAnimation('idle')

            mousepos = list(pygame.mouse.get_pos())
            mousepos[0] = min(PLAY_WIDTH - self.rect.height / 2, max(self.rect.width / 2, mousepos[0]))
            mousepos[1] = min(SCREEN_HEIGHT - self.rect.height / 2, max(self.rect.height / 2, mousepos[1]))
            
            self.set_position(mousepos)
        
    def shoot(self, bullets):
        if self.animName == 'idle' or self.animName == 'shoot':
            b = PlayerBullet(self.rect.center)
            self.bullets.append(b)
            bullets.add(b)
            
            self.changeAnimation('shoot')
            
            sound = pygame.mixer.Sound("data/sounds/shoot.wav")
            sound.set_volume(.25)
            sound.play()

    def collected_ctrlAltDel(self, cadId):
        if cadId is 1:
            self.hasCtrl = True
        elif cadId is 2:
            self.hasAlt = True
        elif cadId is 3:
            self.hasDel = True
        
    def init_safe_mode(self, time):
        self.safeModeTime = time
        if not self.invincible:
            self.changeAnimation('safemode')
            self.invincible = True
            t = threading.Timer(time, self.end_safe_mode)
            t.start()
        
    def end_safe_mode(self):
        self.invincible = False
        self.changeAnimation('idle')
    
    def decrease_life(self):
        self.lives -= 1
        self.dying = True
        self.changeAnimation('death')        
        self.init_safe_mode(10.0)
        
        sound = pygame.mixer.Sound("data/sounds/xplosion1.wav")
        sound.play()
    
    def increase_health(self, amount):
        self.health += amount
    
    def decrease_health(self, amount):
        if not self.invincible:
            if (self.health - amount) > 0:
                self.health -= amount
            elif (self.health - amount) <= 0:
                self.decrease_life()
                self.health = MAX_HEALTH

    def increase_powerup(self, amount):
        self.powerup += amount
        if self.powerup is 100:
            self.destroyAllEnemies = True

    def quarantine(self, mines):
        if self.mines > 0:
            mine = QuarantineMine(pygame.mouse.get_pos())
            mines.add(mine)
            self.mines -= 1


    def after_destroy_all(self):
        self.powerup = 0
        self.destroyAllEnemies = False
        
