import pygame

import entity

class Enemy(entity.Entity):
    def __init__(self, enemyType, position, anims, startAnim):
        super(Enemy, self).__init__(position, anims, startAnim)
        self.typeofenemy = enemyType
        self.health = 1
        self.dead = False
        self.imageOriginal = None
    
    def collideWithBullet(self, bullet):
        if not self.dead:
            self.takeHit(1)
            bullet.kill()
        
    def takeHit(self, damage):
        if not self.dead:
            sound = pygame.mixer.Sound("data/sounds/hit.wav")
            sound.play()
            
            #self.imageOriginal = self.image.copy()
            #self.image.fill((255,0,0,0), None, pygame.BLEND_RGBA_ADD)
            
            self.health -= damage
            if self.health <= 0:
                self.dead = True
                self.changeAnimation('death')
                self.movex = 0
                self.movey = 0
            else:
                self.changeAnimation('takehit')
    
    def update(self):
        super(Enemy, self).update()
        
        if self.imageOriginal and not self.dead:
            self.image = self.imageOriginal
            self.imageOriginal = None
        
        if self.dead and self.anim.done:
            self.kill()
            del self
