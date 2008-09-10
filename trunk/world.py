import pygame
import random
import sys

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

        self.sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.hud = Hud()

        
    def spawnWorld(self):
        self.player = Player((SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50))
        self.sprites.add(self.player)

        self.hud.createHudElements()
        self.frames = 1

        self.scrollPosition = 0
        self.scrollSpeed = 3

    def spawnVirus(self):
        enemy = Virus()
        self.sprites.add(enemy)
        self.enemies.add(enemy)

    def spawnWorm(self):
        enemy = Worm()
        self.sprites.add(enemy)
        self.enemies.add(enemy)

    def spawnPopup(self):
        enemy = Popup((random.randint(0, PLAY_WIDTH), -50))
        self.sprites.add(enemy)
        self.enemies.add(enemy)

    def leftMouseButtonDown(self):
        self.player.shoot()
        

    def update(self):
        self.sprites.update()
        self.hud.update(self)
        
        for enemy in pygame.sprite.spritecollide(self.player, self.enemies, False):
            print "player collided with enemy"
            self.sprites.remove(enemy)
            self.enemies.remove(enemy)
            self.player.decrease_life()
            if self.player.lives == 0 :
                print "Game over"
                sys.exit()
        
        for enemy in self.enemies:       
            if enemy.rect.top > SCREEN_HEIGHT:
                self.sprites.remove(enemy)
                self.damage += 1
        
        if self.frames % 50 == 0:
            self.spawnVirus()
            
        if self.frames % 300 == 0:
            self.spawnWorm()
			
        if self.frames % 250 == 0:
            self.spawnPopup()

        self.scrollPosition += self.scrollSpeed
        self.scrollPosition = min(self.scrollPosition, self.endPosition)

        self.frames += 1

    def draw(self, screen):
        self.sprites.draw(screen)

        self.playSurface.fill((255, 255, 255))
        self.hudSurface.fill((100, 100, 255))

        self.sprites.draw(self.playSurface)
        self.hud.draw(self.hudSurface)
        screen.blit(self.playSurface, (0, 0))
        screen.blit(self.hudSurface, (PLAY_WIDTH, 0))
        
