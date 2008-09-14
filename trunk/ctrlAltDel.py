#!/usr/bin/env python

import pygame, random, threading
import entity
from pygame.locals import *

class Ctrl(entity.Entity):
    def __init__(self):
        
        self.position = random.randint(10,450), random.randint(10,450)
        super(Ctrl, self).__init__(self.position, 'ctrl button.png')
        self.id = 1
        self.lifetime = 1
        self.typeofenemy = "cad"
        t = threading.Timer(2.5, self.delete_pickup)
        t.start()

		
    def update(self):
        super(Ctrl, self).update()
        self.lifetime += 1
        
    def set_position(self,pos):
        entity.Entity.set_position(self,pos)

    def on_collision(self, player1):
        player1.collected_ctrlAltDel(self.id);

    def delete_pickup(self):
        self.kill()
        del(self)
        

class Alt(entity.Entity):
    def __init__(self):
        
        self.position = random.randint(10,450), random.randint(10,450)
        super(Alt, self).__init__(self.position, 'alt button.png')
        self.id = 2
        self.lifetime = 1
        self.typeofenemy = "cad"
        t = threading.Timer(2.5, self.delete_pickup)
        t.start()


    def update(self):
        super(Alt, self).update()
        self.lifetime += 1
        
    def set_position(self,pos):
        entity.Entity.set_position(self,pos)

    def on_collision(self, player1):
        player1.collected_ctrlAltDel(self.id)

    def delete_pickup(self):
        self.kill()
        del(self)
        

class Del(entity.Entity):
    def __init__(self):
        
        self.position = random.randint(10,450), random.randint(10,450)
        super(Del, self).__init__(self.position, 'del button.png')
        self.id = 3
        self.lifetime = 1
        self.typeofenemy = "cad"
        t = threading.Timer(2.5, self.delete_pickup)
        t.start()


    def update(self):
        super(Del, self).update()
        self.lifetime += 1

    def set_position(self,pos):
        entity.Entity.set_position(self,pos)

    def on_collision(self, player1):
        player1.collected_ctrlAltDel(self.id)

    def delete_pickup(self):
        self.kill()
        del(self)




