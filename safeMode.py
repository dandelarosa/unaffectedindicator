import pygame, random
import entity, player, threading
from pygame.locals import *

class SafeMode(entity.StaticEntity):
    def __init__(self):
        pos = random.randint(10,450),random.randint(10,450)
        super(SafeMode, self).__init__(pos, "shield.png")
        self.typeofenemy = "cad"
        t = threading.Timer(5, self.delete_pickup)
        t.start()
        
    def set_position(self,pos):
        entity.Entity.set_position(self,pos)
        
    def update(self):
        super(SafeMode,self).update()
        
    def on_collision(self, player1):
        player1.init_safe_mode(5.0)
        self.delete_pickup()
		
    def delete_pickup(self):
        self.kill()
        del self
