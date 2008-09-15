#!/usr/bin/env python

import pygame, random, threading
import entity
from pygame.locals import *
from constants import *

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

class Bkg(entity.Entity):
    def __init__(self):
        #options: disc.png, folder.png, game icon.png, game icon 2.png, monkey exe.png, mp3.png, my computer.png, notepad.png, world icon.png
        i = random.randint(1,9)
        if i == 1:
            self.image = 'disc.png'
        elif i == 2:
            self.image = 'folder.png'
        elif i == 3:
            self.image = 'game icon.png'
        elif i == 4:
            self.image = 'game icon 2.png'
        elif i == 5:
            self.image = 'monkey exe.png'
        elif i == 6:
            self.image = 'mp3.png'
        elif i == 7:
            self.image = 'my computer.png'
        elif i == 8:
            self.image = 'notepad.png'
        elif i == 9:
            self.image = 'world icon.png'
        self.position = random.randint(10,PLAY_WIDTH-32), random.randint(10,PLAY_WIDTH-32)
        super(Bkg, self).__init__(self.position, self.image)
        
        t = threading.Timer(5, self.deleter)
        t.start()
        
    def deleter(self):
        self.kill()
        del(self)


