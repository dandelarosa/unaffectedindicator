import pygame
import random
import sys

from ctrlAltDel import *
from virus import Virus, DoubleVirus, TripleVirus
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

        # this is normal difficulty by default
        # easy would prolly be .7ish and hard.. 1.3 or so?
        self.difficulty = 1 
        self.spawnFreq = 10
        self.scrollPosition = 0
        self.scrollSpeed = 3
        self.endPosition = FRAMES_UNTIL_BOSS * self.scrollSpeed
        self.startScreen = True
        self.helpScreen = False
        self.difficultyScreen = False
        self.bossMode = False
        self.gameOver = False
        self.winScreen = False
        self.score = 0
	self.call_popcorn = 0
        self.boss_music=False

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
        self.spawnBkg()
        
        # sprite groups listed in draw order (lowest sprite get drawn first)
        self.spriteGroups = [self.backgrounds, self.mines, self.pickups, self.bullets, self.enemies, self.playerGroup]
        
        self.hud = Hud()


        
    def spawnWorld(self):
        self.StartScreen = False
        playerPos = (PLAY_WIDTH / 2, SCREEN_HEIGHT - 50)
        pygame.mouse.set_pos(playerPos)
        self.player = Player(self, playerPos)
        self.playerGroup.add(self.player)


        pygame.mixer.music.load("data/music/Main.mp3")
        pygame.mixer.music.play()
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
        
    def spawnVirus(self, position):
        self.numEnemiesAppeared += 1
        enemy = Virus(position)
        self.enemies.add(enemy)

    def spawnDoubleVirus(self, position):
        self.numEnemiesAppeared += 1
        enemy = DoubleVirus(self, position)
        self.enemies.add(enemy)
        
    def spawnTripleVirus(self):
        self.numEnemiesAppeared += 1
        enemy = TripleVirus(self)
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
	self.boss_music=True
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

    def enemy_popcorn(self):
            if len(self.enemy_list)==1:
		self.call_popcorn=0
            else:
                self.enemy_list[1].takeHit(self.enemy_list[1].health)
		self.enemy_list.remove(self.enemy_list[1])

    def destroy_all_enemies(self):
        self.enemy_list=[0]
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
                    self.enemy_list.insert(1,enemy)
                    #enemy.takeHit(enemy.health)
	    self.call_popcorn=self.frames
        
        
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
                self.score -= 10
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
        
        if self.frames % 360 == 0:
            self.spawnBkg()

        if self.spawnFreq is not 1:
            if self.frames % (500 / self.difficulty) == 0:
                if self.spawnFreq <= 1:
                    self.spawnFreq = 1
                elif self.spawnFreq > 1:
                    self.spawnFreq -= 1
        
        # Spawn more enemies
        baseSpawnRate = (self.spawnFreq * 5 + random.randint(1, 5))
        if not self.bossMode:
            if self.frames % baseSpawnRate == 0:
                self.spawnTripleVirus()
                
            if self.frames % (baseSpawnRate * 6) == 0:
                self.spawnWorm()
			
            if self.frames % (baseSpawnRate * 5) == 0:
                self.spawnPopup()
                
            if self.frames % (baseSpawnRate * 21) == 0:
                self.player.destroyAllEnemies = True
                
            if self.frames % (baseSpawnRate * 4) == 0:
                self.spawnCtrl()
                
            if self.frames % (baseSpawnRate * 8) == 0:
                self.spawnAlt()
                
            if self.frames % (baseSpawnRate * 12) == 0:
                self.spawnDel()
                
            if self.frames % (baseSpawnRate * 7) == 0:
                self.spawnSafe()
                
        # Check if main music has ended, and loop music should start
        if not pygame.mixer.music.get_busy():
          if not self.boss_music:
              pygame.mixer.music.load("data/music/Mainloop.mp3")
              pygame.mixer.music.play(-1)
          elif self.frames == FRAMES_UNTIL_BOSS + MUSIC_LENGTH_BOSS:
              pygame.mixer.music.load("data/music/Bossloop.mp3")
              pygame.mixer.music.play(-1)
	    
	#Check for calling enemy_popcorn
	if self.call_popcorn != 0 and self.call_popcorn<self.frames-10:
	       self.enemy_popcorn()
                
                
        # Check gameover
        if self.player.lives == 0:
            self.gameOver = True
            pygame.mixer.music.stop()
        
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
