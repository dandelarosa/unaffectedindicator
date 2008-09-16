import pygame
import random
import sys

from ctrlAltDel import *
from virus import Virus
from popup import Popup
from worm import Worm
from entity import Entity
from player import Player
from hud import Hud
from boss1 import Boss
from safeMode import SafeMode
from background import Bkg
from constants import *

class World (object):
    
    def __init__(self):
        super(World, self).__init__()

        self.frames = 1

        self.scrollPosition = 0
        self.scrollSpeed = 3
        self.endPosition = FRAMES_UNTIL_BOSS * self.scrollSpeed
        
        self.bossMode = False

        self.damage = 0
        self.lives = 3
        self.score = 0

        self.playerGroup = pygame.sprite.GroupSingle()
        self.enemies = pygame.sprite.Group()
        self.pickups = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.mines = pygame.sprite.Group()
        self.backgrounds = pygame.sprite.Group()
        
        # sprite groups listed in draw order (lowest sprite get drawn first)
        self.spriteGroups = [self.backgrounds, self.mines, self.pickups, self.bullets, self.enemies, self.playerGroup]
        
        self.hud = Hud()

        self.music = pygame.mixer.Sound("data/music/Main.wav")
        self.music.play()
        
    def spawnWorld(self):
        self.player = Player(self, (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50))
        self.playerGroup.add(self.player)

        self.hud.createHudElements()
        self.frames = 1

        self.scrollPosition = 0
        self.scrollSpeed = 3


    def spawnBkg(self):
        bkg = Bkg()
        self.backgrounds.add(bkg)
        
    def spawnCtrl(self):
        ctrl = Ctrl()
        self.pickups.add(ctrl)
        
    def spawnAlt(self):
        alt = Alt()
        self.pickups.add(alt)
    
    def spawnDel(self):
        d = Del()
        self.pickups.add(d)
        
    def spawnVirus(self):
        enemy = Virus()
        self.enemies.add(enemy)

    def spawnWorm(self):
        position1 = random.randint(165,PLAY_WIDTH-50)
        position2 = 10
        position = position1, position2
        enemy = Worm(position,'worm head.png')
        self.enemies.add(enemy)
        for i in range(random.randint(1,5)):
            position1 -= 32
            position = position1, position2
            enemy = Worm(position,'worm body.png')
            self.enemies.add(enemy)
        position1 -= 32
        position = position1, position2
        enemy = Worm(position,'worm tail.png')
        self.enemies.add(enemy)
        

    def spawnPopup(self):
        enemy = Popup()
        self.enemies.add(enemy)
    
    def spawnBoss(self):
        self.boss = Boss((200,-200))
        self.enemies.add(self.boss)
        for tentacle in self.boss.tentacles:
            for link in tentacle.links:
                self.enemies.add(link)

    def spawnSafe(self):
        safe = SafeMode()
        self.pickups.add(safe)

    def leftMouseButtonDown(self):
        self.player.shoot(self.bullets)
        sound = pygame.mixer.Sound("data/sounds/shoot.wav")
        sound.set_volume(.25)
        sound.play()

    def rightMouseButtonDown(self):
        self.player.quarantine(self.sprites, self.mines)
        sound = pygame.mixer.Sound("data/sounds/minedeploy.wav")
        sound.set_volume(.25)
        sound.play()

    def quarantine_explode(self):
        for mine in self.mines:
            for enemy in pygame.sprite.spritecollide(mine, self.enemies, False):
                self.enemies.remove(enemy)
            self.mines.remove(mine)
        sound = pygame.mixer.Sound("data/sounds/mineexplosion.wav")
        sound.play()


    def update(self):
    
        for group in self.spriteGroups:
            group.update()
        
        self.hud.update(self)
        
        # Test player-enemy collisions
        for enemy in pygame.sprite.spritecollide(self.player, self.enemies, False):
            if not self.player.invincible:
                self.player.decrease_life()
                self.score -= 100
                sound = pygame.mixer.Sound("data/sounds/xplosion1.wav")
                sound.set_volume(.25)
                sound.play()
                if self.player.lives == 0 :
                    print "game over!"
            
            self.enemies.remove(enemy)
        
        # Test player-pickup collisions
        for pickup in pygame.sprite.spritecollide(self.player, self.pickups, False):
            pickup.on_collision(self.player)
            self.pickups.remove(pickup)
            sound = pygame.mixer.Sound("data/sounds/keypickup.wav")
            sound.play()
        
        # Test enemy-playerBullet collisions
        for enemy, bullets in pygame.sprite.groupcollide(self.enemies, self.bullets, False, False).items():
            for bullet in bullets:
                enemy.health -= 1
                self.bullets.remove(bullet)
                
                if enemy.health <= 0:
                    if enemy.typeofenemy == "boss" and enemy.phase == 1:
                        enemy.go_to_death_phase()
                        for entry in self.enemies:
                            if entry.typeofenemy == "link":
                                self.enemies.remove(entry)
                                
                    elif enemy.typeofenemy == "boss" and enemy.death_frame == 3:
                        self.enemies.remove(enemy)
                        
                    else:
                        self.enemies.remove(enemy)
                        self.player.increase_powerup(5)
                        
                        if enemy.typeofenemy == "worm":
                            self.score += 25
                        elif enemy.typeofenemy == "virus":
                            self.score += 10
                        elif enemy.typeofenemy == "popup":
                            self.score += 15
                            
                        sounds = pygame.mixer.Sound("data/sounds/hit.wav")
                        sounds.play()
            
        # Check enemies offscreen
        for enemy in self.enemies:       
            if enemy.rect.top > SCREEN_HEIGHT:
                self.enemies.remove(enemy)
                self.damage += 1
            if enemy.typeofenemy == "popup":
                if enemy.frame % 20 == 0:
                    self.score -= 1
        
        # Check bullets offscreen
        for bullet in self.bullets:
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)
        
        # Check backgrounds offscreen
        for bkg in self.backgrounds:
            if bkg.rect.top > SCREEN_HEIGHT:
                self.backgrounds.remove(bkg)
        
        if self.frames % 30 == 0:
            self.spawnBkg()
        
        # Spawn more enemies
        if not self.bossMode:
            if self.frames % 50 == 0:
                self.spawnVirus()
                
            if self.frames % 300 == 0:
                self.spawnWorm()
			
            if self.frames % 250 == 0:
                self.spawnPopup()
                
            if self.frames == 1100:
                self.player.destroyAllEnemies = True
                
            if self.frames == 200:
                self.spawnCtrl()
                
            if self.frames == 400:
                self.spawnAlt()
                
            if self.frames == 600:
                self.spawnDel()
                
            if self.frames == 350:
                self.spawnSafe()
        
        if self.frames % 4200 == 0:
            self.music.stop()
            self.music = pygame.mixer.Sound("data/music/Mainloop.wav")
            self.music.play(-1)
            
        # Scroll level
        self.scrollPosition += self.scrollSpeed
        self.scrollPosition = min(self.scrollPosition, self.endPosition)
        
        if self.scrollPosition == self.endPosition and not self.bossMode:
            self.bossMode = True
            self.spawnBoss()
        
        self.frames += 1


    def destroy_all_enemies(self):
        if self.player.destroyAllEnemies:
            sound = pygame.mixer.Sound("data/sounds/destroyall.wav")
            sound.play()
            if not self.bossMode:
                self.enemies.empty()
        self.player.after_destroy_all()
        

    def draw(self, screen):
        for group in self.spriteGroups:
            for sprite in group:
                sprite.draw(screen)
        self.hud.draw(screen, PLAY_WIDTH)
        
        
