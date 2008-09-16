import pygame

import entity

class Enemy(entity.Entity):
    def __init__(self, enemyType, position, anims, startAnim):
        super(Enemy, self).__init__(position, anims, startAnim)
        self.typeofenemy = enemyType
        self.health = 1
        self.dead = False
    
    def collideWithBullet(self, bullet):
        if not self.dead:
            self.takeHit(1)
            bullet.kill()
        
    def takeHit(self, damage):
        if not self.dead:
            sound = pygame.mixer.Sound("data/sounds/hit.wav")
            sound.play()
            
            self.health -= damage
            if self.health <= 0:
                self.dead = True
                self.changeAnimation('death')
                sound = pygame.mixer.Sound("data/sounds/xplosion1.wav")
                sound.set_volume(.5)
                sound.play()
    
    def update(self):
        super(Enemy, self).update()
        if self.dead and self.anim.done:
            self.kill()
            del self
