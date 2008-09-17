import pygame, threading
import entity
from animation import Animation, ResizeAnimation, ColorFadeAnimation

class QuarantineMine(entity.Entity):
    def __init__(self, pos):
        self.position = pos
        self.exploding = False
        
        anims = {
            'idle': Animation("quarintine mine.png"),
            'explode': ResizeAnimation("quarintine explosion.png", 20, (0.1, 0.1), (1, 1), (0.5, 0.5)),
            'done': ColorFadeAnimation("quarintine explosion.png", 5, 0, (255,255,255,0))
            }
        
        super(QuarantineMine, self).__init__(self.position, anims, 'idle')
        
        t = threading.Timer(3.75, self.explode)
        t.start()

    def update(self):
        super(QuarantineMine, self).update()
        
        if self.animName == 'explode' and self.anim.done:
            self.changeAnimation('done')
            self.exploding = False
            
        elif self.animName == 'done' and self.anim.done:
            self.kill()

    def explode(self):
        self.changeAnimation('explode')
        self.rect.center = self.position
        sound = pygame.mixer.Sound("data/sounds/mineexplosion.wav")
        sound.play()
        self.exploding = True
        
