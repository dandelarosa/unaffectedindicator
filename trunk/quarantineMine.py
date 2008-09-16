import pygame, threading
import entity
from animation import Animation
from pygame.locals import *

class QuarantineMine(entity.Entity):
    def __init__(self,player,pos):
        self.player = player
        self.position = pos
        anims = {'idle': Animation("quarintine mine.png"), 'death': Animation("quarintine explosion.png",100)}
        super(QuarantineMine, self).__init__(self.position, anims, 'idle')
        t = threading.Timer(3.75, self.explode)
        t.start()


    def explode(self):
        self.changeAnimation('death')
        self.rect = self.rect.inflate(100, 100)
        self.player.quarantine_explode()
        print "boom"
