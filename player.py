#!/usr/bin/env python

import pygame, threading
import entity
from playerBullet import PlayerBullet
from quarantineMine import QuarantineMine
from pygame.locals import *

class Player(entity.Entity):
    
    def __init__(self, world, pos):
        self.bullets = []
        self.respawnPos = pos
        self.gameWorld = world
        entity.Entity.__init__(self, pos, "player icon.png", 32)
        pygame.mouse.set_visible(False)
        self.health = 100
        self.powerup = 0
        self.lives = 3
        self.mines = 3
        self.hasCtrl = False
        self.hasAlt = False
        self.hasDel = False
        self.invincible = False
        self.quarantineSet = False
        self.destroyAllEnemies = False
        
    def set_position(self,pos):
        entity.Entity.set_position(self,pos)
        
    def update(self):
        super(Player, self).update()
        pos = pygame.mouse.get_pos()
        self.set_position(pos)
    
    def shoot(self, bullets, sprites):
        b = PlayerBullet(pygame.mouse.get_pos())
        self.bullets.append(b)
        bullets.add(b)
        sprites.add(b)

    def collected_ctrlAltDel(self, cadId):
        if cadId is 1:
            self.hasCtrl = True
        elif cadId is 2:
            self.hasAlt = True
        elif cadId is 3:
            self.hasDel = True
        if self.hasCtrl and self.hasAlt and self.hasDel:
            self.increase_health(50)
        
    def init_safe_mode(self, time):
        if not self.invincible:
            self.invincible = True
            t = threading.Timer(time, self.end_safe_mode)
            t.start()
        
    def end_safe_mode(self):
        self.invincible = False
    
    def decrease_life(self):
        self.lives -= 1
        self.set_position(self.respawnPos)
        self.init_safe_mode(2.0)
    
    def increase_health(self, amount):
        self.health += amount
    
    def decrease_health(self, amount):
        if not self.invincible:
            if (self.health - amount) > 0:
                self.health -= amount
            elif (self.health - amount) <= 0:
                self.decrease_life()
                self.health = 100

    def increase_powerup(self, amount):
        self.powerup += amount
        if self.powerup is 100:
            self.destroyAllEnemies = True

    def quarantine(self, sprites, mines):
        if not self.quarantineSet and self.mines > 0:
            mine = QuarantineMine(self, pygame.mouse.get_pos())
            sprites.add(mine)
            mines.add(mine)
            self.quarantineSet = True
            self.mines -= 1

    def quarantine_explode(self):
         self.quarantineSet = False
         self.gameWorld.quarantine_explode()

    def after_destroy_all(self):
        self.powerup = 0
        self.destroyAllEnemies = False
        
