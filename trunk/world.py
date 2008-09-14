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
from constants import *

class World (object):
    
    def __init__(self):
        super(World, self).__init__()

        self.frames = 1

        self.playSurface = pygame.Surface((PLAY_WIDTH, SCREEN_HEIGHT))
        self.hudSurface = pygame.Surface((HUD_WIDTH, SCREEN_HEIGHT))

        self.scrollPosition = 0
        self.scrollSpeed = 3
        self.endPosition = 1000

        self.damage = 0
        self.lives = 3
        self.score = 0

        self.sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.mines = pygame.sprite.Group()
        self.hud = Hud()

    
        self.music = pygame.mixer.Sound("data/music/Main.wav")
        self.music.play()
        
    def spawnWorld(self):
        self.player = Player(self, (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50))
        self.sprites.add(self.player)

        self.hud.createHudElements()
        self.frames = 1

        self.scrollPosition = 0
        self.scrollSpeed = 3

    def spawnCtrl(self):
        ctrl = Ctrl()
        self.sprites.add(ctrl)
        self.enemies.add(ctrl)
        
    def spawnAlt(self):
        alt = Alt()
        self.sprites.add(alt)
        self.enemies.add(alt)
    
    def spawnDel(self):
        d = Del()
        self.sprites.add(d)
        self.enemies.add(d)
        
    def spawnVirus(self):
        enemy = Virus()
        self.sprites.add(enemy)
        self.enemies.add(enemy)

    def spawnWorm(self):
        enemy = Worm()
        self.sprites.add(enemy)
        self.enemies.add(enemy)

    def spawnPopup(self):
        enemy = Popup()
        self.sprites.add(enemy)
        self.enemies.add(enemy)

    def leftMouseButtonDown(self):
        self.player.shoot(self.bullets, self.sprites)
        sound = pygame.mixer.Sound("data/sounds/shoot.wav")
        sound.set_volume(.5)
        sound.play()

    def rightMouseButtonDown(self):
        self.player.quarantine(self.sprites, self.mines)

    def quarantine_explode(self):
        for mine in self.mines:
            mine.rect.inflate(10, 10)
            for enemy in self.enemies:
                if pygame.sprite.collide_rect(mine, enemy):
                    self.enemies.remove(enemy)
                    self.sprites.remove(enemy)
            self.sprites.remove(mine)
            self.mines.remove(mine)

    def update(self):
    
        self.sprites.update()
        self.hud.update(self)
        
        # Test player-enemy collisions
        for enemy in pygame.sprite.spritecollide(self.player, self.enemies, False):
            
            if enemy.typeofenemy == "cad":
                enemy.on_collision(self.player)
            else:
                self.player.decrease_life()
                self.lives -= 1
                self.score -= 100
                if self.player.lives == 0 :
                    print "game over!"
            self.sprites.remove(enemy)
            self.enemies.remove(enemy)


        
        
        
        # Test enemy-playerBullet collisions
        for enemy, bullets in pygame.sprite.groupcollide(self.enemies, self.bullets, False, False).items():
            for bullet in bullets:
                #enemy.collideBullet(bullet)
                self.sprites.remove(enemy)
                self.sprites.remove(bullet)
                self.enemies.remove(enemy)
                self.bullets.remove(bullet)
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
                self.sprites.remove(enemy)
                self.enemies.remove(enemy)
                self.damage += 1
            if enemy.typeofenemy == "popup":
                if enemy.lifetime > 20:
                    enemy.lifetime = 0
                    self.score -= 1
        
        # Check bullets offscreen
        for bullet in self.bullets:
            if bullet.rect.top < 0:
                self.sprites.remove(bullet)
                self.bullets.remove(bullet)
        
        # Spawn more enemies
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
        
        if self.frames % 4200 == 0:
            self.music.stop()
            self.music = pygame.mixer.Sound("data/music/Mainloop.wav")
            self.music.play(-1)
        # Scroll level
        self.scrollPosition += self.scrollSpeed
        self.scrollPosition = min(self.scrollPosition, self.endPosition)
        
        self.frames += 1


    def destroy_all_enemies(self):
        if self.player.destroyAllEnemies:
            sound = pygame.mixer.Sound("data/sounds/xplosion1.wav")
            sound.play()
            for spr in self.enemies:
                if self.player != spr:
                    self.enemies.remove(spr)
                    self.sprites.remove(spr)
        self.player.after_destroy_all()
        

    def draw(self, screen):
        self.playSurface.fill((255, 255, 255))
        self.hudSurface.fill((100, 100, 255))

        self.sprites.draw(self.playSurface)
        self.hud.draw(self.hudSurface)
        
        screen.blit(self.playSurface, (0, 0))
        screen.blit(self.hudSurface, (PLAY_WIDTH, 0))
        
