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
from boss import Boss
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
        self.startScreen = True
        self.bossMode = False
        self.gameOver = False
        self.winScreen = False
        self.score = 0

        #for keeping track of for the win screen!
        self.numEnemiesAppeared = 0
        self.numEnemiesDestroyed = 0
        self.numViruses = 0
        self.numWorms = 0
        self.numPopUps = 0

        self.playerGroup = pygame.sprite.GroupSingle()
        self.enemies = pygame.sprite.Group()
        self.pickups = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.mines = pygame.sprite.Group()
        self.backgrounds = pygame.sprite.Group()
        
        # sprite groups listed in draw order (lowest sprite get drawn first)
        self.spriteGroups = [self.backgrounds, self.mines, self.pickups, self.bullets, self.enemies, self.playerGroup]
        
        self.hud = Hud()

        pygame.mixer.music.load("data/music/Main.mp3")
        pygame.mixer.music.play()
        
    def spawnWorld(self):
        self.StartScreen = False
        playerPos = (PLAY_WIDTH / 2, SCREEN_HEIGHT - 50)
        pygame.mouse.set_pos(playerPos)
        self.player = Player(self, playerPos)
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
        self.numEnemiesAppeared += 1
        enemy = Virus()
        self.enemies.add(enemy)

    def spawnWorm(self):
        self.numEnemiesAppeared += 1
        position1 = random.randint(195,PLAY_WIDTH-50)
        position2 = 10
        position = position1, position2
        enemy = Worm(position,'head')
        self.enemies.add(enemy)
        for i in range(random.randint(1,5)):
            position1 -= 32
            position = position1, position2
            enemy = Worm(position,'body')
            self.enemies.add(enemy)
        position1 -= 32
        position = position1, position2
        enemy = Worm(position,'tail')
        self.enemies.add(enemy)
        
    def spawnPopup(self):
        self.numEnemiesAppeared += 1
        enemy = Popup()
        while len(pygame.sprite.spritecollide(enemy, self.playerGroup, False)) > 0:
            enemy = Popup()
        self.enemies.add(enemy)
    
    def spawnBoss(self):
        self.numEnemiesAppeared += 1
        pygame.mixer.music.load("data/music/Boss.mp3")
        pygame.mixer.music.play(-1)
        self.boss = Boss((PLAY_WIDTH / 2, -200))
        self.enemies.add(self.boss)
        for tentacle in self.boss.tentacles:
            for link in tentacle.links:
                self.enemies.add(link)

    def spawnSafe(self):
        safe = SafeMode()
        self.pickups.add(safe)

    def leftMouseButtonDown(self):
        self.player.shoot(self.bullets)

    def rightMouseButtonDown(self):
        self.player.quarantine(self.mines)
        sound = pygame.mixer.Sound("data/sounds/minedeploy.wav")
        sound.set_volume(.25)
        sound.play()

    def destroy_all_enemies(self):
        if self.player.destroyAllEnemies:
            self.player.after_destroy_all()
            sound = pygame.mixer.Sound("data/sounds/destroyall.wav")
            sound.play()
            for enemy in self.enemies:
                if enemy.typeofenemy == 'boss' or enemy.typeofenemy == 'link':
                    enemy.takeHit(1)
                else:
                    if enemy.typeofenemy is 'virus':
                        self.numViruses += 1
                    if enemy.typeofenemy is 'worm':
                        self.numWorms += 1
                    if enemy.typeofenemy is 'pop up window':
                        self.numPopUps += 1
                    self.numEnemiesDestroyed += 1
                    enemy.takeHit(enemy.health)
                    
        
        
    def update(self):
    
        for group in self.spriteGroups:
            group.update()
        
        self.hud.update(self)
        
        # Test player-enemy collisions
        for enemy in pygame.sprite.spritecollide(self.player, self.enemies, False):
            if not enemy.dead and not enemy.animName == 'spawn':
                
                if not enemy.typeofenemy == 'boss':
                    enemy.takeHit(enemy.health)
                
                if not self.player.invincible:
                    self.player.decrease_life()
                    self.score -= 100
                    
                if enemy.dead:
                    if enemy.typeofenemy is 'virus':
                        self.numViruses += 1
                        self.numEnemiesDestroyed += 1
                    if enemy.typeofenemy is 'worm':
                        self.numWorms += 1
                        self.numEnemiesDestroyed += 1
                    if enemy.typeofenemy is 'pop up window':
                        self.numPopUps += 1
                        self.numEnemiesDestroyed += 1
        
        # Test player-pickup collisions
        for pickup in pygame.sprite.spritecollide(self.player, self.pickups, False):
            pickup.on_collision(self.player)
            sound = pygame.mixer.Sound("data/sounds/keypickup.wav")
            sound.play()
        
        # Test enemy-playerBullet collisions
        for enemy, bullets in pygame.sprite.groupcollide(self.enemies, self.bullets, False, False).items():
            for bullet in bullets:
                enemy.collideWithBullet(bullet)
                
                if enemy.dead:
                    self.player.increase_powerup(5)
                    
                    if enemy.typeofenemy == "worm":
                        self.numWorms += 1
                        self.numEnemiesDestroyed += 1
                        self.score += 25
                    elif enemy.typeofenemy == "virus":
                        self.numViruses += 1
                        self.numEnemiesDestroyed += 1
                        self.score += 10
                    elif enemy.typeofenemy == "popup":
                        self.numEnemiesDestroyed += 1
                        self.numPopUps += 1
                        self.score += 15
                        
        # Test enemy-mine collisions
        for mine in self.mines:
            if mine.exploding:
                for enemy in pygame.sprite.spritecollide(mine, self.enemies, False):
                    enemy.takeHit(1)
                    if enemy.dead:
                        if enemy.typeofenemy is 'virus':
                            self.numViruses += 1
                            self.numEnemiesDestroyed += 1
                        if enemy.typeofenemy is 'worm':
                            self.numWorms += 1
                            self.numEnemiesDestroyed += 1
                        if enemy.typeofenemy is 'pop up window':
                            self.numPopUps += 1
                            self.numEnemiesDestroyed += 1

                            
            
        # Check enemies offscreen, popups doing damage
        for enemy in self.enemies:       
            if enemy.rect.top > SCREEN_HEIGHT and not enemy.typeofenemy == 'link':
                enemy.kill()
                self.player.decrease_health(1)
                sound = pygame.mixer.Sound("data/sounds/CPUload.wav")
                sound.play()
                               
            if enemy.typeofenemy == "popup":
                if enemy.frame % 20 == 0:
                    self.score -= 1
        
        # Check bullets offscreen
        for bullet in self.bullets:
            if bullet.rect.bottom < 0:
                bullet.kill()
        
        # Check backgrounds offscreen
        for bkg in self.backgrounds:
            if bkg.rect.top > SCREEN_HEIGHT:
                bkg.kill()
        
        if self.frames % 32 == 0:
            for i in range(random.randint(0, 4)):
                self.spawnBkg()
        
        # Spawn more enemies
        if not self.bossMode:
            if self.frames % 50 == 0:
                self.spawnVirus()
                
            if self.frames % 300 == 0:
                self.spawnWorm()
			
            if self.frames % 250 == 0:
                self.spawnPopup()
                
            if self.frames % 1100 == 0:
                self.player.destroyAllEnemies = True
                
            if self.frames % 200 == 0:
                self.spawnCtrl()
                
            if self.frames % 400 == 0:
                self.spawnAlt()
                
            if self.frames % 600 == 0:
                self.spawnDel()
                
            if self.frames % 350 == 0:
                self.spawnSafe()
        
        # Check if main music has ended, and loop music should start
        if self.frames == MUSIC_LENGTH_MAIN:
            pygame.mixer.music.load("data/music/Mainloop.mp3")
            pygame.mixer.music.play(-1)
        elif self.frames == FRAMES_UNTIL_BOSS + MUSIC_LENGTH_BOSS:
            pygame.mixer.music.load("data/music/Bossloop.mp3")
            pygame.mixer.music.play(-1)
                
                
        # Check gameover
        if self.player.lives == 0:
            self.gameOver = True
        
        # Check win screen!
        if self.bossMode and self.boss.dead and self.boss.anim.done:
            if not self.winScreen:
                self.numEnemiesDestroyed += 1
                self.winScreen = True
            
        # Scroll level
        self.scrollPosition += self.scrollSpeed
        self.scrollPosition = min(self.scrollPosition, self.endPosition)
        
        if self.scrollPosition == self.endPosition and not self.bossMode:
            self.bossMode = True
            self.spawnBoss()
        
        self.frames += 1
        

    def draw(self, screen):
        for group in self.spriteGroups:
            for sprite in group:
                sprite.draw(screen)
        self.hud.draw(screen, PLAY_WIDTH)
        
        
